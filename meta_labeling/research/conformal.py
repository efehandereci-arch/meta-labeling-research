"""Conformal Kelly: conformal tahmin aralığını fraksiyonel Kelly'nin ölçeği olarak kullanmak.

Kaynak: R. J. Ryan, "Conformal Kelly: Conformal Prediction Intervals as the Scale
in Fractional Kelly Position Sizing", arXiv:2608.01494 (2026).

Mevcut ``kelly`` yöntemi (``modeling.position_sizes``) kazanç/kayıp oranını
bariyerlerden okur: ``b = pt / sl``. Gerçekte işlemlerin bir kısmı dikey
bariyerde, boşluklu (gap) açılışlarda ve maliyet sonrası kapanır; gerçekleşen
kazanç/kayıp dağılımı ``±k·σ`` değildir. Bu modül Kelly'nin iki girdisini de
gerçekleşmiş işlemlerden, **yalnızca karar anında kapanmış olanlardan** tahmin eder:

1. Beklenen getiri (pay):
       μ̂_i = p_i · W̄ − (1 − p_i) · L̄
   W̄ / L̄: karar anına kadar kapanmış kârlı / zararlı işlemlerin ortalama net
   getirisi (genişleyen ortalama). p_i kalibre edilmiş olmalıdır; dengelenmiş
   (class_weight="balanced") ham olasılık μ̂'yi yanlı yapar.

2. Ölçek (payda): Uygunsuzluk (nonconformity) skoru s_j = |x_j − μ̂_j|. Karar
   anında kapanmış son ``window`` skorun (1 − α) conformal kantili q_roll, tüm
   kapanmış skorların genişleyen kantili q_anchor'a geometrik olarak çekilir:
       q_eff = q_roll^(1−λ) · q_anchor^λ,     σ̂ = q_eff / Φ⁻¹(1 − α/2)
   Makalenin ana bulgusu: ölçek YAVAŞ olmalı. Rejime hızlı uyum sağlayan her
   varyant (ACI, ağırlıklı kalibrasyon, asimetrik aralık) büyümeyi düşürdü;
   Kelly paydasına giren gürültülü σ̂ doğrusal olmayan biçimde cezalandırılır.
   Kantil, standart sapmaya göre uç değerlere dayanıklıdır (sınırlı etki fonksiyonu).

3. Pozisyon:  f_i = κ · μ̂_i / σ̂_i²,  [0, max_position] aralığına kırpılır.

4. Drawdown kadranı (isteğe bağlı): Son ``dial_window`` kapanmış işlemde alt
   bariyer ihlali oranı d (x_j < μ̂_j − q_j), referans α/2'yi aştıkça tüm kitap
   küçültülür:  m = clip(1 − β (d − α/2) / (α/2), floor, 1).  Makalede bu
   kadran büyümeyi değil drawdown'ı iyileştirdi ve placebo kontrolünü geçti;
   burada da ``session.position_sizing`` aynı kontrolleri (dairesel kaydırma
   placebo'su + sabit kaldıraç kontrolü) raporlar.

Makaleden bilinçli sapmalar:

* Skor birimi varsayılan olarak ``vol``: x_j = r_j / σ_{t0,j}. Triple Barrier
  bariyerleri zaten ``k·σ_t`` ile ölçeklendiği için işlem getirileri doğal
  olarak σ biriminde; ham birimde σ̂ o anki volatiliteden bağımsız kalır ve
  yüksek volatilitede aşırı bahis yapılır. ``score_units: raw`` makaledeki
  düz mutlak artığı kullanır. Not: makale (çok varlıklı ETF kesitinde)
  volatiliteyle ölçeklenmiş skorların 3.3 puan kaybettirdiğini raporlar.
* Gauss sabiti tutarlı: z = Φ⁻¹(1 − α/2) (makale α=0.25 için yanlışlıkla
  Φ⁻¹(0.90) kullandığını açıklıyor).
* Kantil, sonlu örneklem conformal indeksiyle alınır: ⌈(n+1)(1−α)⌉ / n.

Nedensellik: Bir işlemin skoru, ödeme istatistiği ve kadran göstergesi ancak
``label_end < t0_i`` olduğunda i kararına girer (``calibrate_walk_forward`` ile
aynı katı eşitsizlik). Finansal getiriler değiştirilebilir (exchangeable)
olmadığından kapsama bir GARANTİ değil, ölçülen bir özelliktir; rapor gerçekleşen
kapsamayı nominal değerle birlikte verir.
"""

