# Ön-kayıt: Long meta-labeling overlay vs Buy & Hold

**Tarih:** 2026-09-27 (kilitli test çalıştırılmadan ÖNCE commit'lendi)
**Kod:** bu dosyanın eklendiği commit; tüm parametreler o commit'teki `config.yaml` varsayılanlarıdır.
**Çalıştırma:** `python -m meta_labeling.research --config <cfg> --overlay-study [--robustness]`

## 1. Bilinen kirlenme (dürüstlük beyanı)

- Kilitli test penceresi (2014-06-12 → 2026-09-25), 2026-09-26/27'de önceki sistemle (EMA 10/40
  long/short + meta filtre) **zaten görüldü**: Meta Sharpe 0.50, Meta+Sizing 0.59, B&H 0.95; long
  tarafı SR 0.67, short tarafı SR −0.14. "Yalnızca long" kararı kısmen bu gözlemden etkilendi. Ex-ante
  gerekçesi: hisse senedi risk primi (uzun vadeli pozitif sürüklenme) ve meta-labeling literatürünün
  iyileşmeyi birincil stratejiye göre ölçmesi (bkz. `docs/karsilastirma_profesyonel_meta_labeling.md`).
- Tasarımın geri kalanı (öznitelikler, conformal Kelly boyutlandırma, vol tavanı, kontroller) yalnızca
  geliştirme verisiyle (2014-06-12 öncesi; `--dev` kilitli veriyi hiç yüklemez) test edildi.

## 2. Sistem tanımı (dondurulmuş)

| Bileşen | Seçim |
|---|---|
| Birincil model | `AlwaysLong`: her CUSUM olayında (eşik 1.0·σ_t) long önerisi |
| Etiket | Triple barrier, pt = sl = 2σ, dikey 10 bar; execution next_open; meta-etiket = net getiri > 0 |
| Meta-model | LightGBM (config varsayılanları), purged walk-forward (6 fold, embargo %1), uniqueness ağırlıkları, isotonic kalibrasyon (yalnızca geçmiş fold'lar) |
| Öznitelikler | Çekirdek 10 rejim özniteliği + yönlü trend (12-1 momentum, SMA200 uzaklığı, 252g zirveden düşüş, EMA10/40 farkı, 5g getiri) + piyasa endeksi (aynı trend seti + vol oranı; SPY / XU100.IS) + birincil model karnesi (son 50 kapanmış işlemde isabet ve ort. getiri) |
| Boyut | m_i = clip(conformal Kelly f_i, 0, 1): μ̂ = pW̄ − (1−p)L̄, σ̂ = q_eff/Φ⁻¹(0.875), κ = 0.25, α = 0.25, W = 500, λ = 0.3; ısınma ve aktif olay yokken maruziyet 1 (tam long) |
| Eşzamanlılık | Olay i, [t0_i, t1_i) karar barlarında m_i önerir; eşzamanlılar ortalanır |
| Vol tavanı | maruziyet × min(1, σ_ref/σ_t); σ_t = EWMA(50) log-getiri std; σ_ref = σ'nın genişleyen medyanı (min. 252 bar) |
| Risk | kaldıraç yok (max_position = max_gross = 1), maliyet 5 bps/yön |

## 3. Hipotezler ve karar kuralları

**H1 (birincil), AAPL:** Sharpe(sistem) > Sharpe(B&H), kilitli pencerede.
- `GEÇTİ (anlamlı)`: ΔSharpe > 0 ve eşli durağan bootstrap P(ΔSharpe ≤ 0) < 0.05 (2000 tekrar, blok 20)
- `GEÇTİ (anlamlı değil)`: ΔSharpe > 0, P ≥ 0.05
- `GEÇEMEDİ`: ΔSharpe ≤ 0

**H2, ML katkısı:** model-olasılığı karıştırma placebo'sunda p < 0.05 **ve**
Sharpe(sistem) > Sharpe(modelsiz Kelly × vol tavanı). *Geliştirme tahmini: BAŞARISIZ.* Geliştirme
döneminde tüm meta-model varyantlarının OOS AUC'si 0.48–0.51 idi (5 varyant: LGBM tüm / RF tüm /
LGBM yalnız yeni / LGBM yalnız çekirdek / LGBM 21 bar ufuk). Placebo p = 0.54 çıktı. Modelsiz Kelly
(Sharpe 1.121) sistemden (1.101) yüksekti.

**H3, vol tavanı katkısı:** Sharpe(B&H × vol tavanı) > Sharpe(B&H). Literatür çelişkili: Harvey vd.
(2018) hisse senetlerinde artış buluyor; Cederburg vd. (2020) OOS'ta çoğu zaman artış olmadığını
gösteriyor.

**Sağlamlık (aynı dondurulmuş sistem):**
- ABD: MSFT, JPM, XOM, INTC, KO, WMT, GE (piyasa SPY)
- BIST: SASA.IS, THYAO.IS, GARAN.IS, ASELS.IS (piyasa XU100.IS; maliyet aynı, gerçek BIST maliyeti daha yüksek)

Her biri için ΔSharpe, bootstrap P ve placebo p raporlanır. "Kaç hissede geçti" sayısı esastır, tek
hisse değil.

**Deneme sayısı (DSR):** kilitli pencerede 5 varyant + geliştirmede 5 meta-model varyantı = 10.

## 4. Taahhütler

1. Kilitli test sonrası hiçbir parametre değiştirilmez. Değiştirilirse bu yeni bir deneydir ve ayrı
   raporlanır.
2. Sonuçlar olduğu gibi raporlanır. CAGR, drawdown ve maruziyet Sharpe ile birlikte verilir.
3. İşlem sayısı azaltılarak sonuç iyileştirilmez. Kitap varsayılan olarak piyasadadır.
