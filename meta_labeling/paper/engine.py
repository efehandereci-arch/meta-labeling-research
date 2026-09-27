"""Sanal portföy motoru: emir, dolum, bölünme, temettü, değerleme, kıyas ve rapor.

Zaman çizelgesi (her yeni işlem günü d için, sırayla):
  1. Bölünme  : lot x oran (küsurat, açılış fiyatından nakde çevrilir); bekleyen emirler de ölçeklenir
  2. Temettü  : d'den önce tutulan lot x temettü nakde (hak kullanım günü açılışta alan almaz)
  3. Dolum    : dünkü emirler d AÇILIŞINDAN; önce satışlar, sonra alışlar; nakit yetmezse alışlar
                orantılı küçülür; komisyon + kayma; kaldıraç ve açığa satış yok
  4. Değerleme: d kapanışı (verisi olmayan hisse son bilinen kapanışla)
  5. Karar    : yalnızca en son günde. Hedef ağırlık = overlay maruziyeti x vol tavanı / N;
                hedef lot = taban(hedef değer / kapanış); fark emir olarak yarının açılışına yazılır
Buy&Hold kıyası aynı sermayeyle ilk gün eşit ağırlıkta alır ve bir daha işlem yapmaz.
"""

from __future__ import annotations

import json
import logging
import math
from dataclasses import asdict, dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd

from ..research.settings import ResearchConfig
from .config import PaperConfig
from .data import Provider, adjusted_ohlcv
from .signals import decide, event_active

log = logging.getLogger("meta_labeling.paper")
SYSTEM, BUYHOLD = "sistem", "buyhold"


@dataclass
class Book:
    cash: float
    positions: dict[str, int] = field(default_factory=dict)
    pending: dict[str, int] = field(default_factory=dict)

    def value(self, prices: dict[str, float]) -> float:
        return self.cash + sum(n * prices.get(t, 0.0) for t, n in self.positions.items())


@dataclass
class PaperState:
    start: str | None = None
    last_date: str | None = None
    books: dict[str, Book] = field(default_factory=dict)
    events: dict[str, list[dict]] = field(default_factory=dict)
    last_close: dict[str, float] = field(default_factory=dict)
    bench_start: float | None = None

    @classmethod
    def new(cls, capital: float) -> "PaperState":
        return cls(books={SYSTEM: Book(capital), BUYHOLD: Book(capital)})

    @classmethod
    def load(cls, path: Path, capital: float) -> "PaperState":
        if not path.exists():
            return cls.new(capital)
        raw = json.loads(path.read_text(encoding="utf-8"))
        raw["books"] = {k: Book(**v) for k, v in raw["books"].items()}
        return cls(**raw)

    def save(self, path: Path) -> None:
        path.write_text(json.dumps(asdict(self), indent=1, ensure_ascii=False, sort_keys=True), encoding="utf-8")


COLUMNS = {
    "trades.csv": ["date", "portfolio", "ticker", "shares", "price", "notional", "cost", "note"],
    "equity.csv": ["date", "sistem", "buyhold", "xu030", "sistem_nakit", "sistem_yatirim_orani"],
    "decisions.csv": ["date", "ticker", "close", "vol_cap", "sigma", "new_event", "m", "p", "mu", "active_events",
                      "meta_exposure", "exposure", "target_shares", "current_shares", "order", "note"],
}


def _append_csv(path: Path, rows: list[dict]) -> None:
    """Sabit sütun sırasıyla ekler (satırlarda eksik alanlar boş kalır)."""
    if not rows:
        return
    df = pd.DataFrame(rows).reindex(columns=COLUMNS[path.name])
    df.to_csv(path, mode="a", header=not path.exists(), index=False)


