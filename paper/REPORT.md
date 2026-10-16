# Paper trading — BIST 30 long meta-labeling overlay

Son işlem günü: **2026-10-16** · başlangıç 2026-09-25 · sanal sermaye 1,000,000 TL · komisyon 10 bps + kayma 5 bps / yön

| Portföy | Değer (TL) | Getiri | Sharpe (≥20 gün) | Max DD |
|---|---|---|---|---|
| Sistem | 952,269 | -4.77% | n/a | -4.8% |
| Buy&Hold (eşit ağırlık) | 926,039 | -7.40% | n/a | -7.4% |
| XU030 endeksi | 912,926 | -8.71% | n/a | -8.7% |

Sistemin yatırım oranı: 44% · nakit 535,744 TL · 16 gün

## Bugünkü kararlar

| Hisse | Kapanış | Maruziyet | Vol tavanı | Yeni olay | m | P(Y=1) | Aktif olay | Emir (lot) | Not |
|---|---|---|---|---|---|---|---|---|---|
| AEFES | 17.50 | 0.587 | 1.000 | evet | 0.625 | 0.571 | 4 | 198 |  |
| AKBNK | 66.85 | 0.289 | 0.975 |  |  |  | 2 | 10 |  |
| ASELS | 340.25 | 0.456 | 0.697 |  |  |  | 1 | 0 |  |
| ASTOR | 164.90 | 0.558 | 0.558 | evet |  | 0.314 | 2 | 6 | conformal ısınma |
| BIMAS | 381.00 | 0.733 | 0.893 | evet | 0.820 | 0.563 | 1 | -18 |  |
| EKGYO | 19.04 | 0.232 | 0.812 | evet | 0.310 | 0.534 | 2 | 0 |  |
| ENKAI | 76.20 | 0.669 | 0.909 |  |  |  | 1 | 10 |  |
| EREGL | 36.26 | 0.293 | 0.903 | evet | 0.431 | 0.550 | 3 | 0 |  |
| FROTO | 69.30 | 1.000 | 1.000 | evet |  |  | 2 | 0 | eksik öznitelik: ret_skew |
| GARAN | 131.50 | 0.373 | 1.000 |  |  |  | 2 | 0 |  |
| GUBRF | 372.75 | 0.340 | 0.832 | evet | 0.482 | 0.572 | 3 | 3 |  |
| ISCTR | 12.89 | 0.241 | 0.789 |  |  |  | 1 | 0 |  |
| KCHOL | 204.00 | 0.570 | 0.943 | evet | 0.584 | 0.553 | 3 | 0 |  |
| KRDMD | 41.26 | 0.599 | 1.000 | evet | 0.631 | 0.575 | 2 | 33 |  |
| MGROS | 452.25 | 0.623 | 0.980 | evet | 0.598 | 0.559 | 2 | 0 |  |
| PETKM | 19.71 | 0.253 | 0.630 | evet | 0.409 | 0.559 | 2 | 45 |  |
| PGSUS | 127.70 | 0.000 | 1.000 |  |  |  | 2 | 0 |  |
| SAHOL | 85.30 | 0.515 | 0.920 |  |  |  | 1 | 0 |  |
| SASA | 1.73 | 0.722 | 0.722 | evet |  |  | 3 | 405 | eksik öznitelik: volume_z |
| SISE | 36.16 | 0.386 | 0.802 | evet | 0.498 | 0.550 | 2 | 23 |  |
| TAVHL | 270.50 | 0.585 | 1.000 |  |  |  | 2 | 0 |  |
| TCELL | 96.80 | 0.530 | 1.000 | evet | 0.581 | 0.567 | 3 | 9 |  |
| THYAO | 273.50 | 0.516 | 1.000 | evet | 0.534 | 0.558 | 2 | 6 |  |
| TOASO | 244.40 | 0.437 | 0.925 |  |  |  | 1 | 0 |  |
| TRALT | 41.30 | 0.313 | 0.858 | evet | 0.368 | 0.527 | 3 | 0 |  |
| TRMET | 120.00 | 0.281 | 0.913 | evet | 0.308 | 0.523 | 1 | 0 |  |
| TTKOM | 50.90 | 0.155 | 0.736 | evet | 0.199 | 0.525 | 3 | 0 |  |
| TUPRS | 375.50 | 0.871 | 0.871 | evet |  |  | 3 | 2 | eksik öznitelik: ret_skew |
| VAKBN | 32.86 | 0.254 | 0.743 | evet | 0.334 | 0.537 | 2 | 0 |  |
| YKBNK | 35.70 | 0.147 | 0.926 |  |  |  | 2 | 0 |  |

## Bugünkü dolumlar (6)

- sistem AEFES: +94 lot @ 17.86 (maliyet 2 TL)
- sistem ASTOR: +6 lot @ 172.29 (maliyet 1 TL)
- sistem GARAN: +5 lot @ 131.97 (maliyet 1 TL)
- sistem MGROS: +5 lot @ 463.23 (maliyet 2 TL)
- sistem SASA: +402 lot @ 1.74 (maliyet 1 TL)
- sistem TRMET: +6 lot @ 125.36 (maliyet 1 TL)

_Sanal para; gerçek emir verilmez. Karar kuralları: `docs/preregistration/long_overlay.md`. Kilitli testte bu sistem 12 hissenin 9'unda B&H'nin gerisinde kaldı; bu çalışma ileriye dönük (görülmemiş veride) testtir._
