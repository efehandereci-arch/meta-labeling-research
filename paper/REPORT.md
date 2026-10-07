# Paper trading — BIST 30 long meta-labeling overlay

Son işlem günü: **2026-10-06** · başlangıç 2026-09-25 · sanal sermaye 1,000,000 TL · komisyon 10 bps + kayma 5 bps / yön

| Portföy | Değer (TL) | Getiri | Sharpe (≥20 gün) | Max DD |
|---|---|---|---|---|
| Sistem | 977,965 | -2.20% | n/a | -3.8% |
| Buy&Hold (eşit ağırlık) | 976,873 | -2.31% | n/a | -5.4% |
| XU030 endeksi | 964,551 | -3.54% | n/a | -6.9% |

Sistemin yatırım oranı: 46% · nakit 527,753 TL · 8 gün

## Bugünkü kararlar

| Hisse | Kapanış | Maruziyet | Vol tavanı | Yeni olay | m | P(Y=1) | Aktif olay | Emir (lot) | Not |
|---|---|---|---|---|---|---|---|---|---|
| AEFES | 18.67 | 0.317 | 0.978 | evet | 0.098 | 0.500 | 2 | -470 |  |
| AKBNK | 69.50 | 0.251 | 0.872 |  |  |  | 2 | 0 |  |
| ASELS | 376.00 | 0.475 | 0.677 | evet | 0.702 | 0.592 | 1 | -17 |  |
| ASTOR | 194.60 | 0.546 | 0.546 |  |  |  | 1 | 0 |  |
| BIMAS | 409.25 | 1.000 | 1.000 |  |  |  | 1 | 0 |  |
| EKGYO | 19.75 | 0.229 | 0.730 |  |  |  | 2 | 0 |  |
| ENKAI | 82.65 | 0.693 | 0.910 | evet | 0.762 | 0.563 | 3 | 0 |  |
| EREGL | 37.08 | 0.307 | 0.823 |  |  |  | 2 | 0 |  |
| FROTO | 74.60 | 1.000 | 1.000 |  |  |  | 0 | 0 |  |
| GARAN | 131.20 | 0.330 | 0.949 |  |  |  | 1 | 0 |  |
| GUBRF | 410.75 | 0.255 | 0.811 |  |  |  | 1 | 0 |  |
| ISCTR | 12.87 | 0.277 | 0.695 |  |  |  | 2 | 0 |  |
| KCHOL | 213.60 | 0.562 | 0.912 |  |  |  | 2 | 0 |  |
| KRDMD | 44.40 | 0.527 | 0.934 |  |  |  | 2 | 0 |  |
| MGROS | 511.00 | 0.513 | 0.943 |  |  |  | 3 | 0 |  |
| PETKM | 19.78 | 0.214 | 0.566 |  |  |  | 2 | 0 |  |
| PGSUS | 140.20 | 1.000 | 1.000 |  |  |  | 0 | 0 |  |
| SAHOL | 88.80 | 0.264 | 0.923 |  |  |  | 2 | 0 |  |
| SASA | 1.90 | 0.646 | 0.646 |  |  |  | 1 | 598 |  |
| SISE | 38.00 | 0.328 | 0.708 |  |  |  | 2 | 0 |  |
| TAVHL | 275.50 | 0.569 | 0.920 |  |  |  | 1 | 0 |  |
| TCELL | 100.70 | 0.577 | 0.959 |  |  |  | 1 | 0 |  |
| THYAO | 290.50 | 0.506 | 1.000 |  |  |  | 2 | 0 |  |
| TOASO | 271.25 | 0.464 | 0.879 | evet | 0.516 | 0.561 | 2 | -3 |  |
| TRALT | 43.32 | 0.264 | 0.850 |  |  |  | 1 | 0 |  |
| TRMET | 129.50 | 0.286 | 0.929 |  |  |  | 1 | 0 |  |
| TTKOM | 53.10 | 0.131 | 0.648 |  |  |  | 2 | 14 |  |
| TUPRS | 379.25 | 0.799 | 0.799 | evet |  |  | 4 | 0 | eksik öznitelik: ret_skew |
| VAKBN | 33.72 | 0.192 | 0.654 |  |  |  | 1 | 0 |  |
| YKBNK | 36.46 | 0.000 | 0.827 |  |  |  | 1 | -105 |  |

## Bugünkü dolumlar (13)

- buyhold TRALT: +0 lot @ 0.50 (maliyet 0 TL) — temettü
- sistem TRALT: +0 lot @ 0.50 (maliyet 0 TL) — temettü
- sistem EKGYO: -86 lot @ 19.90 (maliyet 2 TL)
- sistem ISCTR: -172 lot @ 12.86 (maliyet 2 TL)
- sistem SAHOL: -94 lot @ 88.71 (maliyet 8 TL)
- sistem TAVHL: -9 lot @ 275.36 (maliyet 2 TL)
- sistem TUPRS: -3 lot @ 389.56 (maliyet 1 TL)
- sistem YKBNK: -106 lot @ 35.84 (maliyet 4 TL)
- sistem ASTOR: +6 lot @ 193.10 (maliyet 1 TL)
- sistem ENKAI: +10 lot @ 84.94 (maliyet 1 TL)
- sistem PGSUS: +14 lot @ 143.07 (maliyet 2 TL)
- sistem TCELL: +19 lot @ 100.55 (maliyet 2 TL)
- sistem TRALT: +15 lot @ 43.54 (maliyet 1 TL)

_Sanal para; gerçek emir verilmez. Karar kuralları: `docs/preregistration/long_overlay.md`. Kilitli testte bu sistem 12 hissenin 9'unda B&H'nin gerisinde kaldı; bu çalışma ileriye dönük (görülmemiş veride) testtir._
