# Paper trading — BIST 30 long meta-labeling overlay

Son işlem günü: **2026-10-30** · başlangıç 2026-09-25 · sanal sermaye 1,000,000 TL · komisyon 10 bps + kayma 5 bps / yön

| Portföy | Değer (TL) | Getiri | Sharpe (≥20 gün) | Max DD |
|---|---|---|---|---|
| Sistem | 908,663 | -9.13% | -6.91 | -9.1% |
| Buy&Hold (eşit ağırlık) | 830,143 | -16.99% | -6.91 | -17.0% |
| XU030 endeksi | 841,518 | -15.85% | -6.08 | -15.8% |

Sistemin yatırım oranı: 42% · nakit 531,427 TL · 25 gün

## Bugünkü kararlar

| Hisse | Kapanış | Maruziyet | Vol tavanı | Yeni olay | m | P(Y=1) | Aktif olay | Emir (lot) | Not |
|---|---|---|---|---|---|---|---|---|---|
| AEFES | 15.43 | 0.453 | 0.972 | evet | 0.466 | 0.558 | 1 | -218 |  |
| AKBNK | 60.90 | 0.273 | 0.991 | evet | 0.353 | 0.530 | 2 | 16 |  |
| ASELS | 347.00 | 0.456 | 0.686 |  |  |  | 2 | 0 |  |
| ASTOR | 158.90 | 0.510 | 0.510 | evet |  | 0.278 | 2 | 4 | conformal ısınma |
| BIMAS | 347.50 | 0.738 | 0.803 | evet | 0.838 | 0.576 | 2 | 0 |  |
| EKGYO | 16.19 | 0.218 | 0.768 | evet | 0.291 | 0.534 | 2 | 0 |  |
| ENKAI | 76.65 | 0.581 | 0.898 | evet | 0.655 | 0.553 | 3 | 0 |  |
| EREGL | 29.66 | 0.307 | 0.674 | evet | 0.434 | 0.570 | 2 | 0 |  |
| FROTO | 65.45 | 0.627 | 0.986 | evet | 0.636 | 0.545 | 1 | -17 |  |
| GARAN | 125.20 | 0.428 | 1.000 | evet | 0.442 | 0.534 | 2 | 0 |  |
| GUBRF | 250.25 | 0.260 | 0.630 | evet | 0.413 | 0.587 | 1 | -42 |  |
| ISCTR | 11.65 | 0.230 | 0.846 | evet | 0.272 | 0.531 | 1 | 168 |  |
| KCHOL | 192.80 | 0.524 | 0.939 | evet | 0.545 | 0.549 | 2 | 0 |  |
| KRDMD | 36.16 | 0.480 | 0.878 | evet | 0.549 | 0.573 | 2 | 0 |  |
| MGROS | 413.50 | 0.660 | 1.000 | evet | 0.660 | 0.565 | 1 | 3 |  |
| PETKM | 16.24 | 0.404 | 0.658 | evet | 0.614 | 0.593 | 1 | 143 |  |
| PGSUS | 115.00 | 0.823 | 1.000 | evet | 0.823 | 0.589 | 1 | 197 |  |
| SAHOL | 81.10 | 0.374 | 0.947 | evet | 0.478 | 0.550 | 2 | -17 |  |
| SASA | 1.45 | 0.795 | 0.795 | evet |  |  | 2 | 0 | eksik öznitelik: volume_z |
| SISE | 32.04 | 0.397 | 0.810 | evet | 0.490 | 0.549 | 1 | 0 |  |
| TAVHL | 250.00 | 0.429 | 0.878 |  |  |  | 1 | 0 |  |
| TCELL | 90.10 | 0.423 | 1.000 |  |  |  | 1 | 0 |  |
| THYAO | 242.20 | 0.596 | 1.000 | evet | 0.596 | 0.569 | 1 | 6 |  |
| TOASO | 211.20 | 0.333 | 0.778 | evet | 0.428 | 0.557 | 1 | -11 |  |
| TRALT | 32.42 | 0.210 | 0.726 | evet | 0.289 | 0.522 | 1 | -32 |  |
| TRMET | 94.05 | 0.201 | 0.776 | evet | 0.259 | 0.522 | 1 | 0 |  |
| TTKOM | 46.16 | 0.181 | 0.759 |  |  |  | 3 | 0 |  |
| TUPRS | 343.50 | 0.575 | 0.879 | evet | 0.790 | 0.586 | 3 | 5 |  |
| VAKBN | 28.88 | 0.057 | 0.765 | evet | 0.000 | 0.469 | 2 | -132 |  |
| YKBNK | 33.96 | 0.341 | 0.986 |  |  |  | 2 | 0 |  |

## Bugünkü dolumlar (6)

- sistem AKBNK: -17 lot @ 62.22 (maliyet 1 TL)
- sistem ASELS: -3 lot @ 357.57 (maliyet 1 TL)
- sistem PGSUS: -12 lot @ 120.74 (maliyet 1 TL)
- sistem SAHOL: -35 lot @ 81.96 (maliyet 3 TL)
- sistem TUPRS: -11 lot @ 354.82 (maliyet 4 TL)
- sistem SASA: +606 lot @ 1.47 (maliyet 1 TL)

_Sanal para; gerçek emir verilmez. Karar kuralları: `docs/preregistration/long_overlay.md`. Kilitli testte bu sistem 12 hissenin 9'unda B&H'nin gerisinde kaldı; bu çalışma ileriye dönük (görülmemiş veride) testtir._
