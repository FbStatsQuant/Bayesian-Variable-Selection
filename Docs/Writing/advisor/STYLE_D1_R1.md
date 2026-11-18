# STYLE_D1_R1: advisor report on D1, "The SMC-BVS method, as coded" (2026-11-16)

Read: `smc_bvs_method.tex`, its PDF (14 pp.) and compile log, the current D2 §2, `smcbvs.sty`. I did not check any code
fact. Findings only. Overall: §2, §3, §6 and the leakage example read well. The weak places are the budgets
paragraph (§4.1), the calibration (§4.5), both figures as rendered, and the many empty cells of Table 2.

## 1. Flags (things that look wrong or need a decision; nothing rewritten)

1. **"None is set by the user"** (abstract, §5) against Table 2, which lists the seed, the allocation, and two switches
   that are "on" (search from the start mode, grid fallback). Suggest: "The user supplies the data, a seed and a
   computing allocation. Everything else is fixed, or a stated function of $(n,p)$, in the default configuration, which
   is the one described here."
2. **Example 4.1 is an exact case.** With $p=6$ there are 64 models, far below the threshold of §4.1, so the software
   would enumerate and never build a start law. The closing parenthesis does not say this. Add one sentence.
3. **"Leakage" means two things.** In D1 it is imitation *across blocks*; a same-block proxy "is handled correctly". In
   D2 the leakage set $Q$ holds every predictor that stays correlated with a true one, whatever its block; by D2's
   Example 5.5 it would here also contain predictors 2 and 4. Please align the wording, with Theory.
4. **"Since $\hat Z$ is unbiased"** (§4.7) is stated as a fact. In D2 it is Remark 5.21: given the calibration, under
   the sampler convention, with the pooled form not yet independently checked. Cite it with those conditions.
5. **"The unique Gaussian prior that produces the matrices the code uses"** (§2): "unique" is a claim. Confirm, or
   write "the Gaussian prior that corresponds to".
6. **Figure 1 is drawn wrongly.** The dashed line ends on box 7 and runs through it, and its label "start mode"
   overprints "7. report". By the caption it must end at box 6. The exit of the exact case is not drawn.
7. **"Every tuning constant"** (§5): the text has constants that Table 2 lacks ($1-10^{-10}$ for duplicates,
   $10^{-8}\,y^\top y$ for a small $\mathrm{SS}_S$, $H_1$, $T_1$, trigger E3 and the four unnamed triggers).
8. **Calibration, step 6** does not say what is frozen when tier 0 raises no trigger, and "the calibration succeeds",
   which D2 uses, is never defined in D1.
9. **Compile log:** five overfull boxes. The visible ones: the independence move in §4.4 (34pt into the margin), the
   "grid fallback" row of Table 2 (Code runs into Theory), and Appendix C (38pt).

## 2. Style, and sentences read twice

