# Paper trading — BIST 30 long meta-labeling overlay

Son işlem günü: **2026-10-05** · başlangıç 2026-09-25 · sanal sermaye 1,000,000 TL · komisyon 10 bps + kayma 5 bps / yön

| Portföy | Değer (TL) | Getiri | Sharpe (≥20 gün) | Max DD |
|---|---|---|---|---|
| Sistem | 980,544 | -1.95% | n/a | -3.8% |
| Buy&Hold (eşit ağırlık) | 980,478 | -1.95% | n/a | -5.4% |
| XU030 endeksi | 969,305 | -3.07% | n/a | -6.9% |

Sistemin yatırım oranı: 48% · nakit 514,556 TL · 7 gün

## Bugünkü kararlar

| Hisse | Kapanış | Maruziyet | Vol tavanı | Yeni olay | m | P(Y=1) | Aktif olay | Emir (lot) | Not |
|---|---|---|---|---|---|---|---|---|---|
| AEFES | 18.08 | 0.567 | 1.000 | evet | 0.550 | 0.564 | 2 | 0 |  |
| AKBNK | 68.95 | 0.247 | 0.856 | evet | 0.289 | 0.527 | 2 | 0 |  |
| ASELS | 371.50 | 0.665 | 0.665 |  |  |  | 0 | 0 |  |
| ASTOR | 198.00 | 0.535 | 0.535 | evet |  | 0.485 | 1 | 6 | conformal ısınma |
| BIMAS | 413.50 | 1.000 | 1.000 |  |  |  | 1 | 0 |  |
| EKGYO | 19.91 | 0.225 | 0.716 | evet | 0.261 | 0.531 | 2 | -86 |  |
| ENKAI | 84.85 | 0.698 | 0.917 | evet | 0.767 | 0.563 | 2 | 10 |  |
| EREGL | 37.64 | 0.303 | 0.812 |  |  |  | 2 | 0 |  |
| FROTO | 74.55 | 1.000 | 1.000 |  |  |  | 0 | 0 |  |
| GARAN | 130.40 | 0.324 | 0.931 | evet | 0.347 | 0.533 | 1 | 0 |  |
| GUBRF | 416.00 | 0.251 | 0.796 |  |  |  | 1 | 0 |  |
| ISCTR | 12.87 | 0.271 | 0.682 | evet | 0.305 | 0.547 | 2 | -172 |  |
| KCHOL | 214.90 | 0.552 | 0.895 | evet | 0.648 | 0.569 | 2 | 0 |  |
| KRDMD | 45.02 | 0.519 | 0.920 | evet | 0.577 | 0.575 | 2 | 0 |  |
| MGROS | 517.50 | 0.505 | 0.928 |  |  |  | 3 | 0 |  |
| PETKM | 20.10 | 0.210 | 0.556 | evet | 0.395 | 0.567 | 2 | 0 |  |
| PGSUS | 142.90 | 1.000 | 1.000 |  |  |  | 0 | 14 |  |
| SAHOL | 88.80 | 0.259 | 0.905 | evet | 0.005 | 0.485 | 2 | -94 |  |
| SASA | 1.94 | 0.634 | 0.634 |  |  |  | 1 | 0 |  |
| SISE | 38.10 | 0.321 | 0.694 | evet | 0.465 | 0.556 | 2 | 0 |  |
| TAVHL | 274.50 | 0.558 | 0.902 | evet | 0.618 | 0.583 | 1 | -9 |  |
| TCELL | 100.50 | 0.566 | 0.940 | evet | 0.602 | 0.579 | 1 | 19 |  |
| THYAO | 292.25 | 0.506 | 1.000 |  |  |  | 2 | 0 |  |
| TOASO | 264.75 | 0.473 | 0.878 |  |  |  | 1 | 0 |  |
| TRALT | 43.88 | 0.259 | 0.833 |  |  |  | 1 | 15 |  |
| TRMET | 127.70 | 0.282 | 0.914 |  |  |  | 1 | 0 |  |
| TTKOM | 53.65 | 0.128 | 0.636 | evet | 0.225 | 0.534 | 2 | 0 |  |
| TUPRS | 391.25 | 0.809 | 0.809 | evet |  |  | 3 | -3 | eksik öznitelik: ret_skew |
| VAKBN | 33.94 | 0.189 | 0.642 |  |  |  | 1 | 0 |  |
| YKBNK | 35.90 | 0.116 | 0.814 | evet | 0.000 | 0.444 | 2 | -106 |  |

## Bugünkü dolumlar (11)

- buyhold AEFES: +0 lot @ 0.17 (maliyet 0 TL) — temettü
- sistem AEFES: +0 lot @ 0.17 (maliyet 0 TL) — temettü
- sistem ASTOR: -18 lot @ 221.09 (maliyet 4 TL)
- sistem EKGYO: -773 lot @ 19.17 (maliyet 15 TL)
- sistem PGSUS: -6 lot @ 141.73 (maliyet 1 TL)
- sistem SASA: -859 lot @ 1.96 (maliyet 2 TL)
- sistem THYAO: -8 lot @ 292.10 (maliyet 2 TL)
- sistem ASELS: +3 lot @ 378.19 (maliyet 1 TL)
- sistem BIMAS: +2 lot @ 414.46 (maliyet 1 TL)
- sistem KCHOL: +4 lot @ 207.90 (maliyet 1 TL)
- sistem KRDMD: +25 lot @ 43.92 (maliyet 1 TL)

_Sanal para; gerçek emir verilmez. Karar kuralları: `docs/preregistration/long_overlay.md`. Kilitli testte bu sistem 12 hissenin 9'unda B&H'nin gerisinde kaldı; bu çalışma ileriye dönük (görülmemiş veride) testtir._
