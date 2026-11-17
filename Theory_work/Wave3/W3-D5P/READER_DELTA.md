# W3-D5P — READER_DELTA (v0.2, after council R1 [R1-sol-1..3, R1-opus-2, -3, -8]; HQ passes it to W3-READER; nothing written in W3-READER's folder)

**Current reader version.** `Theory_work/Wave3/W3-READER/READER_VERSIONS.md` §6 (Theorem 6, card row 3.1, section
v0.9, lines 660-812). Unchanged by this ticket: assumptions (A1)–(A6), the displays, the remarks.

**What changes.** One corollary is added under Theorem 6 (proposal; HQ decides placement: under Theorem 6, as a new
card row next to 3.1, or as a sentence of row 3.6 "Outside (A5) …"). No hypothesis is added. It needs the method
companion of D105 (the printed list fields of SPEC_LIST_PIP); until that commit exists the text below speaks of
"quantities computed from the returned list".

**New text (reader form; no internal ids).**

> **Corollary 6L (what the returned list gives).** A run that produces output returns, besides the reported model, a
> list of at most $40p+1$ distinct models with their unnormalised log posterior weights (the best-scored models met by
> the run). The method prints three further summaries. On a run that uses the sampler they are computed from this list:
> the inclusion probabilities $\hat p^{\,\mathrm{list}}_j$ of the posterior renormalised to the list, their median model
> $\hat S^{\mathrm{list}}=\{j:\hat p^{\,\mathrm{list}}_j>\tfrac12\}$ and the list evidence $\hat Z^{\mathrm{list}}$ (the
> sum of the list's weights). On a small problem solved by exact enumeration they are the exact inclusion probabilities,
> the exact median model and, where it is printed, the evidence of the enumeration's list. Write
> $\varepsilon_n:=1-\pi(S_0\mid y)$. Under the assumptions of Theorem 6, on the same data events $\mathcal G_n$, every
> run that produces output, whatever its seed and calibration outcome, reports $\hat S=S_0$ and has $S_0$ in its list
> (on the sampler; on exact enumeration, in the enumeration's list where it is returned), and
> $$
> \max_j\big|\hat p^{\,\mathrm{list}}_j-\mathbf 1\{j\in S_0\}\big|\le\varepsilon_n,\qquad
> \max_j\big|\hat p^{\,\mathrm{list}}_j-\mathrm{PIP}_j\big|\le\varepsilon_n,\qquad
> 1-\varepsilon_n\le\hat Z^{\mathrm{list}}/Z\le1\ \ \text{(where }\hat Z^{\mathrm{list}}\text{ is printed)},
> $$
> so that $0\le\log Z-\log\hat Z^{\mathrm{list}}\le-\log(1-\varepsilon_n)$; and $\hat S^{\mathrm{list}}=\hat S=S_0$ when
> $\varepsilon_n<\tfrac12$. Since $\varepsilon_n=O_P(\sqrt{\log n/n})$, the two PIP errors and the log-evidence error
> $|\log\hat Z^{\mathrm{list}}-\log Z|$ (where printed) are $O_P(\sqrt{\log n/n})$ on output, and without "on output"
> under the delivery conventions (S4).

*Remark for the text.* This covers every design inside Theorem 6 — including AR and block designs that satisfy
Theorem 6's conditions — on which the sampler's averaged PIPs, median model and evidence are not covered (Theorem 10
needs no leakage outside the true model). The list quantities are deterministic functions of the run's output; the price
is that they speak about the posterior restricted to the list, which on Theorem 6's data event holds at least the mass of
$S_0$.

**Bridges needed.** None beyond those of Theorem 6: (A5) gives (T1-R) = LSF (bridge B6.1), which is the input of the
rate; the corollary's master is `W3-D5P:LIST-R` with `LIST-K`, `LIST-CODE`.

**Tag vs the current reader version.** Theorem 6: STRONGER (added conclusions, same hypotheses, same event). Row 3.6:
NEW-CLAIM (different outputs; row 3.6 unchanged). Row 3.5: NEW-CLAIM (a deterministic sandwich for the list evidence, relative error ≤ ε_n, log error ≤ −log(1 − ε_n);
row 3.5's unbiasedness unchanged).
