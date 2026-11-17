# Paper trading — BIST 30 long meta-labeling overlay

Son işlem günü: **2026-11-16** · başlangıç 2026-09-25 · sanal sermaye 1,000,000 TL · komisyon 10 bps + kayma 5 bps / yön

| Portföy | Değer (TL) | Getiri | Sharpe (≥20 gün) | Max DD |
|---|---|---|---|---|
| Sistem | 951,398 | -4.86% | -2.39 | -9.1% |
| Buy&Hold (eşit ağırlık) | 932,558 | -6.74% | -1.51 | -17.0% |
| XU030 endeksi | 930,677 | -6.93% | -1.59 | -15.8% |

Sistemin yatırım oranı: 37% · nakit 598,091 TL · 36 gün

## Bugünkü kararlar

| Hisse | Kapanış | Maruziyet | Vol tavanı | Yeni olay | m | P(Y=1) | Aktif olay | Emir (lot) | Not |
|---|---|---|---|---|---|---|---|---|---|
| AEFES | 16.50 | 0.412 | 1.000 |  |  |  | 1 | 0 |  |
| AKBNK | 69.90 | 0.280 | 0.959 |  |  |  | 2 | 0 |  |
| ASELS | 353.00 | 0.744 | 0.744 |  |  |  | 0 | 20 |  |
| ASTOR | 163.20 | 0.501 | 0.501 |  |  |  | 4 | 0 |  |
| BIMAS | 394.50 | 0.478 | 0.846 |  |  |  | 2 | 0 |  |
| EKGYO | 18.55 | 0.207 | 0.812 |  |  |  | 1 | 0 |  |
| ENKAI | 82.70 | 0.752 | 0.993 |  |  |  | 1 | 56 |  |
| EREGL | 32.22 | 0.270 | 0.693 |  |  |  | 3 | 23 |  |
| FROTO | 73.00 | 0.428 | 0.880 |  |  |  | 2 | 0 |  |
| GARAN | 150.10 | 0.364 | 0.991 |  |  |  | 2 | 0 |  |
| GUBRF | 290.25 | 0.143 | 0.616 |  |  |  | 3 | 0 |  |
| ISCTR | 13.34 | 0.367 | 0.862 | evet | 0.541 | 0.571 | 3 | 137 |  |
| KCHOL | 205.50 | 0.533 | 0.956 |  |  |  | 2 | 4 |  |
| KRDMD | 38.50 | 0.339 | 0.778 |  |  |  | 2 | 22 |  |
| MGROS | 468.75 | 0.473 | 0.951 | evet | 0.532 | 0.554 | 3 | 0 |  |
| PETKM | 16.47 | 0.414 | 0.708 |  |  |  | 2 | 0 |  |
| PGSUS | 157.50 | 0.514 | 0.921 |  |  |  | 1 | 0 |  |
| SAHOL | 84.70 | 0.439 | 0.988 |  |  |  | 2 | 0 |  |
| SASA | 1.59 | 0.773 | 0.773 |  |  |  | 2 | 665 |  |
| SISE | 34.84 | 0.384 | 0.796 | evet | 0.491 | 0.549 | 5 | 0 |  |
| TAVHL | 304.00 | 0.401 | 0.882 |  |  |  | 2 | 0 |  |
| TCELL | 96.00 | 0.348 | 0.933 |  |  |  | 1 | 0 |  |
| THYAO | 323.50 | 0.337 | 0.878 |  |  |  | 2 | 0 |  |
| TOASO | 246.00 | 0.263 | 0.721 |  |  |  | 2 | 0 |  |
| TRALT | 38.76 | 0.191 | 0.729 |  |  |  | 2 | 0 |  |
| TRMET | 115.20 | 0.199 | 0.794 | evet | 0.259 | 0.521 | 4 | 0 |  |
| TTKOM | 51.20 | 0.170 | 0.803 |  |  |  | 2 | 0 |  |
| TUPRS | 356.00 | 0.659 | 0.898 |  |  |  | 1 | 0 |  |
| VAKBN | 33.20 | 0.270 | 0.820 |  |  |  | 1 | 0 |  |
| YKBNK | 37.48 | 0.339 | 1.000 |  |  |  | 3 | 0 |  |

## Bugünkü dolumlar (12)

- sistem TUPRS: -3 lot @ 357.82 (maliyet 1 TL)
- sistem AKBNK: +11 lot @ 69.68 (maliyet 1 TL)
- sistem ASTOR: +7 lot @ 165.08 (maliyet 1 TL)
- sistem BIMAS: +12 lot @ 394.20 (maliyet 5 TL)
- sistem FROTO: +10 lot @ 73.64 (maliyet 1 TL)
- sistem GARAN: +7 lot @ 150.07 (maliyet 1 TL)
- sistem ISCTR: +63 lot @ 13.47 (maliyet 1 TL)
- sistem MGROS: +2 lot @ 475.24 (maliyet 1 TL)
- sistem PETKM: +39 lot @ 16.71 (maliyet 1 TL)
- sistem SISE: +18 lot @ 35.68 (maliyet 1 TL)
- sistem TAVHL: +3 lot @ 301.40 (maliyet 1 TL)
- sistem TOASO: +3 lot @ 241.22 (maliyet 1 TL)

_Sanal para; gerçek emir verilmez. Karar kuralları: `docs/preregistration/long_overlay.md`. Kilitli testte bu sistem 12 hissenin 9'unda B&H'nin gerisinde kaldı; bu çalışma ileriye dönük (görülmemiş veride) testtir._
