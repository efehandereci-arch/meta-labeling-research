# meta-labeling-research

Meta-Labeling + Triple Barrier Method ile uçtan uca ML işlem pipeline'ı ve backtest sonucunun güvenilirliğini test eden araştırma çerçevesi (López de Prado, *Advances in Financial Machine Learning*).

Bu kod önceden `bist-quant-system` reposunda yer alıyordu.

## Meta-Labeling Pipeline (`meta_labeling/`)

Marcos López de Prado'nun *Advances in Financial Machine Learning* (AFML) kitabındaki
metodolojiyi izleyen, modüler bir araştırma/üretim pipeline'ı. Bağımlılıklar yalnızca
`numpy`, `pandas`, `scikit-learn` ve `lightgbm`.

```bash
pip install -r requirements.txt
python -m meta_labeling                                   # sentetik veri, varsayılan ayarlar
python -m meta_labeling --primary bollinger --model rf    # alternatif birincil model / meta-model
python -m meta_labeling --csv SASA.csv --threshold 0.55   # gerçek veri (Date,Open,High,Low,Close,Volume)
python -m pytest                                          # testler
```

**Jupyter Lab:** `notebooks/meta_labeling_pipeline.ipynb` (adım adım hücreler + equity grafiği)
veya tek hücreye yapıştırmak için `notebooks/meta_labeling_tek_hucre.py`. İkisi de kendi kendine
yeter (paket import'u gerektirmez) ve `python scripts/build_notebook.py` ile paketten üretilir.

```python
from meta_labeling import MetaLabelingPipeline, PipelineConfig

pipe = MetaLabelingPipeline(PipelineConfig())
result = pipe.run()                     # veya pipe.run(ohlcv_df)
print(result.summary())
result.events                           # t0, t1, bariyer, meta-etiket, ağırlık, OOS P(Y=1), bet size
pipe.score_events(ohlcv_df, result.final_model, last_n=1)   # canlı karar: side, P(Y=1), size
```

### Akış

| Adım | Modül | AFML | Açıklama |
|---|---|---|---|
| 1. Veri & birincil model | `data.py`, `primary.py`, `sampling.py` | 2.5, 3.6 | Rejim değiştiren GARCH simülasyonu; EMA kesişimi / Bollinger kırılımı ile `side ∈ {-1,0,+1}`; CUSUM filtresiyle olay örnekleme (yüksek recall) |
| 2. Triple Barrier | `volatility.py`, `labeling.py` | 3.1–3.4 | EWMA log-getiri volatilitesi; `pt·σ` kâr al, `sl·σ` zarar kes, `h` bar dikey bariyer; ilk temas `t1` |
| 3. Meta-etiket | `labeling.py` | 3.6 | `Y=1` ⇔ `side·(P_t1/P_t0−1) − maliyet > 0` |
| 4. Öznitelikler | `features.py` | — | Yönden bağımsız rejim göstergeleri: RSI, ATR%, ATR/vol oranı, vol oranı, BB genişliği, otokorelasyon, verimlilik oranı, |momentum| z-skoru, çarpıklık, hacim z-skoru |
| 5. Doğrulama | `cv.py`, `sample_weights.py` | 4, 7 | Benzersizlik ağırlıkları; Purged K-Fold (teşhis) + Purged walk-forward (OOS olasılıklar) |
| 6. Meta-model & karar | `model.py`, `sizing.py`, `backtest.py` | 6, 10, 14 | Dengelenmiş LightGBM/RF; `P(Y=1) > 0.55` filtresi; `m = 2Φ(z)−1` bet sizing; Win Rate, Sharpe, PSR karşılaştırması |

### Sızıntı (leakage) kontrolleri

- **Purging:** Etiket aralığı `[t0, t1]` test setinin `[min t0, max t1]` aralığıyla kesişen eğitim gözlemleri atılır.
- **Embargo:** Test bitişinden sonraki `embargo_pct × toplam süre` içinde başlayan eğitim gözlemleri atılır (rolling özniteliklerin seri korelasyonu).
- **Walk-forward OOS:** Backtest'te kullanılan her olasılık, yalnızca o andan önce *kapanmış* etiketlerle eğitilmiş bir modelden gelir.
- **Look-ahead testi:** `tests/test_features_weights_sizing.py` öznitelikleri kesilmiş veriyle yeniden hesaplayıp değişmediklerini doğrular.
- **Örtüşme:** Eğitim ağırlıkları ve ağaç alt örneklem oranı ortalama benzersizliğe göre ayarlanır.
- **Ex-ante parametreler:** Eşik ve hiperparametreler OOS sonuçlarına göre ayarlanmaz (`config.py`).

### Örnek çıktı (sentetik veri, varsayılan ayarlar)

```
[2] Purged walk-forward OOS
  OOS olay: 1262 | AUC: 0.554 | birincil precision (baz): 50.5% → meta precision: 56.1% | kapsama: 34.2%

[3] Strateji karşılaştırması (OOS, maliyet 5 bps/yön)
                                   İşlem WinRate Ort.İşlem İşlemSR Sharpe     PSR Yıl.Getiri   MaxDD
Birincil (filtresiz)                1262   50.5%    -0.13%   -0.34  -0.01   48.2%      -0.3%  -73.6%
Meta filtre (p>0.55)                 431   56.1%    +0.29%    0.48   0.53   97.4%       7.8%  -45.7%
Meta filtre + bet sizing (p>0.55)    431   56.1%    +0.12%    0.79   0.74   99.7%       2.5%   -9.3%
```

Tek bir fiyat yolu tek bir gerçekleşmedir: 10 farklı simülasyon tohumunda filtre, win rate'i
10'un 9'unda artırmış (ort. %48.7 → %52.9), portföy Sharpe'ını 9'unda iyileştirmiştir
(ort. −0.29 → +0.16). Sentetik verideki iyileşme gerçek piyasada garanti değildir; gerçek
veride aynı pipeline'ı çalıştırıp sonuçları PSR/Deflated Sharpe ile değerlendirin.

## Research Framework (`meta_labeling/research/`)

Amaç backtest performansını maksimize etmek değil, **sonucun güvenilir olup olmadığını test etmek**.
Tüm parametreler `config.yaml` içindedir; bilinmeyen anahtarlar hata verir.

```bash
python -m meta_labeling.research --config config.yaml             # tam rapor (~30 sn)
python -m meta_labeling.research --config config.yaml --universe  # config'deki tüm hisseler
```

Jupyter: `notebooks/research_framework.ipynb` (01_config … 24_final_report). Çıktılar
`research_output/<TICKER>/` altına yazılır: `research_report.md` (25 bölüm), `final_oos_results.csv`,
`robustness_summary.csv`, grafikler ve `research_output/experiments/` deney kayıtları.

| Modül | İçerik |
|---|---|
| `leakage.py` | `run_leakage_audit()`: öznitelik/vol/sinyal/CUSUM/ADV/rejim kesme testi, etiket sırası, CV/CPCV bölmeleri, kalibrasyon; PASS/FAIL + feature + timestamp + neden |
| `execution.py` | Sinyal close(t) → işlem open(t+1) (varsayılan) veya close; `komisyon + spread/2 + slippage + k·sqrt(emir/ADV)`; risk limitleri |
| `modeling.py` | Execution fiyatlı meta-etiketler, purged walk-forward, geçmişe dayalı Platt/Isotonic kalibrasyon, sizing (equal, vol, Prado, prob×vol, fraksiyonel Kelly, conformal Kelly) |
| `conformal.py` | Conformal Kelly (arXiv:2608.01494): ampirik kazanç/kayıp + yavaş conformal ölçek, alt-ihlal drawdown kadranı |
| `session.py` | Aşama aşama `ResearchSession` (benchmark A-I, maliyet, eşik ızgarası, long/short, rejim, dönem, önem + ablation, bootstrap, CPCV, placebo) |
| `metrics.py` | CAGR, Sharpe, Sortino, Calmar, PF, turnover, exposure, PSR, DSR, drawdown dönemleri, blok bootstrap |
| `cpcv.py` | Combinatorial Purged CV ve backtest yolu birleştirme |
| `regimes.py` | Genişleyen kantillerle geleceğe bakmayan vol / trend / piyasa rejimleri |
| `universe.py` | Çoklu hisse (simulated / csv / yfinance), veri doğrulama, tarihsel endeks üyeliği (survivorship) |
| `tracking.py`, `report.py` | Deney kaydı + `reproduce()`, otomatik rapor ve ex-ante robustness kriterleri |

Robustness kriterleri (`config.yaml → criteria`) sonuçlara bakmadan tanımlıdır. Placebo testlerinde
en küçük p-değeri 1/(1+tekrar) olduğundan, tekrar sayısı α'ya ulaşmaya yetmiyorsa test FAIL değil
**INCONCLUSIVE** olarak raporlanır.

## Conformal Kelly sizing (`conformal.py`)

R. J. Ryan, *Conformal Kelly: Conformal Prediction Intervals as the Scale in Fractional Kelly
Position Sizing* ([arXiv:2608.01494](https://www.alphaxiv.org/abs/2608.01494), 2026) uyarlaması.
Mevcut `kelly` yöntemi kazanç/kayıp oranını bariyerlerden varsayar (`b = pt/sl`); gerçekleşen
işlemler ise dikey bariyerde, boşluklu açılışta ve maliyet sonrası kapanır. Conformal Kelly
Kelly'nin iki girdisini de **karar anında kapanmış** (`label_end < t0`) işlemlerden tahmin eder:

- **Pay:** `μ̂ = p·W̄ − (1−p)·L̄`; W̄/L̄ gerçekleşmiş ortalama net kazanç/kayıp, `p` isotonic-kalibre olasılık.
- **Payda:** `s = |x − μ̂|` skorlarının son `window` kapanmış işlemdeki (1−α) conformal kantili,
  genişleyen kantile geometrik çekilir (`q_eff = q_roll^(1−λ)·q_anchor^λ`), `σ̂ = q_eff / Φ⁻¹(1−α/2)`.
  Makalenin ana bulgusu: ölçek **yavaş** olmalı; hızlı uyum sağlayan her varyant büyümeyi düşürdü.
- **Pozisyon:** `f = κ·μ̂/σ̂²`, `[0, max_position]` aralığına kırpılır; `μ̂ ≤ 0` ise bahis yok.
- **Drawdown kadranı** (`conformal_kelly_dial`): son 21 kapanmış işlemde alt sınır ihlali oranı α/2'yi
  aştıkça kitap küçülür. Zamanlamanın bilgi taşıyıp taşımadığı 40 dairesel kaydırma placebo'su ve
  sabit kaldıraç kontrolüyle test edilir.

`position_sizing()` (rapor bölüm 22) iki yeni satır (F, G), gerçekleşen kapsama tablosu ve kadran
placebo testini raporlar; varsayılan `sizing.method` **değişmedi** (`prob`). Ayarlar
`config.yaml → sizing.conformal` altında, varsayılanlar makaleden alındı ve OOS'a göre ayarlanmadı.
Makaleden bilinçli sapmalar: skorlar varsayılan olarak σ biriminde (`score_units: vol`, çünkü
bariyerler `k·σ_t` ölçekli; `raw` makaledeki düz artıktır), Gauss sabiti tutarlı `Φ⁻¹(1−α/2)`,
kantil sonlu örneklem indeksiyle.

Sentetik veride (varsayılan config, SASA simülasyonu) sonuç — **iyileşme yok, ölçüm doğru**:

| Sizing | İşlem | Sharpe | Max DD | Ort. büyüklük |
|---|---|---|---|---|
| D) Probability x volatility | 421 | 0.901 | -4.1% | 0.19 |
| E) Capped Kelly f=0.25 | 237 | 0.909 | -1.7% | 0.09 |
| F) Conformal Kelly κ=0.25 | 206 | 0.585 | -19.9% | 0.81 |
| G) F + drawdown kadranı | 206 | 0.730 | -18.4% | 0.64 |

