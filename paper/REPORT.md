# Paper trading — BIST 30 long meta-labeling overlay

Son işlem günü: **2026-10-07** · başlangıç 2026-09-25 · sanal sermaye 1,000,000 TL · komisyon 10 bps + kayma 5 bps / yön

| Portföy | Değer (TL) | Getiri | Sharpe (≥20 gün) | Max DD |
|---|---|---|---|---|
| Sistem | 968,564 | -3.14% | n/a | -3.8% |
| Buy&Hold (eşit ağırlık) | 959,029 | -4.10% | n/a | -5.4% |
| XU030 endeksi | 941,481 | -5.85% | n/a | -6.9% |

Sistemin yatırım oranı: 44% · nakit 545,706 TL · 9 gün

## Bugünkü kararlar

| Hisse | Kapanış | Maruziyet | Vol tavanı | Yeni olay | m | P(Y=1) | Aktif olay | Emir (lot) | Not |
|---|---|---|---|---|---|---|---|---|---|
| AEFES | 18.15 | 0.376 | 0.968 | evet | 0.515 | 0.560 | 3 | 115 |  |
| AKBNK | 69.25 | 0.256 | 0.889 |  |  |  | 2 | 0 |  |
| ASELS | 348.75 | 0.414 | 0.633 | evet | 0.653 | 0.591 | 1 | -3 |  |
| ASTOR | 184.90 | 0.552 | 0.552 | evet |  | 0.485 | 2 | 8 | conformal ısınma |
| BIMAS | 394.25 | 1.000 | 1.000 | evet | 1.000 | 0.607 | 1 | 3 |  |
| EKGYO | 19.60 | 0.233 | 0.744 |  |  |  | 2 | 0 |  |
| ENKAI | 80.00 | 0.676 | 0.892 | evet | 0.754 | 0.563 | 3 | 0 |  |
| EREGL | 36.52 | 0.321 | 0.835 | evet | 0.407 | 0.551 | 3 | 0 |  |
| FROTO | 73.85 | 1.000 | 1.000 | evet |  |  | 1 | 0 | eksik öznitelik: ret_skew |
| GARAN | 129.90 | 0.335 | 0.965 |  |  |  | 1 | 0 |  |
| GUBRF | 396.75 | 0.287 | 0.814 | evet | 0.391 | 0.556 | 2 | 4 |  |
| ISCTR | 12.97 | 0.282 | 0.709 |  |  |  | 2 | 0 |  |
| KCHOL | 209.60 | 0.573 | 0.916 | evet | 0.643 | 0.567 | 3 | 0 |  |
| KRDMD | 42.92 | 0.524 | 0.927 | evet | 0.567 | 0.573 | 3 | 0 |  |
| MGROS | 499.00 | 0.519 | 0.947 | evet | 0.558 | 0.558 | 4 | 2 |  |
| PETKM | 20.10 | 0.217 | 0.575 |  |  |  | 2 | 0 |  |
| PGSUS | 136.50 | 0.000 | 1.000 | evet | 0.000 | 0.473 | 1 | -228 |  |
| SAHOL | 87.60 | 0.268 | 0.936 |  |  |  | 2 | 0 |  |
| SASA | 1.85 | 0.656 | 0.656 | evet |  |  | 2 | 370 | eksik öznitelik: volume_z |
| SISE | 37.56 | 0.334 | 0.721 |  |  |  | 2 | 0 |  |
| TAVHL | 275.25 | 0.580 | 0.938 |  |  |  | 1 | 0 |  |
| TCELL | 99.40 | 0.584 | 0.971 |  |  |  | 1 | 0 |  |
| THYAO | 286.25 | 0.478 | 1.000 | evet | 0.421 | 0.552 | 3 | -3 |  |
| TOASO | 262.50 | 0.453 | 0.873 | evet | 0.503 | 0.558 | 3 | 0 |  |
| TRALT | 41.34 | 0.274 | 0.839 | evet | 0.341 | 0.525 | 2 | 21 |  |
| TRMET | 126.50 | 0.290 | 0.939 |  |  |  | 1 | 0 |  |
| TTKOM | 52.15 | 0.132 | 0.657 |  |  |  | 2 | 0 |  |
| TUPRS | 379.75 | 0.815 | 0.815 |  |  |  | 4 | 2 |  |
| VAKBN | 33.68 | 0.196 | 0.667 |  |  |  | 1 | 0 |  |
| YKBNK | 36.60 | 0.000 | 0.843 |  |  |  | 1 | 0 |  |

## Bugünkü dolumlar (6)

- sistem AEFES: -470 lot @ 18.79 (maliyet 9 TL)
- sistem ASELS: -17 lot @ 377.06 (maliyet 6 TL)
- sistem TOASO: -3 lot @ 270.86 (maliyet 1 TL)
- sistem YKBNK: -105 lot @ 36.26 (maliyet 4 TL)
- sistem SASA: +598 lot @ 1.91 (maliyet 1 TL)
- sistem TTKOM: +14 lot @ 53.13 (maliyet 1 TL)

_Sanal para; gerçek emir verilmez. Karar kuralları: `docs/preregistration/long_overlay.md`. Kilitli testte bu sistem 12 hissenin 9'unda B&H'nin gerisinde kaldı; bu çalışma ileriye dönük (görülmemiş veride) testtir._
