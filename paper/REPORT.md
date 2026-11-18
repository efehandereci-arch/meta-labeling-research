# Paper trading — BIST 30 long meta-labeling overlay

Son işlem günü: **2026-11-17** · başlangıç 2026-09-25 · sanal sermaye 1,000,000 TL · komisyon 10 bps + kayma 5 bps / yön

| Portföy | Değer (TL) | Getiri | Sharpe (≥20 gün) | Max DD |
|---|---|---|---|---|
| Sistem | 946,565 | -5.34% | -2.60 | -9.1% |
| Buy&Hold (eşit ağırlık) | 922,166 | -7.78% | -1.75 | -17.0% |
| XU030 endeksi | 916,467 | -8.35% | -1.91 | -15.8% |

Sistemin yatırım oranı: 39% · nakit 581,113 TL · 37 gün

## Bugünkü kararlar

| Hisse | Kapanış | Maruziyet | Vol tavanı | Yeni olay | m | P(Y=1) | Aktif olay | Emir (lot) | Not |
|---|---|---|---|---|---|---|---|---|---|
| AEFES | 16.26 | 0.412 | 1.000 |  |  |  | 1 | 41 |  |
| AKBNK | 69.05 | 0.258 | 0.973 | evet | 0.214 | 0.510 | 3 | 0 |  |
| ASELS | 341.50 | 0.545 | 0.743 | evet | 0.733 | 0.587 | 1 | -16 |  |
| ASTOR | 160.00 | 0.511 | 0.511 |  |  |  | 4 | 5 |  |
| BIMAS | 393.25 | 0.488 | 0.862 |  |  |  | 2 | 2 |  |
| EKGYO | 18.35 | 0.211 | 0.826 |  |  |  | 1 | 0 |  |
| ENKAI | 81.90 | 0.757 | 1.000 |  |  |  | 1 | 0 |  |
| EREGL | 31.86 | 0.243 | 0.706 |  |  |  | 2 | -25 |  |
| FROTO | 71.70 | 0.416 | 0.889 | evet | 0.500 | 0.535 | 2 | 0 |  |
| GARAN | 148.70 | 0.368 | 1.000 |  |  |  | 2 | 0 |  |
| GUBRF | 282.75 | 0.146 | 0.626 |  |  |  | 3 | 0 |  |
| ISCTR | 13.05 | 0.369 | 0.865 |  |  |  | 3 | 0 |  |
| KCHOL | 202.00 | 0.568 | 0.963 | evet | 0.624 | 0.557 | 2 | 6 |  |
| KRDMD | 38.52 | 0.346 | 0.794 |  |  |  | 2 | 0 |  |
| MGROS | 466.75 | 0.482 | 0.970 |  |  |  | 3 | 2 |  |
| PETKM | 16.18 | 0.420 | 0.720 | evet | 0.624 | 0.586 | 2 | 46 |  |
| PGSUS | 158.80 | 0.262 | 0.940 | evet | 0.000 | 0.440 | 2 | -49 |  |
| SAHOL | 83.00 | 0.503 | 0.992 | evet | 0.507 | 0.551 | 2 | 31 |  |
| SASA | 1.56 | 0.786 | 0.786 |  |  |  | 2 | 487 |  |
| SISE | 34.30 | 0.388 | 0.808 |  |  |  | 4 | 0 |  |
| TAVHL | 302.75 | 0.408 | 0.898 |  |  |  | 2 | 0 |  |
| TCELL | 96.30 | 0.355 | 0.952 |  |  |  | 1 | 8 |  |
| THYAO | 322.25 | 0.343 | 0.894 |  |  |  | 2 | 0 |  |
| TOASO | 245.40 | 0.268 | 0.735 |  |  |  | 2 | 0 |  |
| TRALT | 37.84 | 0.193 | 0.739 |  |  |  | 2 | 0 |  |
| TRMET | 113.50 | 0.203 | 0.808 |  |  |  | 4 | 0 |  |
| TTKOM | 51.10 | 0.173 | 0.820 |  |  |  | 2 | 0 |  |
| TUPRS | 345.25 | 0.702 | 0.887 | evet | 0.848 | 0.590 | 2 | 7 |  |
| VAKBN | 33.04 | 0.275 | 0.836 |  |  |  | 1 | 21 |  |
| YKBNK | 37.36 | 0.339 | 1.000 |  |  |  | 3 | 0 |  |

## Bugünkü dolumlar (7)

- sistem ASELS: +20 lot @ 351.93 (maliyet 7 TL)
- sistem ENKAI: +56 lot @ 82.59 (maliyet 5 TL)
- sistem EREGL: +23 lot @ 32.26 (maliyet 1 TL)
- sistem ISCTR: +137 lot @ 13.35 (maliyet 2 TL)
- sistem KCHOL: +4 lot @ 205.90 (maliyet 1 TL)
- sistem KRDMD: +22 lot @ 38.44 (maliyet 1 TL)
- sistem SASA: +665 lot @ 1.59 (maliyet 1 TL)

_Sanal para; gerçek emir verilmez. Karar kuralları: `docs/preregistration/long_overlay.md`. Kilitli testte bu sistem 12 hissenin 9'unda B&H'nin gerisinde kaldı; bu çalışma ileriye dönük (görülmemiş veride) testtir._
