# Paper trading — BIST 30 long meta-labeling overlay

Son işlem günü: **2026-09-29** · başlangıç 2026-09-25 · sanal sermaye 1,000,000 TL · komisyon 10 bps + kayma 5 bps / yön

| Portföy | Değer (TL) | Getiri | Sharpe (≥20 gün) | Max DD |
|---|---|---|---|---|
| Sistem | 982,340 | -1.77% | n/a | -1.8% |
| Buy&Hold (eşit ağırlık) | 974,020 | -2.60% | n/a | -2.6% |
| XU030 endeksi | 957,177 | -4.28% | n/a | -4.3% |

Sistemin yatırım oranı: 75% · nakit 247,901 TL · 3 gün

## Bugünkü kararlar

| Hisse | Kapanış | Maruziyet | Vol tavanı | Yeni olay | m | P(Y=1) | Aktif olay | Emir (lot) | Not |
|---|---|---|---|---|---|---|---|---|---|
| AEFES | 18.12 | 0.964 | 0.964 |  |  |  | 0 | 0 |  |
| AKBNK | 69.90 | 0.849 | 0.849 |  |  |  | 0 | 13 |  |
| ASELS | 338.50 | 0.575 | 0.742 | evet | 0.775 | 0.593 | 1 | -18 |  |
| ASTOR | 211.70 | 0.634 | 0.634 | evet |  | 0.491 | 1 | 0 | conformal ısınma |
| BIMAS | 421.75 | 1.000 | 1.000 |  |  |  | 0 | 0 |  |
| EKGYO | 18.77 | 0.705 | 0.705 |  |  |  | 0 | 50 |  |
| ENKAI | 84.75 | 0.889 | 0.889 |  |  |  | 0 | 11 |  |
| EREGL | 36.76 | 0.779 | 0.779 |  |  |  | 0 | 26 |  |
| FROTO | 74.40 | 1.000 | 1.000 |  |  |  | 0 | 0 |  |
| GARAN | 129.10 | 0.984 | 0.984 |  |  |  | 0 | 7 |  |
| GUBRF | 417.00 | 0.233 | 0.741 | evet | 0.315 | 0.547 | 1 | 0 |  |
| ISCTR | 12.95 | 0.701 | 0.701 |  |  |  | 0 | 53 |  |
| KCHOL | 214.10 | 0.917 | 0.917 |  |  |  | 0 | 4 |  |
| KRDMD | 45.18 | 0.500 | 0.907 | evet | 0.551 | 0.572 | 1 | -286 |  |
| MGROS | 520.50 | 0.502 | 0.921 |  |  |  | 1 | 0 |  |
| PETKM | 19.44 | 0.144 | 0.528 | evet | 0.360 | 0.564 | 2 | 88 |  |
| PGSUS | 142.40 | 1.000 | 1.000 |  |  |  | 0 | 0 |  |
| SAHOL | 86.80 | 0.881 | 0.881 |  |  |  | 0 | 10 |  |
| SASA | 1.88 | 0.632 | 0.632 |  |  |  | 0 | 0 |  |
| SISE | 38.22 | 0.676 | 0.676 |  |  |  | 0 | 24 |  |
| TAVHL | 266.50 | 0.880 | 0.880 |  |  |  | 0 | 3 |  |
| TCELL | 98.25 | 0.933 | 0.933 |  |  |  | 0 | 9 |  |
| THYAO | 291.50 | 1.000 | 1.000 |  |  |  | 0 | 0 |  |
| TOASO | 277.00 | 0.506 | 0.908 |  |  |  | 1 | 0 |  |
| TRALT | 45.38 | 0.781 | 0.781 |  |  |  | 0 | 21 |  |
| TRMET | 130.50 | 0.277 | 0.897 | evet | 0.308 | 0.524 | 1 | -145 |  |
| TTKOM | 52.80 | 0.108 | 0.605 | evet | 0.178 | 0.528 | 1 | -291 |  |
| TUPRS | 383.25 | 0.809 | 0.809 | evet |  |  | 1 | 0 | eksik öznitelik: ret_skew |
| VAKBN | 33.68 | 0.639 | 0.639 |  |  |  | 0 | 0 |  |
| YKBNK | 36.00 | 0.828 | 0.828 |  |  |  | 0 | 0 |  |

## Bugünkü dolumlar (0)


_Sanal para; gerçek emir verilmez. Karar kuralları: `docs/preregistration/long_overlay.md`. Kilitli testte bu sistem 12 hissenin 9'unda B&H'nin gerisinde kaldı; bu çalışma ileriye dönük (görülmemiş veride) testtir._
