# Paper trading — BIST 30 long meta-labeling overlay

Son işlem günü: **2026-11-24** · başlangıç 2026-09-25 · sanal sermaye 1,000,000 TL · komisyon 10 bps + kayma 5 bps / yön

| Portföy | Değer (TL) | Getiri | Sharpe (≥20 gün) | Max DD |
|---|---|---|---|---|
| Sistem | 922,808 | -7.72% | -3.51 | -9.1% |
| Buy&Hold (eşit ağırlık) | 869,204 | -13.08% | -2.84 | -17.0% |
| XU030 endeksi | 862,990 | -13.70% | -3.03 | -15.8% |

Sistemin yatırım oranı: 39% · nakit 559,629 TL · 42 gün

## Bugünkü kararlar

| Hisse | Kapanış | Maruziyet | Vol tavanı | Yeni olay | m | P(Y=1) | Aktif olay | Emir (lot) | Not |
|---|---|---|---|---|---|---|---|---|---|
| AEFES | 15.52 | 0.532 | 1.000 | evet | 0.575 | 0.562 | 2 | 105 |  |
| AKBNK | 63.95 | 0.299 | 1.000 |  |  |  | 1 | 19 |  |
| ASELS | 322.50 | 0.586 | 0.800 |  |  |  | 1 | 3 |  |
| ASTOR | 149.70 | 0.548 | 0.548 |  |  |  | 2 | 7 |  |
| BIMAS | 368.00 | 0.760 | 0.911 |  |  |  | 1 | 16 |  |
| EKGYO | 17.26 | 0.266 | 0.880 | evet | 0.307 | 0.529 | 2 | 63 |  |
| ENKAI | 76.00 | 0.835 | 1.000 | evet | 0.835 | 0.562 | 1 | 30 |  |
| EREGL | 29.84 | 0.338 | 0.756 |  |  |  | 1 | 77 |  |
| FROTO | 69.90 | 0.472 | 0.944 |  |  |  | 1 | 26 |  |
| GARAN | 143.30 | 0.388 | 1.000 |  |  |  | 2 | 0 |  |
| GUBRF | 272.00 | 0.158 | 0.677 |  |  |  | 1 | 0 |  |
| ISCTR | 12.30 | 0.502 | 0.909 | evet | 0.597 | 0.577 | 2 | 229 |  |
| KCHOL | 188.10 | 0.576 | 0.944 |  |  |  | 1 | 0 |  |
| KRDMD | 35.84 | 0.421 | 0.855 | evet | 0.497 | 0.567 | 2 | 58 |  |
| MGROS | 414.25 | 0.477 | 0.971 | evet | 0.491 | 0.547 | 1 | 0 |  |
| PETKM | 14.90 | 0.000 | 0.753 |  |  |  | 1 | -447 |  |
| PGSUS | 154.20 | 0.000 | 0.984 |  |  |  | 1 | -51 |  |
| SAHOL | 75.95 | 0.968 | 1.000 | evet | 0.968 | 0.610 | 1 | 172 |  |
| SASA | 1.43 | 0.831 | 0.831 |  |  |  | 1 | 1460 |  |
| SISE | 31.22 | 0.428 | 0.853 | evet | 0.502 | 0.546 | 1 | 52 |  |
| TAVHL | 288.00 | 0.446 | 0.914 |  |  |  | 1 | 3 |  |
| TCELL | 90.15 | 0.996 | 0.996 |  |  |  | 0 | 211 |  |
| THYAO | 320.50 | 0.366 | 0.959 | evet | 0.373 | 0.555 | 3 | 0 |  |
| TOASO | 248.40 | 0.294 | 0.781 |  |  |  | 1 | 3 |  |
| TRALT | 34.32 | 0.222 | 0.773 | evet | 0.290 | 0.520 | 2 | 24 |  |
| TRMET | 102.40 | 0.221 | 0.840 | evet | 0.272 | 0.521 | 3 | 7 |  |
| TTKOM | 46.30 | 0.184 | 0.833 | evet | 0.221 | 0.525 | 1 | 20 |  |
| TUPRS | 320.00 | 0.782 | 0.909 |  |  |  | 1 | 4 |  |
| VAKBN | 32.40 | 0.326 | 0.899 | evet | 0.363 | 0.530 | 1 | 47 |  |
| YKBNK | 35.72 | 0.342 | 1.000 | evet | 0.316 | 0.530 | 2 | 0 |  |

## Bugünkü dolumlar (2)

- buyhold ASELS: +0 lot @ 0.43 (maliyet 0 TL) — temettü
- sistem ASELS: +0 lot @ 0.43 (maliyet 0 TL) — temettü

_Sanal para; gerçek emir verilmez. Karar kuralları: `docs/preregistration/long_overlay.md`. Kilitli testte bu sistem 12 hissenin 9'unda B&H'nin gerisinde kaldı; bu çalışma ileriye dönük (görülmemiş veride) testtir._
