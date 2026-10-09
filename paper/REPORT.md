# Paper trading — BIST 30 long meta-labeling overlay

Son işlem günü: **2026-10-09** · başlangıç 2026-09-25 · sanal sermaye 1,000,000 TL · komisyon 10 bps + kayma 5 bps / yön

| Portföy | Değer (TL) | Getiri | Sharpe (≥20 gün) | Max DD |
|---|---|---|---|---|
| Sistem | 975,784 | -2.42% | n/a | -3.8% |
| Buy&Hold (eşit ağırlık) | 970,551 | -2.94% | n/a | -5.4% |
| XU030 endeksi | 949,725 | -5.03% | n/a | -6.9% |

Sistemin yatırım oranı: 42% · nakit 569,025 TL · 11 gün

## Bugünkü kararlar

| Hisse | Kapanış | Maruziyet | Vol tavanı | Yeni olay | m | P(Y=1) | Aktif olay | Emir (lot) | Not |
|---|---|---|---|---|---|---|---|---|---|
| AEFES | 18.56 | 0.441 | 0.994 | evet | 0.609 | 0.572 | 4 | 103 |  |
| AKBNK | 67.85 | 0.264 | 0.917 |  |  |  | 2 | 13 |  |
| ASELS | 351.25 | 0.429 | 0.657 |  |  |  | 1 | 0 |  |
| ASTOR | 204.40 | 0.542 | 0.542 |  |  |  | 2 | -10 |  |
| BIMAS | 402.75 | 1.000 | 1.000 | evet | 1.000 | 0.603 | 2 | 0 |  |
| EKGYO | 19.85 | 0.242 | 0.770 |  |  |  | 2 | 0 |  |
| ENKAI | 83.50 | 0.660 | 0.884 | evet | 0.723 | 0.561 | 3 | -12 |  |
| EREGL | 37.32 | 0.328 | 0.853 |  |  |  | 3 | 0 |  |
| FROTO | 74.65 | 1.000 | 1.000 |  |  |  | 1 | 0 |  |
| GARAN | 129.30 | 0.347 | 0.998 |  |  |  | 1 | 0 |  |
| GUBRF | 418.00 | 0.294 | 0.819 | evet | 0.372 | 0.551 | 3 | 0 |  |
| ISCTR | 12.67 | 0.292 | 0.733 |  |  |  | 2 | 60 |  |
| KCHOL | 208.00 | 0.581 | 0.928 |  |  |  | 3 | 5 |  |
| KRDMD | 43.12 | 0.545 | 0.963 |  |  |  | 3 | 24 |  |
| MGROS | 503.00 | 0.538 | 0.979 |  |  |  | 3 | 0 |  |
| PETKM | 20.56 | 0.223 | 0.592 |  |  |  | 2 | 0 |  |
| PGSUS | 134.40 | 0.000 | 1.000 |  |  |  | 1 | 0 |  |
| SAHOL | 83.50 | 0.479 | 0.850 | evet | 0.560 | 0.570 | 2 | 91 |  |
| SASA | 1.93 | 0.667 | 0.667 | evet |  |  | 3 | 0 | eksik öznitelik: volume_z |
| SISE | 38.04 | 0.346 | 0.747 |  |  |  | 2 | 26 |  |
| TAVHL | 274.75 | 0.602 | 0.974 |  |  |  | 1 | 5 |  |
| TCELL | 98.55 | 0.500 | 0.992 | evet | 0.407 | 0.550 | 2 | -19 |  |
| THYAO | 287.50 | 0.478 | 1.000 |  |  |  | 3 | 0 |  |
| TOASO | 265.00 | 0.460 | 0.886 |  |  |  | 3 | 0 |  |
| TRALT | 43.90 | 0.280 | 0.831 | evet | 0.360 | 0.529 | 3 | 0 |  |
| TRMET | 137.30 | 0.285 | 0.918 | evet | 0.313 | 0.523 | 2 | 0 |  |
| TTKOM | 52.30 | 0.137 | 0.682 |  |  |  | 2 | 0 |  |
| TUPRS | 386.25 | 0.818 | 0.818 |  |  |  | 4 | 0 |  |
| VAKBN | 33.90 | 0.204 | 0.694 |  |  |  | 1 | 0 |  |
| YKBNK | 35.44 | 0.137 | 0.861 | evet | 0.319 | 0.541 | 2 | 125 |  |

## Bugünkü dolumlar (0)


_Sanal para; gerçek emir verilmez. Karar kuralları: `docs/preregistration/long_overlay.md`. Kilitli testte bu sistem 12 hissenin 9'unda B&H'nin gerisinde kaldı; bu çalışma ileriye dönük (görülmemiş veride) testtir._
