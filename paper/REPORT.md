# Paper trading — BIST 30 long meta-labeling overlay

Son işlem günü: **2026-11-12** · başlangıç 2026-09-25 · sanal sermaye 1,000,000 TL · komisyon 10 bps + kayma 5 bps / yön

| Portföy | Değer (TL) | Getiri | Sharpe (≥20 gün) | Max DD |
|---|---|---|---|---|
| Sistem | 952,911 | -4.71% | -2.37 | -9.1% |
| Buy&Hold (eşit ağırlık) | 933,698 | -6.63% | -1.53 | -17.0% |
| XU030 endeksi | 929,040 | -7.10% | -1.68 | -15.8% |

Sistemin yatırım oranı: 34% · nakit 625,108 TL · 34 gün

## Bugünkü kararlar

| Hisse | Kapanış | Maruziyet | Vol tavanı | Yeni olay | m | P(Y=1) | Aktif olay | Emir (lot) | Not |
|---|---|---|---|---|---|---|---|---|---|
| AEFES | 16.59 | 0.397 | 0.984 |  |  |  | 2 | 60 |  |
| AKBNK | 70.10 | 0.269 | 0.922 |  |  |  | 2 | 0 |  |
| ASELS | 344.75 | 0.504 | 0.722 |  |  |  | 2 | 2 |  |
| ASTOR | 177.20 | 0.496 | 0.496 | evet |  | 0.324 | 4 | -13 | conformal ısınma |
| BIMAS | 388.00 | 0.311 | 0.824 | evet | 0.818 | 0.574 | 3 | 15 |  |
| EKGYO | 18.81 | 0.200 | 0.783 |  |  |  | 1 | 0 |  |
| ENKAI | 82.35 | 0.600 | 0.966 | evet | 0.757 | 0.559 | 2 | 27 |  |
| EREGL | 32.06 | 0.261 | 0.675 |  |  |  | 2 | 0 |  |
| FROTO | 73.35 | 0.413 | 0.849 |  |  |  | 2 | 0 |  |
| GARAN | 152.60 | 0.344 | 0.965 |  |  |  | 1 | 0 |  |
| GUBRF | 280.50 | 0.139 | 0.600 |  |  |  | 3 | 0 |  |
| ISCTR | 13.63 | 0.309 | 0.837 |  |  |  | 2 | 0 |  |
| KCHOL | 208.20 | 0.514 | 0.922 |  |  |  | 2 | 0 |  |
| KRDMD | 38.88 | 0.326 | 0.749 |  |  |  | 2 | 0 |  |
| MGROS | 475.50 | 0.442 | 0.921 |  |  |  | 2 | 0 |  |
| PETKM | 16.79 | 0.398 | 0.681 |  |  |  | 2 | 0 |  |
| PGSUS | 158.20 | 0.502 | 0.900 |  |  |  | 1 | 51 |  |
| SAHOL | 84.50 | 0.424 | 0.953 |  |  |  | 2 | 9 |  |
| SASA | 1.60 | 0.743 | 0.743 |  |  |  | 2 | 521 |  |
| SISE | 36.02 | 0.375 | 0.781 |  |  |  | 4 | 0 |  |
| TAVHL | 301.00 | 0.385 | 0.848 |  |  |  | 2 | 0 |  |
| TCELL | 96.45 | 0.337 | 0.902 |  |  |  | 1 | 0 |  |
| THYAO | 319.00 | 0.324 | 0.844 | evet | 0.346 | 0.558 | 2 | -2 |  |
| TOASO | 238.00 | 0.247 | 0.701 |  |  |  | 1 | 0 |  |
| TRALT | 37.68 | 0.185 | 0.706 | evet | 0.266 | 0.520 | 2 | 0 |  |
| TRMET | 108.30 | 0.195 | 0.786 | evet | 0.253 | 0.521 | 3 | 0 |  |
| TTKOM | 50.55 | 0.164 | 0.779 | evet | 0.209 | 0.526 | 3 | 0 |  |
| TUPRS | 357.00 | 0.684 | 0.865 |  |  |  | 1 | -6 |  |
| VAKBN | 33.62 | 0.260 | 0.791 |  |  |  | 1 | 0 |  |
| YKBNK | 37.90 | 0.324 | 0.968 |  |  |  | 2 | 19 |  |

## Bugünkü dolumlar (0)


_Sanal para; gerçek emir verilmez. Karar kuralları: `docs/preregistration/long_overlay.md`. Kilitli testte bu sistem 12 hissenin 9'unda B&H'nin gerisinde kaldı; bu çalışma ileriye dönük (görülmemiş veride) testtir._
