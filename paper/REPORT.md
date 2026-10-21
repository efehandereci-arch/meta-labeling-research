# Paper trading — BIST 30 long meta-labeling overlay

Son işlem günü: **2026-10-21** · başlangıç 2026-09-25 · sanal sermaye 1,000,000 TL · komisyon 10 bps + kayma 5 bps / yön

| Portföy | Değer (TL) | Getiri | Sharpe (≥20 gün) | Max DD |
|---|---|---|---|---|
| Sistem | 945,652 | -5.43% | n/a | -5.6% |
| Buy&Hold (eşit ağırlık) | 916,244 | -8.38% | n/a | -8.8% |
| XU030 endeksi | 906,982 | -9.30% | n/a | -10.8% |

Sistemin yatırım oranı: 48% · nakit 492,835 TL · 19 gün

## Bugünkü kararlar

| Hisse | Kapanış | Maruziyet | Vol tavanı | Yeni olay | m | P(Y=1) | Aktif olay | Emir (lot) | Not |
|---|---|---|---|---|---|---|---|---|---|
| AEFES | 16.88 | 0.687 | 0.991 | evet | 0.761 | 0.589 | 2 | 218 |  |
| AKBNK | 67.20 | 0.304 | 1.000 |  |  |  | 1 | 0 |  |
| ASELS | 345.75 | 0.434 | 0.659 |  |  |  | 1 | 0 |  |
| ASTOR | 156.60 | 0.575 | 0.575 | evet |  | 0.306 | 2 | 8 | conformal ısınma |
| BIMAS | 385.50 | 0.688 | 0.860 |  |  |  | 2 | 0 |  |
| EKGYO | 18.57 | 0.234 | 0.780 |  |  |  | 2 | 0 |  |
| ENKAI | 75.80 | 0.620 | 0.896 | evet | 0.644 | 0.552 | 3 | 0 |  |
| EREGL | 36.52 | 0.427 | 0.873 |  |  |  | 2 | 26 |  |
| FROTO | 66.85 | 1.000 | 1.000 | evet |  |  | 2 | 0 | eksik öznitelik: ret_skew |
| GARAN | 132.60 | 0.406 | 1.000 |  |  |  | 2 | 0 |  |
| GUBRF | 354.50 | 0.286 | 0.789 | evet | 0.258 | 0.532 | 3 | -3 |  |
| ISCTR | 12.87 | 0.824 | 0.824 |  |  |  | 0 | 0 |  |
| KCHOL | 203.30 | 0.544 | 0.942 | evet | 0.570 | 0.554 | 4 | 0 |  |
| KRDMD | 42.04 | 0.625 | 0.997 |  |  |  | 2 | 23 |  |
| MGROS | 454.00 | 0.605 | 0.971 | evet | 0.614 | 0.562 | 4 | 0 |  |
| PETKM | 19.05 | 0.260 | 0.656 | evet | 0.384 | 0.552 | 2 | 0 |  |
| PGSUS | 129.30 | 0.048 | 1.000 | evet | 0.191 | 0.509 | 4 | 11 |  |
| SAHOL | 88.15 | 0.477 | 0.907 |  |  |  | 1 | 0 |  |
| SASA | 1.66 | 0.716 | 0.716 | evet |  |  | 3 | 0 | eksik öznitelik: volume_z |
| SISE | 35.26 | 0.401 | 0.818 | evet | 0.482 | 0.546 | 2 | 0 |  |
| TAVHL | 287.00 | 0.577 | 1.000 |  |  |  | 1 | 0 |  |
| TCELL | 95.00 | 0.469 | 1.000 | evet | 0.419 | 0.549 | 3 | 0 |  |
| THYAO | 265.00 | 0.534 | 1.000 | evet | 0.539 | 0.563 | 3 | 4 |  |
| TOASO | 227.90 | 0.464 | 0.903 | evet | 0.514 | 0.559 | 1 | -59 |  |
| TRALT | 40.26 | 0.320 | 0.868 | evet | 0.372 | 0.527 | 3 | 19 |  |
| TRMET | 117.50 | 0.286 | 0.923 | evet | 0.311 | 0.523 | 2 | 0 |  |
| TTKOM | 49.40 | 0.153 | 0.736 | evet | 0.220 | 0.528 | 3 | 0 |  |
| TUPRS | 359.25 | 0.845 | 0.845 |  |  |  | 0 | 0 |  |
| VAKBN | 32.30 | 0.263 | 0.770 |  |  |  | 2 | 0 |  |
| YKBNK | 36.42 | 0.314 | 0.972 |  |  |  | 2 | 0 |  |

## Bugünkü dolumlar (16)

- sistem ASELS: -2 lot @ 341.33 (maliyet 1 TL)
- sistem BIMAS: -5 lot @ 381.81 (maliyet 2 TL)
- sistem ENKAI: -15 lot @ 77.01 (maliyet 1 TL)
- sistem KCHOL: -4 lot @ 206.40 (maliyet 1 TL)
- sistem KRDMD: -16 lot @ 42.56 (maliyet 1 TL)
- sistem MGROS: -2 lot @ 461.77 (maliyet 1 TL)
- sistem SAHOL: -19 lot @ 88.71 (maliyet 2 TL)
- sistem TAVHL: -4 lot @ 284.36 (maliyet 1 TL)
- sistem TCELL: -12 lot @ 97.35 (maliyet 1 TL)
- sistem EREGL: +101 lot @ 36.92 (maliyet 4 TL)
- sistem FROTO: +17 lot @ 68.03 (maliyet 1 TL)
- sistem GARAN: +6 lot @ 133.77 (maliyet 1 TL)
- sistem ISCTR: +1404 lot @ 13.02 (maliyet 18 TL)
- sistem SISE: +18 lot @ 35.98 (maliyet 1 TL)
- sistem TOASO: +68 lot @ 235.52 (maliyet 16 TL)
- sistem YKBNK: +142 lot @ 36.48 (maliyet 5 TL)

_Sanal para; gerçek emir verilmez. Karar kuralları: `docs/preregistration/long_overlay.md`. Kilitli testte bu sistem 12 hissenin 9'unda B&H'nin gerisinde kaldı; bu çalışma ileriye dönük (görülmemiş veride) testtir._
