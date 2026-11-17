# How the method works — an intuitive overview (reader-facing draft v0.1, W3-READER, 2026-11-15)

*For the chapter, the paper and the advisor report, placed before the formal setup. Symbols are those of
`NOTATION.md`. Code facts are pinned in the traceability section at the end (file:line on `main`), which is stripped
from reader-facing copies. Facts from the helper file `helpers/CODE_FACTS.md`, spot-checked by the lead.*

---

## The problem

We want the posterior distribution over models, $\pi(S\mid y)$, for all $S$ with at most $K=\min(p,\lfloor n/2\rfloor)$
predictors, when $p$ may be in the thousands or millions. Each model's score $F(S)$ is available in closed form (the
prior and the coefficients integrate out), so the difficulty is purely one of **search and integration over an
astronomically large, rugged space**. Two features make it rugged: correlated predictors create near-ties between
models that differ by swapping a truth for its proxy, and a predictor that is useless given the truth can look useful
on its own ("leakage"). The method is built so that each stage removes one of these difficulties, and so that every
number it prints has a precise meaning.

## The pipeline at a glance

```
 data (X, y)
   │  1. standardise; closed-form score F(S) = log prior + log marginal likelihood
   │     (small problems: enumerate every model exactly and stop)
   ▼
 2. BLOCKS: cluster correlated predictors into blocks of ≤ 16; score every subset of every block
   ▼
 3. START LAW π0 = size prior × product of block scores   (exact normaliser, exact sampler)
   │        └─ start mode S̃0 = most probable model under π0
   ▼
 4. CALIBRATION: pilot runs choose the temperature ladder from π0 to π and the effort level;
   │              everything is then frozen
   ▼
 5. FINAL SMC: 4 independent islands × N particles move from π0 to π along the frozen ladder
   │           (reweight → resample → MCMC moves); evidence Ẑ and Rao–Blackwellised PIPs
   ▼
 6. LOCAL SEARCHES: from the best model found, and from the start mode S̃0 (deterministic);
   │                each move = best single add / delete / swap that strictly improves F
   ▼
 7. OUTPUT: reported model Ŝ (best model ever scored), PIPs, MPM, Ẑ, certificate, diagnostics
```

*Figure for the paper (sketch):* a left-to-right flow with seven boxes as above; under boxes 3–5 a strip showing the
distribution being tracked ($\pi_0\to\pi_{\phi_1}\to\cdots\to\pi$), and an arrow from box 3 to box 6 labelled "start
mode" to show that the second local search does not depend on the particles. Colour the two exact components (block
tables, start law) differently from the stochastic ones (SMC) and the deterministic search.

## Stage by stage: what problem each stage solves

**1. Standardisation and the score.** Every predictor is centred and scaled, and so is the response; the intercept is
removed by centring. Under the shipped prior (a beta-binomial prior on the model, which charges about
$\log(2p/(k+1))+\tfrac12\log n$ for adding a variable to a model of size $k$; a ridge-stabilised $g$-prior with $g=n$ on
the coefficients; an inverse-gamma prior on the noise variance) the score $F(S)$ is a closed-form function of
$X_S^\top X_S$ and $X_S^\top y$. *Problem solved:* the posterior is known up to one constant, and results do not
depend on the units of $y$. When the model space is small enough, the method simply enumerates it and returns the
exact posterior.

**2. Blocks and exact block tables.** Predictors are clustered by absolute correlation (complete linkage) into blocks
of at most 16 columns, and *every* subset of every block is scored against the full response. *Problem solved:* the
hardest local competition — a truth against its close proxies, which tend to land in the same block — is resolved
exactly and once, at a cost of at most $2^{16}$ scores per block.

