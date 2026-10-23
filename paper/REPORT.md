# Paper trading — BIST 30 long meta-labeling overlay

Son işlem günü: **2026-10-23** · başlangıç 2026-09-25 · sanal sermaye 1,000,000 TL · komisyon 10 bps + kayma 5 bps / yön

| Portföy | Değer (TL) | Getiri | Sharpe (≥20 gün) | Max DD |
|---|---|---|---|---|
| Sistem | 923,334 | -7.67% | -6.90 | -7.7% |
| Buy&Hold (eşit ağırlık) | 866,492 | -13.35% | -6.55 | -13.4% |
| XU030 endeksi | 870,022 | -13.00% | -5.86 | -13.0% |

Sistemin yatırım oranı: 43% · nakit 522,549 TL · 21 gün

## Bugünkü kararlar

| Hisse | Kapanış | Maruziyet | Vol tavanı | Yeni olay | m | P(Y=1) | Aktif olay | Emir (lot) | Not |
|---|---|---|---|---|---|---|---|---|---|
| AEFES | 16.22 | 0.670 | 0.988 |  |  |  | 2 | 0 |  |
| AKBNK | 63.35 | 0.286 | 0.989 |  |  |  | 1 | 0 |  |
| ASELS | 338.00 | 0.449 | 0.681 |  |  |  | 1 | 0 |  |
| ASTOR | 142.60 | 0.590 | 0.590 | evet |  | 0.278 | 2 | 7 | conformal ısınma |
| BIMAS | 373.00 | 0.669 | 0.830 |  |  |  | 3 | 0 |  |
| EKGYO | 17.02 | 0.213 | 0.754 | evet | 0.277 | 0.531 | 2 | 0 |  |
| ENKAI | 74.50 | 0.582 | 0.893 |  |  |  | 2 | 0 |  |
| EREGL | 31.60 | 0.317 | 0.663 | evet | 0.478 | 0.579 | 1 | -158 |  |
| FROTO | 65.05 | 0.818 | 1.000 | evet | 0.818 | 0.549 | 2 | -79 |  |
| GARAN | 126.50 | 0.415 | 1.000 |  |  |  | 1 | 5 |  |
| GUBRF | 298.50 | 0.297 | 0.686 | evet | 0.433 | 0.581 | 1 | 5 |  |
| ISCTR | 12.17 | 0.174 | 0.821 |  |  |  | 1 | 0 |  |
| KCHOL | 197.50 | 0.534 | 0.929 |  |  |  | 3 | 0 |  |
| KRDMD | 38.60 | 0.570 | 0.951 | evet | 0.595 | 0.572 | 2 | 0 |  |
| MGROS | 431.50 | 0.615 | 0.980 |  |  |  | 1 | 2 |  |
| PETKM | 18.06 | 0.253 | 0.666 |  |  |  | 2 | 0 |  |
| PGSUS | 124.70 | 0.127 | 1.000 |  |  |  | 3 | 0 |  |
| SAHOL | 87.00 | 0.520 | 0.941 | evet | 0.579 | 0.565 | 2 | 16 |  |
| SASA | 1.60 | 0.743 | 0.743 | evet |  |  | 2 | 472 | eksik öznitelik: volume_z |
| SISE | 33.88 | 0.408 | 0.830 |  |  |  | 2 | 0 |  |
| TAVHL | 265.00 | 0.425 | 0.859 |  |  |  | 1 | 0 |  |
| TCELL | 90.10 | 0.423 | 1.000 | evet | 0.423 | 0.550 | 1 | -17 |  |
| THYAO | 258.00 | 0.541 | 1.000 |  |  |  | 2 | 0 |  |
| TOASO | 222.60 | 0.481 | 0.936 |  |  |  | 1 | 0 |  |
| TRALT | 35.94 | 0.252 | 0.780 |  |  |  | 1 | 0 |  |
| TRMET | 103.10 | 0.230 | 0.832 |  |  |  | 1 | 0 |  |
| TTKOM | 46.04 | 0.182 | 0.723 | evet | 0.227 | 0.530 | 2 | 0 |  |
| TUPRS | 360.75 | 0.647 | 0.853 |  |  |  | 1 | 0 |  |
| VAKBN | 30.06 | 0.189 | 0.765 | evet | 0.150 | 0.500 | 2 | -49 |  |
| YKBNK | 34.68 | 0.337 | 0.972 |  |  |  | 1 | 31 |  |

## Bugünkü dolumlar (12)

- sistem ENKAI: -19 lot @ 74.06 (maliyet 1 TL)
- sistem ISCTR: -1552 lot @ 12.45 (maliyet 19 TL)
- sistem KCHOL: -4 lot @ 196.20 (maliyet 1 TL)
- sistem TAVHL: -15 lot @ 268.12 (maliyet 4 TL)
- sistem TRALT: -41 lot @ 36.84 (maliyet 2 TL)
- sistem TRMET: -9 lot @ 107.75 (maliyet 1 TL)
- sistem TUPRS: -17 lot @ 354.82 (maliyet 6 TL)
- sistem ASTOR: +5 lot @ 150.07 (maliyet 1 TL)
- sistem EREGL: +99 lot @ 34.96 (maliyet 3 TL)
- sistem PGSUS: +20 lot @ 126.46 (maliyet 3 TL)
- sistem SASA: +570 lot @ 1.63 (maliyet 1 TL)
- sistem TTKOM: +21 lot @ 47.62 (maliyet 1 TL)

_Sanal para; gerçek emir verilmez. Karar kuralları: `docs/preregistration/long_overlay.md`. Kilitli testte bu sistem 12 hissenin 9'unda B&H'nin gerisinde kaldı; bu çalışma ileriye dönük (görülmemiş veride) testtir._