def _fill(book: Book, bars: dict[str, pd.Series], pc: PaperConfig, day: str, name: str) -> list[dict]:
    trades = []
    comm, slip = pc.commission_bps / 1e4, pc.slippage_bps / 1e4
    orders = {t: n for t, n in book.pending.items() if n != 0 and t in bars}
    for t, n in sorted(orders.items()):              # satışlar (nakit yaratır)
        if n >= 0:
            continue
        n = -min(-n, book.positions.get(t, 0))       # açığa satış yok
        if n == 0:
            continue
        px = bars[t]["Open"] * (1 - slip)
        notional = -n * px
        book.cash += notional - notional * comm
        book.positions[t] = book.positions.get(t, 0) + n
        trades.append({"date": day, "portfolio": name, "ticker": t, "shares": n, "price": px,
                       "notional": -notional, "cost": notional * comm})
    buys = {t: n for t, n in orders.items() if n > 0}
    need = sum(n * bars[t]["Open"] * (1 + slip) * (1 + comm) for t, n in buys.items())
    scale = min(1.0, book.cash / need) if need > 0 else 1.0
    for t, n in sorted(buys.items()):
        n = int(math.floor(n * scale))
        if n <= 0:
            continue
        px = bars[t]["Open"] * (1 + slip)
        notional = n * px
        book.cash -= notional + notional * comm
        book.positions[t] = book.positions.get(t, 0) + n
        trades.append({"date": day, "portfolio": name, "ticker": t, "shares": n, "price": px,
                       "notional": notional, "cost": notional * comm})
    book.pending = {}
    book.positions = {t: n for t, n in book.positions.items() if n != 0}
    return trades


def _corporate_actions(book: Book, bars: dict[str, pd.Series], day: str, name: str) -> list[dict]:
    rows = []
    for t, bar in bars.items():
        r = float(bar.get("Stock Splits", 0.0) or 0.0)
        if r > 0 and r != 1.0:
            held = book.positions.get(t, 0)
            if held:
                new = held * r
                whole = int(math.floor(new + 1e-9))
                book.cash += (new - whole) * float(bar["Open"])        # küsurat nakde
                book.positions[t] = whole
            if t in book.pending:
                book.pending[t] = int(round(book.pending[t] * r))
            rows.append({"date": day, "portfolio": name, "ticker": t, "shares": 0, "price": r,
                         "notional": 0.0, "cost": 0.0, "note": f"bölünme x{r:g}"})
        dv = float(bar.get("Dividends", 0.0) or 0.0)
        if dv > 0 and book.positions.get(t, 0):
            amt = book.positions[t] * dv
            book.cash += amt
            rows.append({"date": day, "portfolio": name, "ticker": t, "shares": 0, "price": dv,
                         "notional": amt, "cost": 0.0, "note": "temettü"})
    return rows


