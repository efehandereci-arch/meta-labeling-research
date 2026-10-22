# Paper trading — BIST 30 long meta-labeling overlay

Son işlem günü: **2026-10-22** · başlangıç 2026-09-25 · sanal sermaye 1,000,000 TL · komisyon 10 bps + kayma 5 bps / yön

| Portföy | Değer (TL) | Getiri | Sharpe (≥20 gün) | Max DD |
|---|---|---|---|---|
| Sistem | 930,514 | -6.95% | n/a | -6.9% |
| Buy&Hold (eşit ağırlık) | 883,420 | -11.66% | n/a | -11.7% |
| XU030 endeksi | 878,589 | -12.14% | n/a | -12.1% |

Sistemin yatırım oranı: 47% · nakit 497,208 TL · 20 gün

## Bugünkü kararlar

| Hisse | Kapanış | Maruziyet | Vol tavanı | Yeni olay | m | P(Y=1) | Aktif olay | Emir (lot) | Not |
|---|---|---|---|---|---|---|---|---|---|
| AEFES | 16.27 | 0.657 | 0.969 | evet | 0.595 | 0.571 | 2 | 0 |  |
| AKBNK | 64.60 | 0.290 | 0.979 | evet | 0.289 | 0.520 | 2 | 0 |  |
| ASELS | 338.25 | 0.440 | 0.668 |  |  |  | 1 | 0 |  |
| ASTOR | 150.00 | 0.583 | 0.583 |  |  |  | 2 | 5 |  |
| BIMAS | 369.00 | 0.661 | 0.820 | evet | 0.818 | 0.571 | 3 | 0 |  |
| EKGYO | 17.75 | 0.219 | 0.763 | evet | 0.287 | 0.532 | 1 | 0 |  |
| ENKAI | 73.50 | 0.579 | 0.888 | evet | 0.661 | 0.554 | 2 | -19 |  |
| EREGL | 35.10 | 0.529 | 0.847 | evet | 0.816 | 0.609 | 2 | 99 |  |
| FROTO | 66.55 | 1.000 | 1.000 |  |  |  | 2 | 0 |  |
| GARAN | 128.50 | 0.407 | 1.000 | evet | 0.415 | 0.534 | 2 | 0 |  |
| GUBRF | 331.50 | 0.280 | 0.761 | evet | 0.480 | 0.582 | 2 | 0 |  |
| ISCTR | 12.42 | 0.172 | 0.812 | evet | 0.212 | 0.523 | 1 | -1552 |  |
| KCHOL | 196.10 | 0.525 | 0.914 | evet | 0.571 | 0.555 | 3 | -4 |  |
| KRDMD | 39.88 | 0.587 | 0.952 | evet | 0.602 | 0.574 | 2 | 0 |  |
| MGROS | 440.50 | 0.594 | 0.968 | evet | 0.628 | 0.564 | 3 | 0 |  |
| PETKM | 18.30 | 0.248 | 0.654 | evet | 0.375 | 0.550 | 2 | 0 |  |
| PGSUS | 126.40 | 0.127 | 1.000 | evet | 0.191 | 0.509 | 3 | 20 |  |
| SAHOL | 87.55 | 0.486 | 0.924 |  |  |  | 1 | 0 |  |
| SASA | 1.64 | 0.731 | 0.731 |  |  |  | 3 | 570 |  |
| SISE | 34.08 | 0.399 | 0.813 | evet | 0.501 | 0.549 | 2 | 0 |  |
| TAVHL | 267.00 | 0.417 | 0.843 | evet | 0.495 | 0.568 | 1 | -15 |  |
| TCELL | 93.30 | 0.500 | 1.000 |  |  |  | 2 | 0 |  |
| THYAO | 259.00 | 0.541 | 1.000 | evet | 0.542 | 0.563 | 2 | 0 |  |
| TOASO | 223.70 | 0.472 | 0.918 |  |  |  | 1 | 0 |  |
| TRALT | 36.48 | 0.247 | 0.765 | evet | 0.323 | 0.525 | 1 | -41 |  |
| TRMET | 106.20 | 0.227 | 0.821 | evet | 0.277 | 0.523 | 1 | -9 |  |
| TTKOM | 47.38 | 0.178 | 0.720 | evet | 0.275 | 0.538 | 2 | 21 |  |
| TUPRS | 352.25 | 0.647 | 0.853 | evet | 0.759 | 0.584 | 1 | -17 |  |
| VAKBN | 31.14 | 0.260 | 0.766 | evet | 0.343 | 0.537 | 2 | 0 |  |
| YKBNK | 35.32 | 0.318 | 0.962 | evet | 0.346 | 0.540 | 3 | 0 |  |

## Bugünkü dolumlar (9)

- sistem GUBRF: -3 lot @ 350.57 (maliyet 1 TL)
- sistem TOASO: -59 lot @ 227.09 (maliyet 13 TL)
- sistem AEFES: +218 lot @ 16.78 (maliyet 4 TL)
- sistem ASTOR: +8 lot @ 155.68 (maliyet 1 TL)
- sistem EREGL: +26 lot @ 36.54 (maliyet 1 TL)
- sistem KRDMD: +23 lot @ 41.92 (maliyet 1 TL)
- sistem PGSUS: +11 lot @ 128.56 (maliyet 1 TL)
- sistem THYAO: +4 lot @ 266.13 (maliyet 1 TL)
- sistem TRALT: +19 lot @ 39.80 (maliyet 1 TL)

_Sanal para; gerçek emir verilmez. Karar kuralları: `docs/preregistration/long_overlay.md`. Kilitli testte bu sistem 12 hissenin 9'unda B&H'nin gerisinde kaldı; bu çalışma ileriye dönük (görülmemiş veride) testtir._
