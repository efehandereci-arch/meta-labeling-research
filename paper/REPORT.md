# Paper trading — BIST 30 long meta-labeling overlay

Son işlem günü: **2026-11-04** · başlangıç 2026-09-25 · sanal sermaye 1,000,000 TL · komisyon 10 bps + kayma 5 bps / yön

| Portföy | Değer (TL) | Getiri | Sharpe (≥20 gün) | Max DD |
|---|---|---|---|---|
| Sistem | 941,148 | -5.89% | -3.44 | -9.1% |
| Buy&Hold (eşit ağırlık) | 900,732 | -9.93% | -2.82 | -17.0% |
| XU030 endeksi | 898,658 | -10.13% | -2.94 | -15.8% |

Sistemin yatırım oranı: 42% · nakit 547,671 TL · 28 gün

## Bugünkü kararlar

| Hisse | Kapanış | Maruziyet | Vol tavanı | Yeni olay | m | P(Y=1) | Aktif olay | Emir (lot) | Not |
|---|---|---|---|---|---|---|---|---|---|
| AEFES | 16.69 | 0.362 | 0.898 | evet | 0.412 | 0.552 | 2 | 0 |  |
| AKBNK | 66.20 | 0.165 | 0.863 | evet | 0.153 | 0.504 | 2 | -41 |  |
| ASELS | 353.75 | 0.475 | 0.711 | evet | 0.637 | 0.574 | 3 | 0 |  |
| ASTOR | 165.70 | 0.520 | 0.520 | evet |  | 0.278 | 3 | -5 | conformal ısınma |
| BIMAS | 372.50 | 0.474 | 0.780 | evet | 0.000 | 0.382 | 3 | -21 |  |
| EKGYO | 17.49 | 0.205 | 0.729 | evet | 0.285 | 0.535 | 3 | -37 |  |
| ENKAI | 81.25 | 0.491 | 0.870 |  |  |  | 2 | 0 |  |
| EREGL | 31.84 | 0.321 | 0.672 |  |  |  | 2 | 0 |  |
| FROTO | 68.65 | 0.566 | 0.957 | evet | 0.591 | 0.541 | 1 | -31 |  |
| GARAN | 137.50 | 0.371 | 0.990 | evet | 0.375 | 0.532 | 1 | -16 |  |
| GUBRF | 283.50 | 0.207 | 0.580 |  |  |  | 1 | 0 |  |
| ISCTR | 12.87 | 0.329 | 0.770 | evet | 0.434 | 0.565 | 2 | 0 |  |
| KCHOL | 203.00 | 0.506 | 0.919 | evet | 0.531 | 0.550 | 2 | -4 |  |
| KRDMD | 40.80 | 0.409 | 0.810 | evet | 0.505 | 0.572 | 1 | -73 |  |
| MGROS | 454.00 | 0.447 | 0.905 | evet | 0.493 | 0.552 | 1 | -6 |  |
| PETKM | 17.77 | 0.393 | 0.648 | evet | 0.588 | 0.590 | 2 | -60 |  |
| PGSUS | 134.60 | 0.000 | 0.919 | evet | 0.000 | 0.436 | 1 | -164 |  |
| SAHOL | 86.20 | 0.373 | 0.901 | evet | 0.507 | 0.559 | 3 | 0 |  |
| SASA | 1.65 | 0.694 | 0.694 | evet |  |  | 1 | -3027 | eksik öznitelik: volume_z |
| SISE | 35.60 | 0.363 | 0.754 | evet | 0.474 | 0.551 | 2 | -26 |  |
| TAVHL | 278.75 | 0.383 | 0.812 | evet | 0.472 | 0.567 | 1 | -3 |  |
| TCELL | 93.95 | 0.468 | 1.000 |  |  |  | 2 | 0 |  |
| THYAO | 291.25 | 0.280 | 0.775 | evet | 0.361 | 0.566 | 1 | -22 |  |
| TOASO | 226.00 | 0.296 | 0.753 | evet | 0.392 | 0.553 | 2 | 0 |  |
| TRALT | 36.74 | 0.175 | 0.674 | evet | 0.252 | 0.520 | 2 | -26 |  |
| TRMET | 107.30 | 0.179 | 0.735 | evet | 0.243 | 0.523 | 1 | -7 |  |
| TTKOM | 48.90 | 0.174 | 0.762 | evet | 0.208 | 0.526 | 4 | 0 |  |
| TUPRS | 343.25 | 0.708 | 0.914 |  |  |  | 2 | 2 |  |
| VAKBN | 31.50 | 0.107 | 0.745 | evet | 0.282 | 0.526 | 3 | 46 |  |
| YKBNK | 35.88 | 0.310 | 0.920 | evet | 0.329 | 0.539 | 5 | 0 |  |

## Bugünkü dolumlar (3)

- sistem MGROS: -5 lot @ 439.28 (maliyet 2 TL)
- sistem PGSUS: -10 lot @ 128.94 (maliyet 1 TL)
- sistem TCELL: +9 lot @ 94.30 (maliyet 1 TL)

_Sanal para; gerçek emir verilmez. Karar kuralları: `docs/preregistration/long_overlay.md`. Kilitli testte bu sistem 12 hissenin 9'unda B&H'nin gerisinde kaldı; bu çalışma ileriye dönük (görülmemiş veride) testtir._