**3. The start law and the start mode.** The start law multiplies the size prior by the block scores,
$\pi_0(S)\propto w(|S|)\prod_b r_b(S\cap C_b)$: it is the posterior one would have if the evidence for a model split
across blocks. It ignores interactions *between* blocks, but it can be normalised and sampled exactly by a dynamic
programme over model sizes. *Problems solved:* (i) the sampler starts from i.i.d. draws of a distribution close to
the target instead of from an arbitrary model; (ii) its exact normaliser anchors the evidence estimate; (iii) its mode
$\tilde S_0$ is a data-driven, deterministic guess of the true model. *What it gets wrong:* a predictor in one block
that imitates a truth in another block looks useful on its own, so $\pi_0$ may include it (leakage). Theorem 5 shows
that, when such imitators are confined to a small set, $\pi_0$ puts mass $1-n^{-c}$ ($c<\tfrac12$) on the right models as
$n$ grows.

**4. Calibration (choosing the ladder, then freezing it).** The sampler moves from $\pi_0$ to $\pi$ through tempered
distributions $\pi_\phi\propto\pi_0^{1-\phi}\pi^{\phi}$, $0=\phi_0<\phi_1<\dots<\phi_T=1$. Pilot runs choose the ladder
adaptively (each step keeps an effective sample size of $90\%$), then refine it on the set of good models already
found until it stops changing; if diagnostics fail, the whole calibration is repeated once with four times the effort.
If no acceptable ladder is built, the pilot's own ladder is used, so the run always proceeds. *Problems solved:* the
ladder is fitted to this data set, and it is **frozen before the final run draws any random number**, so the final run
is a standard SMC sampler with a fixed schedule — this is what makes its evidence estimate unbiased and its outputs
analysable. Together with the fallback ladder, freezing guarantees that a run with enough computing allocation always produces
output (the delivery result used in Theorems 6–7).

**5. The final SMC run.** Four independent islands, each with $N\ge\max(2500,n,p)$ particles, start from i.i.d. draws
of $\pi_0$. At each rung of the ladder the particles are reweighted by how much more the next distribution likes them,
resampled, and moved by MCMC steps that leave the current distribution invariant: a Gibbs update of every coordinate,
random swaps, swaps with correlated neighbours, and independence proposals drawn from $\pi_0$. At $\phi=1$ the PIPs are
averaged from the Gibbs inclusion probabilities (Rao–Blackwellisation) and pooled with **equal weights** across islands (islands are not weighted by their evidence);
the evidence $\hat Z$ is the product of the average reweighting factors, averaged across islands. *Problems solved:*
moving from an easy distribution to the hard one in small steps avoids getting trapped; the independence and
neighbour-swap moves let particles jump between near-equivalent models; independent islands give a check of
stability.

**6. Local searches.** After the islands, the method runs a deterministic hill climb twice: from the best model found so
far, and — independently of all particles — from the start mode $\tilde S_0$. Each move scans every neighbour (delete
one, add one, swap one for one) and moves to the best one only if it strictly improves $F$; a search that ends because
no neighbour improves has **certified** its end point as a local optimum. *Problems solved:* the search from the start
mode undoes leakage: spurious members of $\tilde S_0$ are deleted one per move (Theorems 6–7 show it lands exactly on
$S_0$, deleting at most $n^b$ columns, under their conditions); and certification gives a checkable guarantee
(Theorem 8: certified small models contain $S_0$).

