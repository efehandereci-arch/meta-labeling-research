# Paper trading — BIST 30 long meta-labeling overlay

Son işlem günü: **2026-10-27** · başlangıç 2026-09-25 · sanal sermaye 1,000,000 TL · komisyon 10 bps + kayma 5 bps / yön

| Portföy | Değer (TL) | Getiri | Sharpe (≥20 gün) | Max DD |
|---|---|---|---|---|
| Sistem | 927,275 | -7.27% | -6.10 | -7.7% |
| Buy&Hold (eşit ağırlık) | 870,505 | -12.95% | -5.96 | -13.4% |
| XU030 endeksi | 873,815 | -12.62% | -5.35 | -13.0% |

Sistemin yatırım oranı: 43% · nakit 528,509 TL · 23 gün

## Bugünkü kararlar

| Hisse | Kapanış | Maruziyet | Vol tavanı | Yeni olay | m | P(Y=1) | Aktif olay | Emir (lot) | Not |
|---|---|---|---|---|---|---|---|---|---|
| AEFES | 16.26 | 0.582 | 0.967 | evet | 0.609 | 0.572 | 2 | -175 |  |
| AKBNK | 64.30 | 0.288 | 0.997 |  |  |  | 1 | 0 |  |
| ASELS | 340.75 | 0.464 | 0.704 |  |  |  | 1 | 3 |  |
| ASTOR | 172.40 | 0.521 | 0.521 | evet |  | 0.278 | 2 | -34 | conformal ısınma |
| BIMAS | 363.00 | 0.759 | 0.835 | evet | 1.000 | 0.606 | 2 | 9 |  |
| EKGYO | 16.99 | 0.220 | 0.781 |  |  |  | 2 | 0 |  |
| ENKAI | 77.05 | 0.576 | 0.895 |  |  |  | 1 | -14 |  |
| EREGL | 31.46 | 0.323 | 0.676 |  |  |  | 1 | 0 |  |
| FROTO | 69.90 | 0.693 | 1.000 | evet | 0.693 | 0.545 | 1 | -80 |  |
| GARAN | 127.30 | 0.415 | 1.000 |  |  |  | 1 | 0 |  |
| GUBRF | 278.75 | 0.664 | 0.664 |  |  |  | 0 | 43 |  |
| ISCTR | 12.29 | 0.181 | 0.851 |  |  |  | 1 | 0 |  |
| KCHOL | 198.70 | 0.547 | 0.951 |  |  |  | 3 | 0 |  |
| KRDMD | 37.60 | 0.471 | 0.863 | evet | 0.546 | 0.574 | 1 | -81 |  |
| MGROS | 423.75 | 0.628 | 1.000 |  |  |  | 1 | 2 |  |
| PETKM | 17.58 | 0.347 | 0.691 | evet | 0.629 | 0.590 | 2 | 202 |  |
| PGSUS | 122.10 | 0.135 | 1.000 | evet | 0.078 | 0.495 | 2 | 0 |  |
| SAHOL | 86.00 | 0.534 | 0.967 |  |  |  | 2 | 8 |  |
| SASA | 1.52 | 0.768 | 0.768 | evet |  |  | 2 | 1322 | eksik öznitelik: volume_z |
| SISE | 33.76 | 0.416 | 0.847 |  |  |  | 2 | 24 |  |
| TAVHL | 264.75 | 0.442 | 0.891 |  |  |  | 1 | 3 |  |
| TCELL | 91.10 | 0.423 | 1.000 |  |  |  | 1 | 0 |  |
| THYAO | 253.00 | 0.560 | 1.000 | evet | 0.578 | 0.564 | 2 | 5 |  |
| TOASO | 231.50 | 0.440 | 0.872 | evet | 0.494 | 0.558 | 2 | -6 |  |
| TRALT | 35.36 | 0.262 | 0.812 |  |  |  | 1 | 19 |  |
| TRMET | 102.50 | 0.236 | 0.853 |  |  |  | 1 | 0 |  |
| TTKOM | 47.08 | 0.186 | 0.740 |  |  |  | 2 | 0 |  |
| TUPRS | 361.50 | 0.670 | 0.883 |  |  |  | 1 | 0 |  |
| VAKBN | 30.88 | 0.193 | 0.784 |  |  |  | 2 | 0 |  |
| YKBNK | 35.38 | 0.337 | 0.972 |  |  |  | 1 | 0 |  |

## Bugünkü dolumlar (0)


_Sanal para; gerçek emir verilmez. Karar kuralları: `docs/preregistration/long_overlay.md`. Kilitli testte bu sistem 12 hissenin 9'unda B&H'nin gerisinde kaldı; bu çalışma ileriye dönük (görülmemiş veride) testtir._
