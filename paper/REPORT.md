# Paper trading — BIST 30 long meta-labeling overlay

Son işlem günü: **2026-11-19** · başlangıç 2026-09-25 · sanal sermaye 1,000,000 TL · komisyon 10 bps + kayma 5 bps / yön

| Portföy | Değer (TL) | Getiri | Sharpe (≥20 gün) | Max DD |
|---|---|---|---|---|
| Sistem | 937,065 | -6.29% | -2.98 | -9.1% |
| Buy&Hold (eşit ağırlık) | 900,925 | -9.91% | -2.20 | -17.0% |
| XU030 endeksi | 896,720 | -10.33% | -2.35 | -15.8% |

Sistemin yatırım oranı: 39% · nakit 571,465 TL · 39 gün

## Bugünkü kararlar

| Hisse | Kapanış | Maruziyet | Vol tavanı | Yeni olay | m | P(Y=1) | Aktif olay | Emir (lot) | Not |
|---|---|---|---|---|---|---|---|---|---|
| AEFES | 16.24 | 0.488 | 1.000 |  |  |  | 1 | 0 |  |
| AKBNK | 66.85 | 0.284 | 0.983 |  |  |  | 3 | 0 |  |
| ASELS | 337.00 | 0.562 | 0.766 |  |  |  | 1 | 2 |  |
| ASTOR | 152.90 | 0.526 | 0.526 |  |  |  | 3 | 0 |  |
| BIMAS | 384.00 | 0.580 | 0.886 | evet | 0.834 | 0.567 | 3 | 8 |  |
| EKGYO | 17.75 | 0.233 | 0.845 |  |  |  | 2 | 43 |  |
| ENKAI | 79.25 | 0.787 | 1.000 |  |  |  | 2 | 0 |  |
| EREGL | 31.28 | 0.276 | 0.729 |  |  |  | 3 | 0 |  |
| FROTO | 71.70 | 0.429 | 0.916 |  |  |  | 2 | 0 |  |
| GARAN | 146.40 | 0.378 | 1.000 |  |  |  | 3 | 0 |  |
| GUBRF | 273.75 | 0.150 | 0.651 |  |  |  | 2 | 3 |  |
| ISCTR | 12.74 | 0.422 | 0.870 |  |  |  | 2 | 0 |  |
| KCHOL | 193.70 | 0.590 | 0.955 |  |  |  | 2 | 0 |  |
| KRDMD | 37.74 | 0.380 | 0.819 |  |  |  | 2 | 0 |  |
| MGROS | 449.00 | 0.518 | 0.982 |  |  |  | 3 | 3 |  |
| PETKM | 15.39 | 0.225 | 0.720 |  |  |  | 2 | 0 |  |
| PGSUS | 156.60 | 0.266 | 0.955 |  |  |  | 2 | 0 |  |
| SAHOL | 80.20 | 0.577 | 1.000 |  |  |  | 2 | 0 |  |
| SASA | 1.50 | 0.803 | 0.803 |  |  |  | 2 | 0 |  |
| SISE | 33.32 | 0.409 | 0.833 |  |  |  | 3 | 0 |  |
| TAVHL | 291.50 | 0.419 | 0.881 |  |  |  | 2 | 3 |  |
| TCELL | 93.05 | 0.385 | 0.965 |  |  |  | 1 | 12 |  |
| THYAO | 328.25 | 0.369 | 0.928 | evet | 0.425 | 0.563 | 3 | 3 |  |
| TOASO | 249.30 | 0.272 | 0.747 |  |  |  | 2 | 0 |  |
| TRALT | 35.64 | 0.205 | 0.746 |  |  |  | 2 | 0 |  |
| TRMET | 110.40 | 0.213 | 0.831 |  |  |  | 4 | 0 |  |
| TTKOM | 48.80 | 0.177 | 0.813 |  |  |  | 3 | 0 |  |
| TUPRS | 334.75 | 0.763 | 0.893 | evet | 0.861 | 0.590 | 2 | 7 |  |
| VAKBN | 33.36 | 0.284 | 0.862 |  |  |  | 1 | 0 |  |
| YKBNK | 36.76 | 0.349 | 1.000 |  |  |  | 3 | 0 |  |

## Bugünkü dolumlar (15)

- sistem PETKM: -371 lot @ 15.45 (maliyet 6 TL)
- sistem AEFES: +148 lot @ 16.17 (maliyet 2 TL)
- sistem ASTOR: +5 lot @ 154.58 (maliyet 1 TL)
- sistem ENKAI: +20 lot @ 80.29 (maliyet 2 TL)
- sistem EREGL: +31 lot @ 31.32 (maliyet 1 TL)
- sistem GARAN: +5 lot @ 146.57 (maliyet 1 TL)
- sistem ISCTR: +151 lot @ 12.70 (maliyet 2 TL)
- sistem KCHOL: +4 lot @ 195.90 (maliyet 1 TL)
- sistem KRDMD: +24 lot @ 37.82 (maliyet 1 TL)
- sistem SAHOL: +29 lot @ 80.94 (maliyet 2 TL)
- sistem SASA: +523 lot @ 1.51 (maliyet 1 TL)
- sistem SISE: +31 lot @ 33.58 (maliyet 1 TL)
- sistem TRALT: +25 lot @ 36.20 (maliyet 1 TL)
- sistem TRMET: +7 lot @ 110.05 (maliyet 1 TL)
- sistem YKBNK: +28 lot @ 36.74 (maliyet 1 TL)

_Sanal para; gerçek emir verilmez. Karar kuralları: `docs/preregistration/long_overlay.md`. Kilitli testte bu sistem 12 hissenin 9'unda B&H'nin gerisinde kaldı; bu çalışma ileriye dönük (görülmemiş veride) testtir._