from __future__ import annotations

import math
from collections import deque
from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy.special import ndtri

from .settings import ConformalKellySettings


@dataclass
class ConformalKellyResult:
    """Olay bazında (t0 indeksli) conformal Kelly çıktıları."""

    size: pd.Series            # kadran uygulanmış büyüklük (dial=False ise size_undialed ile aynı)
    size_undialed: pd.Series   # kadransız büyüklük, [0, cap]
    mu: pd.Series              # beklenen net işlem getirisi (getiri biriminde)
    sigma: pd.Series           # conformal ölçek σ̂ (getiri biriminde)
    q_eff: pd.Series           # conformal yarı genişlik (skor biriminde)
    dial: pd.Series            # drawdown kadranı çarpanı [floor, 1]
    covered: pd.Series         # 1/0: gerçekleşen getiri aralıkta mı (NaN: aralık yoktu)
    lower_break: pd.Series     # 1/0: alt sınır ihlali
    upper_break: pd.Series     # 1/0: üst sınır ihlali
    n_scores: pd.Series        # karar anında kullanılabilen skor sayısı
    payoff_ratio: pd.Series    # karar anındaki ampirik kazanç/kayıp oranı b̂ = W̄ / L̄
    alpha: float

    def coverage_summary(self) -> dict[str, float]:
        """Gerçekleşen kapsama (nominal 1-α) ve tek taraflı ihlal oranları (referans α/2)."""
        c = self.covered.dropna()
        n = len(c)
        rate = float(c.mean()) if n else float("nan")
        return {
            "Aralıklı olay": n,
            "Nominal kapsama": 1.0 - self.alpha,
            "Gerçekleşen kapsama": rate,
            # iid varsayımıyla standart hata; örtüşen etiketlerde gerçek belirsizlik daha büyüktür
            "Std. hata (iid)": float(math.sqrt(rate * (1 - rate) / n)) if n else float("nan"),
            "Alt ihlal oranı": float(self.lower_break.dropna().mean()) if n else float("nan"),
            "Üst ihlal oranı": float(self.upper_break.dropna().mean()) if n else float("nan"),
            "Referans (α/2)": self.alpha / 2.0,
            "Isınma (aralıksız) olay": int(self.q_eff.isna().sum()),
            "Ort. kadran": float(self.dial.mean()) if len(self.dial) else float("nan"),
            "Son ampirik b̂ = W̄/L̄": float(self.payoff_ratio.dropna().iloc[-1])
            if self.payoff_ratio.notna().any() else float("nan"),
        }


def conformal_quantile(scores: np.ndarray, alpha: float) -> float:
    """Sonlu örneklem split-conformal kantili: ⌈(n+1)(1−α)⌉'inci en küçük skor (n'de kırpılır)."""
    n = len(scores)
    if n == 0:
        return float("nan")
    k = min(n, int(math.ceil((n + 1) * (1.0 - alpha))))
    return float(np.partition(scores, k - 1)[k - 1])