**7. What is reported.** Every model scored anywhere — block tables, calibration, particles and their proposals, both
local searches — is recorded, and the **reported model** $\hat S$ is the best-scoring one. The method also reports the
pooled PIPs, the MPM ($\mathrm{PIP}>\tfrac12$), the evidence $\hat Z$ (with a one-sided lower bound), whether $\hat S$ is
certified, and diagnostics (island disagreement, low effective sample size). *What the output looks like at moderate
$n$:* with many predictors, the posterior (and the method's output) is a mixture over the true model and its many
one-variable supersets $S_0\cup\{j\}$. Each superset is individually light, but together they can weigh as much as
$S_0$ itself, so $\pi(S_0\mid y)$ may be well below one at moderate $n$; the theorems describe the limit. If the run hits its time or memory
allocation it stops, returns the best model scored so far, and marks the estimates unavailable.

## Which theorem speaks to which stage

| Stage | Question | Theorem |
|---|---|---|
| target $\pi$ | does the exact posterior find the truth, and how fast? | 1, 2 (rate), 3 (optimality), 4 (omitted variables), 9 (distributions; in progress) |
| start law $\pi_0$ | does the cheap block approximation already point at the truth? | 5 |
| local search from $\tilde S_0$ + reported model | does the software report $S_0$? | 6 (random design), 7 (fixed design) |
| certificate | what does a certified small model guarantee without any structural condition? | 8 |
| calibration freezing | does a run always produce output? | delivery result, used inside 6–7 |
| SMC estimates | are the printed PIPs and $\hat Z$ consistent / unbiased? | sampler results (body of the paper; not on the headline card) |

## A toy example

Six predictors, $n=100$, true model $S_0=\{1,3\}$ with coefficients $1$ and unit noise. Predictor 2 is a near copy of 1
(correlation $0.93$); 4 is moderately correlated with 3 ($0.69$); 5 is correlated with 1 ($0.63$) and 6 is a near copy
of 5 ($0.89$). With $p=6$ the method's blocks have at most two columns; here they are $\{1,2\},\{3,4\},\{5,6\}$ — the
imitator 5 sits in a different block from the truth it imitates.

| model | start law $\pi_0$ | posterior $\pi(\cdot\mid y)$ |
|---|---|---|
| $\{1,3,5\}$ | **0.517** | 0.042 |
| $\{1,3\}$ | 0.198 | **0.688** |
| $\{1,3,6\}$ | 0.067 | 0.118 |
| $\{1,3,4\}$ | 0.012 | 0.051 |
| $\{1,2,3\}$ | 0.008 | 0.037 |

*Reading.* Within its own block, predictor 5 explains a lot of $y$ (it carries part of predictor 1's signal), and the
start law cannot see that predictor 1, in another block, already explains it. So the start mode is $\{1,3,5\}$:
**leakage**. The proxy 2, which shares predictor 1's block, is correctly handled already by the block table. The true
posterior, which sees all interactions, puts $0.69$ on $\{1,3\}$, and the PIPs are $(0.99,0.07,1.00,0.08,0.06,0.16)$, so
the MPM and the HPM are $\{1,3\}$. (With six predictors the posterior is nearly concentrated; with thousands of
predictors at moderate $n$ it is a mixture over $\{1,3\}$-like truths and their many one-variable supersets, each light,
together comparable to the truth's own weight.) The local search from the start mode makes one move — delete 5 — reaches $\{1,3\}$,
finds no improving neighbour and certifies it. In the theory, $Q=\{1,3,5\}$ is the leakage set, the lattice
$\{\{1,3\},\{1,3,5\}\}$ is the route, and "delete the extras one at a time" is exactly what Theorems 6–7 prove happens
in general.

(Computed with an independent re-implementation of the coded score, start law and search rule on this one data set:
`numerics/toy_example.py`, output `numerics/toy_example_out.txt`; the partition was fixed by hand to the one the
clustering produces for these correlations. Illustration only, not a test of the production code.)

---

## Traceability (internal; strip before use)

All pins are `Scripts/SMC_BVS/core/…` on `main` (equal on this branch); from `helpers/CODE_FACTS.md`; the lead
re-checked the ones marked ✓.

| Fact | Pin |
|---|---|
| entry point `v3_fit(X, y, seed, allocation, ls0 = TRUE)` | `v3_fit.R:73` |
| constant columns dropped; standardisation ($\|x_j\|^2=n-1$, $y^\top y=n-1$) | `v3_preprocess.R:111-113`, `:37-68` |
| $a_0=b_0=0.01$ ✓; $K=\min(p,\lfloor n/2\rfloor)$ ✓; $\log w(k)=-\log2-\log\binom{2p-1}{k}$ ✓ | `cpp/v3_score.h:14`, `:40`, `:64-65` |
| $H_S=(n+1)G_S+I$, $A_S=G_S+I$, $Q_S$, $\log m(S)$ | `cpp/v3_score.h:175-183`, `:217-223` |
| $F(S)=\log\varpi(|S|)+\log m(S)$ | `cpp/v3_engine.h:97` |
| exact branch iff $\sum_{k\le K}\binom pk\le(5H_0+4N_0)p$ | `v3_fit.R:105-106`; `cpp/v3_core.cpp:71-85` |
| block size $B=\min(\lfloor\sqrt n\rfloor,\lfloor\sqrt p\rfloor,16)$ ✓; complete linkage on $1-|r|$, top-down cut, next-fit packing | `v3_preprocess.R:22`; `cpp/v3_blocks.h:39-141` |
| block tables $r_b(U)=m(U)/m(\emptyset)$ | `cpp/v3_start.h:76-98` |
| start law $\gamma_0$, exact normaliser (size-profile DP), exact sampler | `cpp/v3_start.h:68-70`, `:101-137`, `:153-176` |
| start mode (max-plus DP; tie-aware fallback; enumeration cap $10^6$) | `cpp/v3_start.h:195-305`; `cpp/v3_core.cpp:469` |
| bridge $\gamma_\phi=\gamma_0e^{\phi d}$, $d(S)=\log\mathrm{BF}(S)-\sum_b\log r_b$ | `cpp/v3_engine.h:14`, `:88-97` |
| reweight, $\log$ increment, resample every stage ✓, one MCMC round per stage | `cpp/v3_engine.h:316-331` |
| MCMC round: $p$ Gibbs + uniform swap + $B$ neighbour swaps + independence from $\pi_0$, random order | `cpp/v3_engine.h:111-214` |
| islands $R=4$ ✓; $N_0=\max(2500,n,p)$ ✓; burn-in $L=\max(4,\lceil\log_2(n+1)\rceil)$; 4 measured rounds | `v3_run.R:91`; `v3_preprocess.R:24-25`; `v3_run.R:90` |
| pilot: adaptive step, ESS $\ge0.90H$, step floor $1/T_e$ | `cpp/v3_calib.h:25-46` |
| grid on candidate set $V$ (restricted ESS $\ge0.90$); rebuild until identical | `cpp/v3_calib.h:48-98`; `v3_calib.R:84-119` |
| triggers E1/E2/E3 etc.; one escalation to tier 1 ($4\times$) | `v3_calib.R:60-61`, `:101-110`, `:150-159` |
| grid fallback (pilot schedule / last success), default on | `v3_calib.R:120-124`, `:141-151`; `v3_fit.R:151` |
| frozen schedule; final run on disjoint random streams | `v3_run.R:68-76`, `:8-11`; `v3_calib.R:184-190` |
| local search: neighbours, strict improvement, lexicographic ties, certification, cap | `cpp/v3_engine.h:370-419` |
| final local search from HPM, cap $\ell=\lceil\log_2(n+p+1)\rceil$ | `cpp/v3_core.cpp:453-458`; `v3_preprocess.R:23` |
| LS0 from start mode, cap $\ell+|\tilde S_0|$ ✓, no uniforms; guard stop ⇒ no output | `cpp/v3_core.cpp:460-481`, `:473` |
| pooled PIP = equal-weight island mean ✓; MPM = PIP > 0.5 ✓ | `v3_run.R:159-163` |
| evidence $\hat Z=\frac1R\sum_r\hat Z_r$; lower bound $0.05\hat Z$ | `v3_run.R:154-155` |
| HPM = best $F$ over every scored model (ties: smaller, then lexicographic) | `cpp/v3_util.h:120-126`; `cpp/v3_ledger.h:82-113` |
| `local_certified` meaning | `v3_run.R:178-195` |
| no-output statuses; best model returned on stops | `v3_run.R:109-114`; `v3_fit.R:134-137`, `:154-159`; `cpp/v3_runtime.h:13-27` |

Notes for HQ: (i) the code reports `hpm` and `mpm` without naming one "the selected model"; the theory's reported
model is `hpm`. (ii) The Ẑ-weighted PIP described in the methodology document, and called primary for v3.1 in
`Theory_work/State_of_Project/sections/02_method.tex:440-451`, is not computed by the shipped code (README:16); the code
pools with equal weights (`v3_run.R:154`, `:162`). Follow the code (Theory Dept manager, 2026-11-15). (iii) The tempered target is written $\pi_0^{1-\phi}\pi^\phi$ up to constants
($\gamma_\phi=\gamma_0^{1-\phi}\gamma_1^{\phi}$ with $\gamma_1\propto$ target).