- Gerçekleşen kapsama %75.5 (nominal %75, iid s.h. %1.3); alt/üst ihlal %12.5 / %12.0: ölçek kalibre.
- Ampirik `b̂ = W̄/L̄ = 0.93`; bariyer varsayımı 1.00 ile Kelly kırılma olasılığını olduğundan düşük tahmin ediyor.
- İşlem başına tam Kelly medyanda ~10× kaldıraç istiyor (işlem başı μ/σ ≈ 0.2, işlem σ'sı ≈ %4);
  κ=0.25'te bile alınan işlemlerin %72'si `max_position`'a dayanıyor (makalede de sınır neredeyse her
  gün bağlayıcıydı). Bu yüzden F, olasılık bazlı yöntemlerden çok daha yoğun ve oynak. İşlem başına
  Kelly eşzamanlı (örtüşen) işlemler arasındaki korelasyonu da yok sayar.
- Kadran Sharpe'ı 0.59 → 0.73'e çıkardı ama placebo p = 0.073 (anlamlı değil), drawdown'da placebo'dan
  iyi değil (p = 0.61). Sabit kaldıraç kontrolü drawdown'ı kadrandan daha çok azaltıyor.

Bu tek bir sentetik fiyat yolu. Gerçek BIST verisinde test için `data.source: yfinance`.