| Where | Problem | Proposed wording |
|---|---|---|
| §1 Notation | Sentences start with symbols; "model" and $X_S$ come before $p$ and $X$ exist. It is not the text of D2 §2.1. | Use D2 §2.1's sentences word for word, and move "A *model* is …; $X_S$ …" after the standardisation. |
| §1, "The intercept … Exact duplicate predictors (sample correlation at least $1-10^{-10}$) are reported but kept." | Wrong heading; "exact" with a tolerance. | Own paragraph, "Duplicated predictors": "Two predictors whose sample correlation is at least $1-10^{-10}$ in absolute value are reported as duplicates. Both are kept." |
| §2, "a true model that need not coincide with any prior draw" | Second read. | D2's sentence: "Here $\theta_S$ and $\sigma^2$ are working parameters, not true values. The theorems are proved under the data-generating model of the companion section, not under this working model." |
| §3, "if that fails it recomputes the Gram matrix … only if all three fail" | Which three? | "It tries three computations in turn: a Cholesky factorisation; the same after recomputing the Gram matrix from $X$; a QR factorisation. It reports a numerical failure only if all three fail." |
| §4.1, "From $(n,p)$ alone … $T_0:=\max(1000,\ell_n^2)$" | Six constants in one sentence, each named after something not yet described (burn-in rounds, stage ceiling). | Keep here only the tiers and a pointer to Table 2. Define each constant where it is used: $B$ in §4.2, $N$ and $L$ in §4.4, $H_e$ and $T_e$ in §4.5, $\ell_n$ in §4.6. |
| §4.1, exact case | No reason for the threshold $(5H_0+4N_0)p$. | One clause on why, if the source gives one. |
| §4.2, "splits every cluster … from the top down; and packs the resulting clusters, in leaf order and whole" | Second read. | If this is what the method does: "It cuts the clustering tree from the top until every cluster has at most $B$ members. It then fills the blocks with whole clusters, in the order of the tree's leaves." |
| §4.2, neighbour graph | Purpose not given; "at least one" unexplained. | "… (used by the swap moves of Section 4.4). If no predictor passes the threshold, the most correlated one is kept." (if so) |
| §4.3, "with $e_b(j):=\dots$, the size profiles $F_b(k):=\dots$, $F_0(0)=1$, give …" | Three definitions inside one sentence; no words. | Display the recursion. Add: "$F_b(k)$ is the total table weight of all ways to choose subsets in blocks $1,\dots,b$ with $k$ predictors in all." |
| §4.4, step 2(c), "that leave $\gamma_{\phi_t}$ invariant to every particle" | Ambiguous attachment. | "apply to every particle one round of Markov moves, each of which leaves $\gamma_{\phi_t}$ invariant". |
| §4.4, step 3, "$o_j$"; "a Rao–Blackwellised estimate" | $o_j$ is defined only later, under the moves. Jargon. | Put "The Markov moves" before "One island". "… an average of conditional probabilities instead of 0/1 indicators, which has a smaller variance." |
| §4.4, "accept with the Metropolis–Hastings probability" | Not given, while the other three moves are explicit. | State the acceptance ratio. |
| §4.5, step 3 | "appends the next pilot temperature if $\rho_V\ge0.90$" (of which arguments?); "stops progressing"; no words for $\rho_V$. | "$\rho_V(u,v)$ is the effective sample size, as a fraction, that the step from $u$ to $v$ would leave if the population were all of $V$." Define "stops progressing". |
| §4.5, step 5 | E1–E3 are code names; four more triggers are unnamed; "overall best" of what? | Name each trigger in words ("island disagreement (E1)", "evidence spread (E2)", "late improvement (E3)", …), as a list. |
| §4.7, "the one-sided lower bound $\log(0.05\,\hat Z)$ (from Markov's inequality …)" | Second read. | "a 95% lower confidence bound for $\log Z$: by Markov's inequality $\P(\hat Z>20Z)\le0.05$, because $\E\hat Z=Z$ (flag 4)". |
| §6, "what lets every reported number be analysed" | Vague. | "and what the results on the reported estimates rely on". |
| Text of §2–§5 | "The code computes …", "the code does not write …", "slab" (Tables 1, 2) | "The method" in running text; "coefficient prior" for "slab". |
| Appendix A | "an arm", "leader stores", "occupancy-based", "top-down cut" are undefined. | Two columns, "the method" and "the $10^6$ engine", one row per change. That also makes the difference unmistakable. |

**Order.** §4.4 (one island, stage 5) comes before §4.5 (calibration, stage 4). That is the right teaching order, but say
so: "We describe one island first, because the calibration is built from islands." Put the stage number of Figure 1 in
each subsection title. Consider moving §6 (intuition) before §4: it motivates the start law, the islands and the local
search, and the reader needs it before the details, not after the table.

## 3. Notation: D1 against D2 §2

**D1 should take from D2:**
- the Notation sentences themselves, and the items D1 lacks: $a\vee b$, $\mathbf 1\{E\}$, $B_{UV}$, $\gg$ ("$\gtrsim$" is
  used in §5 and not defined), "with probability tending to one";
- the run vocabulary that the theorems use: *run*, *valid* inputs, *produces output*, the two statuses, *completed
  run*, *the calibration succeeds*. D1 is the place to define them; today it says only "stops without estimates";
- the two-case definition of *certifies* (D1 uses "certified" for any search end point in §4.6, and for $\hat S$ in
  §4.7);
- one sentence saying that the data-generating model and the starred parameters are introduced in the companion
  section. D1 announces the star and never uses it.

**D2 should take from D1:**
- the order "log score $F$, then $\pi(S\mid y)=e^{F(S)}/Z$, $Z=\sum_V e^{F(V)}$". It is the same $Z$ as D2's, but
  written differently in the two places;
- $\gamma_\phi$ in place of $\pi_\phi$, or D1 defines $\pi_\phi:=\gamma_\phi/\sum_S\gamma_\phi(S)$;
- the block cap $B\le16$, and the tie rule of the start mode.

