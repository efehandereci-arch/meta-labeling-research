# Paper trading — BIST 30 long meta-labeling overlay

Son işlem günü: **2026-10-14** · başlangıç 2026-09-25 · sanal sermaye 1,000,000 TL · komisyon 10 bps + kayma 5 bps / yön

| Portföy | Değer (TL) | Getiri | Sharpe (≥20 gün) | Max DD |
|---|---|---|---|---|
| Sistem | 968,850 | -3.12% | n/a | -3.8% |
| Buy&Hold (eşit ağırlık) | 956,697 | -4.33% | n/a | -5.4% |
| XU030 endeksi | 943,618 | -5.64% | n/a | -6.9% |

Sistemin yatırım oranı: 43% · nakit 551,073 TL · 14 gün

## Bugünkü kararlar

| Hisse | Kapanış | Maruziyet | Vol tavanı | Yeni olay | m | P(Y=1) | Aktif olay | Emir (lot) | Not |
|---|---|---|---|---|---|---|---|---|---|
| AEFES | 18.24 | 0.443 | 1.000 |  |  |  | 4 | 0 |  |
| AKBNK | 67.10 | 0.282 | 0.952 | evet | 0.304 | 0.525 | 2 | 0 |  |
| ASELS | 348.00 | 0.445 | 0.681 |  |  |  | 1 | 0 |  |
| ASTOR | 193.00 | 0.573 | 0.573 | evet |  | 0.343 | 3 | 5 | conformal ısınma |
| BIMAS | 408.00 | 0.994 | 0.994 |  |  |  | 1 | -3 |  |
| EKGYO | 19.51 | 0.256 | 0.816 |  |  |  | 2 | 0 |  |
| ENKAI | 79.75 | 0.665 | 0.903 |  |  |  | 2 | 12 |  |
| EREGL | 37.10 | 0.269 | 0.901 |  |  |  | 3 | 0 |  |
| FROTO | 71.85 | 1.000 | 1.000 |  |  |  | 1 | 15 |  |
| GARAN | 130.50 | 0.347 | 1.000 |  |  |  | 1 | 0 |  |
| GUBRF | 391.00 | 0.314 | 0.845 |  |  |  | 3 | 2 |  |
| ISCTR | 13.01 | 0.233 | 0.764 |  |  |  | 1 | -170 |  |
| KCHOL | 211.20 | 0.595 | 0.952 |  |  |  | 3 | 0 |  |
| KRDMD | 43.16 | 0.572 | 1.000 |  |  |  | 2 | 17 |  |
| MGROS | 484.75 | 0.581 | 1.000 | evet | 0.604 | 0.556 | 2 | 3 |  |
| PETKM | 20.78 | 0.244 | 0.619 |  |  |  | 1 | 0 |  |
| PGSUS | 129.70 | 0.000 | 1.000 | evet | 0.000 | 0.483 | 2 | 0 |  |
| SAHOL | 84.75 | 0.496 | 0.886 |  |  |  | 1 | 0 |  |
| SASA | 1.82 | 0.701 | 0.701 | evet |  |  | 3 | 992 | eksik öznitelik: volume_z |
| SISE | 37.42 | 0.366 | 0.787 |  |  |  | 1 | 20 |  |
| TAVHL | 271.25 | 0.578 | 0.989 |  |  |  | 2 | 0 |  |
| TCELL | 98.30 | 0.504 | 1.000 |  |  |  | 2 | 0 |  |
| THYAO | 279.25 | 0.460 | 1.000 | evet | 0.498 | 0.556 | 2 | 0 |  |
| TOASO | 250.25 | 0.436 | 0.892 | evet | 0.473 | 0.554 | 3 | 0 |  |
| TRALT | 42.64 | 0.307 | 0.842 | evet | 0.368 | 0.529 | 2 | 18 |  |
| TRMET | 129.30 | 0.296 | 0.938 | evet | 0.317 | 0.523 | 2 | 0 |  |
| TTKOM | 52.50 | 0.155 | 0.721 |  |  |  | 2 | 15 |  |
| TUPRS | 391.00 | 0.865 | 0.865 |  |  |  | 3 | 2 |  |
| VAKBN | 34.24 | 0.257 | 0.734 |  |  |  | 1 | 28 |  |
| YKBNK | 35.94 | 0.143 | 0.899 |  |  |  | 2 | 0 |  |

## Bugünkü dolumlar (2)

- buyhold GUBRF: +0 lot @ 4.49 (maliyet 0 TL) — temettü
- sistem GUBRF: +0 lot @ 4.49 (maliyet 0 TL) — temettü

_Sanal para; gerçek emir verilmez. Karar kuralları: `docs/preregistration/long_overlay.md`. Kilitli testte bu sistem 12 hissenin 9'unda B&H'nin gerisinde kaldı; bu çalışma ileriye dönük (görülmemiş veride) testtir._