def conformal_kelly(
    proba: pd.Series,
    events: pd.DataFrame,
    cs: ConformalKellySettings,
    *,
    cap: float,
    threshold: float,
    dial: bool,
) -> ConformalKellyResult:
    """Olay listesi üzerinde nedensel conformal Kelly büyüklükleri.

    ``events`` sütunları: ``trgt`` (σ_t0), ``label_end`` (etiket bilgisinin
    tamamlandığı bar), ``exec_net_ret`` (birim büyüklükte net işlem getirisi).
    Gerçekleşen getiriler yalnızca ``label_end < t0_i`` olan işlemler için,
    i'den SONRA kullanılır; ``proba`` NaN olan olaylar büyüklük almaz ama
    kapanınca ödeme istatistiğine katılır (getirileri modelden bağımsızdır).
    """
    ev = events.sort_index()
    t0 = ev.index.to_numpy()
    land = pd.DatetimeIndex(ev["label_end"]).to_numpy()
    if np.any(land <= t0):
        raise ValueError("label_end her olayda t0'dan sonra olmalı (aksi halde nedensellik tanımsız)")
    p = proba.reindex(ev.index).to_numpy(dtype=float)
    scale = ev["trgt"].to_numpy(dtype=float) if cs.score_units == "vol" else np.ones(len(ev))
    x = ev["exec_net_ret"].to_numpy(dtype=float) / scale      # skor biriminde gerçekleşen getiri
    z = float(ndtri(1.0 - cs.alpha / 2.0))
    half = cs.alpha / 2.0

    n = len(ev)
    mu_u = np.full(n, np.nan)       # skor biriminde μ̂
    q_eff = np.full(n, np.nan)
    size_raw = np.zeros(n)
    dial_m = np.ones(n)
    n_scores = np.zeros(n, dtype=int)
    b_hat = np.full(n, np.nan)
    covered = np.full(n, np.nan)
    lower = np.full(n, np.nan)
    upper = np.full(n, np.nan)

    order_land = np.argsort(land, kind="stable")
    k = 0
    win_sum = loss_sum = 0.0
    win_n = loss_n = 0
    window: deque[float] = deque(maxlen=cs.window)
    all_scores: list[float] = []
    anchor = float("nan")
    anchor_at = 0
    breaks: deque[float] = deque(maxlen=cs.dial_window)

    for i in range(n):
        # 1) t0_i'den ÖNCE kapanmış işlemleri "indir"
        while k < n and land[order_land[k]] < t0[i]:
            j = order_land[k]
            k += 1
            if x[j] > 0:
                win_sum, win_n = win_sum + x[j], win_n + 1
            else:
                loss_sum, loss_n = loss_sum - x[j], loss_n + 1
            if np.isnan(mu_u[j]):
                continue  # karar anında μ̂ yoktu (olasılık/ödeme geçmişi yok) -> skor yok
            s = abs(x[j] - mu_u[j])
            window.append(s)
            all_scores.append(s)
            if len(all_scores) >= cs.min_scores and (
                np.isnan(anchor) or len(all_scores) - anchor_at >= cs.anchor_refresh
            ):
                anchor = conformal_quantile(np.asarray(all_scores), cs.alpha)
                anchor_at = len(all_scores)
            if not np.isnan(q_eff[j]):  # j kararında aralık vardı -> ihlal göstergeleri
                lo, hi = mu_u[j] - q_eff[j], mu_u[j] + q_eff[j]
                covered[j] = float(lo <= x[j] <= hi)
                lower[j] = float(x[j] < lo)
                upper[j] = float(x[j] > hi)
                breaks.append(lower[j])

        # 2) i kararı: yalnızca yukarıda inen bilgiyle
        n_scores[i] = len(window)
        if np.isnan(p[i]) or min(win_n, loss_n) < cs.min_payoff_events:
            continue
        w_bar = win_sum / win_n
        l_bar = loss_sum / loss_n
        b_hat[i] = w_bar / l_bar if l_bar > 0 else np.inf
        mu_u[i] = p[i] * w_bar - (1.0 - p[i]) * l_bar
        if len(window) < cs.min_scores or np.isnan(anchor):
            continue
        q_roll = conformal_quantile(np.asarray(window), cs.alpha)
        q = q_roll ** (1.0 - cs.anchor_lambda) * anchor ** cs.anchor_lambda
        q_eff[i] = max(q, 1e-12)
        sigma_u = q_eff[i] / z
        if p[i] > threshold and mu_u[i] > 0:
            # getiri biriminde: μ = μ_u·scale, σ = σ_u·scale -> f = κ μ_u / (σ_u² · scale)
            size_raw[i] = cs.kappa * mu_u[i] / (sigma_u**2 * scale[i])
        if len(breaks) == cs.dial_window:
            d = float(np.mean(breaks))
            dial_m[i] = float(np.clip(1.0 - cs.dial_beta * (d - half) / half, cs.dial_floor, 1.0))

    idx = ev.index
    undialed = np.clip(size_raw, 0.0, cap)
    sized = np.clip(undialed * dial_m, 0.0, cap) if dial else undialed
    s_ser = lambda a, name: pd.Series(a, index=idx, name=name)  # noqa: E731
    return ConformalKellyResult(
        size=s_ser(sized, "size"),
        size_undialed=s_ser(undialed, "size"),
        mu=s_ser(mu_u * scale, "mu"),
        sigma=s_ser(q_eff / z * scale, "sigma"),
        q_eff=s_ser(q_eff, "q_eff"),
        dial=s_ser(dial_m, "dial"),
        covered=s_ser(covered, "covered"),
        lower_break=s_ser(lower, "lower_break"),
        upper_break=s_ser(upper, "upper_break"),
        n_scores=s_ser(n_scores, "n_scores"),
        payoff_ratio=s_ser(b_hat, "payoff_ratio"),
        alpha=cs.alpha,
    )
