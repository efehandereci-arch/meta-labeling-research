# Paper trading — BIST 30 long meta-labeling overlay

Son işlem günü: **2026-10-02** · başlangıç 2026-09-25 · sanal sermaye 1,000,000 TL · komisyon 10 bps + kayma 5 bps / yön

| Portföy | Değer (TL) | Getiri | Sharpe (≥20 gün) | Max DD |
|---|---|---|---|---|
| Sistem | 974,439 | -2.56% | n/a | -3.8% |
| Buy&Hold (eşit ağırlık) | 965,501 | -3.45% | n/a | -5.4% |
| XU030 endeksi | 953,495 | -4.65% | n/a | -6.9% |

Sistemin yatırım oranı: 49% · nakit 494,635 TL · 6 gün

## Bugünkü kararlar

| Hisse | Kapanış | Maruziyet | Vol tavanı | Yeni olay | m | P(Y=1) | Aktif olay | Emir (lot) | Not |
|---|---|---|---|---|---|---|---|---|---|
| AEFES | 18.04 | 0.579 | 0.991 |  |  |  | 1 | 0 |  |
| AKBNK | 67.10 | 0.246 | 0.859 |  |  |  | 1 | 0 |  |
| ASELS | 362.75 | 0.659 | 0.659 |  |  |  | 0 | 3 |  |
| ASTOR | 220.00 | 0.557 | 0.557 |  |  |  | 0 | -18 |  |
| BIMAS | 414.00 | 1.000 | 1.000 |  |  |  | 1 | 2 |  |
| EKGYO | 19.07 | 0.268 | 0.729 | evet | 0.367 | 0.552 | 1 | -773 |  |
| ENKAI | 84.00 | 0.683 | 0.904 |  |  |  | 1 | 0 |  |
| EREGL | 37.02 | 0.299 | 0.803 | evet | 0.353 | 0.545 | 2 | 0 |  |
| FROTO | 74.15 | 1.000 | 1.000 |  |  |  | 0 | 0 |  |
| GARAN | 125.90 | 0.330 | 0.949 |  |  |  | 1 | 0 |  |
| GUBRF | 419.75 | 0.246 | 0.781 |  |  |  | 1 | 0 |  |
| ISCTR | 12.45 | 0.336 | 0.685 |  |  |  | 1 | 0 |  |
| KCHOL | 206.80 | 0.547 | 0.934 |  |  |  | 1 | 4 |  |
| KRDMD | 43.28 | 0.515 | 0.935 |  |  |  | 1 | 25 |  |
| MGROS | 515.00 | 0.496 | 0.911 | evet | 0.541 | 0.558 | 3 | 0 |  |
| PETKM | 19.55 | 0.198 | 0.552 |  |  |  | 1 | 0 |  |
| PGSUS | 141.60 | 0.938 | 1.000 |  |  |  | 1 | -6 |  |
| SAHOL | 86.70 | 0.515 | 0.908 |  |  |  | 1 | 0 |  |
| SASA | 1.93 | 0.623 | 0.623 |  |  |  | 1 | -859 |  |
| SISE | 37.22 | 0.318 | 0.691 |  |  |  | 1 | 0 |  |
| TAVHL | 266.25 | 0.638 | 0.914 |  |  |  | 1 | 0 |  |
| TCELL | 97.80 | 0.506 | 0.957 |  |  |  | 1 | 0 |  |
| THYAO | 292.00 | 0.506 | 1.000 | evet | 0.441 | 0.557 | 2 | -8 |  |
| TOASO | 259.25 | 0.471 | 0.874 |  |  |  | 1 | 0 |  |
| TRALT | 43.84 | 0.254 | 0.817 |  |  |  | 1 | 0 |  |
| TRMET | 128.80 | 0.276 | 0.896 |  |  |  | 1 | 0 |  |
| TTKOM | 52.45 | 0.113 | 0.631 |  |  |  | 1 | 0 |  |
| TUPRS | 377.00 | 0.821 | 0.821 | evet |  |  | 2 | 0 | eksik öznitelik: ret_skew |
| VAKBN | 33.18 | 0.186 | 0.633 |  |  |  | 1 | 0 |  |
| YKBNK | 34.94 | 0.231 | 0.812 |  |  |  | 1 | 0 |  |

## Bugünkü dolumlar (0)


_Sanal para; gerçek emir verilmez. Karar kuralları: `docs/preregistration/long_overlay.md`. Kilitli testte bu sistem 12 hissenin 9'unda B&H'nin gerisinde kaldı; bu çalışma ileriye dönük (görülmemiş veride) testtir._
