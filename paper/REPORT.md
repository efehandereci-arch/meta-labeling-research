# Paper trading — BIST 30 long meta-labeling overlay

Son işlem günü: **2026-10-12** · başlangıç 2026-09-25 · sanal sermaye 1,000,000 TL · komisyon 10 bps + kayma 5 bps / yön

| Portföy | Değer (TL) | Getiri | Sharpe (≥20 gün) | Max DD |
|---|---|---|---|---|
| Sistem | 971,134 | -2.89% | n/a | -3.8% |
| Buy&Hold (eşit ağırlık) | 962,343 | -3.77% | n/a | -5.4% |
| XU030 endeksi | 940,697 | -5.93% | n/a | -6.9% |

Sistemin yatırım oranı: 43% · nakit 553,888 TL · 12 gün

## Bugünkü kararlar

| Hisse | Kapanış | Maruziyet | Vol tavanı | Yeni olay | m | P(Y=1) | Aktif olay | Emir (lot) | Not |
|---|---|---|---|---|---|---|---|---|---|
| AEFES | 18.53 | 0.443 | 1.000 |  |  |  | 4 | 0 |  |
| AKBNK | 68.35 | 0.269 | 0.933 |  |  |  | 2 | 0 |  |
| ASELS | 341.75 | 0.434 | 0.664 |  |  |  | 1 | 3 |  |
| ASTOR | 197.50 | 0.551 | 0.551 |  |  |  | 2 | 4 |  |
| BIMAS | 396.50 | 1.000 | 1.000 |  |  |  | 2 | 0 |  |
| EKGYO | 19.73 | 0.246 | 0.785 |  |  |  | 2 | 35 |  |
| ENKAI | 80.95 | 0.642 | 0.870 | evet | 0.710 | 0.561 | 4 | 0 |  |
| EREGL | 37.60 | 0.279 | 0.868 | evet | 0.135 | 0.511 | 4 | -34 |  |
| FROTO | 73.85 | 1.000 | 1.000 |  |  |  | 1 | 0 |  |
| GARAN | 129.80 | 0.347 | 1.000 |  |  |  | 1 | 0 |  |
| GUBRF | 403.75 | 0.294 | 0.821 | evet | 0.353 | 0.548 | 4 | 0 |  |
| ISCTR | 12.70 | 0.298 | 0.748 |  |  |  | 2 | 0 |  |
| KCHOL | 206.90 | 0.582 | 0.946 | evet | 0.585 | 0.553 | 4 | 0 |  |
| KRDMD | 44.06 | 0.549 | 0.971 |  |  |  | 3 | 0 |  |
| MGROS | 501.00 | 0.548 | 0.999 |  |  |  | 3 | 2 |  |
| PETKM | 20.28 | 0.227 | 0.602 |  |  |  | 2 | 37 |  |
| PGSUS | 132.90 | 0.000 | 1.000 | evet | 0.000 | 0.461 | 2 | 0 |  |
| SAHOL | 84.35 | 0.486 | 0.862 |  |  |  | 2 | 0 |  |
| SASA | 1.87 | 0.676 | 0.676 |  |  |  | 3 | 0 |  |
| SISE | 37.60 | 0.352 | 0.760 |  |  |  | 2 | 0 |  |
| TAVHL | 266.50 | 0.559 | 0.957 | evet | 0.551 | 0.567 | 2 | -4 |  |
| TCELL | 97.25 | 0.504 | 1.000 |  |  |  | 2 | 0 |  |
| THYAO | 285.75 | 0.478 | 1.000 |  |  |  | 3 | 0 |  |
| TOASO | 259.25 | 0.458 | 0.894 | evet | 0.491 | 0.556 | 4 | 0 |  |
| TRALT | 43.48 | 0.286 | 0.847 |  |  |  | 3 | 0 |  |
| TRMET | 135.40 | 0.290 | 0.933 |  |  |  | 2 | 0 |  |
| TTKOM | 51.85 | 0.141 | 0.695 | evet | 0.207 | 0.529 | 3 | 0 |  |
| TUPRS | 384.75 | 0.834 | 0.834 |  |  |  | 4 | 0 |  |
| VAKBN | 34.44 | 0.227 | 0.705 | evet | 0.350 | 0.542 | 2 | 29 |  |
| YKBNK | 35.70 | 0.140 | 0.877 |  |  |  | 2 | 0 |  |

## Bugünkü dolumlar (12)

- sistem ASTOR: -10 lot @ 206.90 (maliyet 2 TL)
- sistem ENKAI: -12 lot @ 83.41 (maliyet 1 TL)
- sistem TCELL: -19 lot @ 98.60 (maliyet 2 TL)
- sistem AEFES: +103 lot @ 18.61 (maliyet 2 TL)
- sistem AKBNK: +13 lot @ 67.93 (maliyet 1 TL)
- sistem ISCTR: +60 lot @ 12.70 (maliyet 1 TL)
- sistem KCHOL: +5 lot @ 208.00 (maliyet 1 TL)
- sistem KRDMD: +24 lot @ 43.30 (maliyet 1 TL)
- sistem SAHOL: +91 lot @ 83.64 (maliyet 8 TL)
- sistem SISE: +26 lot @ 38.18 (maliyet 1 TL)
- sistem TAVHL: +5 lot @ 274.64 (maliyet 1 TL)
- sistem YKBNK: +125 lot @ 35.50 (maliyet 4 TL)

_Sanal para; gerçek emir verilmez. Karar kuralları: `docs/preregistration/long_overlay.md`. Kilitli testte bu sistem 12 hissenin 9'unda B&H'nin gerisinde kaldı; bu çalışma ileriye dönük (görülmemiş veride) testtir._
