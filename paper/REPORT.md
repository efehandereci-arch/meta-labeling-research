# Paper trading — BIST 30 long meta-labeling overlay

Son işlem günü: **2026-11-06** · başlangıç 2026-09-25 · sanal sermaye 1,000,000 TL · komisyon 10 bps + kayma 5 bps / yön

| Portföy | Değer (TL) | Getiri | Sharpe (≥20 gün) | Max DD |
|---|---|---|---|---|
| Sistem | 941,786 | -5.82% | -3.25 | -9.1% |
| Buy&Hold (eşit ağırlık) | 907,169 | -9.28% | -2.49 | -17.0% |
| XU030 endeksi | 896,106 | -10.39% | -2.85 | -15.8% |

Sistemin yatırım oranı: 36% · nakit 601,678 TL · 30 gün

## Bugünkü kararlar

| Hisse | Kapanış | Maruziyet | Vol tavanı | Yeni olay | m | P(Y=1) | Aktif olay | Emir (lot) | Not |
|---|---|---|---|---|---|---|---|---|---|
| AEFES | 16.85 | 0.375 | 0.932 |  |  |  | 2 | 42 |  |
| AKBNK | 68.65 | 0.223 | 0.880 | evet | 0.353 | 0.535 | 2 | 39 |  |
| ASELS | 331.75 | 0.472 | 0.676 |  |  |  | 2 | 2 |  |
| ASTOR | 161.50 | 0.492 | 0.492 | evet |  | 0.811 | 4 | -10 | conformal ısınma |
| BIMAS | 371.75 | 0.492 | 0.808 |  |  |  | 3 | 2 |  |
| EKGYO | 17.66 | 0.212 | 0.756 |  |  |  | 3 | 0 |  |
| ENKAI | 80.85 | 0.511 | 0.905 |  |  |  | 2 | 0 |  |
| EREGL | 31.06 | 0.287 | 0.685 |  |  |  | 3 | 0 |  |
| FROTO | 73.15 | 0.360 | 0.825 | evet | 0.437 | 0.532 | 1 | -104 |  |
| GARAN | 144.30 | 0.367 | 0.996 |  |  |  | 1 | -5 |  |
| GUBRF | 289.25 | 0.174 | 0.597 |  |  |  | 2 | 0 |  |
| ISCTR | 13.29 | 0.355 | 0.791 | evet | 0.463 | 0.565 | 2 | 0 |  |
| KCHOL | 206.10 | 0.499 | 0.941 |  |  |  | 1 | 0 |  |
| KRDMD | 36.16 | 0.308 | 0.716 |  |  |  | 1 | 0 |  |
| MGROS | 468.75 | 0.446 | 0.894 | evet | 0.505 | 0.554 | 2 | 0 |  |
| PETKM | 16.33 | 0.375 | 0.642 |  |  |  | 2 | 0 |  |
| PGSUS | 141.60 | 0.282 | 0.916 |  |  |  | 2 | 0 |  |
| SAHOL | 87.30 | 0.404 | 0.909 | evet | 0.382 | 0.539 | 2 | 0 |  |
| SASA | 1.58 | 0.716 | 0.716 | evet |  |  | 2 | 1028 | eksik öznitelik: volume_z |
| SISE | 34.24 | 0.370 | 0.765 | evet | 0.486 | 0.552 | 3 | 19 |  |
| TAVHL | 294.50 | 0.359 | 0.805 |  |  |  | 1 | 0 |  |
| TCELL | 90.00 | 0.457 | 1.000 | evet | 0.454 | 0.552 | 3 | 0 |  |
| THYAO | 299.25 | 0.289 | 0.801 |  |  |  | 1 | 0 |  |
| TOASO | 243.00 | 0.237 | 0.672 | evet | 0.353 | 0.554 | 1 | -12 |  |
| TRALT | 38.14 | 0.174 | 0.690 |  |  |  | 1 | 0 |  |
| TRMET | 111.90 | 0.183 | 0.754 |  |  |  | 1 | 0 |  |
| TTKOM | 48.16 | 0.166 | 0.779 |  |  |  | 3 | 0 |  |
| TUPRS | 337.50 | 0.685 | 0.905 |  |  |  | 2 | 0 |  |
| VAKBN | 33.06 | 0.229 | 0.751 | evet | 0.329 | 0.536 | 2 | 57 |  |
| YKBNK | 37.24 | 0.310 | 0.941 | evet | 0.331 | 0.538 | 3 | 0 |  |

## Bugünkü dolumlar (9)

- sistem AKBNK: -16 lot @ 66.32 (maliyet 1 TL)
- sistem EREGL: -22 lot @ 30.34 (maliyet 1 TL)
- sistem GUBRF: -4 lot @ 281.36 (maliyet 1 TL)
- sistem KRDMD: -57 lot @ 36.40 (maliyet 2 TL)
- sistem TAVHL: -5 lot @ 288.36 (maliyet 1 TL)
- sistem ASTOR: +7 lot @ 146.57 (maliyet 1 TL)
- sistem ENKAI: +10 lot @ 81.04 (maliyet 1 TL)
- sistem PGSUS: +61 lot @ 136.07 (maliyet 8 TL)
- sistem VAKBN: +54 lot @ 31.38 (maliyet 2 TL)

_Sanal para; gerçek emir verilmez. Karar kuralları: `docs/preregistration/long_overlay.md`. Kilitli testte bu sistem 12 hissenin 9'unda B&H'nin gerisinde kaldı; bu çalışma ileriye dönük (görülmemiş veride) testtir._
