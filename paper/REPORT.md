# Paper trading — BIST 30 long meta-labeling overlay

Son işlem günü: **2026-11-10** · başlangıç 2026-09-25 · sanal sermaye 1,000,000 TL · komisyon 10 bps + kayma 5 bps / yön

| Portföy | Değer (TL) | Getiri | Sharpe (≥20 gün) | Max DD |
|---|---|---|---|---|
| Sistem | 949,491 | -5.05% | -2.66 | -9.1% |
| Buy&Hold (eşit ağırlık) | 930,929 | -6.91% | -1.66 | -17.0% |
| XU030 endeksi | 916,009 | -8.40% | -2.11 | -15.8% |

Sistemin yatırım oranı: 35% · nakit 621,721 TL · 32 gün

## Bugünkü kararlar

| Hisse | Kapanış | Maruziyet | Vol tavanı | Yeni olay | m | P(Y=1) | Aktif olay | Emir (lot) | Not |
|---|---|---|---|---|---|---|---|---|---|
| AEFES | 16.62 | 0.386 | 0.957 |  |  |  | 2 | 0 |  |
| AKBNK | 70.70 | 0.259 | 0.889 |  |  |  | 2 | 0 |  |
| ASELS | 337.00 | 0.488 | 0.699 |  |  |  | 2 | 0 |  |
| ASTOR | 157.10 | 0.508 | 0.508 |  |  |  | 4 | 0 |  |
| BIMAS | 381.25 | 0.129 | 0.819 |  |  |  | 2 | 0 |  |
| EKGYO | 18.38 | 0.206 | 0.762 |  |  |  | 2 | 0 |  |
| ENKAI | 81.00 | 0.531 | 0.940 |  |  |  | 2 | 0 |  |
| EREGL | 32.52 | 0.257 | 0.665 |  |  |  | 2 | 0 |  |
| FROTO | 75.90 | 0.411 | 0.844 | evet | 0.537 | 0.543 | 2 | 17 |  |
| GARAN | 155.40 | 0.336 | 0.942 |  |  |  | 1 | 0 |  |
| GUBRF | 288.00 | 0.134 | 0.578 | evet | 0.228 | 0.545 | 3 | 0 |  |
| ISCTR | 13.66 | 0.297 | 0.805 |  |  |  | 2 | 0 |  |
| KCHOL | 206.00 | 0.505 | 0.905 | evet | 0.557 | 0.553 | 2 | 0 |  |
| KRDMD | 37.66 | 0.317 | 0.729 | evet | 0.440 | 0.571 | 2 | 0 |  |
| MGROS | 491.00 | 0.428 | 0.893 |  |  |  | 2 | 0 |  |
| PETKM | 16.58 | 0.385 | 0.658 |  |  |  | 2 | 41 |  |
| PGSUS | 154.40 | 0.243 | 0.871 | evet | 0.557 | 0.586 | 2 | -12 |  |
| SAHOL | 87.30 | 0.415 | 0.935 |  |  |  | 2 | 11 |  |
| SASA | 1.59 | 0.726 | 0.726 |  |  |  | 2 | 0 |  |
| SISE | 35.72 | 0.367 | 0.765 |  |  |  | 4 | 0 |  |
| TAVHL | 302.00 | 0.372 | 0.819 |  |  |  | 2 | 0 |  |
| TCELL | 97.75 | 0.335 | 0.896 | evet | 0.373 | 0.551 | 1 | -45 |  |
| THYAO | 313.75 | 0.343 | 0.813 |  |  |  | 1 | 0 |  |
| TOASO | 240.80 | 0.245 | 0.694 |  |  |  | 1 | 0 |  |
| TRALT | 38.90 | 0.175 | 0.683 |  |  |  | 1 | 0 |  |
| TRMET | 112.20 | 0.188 | 0.764 |  |  |  | 2 | 0 |  |
| TTKOM | 50.45 | 0.164 | 0.779 | evet | 0.214 | 0.526 | 2 | -14 |  |
| TUPRS | 331.25 | 0.709 | 0.937 |  |  |  | 2 | 0 |  |
| VAKBN | 33.48 | 0.256 | 0.777 |  |  |  | 1 | 24 |  |
| YKBNK | 38.48 | 0.314 | 0.938 |  |  |  | 2 | 0 |  |

## Bugünkü dolumlar (13)

- sistem BIMAS: -31 lot @ 386.81 (maliyet 12 TL)
- sistem EREGL: -44 lot @ 32.90 (maliyet 1 TL)
- sistem GARAN: -11 lot @ 153.72 (maliyet 2 TL)
- sistem GUBRF: -4 lot @ 307.85 (maliyet 1 TL)
- sistem ISCTR: -147 lot @ 13.75 (maliyet 2 TL)
- sistem MGROS: -2 lot @ 483.26 (maliyet 1 TL)
- sistem SISE: -18 lot @ 35.58 (maliyet 1 TL)
- sistem YKBNK: -21 lot @ 38.94 (maliyet 1 TL)
- sistem AKBNK: +12 lot @ 71.34 (maliyet 1 TL)
- sistem ASTOR: +6 lot @ 145.07 (maliyet 1 TL)
- sistem ENKAI: +12 lot @ 80.89 (maliyet 1 TL)
- sistem THYAO: +4 lot @ 311.66 (maliyet 1 TL)
- sistem TUPRS: +2 lot @ 329.66 (maliyet 1 TL)

_Sanal para; gerçek emir verilmez. Karar kuralları: `docs/preregistration/long_overlay.md`. Kilitli testte bu sistem 12 hissenin 9'unda B&H'nin gerisinde kaldı; bu çalışma ileriye dönük (görülmemiş veride) testtir._
