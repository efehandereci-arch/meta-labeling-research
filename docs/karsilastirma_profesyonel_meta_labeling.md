# Profesyonel meta-labeling uygulamalarıyla karşılaştırma

Karşılaştırma kaynakları:
- López de Prado, *Advances in Financial Machine Learning* (AFML, 2018)
- Joubert, "Meta-Labeling: Theory and Framework", *JFDS* 4(3), 2022
- Meyer, Barziy & Joubert, "Meta-Labeling: Calibration and Position Sizing", *JFDS* 5(2), 2023
- Hudson & Thames: mlfinlab ve "Does Meta-Labeling Add to Signal Efficacy?" (Singh & Joubert)
- RiskLabAI (açık kaynak AFML kütüphanesi)

| Bileşen | Profesyonel uygulama | Bu depo (önce) | Durum |
|---|---|---|---|
| Birincil model | Yüksek recall'lı yön önerisi; güven gücü (−1…1) meta-modele girdi olur | EMA 10/40 long/short; yalnızca yön | **Eksikti.** `AlwaysLong` birincil model ve EMA farkı z-skoru (güven) eklendi |
| Meta-model girdileri | 4 grup (Joubert 2022): genel öngörücüler, birincil modelin karnesi (kayan isabet/F1/AUC), piyasa rejimi/makro, birincil modelin güveni | Yalnızca yönden bağımsız 10 rejim özniteliği + side | **En büyük eksik.** Karne (son 50 kapanmış işlem), piyasa endeksi rejimi, yönlü trend öznitelikleri eklendi |
| Etiketleme | Triple barrier; trend-scanning (mlfinlab, RiskLabAI) | Triple barrier, **execution fiyatı ve maliyet dahil** | Kütüphanelerden daha gerçekçi; trend-scanning yok |
| Örnekleme | CUSUM + sequential bootstrap | CUSUM + benzersizlik ağırlığı + max_samples | Sequential bootstrap yok (AFML'de RF için önerilir) |
| Durağanlık | Kesirli türev (fracdiff) öznitelikleri | Yok (getiri/oran tabanlı öznitelikler) | Eksik, düşük öncelik |
| Mimari | Tek model, DSML (long/short ayrı), koşula özel, sıralı, ensemble (Meyer vd. 2023) | Tek model; ayrı long/short yalnızca teşhiste | Long-overlay tek taraflı olduğundan DSML'ye gerek kalmadı |
| Doğrulama | Purged k-fold + embargo, CPCV | Purged walk-forward + k-fold + CPCV + **otomatik sızıntı denetimi** | Kütüphanelerden güçlü |
| Kalibrasyon | Platt / isotonic | Walk-forward Platt / isotonic | Eşdeğer |
| Boyutlandırma | Hepsi-ya-hiç, güven, doğrusal, NCDF, ECDF, SOPS; AFML: aktif bahis ortalaması, ayrıklaştırma, dinamik, bütçe, rezerv | Hepsi-ya-hiç, NCDF (Prado), vol hedefi, fraksiyonel Kelly, **conformal Kelly**, aktif ortalama, ayrıklaştırma | ECDF/SOPS yok; conformal Kelly literatürde yeni |
| Değerlendirme | Birincil stratejiye göre iyileşme (precision, Sharpe) | PSR, DSR, CPCV, 4 placebo, bootstrap, maliyet eşiği, alpha/beta | Kütüphanelerden güçlü |

## Temel ders

Meta-labeling literatürü başarıyı **birincil stratejiye göre** ölçer. Meta-model precision'ı artırır ve
yanlış pozitifleri eler. Birincil strateji hisse senedi primini taşımıyorsa (önceki sistem zamanın
%42'sinde piyasadaydı ve yükselen hissede short açıyordu), meta-model ne kadar iyi olursa olsun B&H'nin
Sharpe'ını yakalaması beklenmez. Bu yüzden B&H'yi hedefleyen sistem **varsayılan olarak long**
olmalıdır. Meta-model yalnızca beklentisi negatif dönemlerde riski azaltmalıdır (long overlay).
Tasarım ve kilitli test kuralları `docs/preregistration/long_overlay.md` dosyasında.

Ek kaynaklar (volatilite tavanı):
- Harvey vd., "The Impact of Volatility Targeting", *JPM* 45(1), 2018
- Cederburg, O'Doherty, Wang & Yan, "On the performance of volatility-managed portfolios", *JFE* 138(1), 2020