def run_day(pc: PaperConfig, rc: ResearchConfig, provider: Provider, state_dir: str | Path) -> dict:
    """Bir çalıştırma: yeni işlem günlerini işler, son gün için karar verir, dosyaları günceller."""
    out = Path(state_dir)
    out.mkdir(parents=True, exist_ok=True)
    state = PaperState.load(out / "state.json", pc.capital)
    symbols = [t + pc.suffix for t in pc.tickers]
    data = provider.fetch(symbols + [pc.market_index, pc.benchmark_index])
    stocks = {t: data[t + pc.suffix] for t in pc.tickers if t + pc.suffix in data}
    missing = [t for t in pc.tickers if t not in stocks]
    market = adjusted_ohlcv(data[pc.market_index]) if pc.market_index in data else None
    bench = data.get(pc.benchmark_index)
    calendar = bench.index if bench is not None and len(bench) else \
        pd.DatetimeIndex(sorted(set().union(*[set(d.index) for d in stocks.values()])))
    last = pd.Timestamp(state.last_date) if state.last_date else None
    new_days = [d for d in calendar if last is None or d > last]
    if not new_days:
        log.info("Yeni işlem günü yok (son: %s)", state.last_date)
        return {"status": "no-new-day", "last_date": state.last_date, "missing": missing}
    if last is None:
        new_days = new_days[-1:]                      # ilk çalıştırma: yalnızca bugün için karar

    trades, equity_rows, decision_rows = [], [], []
    for d in new_days:
        day = str(d.date())
        bars = {t: df.loc[d] for t, df in stocks.items() if d in df.index}
        for name, book in state.books.items():
            trades += _corporate_actions(book, bars, day, name)
            trades += _fill(book, bars, pc, day, name)
        for t, bar in bars.items():
            state.last_close[t] = float(bar["Close"])
        if bench is not None and d in bench.index:
            if state.bench_start is None:
                state.bench_start = float(bench.loc[d, "Close"])
            bench_val = pc.capital * float(bench.loc[d, "Close"]) / state.bench_start
        else:
            bench_val = float("nan")
        values = {name: b.value(state.last_close) for name, b in state.books.items()}

        if d == new_days[-1]:
            decision_rows = _decide_all(state, pc, rc, stocks, market, d, values[SYSTEM], missing)
            if state.start is None:                   # Buy&Hold: ilk gün eşit ağırlık, sonra dokunulmaz
                alloc = pc.capital / len(pc.tickers)
                unit = 1 + (pc.commission_bps + pc.slippage_bps) / 1e4      # maliyet payı ayrılır
                state.books[BUYHOLD].pending = {t: int(alloc // (state.last_close[t] * unit)) for t in bars}
                state.start = day
        sys_book = state.books[SYSTEM]
        invested = sum(n * state.last_close.get(t, 0.0) for t, n in sys_book.positions.items())
        equity_rows.append({"date": day, "sistem": values[SYSTEM], "buyhold": values[BUYHOLD],
                            "xu030": bench_val, "sistem_nakit": sys_book.cash,
                            "sistem_yatirim_orani": invested / values[SYSTEM] if values[SYSTEM] else np.nan})
        state.last_date = day

    _append_csv(out / "trades.csv", trades)
    _append_csv(out / "equity.csv", equity_rows)
    _append_csv(out / "decisions.csv", decision_rows)
    state.save(out / "state.json")
    write_report(out, pc, state, decision_rows, trades, missing)
    return {"status": "ok", "days": [str(d.date()) for d in new_days], "trades": len(trades), "missing": missing}


def _decide_all(state: PaperState, pc: PaperConfig, rc: ResearchConfig, stocks: dict[str, pd.DataFrame],
                market: pd.DataFrame | None, d: pd.Timestamp, equity: float, missing: list[str]) -> list[dict]:
    rows = []
    n = len(pc.tickers)
    book = state.books[SYSTEM]
    alloc = equity / n
    default = rc.overlay.default_exposure
    for t in pc.tickers:
        if t not in stocks or d not in stocks[t].index:
            rows.append({"date": str(d.date()), "ticker": t, "note": "veri yok, pozisyon korunuyor"})
            continue
        adj = adjusted_ohlcv(stocks[t].loc[:d])
        evs = [e for e in state.events.get(t, [])
               if event_active(adj["Close"], pd.Timestamp(e["t0"]), e["trgt"], rc)]
        try:
            dec = decide(adj, market, rc, pc.min_history_bars)
        except Exception as exc:  # tek hisse hatası tüm çalıştırmayı durdurmasın
            log.exception("%s karar hatası", t)
            rows.append({"date": str(d.date()), "ticker": t, "note": f"hata: {exc}"})
            continue
        if dec.new_event and np.isfinite(dec.sigma):
            evs.append({"t0": str(d.date()), "trgt": dec.sigma, "m": None if np.isnan(dec.m) else dec.m})
        state.events[t] = evs
        opined = [e["m"] for e in evs if e["m"] is not None]
        meta = float(np.mean(opined)) if opined else default
        exposure = float(np.clip(meta * dec.vol_cap, 0.0, 1.0))
        close = float(stocks[t].loc[d, "Close"])
        target = int(math.floor(exposure * alloc / (close * (1 + (pc.commission_bps + pc.slippage_bps) / 1e4))))
        cur = book.positions.get(t, 0)
        delta = target - cur
        if abs(delta) * close < pc.min_trade_frac * alloc:
            delta = 0
        if delta:
            book.pending[t] = delta
        rows.append({"date": str(d.date()), "ticker": t, "close": close, "vol_cap": dec.vol_cap,
                     "sigma": dec.sigma, "new_event": dec.new_event, "m": dec.m, "p": dec.p, "mu": dec.mu,
                     "active_events": len(evs), "meta_exposure": meta, "exposure": exposure,
                     "target_shares": target, "current_shares": cur, "order": delta, "note": dec.note})
    return rows


def _stats(v: pd.Series) -> dict[str, float]:
    r = v.pct_change().dropna()
    dd = (v / v.cummax() - 1).min() if len(v) else np.nan
    sr = r.mean() / r.std() * np.sqrt(252) if len(r) >= 20 and r.std() > 0 else np.nan
    return {"değer": v.iloc[-1], "getiri": v.iloc[-1] / v.iloc[0] - 1 if len(v) else np.nan, "sharpe": sr, "maxdd": dd}


def write_report(out: Path, pc: PaperConfig, state: PaperState, decisions: list[dict], trades: list[dict],
                 missing: list[str]) -> None:
    eq = pd.read_csv(out / "equity.csv", parse_dates=["date"]).set_index("date")
    lines = [f"# Paper trading — BIST 30 long meta-labeling overlay\n",
             f"Son işlem günü: **{state.last_date}** · başlangıç {state.start} · sanal sermaye "
             f"{pc.capital:,.0f} TL · komisyon {pc.commission_bps:g} bps + kayma {pc.slippage_bps:g} bps / yön\n",
             "| Portföy | Değer (TL) | Getiri | Sharpe (≥20 gün) | Max DD |", "|---|---|---|---|---|"]
    for col, label in (("sistem", "Sistem"), ("buyhold", "Buy&Hold (eşit ağırlık)"), ("xu030", "XU030 endeksi")):
        s = eq[col].dropna()
        if s.empty:
            continue
        st = _stats(s)
        sr = "n/a" if np.isnan(st["sharpe"]) else f"{st['sharpe']:.2f}"
        lines.append(f"| {label} | {st['değer']:,.0f} | {100 * st['getiri']:+.2f}% | {sr} | {100 * st['maxdd']:.1f}% |")
    lines += ["", f"Sistemin yatırım oranı: {100 * eq['sistem_yatirim_orani'].iloc[-1]:.0f}% · "
              f"nakit {eq['sistem_nakit'].iloc[-1]:,.0f} TL · {len(eq)} gün\n"]
    if decisions:
        lines += ["## Bugünkü kararlar\n", "| Hisse | Kapanış | Maruziyet | Vol tavanı | Yeni olay | m | P(Y=1) | Aktif olay | Emir (lot) | Not |",
                  "|---|---|---|---|---|---|---|---|---|---|"]
        f = lambda x, k=3: "" if x is None or (isinstance(x, float) and np.isnan(x)) else (f"{x:.{k}f}" if isinstance(x, float) else str(x))  # noqa: E731
        for r in decisions:
            lines.append(f"| {r['ticker']} | {f(r.get('close'), 2)} | {f(r.get('exposure'))} | {f(r.get('vol_cap'))} | "
                         f"{'evet' if r.get('new_event') else ''} | {f(r.get('m'))} | {f(r.get('p'))} | "
                         f"{r.get('active_events', '')} | {r.get('order', '')} | {r.get('note', '')} |")
    today = [t for t in trades if t["date"] == state.last_date]
    lines += ["", f"## Bugünkü dolumlar ({len(today)})\n"]
    for t in today:
        lines.append(f"- {t['portfolio']} {t['ticker']}: {t['shares']:+d} lot @ {t['price']:.2f} "
                     f"(maliyet {t['cost']:.0f} TL){' — ' + t['note'] if t.get('note') else ''}")
    if missing:
        lines += ["", f"**Veri alınamayan hisseler:** {', '.join(missing)}"]
    lines += ["", "_Sanal para; gerçek emir verilmez. Karar kuralları: `docs/preregistration/long_overlay.md`. "
              "Kilitli testte bu sistem 12 hissenin 9'unda B&H'nin gerisinde kaldı; bu çalışma ileriye dönük "
              "(görülmemiş veride) testtir._"]
    (out / "REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
