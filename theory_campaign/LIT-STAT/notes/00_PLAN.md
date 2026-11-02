# LIT-STAT working notes: plan
Run LIT-STAT, 2026-11-02. Scope: statistical theory of the BVS posterior vs our Thm 1 (T03♯ + T02(i♯) exact BB(1,p) tail),
Prop 1 (T07), naive-merge proposition (A-DRAFT Prop M).
Our prior (00_COMMON): standardised X,y; beta_S ~ N(0, n sigma^2 (G_S+I)^{-1}) (ridge-stabilised unit-information g=n prior);
sigma^2 ~ IG(0.01,0.01); size prior BB(1,p), w(k)=1/2 / C(2p-1,k), capped at K=min(p, floor(n/2)).
Note: w(k) = B(k+1, 2p-k)/B(1,p) exactly (BB(1,p) per-model weight).
Already covered elsewhere (A-DRAFT, computational side): Song-Liang 2015, Zanella-Roberts 2019, Lindsten 2017,
Schafer-Chopin 2013, DDJ 2006, Gutierrez-Guhaniyogi 2022. Not repeated here.
Sources: local PDFs under Papers/ read by pdftotext (output to /tmp, not committed); web primary sources by WebFetch.
