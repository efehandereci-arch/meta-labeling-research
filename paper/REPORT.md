# Paper trading — BIST 30 long meta-labeling overlay

Son işlem günü: **2026-10-20** · başlangıç 2026-09-25 · sanal sermaye 1,000,000 TL · komisyon 10 bps + kayma 5 bps / yön

| Portföy | Değer (TL) | Getiri | Sharpe (≥20 gün) | Max DD |
|---|---|---|---|---|
| Sistem | 956,704 | -4.33% | n/a | -5.6% |
| Buy&Hold (eşit ağırlık) | 937,880 | -6.21% | n/a | -8.8% |
| XU030 endeksi | 920,332 | -7.97% | n/a | -10.8% |

Sistemin yatırım oranı: 45% · nakit 528,529 TL · 18 gün

## Bugünkü kararlar

| Hisse | Kapanış | Maruziyet | Vol tavanı | Yeni olay | m | P(Y=1) | Aktif olay | Emir (lot) | Not |
|---|---|---|---|---|---|---|---|---|---|
| AEFES | 17.69 | 0.599 | 1.000 |  |  |  | 3 | 0 |  |
| AKBNK | 68.30 | 0.304 | 1.000 |  |  |  | 1 | 0 |  |
| ASELS | 342.75 | 0.426 | 0.647 | evet | 0.659 | 0.590 | 1 | -2 |  |
| ASTOR | 165.90 | 0.571 | 0.571 |  |  |  | 1 | 0 |  |
| BIMAS | 385.50 | 0.675 | 0.843 | evet | 0.780 | 0.565 | 2 | -5 |  |
| EKGYO | 19.03 | 0.233 | 0.774 | evet | 0.291 | 0.533 | 2 | 0 |  |
| ENKAI | 77.90 | 0.644 | 0.900 | evet | 0.695 | 0.557 | 2 | -15 |  |
| EREGL | 37.18 | 0.399 | 0.865 | evet | 0.546 | 0.569 | 3 | 101 |  |
| FROTO | 68.45 | 1.000 | 1.000 | evet |  |  | 1 | 17 | eksik öznitelik: ret_skew |
| GARAN | 134.60 | 0.406 | 1.000 | evet | 0.412 | 0.533 | 2 | 6 |  |
| GUBRF | 373.25 | 0.333 | 0.801 | evet | 0.349 | 0.549 | 2 | 0 |  |
| ISCTR | 13.08 | 0.814 | 0.814 |  |  |  | 0 | 1404 |  |
| KCHOL | 208.40 | 0.564 | 0.947 | evet | 0.571 | 0.553 | 4 | -4 |  |
| KRDMD | 42.80 | 0.598 | 0.985 | evet | 0.622 | 0.574 | 3 | -16 |  |
| MGROS | 465.25 | 0.605 | 0.966 | evet | 0.605 | 0.560 | 3 | -2 |  |
| PETKM | 19.60 | 0.266 | 0.650 |  |  |  | 1 | 0 |  |
| PGSUS | 132.00 | 0.000 | 1.000 | evet | 0.000 | 0.484 | 3 | 0 |  |
| SAHOL | 89.20 | 0.470 | 0.893 | evet | 0.526 | 0.562 | 1 | -19 |  |
| SASA | 1.74 | 0.717 | 0.717 | evet |  |  | 2 | 0 | eksik öznitelik: volume_z |
| SISE | 36.24 | 0.406 | 0.815 |  |  |  | 1 | 18 |  |
| TAVHL | 286.25 | 0.566 | 0.982 | evet | 0.577 | 0.569 | 1 | -4 |  |
| TCELL | 97.65 | 0.494 | 1.000 |  |  |  | 2 | -12 |  |
| THYAO | 273.50 | 0.531 | 1.000 | evet | 0.528 | 0.560 | 2 | 0 |  |
| TOASO | 237.70 | 0.921 | 0.921 |  |  |  | 0 | 68 |  |
| TRALT | 41.72 | 0.319 | 0.867 |  |  |  | 2 | 0 |  |
| TRMET | 122.60 | 0.286 | 0.929 |  |  |  | 1 | 0 |  |
| TTKOM | 51.20 | 0.151 | 0.747 |  |  |  | 2 | 0 |  |
| TUPRS | 362.00 | 0.829 | 0.829 |  |  |  | 0 | 0 |  |
| VAKBN | 33.20 | 0.262 | 0.766 |  |  |  | 2 | 0 |  |
| YKBNK | 36.66 | 0.308 | 0.954 | evet | 0.327 | 0.537 | 2 | 142 |  |

## Bugünkü dolumlar (0)


_Sanal para; gerçek emir verilmez. Karar kuralları: `docs/preregistration/long_overlay.md`. Kilitli testte bu sistem 12 hissenin 9'unda B&H'nin gerisinde kaldı; bu çalışma ileriye dönük (görülmemiş veride) testtir._