## Frekans çalışması (aynı sistem, üç zaman ölçeği)

```bash
pip install yfinance
python -m meta_labeling.research --config config.yaml --frequency-study            # varsayılan: AAPL
python -m meta_labeling.research --config config.yaml --frequency-study --ticker MSFT
```

`config.yaml → frequency_study` profilleri: günlük (15 yıl), saatlik (~730 gün), 5 dakikalık (~60 gün;
yfinance sınırı). Strateji parametreleri **bar cinsinden aynı** kalır; yalnızca veri frekansı ve Sharpe
yıllıklandırması (252 / 1764 / 19656 bar/yıl) değişir. Çıktı: `research_output/frequency_study_<TICKER>.md|csv|png`
ve her frekans için ayrı 25 bölümlük rapor. Olay sayısı yetersizse (ör. 5 dakikalık bar volatilitesi
`min_target`'ın altında) çalışma çökmez; ilgili frekans "Test edilemedi — yetersiz veri" olarak raporlanır.
"5 dakikalık" bar, tick verisi gerektiren gerçek HFT değildir.

## Placebo teşhisleri (`diagnostics.py`)

```bash
python -m meta_labeling.research --config config.yaml --diagnostics
```

Placebo testleri neden geçiyor/başarısız oluyor? Yalnızca raporlama yapar (`research_output/<TICKER>/diagnostics_report.md`):

1. **Öznitelik bazında karıştırma:** her öznitelik tek başına karıştırılıp yeniden eğitilir; ΔSharpe / ΔCAGR / Δisabet / Δturnover / ΔAUC, *aynı tohumlarla* eğitilmiş karıştırılmamış modellerin ortalamasına ve tohum gürültü bandına göre raporlanır.
2. **Olay zamanı placebo'su:** CUSUM → rastgele zaman → rastgele zaman + rastgele yön → tüm barlar; getiri zamanlama, yön ve filtre katkılarına ayrıştırılır.
3. **Meta-model kalitesi (Sharpe'tan bağımsız):** precision, recall, PR-AUC, koşullu beklenti (alınan vs reddedilen, Welch t), kalibrasyon, P(Y=1) dilimleri.
4. **Ayrı long / short meta-modelleri** (ortak model ve birincil sinyalle karşılaştırmalı).
5. **Sizing duyarlılığı:** 0.25x–1.25x (max_position üstü kırpılır, kaldıraç yok).

Ayrıca: maliyet breakeven'ı artık işlem bazlı (ort. brüt getiri / 2 × ort. büyüklük) hesaplanır ve her zaman sonludur; ızgara dışı sonuç "∞" yerine "> 100 bps (ızgaranın dışında)" olarak yazılır. Strateji getirileri Buy&Hold'a regres edilerek alpha/beta raporlanır.
