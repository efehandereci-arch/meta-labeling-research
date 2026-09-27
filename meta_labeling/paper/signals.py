"""Canlı karar: araştırmadaki long meta-labeling overlay'in bugünkü (son bar) hali.

``decide`` yalnızca verilen veriyi (son barı "bugün") kullanır, gelecek veri yoktur. Yeni bir CUSUM
olayı varsa meta-model, bugüne kadar etiketi KAPANMIŞ olaylarla eğitilir:

* walk-forward OOS olasılıkları -> isotonic kalibratör + conformal skorlar (``overlay.py`` ile aynı)
* tüm kapanmış olaylarla eğitilen son model -> bugünkü olayın P(Y=1)'i
* m = clip(conformal Kelly f, 0, 1); ısınmada / yetersiz veride görüş yok (NaN -> tam long)

Olay yaşam döngüsü (``event_active``): olay t0'da açılır, kapanış yolunda ±k·σ bariyerine ilk
temasta ya da ``max_holding_bars`` sonra kapanır; araştırmadaki [t0, t1) karar penceresiyle aynı.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, replace

import numpy as np
import pandas as pd
from sklearn.base import clone

from ..model import positive_class_proba
from ..research.conformal import conformal_kelly
from ..research.execution import adv_value
from ..research.modeling import (
    EventDataset,
    _fit_calibrator,
    build_event_dataset,
    build_market_state,
    calibrate_walk_forward,
    make_estimator,
    sample_candidate_events,
    sample_weight,
    walk_forward,
)
from ..research.overlay import market_features, track_record_features, trend_features, vol_cap_series
from ..research.settings import ResearchConfig

log = logging.getLogger("meta_labeling.paper")
FAR = pd.Timestamp("2200-01-01")


@dataclass
class Decision:
    date: pd.Timestamp
    vol_cap: float
    sigma: float                 # σ_t (EWMA log-getiri std) -> olay bariyer birimi
    new_event: bool
    m: float = float("nan")      # yeni olayın maruziyet önerisi (NaN: görüş yok)
    p: float = float("nan")      # kalibre P(Y=1)
    mu: float = float("nan")     # beklenen net işlem getirisi
    note: str = ""


def overlay_config(cfg: ResearchConfig) -> ResearchConfig:
    return replace(cfg, primary=replace(cfg.primary, kind="long"),
                   meta_model=replace(cfg.meta_model, use_side_feature=False))


def event_active(adj_close: pd.Series, t0: pd.Timestamp, trgt: float, cfg: ResearchConfig) -> bool:
    """Olay bugünün (son bar) kararında hâlâ aktif mi? Bariyerler araştırmadakiyle aynı (kapanış yolu)."""
    b = cfg.barriers
    idx = adj_close.index
    if t0 not in idx:
        return False
    i0 = idx.get_loc(t0)
    n_since = len(idx) - 1 - i0
    if n_since >= b.max_holding_bars:
        return False
    path = adj_close.iloc[i0 + 1:] / adj_close.iloc[i0] - 1.0
    if b.pt_mult > 0 and (path >= b.pt_mult * trgt).any():
        return False
    if b.sl_mult > 0 and (path <= -b.sl_mult * trgt).any():
        return False
    return True


def decide(adj: pd.DataFrame, market: pd.DataFrame | None, cfg: ResearchConfig, min_history_bars: int) -> Decision:
    ocfg = overlay_config(cfg)
    oc = ocfg.overlay
    today = adj.index[-1]
    ms = build_market_state(adj, ocfg, adv_value(adj, ocfg.costs.adv_window))
    vcap = float(vol_cap_series(ms.vol, oc.vol_cap_min_history).iloc[-1]) if oc.vol_cap else 1.0
    sigma = float(ms.vol.iloc[-1]) if pd.notna(ms.vol.iloc[-1]) else float("nan")
    if len(adj) < min_history_bars:
        return Decision(today, vcap, sigma, False, note=f"kısa geçmiş ({len(adj)} bar)")
    extra = [trend_features(adj)] if oc.trend_features else []
    if market is not None:
        extra.append(market_features(market.loc[:today], adj.index))
    if extra:
        ms.features = pd.concat([ms.features, *extra], axis=1)
    t_events = sample_candidate_events(ms, ocfg)
    if today not in t_events:
        return Decision(today, vcap, sigma, False)

    dec = Decision(today, vcap, sigma, True)
    try:
        ds = build_event_dataset(ms, ocfg, t_events[t_events < today])
    except ValueError as exc:
        dec.note = f"etiketli olay yok ({exc})"
        return dec
    # güvenlik: eğitimde yalnızca bilgisi bugüne kadar tamamlanmış etiketler
    ds = EventDataset(ds.events.loc[ds.events["label_end"] <= today], ds.X.loc[ds.events["label_end"] <= today], ms)
    today_row = pd.DataFrame({"label_end": [FAR], "bin": [np.nan], "exec_net_ret": [np.nan], "trgt": [sigma]},
                             index=pd.DatetimeIndex([today]))
    tr_all = track_record_features(pd.concat([ds.events[["label_end", "bin", "exec_net_ret", "trgt"]], today_row]),
                                   oc.track_record_window)
    X = ds.X.join(tr_all)
    valid = X.notna().all(axis=1)
    ds = EventDataset(ds.events.loc[valid].copy(), X.loc[valid], ms)
    x_today = ms.features.loc[[today]].join(tr_all.loc[[today]])[ds.X.columns]
    if x_today.isna().any(axis=None):
        dec.note = "eksik öznitelik: " + ", ".join(x_today.columns[x_today.isna().iloc[0]])
        return dec
    if len(ds.events) < ocfg.cv.min_train_events + 50 or ds.y.nunique() < 2:
        dec.note = f"yetersiz eğitim verisi ({len(ds.events)} olay)"
        return dec

    oos = walk_forward(ds, ocfg)
    cal = calibrate_walk_forward(oos, ds.y, ds.label_end, "isotonic", ocfg.calibration.min_history)
    model = clone(make_estimator(ds, ocfg)).fit(
        ds.X, ds.y, sample_weight=sample_weight(ds, ocfg.meta_model.weighting).to_numpy())
    p_raw = float(positive_class_proba(model, x_today)[0])
    hist = oos.proba.notna()
    if hist.sum() >= ocfg.calibration.min_history and ds.y[hist].nunique() == 2:
        p_today = float(_fit_calibrator("isotonic", oos.proba[hist].to_numpy(), ds.y[hist].to_numpy())(np.array([p_raw]))[0])
    else:
        p_today = p_raw

    ev = ds.events.loc[hist, ["label_end", "exec_net_ret", "trgt"]]
    ev = pd.concat([ev, today_row[["label_end", "exec_net_ret", "trgt"]]])
    p_series = pd.concat([cal.proba.reindex(ev.index[:-1]).fillna(oos.proba.reindex(ev.index[:-1])),
                          pd.Series([p_today], index=[today])])
    ck = conformal_kelly(p_series, ev, ocfg.sizing.conformal, cap=1.0, threshold=-1.0, dial=False)
    dec.p, dec.mu = p_today, float(ck.mu.loc[today])
    if pd.notna(ck.q_eff.loc[today]) and pd.notna(ck.mu.loc[today]):
        dec.m = float(ck.size_undialed.loc[today])
    else:
        dec.note = "conformal ısınma"
    return dec
