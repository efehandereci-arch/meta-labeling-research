# Paper trading — BIST 30 long meta-labeling overlay

Son işlem günü: **2026-11-13** · başlangıç 2026-09-25 · sanal sermaye 1,000,000 TL · komisyon 10 bps + kayma 5 bps / yön

| Portföy | Değer (TL) | Getiri | Sharpe (≥20 gün) | Max DD |
|---|---|---|---|---|
| Sistem | 952,306 | -4.77% | -2.37 | -9.1% |
| Buy&Hold (eşit ağırlık) | 933,910 | -6.61% | -1.50 | -17.0% |
| XU030 endeksi | 930,877 | -6.91% | -1.60 | -15.8% |

Sistemin yatırım oranı: 36% · nakit 610,191 TL · 35 gün

## Bugünkü kararlar

| Hisse | Kapanış | Maruziyet | Vol tavanı | Yeni olay | m | P(Y=1) | Aktif olay | Emir (lot) | Not |
|---|---|---|---|---|---|---|---|---|---|
| AEFES | 16.55 | 0.403 | 1.000 |  |  |  | 2 | 0 |  |
| AKBNK | 69.95 | 0.274 | 0.940 |  |  |  | 2 | 11 |  |
| ASELS | 345.50 | 0.514 | 0.736 |  |  |  | 2 | 0 |  |
| ASTOR | 163.80 | 0.491 | 0.491 | evet |  | 0.324 | 4 | 7 | conformal ısınma |
| BIMAS | 395.50 | 0.469 | 0.829 |  |  |  | 2 | 12 |  |
| EKGYO | 18.56 | 0.203 | 0.796 |  |  |  | 1 | 0 |  |
| ENKAI | 83.40 | 0.607 | 0.978 |  |  |  | 2 | 0 |  |
| EREGL | 32.70 | 0.265 | 0.681 | evet | 0.395 | 0.564 | 3 | 0 |  |
| FROTO | 73.75 | 0.421 | 0.865 |  |  |  | 2 | 10 |  |
| GARAN | 150.30 | 0.357 | 0.972 | evet | 0.379 | 0.534 | 2 | 7 |  |
| GUBRF | 284.50 | 0.141 | 0.609 |  |  |  | 3 | 0 |  |
| ISCTR | 13.55 | 0.315 | 0.853 |  |  |  | 2 | 63 |  |
| KCHOL | 207.50 | 0.524 | 0.940 |  |  |  | 2 | 0 |  |
| KRDMD | 38.90 | 0.333 | 0.764 |  |  |  | 2 | 0 |  |
| MGROS | 475.75 | 0.451 | 0.939 |  |  |  | 2 | 2 |  |
| PETKM | 16.66 | 0.406 | 0.694 |  |  |  | 2 | 39 |  |
| PGSUS | 155.30 | 0.505 | 0.905 |  |  |  | 1 | 0 |  |
| SAHOL | 85.20 | 0.431 | 0.969 |  |  |  | 2 | 0 |  |
| SASA | 1.59 | 0.758 | 0.758 |  |  |  | 2 | 0 |  |
| SISE | 35.86 | 0.382 | 0.797 |  |  |  | 4 | 18 |  |
| TAVHL | 302.25 | 0.393 | 0.865 |  |  |  | 2 | 3 |  |
| TCELL | 97.00 | 0.343 | 0.919 |  |  |  | 1 | 0 |  |
| THYAO | 320.25 | 0.330 | 0.861 |  |  |  | 2 | 0 |  |
| TOASO | 243.00 | 0.258 | 0.708 | evet | 0.376 | 0.553 | 2 | 3 |  |
| TRALT | 38.18 | 0.188 | 0.718 |  |  |  | 2 | 0 |  |
| TRMET | 110.80 | 0.197 | 0.795 |  |  |  | 3 | 0 |  |
| TTKOM | 51.40 | 0.167 | 0.788 |  |  |  | 2 | 0 |  |
| TUPRS | 359.00 | 0.648 | 0.882 | evet | 0.734 | 0.583 | 1 | -3 |  |
| VAKBN | 33.24 | 0.265 | 0.804 |  |  |  | 1 | 0 |  |
| YKBNK | 37.78 | 0.335 | 0.986 | evet | 0.350 | 0.538 | 3 | 0 |  |

## Bugünkü dolumlar (11)

- sistem ASTOR: -13 lot @ 177.91 (maliyet 2 TL)
- sistem THYAO: -2 lot @ 315.59 (maliyet 1 TL)
- sistem TUPRS: -6 lot @ 361.32 (maliyet 2 TL)
- sistem AEFES: +60 lot @ 16.52 (maliyet 1 TL)
- sistem ASELS: +2 lot @ 344.67 (maliyet 1 TL)
- sistem BIMAS: +15 lot @ 388.19 (maliyet 6 TL)
- sistem ENKAI: +27 lot @ 82.29 (maliyet 2 TL)
- sistem PGSUS: +51 lot @ 156.28 (maliyet 8 TL)
- sistem SAHOL: +9 lot @ 84.54 (maliyet 1 TL)
- sistem SASA: +521 lot @ 1.59 (maliyet 1 TL)
- sistem YKBNK: +19 lot @ 37.82 (maliyet 1 TL)

_Sanal para; gerçek emir verilmez. Karar kuralları: `docs/preregistration/long_overlay.md`. Kilitli testte bu sistem 12 hissenin 9'unda B&H'nin gerisinde kaldı; bu çalışma ileriye dönük (görülmemiş veride) testtir._
