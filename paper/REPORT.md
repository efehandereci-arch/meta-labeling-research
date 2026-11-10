# Paper trading — BIST 30 long meta-labeling overlay

Son işlem günü: **2026-11-09** · başlangıç 2026-09-25 · sanal sermaye 1,000,000 TL · komisyon 10 bps + kayma 5 bps / yön

| Portföy | Değer (TL) | Getiri | Sharpe (≥20 gün) | Max DD |
|---|---|---|---|---|
| Sistem | 949,251 | -5.07% | -2.71 | -9.1% |
| Buy&Hold (eşit ağırlık) | 931,031 | -6.90% | -1.69 | -17.0% |
| XU030 endeksi | 916,222 | -8.38% | -2.14 | -15.8% |

Sistemin yatırım oranı: 36% · nakit 605,542 TL · 31 gün

## Bugünkü kararlar

| Hisse | Kapanış | Maruziyet | Vol tavanı | Yeni olay | m | P(Y=1) | Aktif olay | Emir (lot) | Not |
|---|---|---|---|---|---|---|---|---|---|
| AEFES | 16.94 | 0.382 | 0.949 |  |  |  | 2 | 0 |  |
| AKBNK | 70.95 | 0.254 | 0.872 | evet | 0.230 | 0.516 | 2 | 12 |  |
| ASELS | 337.75 | 0.478 | 0.685 |  |  |  | 2 | 0 |  |
| ASTOR | 155.10 | 0.499 | 0.499 |  |  |  | 4 | 6 |  |
| BIMAS | 381.50 | 0.126 | 0.802 | evet | 0.314 | 0.511 | 2 | -31 |  |
| EKGYO | 18.32 | 0.202 | 0.747 | evet | 0.256 | 0.528 | 2 | 0 |  |
| ENKAI | 80.60 | 0.522 | 0.923 |  |  |  | 2 | 12 |  |
| EREGL | 32.76 | 0.252 | 0.652 | evet | 0.294 | 0.548 | 2 | -44 |  |
| FROTO | 74.45 | 0.365 | 0.835 |  |  |  | 1 | 0 |  |
| GARAN | 153.10 | 0.330 | 0.926 | evet | 0.357 | 0.534 | 1 | -11 |  |
| GUBRF | 307.00 | 0.137 | 0.583 | evet | 0.242 | 0.549 | 2 | -4 |  |
| ISCTR | 13.70 | 0.291 | 0.790 | evet | 0.275 | 0.533 | 2 | -147 |  |
| KCHOL | 212.40 | 0.516 | 0.924 | evet | 0.559 | 0.552 | 1 | 0 |  |
| KRDMD | 37.38 | 0.308 | 0.715 |  |  |  | 1 | 0 |  |
| MGROS | 480.50 | 0.427 | 0.890 | evet | 0.455 | 0.548 | 2 | -2 |  |
| PETKM | 16.73 | 0.377 | 0.645 |  |  |  | 2 | 0 |  |
| PGSUS | 146.50 | 0.279 | 0.909 | evet | 0.000 | 0.437 | 2 | 0 |  |
| SAHOL | 88.40 | 0.410 | 0.922 |  |  |  | 2 | 0 |  |
| SASA | 1.63 | 0.715 | 0.715 |  |  |  | 2 | 0 |  |
| SISE | 35.48 | 0.360 | 0.751 | evet | 0.469 | 0.551 | 4 | -18 |  |
| TAVHL | 303.75 | 0.366 | 0.805 | evet | 0.463 | 0.566 | 2 | 0 |  |
| TCELL | 92.10 | 0.457 | 1.000 | evet | 0.459 | 0.553 | 4 | 0 |  |
| THYAO | 310.00 | 0.336 | 0.798 | evet | 0.422 | 0.574 | 1 | 4 |  |
| TOASO | 245.60 | 0.241 | 0.684 |  |  |  | 1 | 0 |  |
| TRALT | 40.24 | 0.174 | 0.677 | evet | 0.257 | 0.520 | 1 | 0 |  |
| TRMET | 115.90 | 0.186 | 0.757 | evet | 0.248 | 0.522 | 2 | 0 |  |
| TTKOM | 49.26 | 0.166 | 0.779 |  |  |  | 3 | 0 |  |
| TUPRS | 332.25 | 0.695 | 0.918 |  |  |  | 2 | 2 |  |
| VAKBN | 33.62 | 0.251 | 0.762 |  |  |  | 1 | 0 |  |
| YKBNK | 38.74 | 0.308 | 0.922 | evet | 0.338 | 0.541 | 2 | -21 |  |

## Bugünkü dolumlar (11)

- sistem ASTOR: -10 lot @ 163.22 (maliyet 2 TL)
- sistem FROTO: -104 lot @ 73.16 (maliyet 8 TL)
- sistem GARAN: -5 lot @ 144.93 (maliyet 1 TL)
- sistem TOASO: -12 lot @ 242.78 (maliyet 3 TL)
- sistem AEFES: +42 lot @ 16.89 (maliyet 1 TL)
- sistem AKBNK: +39 lot @ 68.93 (maliyet 3 TL)
- sistem ASELS: +2 lot @ 333.42 (maliyet 1 TL)
- sistem BIMAS: +2 lot @ 373.19 (maliyet 1 TL)
- sistem SASA: +1028 lot @ 1.59 (maliyet 2 TL)
- sistem SISE: +19 lot @ 34.46 (maliyet 1 TL)
- sistem VAKBN: +57 lot @ 33.20 (maliyet 2 TL)

_Sanal para; gerçek emir verilmez. Karar kuralları: `docs/preregistration/long_overlay.md`. Kilitli testte bu sistem 12 hissenin 9'unda B&H'nin gerisinde kaldı; bu çalışma ileriye dönük (görülmemiş veride) testtir._