**Collisions** (D1 alone, then across the paper):
- $B$: block cap, the symmetric matrix of the Notation paragraph, and the beta function in §2.
- $H_0$, $H_e$ (calibration particles) against $H_S$ (matrix of (6)).
- $F$: log score $F(S)$, size profiles $F_b(k)$, restricted log-normaliser $F_V(t)$.
- $e$: the tier, $e_b(j)$, and Euler's $e$; "$4^e$" reads as an exponential.
- $V$: the candidate set, and the summation index in (8). $t$: the stage index, and a temperature in $F_V(t)$.
- $r$: $r_{jl}$ (correlation; say it is an entry of $\hat R$), $r_b(U)$ (block table), island index $r$, and D2's $r_n$.
- $j$ is a size in $e_b(j)$ and a predictor everywhere else.
- Across the paper: $\phi_0$ (first temperature) against $\varphi_0$ (D2's eigenvalue constant); $L$ and $T$ against
  D2's $L$, $L_n$, $T$, $\mathcal T$; $\omega_i$ against D2's $\omega_n$; $\gamma_0$, $\gamma_\phi$ against D2's gain
  $\gamma(t\mid S)$; $N$ against D2's $N_l$. The first is the one a reader will trip on: never write $\phi_0$ alone
  ("the grid starts at 0").

## 4. Figures and examples

- **Figure 1** has the right idea (stages, and exact / random / deterministic). Apart from flag 6: the colours are pale
  and vanish in print, so add a letter or a line style; "stan-dardise" is hyphenated in the box.
- **Figure 2 does not do its job.** In panel (b) only three of five particles carry a multiplier, and they do not add
  up to five; the dots sit on a line that means nothing; panel (c) is five small arrows. Suggest redrawing it with the
  numbers of Example 4.1: particles drawn from the start law sit mostly on $\{1,3,5\}$ (0.517); one step to $\phi=1$
  reweights by $\pi/\pi_0$, which is small for $\{1,3,5\}$ and large for $\{1,3\}$; resampling moves the mass to
  $\{1,3\}$ (0.688). That is the worked SMC step the standard asks for, and it ties the figure to the example.
- **Example 2.1 ($p=3$)** is correct, including the $n=4$ case. It would say more with two lines: each predictor has
  prior inclusion probability $1/(p+1)$, here $\tfrac14$; and for large $p$ the prior probability of size $k$ is about
  $2^{-(k+1)}$. Both follow from (4); please verify before use.
- **Example 4.1 (six predictors)** does its job. Besides flags 2 and 3: say that here $B=2$; say how the five models
  shown were chosen (the masses shown add to 0.80 and 0.94); use one word for each role (*proxy* in the same block,
  *leak* across blocks) and drop "imitator" and "near copy". A six-node sketch of the three blocks would replace four
  lines of prose.
- **Calibration is not understandable without pseudocode.** It is a control flow with a loop (rebuild), a branch
  (escalation) and a fallback, written as six noun-phrase items. Add "Algorithm 1: calibration", about 15 lines, and
  keep the prose as commentary in which each step starts with its purpose. Open with: "The calibration answers two
  questions: which temperatures, and how many particles."
- **Still missing for a reader:** one line on the cost of a run (score evaluations per round), which is also what
  explains why Appendix A exists; and a typical number of stages $T$.

## 5. The parameter table (Table 2)

It is complete enough to be the core, but it is hard to read as it stands.

1. **About 70% of the cells in "Symbol" and in the example column are "—"** (29 and 28 of 40 rows). Lead with the
   name: columns "Parameter, Symbol, Value, Example, Theory, Code", with Code last and widest (it overflows now).
2. **Fill the example column wherever the value depends on $(n,p)$**, and leave it blank, not "—", for fixed
   constants (now "4 | 4" for islands but "—" for other constants). By my arithmetic, to be verified: neighbour
   threshold 0.30; enumeration threshold $5.0\times10^8$; moves per round 10,016; pilot target 1,843; step floor
   0.001; score cache $5\times10^6$; $H_1=8{,}192$; $T_1=4{,}000$.
3. **The "Theory" column uses words a reader cannot follow up** ("delivery", "sampler conventions", "estimates",
   "all", "scope of the estimate results"). Cite the theorem numbers and the labels (C1)–(C3) of the companion
   section, and explain "none": the theorems hold whatever the calibration returns.
4. **Group headings** are small italics and get lost; set them in bold with a rule above.
5. **Table 1 repeats the Prior group of Table 2**, with slightly different line ranges. Keep one.
6. **Row names that are fragments:** "enumerate if $|\Omega|\le$" → "exact-case threshold"; "(15 = 16 − 1)" in the
   Theory cell of $B$ needs words.

## Top five

(1) Settle the flags of §1, first "none is set by the user", the exact-case status of Example 4.1, and the two
meanings of "leakage". (2) Make D1 §1 and D2 §2 one text: the same Notation sentences, the run vocabulary defined in
D1, the same form of $Z$ and of the path. (3) Add Algorithm 1 for the calibration, and move the six budget constants
from §4.1 to where each is used. (4) Fix Figure 1 and redraw Figure 2 on the numbers of Example 4.1. (5) Rework Table
2: name first, example column filled, theorem numbers in "Theory", one prior table instead of two.
