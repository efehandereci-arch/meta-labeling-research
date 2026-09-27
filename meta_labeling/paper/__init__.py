"""Sanal parayla ileriye dönük alım-satım (paper trading).

Her iş günü BIST kapanışından sonra:
  1. Veriyi çeker (yfinance; bölünme ve temettüler dahil).
  2. Dünkü emirleri BUGÜNÜN açılışından doldurur (tam lot, komisyon + kayma).
  3. Portföyü kapanıştan değerler; Buy&Hold ve XU030 ile karşılaştırır.
  4. Long meta-labeling overlay ile her hisse için yarınki hedef pozisyonu belirler.
  5. Durumu ve raporu ``paper/`` klasörüne yazar (GitHub Actions commit'ler).

Karar kuralları araştırma katmanıyla (``meta_labeling.research.overlay``) aynıdır;
model her yeni olayda yalnızca o güne kadar KAPANMIŞ etiketlerle eğitilir.
"""

from .config import PaperConfig, load_paper_config
from .engine import PaperState, run_day

__all__ = ["PaperConfig", "PaperState", "load_paper_config", "run_day"]
