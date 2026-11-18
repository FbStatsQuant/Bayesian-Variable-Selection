# Reader versions of the headline theorems — draft v0.4 (W3-READER, bridge leg, 2026-11-16)

v0.4 = v0.3 with H5 card 6, the Engineering D-17 wording, and the repairs of the S2 line check and the S3 diff check
(markers [H5-6], [ENG-D17], [S2-F#], [S3-N#]); per-row tags in the update logs (confirmed by S3).
S4 repairs (Sol statement-change check, `reviews/S4_statement_change_sol.md`) carry markers [S4-S1], [S4-F1], [S4-F2], [S4-S3],
[S4-E1]; swap tags are delta-relative, with the S3-relative strength recorded in each row's update log [S4-S3].

v0.3 = v0.2 with the manager's CP1 decisions and the H5 card-5 actions (markers [H5-#]): Theorem 1 re-based on the
posterior refinements (expectation rate; Theorem 1′); (S4) completed from the delivery premise table
(`lemmas/R3_delivery_assembly.md`) [R3]; Theorem 7 states non-constant raw columns [R3]; Theorem 4's masters are the
fixed-design MIS(i)/(ii) with Cor-G(b) as their Gaussian-row reader version [H5-3]; new Theorem 10 (card row 3.6,
printed outputs) and the pooled-evidence remark (row 3.5). v0.2 = v0.1 with all twelve findings of the Sol fidelity
read S1 applied (`reviews/S1_fidelity_sol.md`, `reviews/S1_disposition.md`); markers [S1-F#].

**How to read this file.** Each section has: the **reader statement** (numbered assumptions in standard terms, a
conclusion in 1–3 displays, notation from `NOTATION.md` only); **one line per assumption** (why it is there, whether it
is known to be necessary); the **master theorem** it follows from (registry id@version, file:lines, status verbatim);
the **bridges** from the reader assumptions to the master's hypotheses, each marked **EXISTS-CHECKED** (registry status
"PROVED-CHECKED"), **EXISTS-UNCHECKED** (exists, status below PROVED-CHECKED, quoted) or **NEW** (stated precisely
here, with an effort estimate); and **honest limits**. Reader statements are deliberately *stronger in hypotheses*
than the masters where that buys clarity; nothing in a conclusion goes beyond the master.

Status conventions (binding): statuses are quoted verbatim from `Theory_work/INFRA/registry/claims.tsv` (requoted at
main 14892123); long council suffixes are cut after the first clause and marked "…". Nothing below
PROVED-CHECKED is called checked; "conditional on …" is carried.

**Standing assumptions and conventions** (used by every theorem below; stated once in the paper's setup section).
(S1) Model of §1 of the notation: Gaussian errors with fixed variance $\sigma_*^2>0$, independent of the design.
(S2) Asymptotics: $n\to\infty$, $p=p_n$ with $2\le p\le n^A$ for a fixed $A\ge1$ ($p\gg n$ allowed).
(S3) "The method" means the method as coded, under the standing conventions of `NOTATION.md` §5 (exact arithmetic,
shipped configuration, admissible runs). (S3) matters only for Theorems 5–8.
(S4) *Delivery conventions* (used only by the "always produces output" clauses of Theorems 6–7) [S1-F2, S2-F1, FUNI-N, RM2R-1] — the
delivery contract of the method, incorporated by reference and stated here in words: (i) *idealised machine*: exact
arithmetic at unit cost (including exp and log); no integer, index, stream-id or allocation overflow, and the two fixed
integer limits of the code named below the delivery display of Theorems 6–7 are idealised (IDEAL-W⁺) [RM2R-1, RM2R-5]; wall time at most
$\tau\cdot(\text{operation count})+\tau_0$ and peak memory at most $\beta\cdot(\text{words held})+\beta_0$ for fixed constants
$(\tau,\tau_0,\beta,\beta_0)$; every allocation within the declared memory succeeds; the build and its dependencies work; no
external interruption or worker crash; (ii) *covered configuration*: the production core with the local search from the
start mode (cap $\ell_n+|\tilde S_0|$) and the tie-aware start-mode fallback, implemented with
$O\big(p\sum_b(2^{|C_b|}+(K+1)^2)\big)$ operations and $O\big(\sum_b2^{|C_b|}+J(K+1)\big)$ storage; the local search from the
start mode starting at the smallest, lexicographically first maximiser of the start law; the default list of
summaries only; certificate computations with declared polynomial operation and memory budgets, included in the
allocation; serial execution or a fixed number of concurrent workers (memory envelope multiplied by that number); fixed
number of islands; the grid fallback switched on (shipped default); (iii) *random numbers and stops*: ideal independent
uniform random numbers; the method's stop/return rule and stop-only resource guard as coded (a stopped run returns no
estimates); (iv) *inputs and allocation*: a valid non-degenerate input (finite data, response of length $n$ and not constant, at
least one non-constant predictor column; a single seed, an integer in $[1,2^{31}-1]$) [RM2R-1] and a declared memory and time
allocation $(\mathrm{mem}_n,\mathrm{time}_n)$ at least the method's explicit polynomial work and memory envelopes in
$(n,p_{\mathrm{raw}})$, including the preflight bounds and the local-search archive and time bounds (stated in full in the
paper's appendix). These are operational assumptions, not consequences of (S1)–(S3) or of any design condition.
*Source of record (shipped method):* the delivery premises (D) with IDEAL-W⁺ of `Theory_work/Wave3/W3-RM2-R/STATEMENT.md:71-93`,
whose lemma DLV-0 re-audits the code as pinned [RM2R-2]; they take over, with the two additions above, the premises of
`Theory_work/Wave1C/C-DLV/STATEMENT.md:21-46` (IDEAL-W, EX-A as a cost model, MACH, CONFIG,
TDP-IMPL, valid inputs, declared allocation) and the amended allocation of `Theory_work/Wave1C/FINAL/sections/s6_delivery.tex:29-62`
($W_G$, $M_G$, $P_0$, $P_1$, $\bar P_t$, certificate budgets, the LS0 preflight addition). The two limits: `Scripts/SMC_BVS/core/v3_run.R:96` (`le > 10^6`) and
`cpp/v3_core.cpp:474` (`cap_ll > INT_MAX`); $\mathfrak D:=\{(n,p_{\mathrm{raw}}):\lceil\log_2(n+p_{\mathrm{raw}}+1)\rceil\le10^6,\ \lceil\log_2(n+p_{\mathrm{raw}}+1)\rceil+\lfloor n/2\rfloor\le2^{31}-1\}$
(sufficient, not necessary); A:IDEAL-W⁺ as registered in `Theory_work/INFRA/registry/assumptions.tsv` (row `A:IDEAL-W+`, version 1.0.0;
source `FUNI_NARROW/A_IDEALW_PLUS.md@fc30c749`; its statement is contained word for word in this ticket's earlier carrier copy
`reviews/carriers/A_IDEALW_PLUS.md`) [FRZ-RQ]. The two limits in words: the sentence [RM2R-5] after the
delivery displays of Theorems 6 and 7.
(S5) *Sampler conventions* (used only by Theorem 10 and the pooled-evidence remark) [R4, S2-F2] — the sampler contract,
incorporated by reference and stated in words: exact arithmetic; within each random stream, fresh independent ideal
uniforms; the final run's stream for each island independent of the data and of the calibration's streams [S3-N1]; the coded start sampler
returns exact draws from $\pi_0$ **and** the reported start normaliser equals $\sum_{S\in\Omega}\gamma_0(S)$ exactly; the coded
MCMC steps realise their stated kernels, applied in a uniformly random order independent of the state; the calibration
record is a function of the data and the calibration streams; the island record is a measurable function of the
calibration value and its stream; statements about estimates refer to the potential (uninterrupted) run, identified
with the reported fields on completed runs. *Source of record:* `Theory_work/Wave1/W1-N1/STATEMENT.md:70-88` (EX-A,
EX-S/H-U, START, KERNEL, CAL, SI, MEAS, potential run; inherited statuses: START "PROVED (candidate)" (N1:75), KERNEL
"PROVED (candidate), code-checked; CHK_INHERITED VERIFIED WITH AMENDMENT") [S3-N8], the code bridge `W1-N1/lemmas/L1_bridge.md:33-55` (measurability,
control flow), and `W3-SAMP/STATEMENT.md:29-53, 64-70, 90-95` (localisation, production values, Lemma PC).


**Row structure (for in-place updates).** Each theorem section is one card row, delimited by
`<!-- ROW thmK BEGIN -->` / `<!-- ROW thmK END -->`. A READER_DELTA (from the Theory Department riders) replaces the
affected blocks of one row in place — reader statement, assumption lines, master, bridges — bumps that row's
**Section version**, and adds one line to its **Update log** (with the STRONGER / WEAKER / EQUAL tag of the master's
changelog). No other row changes. The bridge summary at the end is regenerated from the rows.

Numbering of the headline theorems (proposal; see `CLAIMS_CARD.md`):
1. Posterior concentration, fixed design — §1
2. Posterior concentration, random Gaussian design — §2
3. The rate cannot be improved — §3
4. Omitted variables (misspecification) — §4 (card row 1.4)
5. The start law already concentrates — §5
6. The reported model, random Gaussian design (main theorem) — §6
7. The reported model, fixed design — §7 (honest limits: sample-level conditions)
8. Certified screening — §8
9. Distribution-level consistency — §9
10. The printed outputs are consistent, for designs with no leakage outside the true model such as independent predictors (card row 3.6) — §10; with the pooled-evidence remark (row 3.5)

---

## 1. Theorem 1 — Posterior concentration (fixed design)
<!-- ROW thm1 BEGIN -->
**Card row** 1.1 · **Section version** 1.0 (2026-11-16) · **Pending delta** —


### Reader statement
**Theorem 1.** Let the design be fixed. Assume
- **(A1) Model.** (S1) and (S2).
- **(A2) Sparsity.** $s_0\ge1$ is fixed.
- **(A3) Bounded coefficients.** $\max_{j}|\theta^*_j|\le\bar\theta$ for a fixed $\bar\theta<\infty$.
- **(A4) Sparse eigenvalue floor.** $\lambda_{\min}(\hat R_S)\ge\varphi_0^2$ for every $S\subseteq[p]$ with
  $|S|\le 2(A+1)s_0+2$, for a fixed $\varphi_0\in(0,1]$.
- **(A5) No near-collinearity among $O(\log n)$ columns.** $\lambda_{\min}(X_S^\top X_S)\ge g_0$ for every $S$ with
  $|S|\le 3(A+1)(s_0+1)\log n$, for a fixed $g_0>0$.
- **(A6) Beta-min.** $\theta^*_{\min}\ge C_\beta\,\sigma_*\sqrt{\log n/n}$ with a fixed $C_\beta>0$ such that
  $C_\beta^2\varphi_0^2>c_0(s_0,A)$ [S1-F1]; or $\theta^*_{\min}\ge\sigma_*\sqrt{M_n\log n/n}/\varphi_0$ for a fixed sequence $M_n\to\infty$.

Then there are $n_0$ and $C$, depending only on $(s_0,A,\sigma_*^2,\bar\theta,\varphi_0,g_0,C_\beta)$, such that for every
$n\ge n_0$ and every design and $\theta^*$ satisfying (A1)–(A6) at that $n$ [H5-1]
$$
E\big[1-\pi(S_0\mid y)\big]\ \le\ C\sqrt{\tfrac{\log n}{n}},
$$
and consequently, along any sequence satisfying (A1)–(A6),
$$
P\big(\mathrm{HPM}=\mathrm{MPM}=S_0\big)\ \ge\ 1-4C\sqrt{\tfrac{\log n}{n}}\ \to1,\qquad
\max_{j\le p}\big|\mathrm{PIP}_j-\mathbf 1\{j\in S_0\}\big|\le 1-\pi(S_0\mid y)=O_P\Big(\sqrt{\tfrac{\log n}{n}}\Big).
$$
(Expectation over the noise, design fixed. With the second form of (A6), $n_0$ depends also on the sequence
$(M_n)$.)

**Theorem 1′ (no eigenvalue condition off $S_0$ beyond the vanishing floor (A5)).** Replace (A4) by
- **(A4′) Floor on the truth and an identifiability margin.** $\lambda_{\min}(\hat R_{S_0})\ge\varphi_0^2$, and every model
  $S$ with $|S|\le K$, $S_0\not\subseteq S$ and at most $j_0:=\lceil(2A+1)s_0\rceil+1$ variables outside $S_0$ leaves
  residual signal $\|(I-P_S)X\theta^*\|^2\ge c\,\sigma_*^2\log n$, with a fixed $c>c_1(s_0,A)$, where $c_1(s_0,A)$ is an
  explicit constant, not optimised [H5-6],

and drop (A6). Then the conclusions of Theorem 1 hold (the expectation bound with constants depending on
$(s_0,A,\sigma_*^2,\bar\theta,\varphi_0,g_0,c)$). [H5-1]

*Remarks (go to the paper's remarks, not the statement).* (o) [H5-1] (A5) can be weakened to a condition on the
Occam factors of over-fitted models (a "superset Occam sum"); a readable sufficient form is determinant growth,
$\det H_{S_0\cup J}\det(G_{S_0}+I)/(\det H_{S_0}\det(G_{S_0\cup J}+I))\ge[c_D(n+1)]^{|J|}$ for $1\le|J|\le3(A+1)(s_0+1)\log n$.
In Theorem 1′ the margin replaces the bounded-size floor (A4) off $S_0$ and beta-min (the vanishing floor (A5) on
$O(\log n)$-sets is kept) [S2-F6]: under (A4) and (A6) it holds with
$c=C_\beta^2\varphi_0^2(1-1/n)$, so Theorem 1′ contains Theorem 1 when $C_\beta^2\varphi_0^2>c_1$; for
$c_0<C_\beta^2\varphi_0^2\le c_1$ the two coexist (both are explicit constants depending only on $(s_0,A)$, not
optimised) [H5-6]. (i) The last inequality holds for every data set; with the
first display it gives sensitivity and specificity of all PIPs at rate $\sqrt{\log n/n}$, uniformly in $j$.
(ii) Without (A6): $\pi(S\supsetneq S_0\mid y)=O_P(\sqrt{\log n/n})$ (no over-fitting mass) and every truth with
$\theta_j^{*2}\ge c\,\sigma_*^2\log n/(n\varphi_0^2)$, $c>c_0$, has $1-\mathrm{PIP}_j=O_P(\sqrt{\log n/n})$; specificity can
fail without beta-min (numerical counterexample). (iii) $c_0(s_0,A)$ is an explicit constant depending only on $(s_0,A)$, not optimised (formula in the appendix)
[H5-6]. (iv) (A3) is used only through the energy bound $\|X\theta^*\|^2\le n s_0^2\bar\theta^2$; any bound
$\|X\theta^*\|^2\le nM$ suffices. (v) Models of size $\ge 3(A+1)(s_0+1)\log n$ carry posterior mass $O_P(n^{-1/2})$ with
no eigenvalue condition (size-tail lemma, which uses a coefficient bound instead; separate statement). (vi) *Scope of
the rate* [H5-6]: on every design with $s_0\le\min(K-1,p/2)$ the posterior miss is at least of order $n^{-1/2}$ (Theorem 3(a); $s_0\le K-1$ suffices, by Corollary B with $c(p,s_0)\ge1$ or by Prop. LB) [R1-S3, R2-O2]; the extra
$\sqrt{\log n}$ has been shown to be attained on the witness designs of Theorem 3(b); on other designs it is not known
[S3-N5]. No two-sided rate on every design is claimed: a matching lower bound $E[1-\pi(S_0\mid y)]\gtrsim\sqrt{\log n/n}$ in
expectation, under a floor on $S_0\cup\{j\}$, is open (post-freeze rider POST2-R1); in probability the $\sqrt{\log n}$
factor is shown only when $\log p\asymp\log n$ (Theorem 3(b)) [S3-N4]. (vii) *What was observed at
moderate $n$ (an observation, not a theorem)* [ENG-D17, R1-F3]: in the Engineering configurations measured for decision D-17 (Engineering working file `Docs/Experiments/P1M/DECISIONS.md` in the main checkout, not git-tracked), substantial posterior mass sat on $S_0$ and its one-variable
supersets $S_0\cup\{j\}$, each individually light but together comparable to $S_0$. No general finite-$n$ statement about
the shape of the posterior or of the output is proved here; the theorem describes the limit $n\to\infty$.

### Why each assumption, and is it necessary
- (A1) Gaussian errors give exact $\chi^2$ laws for the score differences. Necessity open; every comparable Bayesian
  selection theorem assumes it. $p\le n^A$ enters through union bounds over models of size $O(\log n)$; open.
- (A2) Fixed $s_0$ keeps combinatorial constants bounded. Close to necessary for this rate: on *every* design with $s_0\le\min(K-1,p/2)$ the rate
  $\sqrt{\log n/n}$ forces $s_0=O(\sqrt{\log n})$, and $\pi(S_0\mid y)\to1$ forces $s_0=o(\sqrt n)$ (Theorem 3).
- (A3) Bounded signal energy keeps the posterior of the noise variance on scale. Believed improvable (sub-linear growth);
  some control of the coefficients is necessary for the size-tail step (explicit counterexample).
- (A4) Lets the posterior separate $S_0$ from under-fitted models of bounded size. The part *anchored at $S_0$* is
  needed at the beta-min scale (numerics); the floor on null-only directions looks removable (numerics; an unchecked
  strengthening replaces it by an identifiability margin).
- (A4′) of Theorem 1′, the floor $\lambda_{\min}(\hat R_{S_0})\ge\varphi_0^2$ on the truth: **sufficient; not known to be
  necessary (open item O3)** [H5-6]. The margin's constant $c_1$: proof artefact (open item O2).
- (A5) Excludes exact (or near-exact, $\lambda_{\min}<g_0$ unnormalised) linear dependence among $O(\log n)$ columns, so
  over-fitted models pay their full Occam factor. Note the floor is $g_0/(n-1)$ on the correlation scale: it vanishes.
  Looks improvable (numerics); an unchecked strengthening replaces it by a weaker Occam-sum condition.
- (A6) The signal must beat the prior cost of one variable plus a $\chi^2$ fluctuation, both of order $\log n$. The
  order $\sqrt{\log n/n}$ is necessary by numerics and a leading-order heuristic (not proved); the constant $c_0$ is a
  proof artefact.

### Master theorem
`W3-POST:Thm-1@1.0.1` (= `SOP:TH09@1.0.2`, T03♯ with the SL0/SL1 consequences), `Theory_work/Wave3/W3-POST/STATEMENT.md:61-100`
(hypotheses :63-75; conclusions 1–3 at :80-85).
Registry status of `W3-POST:Thm-1@1.0.1`, verbatim: **"PROVED-CHECKED; council C3, MANIFEST 420c1cb0…, astra=8.8 PASS, opus=8.7 PASS"**.
Registry status of `SOP:TH09@1.0.2` (main 6cd699dd, W3-T03ACC accepted) [REG-6cd6], verbatim: **"PROVED-CHECKED (T03♯ only: the conjunction of W3-T03ACC:T03S.1–T03S.4, clause map CHECKPOINT_4.md §2; council R1, MANIFEST 9714aea4…, astra=9.5 PASS, opus=9.4 PASS; LC-A, LC-B, LC-C VERIFIED). Not upgraded (their statuses stay as at theory_main.tsv:68): T02(i♯) and T02(ii♯) PROVED, SF/XF VERIFIED; T01–T03 PROVED-LOCKED (wave 3; external review queued), SAME-FAMILY-ONLY"** [S1-F9]. Theorem 1 (T03♯) is therefore PROVED-CHECKED through `SOP:TH09`, and `W3-POST:Thm-1@1.0.1` now carries the label above and no open condition (relabel, main 2676e71f).
**Re-base [H5-1].** Expectation display: `W3-POST2:C@1.0.7`, `Theory_work/Wave3/W3-POST2/STATEMENT.md:83-94`, case (i)
(hypotheses = Theorem 1's: R1 size conditions, G, (E), (F₀), (F_λ), (F_w), BM($c$), $c>c_0$, all "at that $n$"; HPM/MPM
bounds $P(\cdot\neq S_0)\le2E\delta_n$ at :91). Theorem 1′: `W3-POST2:E@1.0.7` (:126-133) with `W3-POST2:C` case (iii),
and `W3-POST2:A0@1.0.7` (`lemmas/A_occam.md:14-15`) for (F_w) ⇒ (OS). Remark (o): `W3-POST2:A1@1.0.7` (:54-56).
Registry statuses (main 33bfcb9c: `W3-POST:Prop-LB` relabelled PROVED-CHECKED, so `W3-POST2:C` no longer lists it; earlier, at main 2676e71f, `W3-POST2:C@1.0.6` was "PROVED-CHECKED, conditional on W3-POST:Prop-LB, W2-APP:POST"), verbatim [REG-33bf]: `W3-POST2:C@1.0.7` **"PROVED-CHECKED, conditional on W2-APP:POST"**; `W3-POST2:E@1.0.7` **"PROVED-CHECKED, conditional on
W2-APP:POST"**; `W3-POST2:A1@1.0.7` **"PROVED-CHECKED, conditional on W2-APP:POST"**;
`W3-POST2:A0@1.0.7` **"PROVED-CHECKED"**; `W2-APP:POST@1.0.7` **"PROVED-CHECKED"**. W3-T03ACC passed: **Form A applies**
(below). `W3-POST:Prop-LB@1.0.1` is "PROVED-CHECKED; council C3, …" (main 33bfcb9c), so the expectation route (`W3-POST2:C`) lists only `W2-APP:POST`; `[L1a′]` is no longer a listed condition (main 2676e71f).

### Abstract forms of row 1.1 (HQ order 2026-11-16; outcome: **Form A**, W3-T03ACC accepted, main 6cd699dd) [REG-f526, REG-6cd6]
- **Form A — W3-T03ACC passes (T03♯ PROVED-CHECKED).** The abstract states Theorem 1 in its $O_P$ form (rate,
  HPM = MPM = $S_0$, PIPs), whose master then carries no open condition. The design-uniform expectation display and
  Theorem 1′ are stated in the body with their own conditions until those are cleared: the expectation route
  (`W3-POST2:C`) lists `W2-APP:POST` (now "PROVED-CHECKED"; `SOP:TH128` discharged, main 6cd699dd; `[L1a′]` no longer listed, main 2676e71f)
  and, until main 33bfcb9c, listed `W3-POST:Prop-LB` (now "PROVED-CHECKED; council C3, …").
- **Form B — not used (W3-T03ACC passed; kept for the record).** Two variants:
  - **B1 (abstract, condition stated verbatim in reader words):** *"Conditional on the posterior concentration theorem
    for the coded prior — verified independently by reviewers of the same and of a different model family, but without
    a council review yet — the posterior …"*, stated **once** for the abstract rows that rest on it (1.1, 1.2, 3.1).
  - **B2 (body):** row 1.1 moves to the body; then rows 1.2 and 3.1, which rest on the same theorem, move with it.
  - **HQ decision (2026-11-16): Form A if W3-T03ACC passes, B1 otherwise (sentence approved as written); B2 rejected;
    the expectation display and Theorem 1′ stay in the body with their conditions; the abstract uses Theorem 1's $O_P$
    form.** Lead's earlier recommendation: B1. Row 1.1 is the foundation of pillar 1, and rows 1.2 and 3.1 (the main theorem) rest on
    the same theorem; B2 would empty the abstract of its main results, while B1 keeps them with an honest, single
    condition sentence that the reader can check against the statuses.


### Bridges
| # | Bridge | Mark | Detail |
|---|---|---|---|
| B1.1 | (A3) ⇒ (E) $\|\mu\|^2\le nM$, $M=s_0^2\bar\theta^2$ | NEW (one line) | $\|X\theta^*\|\le\sum_{j\in S_0}|\theta^*_j|\,\|x_j\|\le s_0\bar\theta\sqrt{n-1}$. Same remark at W3-POST STATEMENT.md:57. |
| B1.2 | (A4) ⇒ (F_λ) = SE_λ(j₀) | NEW (one line) | Every $S_0\cup J$ with $|J|\le j_0=\lceil(2A+1)s_0\rceil+1$ has $|S_0\cup J|\le(2A+2)s_0+2$. |
| B1.3 | (A5) ⇒ (F_w) = SE_w(m♯_n; g₀) | EXISTS-UNCHECKED + NEW arithmetic | $m^\sharp_n\le s_0+\lceil(\log\binom{p}{s_0}+\tfrac{s_0+1}2\log n+\tfrac12\log n)/\log2\rceil$ ([T03R] E2(ii), stated at W3-POST STATEMENT.md:38-39; inside SOP:TH09, status above). With $\binom{p}{s_0}\le n^{As_0}$ and $n\ge3$: $s_0+m^\sharp_n\le(2s_0+1)\log n+1.45(As_0+\tfrac{s_0}2+1)\log n\le3(A+1)(s_0+1)\log n$. Checked numerically on $A\in[1,20]$, $s_0\le39$, $n\in[3,10^{15}]$ (LOG 2026-11-15). |
| B1.4 | (A6) ⇔ (BM) | identity | (A6) is BM($c$) with $c=C_\beta^2\varphi_0^2$, or BM-∞. |
| B1.5 | δ_n rate ⇒ HPM/MPM/PIP clauses | inside the master | SL0/SL1, deterministic (W3-POST STATEMENT.md:121); expectation form: POST2 C :90-91 ($P(\mathrm{HPM}\neq S_0)\le2E\delta_n$, same for MPM) and Markov. |
| B1.6 | (A1)–(A6) at $n$ ⇒ POST2 C case (i) at $n$ | identity (+ R1) | Same hypotheses, read at a single $n$ (C is uniform: constants depend only on the fixed constants). (F₀) ⇐ (A4) with $S=S_0$. $M=s_0^2\bar\theta^2$ (B1.1). |
| B1.7 | (A4′) ⇒ (F₀) and (ID; $c$) ⇒ (ID$^M$; $c$); (A5) ⇒ (OS) | identity / EXISTS-CHECKED | (ID) ⇒ (ID$^M$) since $L_S\ge\Delta_S$ (POST2 STATEMENT.md:40-41, inside the claim's definitions). (A5) ⇒ (F_w) (B1.3) ⇒ (DG) ⇒ (ADG) ⇒ (OS) for $n\ge n_0$: `W3-POST2:A0@1.0.7`, "PROVED-CHECKED" [REG-6cd6] [REG-f526]. |

**Effort:** B1.1–B1.4 are a half page; one Sol line check.

### Honest limits
None for the statement: every assumption is primitive. The beta-min and margin constants are explicit but not
optimised; the paper should say "a sufficiently large constant depending only on $(s_0,A,\varphi_0)$" in the statement
and give the formulas in an appendix, without numerical values [H5-6]. Theorem 1′ keeps the vanishing floor (A5), which
still excludes exact linear dependence among $O(\log n)$ columns, duplicated null columns included; it is never to be
called "the design-agnostic form" [H5-7.1]. Named open items attached to this row: O1 (a design-free sufficient
condition for the Occam-sum condition; **whether (OS) holds without any eigenvalue condition is open**; ranks with O3
as a post-freeze rider — it would make "no eigenvalue condition off $S_0$" literally true), O2 (margin constant), O3
(floor on the truth) [H5-7.2] — `CARD_ROW11_R03b.md`.

#### Update log (thm1)
- v0.1 2026-11-15: first version (CP1).
- v0.2 2026-11-15: S1 fixes [S1-F1] C_β>0 (STRONGER hypothesis, i.e. corrected); [S1-F9] statuses.
- v0.3 2026-11-16: [H5-1] re-based on W3-POST2 C (uniform expectation rate; conclusion STRONGER, same hypotheses) with
  Theorem 1′ (W3-POST2 E: identifiability margin, no bounded-size floor off $S_0$, no beta-min) and remark (o) (W3-POST2 A1).
  Masters C/E/A1/A0 below PROVED-CHECKED until recorded.
- v0.4 2026-11-16: [H5-6] consultant's conditions: "off $S_0$" wording for Theorem 1′; (A4′) floor line "sufficient;
  not known to be necessary (O3)"; no numerical constant values; rate-scope remark (vi) (EQUAL; wording).
- v0.5 2026-11-16: [ENG-D17] remark (vii) on the moderate-$n$ shape of the posterior (EQUAL; description only).
- v0.6 2026-11-16: [S2-F6] Theorem 1′ title: "no eigenvalue condition off $S_0$ beyond the vanishing floor (A5)" (EQUAL;
  description; HQ-accepted wording).
- v0.7 2026-11-16: [S3-N4, N5] remark (vi): open item scoped to the expectation lower bound under a floor on
  $S_0\cup\{j\}$; "has been shown … on other designs it is not known" (EQUAL; tags confirmed by S3).
- v0.8 2026-11-16: [H5-7] honest-limits paragraph: (A5) still excludes exact dependence (duplicated nulls); O1 ranked
  with O3; "whether (OS) holds without any eigenvalue condition is open" (EQUAL; presentation).
- v0.9 2026-11-16: [REG-f526] statuses refreshed (POST2 C/E/A0/A1 recorded, conditional); abstract Forms A/B added
  (HQ order; CP3 picks on W3-T03ACC) (EQUAL).
- v1.0 2026-11-16: [REG-33e1] Form A no longer carries an SL0 condition; `W2-APP:POST` conditional on SOP:TH09 only (EQUAL).
- FRZ-RQ 2026-11-16: [REG-6cd6] freeze requote (main 14892123): `SOP:TH09@1.0.2` PROVED-CHECKED (W3-T03ACC accepted, 6cd699dd); POST2 C/E/A1/A0 @1.0.5 with TH09/TH128 dropped; Form A applies. Statuses only (EQUAL).
- R1 2026-11-16: council R1 fixes — [R1-S3] lower-bound remark (vi) and (A2) line restricted to $s_0\le\min(K-1,p/2)$ (WEAKER: restores the master's domain); [R1-F3] remark (vii) relabelled an Engineering observation, mechanism sentence removed (WEAKER); [R1-E5] status base line (EQUAL).
- R2-ED 2026-11-16: [R2-O2] remark (vi) domain pointer: $s_0\le K-1$ via Corollary B or Prop. LB (EQUAL).
- FRZ-B 2026-11-16: requote at main 2676e71f [REG-2676] (relabel D97): `W3-POST:Thm-1@1.0.1` "PROVED-CHECKED; council C3, …"; POST2 C/E/A0/A1 @1.0.6 with the Thm-1 and [L1a′] conditions dropped; EQUAL (statuses only).
<!-- ROW thm1 END -->

---

## 2. Theorem 2 — Posterior concentration (random Gaussian design)
<!-- ROW thm2 BEGIN -->
**Card row** 1.2 · **Section version** 0.5 (2026-11-17) · **Pending delta** — (v0.5 update-log entry: last line of #### Update log (thm2))


### Reader statement
**Theorem 2.** Let the rows of $X^{\mathrm r}$ be i.i.d. with mean $m_n$ and covariance matrix $\Sigma_n$, a correlation matrix, sub-Gaussian along sparse directions: for a fixed $L$, $E\exp\{\lambda u^\top(x-m_n)\}\le\exp\{L^2\lambda^2u^\top\Sigma_nu/2\}$ for every $\lambda\in\mathbb R$ and every $u$ with at most $5(A+1)(s_0+1)\log n$ nonzero entries (Gaussian rows $N_p(m_n,\Sigma_n)$: $L=1$), and
assume
- **(A1) Model.** (S1) and (S2).
- **(A2) Sparsity and fixed signals.** $s_0\ge1$ is fixed and $b_{\mathrm{lo}}\le|\beta^*_j|\le b_{\mathrm{hi}}$ for
  $j\in S_0$, with fixed $0<b_{\mathrm{lo}}\le b_{\mathrm{hi}}<\infty$.
- **(A3) Population sparse eigenvalue floor.** $\lambda_{\min}(\Sigma_{n,S})\ge\varphi^2$ for every $S$ with
  $|S|\le 5(A+1)(s_0+1)\log n$, for a fixed $\varphi\in(0,1]$ (for instance, $\lambda_{\min}(\Sigma_n)\ge\varphi^2$).

Then, under the joint law of design and noise, the three conclusions of Theorem 1 hold:
$$
1-\pi(S_0\mid y)=O_P\Big(\sqrt{\tfrac{\log n}{n}}\Big),\qquad P(\mathrm{HPM}=\mathrm{MPM}=S_0)\to1,\qquad
\max_j|\mathrm{PIP}_j-\mathbf 1\{j\in S_0\}|=O_P\Big(\sqrt{\tfrac{\log n}{n}}\Big).
$$

*Remarks.* (i) Gaussian rows satisfy the sub-Gaussian condition with $L=1$, so the Gaussian statement (the previous Theorem 2) is the case $L=1$; it also holds with the constant $L$ of the coordinates when $x=m_n+B\xi$, $BB^\top=\Sigma_n$, and $\xi$ has independent, mean-zero, unit-variance coordinates sub-Gaussian with constant $L$ (Rademacher or uniform coordinates: $L=1$; coordinates within $K$ standard deviations of the mean: $L=K$); it fails for a binary predictor whose success probability tends to zero.
(ii) For centred rows it contains the i.i.d. case of the isotropic sub-Gaussian rows of Narisetty and He (2014, Lemma 6.1), the case $\Sigma_n=I$, with a uniform sub-Gaussian bound (verified against arXiv v1: Lemma 6.1, statement p. 16, proof p. 28; journal version (Ann. Statist. 42(2)) not accessed: `reviews/NH14_check.md`); this is the class-1 anchor (HQ rulings D114, D120). As a factual remark, not an anchor, it implies Song and Liang's Condition 1 for the centred rows $x-m_n$.
(iii) No upper eigenvalue bound on $\Sigma_n$ and no beta-min beyond (A2) are needed; $p\gg n$ is allowed. The master allows the floor on sets of size $O(\log n)$ to vanish slowly ($\psi_n\gg(\log n)^{3/2}/\sqrt n$); the reader version uses a constant for simplicity; the sub-Gaussian statement keeps the fixed floor. The coexisting expectation-form statement (Theorem 2X, MIXED / incomparable, conditional) is in §11.

### Why each assumption
- (A1) as Theorem 1.
- (A2) Fixed nonzero coefficients sit far above the $\sqrt{\log n/n}$ detection level, so no separate beta-min is
  needed; fixed $s_0$ as in Theorem 1. Without the lower bound $b_{\mathrm{lo}}$, the no-over-fitting and strong-signal
  clauses still hold (remark (ii) of Theorem 1).
- (A3) Transfers to the sample floors (A4)–(A5) of Theorem 1 with probability $\to1$ (entrywise Gram concentration).
  The small-set part is needed (anchored floors); the $O(\log n)$ part is improvable (the entrywise transfer is crude).
  The sub-Gaussian condition on the rows is used only for the entrywise concentration step (so as to transfer (A3) from the
  population to the sample); the posterior argument uses the observed design only. Gaussian rows are the case $L=1$.

### Master theorem
`W3-POST:Thm-1@1.0.1` item 6 (random-design interface), `Theory_work/Wave3/W3-POST/STATEMENT.md:95-100`, status as in §1;
with `W2-APP:POST@1.0.7`, `Theory_work/Wave2/W2-APP/lemmas/L1_POST.md:27-33`, status verbatim **"PROVED-CHECKED"**
(main 6cd699dd) [REG-6cd6] (`C-PACK:SL0@1.0.1`, the posterior-summary lemma, is now "PROVED-CHECKED"), and its restatement `W3-POST:Cor-1R@1.0.0`
(`W3-POST/STATEMENT.md:106-118`), status **"PROVED (by this seat, unchecked)"**. **Presented statement (sub-Gaussian rows; Gaussian = the case $L=1$):** `W3-D3:Thm2SG@1.0.0` (with `W3-D3:B3w@1.0.0`, `W3-D3:ExSG@1.0.0`), main 0eb1b6ef [REG-0eb1], status verbatim **"PROVED-CHECKED; council R2, MANIFEST 1c14a298…, sol=8.5 PASS, opus=9.3 PASS"** (each); inputs `W3-POST:Thm-1@1.0.1`, `W3-DIST:B0/B1/B2core/B2@1.0.2` (and `W3-DIST:B3@1.0.2` as the proof template of B3w only; its last sentence, conditional on `W3-POST:Thm-1`, is not used), `W3-READER:R1@1.0.5`. **Coexisting statement (Theorem 2X, §11):** `W3-D2:Thm2X@1.0.3` (with `W3-D2:Cor2X@1.0.0`), recorded at main 2e0decc8, status as at main 34c8fb4d [REG-2e0d], **"PROVED-CHECKED, conditional on W2-APP:POST, C-MIS:GDb, C-MIS:Prop-P; council R2, MANIFEST d408b7dc…, sol=9.2 PASS, opus=9.6 PASS"** (each).

### Bridges
| # | Bridge | Mark | Detail |
|---|---|---|---|
| B2.1 | (A3) ⇒ LSF (i) and (ii) with $\psi_n=\varphi^2$ | NEW arithmetic | LSF asks the floor on $|S|\le\min(p,s_0+j_0)$ and on $|S|\le\bar k_n=\min\{p,s_0+\max(j_0,\bar m_n)\}$, $\bar m_n=\lceil[s_0(A\log n+\log2)+\log2+\tfrac{s_0+2}2\log n]/\log\tfrac32\rceil$ (L1_POST.md:20-25). For $n\ge3$: $\bar k_n<(2.4664As_0+3.6996s_0+4.9327)\log n\le5(A+1)(s_0+1)\log n$ (R1) [R1-E6], and $s_0+j_0\le(2A+2)s_0+2$ is smaller. Checked numerically (LOG). |
| B2.2 | LSF + Gaussian rows + fixed coefficients ⇒ events $\mathcal A_n$, $P(\mathcal A_n)\to1$, carrying (E), (F_λ), (F_w), BM-∞ with common constants | EXISTS-CHECKED | `W2-APP:POST@1.0.7` part (a), "PROVED-CHECKED" (accepted at W2-APP's CP3, main f526e45b; SOP:TH09 discharged, main 6cd699dd) [REG-f526, REG-6cd6]. Raw-scale coefficients are covered (L1_POST.md:12-15, event $\mathcal H_n$). Theorems 6 and 10 depend on it, as did the previous Gaussian proof of Theorem 2 (the presented Theorem 2 uses B2.2′ instead); Theorem 4 does not (its master uses its own Gaussian-design transfer [S1-F12]). |
| B2.3 | events ⇒ conclusions under the joint law | inside the master | Theorem 1 item 6 (diagonal transfer), via `W3-D3:Thm2SG`. **B2.2′** (sub-Gaussian rows: (A3) and the sub-Gaussian condition ⇒ the events $\mathcal A_n$ of B2.2; replaces B2.2 for the presented statement; EXISTS-CHECKED): `W3-D3:B3w@1.0.0` (built on `W3-DIST:B1`, `B2core`, `B2` part (a), `W3-READER:R1`), main 0eb1b6ef [REG-0eb1]; B2.2 stays for the Gaussian case. Bridges B2.1′, B2.1″ of Theorem 2X: §11. |

**Effort:** B2.1 half a page.
### Honest limits
None for the statement. Status [REG-6cd6]: T03♯ is PROVED-CHECKED (`SOP:TH09@1.0.2`, main 6cd699dd) and `W2-APP:POST` is
"PROVED-CHECKED"; the posterior-summary lemma SL0 is "PROVED-CHECKED" since main 33e1f0f5 [REG-33e1]. Abstract wording: Form A of
row 1.1 applies here too. The statement is Theorem 2 with sub-Gaussian rows (v0.5, H5 card 17); its status is that of `W3-D3:Thm2SG` (above).

#### Update log (thm2)
- v0.1 2026-11-15: first version (CP1).
- v0.2 2026-11-15: S1 fixes none needed (S1: FAITHFUL); [S1-F12] dependency note.
- v0.3 2026-11-16: [REG-f526] `W2-APP:POST@1.0.5` status refreshed (accepted, conditional on SOP:TH09, C-PACK:SL0); B2.2
  mark and honest limits updated (EQUAL).
- v0.4 2026-11-16: [REG-33e1] SL0 cleared: `W2-APP:POST@1.0.6` conditional on SOP:TH09 only (EQUAL).
- FRZ-RQ 2026-11-16: [REG-6cd6] `W2-APP:POST@1.0.7` "PROVED-CHECKED"; T03♯ discharged; Form A. Statuses only (EQUAL).
- R1 2026-11-16: [R1-E6] B2.1 constant harmonised with R1 (EQUAL).
- FRZ-B 2026-11-16: requote at main 2676e71f [REG-2676] (relabel D97): `W3-POST:Thm-1@1.0.1`; EQUAL (statuses only).
- v0.5 2026-11-17: [H5-17] H5 card 17 (consultant AGREED; D115, D120): Theorem 2 is presented with sub-Gaussian rows on sparse directions (text of W3-D3 READER_DELTA; Gaussian rows = $L=1$); the expectation-form statement Theorem 2X coexists (§11). Tag: Theorem 2 **STRONGER** than the Gaussian statement; Theorem 2X **MIXED / incomparable**. Statuses verbatim from main 0eb1b6ef, 2e0decc8.
<!-- ROW thm2 END -->

---

## 3. Theorem 3 — The rate cannot be improved
<!-- ROW thm3 BEGIN -->
**Card row** 1.3 · **Section version** 0.4 (2026-11-16) · **Pending delta** —


### Reader statement
**Theorem 3.** (a) *(Every design.)* For every $n\ge3$, every standardised design with $p\ge2$, every response and every
model $S$ with $|S|\le\min(K-1,p/2)$,
$$
\pi(S\mid y)\ \le\ \Big(1+\frac{|S|+1}{3\sqrt n}\Big)^{-1}.
$$
(b) *(Orthogonal or Gaussian null columns.)* Assume (S1), $s_0$ fixed, $\|X\theta^*\|^2\le nM$ and
$\|\theta^*\|^2\le nM'$ with fixed $M,M'$, and either
- **(N-orth)** the columns outside $S_0$ are mutually orthogonal and orthogonal to the columns in $S_0$; or
- **(N-gauss)** the raw columns outside $S_0$ have i.i.d. $N(0,1)$ entries, independent of $X^{\mathrm r}_{S_0}$ and
  $\varepsilon$, and $p\le n^A$.

Then, for every $p$ with $s_0<p$ (bounded or growing),
$$
\mathbb E\big[1-\pi(S_0\mid y)\big]\ \ge\ (1-o(1))\,(s_0+1)\,\frac{2(p-s_0)}{2p-1-s_0}\,\sqrt{\frac{\log\!\big(p\sqrt n/(s_0+1)\big)}{\pi n}},
$$
and, if moreover $p\to\infty$,
$$
1-\pi(S_0\mid y)\ \ge\ (1-o_P(1))\,(s_0+1)\sqrt{\frac{\log p}{\pi n}}.
$$

*In words (headline).* The rate of Theorem 1 cannot be improved under its assumptions: on orthogonal or Gaussian null
columns, $E[1-\pi(S_0\mid y)]\ge c\cdot(s_0+1)\cdot\sqrt{\log n/n}$, for every $p$. Here $c>0$ depends only on $s_0$, and does
not depend on $s_0$ when $s_0\le p/2$. The $\sqrt{\log n}$ bounds hold on these null-column designs only; on every design
only the order $n^{-1/2}$ of part (a) is proved.

*Remarks.*
(i) *What is attained where.* By (a), for true models with $s_0\le\min(K-1,p/2)$, no design gives a rate faster than
$n^{-1/2}$; $\pi(S_0\mid y)\to1$ requires $s_0=o(\sqrt n)$; the rate $\sqrt{\log n/n}$ requires $s_0=O(\sqrt{\log n})$.
(Without the size restriction (a) is false: e.g. $S=[p]$ with $p=2$.) By (b), on orthogonal or Gaussian null columns,
the factor $\sqrt{\log n}$ is present **in expectation for every $p$**, bounded $p$ included (with $p=n^a$ the constant is
$\sqrt{(a+\frac12)/\pi}$), and **in probability whenever $\log p\asymp\log n$**. The rate $\sqrt{\log n/n}$ of Theorem 1 is
exact in the following named cases:
- **in expectation**, on fully orthogonal designs (all columns mutually orthogonal, any $p$ with $s_0<p\le n-1$, bounded
  or growing) with fixed nonzero coefficients: these designs satisfy the assumptions of Theorem 1 and of the expectation
  display in (b), so $E[1-\pi(S_0\mid y)]$ is of exact order $\sqrt{\log n/n}$, with constants depending only on $s_0$, the
  coefficients and the noise variance (conditional on Theorem 1);
- **in probability**, on fully orthogonal designs with $p=\min(n-1,\lfloor n^a\rfloor)$ and on raw designs with i.i.d.
  $N(0,1)$ entries and $p=\lfloor n^a\rfloor$, both with fixed nonzero coefficients (conditional on Theorems 1 and 2).

The extra $\sqrt{\log n}$ in expectation at bounded $p$ comes from rare large gains of a single extra variable, not from
the number of competitors.

(ii) *Growing $s_0$.* Keep the energy and coefficient bounds of (b), let all columns outside $S_0$ be null columns of
type (N-orth), or of type (N-gauss) with the columns in $S_0$ and the coefficients fixed (nonrandom), and let $s_0\le p/2$
grow with $n$. Then a posterior mean error $E[1-\pi(S_0\mid y)]$ of order $\sqrt{\log n/n}$ forces $s_0$ to stay bounded,
for every $p$.

(iii) *Critical scale (orthogonal null columns only).* Keep the energy and coefficient bounds of (b) and (N-orth), let
$p\to\infty$ and let $s_0$ grow with $s_0/p\to0$ and $(s_0+1)\sqrt{\log p/(\pi n)}\to\lambda\in(0,\infty)$. Then
$\pi(S_0\mid y)\le e^{-\lambda}+o_P(1)$.

(iv) *What is open.* On a general design only the order $n^{-1/2}$ of part (a) is proved as a lower bound; a matching
lower bound $E[1-\pi(S_0\mid y)]\gtrsim\sqrt{\log n/n}$ under a floor on $S_0\cup\{j\}$ is open (post-freeze rider
POST2-R1). When $\log p=o(\log n)$, nothing is claimed **in probability**: the in-probability display gives only order
$\sqrt{\log p/n}$, and whether the $\sqrt{\log n}$ is present in probability there is open. On raw Gaussian designs the
matching upper bound **in expectation** is open (Theorem 2 is an in-probability statement). Whether the constant of the
expectation display is attained is not proved.

### Why each assumption
(a) has none: it is a deterministic property of the prior and the Occam factor (each of the $p-s_0$ one-variable
supersets keeps posterior odds at least of order $n^{-1/2}/p$). (b): the witness conditions make the one-variable
supersets behave as independent $\chi^2_1$ competitors; for the expectation display a single such competitor already
suffices (its heavy upper tail gives the $\sqrt{\log n}$); for the in-probability display $p\to\infty$ competitors are
used (the sum of their truncated fit factors gives the $\sqrt{\log p}$); energy and coefficient bounds keep the variance
posterior on scale. These are witnesses, not claimed necessary.

### Master theorems
`W3-PSHARP:B@1.0.0`, `Theory_work/Wave3/W3-PSHARP/STATEMENT.md:90-114` (display at :94-96, consequence (B1) at :99), and
`W3-PSHARP:A@1.0.0`, same file :46-77 (Corollary A1 at :71-73; (N-gauss) is the example at :59-60 of (W-sph)). Status of
both, verbatim: **"PROVED-CHECKED; council R2, MANIFEST 4513e05a…, sol=9.2 PASS, opus=9.3 PASS; …"**.
Expectation display and remarks (ii)–(iii): `W3-PSHARP-R:AE@1.0.0` (`Theory_work/Wave3/W3-PSHARP-R/STATEMENT.md:61-92`;
Corollary A1-E at :74-84, Cor A2-E(ii) at :86-92) and `W3-PSHARP-R:A2C@1.0.0` (:94-100), statuses verbatim (registry,
main): **"PROVED-CHECKED; council R2, MANIFEST fdfd45629f8716ac00e9854310cc3265ead8ce60679290b8eb09089eddf3999e, sol=9.5
PASS, opus=9.2 PASS"** (each). Named exactness case in expectation: bridge B3.8.

### Bridges
| # | Bridge | Mark | Detail |
|---|---|---|---|
| B3.1 | (a) from Corollary B: $c(p,s_0)\ge(s_0+1)/3$ for $s_0\le p/2$ | EXISTS-CHECKED | Inside `W3-PSHARP:B` (:95, :99). Reader version renames $S_0$ to any $S$ (Corollary B holds for every subset, :92-93). |
| B3.2 | (N-gauss) ⇒ (W-sph) | EXISTS-CHECKED (example in the claim text) + NEW one line | (W-sph) asks $(\log N_n)^2=o(n)$ and $(r_0+1)\log N_n=o(n)$; with $N_n\le p\le n^A$ and $s_0$ fixed both hold (R1). |
| B3.3 | (N-orth), $s_0$ fixed ⇒ (W-orth-E) with $\mathcal N=[p]\setminus S_0$ | NEW one line (council-checked inside W3-PSHARP-R R2 as READER_DELTA v0.3) | (N-orth) gives $N=p-s_0\le n-1-r_0$, so $p\le2n$ and $(\log p)^2=o(n)$ (W3-PSHARP-R `STATEMENT.md` §2). |
| B3.4 | (N-gauss), (S2) $p\le n^A$, $s_0$ fixed ⇒ (W-sph-E) | NEW one line (as B3.3) | $(\log p)^2\le A^2(\log n)^2=o(n)$; $(r_0+1)\log(pn)\le(s_0+1)(A+1)\log n=o(n)$; any number of null columns $\ge1$. |
| B3.5 | expectation display ⇐ Cor A1-E (W3-PSHARP-R `STATEMENT.md:74-84`) | EXISTS-CHECKED | `W3-PSHARP-R:AE@1.0.0` "PROVED-CHECKED; council R2, …". Under (N-gauss) via the random-$(X_{S_0},\theta^*)$ clause (:70-72) with $P(\mathcal A_n)\to1$. Headline constant: $(s_0+1)\cdot2(p-s_0)/(2p-1-s_0)\ge2$ for $s_0\ge1$, $\ge(s_0+1)/2$ for $s_0\le p/2$, and $\log(p\sqrt n/(s_0+1))\ge\frac12\log n$ (B3.8 step 3). |
| B3.6 | in-probability display needs $p\to\infty$ | EXISTS-CHECKED | `W3-PSHARP:A@1.0.0`, Cor A1 (`W3-PSHARP/STATEMENT.md:71-73`), unchanged. |
| B3.7 | remark (ii) ⇐ Cor A2-E(ii) (:86-92); remark (iii) ⇐ A2C (:94-100) | EXISTS-CHECKED | `W3-PSHARP-R:AE`, `W3-PSHARP-R:A2C` "PROVED-CHECKED; council R2, …". |
| B3.8 | fully orthogonal designs, fixed nonzero coefficients, $s_0<p\le n-1$ ⇒ Theorem 1 (A1)–(A6) and the hypotheses of the expectation display of (b); hence exact order $\sqrt{\log n/n}$ in expectation, every such $p$ | NEW, checked: `lemmas/B3_8_orth_witness.md` (verbatim copy of theory/W3-PSHARP-R @34d56f5b `reviews/post_cp3/BRIDGE_orth_thm1.md`) [R1-E11] (sha256 d54a2a7a…); Sol line check L06 (CORRECT-WITH-FIXES, C 0, one S applied) and Sol confirm L07 (YES, 0 findings), theory/W3-PSHARP-R @ 8e22c756 | (A1)–(A6) with $A=1$, $\bar\theta=\max|\theta^*_j|$, $\varphi_0=1$, $g_0=1$, second form of (A6); the upper half carries Theorem 1's master status (row 1.1). |

### Honest limits
The $\sqrt{\log n}$ lower bounds hold on the two witness designs only; on every design only order $n^{-1/2}$ is proved
(part (a)). Exactness in expectation is shown on fully orthogonal designs only. Whether the constant of the expectation
display is attained is not proved. Status: the expectation display and remarks (ii)–(iii) rest on `W3-PSHARP-R:AE`,
`W3-PSHARP-R:A2C`, "PROVED-CHECKED; council R2, …" (registry, main).

#### Update log (thm3)
- v0.1 2026-11-15: first version (CP1).
- v0.2 2026-11-15: S1 fixes [S1-F5] domain on remarks; [S1-F6] named witnesses (EQUAL).
- v0.3 2026-11-16: [H5-6, S3-N4] scope sentence: on a general design only order $n^{-1/2}$; the open item is the
  expectation lower bound under a floor on $S_0\cup\{j\}$ (EQUAL: a non-claim, S3); header points to the staged,
  not-in-force W3-PSHARP-R delta.
- v0.4 2026-11-16: [W3-PSHARP-R CP3; H5 card 8; HQ signal] swap to W3-PSHARP-R READER_DELTA v0.4
  (`/home/fb31/BVS-wt/W3-PSHARP-R/Theory_work/Wave3/W3-PSHARP-R/reviews/post_cp3/READER_DELTA_v0.4.md`, theory/W3-PSHARP-R
  @ 8e22c756): expectation display for every $p$ ("$p\to\infty$" only for the in-probability display); headline sentence
  (HQ wording); remarks (i)–(iv) with named exactness cases; mechanism sentence corrected (sum of truncated fit factors);
  bridges B3.3–B3.8 (B3.8 checked by Sol L06 + L07 confirm YES, 0 findings); masters' statuses verbatim
  (AE, A2C PROVED-CHECKED, council R2) (STRONGER: new expectation display for every $p$; EQUAL elsewhere).
- S4 tag record 2026-11-16 [S4-S3]: v0.4 is EQUAL to its delta (W3-PSHARP-R v0.4). Against the S3 text: STRONGER for the
  every-$p$ expectation display, the fully orthogonal expectation exactness, the growing-$s_0$ expectation obstruction and the
  critical-scale $e^{-\lambda}$ bound; EQUAL for the original probability clauses and size-domain consequences.
- R1 2026-11-16: [R1-E11] B3.8 check record copied into `lemmas/B3_8_orth_witness.md` (EQUAL).
<!-- ROW thm3 END -->

---

## 4. Theorem 4 — Omitted variables (misspecification)
<!-- ROW thm4 BEGIN -->
**Card row** 1.4 · **Section version** 0.5 (2026-11-16) · **Pending delta** —


### Reader statement
**Theorem 4** (candidate-only fitting with omitted Gaussian predictors; $\Sigma$, $\beta$, $\sigma^2$ may vary with $n$, subject only to (A1)–(A3)) [P4]. The method is run on the candidate predictors
$x_{\mathcal C}$ and the response $y^{\mathrm r}$ only ($p$ = number of candidates). Assume:
- **(A0) Model.** The candidate rows $x_{\mathcal C,1},\dots,x_{\mathcal C,n}$ are i.i.d. $N_p(m,\Sigma)$, and, given the
  candidate design, the responses are independent with
  $y^{\mathrm r}_i\mid x_{\mathcal C}\sim N\big(\alpha'+x_{\mathcal C,i}^\top\beta^{\mathcal C},\ \sigma^2_{\mathcal C}\big)$, $\sigma^2_{\mathcal C}>0$.
  Write $S_0^{\mathcal C}:=\operatorname{supp}\beta^{\mathcal C}$ and $s:=|S_0^{\mathcal C}|$.
- **(A1) Dimension and sparsity.** $2\le p\le n^A$; $s\ge1$ fixed.
- **(A2) Floor.** With $R$ the correlation matrix of a candidate row, $\lambda_{\min}(R_{TT})\ge c$ for every
  $T\subseteq\mathcal C$ with $|T|\le 3(A+1)(s+1)\log n$, for a fixed $c>0$.
- **(A3) Signal relative to the residual variance.**
  $\beta^{\mathcal C\top}\Sigma\beta^{\mathcal C}\le M_0\,\sigma^2_{\mathcal C}$ and
  $n\min_{j\in S_0^{\mathcal C}}\Sigma_{jj}(\beta^{\mathcal C}_j)^2/(\sigma^2_{\mathcal C}\log n)\to\infty$.

$m$, $\Sigma$, $\beta^{\mathcal C}$ and $\sigma^2_{\mathcal C}$ may depend on $n$; no condition beyond (A1)–(A3) is placed on how they vary. Then
$$
E\big[1-\pi(S_0^{\mathcal C}\mid y)\big]=O\Big(\sqrt{\tfrac{\log n}{n}}\Big),\qquad
P\big(\mathrm{HPM}\neq S_0^{\mathcal C}\big)=O\Big(\sqrt{\tfrac{\log n}{n}}\Big).
$$
*Example (omitted predictors: the full model is misspecified for the candidate-only fit) [P4].* If the rows $(x_{\mathcal C,i},x_{\mathcal M,i})$ are i.i.d. Gaussian with
$\Sigma_{\mathcal C\mathcal C}$ invertible and
$y^{\mathrm r}_i=\alpha+x_{\mathcal C,i}^\top\beta_{\mathcal C}+x_{\mathcal M,i}^\top\beta_{\mathcal M}+\varepsilon_i$ with
$\varepsilon\sim N_n(0,\sigma^2I)$ independent of the rows, then (A0) holds, provided the $\sigma^2_{\mathcal C}$ below is positive (for instance $\sigma^2>0$), with
$\beta^{\mathcal C}=\beta_{\mathcal C}+\Sigma_{\mathcal C\mathcal C}^{-1}\Sigma_{\mathcal C\mathcal M}\beta_{\mathcal M}$ and
$\sigma^2_{\mathcal C}=\sigma^2+\beta_{\mathcal M}^\top(\Sigma_{\mathcal M\mathcal M}-\Sigma_{\mathcal M\mathcal C}\Sigma_{\mathcal C\mathcal C}^{-1}\Sigma_{\mathcal C\mathcal M})\beta_{\mathcal M}$.
(If $\Sigma_{\mathcal C\mathcal C}$ is singular, the same holds with its Moore–Penrose inverse in place of the inverse.)
The same holds when the omitted predictors are a linear function of the candidates plus Gaussian noise whose rows are
i.i.d. and independent of the candidates.
*Remark.* The law in (A0) is the conditional law of $y$ given the candidates, hence the Kullback–Leibler projection of
the truth onto the candidate linear models: the posterior concentrates on the support of the best candidate
predictor. Under the same assumptions the posterior's fitted mean and variance also contract around this law, with its
mean centred over the sample (the fitted mean carries no intercept), in the in-sample average Hellinger and
Kullback–Leibler distances, at rate $M_n/\sqrt n$ in Hellinger and $M_n/n$ in Kullback–Leibler (any $M_n\to\infty$).
For a fixed design, under the same Gaussian model for the responses and (A1), the contraction needs only that the posterior mass of $S_0^{\mathcal C}$ tends to one in probability
(with the energy bound and a floor on $S_0^{\mathcal C}$); it holds uniformly over any class of fixed-design configurations with
common constants and bounded support size on which this convergence is uniform. A fixed-design version of the theorem, uniform
over the residual variance, also holds (remarks in the paper; same status).
*Relation to Theorem 2 [P4].* Theorem 2 does not give Theorem 4: Theorem 2 fixes $\sigma^2$ and has no omitted predictors.
Whether Theorem 4's hypotheses cover Theorem 2's setting without omitted predictors is open and being checked; until then the
two rows rest on different masters with their own conditions.

### Why each assumption
- (A0) is a convenient sufficient form. The proof uses only a weaker condition: given the candidates, the coordinates of
  the residual vector $y^{\mathrm r}-\alpha'1-x_{\mathcal C}\beta^{\mathcal C}$ in an orthonormal basis of the vectors
  orthogonal to the constant vector are i.i.d. $N(0,\sigma^2_{\mathcal C})$ — centred, with the variance of (A0); nothing
  is required of the residual's sample mean. When the noise is Gaussian with variance $\sigma^2$ and independent of all
  predictors, this holds if and only if the omitted contribution, after subtracting its linear candidate component, has
  (given the candidates) such coordinates i.i.d. $N(0,\sigma^2_{\mathcal C}-\sigma^2)$, the variance possibly zero. (A0) covers omitted Gaussian predictors and omitted predictors that are
  linear in the candidates plus Gaussian noise. The Gaussian law of the candidate rows is an assumption on how the data
  are generated (not a choice of design); it is used only to transfer the population floor (A2) and (A3) to the sample.
- (A1) as Theorem 1.
- (A2) The method standardises each column, so only correlations matter; the floor is on the candidates only.
- (A3) Everything is measured relative to $\sigma^2_{\mathcal C}$ because the method is invariant to shifts and rescaling of
  $y$. The energy bound cannot simply be dropped (numerical evidence); the beta-min order is that of Theorem 1
  (a liminf condition at a fixed constant suffices; remark).

### Master theorem
**Headline masters [H5-3]:** the fixed-design theorems `W3-MISR:MIS(i)@1.0.2` (:110-123; uniform over the residual
variance), `W3-MISR:MIS(i')@1.0.2` (:127-140) and `W3-MISR:MIS(ii)@1.0.2` (:144-160; random candidate designs,
conditional form) carry the headline flag; statuses verbatim (versions and statuses as at main 34c8fb4d): MIS(i), MIS(i′) and MIS(ii)
**"PROVED-CHECKED, conditional on W2-APP:POST; council R2, MANIFEST 217d6708…,
sol=9.2 PASS, opus=8.9 PASS; …"** (each) [REG-34c8]. The reader statement above is their **Gaussian-row reader version**: `W3-MISR-R:CorGb-plus` (with `W3-MISR-R:CorG-min`
(E1), (E2) for the Example) and, for the remark, `W3-MISR-R:CorH-plus`, `W3-MISR-R:CorH-U` — statuses verbatim from the
registry (versions and statuses as at main 34c8fb4d) [REG-34c8]: `W3-MISR-R:CorGb-plus@1.0.3` **"PROVED-CHECKED, conditional on W2-APP:POST,
C-MIS:GDb, C-MIS:Prop-P; council R3, MANIFEST 052ea6dffa0495584b051435b1e82d6b7c598d965e3b13ddc067545728728069, sol=10.0 PASS, opus=9.6 PASS"**;
`W3-MISR-R:CorG-min@1.0.3` **"PROVED-CHECKED; council R3, MANIFEST 052ea6dffa0495584b051435b1e82d6b7c598d965e3b13ddc067545728728069, sol=10.0 PASS, opus=9.6 PASS"**;
`W3-MISR-R:CorH-plus@1.0.3` **"PROVED-CHECKED, conditional on W2-APP:POST; council R3, MANIFEST 052ea6dffa0495584b051435b1e82d6b7c598d965e3b13ddc067545728728069, sol=10.0 PASS, opus=9.6 PASS"**;
`W3-MISR-R:CorH-U@1.0.3` **"PROVED-CHECKED, conditional on W2-APP:POST,
C-MIS:Prop-P; clause (G) also conditional on C-MIS:GDb; council R3, MANIFEST 052ea6dffa0495584b051435b1e82d6b7c598d965e3b13ddc067545728728069, sol=10.0 PASS, opus=9.6 PASS"**.
These replace `W3-MISR:Cor-G(b)` below as the row's reader-version master. `W3-MISR:Cor-G(b)` stays ACTIVE and coexists
with CorGb-plus (CorGb-plus implies it and reuses its proof steps); `W3-MISR:Cor-G(a)` is SUPERSEDED-VALID by CorG-min.
The remark's Kullback–Leibler sentence rests on CorH-plus (centred reference), not on `W3-MISR:Cor-H` (whose KL reading
is restricted to a deterministic intercept at 2.1.0).
Earlier reader-version master, kept for the record: `W3-MISR:Cor-G(b)@1.0.2`,
`Theory_work/Wave3/W3-MISR/STATEMENT.md:171-174`, status verbatim (main 34c8fb4d):
**"PROVED-CHECKED, conditional on W2-APP:POST, C-MIS:Prop-P, C-MIS:GDb; input
versions …; council R2, MANIFEST 217d6708…, sol=9.2 PASS, opus=8.9 PASS; …"**.
Inputs, verbatim (main 6cd699dd) [REG-6cd6]: `W3-POST2:C/E/A1/A0@1.0.7` as quoted in §1 (main 33bfcb9c) (C, E, A1 "PROVED-CHECKED,
conditional on …"; A0 "PROVED-CHECKED"); `C-MIS:Prop-P@1.0.0`: **"R02
VERIFIED; R04 wording fixes checked in R05; council PASS"**; `C-MIS:GD(b)@1.0.0`: **"R02 VERIFIED-WITH-AMENDMENTS
(applied); council PASS"**; `SOP:TH09` as in §1; `SOP:TH128@1.0.2`: **"PROVED-CHECKED (the conjunction of W3-T03ACC:T03S.1–T03S.5 = record clauses
1–5, clause map CHECKPOINT_4.md §2; council R1, MANIFEST 9714aea4…, astra=9.5 PASS, opus=9.4 PASS; LC-A, LC-B, LC-C
VERIFIED)"** [S1-F9, REG-6cd6]; neither is a condition of the masters any more (discharged, main 6cd699dd).
Fixed-design form: `W3-MISR:MIS(i)@1.0.2` (:110-123), **"PROVED-CHECKED, conditional on W2-APP:POST; …"** (main 34c8fb4d).

### Bridges
| # | bridge | mark | detail |
|---|---|---|---|
| B4.0 | (A0) ⇒ CorGb-plus setting | NEW (one line) | take no explicit omitted columns, ε := y^r − α′1 − X_𝒞β^𝒞: given X_𝒞 it is N_n(0, σ²_𝒞I), hence independent of X_𝒞 ((N) with q = 0; (OV) with γ = 0, τ² = 0). The Example is `CorG-min` (E1) (and (E2) for the linear-plus-noise sentence) |
| B4.1 | (A2) size 3(A+1)(s+1)log n ⇒ CorGb-plus's \|T\| ≤ s + max(j₀, m♯_n), for all large n | NEW arithmetic (as current B4.1) | unchanged arithmetic; the floor is now on R; sufficient for the O(·) conclusions |
| B4.2 | (A3) = CorGb-plus's signal conditions (→ ∞ branch of its liminf condition) | identity | `STATEMENT.md` §3 |
| B4.3 | POST2 C, E, A1, A0 (and D for the remark) | EXISTS-CHECKED, conditional (A0 unconditional) | recorded at main f526e45b; `SOP:TH09`/`TH128` discharged (main 6cd699dd); C no longer conditional on `W3-POST:Prop-LB` (PROVED-CHECKED, main 33bfcb9c; §1; [L1a′] no longer listed, main 2676e71f) [REG-f526, REG-6cd6, REG-33bf] |
| B4.4 | Remark ⇒ CorH-U (RD) with 𝒦^♭_n := 𝒦^λ_n(s, A, 2M₀+1, (c_R/8)^{1/2}, C_OS, c) ((UP) by MIS(i) + Markov) and the events 𝒜_n of CorGb-plus's proof (P(𝒜_n) → 1); contraction sentence for a fixed design ⇒ CorH-plus (a′), (KL), with the premise δ_n → 0 in probability; uniform sentence ⇒ CorH-U (U-a), with its premise (UP); "fixed-design version of the theorem, uniform over the residual variance" ⇒ W3-MISR:MIS(i)@1.0.2 (BASE `STATEMENT.md:110-114`, constants free of v) | NEW (composition; the random-design part is `CorH-U` clause (G), STATEMENT §5) | the Hellinger rate M_n/√n and KL rate M_n/n are the sets H^a, K^a; the reference is centred (STATEMENT §1: μ(κ) = Cxβ) [R1] |

### Honest limits
Nothing is claimed when, given the candidates, $y$ is not Gaussian with a mean linear in the candidates and a constant
variance (beyond the contrast form described under (A0) in §3). Status: the masters' statuses, verbatim in §5, with their
conditions.

#### Update log (thm4)
- v0.1 2026-11-15: first version (CP1).
- v0.2 2026-11-15: S1 fixes [S1-F9] TH128 status; [S1-F12] no W2-APP:POST dependency (EQUAL).
- v0.3 2026-11-16: [H5-3] headline masters named: MIS(i), MIS(i′), MIS(ii); reader statement = their Gaussian-row
  reader version Cor-G(b) (EQUAL); card row 3.4 → 1.4.
- v0.4 2026-11-16: [REG-f526] POST2 input statuses refreshed (EQUAL).
- v0.5 2026-11-16: [W3-MISR-R CP3, accepted main 2b54cb3c; H5 card 10; swap signal task Q] reader statement → W3-MISR-R READER_DELTA v0.4 (@93e50640): model (A0)
  (candidate rows Gaussian; Gaussian linear conditional law given the candidates), floor on the correlation matrix, no
  variance bound; omitted Gaussian predictors as the Example; Hellinger/KL remark; non-implication note on Theorem 2;
  honest limits; masters CorGb-plus, CorG-min, CorH-plus, CorH-U (STRONGER: weaker hypotheses, same conclusion).
- S4 tag record 2026-11-16 [S4-S3]: v0.5 is EQUAL to its delta (W3-MISR-R v0.4). Against the S3 text: STRONGER for the main
  theorem (weaker model assumption (A0) and floor (A2); (A3) unchanged; the same two displayed conclusions) [S5-N1]; the
  Hellinger/KL remark and the fixed-design selection-only and uniform forms are new (STRONGER) statements; in the
  Example, the jointly Gaussian case with invertible $\Sigma_{\mathcal C\mathcal C}$ was already present, and the
  pseudoinverse and linear-plus-noise cases are the new (STRONGER) scope.
- FRZ-RQ 2026-11-16: [REG-6cd6] MIS(i)/(i′)/(ii), Cor-G(b) @1.0.1 and MISR-R CorGb-plus/CorG-min/CorH-plus/CorH-U @1.0.1 with SOP:TH09/TH128 dropped; POST2 @1.0.5; `SOP:TH128@1.0.2` PROVED-CHECKED. Statuses only (EQUAL).
- FRZ-B 2026-11-16: requote at main 2676e71f [REG-2676] (relabel D97): POST2 inputs @1.0.6 and `W3-POST:Thm-1` conditions dropped; EQUAL (statuses only).
<!-- ROW thm4 END -->

---

## 5. Theorem 5 — The start law already concentrates
<!-- ROW thm5 BEGIN -->
**Card row** 3.3 · **Section version** 0.3 (2026-11-16)


### Reader statement
**Theorem 5.** Let the rows of $X^{\mathrm r}$ be i.i.d. $N_p(m_n,\Sigma_n)$, $\Sigma_n$ a correlation matrix, and let
$y^{\mathrm r}=\alpha\mathbf 1+X\theta^*+\varepsilon$ with a deterministic $\theta^*$ (signal fixed on the standardised
scale). Assume
- **(A1) Model.** (S1), (S2), and $p>s_0$.
- **(A2) Sparsity and fixed signals.** $s_0\ge1$ fixed; $\theta_{\mathrm{lo}}\le|\theta^*_j|\le\theta_{\mathrm{hi}}$ on
  $S_0$.
- **(A3) Small-set floor.** $\lambda_{\min}(\Sigma_{n,S})\ge c$ for every $|S|\le16+s_0$.
- **(A4) Visibility.** For every $j\in S_0$ and every $U\not\ni j$ with $|U|\le15$:
  $|\operatorname{Cov}(W_j,\,W^\top\theta^*\mid W_U)|\ge a$, for a fixed $a>0$.
- **(A5) No leakage.** For every $l\notin S_0$ there is a set $H_l\supseteq\{l\}\cup S_0$ with
  **$|H_l|\le e^{\kappa\sqrt{\log n}}$** such that, for every $U\not\ni l$ with $|U|\le15$ and $U_0:=U\cap H_l$:
  $|\operatorname{Cov}(W_l,W_j\mid W_{U_0})|\le Cn^{-1/2}$ for $j\in S_0\setminus U_0$, and
  $|\operatorname{Cov}(W_l,W_v\mid W_{U_0})|,|\operatorname{Cov}(W_j,W_v\mid W_{U_0})|\le r_n$ for $v\in U\setminus H_l$,
  $j\in S_0\setminus U_0$, where $r_n(n\log n)^{1/4}\to0$.

Then for every $c<\tfrac12$,
$$
P\big(\pi_0(S_0)\ge1-n^{-c}\big)\to1 .
$$
**If moreover (A6) every null column is uncorrelated with every true column, $\operatorname{Cov}(W_l,W_j)=0$ for
$l\notin S_0$, $j\in S_0$, then**
$$
\mathbf{1-\pi_0(S_0)=O_P\big(\sqrt{\log n/n}\big)} .
$$
The exponent $\tfrac12$ cannot be improved: $1-\pi_0(S_0)\ge\tfrac13(n+1)^{-1/2}$ for every valid data set with
$n\ge4$ and $s_0<K$ (hence for all large $n$) [S1-F4]; **so the rate under (A6) is optimal up to the factor
$\sqrt{\log n}$.**

*With leakage (remark or second display).* If (A5) holds with "$l\notin S_0$" replaced by "$l\notin Q$" for a deterministic $Q\supseteq S_0$ ($H_l$ and the truths $j$
unchanged), $|Q|\le K$ (columns outside $Q$ do not leak) [R1-E1], then
$P\big(\pi_0(\mathcal L(Q))\ge1-(|Q|+1)n^{-1/2}e^{C\sqrt{\log n}}\big)\to1$; for $|Q|\le n^{1/2-\epsilon}$ this is
$\ge1-n^{-c}$ for every $c<\epsilon$.

### Why each assumption
- (A3) Block regressions of at most 16 columns are well posed. Necessity open.
- (A4) Each truth, alone, improves the fit of every small model it is missing from: then the start law, which only sees
  within-block interactions, still ranks $S_0$ first. The level is sharp in the fixed-design analogue **(threshold
  $\log n+2\log p$ for every $p$)**; masked truths violate it and are treated separately.
- (A5) Nulls must not imitate truths within the start law's block view; the partial-covariance level $n^{-1/2}$ is a
  proof threshold (numerics show no cliff there); localisation is needed because the blocks are data-dependent.
  **The size bound on $H_l$ only counts reference sets in a union bound; it is not known to be needed.**
- **(A6) The start odds are, to first order, a sum over null columns of block Bayes factors computed given subsets of
  the truth. With uncorrelated nulls the proof bounds the expectation of a truncated envelope of these factors by
  $O(\sqrt{\log n})$ (an upper bound), and averaging over the columns and Markov's inequality give the displayed rate;
  under (A5) alone a correlation of size $Cn^{-1/2}$ shifts the Gaussian score, and the same upper bound then carries a
  factor $e^{O(\sqrt{\log n})}$. It suffices that these correlations be at most $C/\sqrt{n\log n}$ given every proper
  subset of the truth (master statement). Not known to be necessary.**
- The exponent $\tfrac12$ is optimal (deterministic floor).

### Master theorem
**`W3-START2-R:START-R@1.0.0`, `Theory_work/Wave3/W3-START2-R/STATEMENT.md:226-240` (clauses (i), (iii); (L-R⁺⁺) at :70-81,
(L-gain-0) at :82-87; (FL-R16), (V-R) at `W3-START/STATEMENT.md:160-162`), status verbatim (`claims.tsv`, main b48fd0a1)
[REG-b48f]: "PROVED-CHECKED; council R2, MANIFEST 12bb52cd… (= R2 90886d06 re-frozen CITATION-ONLY as R2r), sol=9.0 PASS, opus=9.3 PASS". Bridge (B-R⁺⁺): `W3-START2-R:BR@1.0.0` (`W3-START2-R/STATEMENT.md:217-225`), "PROVED-CHECKED; council R2, MANIFEST 12bb52cd… (= R2 90886d06 re-frozen CITATION-ONLY as R2r), sol=9.0 PASS, opus=9.3 PASS".** The previous masters
`W3-START2:START-R@1.1.0` and `W3-START2:IF-START@1.1.0` are SUPERSEDED-VALID by `W3-START2-R:START-R` / `IF-START` (same
status). Floor:
`W3-START:FLOOR@1.0.0` (`W3-START/STATEMENT.md:241-243`), **"PROVED-CHECKED"**.

### Bridges
| # | Bridge | Mark | Detail |
|---|---|---|---|
| **B5.1′** | **(A3)–(A5) = (FL-R16), (V-R), (L-R⁺⁺) with $Q=S_0$, $\bar H_n=e^{\kappa\sqrt{\log n}}$ ($\kappa_H=\kappa$)** | identity | **word for word (`W3-START2-R/STATEMENT.md:70-81`).** |
| B5.2 | floor $\tfrac13(n+1)^{-1/2}$ | EXISTS-CHECKED | (T0) holds for valid data with $n\ge4$ and $|S|<K$; with $S=S_0$ this is all large $n$ since $p>s_0$ (statement restricted accordingly [S1-F4]). |
| **B5.3** | **(A6) ⇒ (L-gain-0) with $C_0=0$** | **checked with the master (council R1/R2 of W3-START2-R)** | **for $U\subseteq S_0$: $\operatorname{Cov}(W_l,W_j\mid W_U)=\Sigma_{lj}-\Sigma_{lU}\Sigma_{UU}^{-1}\Sigma_{Uj}=0$ (`W3-START2-R/STATEMENT.md:82-87`).** |

### Honest limits
The statement is in population terms but (A5) is long. Two presentation options for HQ: (i) state the theorem with
$Q=S_0$ only (as above) and move the leakage form to a remark; (ii) a shorter sufficient condition (e.g. exact conditional uncorrelatedness of nulls and truths) does **not**
immediately give the localisation clause, because that clause also constrains columns outside $H_l$; no such
simplification is proposed without a proof. Recommendation: option (i). **(A6) is an additional hypothesis for the
sharper rate only; it does not replace (A5).**
Also: this theorem is about an internal object of the method; it belongs in the paper's method section, not in the
abstract.

#### Update log (thm5)
- v0.1 2026-11-15: first version (CP1).
- v0.2 2026-11-15: S1 fixes [S1-F4] floor restricted to n≥4, s₀<K (WEAKER clause, now faithful).
- **v0.3 2026-11-16: rider START2 v1.5 (W3-START2-R, CP3 accepted; H5 card 14 AGREED, row 3.3 STRONGER): (A5) with
  $|H_l|\le e^{\kappa\sqrt{\log n}}$; new (A6) with the rate $O_P(\sqrt{\log n/n})$; "why" lines for (A4)–(A6); master
  W3-START2-R:START-R/BR.**
- v0.3 applied 2026-11-16 [manager signal; recorder task U, main b48fd0a1]: statuses requoted verbatim from `claims.tsv`
  at b48fd0a1 (STRONGER, H5 card 14 (A)).
- R1 2026-11-16: [R1-E1] leakage form: only "$l\notin S_0$" becomes "$l\notin Q$" ($H_l$, truths unchanged), as in the master (EQUAL; removes a literal-reading contradiction).
<!-- ROW thm5 END -->

---

## 6. Theorem 6 — The reported model equals the truth (random Gaussian design; main theorem)
<!-- ROW thm6 BEGIN -->
**Card row** 3.1 · **Section version** 1.0 (2026-11-17) · **Pending delta** — (RM2-R rider merged, v0.8; Corollaries 6L and FAMC: §11; v1.0 log entry: last line of #### Update log (thm6))


### Reader statement
**Theorem 6.** Let the rows of $X^{\mathrm r}$ be i.i.d. $N_p(m_n,\Sigma_n)$ with $\Sigma_n$ a positive definite
correlation matrix, and $y^{\mathrm r}=\alpha\mathbf 1+X\theta^*+\varepsilon$ with deterministic $\theta^*$. Fix
$b\in(0,\tfrac12)$ and $\rho>0$ with $15\rho+b<\tfrac12$. Assume
- **(A1) Model.** (S1), (S2) ($p\gg n$ allowed), (S3).
- **(A2) Sparsity and fixed signals.** $s_0\ge1$ fixed; $\theta_{\mathrm{lo}}\le|\theta^*_j|\le\theta_{\mathrm{hi}}$ on
  $S_0$.
- **(A3) Visibility.** $|\operatorname{Cov}(W_j,\,W^\top\theta^*\mid W_U)|\ge a>0$ for every $j\in S_0$ and every
  $U\not\ni j$ with $|U|\le15$.
- **(A4) Polynomial leakage set.** There is a deterministic $Q\supseteq S_0$ with $|Q|\le n^b$ and, for large $n$,
  $|Q|\le K$ and ($Q=[p]$ or $K\ge2|Q|+32s_0+1$), such that:
  (i) *(no leak outside $Q$)* there is a deterministic $\varpi_n$ with $\varpi_n\sqrt{n/\log n}\to0$ such that
  $|\operatorname{Cov}(W_l,W_j\mid W_U)|\le\varpi_n$ for all $l\notin Q$, $j\in S_0\setminus U$, $|U|\le15$;
  (ii) *(locality)* there is a deterministic $r_n\to0$, and every $l\notin Q$ has a deterministic
  $H_l\supseteq\{l\}\cup S_0$, $|H_l|\le n^{\rho}$, such that for all $l\notin Q$, all $U\not\ni l$ with $|U|\le15$
  and $U_0:=U\cap H_l$: $|\operatorname{Cov}(W_l,W_v\mid W_{U_0})|\le r_n$ and
  $|\operatorname{Cov}(W_j,W_v\mid W_{U_0})|\le r_n$ for all $v\in U\setminus H_l$, $j\in S_0\setminus U_0$ [S1-F3].
- **(A5) Population sparse eigenvalue floor.** $\lambda_{\min}(\Sigma_{n,S})\ge c>0$ for every $S$ with
  $|S|\le5(A+1)(s_0+1)\log n$ and for every $S=Q\cup\{l\}$, $l\in[p]$.
- **(A6) Local regressions within $Q$.** There are deterministic sequences $\nu_n=o(\log n)$ and $L_n$, and for every
  $l\in[p]$ a deterministic $N_l\subseteq Q\setminus\{l\}$ with $|N_l|\le\nu_n$ [S1-F3], such that
  $\|\bar\beta_{T,l}-\bar\beta_{T\cap N_l,l}\|_1\le L_n$ for every $T$ with $S_0\subseteq T\subseteq Q$, $l\notin T$,
  where $L_n\to0$ and $L_n^2\log(|Q|+1)=o(\log n)$ (bars: population regression coefficients, zero-padded).

Then, under the joint law of design and noise, there are data events $\mathcal G_n$ with $P(\mathcal G_n)\to1$ on
which **every** admissible run that produces output reports $\hat S=S_0$, whatever its seed and the outcome of its
internal calibration; in particular $P(\text{output and }\hat S\neq S_0)\to0$. If moreover the delivery conventions
(S4) hold [S1-F2, RM2R-1],
$$
P(\text{the run produces output})=1\ \ \text{for every admissible }n\ge3,\qquad P(\hat S=S_0)\to1 .
$$
The delivery statement lifts two integer limits of the code (IDEAL-W⁺); in the default configuration neither can be reached on any input R can represent ($n, p_{\mathrm{raw}} \le 2^{31}-1$) [T14-REP], so this matters only for the $n\to\infty$ form. The two limits are a base search cap of $10^6$ (`v3_run.R:96`) and a 32-bit integer bound $2^{31}-1$ on the search cap (`cpp/v3_core.cpp:474`). R stores matrix dimensions as 32-bit integers, so in the default configuration the base cap is $\lceil\log_2(n+p_{\mathrm{raw}}+1)\rceil\le32$ and the search cap is at most $32+\lfloor n/2\rfloor\le2^{30}+31$, and neither limit can fire [T14-REP]. Every such input lies in the bounded domain $\mathfrak D=\{\lceil\log_2(n+p_{\mathrm{raw}}+1)\rceil\le10^6,\ \lceil\log_2(n+p_{\mathrm{raw}}+1)\rceil+\lfloor n/2\rfloor\le2^{31}-1\}$, on which delivery holds under the remaining conventions (S4), without IDEAL-W⁺ [RM2R-5]; IDEAL-W⁺ is used only by the asymptotic form. Representable inputs still carry the other obligations of IDEAL-W (for example `2*p-1` in `int` for $p\ge2^{30}$); the statement is for the default configuration (`v3.ls0_ell` unset).
The guarantees describe the run as if uninterrupted; a run stopped by its time guard reports status `resource_limit` and returns no estimates; anything else it returns is flagged incomplete and is not covered (`v3_fit.R:84-85`; `v3_run.R:110-113, 142-147`) [B2]. [GUARD-W]

*Remarks.* (o) [RM2R-3] Under (S4), for every seed and calibration outcome,
$P(\hat S\neq S_0)\le P(S_0\text{ is not the unique maximiser of the score})+P(\text{the local search from the start mode
does not reach }S_0)$. *(Interpretation, not part of the theorem [D71]: the two terms are the posterior-mode error and the
search error.)* (i) $\mathcal G_n$ can be chosen ($\mathcal M_n\cap\mathrm{Sand}_n(Q)\cap\mathrm{NA}\cap\mathrm{TL}$) so that on it the local search from the start mode only deletes the spurious members of the start
mode, one per move, at most $n^b$ moves, and certifies $S_0$; its move cap never binds. (ii) The polylogarithmic case
$|Q|\le(\log n)^{\kappa}$ is a special case (the earlier version of the theorem). (iii) Examples (never hypotheses):
metric-local correlation, polynomial correlation decay of exponent $\alpha>2$ (`W3-RM2:Ex-PolyR@1.0.5` "PROVED-CHECKED; council R1, MANIFEST c8596ad0…, astra=9.5 PASS, opus=9.5 PASS"
(main 8b4d3101)),
one-factor blocks [R2-O6].
### Why each assumption
- (A2) Fixed signals give the posterior input (Theorem 2) and the truth-removal margin.
- (A3) No truth can be explained away by at most 15 others: every truth enters the start mode. Needed in this form for
  the start; masked designs violate it and are separate examples (the method still works there, by other theorems).
- (A4) Columns outside $Q$ never enter the start mode; columns inside $Q$ may, and the search removes them. $b<\tfrac12$
  is where the prior-plus-Occam penalty of one more variable ($\approx\log p+\tfrac12\log n$) stops dominating the best
  of $p$ noise gains ($\approx\log p$) at model size $\approx\sqrt n$; beyond it the route's key events are expected to
  fail (heuristic; whether the conclusion fails is open). Locality (ii) is needed because the method's blocks are
  data-dependent.
- (A5) Floors make block regressions and the lattice directions well defined; the floor on $Q\cup\{l\}$ is a floor on
  sets of polynomial size; necessity not asserted.
- (A6) Guarantees that no addition improves the score anywhere on the lattice of $Q$, so the search goes straight down
  to $S_0$. It is a sufficient form of a width condition that is *forced* by this route (if the width gap diverges the
  other way, no-addition fails w.p. $\to1$). Not known to be necessary for the conclusion.

### Master theorems
0. [RM2R-2] `W3-RM2-R:RM2-R-plus@1.0.1`, `Theory_work/Wave3/W3-RM2-R/STATEMENT.md:177-182` (same hypotheses as RM2-R; conclusion
   adds [MODE] and, under (D), delivery and $P(\hat S=S_0)\to1$ with the error split), status verbatim **"PROVED-CHECKED; council R3, MANIFEST 5d6d3c90… (= R3 b06a8588 re-frozen as R3r), sol=9.5 PASS, opus=9.4 PASS"** (main fe05ccec, D95) [REG-fe05]; DLV-0 takes the two C-DLV code-reading audits as hypotheses [RM2R-7]; `C-DLV:L2-S3@1.0.1` and `C-DLV:P1-Inventory@1.1.1` are now each **"CODE-CHECKED (second seat, code reading; holds at pin 4676af6 after amendments A-1–A-7); council R2, MANIFEST 12802ac7…, sol=9.3 PASS, opus=9.4 PASS"**.
   With `W3-RM2-R:RM0-plus@1.0.1` (`STATEMENT.md:118-143`, mode form of the core) and `W3-RM2-R:DLV-0@1.0.1` (`STATEMENT.md:144-163`,
   deterministic delivery at the pinned code), each with the same status verbatim. RM2-R-plus implies RM2-R
   (`W3-RM2-R:Cont-plus@1.0.1`, same status); the supersession is not applied (deferred post-freeze), so `W3-RM2:RM2-R` stays ACTIVE.
   **Conditions of the row (current master) [RM2R-7]:** none open: the posterior input `W2-APP:POST@1.0.7` is "PROVED-CHECKED" (main 6cd699dd [REG-6cd6]) and the two code-reading audits of the delivery path (`C-DLV:L2-S3`, `C-DLV:P1-Inventory`) were discharged at main fe05ccec (D95); before D95 the recording showed
   `W3-RM2-R:RM0-plus`, `RM2-R-plus` and `Cont-plus` with the latter two conditions.
1. `W3-RM2:RM2-R@1.0.3` (ACTIVE; supersession by RM2-R-plus deferred post-freeze), `Theory_work/Wave3/W3-RM2/STATEMENT.md:216-218`
   (assumptions :172-202), status verbatim
   **"PROVED-CHECKED, conditional on W2-APP:POST; input versions W2-APP:POST@1.0.1; council R1, MANIFEST 00bbeab8…,
   astra=9.5 PASS, opus=8.8 PASS; …"**. Its input `W2-APP:POST@1.0.7` is "PROVED-CHECKED" [REG-6cd6] (the polylogarithmic special case `W3-RM:RM-R@1.2.0`,
   SUPERSEDED-VALID, reads "PROVED-CHECKED, conditional on SOP:TH05.0"). Abstract wording: Form A of row 1.1.
2. `W3-RM:RM-0@1.0.0`, `Theory_work/Wave3/W3-RM/STATEMENT.md:160-176` (pathwise reduction; common good event
   :173-175), **"PROVED-CHECKED"**; `W3-RM:E4@1.0.0` (:219-230), **"PROVED-CHECKED"**.
3. `W2-UNI:F-UNI@2.1.0` (history; no longer the delivery master), `Theory_work/Wave2/W2-UNI/lemmas/L5_delivery.md:15-21` (delivery),
   **"PROVED-CHECKED"** (registry; correctness gate PASS; narrowed, task S2/S4). Inherited qualifications, verbatim
   (`L5_delivery.md:39-40`): "[OP] "PROVED (by this seat, unchecked)"; e4 rests on N3, "OPEN" (only "some maximiser" is
   used for consistency; delivery keeps e4 with TDP-IMPL as in Proposition F); S.3 is a code-reading audit." [R3]
   **Narrowing [FUNI-N]:** F-UNI is NARROWED to `@2.1.0` (recorder task S2; Dept FUNI_NARROW, Sol DIFF PASS @fc30c749):
   delivery for every $n$ under A:IDEAL-W⁺, and on the bounded domain $\mathfrak D$ under IDEAL-W. The v0.7 delivery
   sentences followed the narrowed statement; from v0.8 they follow item 0 (RM2R-5 sentence). F-UNI requoted from
   `claims.tsv` at the freeze (history only).
   **Abstract [H5-2]:** the delivery clause ("always produces output; $P(\hat S=S_0)\to1$") stays out of the abstract
   until the F-UNI gate is resolved; the abstract states the common-data-event clause.
   **Delivery route [RM2R-2, HQ D74, R1-F6]:** the original `C-DLV:Prop-F` configuration used the LS0 cap $\ell_n$; the frozen `W2-UNI:F-UNI@2.1.0` states the shipped cap $\ell_n+|\tilde S_0|$ and the amended allocation (`W2-UNI/lemmas/L5_delivery.md:8-12`); the active delivery route here is `W3-RM2-R:DLV-0`, whose shipped-code audit and conditions are carried explicitly [R1-F6] (item 0). Items 1–3 and the bridge B6.6 / lemma R3 are kept as the history of the row
   and are not used by the current statement. The abstract still leads with the common-data-event clause (H5 card 14).

### Bridges
| # | Bridge | Mark | Detail |
|---|---|---|---|
| B6.1 | (A5) ⇒ (T1-R) (= LSF with $\psi_n=c$) and (FL-R) | NEW arithmetic | As B2.1; and $16+s_0\le5(A+1)(s_0+1)\log n$ for $n\ge3$, $s_0\ge1$. |
| B6.2 | (A4)(i),(ii) = (L-R^b) | identity | (L-gain-R) with $\varpi_n=o(\sqrt{\log n/n})$; (L-loc-R) with $r_n\to0$ (RM2 STATEMENT.md:176-189). (L-feas) carried in (A4). |
| B6.3 | (A6) + (A5) ⇒ (D-loc^b) incl. its variance clause | **NEW** (one paragraph; proof below) | (D-loc^b) = RM (D-loc) (RM STATEMENT.md:154-156) with $L_n^2\log(|Q|+1)=o(\log n)$; its second clause $\operatorname{Var}(W_l\mid W_{T\cap N_l})\le(1+\eta_n)\operatorname{Var}(W_l\mid W_T)$, $\eta_n\to0$, follows from (A6) and (A5): see proof. |
| B6.4 | (D-loc^b) ⇒ (D-R^b) ⇒ (W-R) | EXISTS-CHECKED | `W3-RM2:D-to-W@1.0.3`, "PROVED-CHECKED; council R1, …" (STATEMENT.md:256, (C3)/(P9)). |
| B6.5 | (T1-R) ⇒ posterior input [POST] | EXISTS-CHECKED, conditional | `W3-RM2:POST-R@1.0.3`, "PROVED-CHECKED, conditional on W2-APP:POST; …" ⇐ B2.2 (EXISTS-CHECKED; `W2-APP:POST@1.0.7` "PROVED-CHECKED", main 6cd699dd) [S4-F1, REG-6cd6]. |
| B6.6 | RM2-R conclusions ⇒ F-UNI premises (S), (P), (V); F-UNI's operational premises carried as (S4) | **NEW** (assembly; (V)/(S)/(P) part passed S1) | (S): $P(\mathrm{Sand}\cap\mathrm{NA}\cap\mathrm{TL})\ge1-\sum P(\cdot^c)\to1$ from [SAND(Q)], [NA(Q)], [TL(Q)]; (P) = [POST]; (V) = "(R) with $\lambda_{\min}(\Sigma_n)>0$". LS0 cap and default-on tier-1 fallback match (`v3_calib.R:141-144`). F-UNI's method/premise/allocation paragraph (`L5_delivery.md:7-12`: EX-A as cost model, IDEAL-W, EX-S, SR, e4/TDP-IMPL, GUARD-W, MACH, CONFIG, valid seed, allocation and preflight inequalities at $(n,p_{\mathrm{raw}})$; P1/S.3 "AUDITED (code reading)") is **not derived**: it is carried as (S4) [S1-F2]. Premise-by-premise table: proof leg (`lemmas/R3_delivery_assembly.md`). **Historical** (former hypotheses only; superseded by B6.6′) [R1-F2]. |
| B6.6′ | (S4) ⇔ delivery premises (D) of RM2-R-plus; RM2-R-plus's conclusions are the reader conclusions | identity [RM2R-2] | (S4)(i)–(iv) state in words `W3-RM2-R/STATEMENT.md:71-93` (IDEAL-W⁺, EX-A, MACH, CONFIG at the shipped configuration, TDP-IMPL, allocation 𝒜_n, valid non-degenerate input). No assembly with F-UNI is needed; B6.6 is kept for the record and superseded by B6.6′ for the shipped method. Needs one line check with the bridges leg. |
| B6.7 | standardised-signal convention | limit | The masters take $\theta^*$ deterministic (Setting R). A raw-scale version (fixed $\beta^*$) would need a **NEW** bridge (medium; the population conditions involve $\theta^*$). Not proposed for CP1. |

**Proof of B6.3.** Fix $l$ and $T$ in the lattice with $l\notin T$, put $A:=T\cap N_l\subseteq T$ and
$d:=\bar\beta_{T,l}-\bar\beta_{A,l}$ (supported in $T$, $\|d\|_1\le L_n$). Since $W_l-W_T^\top\beta_{T,l}$ is
uncorrelated with $W_T$,
$\operatorname{Var}(W_l-W_A^\top\beta_{A,l})=\operatorname{Var}(W_l\mid W_T)+d^\top\Sigma_{n,TT}d$. Unit diagonal gives
$|\Sigma_{ik}|\le1$, so $d^\top\Sigma_{n,TT}d\le\|d\|_1^2\le L_n^2$; and
$\operatorname{Var}(W_l\mid W_T)\ge\lambda_{\min}(\Sigma_{n,T\cup\{l\}})\ge c$ by (A5) (interlacing, $T\cup\{l\}\subseteq Q\cup\{l\}$).
Hence $\operatorname{Var}(W_l\mid W_A)\le(1+L_n^2/c)\operatorname{Var}(W_l\mid W_T)$ with $\eta_n:=L_n^2/c\to0$ by
(A6). (This is why (A6) asks $L_n\to0$ besides $L_n^2\log(|Q|+1)=o(\log n)$; the two coincide when $|Q|\ge n^{b'}$ for a
fixed $b'>0$. When $|Q|$ is only polylogarithmic the master allows a bounded $L_n$ with the variance clause assumed
separately; the reader version gives that case up for a shorter statement.) ∎

**Effort:** B6.1, B6.3 half a page; B6.6 one page with a premise-by-premise table; all three need one Sol line check.

### Honest limits
All assumptions are on the population law, but (A4) and (A6) are long and specific (15 = block size − 1; partial
covariances; local regressions). They are the natural price of a statement about a *search* algorithm: they say that
the signal is not masked, that what can imitate it is confined to a set of size $n^b$, and that within that set
regressions are local. HQ choices: keep them as stated (faithful), or state Theorem 6 in words in the abstract
("under visibility, polynomially bounded leakage and local dependence") with the full list in the theorem.

#### Update log (thm6)
- v0.1 2026-11-15: first version (CP1).
- v0.2 2026-11-15: S1 fixes [S1-F2] delivery under (S4); [S1-F3] common envelopes (STRONGER hypotheses; WEAKER unconditional clause).
- v0.3 2026-11-16: [R3] (S4) completed from the delivery premise table (EX-S, stop/return rule, stop-only guard, e4 tie
  rule; STRONGER convention list, now faithful); F-UNI qualifications quoted; [H5-2] delivery clause out of the
  abstract until F-UNI's correctness gate is resolved.
- v0.4 2026-11-16: [S2-F1] (S4) carries MACH, CONFIG, TDP-IMPL and the amended allocation by exact source reference.
  Tag (S3): **WEAKER** for the "always produces output" clause — restores the master's own premises
  (`C-DLV/STATEMENT.md:28-46`, `FINAL/sections/s6_delivery.tex:29-35`); common-data-event clause EQUAL.
- v0.5 2026-11-16: [REG-f526] RM2-R's input `W2-APP:POST@1.0.6` status and the RM-R special-case status quoted (EQUAL).
- v0.6 2026-11-16: [REG-33e1] SL0 cleared: row 3.1 conditional on T03♯ only; RM2-R/POST-R @1.0.2, RM-R @1.1.2 (EQUAL).
- v0.7 2026-11-16: [FUNI-N] delivery clause narrowed with F-UNI 2.1.0: bounded domain $\mathfrak D$ under (S4)(i)–(iv), every $n$
  under IDEAL-W⁺ ((S4)(v)); F-UNI narrowing to 2.1.0 noted; sentence [RM2R-5] added after the display. Tag: **WEAKER** for the delivery clause (follows the
  master's narrowing); common-data-event clause EQUAL.
- v0.8 2026-11-16: [RM2R-1..3, RM2R-7] RM2-R rider (READER_DELTA v-next e78a1055) (statuses verbatim, main 5d3a8a70 [REG-5d3a]) (W3-RM2-R CP3, HQ card 14). Master: RM2-R-plus + RM0-plus + DLV-0; method-drift
  note; (S4) adds the two lifted code ceilings and the valid-input clause; error split as a remark. Tag **MIXED**:
  STRONGER — the conclusion now has the mode form (RM0-plus) and its delivery clause is about the shipped configuration;
  WEAKER — delivery needs IDEAL-W⁺ (two code ceilings lifted) and a narrower (valid, non-degenerate) input domain, and
  the implication edge to `C-DLV:Prop-F` is withdrawn. Assumptions (A1)–(A6) EQUAL.
  Supersedes the [FUNI-N] delivery wording of v0.7: delivery now rests on DLV-0 (method drift [D74]); (S4)(v) folded into (S4)(i) as IDEAL-W⁺, and $\mathfrak D$ is stated in the [RM2R-5] sentence.
- FRZ-RQ 2026-11-16: [REG-6cd6] RM2-R @1.0.3 (ACTIVE, supersession deferred), POST-R/D-to-W @1.0.3, `W2-APP:POST@1.0.7` "PROVED-CHECKED", F-UNI @2.1.0 (history), RM-R @1.2.0 SUPERSEDED-VALID; row conditions now only the two delivery-path audits. Statuses only (EQUAL).
- v0.9 2026-11-16: [GUARD-W] (HQ YES 11-16; W3-AUDIT track A T1 GUARD-W, theory/W3-AUDIT 58e24245, `track_A/T1_GW/`) sentence added after the delivery display, with a pointer to the meaning of "output" (code: `v3_fit.R:84`, `v3_run.R:142-145`): "The guarantees describe the run as if uninterrupted; a run stopped by its time guard reports status `resource_limit` and no output." Presentation (EQUAL).
- R1 2026-11-16: [R1-F6] delivery-route sentence corrected (frozen F-UNI@2.1.0 states the shipped cap; only C-DLV Prop-F used $\ell_n$); [R1-F2] B6.6 / R3 marked historical; [R1-E7] $\mathcal G_n$ choice in remark (i) (EQUAL; corrections of descriptions).
- R2-ED 2026-11-16: [R2-O6] remark (iii) example status verbatim (EQUAL).
- FRZ-B 2026-11-16: [B2] GUARD-W wording "returns no estimates; anything else … flagged incomplete and is not covered" with code lines (EQUAL).
- FRZ-B 2026-11-16: [T14-REP] (H5 card 16, AGREED; `W3-AUDIT-AX:REP@1.0.0`; W3-AUDIT d727e7a3 `track_A_C/H5_T14_CARD.md` "Consultant edits") integer-limit passage: one sentence, then the caps, $\mathfrak D$, code lines with $p_{\mathrm{raw}}$; in the default configuration neither limit can be reached on any input R can represent; the other IDEAL-W obligations remain — **STRONGER** (informal remark [RM2R-6] → proved code fact; no premise added or dropped).
- FRZ-B 2026-11-16: requote at main fe05ccec [REG-fe05] (D95): masters RM2-R-plus/RM0-plus/DLV-0/Cont-plus @1.0.1 plain "PROVED-CHECKED; council R3, …"; the two C-DLV audits "CODE-CHECKED"; row 3.1 carries no open registry condition; B1 moot (EQUAL, statuses only).
- v1.0 2026-11-17: [H5-17] H5 card 17 (consultant AGREED; D115, D120, D121): Corollary 6L (pending recording; pathwise sentence for Cor 9C) and Corollary FAMC (`W3-FAMC:Cor-FAMC`, main 8b4d3101) added in §11. No hypothesis of Theorem 6 changed. Tag: Theorem 6 **STRONGER** through 6L (added conclusions); FAMC additive.
<!-- ROW thm6 END -->

---

## 7. Theorem 7 — The reported model equals the truth (fixed design)
<!-- ROW thm7 BEGIN -->
**Card row** 3.2 · **Section version** 0.6 (2026-11-16) · **Pending delta** — (RM2-F rider T4/T2 merged, v0.6)


### Reader statement (two sufficient versions)
**Theorem 7.** Let the design be fixed, with non-constant raw columns [R3]. Assume
- **(A1) Model and posterior conditions.** (S1), (S2), (S3); (A2)–(A5) of Theorem 1; and the beta-min
  $\theta^*_{\min}\ge C_\beta\,\sigma_*\sqrt{\log n/n}$ with a fixed $C_\beta$ above an explicit constant depending on
  $(s_0,A,M,\sigma_*^2,\varphi_0)$ (Remark (a)), or $\theta^*_{\min}\ge\sigma_*\sqrt{M_n\log n/n}/\varphi_0$ for a fixed sequence $M_n\to\infty$ [RM2R-4].
- **(A2) Floors.** $\lambda_{\min}(\hat R_T)\ge\varphi_0^2$ for every $T$ with $|T|\le16$ and for every
  $T=Q\cup\{l\}$, $l\in[p]$ ($Q$ as in (A4)).
- **(A3) Visibility.** There is a fixed $M_V$, larger than an explicit constant depending on $(A,M,\sigma_*^2)$
  (Remark (a)), such that $\delta^2_{U,j}\ge M_V\log n$ for every $j\in S_0$ and every $U\not\ni j$ with $|U|\le15$
  (large $n$) [RM2R-4].
- **(A4) Bounded leakage.** There are a deterministic $Q\supseteq S_0$ (with $|Q|\le K$ and ($Q=[p]$ or
  $K\ge2|Q|+32s_0+1$) for large $n$) and a fixed $\eta\in[0,\eta_A)$, $\eta_A:=(\sqrt{2A+1}-\sqrt{2A})^2$, such that
  $\delta^2_{U,l}\le\eta\,\tau^2_U\log n$ for every $l\notin Q$ and every $U\not\ni l$ with $|U|\le15$.
- **(A5) Size of the leakage set**, one of:
  (a) $|Q\setminus S_0|\le(1-\delta)\log n$ for a fixed $\delta\in(0,1)$; or
  (b) $|Q|\le n^b$ with $b<\tfrac12-\tfrac\eta2-\sqrt{2A\eta}$; $\theta^{*2}_{\min}\ge C_Q\,\sigma_*^2(|Q|+\log n)/(n\varphi_0^2)$ for a
  fixed $C_Q$ above an explicit constant (e.g. any fixed $C_Q>\max\{32,\,64A+c\}$ with $c$ as in Remark (a)) [RM2R-4, R2-O4]; and *local
  regressions*: for every $l$ a deterministic set $N_l\subseteq Q\setminus\{l\}$ with $|N_l|\le h\log_2n$, $h+b<\tfrac12$,
  and a deterministic $L_n\to0$ with $L_n^2\log(|Q|+1)=o(\log n)$, such that
  $\|\hat\beta_{T,l}-\hat\beta_{T\cap N_l,l}\|_1\le L_n$ for every $T$ with $S_0\subseteq T\subseteq Q$, $|T|<K$,
  $l\notin T$.

Then there are data events $\mathcal G_n$, $P(\mathcal G_n)\to1$, on which every admissible run that produces output
reports $\hat S=S_0$, for every seed and calibration outcome; in particular $P(\text{output and }\hat S\neq S_0)\to0$.
If moreover the delivery conventions (S4) hold [S1-F2, RM2R-1],
$$
P(\text{the run produces output})=1\ \ \text{for every admissible }n\ge3,\qquad P(\hat S=S_0)\to1 .
$$
The delivery statement lifts two integer limits of the code (IDEAL-W⁺); in the default configuration neither can be reached on any input R can represent ($n, p_{\mathrm{raw}} \le 2^{31}-1$) [T14-REP], so this matters only for the $n\to\infty$ form. The two limits are a base search cap of $10^6$ (`v3_run.R:96`) and a 32-bit integer bound $2^{31}-1$ on the search cap (`cpp/v3_core.cpp:474`). R stores matrix dimensions as 32-bit integers, so in the default configuration the base cap is $\lceil\log_2(n+p_{\mathrm{raw}}+1)\rceil\le32$ and the search cap is at most $32+\lfloor n/2\rfloor\le2^{30}+31$, and neither limit can fire [T14-REP]. Every such input lies in the bounded domain $\mathfrak D=\{\lceil\log_2(n+p_{\mathrm{raw}}+1)\rceil\le10^6,\ \lceil\log_2(n+p_{\mathrm{raw}}+1)\rceil+\lfloor n/2\rfloor\le2^{31}-1\}$, on which delivery holds under the remaining conventions (S4), without IDEAL-W⁺ [RM2R-5]; IDEAL-W⁺ is used only by the asymptotic form. Representable inputs still carry the other obligations of IDEAL-W (for example `2*p-1` in `int` for $p\ge2^{30}$); the statement is for the default configuration (`v3.ls0_ell` unset).
The guarantees describe the run as if uninterrupted; a run stopped by its time guard reports status `resource_limit` and returns no estimates; anything else it returns is flagged incomplete and is not covered (`v3_fit.R:84-85`; `v3_run.R:110-113, 142-147`) [B2]. [GUARD-W]

*Remarks* [RM2R-4]. (a) *Constants.* With $C_R:=3(M+\sigma_*^2)$ ($\|X\theta^*\|^2\le nM$): (A3) holds with any
$M_V>(\sigma_*\sqrt{2A}+\sqrt{(2A+1)C_R})^2$; (A5)(b)'s signal clause may be replaced by the master's (BM-Q♭) [R1-E2]:
$(n-1)\varphi_0^2\theta^{*2}_{\min}/\sigma_*^2\ge32(|Q|+1)+64\log(2p)+c\log n$ with a fixed $c>\max\{16,\,8(A+1)+4(2A+1)C_R/\sigma_*^2\}$;
under (A5)(a) the beta-min of (A1) suffices with $C_\beta^2\varphi_0^2>\max\{c_0(s_0,A),\,8(A+1)+4(2A+1)C_R/\sigma_*^2,\,8(1+\sqrt{D/2})^2\}$
for a fixed $D>2+4A$. These are proof constants, not sharp. (b) Under (S4), for every seed and calibration outcome,
$P(\hat S\neq S_0)\le P(S_0\text{ is not the unique maximiser of the score})+P(\text{the local search from the start mode does not
reach }S_0)$. *(Interpretation, not part of the theorem [D71]: posterior-mode error plus search error.)*

### Intuition for each condition (for the paper's text)
- *Visibility (A3).* Each truth, added alone to any small model that misses it, explains at least a fixed multiple of
  $\log n$ more signal — more than the prior charges for one variable plus the largest noise gain among the $p$
  candidates [RM2R-4]. So the start law, which judges variables block by block, never leaves a
  truth out.
- *Bounded leakage (A4).* Outside $Q$, no column, added to any small model, explains more than a fraction $\eta$ of
  $\log n$ residual-variance units; such columns never look like signal and stay out of the start mode.
- *Size of $Q$ (A5).* Columns of $Q$ may enter the start mode. The local search then removes them one at a time; for that
  the score must not reward *adding* any column at any model between $S_0$ and $Q$. This holds automatically when $Q$
  has fewer than $\log n$ extra columns (a), or when every column's regression on such models is carried by a few
  ($O(\log n)$) members of $Q$ (b).
- *Floors (A2).* Regressions on blocks and on $Q\cup\{l\}$ are well posed.

### Master theorem
[RM2R-2] `W3-RM2-R:RM2-F-plus@1.0.1`, `Theory_work/Wave3/W3-RM2-R/STATEMENT.md:166-176` (hypotheses §2 :95-112 and PARENT's;
conclusion with [MODE] and, under (D), delivery and the error split; conditions of the row: none open (T03♯ discharged, main 6cd699dd; the two C-DLV code-reading audits discharged, main fe05ccec) [RM2R-7]), status verbatim **"PROVED-CHECKED; council R3, MANIFEST 5d6d3c90… (= R3 b06a8588 re-frozen as R3r), sol=9.5 PASS, opus=9.4 PASS"** (main fe05ccec, D95) [REG-fe05]; DLV-0 takes the two C-DLV code-reading audits as hypotheses [RM2R-7]; `C-DLV:L2-S3@1.0.1` and `C-DLV:P1-Inventory@1.1.1` are now each **"CODE-CHECKED (second seat, code reading; holds at pin 4676af6 after amendments A-1–A-7); council R2, MANIFEST 12802ac7…, sol=9.3 PASS, opus=9.4 PASS"**; with `W3-RM2-R:RM0-plus`
and `W3-RM2-R:DLV-0` as in §6. It implies the previous master (`W3-RM2-R:Cont-plus`), kept below for the record (supersession deferred post-freeze; `W3-RM2:RM2-F` stays ACTIVE).
Delivery route: as §6 [HQ D74, R1-F6].
Previous master: `W3-RM2:RM2-F@1.0.3` (ACTIVE), `Theory_work/Wave3/W3-RM2/STATEMENT.md:206-214` (assumptions :126-170), status verbatim
**"PROVED-CHECKED; council R1, MANIFEST 00bbeab8…, astra=9.5 PASS, opus=8.8 PASS; …"** [REG-6cd6]; with `W3-RM:RM-0@1.0.0` and `W2-UNI:F-UNI@2.1.0` as in §6 (input validity "(E) with
nonconstant raw columns").

### Bridges
| # | Bridge | Mark | Detail |
|---|---|---|---|
| B7.1′ | (A1) ⇒ (T1-F♭) | identity + B1.1–B1.4 [RM2R-4] | (T1-F♭) = Theorem 1's (H0) with BM-∞ or BM(c), c > c₀ (`W3-RM2-R/STATEMENT.md:95-99`); (A1)'s constant exceeds c₀. Replaces B7.1. |
| B7.2′ | (A5)(a) + (A1) ⇒ (BM-W⁺) | NEW (two lines; council-checked as READER_DELTA R7.2 of W3-RM2-R) | fixed $D>2+4A$, $d_n^2\le D\log n$ for large $n$; the strict constant of Remark (a); `W3-RM2-R/STATEMENT.md:107-112` (last sentence of (BM-W⁺)). Under $\theta^*_{\min}\ge\sigma_*\sqrt{M_n\log n/n}/\varphi_0$ for a fixed sequence $M_n\to\infty$: (BM-W) ⇒ (BM-W⁺). |
| B7.3′ | (A5)(b) signal clause (Remark (a) form) ⇒ (BM-Q♭) ⇒ (BM-W⁺) | identity | `W3-RM2-R/STATEMENT.md:107-112`; checked as R7.3 of W3-RM2-R. |
| B7.4′ | (A3) = (V♭) | identity | `W3-RM2-R/STATEMENT.md:101-105`. |
| B7.1 | (A1) ⇒ (T1-F) | as B1.1–B1.4 (with BM-∞) | (T1-F) uses BM-∞ (RM STATEMENT.md:91-92). Superseded by B7.1′ for the current master. |
| B7.2 | (A5)(a) ⇒ (L-size^b) for every small $b>0$, (W) via (W-χ), (BM-W) = BM-∞ | EXISTS-CHECKED | `W3-RM2:W-suff@1.0.3` (C3)(c) "(W-χ) ⇒ (W-δ)" (current); historical, under the former hypotheses: (BM-W) reduces to BM-∞ when $d_n^2=O(\log n)$ (STATEMENT.md:137-139); truth removal now via B7.2′ [R2-E1]. $b<\beta(\eta,A)$ is possible because $\eta<\eta_A$. |
| B7.3 | (A5)(b) ⇒ (W) via (W-loc) ⇒ (W-ref) ⇒ (W-unif) ⇒ (W-δ) | EXISTS-CHECKED | `W3-RM2:W-suff@1.0.3`; the variance clause of (W-loc) follows from $L_n\to0$ under the floor on $Q\cup\{l\}$ (STATEMENT.md:164). Historical, under the former hypotheses: $\theta^{*2}_{\min}n/(|Q|+\log n)\to\infty$ is (BM-Q) ⇒ (BM-W) (:138-139); truth removal now via B7.3′ [R2-E1]. |
| B7.4 | RM2-F conclusions ⇒ F-UNI premises (S), (P), (V) | **NEW** (assembly) | as B6.6, fixed-design input validity ((E) with nonconstant raw columns); operational premises carried as (S4) [S1-F2]. Superseded by B7.5 for the shipped method (method drift, §6). |
| B7.5 | (S4) ⇔ (D) | identity [RM2R-2] | as B6.6′. |

### Honest limits (the case the brief names)
(A3)–(A5) are **sample-level conditions on $(X,\theta^*)$**: partial signal gains $\delta^2_{U,j}$ and sample regressions.
They are interpretable but not reducible to eigenvalue floors and beta-min: visibility fails on well-conditioned designs
where truths cancel (masking), and the lattice condition (A5) is a condition on the *search route*, not on the
posterior. What exists instead: (i) the intuition paragraphs above, one per condition; (ii) Theorem 6, which gives the
same conclusion under population analogues of these conditions [R1-S6]; (iii) the examples table (polylog: every
example of the earlier version; polynomial: one truth with $n^b$ weak proxies, `W3-RM2:Ex-Proxy@1.0.3` "PROVED-CHECKED; council R1, …"; one
equicorrelated group, $b<3/10$, `W3-RM2:Ex-Equi@1.0.3` "PROVED-CHECKED; council R1, …"; polynomial decay $\alpha>2$,
`W3-RM2:Ex-PolyF@1.0.4` "PROVED; line-checked LC2-C; Astra seat ACCEPT; not examined by the Opus seat — next council round"
(main c9b3b967: the conditions on W2-LOC2:Lemma-BC, W2-LOC2:Lemma-IR are dropped) [R1-E8].
**Not available:** the theorem without any lattice condition (open problem: control of the actual search path), and
any $b\ge\tfrac12$. Recommendation: present (A5)(a) in the main text (fully explicit) and (b) as the strengthening.

#### Update log (thm7)
- v0.1 2026-11-15: first version (CP1).
- v0.2 2026-11-15: S1 fixes [S1-F2] delivery under (S4) (WEAKER unconditional clause).
- v0.3 2026-11-16: [R3] non-constant raw columns stated (input validity of the delivery result); $N_l$, $L_n$ deterministic
  (as the master's (W-loc)); (S4) completed (STRONGER, now faithful).
- v0.4 2026-11-16: [S2-F1] as Theorem 6 (S4). Tag (S3): **WEAKER** for the delivery clause (restores the master's
  premises); statistical clauses EQUAL.
- v0.5 2026-11-16: [FUNI-N] as Theorem 6 v0.7 (delivery on $\mathfrak D$; every $n$ under IDEAL-W⁺). Tag: **WEAKER** for the
  delivery clause; statistical clauses EQUAL.
- v0.6 2026-11-16: [RM2R-1..4, RM2R-7] RM2-F rider (READER_DELTA v-next e78a1055) (statuses verbatim, main 5d3a8a70 [REG-5d3a]) (W3-RM2-R CP3, HQ card 14). Master RM2-F-plus; (A1) beta-min, (A3)
  visibility and the (A5)(b) signal clause at the constant level, constants in Remark (a); error split in Remark (b);
  method-drift note. Tag **MIXED**: STRONGER — (A1), (A3), (A5)(b) weakened to constant level, mode-form conclusion
  (RM0-plus); WEAKER — delivery needs IDEAL-W⁺ (two code ceilings lifted) and a narrower input domain, and the implication
  edge to `C-DLV:Prop-F` is withdrawn.
  Supersedes the [FUNI-N] delivery wording of v0.5: delivery now rests on DLV-0 (method drift [D74]); (S4)(v) folded into (S4)(i) as IDEAL-W⁺, and $\mathfrak D$ is stated in the [RM2R-5] sentence.
- FRZ-RQ 2026-11-16: [REG-6cd6] previous master RM2-F @1.0.3 "PROVED-CHECKED; …" (ACTIVE), W-suff @1.0.3, F-UNI @2.1.0 (history); T03♯ discharged. Statuses only (EQUAL).
- R1 2026-11-16: [R1-S6] honest limits (ii): Theorem 6 gives the same conclusion under population analogues (WEAKER); [R1-E8] example statuses verbatim; [R1-E2] Remark (a) reworded as the master's (BM-Q♭) replacement; [R1-F6] delivery-route label (EQUAL).
- R2-ED 2026-11-16: [GUARD-W] (manager 11-16: Theorem 7's guarantee concerns a run's output) time-guard sentence after the delivery display, as in Theorem 6 (EQUAL). [R2-O4] (A5)(b) $C_Q$ threshold example; [R2-E1] B7.2/B7.3 historical commentary labelled (EQUAL).
- FRZ-B 2026-11-16: [B2] as Theorem 6 (EQUAL).
- FRZ-B 2026-11-16: [T14-REP] as Theorem 6 — **STRONGER** (same delivery sentence).
- FRZ-B 2026-11-16: requote at main fe05ccec [REG-fe05] as Theorem 6: RM2-F-plus @1.0.1 (EQUAL, statuses only).
<!-- ROW thm7 END -->

---

## 8. Theorem 8 — Certified screening
<!-- ROW thm8 BEGIN -->
**Card row** 3.7 · **Section version** 0.6 (2026-11-16) · **Pending delta** —


### Reader statement
**Theorem 8.** Let the design be fixed and assume (S1), (S3) and
- **(A1) Sparse eigenvalue floor.** $\lambda_{\min}(\hat R_S)\ge\kappa$ for every $S$ with $|S|\le q_n+s_0$, with a constant
  $\kappa>0$ fixed in $n$;
- **(A2) Signals bounded below and coefficients bounded above by constants fixed in $n$.** $\theta^*_{\min}\ge b_0>0$ and
  $\|\theta^*\|_1\le M$, where $\kappa$, $b_0$, $M$ and the noise variance $\sigma_*^2$ do not depend on $n$ [SCR-PC];
- **(A3) Size budget.** $(q_n+1)\log p+\log n\le c_1n$, $c_1:=\kappa^2b_0^2/(200(M^2+\sigma_*^2))$, with
  $q_n\in\{0,\dots,K-1\}$ [S1-F8].

A run *certifies* its reported model $\hat S$ when the run's local-optimality flag is set for $\hat S$. Then
$$
P\big(\text{output},\ \hat S\text{ certified},\ |\hat S|\le q_n,\ S_0\not\subseteq\hat S\big)\to0 .
$$
In particular this holds for $p\le n^A$ and every $q_n=o(n/\log n)$. Signal sizes or floors that vary with $n$ are
**not** covered by this theorem (removing "fixed" is the named open item SCR-R1, a post-freeze rider) [SCR-PC]. No condition on the start, leakage, blocks or
visibility is used beyond (A1)–(A3), and $p\le n^A$ is not needed. (The master needs only a weaker directional floor,
which leaves null-null correlations free; the full floor (A1) does constrain them [S1-F8].)

### Placements of row 3.7 (form (a), plain: second SCR council round passed — W3-SCR-R2 R2 + diff round R3, MANIFEST_R3 `19847f54…`, both seats PASS; H5 cards 9 and 11; HQ acceptance) [SCR-R2]
- **Abstract:** *"Certified screening: if the design has a sparse eigenvalue floor $\kappa$ on models of size $q_n+s_0$, the
  true coefficients satisfy $\theta^*_{\min}\ge b$ and $\|\theta^*\|_1\le M$, the constants $\kappa$, $b$, $M$ and the noise
  variance $\sigma_*^2$ are fixed in $n$, $q_n$ is below the method's model-size cap $\min(p,\lfloor n/2\rfloor)$, and
  $(q_n+1)\log p+\log n\le c_1n$ with an explicit constant $c_1$ depending only on $\kappa,b,M,\sigma_*$, then the probability
  that a run produces output, certifies a reported model of size at most $q_n$ ("certifies": the run's local-optimality
  flag is set for that model), and that model misses a true predictor tends to zero — with no visibility, leakage, start
  or block condition."* (The formula for $c_1$ stays in Theorem 8 (A3).)
- **Body:** Theorem 8′ (signals that may vary with $n$; master `W3-SCR:A-inf`), plain.

**Theorem 8′ (body; certified screening with signals that may vary with $n$).** Let the design be fixed and assume (S1),
(S3). For $S\subseteq[p]$ and $t\notin S$ let $\gamma(t\mid S)$ be the *noiseless gain* of $t$ given $S$,
$\gamma(t\mid S):=(x_t^\top R_S\mu)^2/(x_t^\top R_Sx_t+\tfrac1{n+1})$ with $R_S:=I-X_S(G_S+\tfrac1{n+1}I)^{-1}X_S^\top$ (`W3-SCR/STATEMENT.md:51-56`);
equivalently $\tfrac{n+1}n$ times the decrease of the method's quadratic form $Q^\mu_S$ when $t$ joins $S$ and the response is
replaced by its mean $\mu$ [R1-E2]. Let $\Gamma_n(q):=\min\{\max_{t\in S_0\setminus S}\gamma(t\mid S):|S|\le q,\ S\not\supseteq S_0\}$ (every model of
size $\le q$ that misses a truth has some missing truth with gain at least $\Gamma_n(q)$), and
$\tau_n^2:=\sigma_*^2+\|\mu\|^2/(n-1)$. If $q_n\in\{0,\dots,K-1\}$ and
$$
\liminf_{n\to\infty}\frac{\sqrt{\Gamma_n(q_n)}}{\tau_n\sqrt{2\log p+\log n}+\sigma_*\sqrt{2q_n\log p}}>1 ,
$$
then $P\big(\text{output},\ \hat S\text{ certified},\ |\hat S|\le q_n,\ S_0\not\subseteq\hat S\big)\to0$. No condition $p\le n^A$, no
bound on $s_0$, and no condition on the start, leakage, blocks or the collinearity of the null columns is used.
*Master:* `W3-SCR:A-inf@1.0.0`, `Theory_work/Wave3/W3-SCR/STATEMENT.md:87-90` (with the definitions at §1), status
**"PROVED-CHECKED"**; its non-asymptotic form `W3-SCR:SCR-A@1.0.0` (:79-85, probability $\le3e^{-x}$ under a finite-$n$
margin condition), **"PROVED-CHECKED"**. Theorem 8 is its corollary under fixed constants (`W3-SCR:A1`). *Bridge:* none
(the quantities are the master's, described in words).
*Reviewed together with Theorem 8 in the second SCR council round; A-inf ACCEPTed by both seats (stated plain).*

### Why each assumption
(A1) only the realised combination of missing truths must keep a fraction of its energy outside any small model (the
master uses a weaker directional floor); the full floor is not needed (numerics with highly correlated nulls).
(A2) signals and coefficient bounds are constants fixed in $n$, as in the master (`W3-SCR/STATEMENT.md:158-160`, "with κ,
b, M, σ fixed (not depending on n)"); a separate statement with beta-min at rate
$\sigma\sqrt{((q_n+1)\log p+\log n)/n}$ exists (`W3-SCR:A1o`, different hypotheses), and is not part of this theorem [SCR-PC].
(A3) a union bound over models of size $\le q_n$.

### Master theorem
`W3-SCR:A1@1.0.0`, `Theory_work/Wave3/W3-SCR/STATEMENT.md:158-163`, status **"PROVED-CHECKED"** (registry main d2b600ba,
interim label removed; council cell R3, MANIFEST 19847f54…, sol=10.0 PASS, opus=9.4 PASS) [REG-d2b6]. Companion for
uncertified runs, not part of Theorem 8: `W3-SCR:SCR-G@1.0.0` (:132-145), status **"PROVED-CHECKED"** (same registry
commit and council cell) [REG-d2b6].

### Bridges
None: the statement is the master's, with the floor named in standard terms (the master already lists the sparse
eigenvalue floor as the sufficient case, :158-159). "Certified" must be explained in words (NOTATION §5).

### Honest limits
- The bound is on the probability of an intersection: a run produces output, certifies a small model, **and** that
  model misses a true predictor. It is not a guarantee conditional on certification, and it does not say that the
  method returns a superset of the true model with probability tending to one.
- A run is not claimed to certify a small model with probability tending to one (`W3-SCR/STATEMENT.md:217-218`); how
  often it does is reported from numerics (see the certification-frequency line).
- It is one-sided: certified small models are not shown to equal the true model; exact recovery from the
certificate needs a near-orthogonality floor (`W3-SCR:SCR-C`, PROVED-CHECKED), which is not reader-friendly
($\varphi_n(q_n)\ge2A/(2A+1)+\epsilon$) — keep it as a remark.

### Certification frequency (numerics, not a theorem) [SCR-R2]
A run certifies a model when its local-optimality flag is set. In existing numerics the method certified the
reported model in every completed run: 2,394 of 2,394 in the 2,400-fit study ($n=200$); 376 of 376 in the strong-factor
experiment ($n\le150$, $p$ up to $10n$); 71 of 71 in the screening study ($n=100$). Where model sizes were recorded the
certified models were small: all 376 strong-factor fits had at most $2s_0$ predictors, all 71 screening fits at most 5
(the 2,400-fit study records no per-fit size) [S4-F2]. On strong-factor designs
(equicorrelation $\rho\in\{0.5,0.7\}$, $p\ge2.5n$, $s_0\in\{4,8\}$) the certified model contained every true predictor in
61 of 122 fits at $n=50$, 18 of 20 at $n=75$ and 30 of 30 at $n=100$. At these constants (A3) requires $n\gtrsim1{,}450$.
(Sources: `/home/fb31/BVS-wt/W3-SCR-R2/Theory_work/Wave3/W3-SCR-R2/reviews/READER_DELTA.md` §5, theory/W3-SCR-R2 @ 048b6b23.)

#### Update log (thm8)
- v0.1 2026-11-15: first version (CP1).
- v0.2 2026-11-15: S1 fixes [S1-F8] q_n range and null-correlation wording (EQUAL).
- v0.3 2026-11-16: [SCR-PC] (A1)–(A2) state that κ, b₀, M, σ* are fixed in $n$, matching `W3-SCR/STATEMENT.md:158-160`
  (the master's current text); n-dependent signals not covered (SCR-R1); A1° named as a separate claim; placements
  (i) abstract clause / (ii) body theorem for H5 card 7 (EQUAL to the current master; tag to be confirmed by the Sol
  statement-change check).
- v0.4 2026-11-16: [H5 card 7 verdict] abstract clause names κ, b, M, σ as fixed in $n$; body Theorem 8′ (master
  A-inf) for $n$-varying signals; forms (a)/(b1)/(b2) for the second SCR council round, (b1) recommended (NEW body
  statement = master A-inf in words; EQUAL to its master).
- v0.5 2026-11-16: Theorem 8′ form dependency on the W3-SCR-R2 per-claim table noted (plain if A-inf ACCEPT, else
  (b1) label) (EQUAL).
- v0.6 2026-11-16: [W3-SCR-R2 CP3; H5 cards 9, 11; recorder task R main 8875eeba, interim label removed d2b600ba] form (a) for row 3.7, plain (second SCR council round passed, R3 bind
  OK 19847f54…); Theorem 8′ plain (A-inf ACCEPT); abstract: $c_1$ by name only (formula in body), $q_n$ below the cap
  $\min(p,\lfloor n/2\rfloor)$ stated; honest limits: intersection event, certification not claimed w.p. → 1;
  certification-frequency line (EQUAL). Source: W3-SCR-R2 `reviews/READER_DELTA.md` v4 @ 048b6b23. At application:
  "certifies" defined at first use in the reader statement; the delta line's closing sentence on the sample size (A3)
  requires at these constants is omitted (owner rule: no sample-size thresholds); A1, SCR-G statuses quoted at d2b600ba.
- S4 tag record 2026-11-16 [S4-S3]: v0.6 is EQUAL to its delta (W3-SCR-R2 v4). Against the S3 text: card row 3.7's
  intersection event and fixed-constant scope are WEAKER (restore `W3-SCR:SCR-A` :80-89, `A1` :158-163); Theorem 8′ is a
  STRONGER addition (EQUAL to `W3-SCR:A-inf`). S4 [S4-F2]: certification counts separated from size evidence (WEAKER, restores
  the cited measurements' scope).
- v0.6.1 2026-11-16: [HQ card 11 follow-up] the delta's closing sentence "At these constants (A3) requires $n\gtrsim1{,}450$."
  restored verbatim in the certification-frequency line (HQ: "the (A3) n ≳ 1,450 fact stays"; supersedes the v0.6
  omission) (EQUAL).
- R1 2026-11-16: [R1-E2(sol)] Theorem 8′: noiseless gain given by its exact formula (EQUAL).
<!-- ROW thm8 END -->

---

## 9. Theorem 9 — The posterior recovers the conditional law of the response, in Song–Liang's distance
<!-- ROW thm9 BEGIN -->
**Card row** 2.1 · **Section version** 0.4 (2026-11-16) · **Pending delta** —


### Setting and notation
The data are $n$ independent copies $(x_i,y_i)$, $i=1,\dots,n$, of a pair $(x,y)$: $x\in\mathbb R^{p_{\mathrm{raw}}}$ is the
vector of all observed predictors (a row of $X^{\mathrm r}$, §1 of the notation) and $y\in\mathbb R$ the response (an entry of
$y^{\mathrm r}$). $D_n$ denotes the data set. $p_{\mathrm{raw}}$ may grow with $n$ and may be much larger than $n$; the law of
$(x,y)$ may change with $n$. As in every theorem, $p\le p_{\mathrm{raw}}$ is the number of predictors not constant in the
sample, and the method runs on these (standardisation §2, prior $\mathrm{BB}(1,p)$ capped at $\min(p,\lfloor n/2\rfloor)$, slab
and inverse-gamma prior §3; no tuning). $\Pi(\cdot\mid D_n)$ is the resulting exact posterior of $(S,\beta,\sigma^2)$, mapped
back to the original units: $S$ is the set of included predictors, $\beta\in\mathbb R^{p_{\mathrm{raw}}}$ the coefficient vector
(zero outside $S$ and on removed predictors), $\sigma^2$ the noise variance. If fewer than two predictors remain, or the
response is constant in the sample, the posterior is not defined; under the assumptions below such data sets have
probability smaller than the exceptional probabilities in the theorems and are counted in them: there the posterior probabilities in the displays are read as 1.
The common exceptional set of the proofs also contains every data set with $p<p_{\mathrm{raw}}$.

*What is estimated.* A draw $(S,\beta,\sigma^2)$ defines a conditional law of $y$ given $x$,
$N\big(\bar y+(x-\bar x)^\top\beta,\ \sigma^2\big)$, with the sample-mean intercept ($\bar y$, $\bar x$ are the sample means). The
law of $x$ is **not** estimated: $f$ denotes the joint density of $(x,y)$ in which $x$ has its true law and $y$ given $x$
has the law above, and $f^*$ is the true joint density. Because $f$ and $f^*$ share the law of $x$,
$$
d_H^2(f,f^*)=E_x\Big[H^2\Big(N\big(\bar y+(x-\bar x)^\top\beta,\sigma^2\big),\ N\big(\alpha^*+x^\top\beta^*,\sigma_*^2\big)\Big)\Big],
$$
the squared Hellinger distance between the fitted and the true conditional laws of $y$ given $x$, averaged over $x$ (with
$x$ independent of the data). This is the joint-density distance of Song and Liang (2015), Theorems 1–2 (they use
$\int(\sqrt f-\sqrt{f^*})^2=2d_H^2$).

*Further notation.* $H^2(P,Q):=1-\int\sqrt{dP\,dQ}$ and $d_H(f,g):=\big(1-\int\sqrt{fg}\big)^{1/2}$. $P^*$ is the distribution
of the data. $\mathrm{sd}$, $\mathrm{Var}$, $\mathrm{Corr}$ are population standard deviations, variances and correlation
matrices; $z_j:=(x_j-Ex_j)/\mathrm{sd}(x_j)$ and $z:=(z_1,\dots,z_{p_{\mathrm{raw}}})$; $x_T$ is the sub-vector of $x$ indexed by a
set $T$; $|S|$ is the number of predictors in $S$; $a\vee b:=\max(a,b)$; $\log$ is the natural logarithm.

*Constants, level and window.* $s\ge0$ is an integer and $A\ge1$, $L\ge1$, $c_\psi>0$, $\bar b>0$ are constants; none depends
on $n$. The reader fixes a **level** $M\ge1$ (a larger $M$ gives a larger ball and a smaller exceptional probability). The
**window** is
$$
q_n:=\min\big\{p_{\mathrm{raw}},\ \lceil C_qM\log n\rceil\big\},\qquad C_q:=2\big(s(A+2)+4\big)/\log 2 ,
$$
the largest number of predictors that (A3) and (A4) constrain jointly (of order $\log n$ for a fixed level).

### Assumptions
- **(A1) Gaussian linear model.** $y=\alpha^*+x^\top\beta^*+\varepsilon$ with $\varepsilon\sim N(0,\sigma_*^2)$, $\sigma_*^2>0$,
  independent of $x$ ($\alpha^*$, $\beta^*$, $\sigma_*$ and the law of $x$ may depend on $n$).
- **(A2) Sparsity and dimension.** At most $s$ coordinates of $\beta^*$ are nonzero, and $2\le p_{\mathrm{raw}}\le n^A$.
- **(A3) Sub-Gaussian predictors on sparse directions.** Every predictor has positive variance, and for every
  $u\in\mathbb R^{p_{\mathrm{raw}}}$ with at most $q_n$ nonzero entries and every $\lambda\in\mathbb R$:
  $E\exp(\lambda u^\top z)\le\exp\big(L^2\lambda^2\,\mathrm{Var}(u^\top z)/2\big)$.
- **(A4) No near-exact collinearity.** $\lambda_{\min}(\mathrm{Corr}(x_T))\ge c_\psi/n$ for every set $T$ of at most $q_n$
  predictors.
- **(A5) Bounded signal.** $|\beta^*_j|\,\mathrm{sd}(x_j)\le\bar b\,\sigma_*$ for every $j$.

No lower bound on the nonzero coefficients (no beta-min condition) and no fixed lower bound on eigenvalues is assumed:
under (A4) predictors may be correlated up to $1-c_\psi/n$.

### Reader statement
**Theorem 9 (distribution-level consistency).** There are constants $c>0$, $C_1$, $M_0$ and $n_0$, depending only on
$(s,A,L,c_\psi,\bar b)$, such that the following holds. Fix a level $M\ge M_0$ and assume (A1)–(A5) with the window $q_n$
of this $M$. Then for every $n\ge n_0$ with $\sqrt n/\log n\ge M$:
$$
\text{(i)}\quad P^*\Big[\,\Pi\Big(d_H(f,f^*)>\sqrt{M\log n/n}\ \Big|\ D_n\Big)>n^{-cM}\Big]\le n^{-cM}.
$$
*In words.* Except on data sets of probability at most $n^{-cM}$, the posterior gives probability at most $n^{-cM}$ to
draws whose conditional law of $y$ given $x$ is farther than $\sqrt{M\log n/n}$ from the true one in Hellinger distance
averaged over $x$: the posterior contracts at the rate $\sqrt{\log n/n}$.

*Level-M form.* The same constants serve every level $M$ with $M_0\le M\le\sqrt n/\log n$, which may depend on $n$:
whenever $n\ge n_0$ and (A1)–(A5) hold with the window $q_n$ of this $M$, display (i) holds, and also
$$
\text{(ii)}\quad P^*\Big[\,\Pi\big(|S|>s+C_1M\ \big|\ D_n\big)>n^{-cM}\Big]\le n^{-cM}.
$$
The two exceptional sets of data sets can be taken to be the same set, and the bounds are uniform over all laws of the
data that satisfy (A1)–(A5) with the given constants. Statement (ii) bounds the number of selected predictors; it does
not say that they are the true ones.

*Without (A4).* If (A4) is dropped and (A3) is required only for single predictors ($u$ with one nonzero entry), then
$$
\text{(iii)}\quad P^*\Big[\,\Pi\Big(d_H(f,f^*)>\sqrt{M\log n\cdot\log(p_{\mathrm{raw}}\vee n)/n}\ \Big|\ D_n\Big)>n^{-cM}\Big]\le n^{-cM},
$$
and (ii) holds with $s+C_1M\log n$ in place of $s+C_1M$.

**Theorem 9B (parametric rate when the true predictors are detectable).** Assume (A1)–(A5) with the window $q_n$ of $M=1$,
with exactly $s\ge1$ nonzero coordinates of $\beta^*$, and in addition
- **(A6) Detectable signal.** (a) $\lambda_{\min}(\mathrm{Corr}(x_T))\ge\psi$ for a constant $\psi>0$ and every set $T$ of
  at most $(2A+3)s+2$ predictors; (b) $\min\{|\beta^*_j|\,\mathrm{sd}(x_j)/\sigma_*:\beta^*_j\neq0\}\ge b_n$, where $b_n>0$ and
  $b_n^2n/\log n\to\infty$.

Then for every sequence $M_n\to\infty$: $\ \Pi\big(d_H(f,f^*)>M_n/\sqrt n\ \big|\ D_n\big)\to0$ in $P^*$-probability.

**Corollary 9C (the output of the sampler).** The method explores the models with a sequential Monte Carlo sampler; it
does not compute the full posterior (small problems that it solves by exact enumeration are not covered here). A run is
*completed* when the method reports the status "completed"; runs that stop early are not covered. The output of a
completed run contains a list $\mathcal T$ of at most $40p+1$ distinct models: the best-scoring models among those offered to
the final run of the sampler (the models scored in that run, together with models scored earlier and carried into it:
the precomputed tables for small groups of predictors and the models kept from the calibration stage). Each model in the
list comes with the logarithm of its unnormalised posterior weight, taken to be computed in exact arithmetic. The output
contains no draws of $(\beta,\sigma^2)$. This description of the output was code-checked by independent reviewers. Let $\pi(\mathcal T)$ be the posterior probability of the list, and let $\hat\Pi$ (not
computed by the method) be the posterior restricted to the list: the models in $\mathcal T$, weighted in proportion to the
exponentials of their returned log-weights, each with its exact conditional posterior of $(\beta,\sigma^2)$. Under the
conditions of Theorem 9 (level-M form), with $P^*$-probability at least $1-n^{-cM}$ over the data, **every** completed run
(whatever its random numbers) with $\pi(\mathcal T)\ge n^{-cM/2}$ satisfies
$$
\hat\Pi\Big(d_H(f,f^*)>\sqrt{M\log n/n}\Big)\le n^{-cM/2}.
$$
If a completed run scored the true model $\{j:\beta^*_j\neq0\}$ and the posterior probability of that model exceeds $\tfrac12$,
then the list contains it, it is the model the method reports as most probable, and $\pi(\mathcal T)>\tfrac12$. Whether
the list carries enough posterior probability is a property of the run: the corollary does not assert it, and the output
does not certify it.

*Example.* Jointly Gaussian predictors satisfy (A3) with $L=1$; independent predictors satisfy it when each satisfies it
with a common constant $L$. (A4) holds for all large $n$ whenever every $q_n\times q_n$ principal block of the correlation
matrix has smallest eigenvalue at least a fixed $\psi>0$, for instance correlation $\rho^{|j-k|}$ with $|\rho|<1$, or equal
correlation $\rho\in[0,1)$.

*Conditions, in words.* Theorem 9 and Corollary 9C concern the exact posterior and need no further input; Corollary 9C
takes the returned log-weights to be computed in exact arithmetic, and its description of the output was code-checked by
independent reviewers. Theorem 9B also uses the posterior-concentration theorem (Theorem 1), which makes the posterior
select the true model. The sampler's delivery statements (that a completed run has found and kept the true model), which
Corollary 9C does not use, rest in addition on the premises of the sampler results (as for Theorem 10) and on exact
arithmetic.

### Placements (HQ card 13)
- **Abstract: display (i) only**, at a fixed level: *"If the rows are i.i.d., the response follows a Gaussian linear model
  with at most $s$ nonzero coefficients among at most $n^A$ predictors, the predictors are sub-Gaussian on sparse
  directions, no group of $O(\log n)$ predictors is nearly collinear (smallest correlation eigenvalue at least $c_\psi/n$),
  and each predictor's standardised signal is bounded, then for every fixed level $M\ge M_0$ and all large $n$, except on data sets of
  probability at most $n^{-cM}$, the posterior gives probability at most $n^{-cM}$ to conditional laws of the response
  given the predictors that are farther than $\sqrt{M\log n/n}$ from the true one in Hellinger distance averaged over the
  predictors — with no beta-min condition and no fixed lower bound on eigenvalues."*
- **Body:** the level-M form, (ii), (iii), Theorem 9B, Corollary 9C, and the remark of card row 2.2.

### Comparison with Song and Liang (2015), Theorems 1–2
Page and equation numbers are those of the published paper (J. R. Statist. Soc. B 77, 2015).
- **The analogue is display (i).** Their distance is $d(f_1,f_2)=\{\int\!\!\int(f_1^{1/2}-f_2^{1/2})^2\,dx\,dy\}^{1/2}$ between
  joint densities of $(x,y)$ that share the law of $x$ (§2.1.2, p. 952), so $d^2=2d_H^2$: the same distance. Their
  display (15) (Theorem 1, p. 952; Theorem 2 states the same form, p. 953) reads
  $P^*[\pi\{d(f,f^*)>\varepsilon_n\mid D_n\}>\exp(-c_1n\varepsilon_n^2)]<\exp(-c_1n\varepsilon_n^2)$; display (i) has this form
  with $n\varepsilon_n^2=M\log n$ (and $d_H$ in place of $d$).
- **Stronger.** (1) The prior is the one the method uses, with no tuning. Their theorems assume independent
  Bernoulli$(r_n/P_n)$ inclusion with a hard cap $|\xi|\le\bar r_n$ on the model size and conditions (9)–(14)
  (pp. 951–953), which the method's beta-binomial prior with cap $\min(p,\lfloor n/2\rfloor)$ does not meet. (2) The radius
  is a constant times $\sqrt{\log n/n}$. At polynomial $p$ their Theorem 2 (p. 953) needs $\bar r_n\log n=o(n\varepsilon_n^2)$
  with $\bar r_n\ge r_n\to\infty$ (and their (14)), so $n\varepsilon_n^2/\log n\to\infty$; their Corollary 1 (p. 954) gives
  $\varepsilon_n=O\{n^{-(1-\alpha)/2}\log^{k/2}n\}$. In display (i) the radius constant does not depend on $s$, and the
  smallest level $M_0$ grows at most linearly in $s$ (in the general form of the theorem, where the in-sample signal
  energy and coefficient cost are bounded by fixed constants; under (A5) those bounds themselves grow with $s$).
  (3) Theorem 9B gives the parametric rate $M_n/\sqrt n$ and Corollary 9C covers the sampler's output at the coded budget;
  their posterior results give no parametric rate, and their statements on the sampler's output are limits in the number of iterations at fixed data, for every data set (supplement pp. 9–10, 12–13, 16–17); ours hold at the coded budget under design conditions (and, for Corollary 9C, given that the returned list carries posterior mass at least $n^{-cM/2}$); neither implies the other [AUD-S4]. (4) No lower bound on the growth of $p$ is needed; they
  assume $P_n\succ n^\theta$ (p. 950).
- **Weaker.** (1) $p_{\mathrm{raw}}\le n^A$; their Corollary 1 allows $P_n<\exp(Cn^\alpha)$. (2) Exact sparsity; their
  Theorem 1 covers approximate sparsity (their (3): $\lim_n\sum_j|\beta^*_j|<\infty$, with predictors bounded by 1), under
  which the number of nonzero coefficients may grow. (3) $s$ is fixed, with constants depending on $s$; their Theorem 2
  also has a true model of bounded size (their (4), p. 950), so this is weaker only against their Theorem 1. (4) (A4) is
  a condition on the design that their Theorems 1–2 do not have (their eigenvalue conditions, (11) and (14), are on the
  prior covariance).
- **Not the analogue: display (iii)**, the fallback without (A4). Its radius is larger by $\sqrt{\log(p_{\mathrm{raw}}\vee n)}$,
  so its exponent is $c\,n\varepsilon_n^2/\log(p_{\mathrm{raw}}\vee n)$, not $c\,n\varepsilon_n^2$; and, as proved, in the general form
  of the theorem (in-sample signal energy and coefficient cost bounded by fixed constants), its squared radius at the
  smallest admissible level is at most of order $(1+s)^3\log n\log(p_{\mathrm{raw}}\vee n)/n$ for fixed $s$ (an upper bound;
  the proof is not known to be tight in $s$); under (A5) those bounds themselves grow with $s$.
- **Different, not ranked:** tail conditions on the predictors — (A3) and (A5) here; theirs are $|x_i|\le1$ (Theorem 1),
  Condition 1 (an exponential-moment bound on averages of at most $\bar r_n$ predictors, Theorem 2, p. 953) and
  Condition 2 (second moments, for their limit form (16), p. 954).
- **Overall: incomparable** — stronger on the prior, the rate and the coded output; weaker on the range of $p$, on
  approximate sparsity and, for display (i), by (A4).

### Why each assumption
- (A1) It is the model under which the method's likelihood is correct; it gives the posterior a closed form given the
  predictors. $\sigma_*$ is free because rescaling the response leaves the posterior over models unchanged and rescales the
  posterior of $(\beta,\sigma^2)$.
- (A2) Posterior model size is controlled relative to $s$; the constants depend on $s$ and $A$.
- (A3) Only to make the sample variances of the predictors and the sample covariances of small groups of predictors track
  their population values with probability $1-n^{-cM}$. The passage from the sample to the population distance uses no
  tail condition.
- (A4) It keeps in force the prior's penalty for each extra predictor (a factor of order $n^{-1/2}$); this gives the rate
  $\sqrt{\log n/n}$, the level $n^{-cM}$ and the bounded model size. Without it the radius gains the factor
  $\sqrt{\log(p_{\mathrm{raw}}\vee n)}$ (display (iii)). Whether it is needed for the rate $\sqrt{\log n/n}$ is open.
- (A5) It bounds the signal in units of the noise and excludes huge coefficients that cancel.
- (A6) (Theorem 9B only) It makes the posterior select the true model, which removes the logarithm.

### Master theorem
W3-DIST reader versions (`Theory_work/Wave3/W3-DIST/STATEMENT.md` v1.4.10, §1R :126-269); H5 card 13 AGREED; recorded on
main cb642afd (rule e7a7216c). Statuses verbatim from `Theory_work/INFRA/registry/claims.tsv` at cb642afd [REG-cb64]; versions `@1.0.2` and the Cor-C and DIST-C conditions as at main 20d01e52 (HQ D111; at 2676e71f they were "conditional on W1-N1:B, W1-N1:F, EX-A"):
- Theorem 9 (display (i), level-M form, (ii), (iii)) = `W3-DIST:Thm-A` (:185-207; = DIST-1 (1.1) + bridges B0, B1, B2; the
  sentence without (A4) = DIST-2 (1.2) + B0, B1): `W3-DIST:Thm-A@1.0.2` **"PROVED-CHECKED; council R2, MANIFEST 9719c817… (= R2 c5cd9cdd re-frozen CITATION-ONLY as R2r), astra=9.3 PASS, opus=9.2 PASS"**; masters
  `W3-DIST:DIST-1@1.0.2`, `W3-DIST:DIST-2@1.0.2` the same.
- Theorem 9B = `W3-DIST:Thm-B@1.0.2` (:209-215): **"PROVED-CHECKED; council R2, MANIFEST 9719c817… (= R2 c5cd9cdd re-frozen CITATION-ONLY as R2r), astra=9.3 PASS, opus=9.2 PASS"**; bridge
  `W3-DIST:B3@1.0.2` **"PROVED-CHECKED, conditional on W3-POST:Thm-1 (for its last sentence); …"**.
- Corollary 9C = `W3-DIST:Cor-C@1.0.2` (:217-238): **"PROVED-CHECKED, conditional on EX-A (exact arithmetic); council R2, MANIFEST 9719c817… (= R2 c5cd9cdd re-frozen CITATION-ONLY as R2r), astra=9.3 PASS, opus=9.2 PASS"**.
  DIST-C's delivery statements (not used by 9C): `W3-DIST:DIST-C@1.0.2` **"PROVED-CHECKED, conditional on
  EX-A (exact arithmetic); council R2, MANIFEST 9719c817… (= R2 c5cd9cdd re-frozen CITATION-ONLY as R2r), astra=9.3 PASS, opus=9.2 PASS"**.

### Bridges
| # | bridge | mark | detail |
|---|---|---|---|
| B9.0 | renaming: DIST's $p$ ↦ $p_{\mathrm{raw}}$, $r$ ↦ $p$, (A3) constant $K$ ↦ $L$, $\sigma^*$ ↦ $\sigma_*$ | identity | to match `NOTATION.md` §1, §3 (there $K$ is the size cap) |
| B9.1 | Theorem 9 (i), (ii), the "same set" and uniformity sentences, the Example = W3-DIST Theorem A | identity (text) | STATEMENT :185-207 |
| B9.1a | fixed-level statement first, then the level-M form = Theorem A with $M$ constant, then as written (same constants, same $n_0$ for all $M\le\sqrt n/\log n$) | identity (reordering) | STATEMENT :185-191 (the constants, $n_0$ included, depend only on $(s,A,K,c_\psi,\bar b)$; the fixed-level form adds $M\le\sqrt n/\log n$ to $n\ge n_0$) |
| B9.2 | display (iii) = Theorem A's "Without (A4)" sentence written as a display (same level $n^{-cM}$, radius times $\sqrt{\log(p_{\mathrm{raw}}\vee n)}$) | identity (transcription) | STATEMENT :200-202 |
| B9.3 | Theorem 9B, Corollary 9C = W3-DIST Theorem B, Corollary C | identity (text; the mixture sentence of C shortened, no content dropped from the claim) | STATEMENT :209-238; "code-checked by independent reviewers": the output description rests on the code facts of STATEMENT §2 :273-287 (scores: W3-SAMP CC2, "CODE-CHECKED"), and Corollary C's reported-model conclusion was verified against the code by D3, the sweep and both council seats (CHECKPOINT_3 §4) |
| B9.4 | "$p=p_{\mathrm{raw}}$ outside the exceptional sets" | EXISTS-CHECKED (line-checked + council R2) | W3-DIST Setup :150-152 and bridge B1 :391-395 (on B1's event no column is dropped) |
| B9.5 | exponent in (iii): $cM\log n=c\,n\varepsilon_n^2/\log(p_{\mathrm{raw}}\vee n)$ at $\varepsilon_n^2:=M\log n\log(p_{\mathrm{raw}}\vee n)/n$ | VERIFIED (F9) | substitute $\varepsilon_n$ |
| B9.6 | Song–Liang sentences | checked against the paper: `reviews/SL_PDF_CHECK.md` | page / equation / theorem numbers there |
| B9.7 | "what is estimated": $d_H^2(f,f^*)$ = averaged conditional Hellinger distance; plug-in sample-mean intercept; law of $x$ not estimated | EXISTS (W3-DIST §0, council R2) | STATEMENT :42-52 |
| B9.8 | sparsity statements of the comparison: (i) radius constant free of $s$, level at most linear in $s$, in DIST-1's interface form; (iii) as proved, squared radius at most of order $(1+s)^3\log n\log(p_{\mathrm{raw}}\vee n)/n$ for fixed $s$ | EXISTS: (i) DIST-1 (c) :84-87 (TC3, checked D1, D5, both R2 seats); (iii) Dept RT1 (Sol) steps 4–11, W3-DIST `reviews/UNHARVESTED_STRENGTH.md` item 9 | interface form: energy and coefficient-cost bounds held fixed; under (A5) these bounds grow with $s$ (bridge B1 :391-395) |

### Honest limits
Statement (ii) bounds the size of the selected models, not their identity. Corollary 9C does not assert that a run's
list carries enough posterior probability, and the output does not certify it; runs that stop early and the exact
enumeration branch are not covered. Status: the masters' statuses above, with their conditions.

#### Update log (thm9)
- v0.1 2026-11-15: first version (CP1).
- v0.2 2026-11-15: S1 fixes none.
- v0.3 2026-11-16 (proposal, HQ card 13): placeholder → proved version from W3-DIST §1R (council R2 passed): setting,
  numbered assumptions (A1)–(A6), displays (i)–(iii), Theorems 9B and Corollary 9C, Song–Liang comparison (STRONGER:
  placeholder → theorem). F9 repairs to the card rows.
- v0.4 2026-11-16 (proposal, H5 card 13 AGREED): "what is estimated" (conditional law of $y$, Hellinger averaged over
  $x$; law of $x$ not estimated) replaces "joint distribution"; fixed-level display first, level-M form second; the
  Song–Liang analogue is display (i) only, (iii) is the fallback; sparsity statements per B9.8; "s fixed" added to the
  weaker list; every Song–Liang sentence checked against the paper; placements (abstract: display (i) only) (EQUAL on
  the theorems; presentation and comparison only).
- v0.4 applied 2026-11-16 [HQ card 13; recorder task W, main cb642afd]: variant A; statuses requoted verbatim from
  `claims.tsv` at cb642afd; "Conditions, in words" paragraph added (STRONGER: placeholder → theorem).
- FRZ-B 2026-11-16: [AUD-S4] Song–Liang comparison (3): their sampler-output statements are iteration limits at fixed data; ours at the coded budget; neither implies the other (W3-AUDIT TRACK_B v1.4.1) (EQUAL).
- FRZ-B 2026-11-16: requote at main 2676e71f [REG-2676] (relabel D97): W3-DIST @1.0.1 statuses (Thm-B unconditional; Cor-C, DIST-C conditional on W1-N1:B, W1-N1:F, EX-A); EQUAL (statuses only).
<!-- ROW thm9 END -->

---

## 10. Theorem 10 — The printed outputs are consistent (card row 3.6; row 3.5 as a remark)
<!-- ROW thm10 BEGIN -->
**Card row** 3.6 (and 3.5) · **Section version** 1.1 (2026-11-16) · **Pending delta** post-freeze rider SAMP-R1

### Reader statement
**Theorem 10.** Let the rows of $X^{\mathrm r}$ be i.i.d. $N_p(m_n,\Sigma_n)$ with $\Sigma_n$ a correlation matrix, and
$y^{\mathrm r}=\alpha\mathbf 1+X\theta^*+\varepsilon$ with a deterministic $\theta^*$. Assume
- **(A1) Model and method.** (S1), (S2), (S3), (S5); $p>s_0$.
- **(A2) Sparsity and fixed signals.** $s_0\ge1$ fixed; $\theta_{\mathrm{lo}}\le|\theta^*_j|\le\theta_{\mathrm{hi}}$ on $S_0$.
- **(A3) Population sparse eigenvalue floor.** $\lambda_{\min}(\Sigma_{n,S})\ge c>0$ for every $|S|\le5(A+1)(s_0+1)\log n$.
- **(A4) Visibility** and **(A5) no leakage**: (A4) and (A5) of Theorem 5.

*Which designs.* (A5) holds only for designs with no leakage outside the true model, such as independent predictors.
AR and block designs, where a null is correlated with a truth at a fixed level, are **not** covered. For those designs
Theorem 6 (row 3.1, the reported model is $S_0$) still applies under its own conditions, and the pooled evidence is
unbiased for every design (row 3.5, remark below); consistency of the printed PIPs, MPM and $\hat Z$ is not claimed
there [AUD-B11].

This theorem concerns the sampler branch of the method (the model space is too large to enumerate; the exact branch is
the scope note below) [S2-F3]. Let $\mathcal A$ be the event that the method takes the sampler branch and its calibration
succeeds (fallback ladder included); every completed sampler run lies in $\mathcal A$. On $\mathcal A$ let $\hat Z$,
$\widehat{\mathrm{PIP}}$, $\widehat{\mathrm{MPM}}$ denote the evidence estimate, pooled PIPs and their MPM computed from the
four islands' uninterrupted records (equal-weight pooling, `NOTATION.md` §5); on completed runs they are exactly the
printed fields, and $\hat S$ is the reported model. Let $\rho_n:=n^{-1/2}e^{C\sqrt{\log n}}$ for a suitable constant $C$
(so $\rho_n\le n^{-c}$ eventually, for every $c<\tfrac12$). Then, under the joint law of design, noise and the method's
random numbers,
$$
\mathbf 1_{\mathcal A}\Big(\big|\hat Z/Z-1\big|+\big|\log\hat Z-\log Z\big|+\max_{j}\big|\widehat{\mathrm{PIP}}_j-\mathbf 1\{j\in S_0\}\big|\Big)=O_P(\rho_n),
$$
$$
P\big(\mathcal A\cap\{\widehat{\mathrm{MPM}}\neq S_0\}\big)\to0,\qquad P\big(\text{the run completes and }\hat S\neq S_0\big)\to0 ,
$$
and the same rate holds for the printed fields multiplied by the indicator of a completed run. Here $Z$ is the exact
normalising constant. No lower bound on $P(\mathcal A)$ is asserted: the statements are about intersections with
$\mathcal A$ or with completion, not conditional on them. The guarantees describe the run as if uninterrupted; a run stopped by its time guard reports status `resource_limit` and returns no estimates; anything else it returns is flagged incomplete and is not covered (`v3_fit.R:84-85`; `v3_run.R:110-113, 142-147`) [B2]. [GUARD-W]

*Scope.* The exact-enumeration branch (small model spaces) is not covered by this theorem [S3-N3].

*Remark (row 3.5: the pooled evidence is unbiased).* Given the calibration, on $\mathcal A$, $E[\hat Z\mid\text{calibration}]=Z$
for every design and data set; no statistical condition is needed (claim `W3-READER:PoolZ@1.0.2`, `STATEMENT.md`, from the
per-island identity of the unbiasedness theorem by linearity). The guarantees describe the run as if uninterrupted; a run stopped by its time guard reports status `resource_limit` and returns no estimates; anything else it returns is flagged incomplete and is not covered (`v3_fit.R:84-85`; `v3_run.R:110-113, 142-147`) [B2]. [GUARD-W]

### Why each assumption
- (A2)–(A3) give posterior concentration (Theorem 2) and the start's small-set floor.
- (A4)–(A5) make the start law concentrate on $S_0$ as $n\to\infty$ (Theorem 5): asymptotically the sampler then has
  vanishing mass to transport and $\hat Z/Z\to1$, independently of the ladder length. (At moderate $n$ the posterior $\pi$
  had substantial mass on one-variable supersets of $S_0$ in the measured Engineering configurations — an observation
  (Theorem 1, remark (vii)), not a proved finite-$n$ statement.) [ENG-D17, S3-N9, R1-F3]
  This is the regime of the result; an alternative route with no condition on $\hat Z$ (a global-overlap condition)
  exists for the PIPs, MPM and HPM (remark).
- (S5) idealises the random numbers and the coded kernels; they are not statistical assumptions.

### Master theorem
`W3-SAMP:C@1.1.6`, `Theory_work/Wave3/W3-SAMP/STATEMENT.md:149-163`, clause (C-v) at :158-162, status **"PROVED-CHECKED; council R1, MANIFEST 68480a72…, astra=9.1 PASS, opus=8.8 PASS"**
(main 20d01e52, W1-N1:B/F discharge, HQ D111; at main 2676e71f it was "PROVED-CHECKED, conditional on W1-N1:B, W1-N1:F") [REG-2676, REG-20d0]; `W1-N1:B`, `W1-N1:F` (formerly the conditions) each **"PROVED under the named premises of STATEMENT §2 — cross-family checked (Codex gpt-6.1-sol: LC1, MP1 CONTINUE, SW1, council C1 9.3) and council-passed (Claude Opus 5.5: C1 8.9), round 1, 2026-11-08."**;
start input `W3-START2-R:IF-START@1.0.0` (IF-START⁺⁺, `W3-START2-R/STATEMENT.md:241-246`, under (T3⁺⁺)(b) at :226-240 with (L-R⁺⁺) at
:70-81), **"PROVED-CHECKED; council R2, MANIFEST 12bb52cd… (= R2 90886d06 re-frozen CITATION-ONLY as R2r), sol=9.0 PASS, opus=9.3 PASS"** (main b48fd0a1; supersedes `W3-START2:IF-START`, free, SUPERSEDED-VALID) [REPIN]; posterior input Theorem 2
(`W3-POST:Thm-1@1.0.1` item 6 with `W2-APP:POST@1.0.7`, "PROVED-CHECKED"). Alternative
route (remark): `W3-SAMP:TR@2.1.6`, "PROVED-CHECKED; council R1, MANIFEST 68480a72…, astra=9.1 PASS, opus=8.8 PASS" [REG-2676]. Row 3.5: `W1-N1:Thm-N1@1.0.0`,
"PROVED-CHECKED", and `W3-READER:PoolZ@1.0.2` "PROVED-CHECKED; council R3, MANIFEST 7aebdf2e…, sol=9.5 PASS, opus=9.4 PASS".

### Bridges
| # | Bridge | Mark | Detail |
|---|---|---|---|
| B10.1 | (A2)–(A3) ⇒ $o_1=O_P(\sqrt{\log n/n})$ | via Theorem 2: EXISTS-CHECKED (`W2-APP:POST@1.0.7`) + R1 (B2.1) | `lemmas/R4_printed_outputs.md` step (1); standardised-signal convention covered by `L1_POST.md:11, 15-18`. |
| B10.2 | (A3)–(A5) ⇒ $\mathbf 1_{\mathcal A}o_0=O_P(\rho_n)$ | EXISTS-CHECKED + R1 (B6.1) | IF-START⁺⁺ under (T3⁺⁺)(b) with $Q=S_0$; (A4)–(A5) = (V-R), (L-R⁺⁺) with $\bar H_n=e^{\kappa\sqrt{\log n}}$ (Theorem 5, B5.1′) [REPIN]. |
| B10.3 | $\mathbf 1_{\mathcal A}\max(o_0,o_1)=O_P(\rho_n)$ ⇒ (C-v) with rate $\rho_n$ | **NEW** (assembly) | `lemmas/R4_printed_outputs.md` steps (3)–(4). |
| B10.4 | pooled $\hat Z$ unbiased | **NEW** (claim) | `W3-READER:PoolZ@1.0.2`, two-line proof from N1. |

### Honest limits
The conclusion is localised to calibration success $\mathcal A$ on the sampler branch (intersections, not conditioning);
that $P(\mathcal A)\to1$ is not claimed here (under (S4), whose item (i) now includes IDEAL-W⁺, completion holds for every
admissible $n$, and without the two limits lifted on $\mathfrak D$; that link is not used here) [S4-S1, RM2R-1]. The theorem covers only designs with no leakage outside the true model (A5), such as independent predictors; AR and
block designs are outside it (row 3.5 applies there, and row 3.1 for particular AR or block designs that satisfy Theorem 6's
conditions) [AUD-B11, R2-L1]. The rate $\rho_n$ is the start law's rate;
its ratio to the posterior rate $\sqrt{\log n/n}$ is $e^{C\sqrt{\log n}}/\sqrt{\log n}$ [R2-E2]. Registry conditions: since main 20d01e52 (HQ D111) `W3-SAMP:C@1.1.6` and `W3-READER:R4@1.0.3` carry no condition on W1-N1:B, W1-N1:F (at main 2676e71f [REG-2676] they were "PROVED-CHECKED, conditional on W1-N1:B, W1-N1:F"; the two
N1 premises remain "PROVED under the named premises", cross-family checked and council-passed); `W2-APP:POST` is "PROVED-CHECKED".

#### Update log (thm10)
- v0.3 2026-11-16: first version (manager's CP1 decision 4; bridge leg).
- v0.4 2026-11-16: [ENG-D17] "why" line reworded: concentration is asymptotic; moderate-$n$ mixture noted (EQUAL).
- v0.5 2026-11-16: [S2-F2] (S5) carries the full sampler contract; [S2-F3] sampler-branch scope, potential estimates on
  $\mathcal A$, printed fields on completion. Tags (S3): **WEAKER** (restores `W1-N1/STATEMENT.md:73-86`,
  `W3-SAMP/STATEMENT.md:29-41, 64-70, 90-95, 186`).
- v0.6 2026-11-16: [S3-N1] (S5) restores "independent of the data" for the final-run streams (`W3-SAMP/STATEMENT.md:39-41`;
  undoes v0.5's accidental STRONGER part); [S3-N3] the exact-branch remark (a new claim, STRONGER) is withdrawn and
  replaced by a scope note "not covered"; [S3-N9] moderate-$n$ note about $\pi$ only; [S3-N8] START and KERNEL
  statuses quoted separately. Net tag vs S2-frozen: **WEAKER** (master premises restored).
- v0.7 2026-11-16: [REG-f526] `W3-SAMP:C/TR` and `W2-APP:POST` statuses refreshed (conditional on C-PACK:SL0, SOP:TH09) (EQUAL).
- v0.8 2026-11-16: [REG-33e1] SL0 cleared: `W3-SAMP:C/TR` @1.1.3/2.1.3 and `W2-APP:POST@1.0.6` conditional on SOP:TH09 only (EQUAL).
- S4 2026-11-16 [S4-S1]: the completion remark in the honest limits follows the F-UNI narrowing (on $\mathfrak D$ under
  (S4)(i)–(iv); every $n$ under A:IDEAL-W⁺; WEAKER, unused link).
- v0.9 2026-11-16: [AUD-B11] (HQ 11-16, from W3-AUDIT CHECKPOINT_1, theory/W3-AUDIT 81291dd9, TRACK_B.md B11) scope of
  (A5) stated plainly: no leakage outside the true model, such as independent predictors; AR and block designs not
  covered; rows 3.1 and 3.5 named for them. Presentation only (EQUAL; the statement already names (A5)).
- v1.0 2026-11-16: [REPIN] start input repinned `W3-START2:IF-START` → `W3-START2-R:IF-START@1.0.0` (free supersession,
  main b48fd0a1); B10.2 reads IF-START⁺⁺ under (T3⁺⁺)(b). Tag **STRONGER**: since the row 3.3 swap (Theorem 5 v0.3,
  a33d890d) (A5) here is (L-R⁺⁺) with reference sets up to $e^{\kappa\sqrt{\log n}}$, which only the new master covers (the old
  one needs (L-R⁺), polylogarithmic sets). The rate $\rho_n$ and the conclusions are unchanged. [RM2R-1] the completion
  remark refers to (S4) as amended (EQUAL).
- FRZ-RQ 2026-11-16: [REG-6cd6] `W3-SAMP:C/TR` @1.1.4/2.1.4 and `W2-APP:POST@1.0.7` "PROVED-CHECKED"; no open registry condition (R4, PoolZ unchecked). Statuses only (EQUAL).
- v1.1 2026-11-16: [GUARD-W] (HQ YES 11-16; W3-AUDIT track A T1 GUARD-W, theory/W3-AUDIT 58e24245, `track_A/T1_GW/`) sentence added to Theorem 10 and to the row 3.5 remark: "The guarantees describe the run as if uninterrupted; a run stopped by its time guard reports status `resource_limit` and no output." Presentation (EQUAL).
- R1 2026-11-16: [R1-F3] moderate-$n$ parenthesis relabelled an observation (WEAKER).
- R2-ED 2026-11-16: post-council editorial items [R2-E2] exact rate ratio, [R2-L1] AR/block pointer as in card row 3.6 (EQUAL).
- FRZ-B 2026-11-16: [B2] GUARD-W wording (Theorem 10 and row 3.5 remark); [R3-O1] comma splice fixed (EQUAL).
- FRZ-B 2026-11-16: requote at main 2676e71f [REG-2676] (relabel D97): `W3-SAMP:C@1.1.5` and `W3-READER:R4@1.0.1` conditional on W1-N1:B, W1-N1:F (these are now registry conditions of row 3.6; the earlier "no open registry condition" is superseded); `TR@2.1.5`, PoolZ@1.0.1; EQUAL (statuses only).
<!-- ROW thm10 END -->

---

## Summary of bridges (v0.3)

| Bridge | Theorem | Mark | Where proved | Importance |
|---|---|---|---|---|
| B2.2 `W2-APP:POST@1.0.7` | 2, 6, 10 | EXISTS-CHECKED | accepted at W2-APP CP3; SL0 cleared (main 33e1f0f5); SOP:TH09 discharged (main 6cd699dd) | none |
| B4.3 / B1.7 POST2 C/E/A1/A0 | 1 (re-base), 1′, 4 | EXISTS-CHECKED, conditional (A0 unconditional; §1) | recorded at main f526e45b; @1.0.7 after main 33bfcb9c | conditions quoted in §1 (C, E, A1: W2-APP:POST; A0 unconditional) [S4-F1, REG-6cd6, REG-33bf] |
| B6.6′ / B7.5 (S4) ⇔ delivery premises (D) of `W3-RM2-R:DLV-0` | 6, 7 | identity | `W3-RM2-R/STATEMENT.md:71-93` | low |
| B6.6 / B7.4 RM2 ⇒ delivery assembly; (S4) premise table — **historical** (former hypotheses; not used by current 6, 7) [R1-F2] | — | NEW | `lemmas/R3_delivery_assembly.md` | — |
| B6.3 local regressions ⇒ variance clause | 6 (7: B7.3) | NEW | `lemmas/R2_local_regression.md` | medium |
| B1.1–B1.3, B2.1, B3.2, B4.1, B6.1 set sizes and elementary bridges | 1, 2, 3, 4, 6, 10 | NEW | `lemmas/R1_set_sizes.md` | medium |
| B10.3 printed outputs assembly | 10 | NEW | `lemmas/R4_printed_outputs.md` | high (row 3.6) |
| B10.4 pooled evidence unbiased (`W3-READER:PoolZ@1.0.2`) | 10 (row 3.5), card 4.1 | NEW (registered claim, approved) | `STATEMENT.md` | medium |
| B6.7 raw-scale coefficients in Theorems 5, 6, 10 | 5, 6, 10 | NEW (optional) | not proposed | low–medium |

All NEW items are covered by the bridge leg's one Sol line check, together with the v0.1 → v0.3 diff of the reader
statements. The CP3 council's Sol seat gives the fresh `FIDELITY: FAITHFUL | NOT-FAITHFUL` line on the final reader
statements (HQ-confirmed; no separate review).

---

## 11. Additions of H5 card 17 (2026-11-17; consultant AGREED; D115, D120, D121)

These blocks are appended here so that the line numbers of §§1–10 stay unchanged. They belong to the reader versions of Theorem 2 (§2), Theorem 6 (§6) and card rows 1.2, 3.1L and 3.1F. Update-log entries are in §2 (v0.5) and §6 (v1.0).

### 11.1 Theorem 2X (coexisting statement under Theorem 2; tag MIXED / incomparable; conditional)
**Source:** W3-D2 READER_DELTA (text) and `W3-D2/REPORT.md` §3 (card text). Statuses verbatim (recorded at main 2e0decc8; `Thm2X@1.0.3`, status as at main 34c8fb4d) [REG-2e0d]: `W3-D2:Thm2X@1.0.3`, `W3-D2:Cor2X@1.0.0`: **"PROVED-CHECKED, conditional on W2-APP:POST, C-MIS:GDb, C-MIS:Prop-P; council R2, MANIFEST d408b7dc…, sol=9.2 PASS, opus=9.6 PASS"** (each).

**Theorem 2X (smaller-set, expectation form).** Let the rows of $X^{\mathrm r}$ be i.i.d. $N_p(m,\Sigma)$ with $\Sigma_{jj}>0$, and let $R$ be the correlation matrix of a row. Assume (S1) with $\sigma^2>0$ allowed to depend on $n$ and
- **(A1) Dimension and sparsity.** $2\le p\le n^A$; $s_0\ge1$ fixed.
- **(A2) Sparse eigenvalue floor.** $\lambda_{\min}(R_{TT})\ge c$ for every $T$ with $1\le|T|\le3(A+1)(s_0+1)\log n$, for a fixed $c>0$.
- **(A3) Signal relative to the noise.** $\beta^\top\Sigma\beta\le M_0\sigma^2$ and $n\min_{j\in S_0}\Sigma_{jj}\beta_j^2/(\sigma^2\log n)\to\infty$.

$m$, $\Sigma$, $\beta$ and $\sigma^2$ may depend on $n$; no condition beyond (A1)–(A3) is placed on how they vary. Then
$$E\big[1-\pi(S_0\mid y)\big]=O\Big(\sqrt{\tfrac{\log n}{n}}\Big),\quad P(\mathrm{HPM}\neq S_0)+P(\mathrm{MPM}\neq S_0)=O\Big(\sqrt{\tfrac{\log n}{n}}\Big),\quad E\max_j|\mathrm{PIP}_j-\mathbf 1\{j\in S_0\}|=O\Big(\sqrt{\tfrac{\log n}{n}}\Big).$$
It is conditional on `W2-APP:POST`, `C-MIS:GDb` and `C-MIS:Prop-P` (the inputs of Theorem 4's master), as recorded.

*Remarks.* Fixed $\sigma^2$, a correlation matrix $\Sigma$ and $b_{\mathrm{lo}}\le|\beta_j|\le b_{\mathrm{hi}}$ on $S_0$ give (A3) with $M_0=s_0^2b_{\mathrm{hi}}^2/\sigma^2$. This is Theorem 4 with no omitted predictors, plus the deterministic PIP/MPM consequences. Against Theorem 2: it asks the floor on smaller sets and lets the parameters vary with $n$, but needs Gaussian rows and gives an expectation form; Theorem 2's sub-Gaussian rows are not covered, and Theorem 2's fixed parameters are not required here.

**Bridges.** B2.1′ := `W3-D2:Thm2X` (`W3-MISR-R:CorGb-plus` with $q=0$ and `W3-READER:R1` B4.1); B2.1″ := `W3-D2:Cor2X` (the old hypotheses ⇒ the new ones). B2.1–B2.3 stay for the coexisting statement of §2.

### 11.2 Corollary 6L (what the returned list gives) — recorded (W3-D5P)
Presented as a software statement once the code re-pin to method-v3.1.1-listpip is recorded. Source: `theory/W3-D5P` (CARD.md v0.3 Option A, READER_DELTA v0.2). Master, recorded: `W3-D5P:LIST-R@1.0.0` "PROVED-CHECKED; council R4, …" (unconditional: IMPL-LIST discharged at `method-v3.1.1-listpip`, main 7100bb3b, `W3-D5P/reviews/IMPL_LIST_codeprint.md` §5); `W3-D5P:LIST-K@1.0.0` "PROVED-CHECKED; council R4, …"; `W3-D5P:LIST-CODE@1.0.0` "CODE-CHECKED (code reading at core 4676af6); council R4, …". Inputs: `W3-RM2-R:RM2-R-plus@1.0.1`, `RM0-plus@1.0.1`, `DLV-0@1.0.1` "PROVED-CHECKED; council R3, …"; `W2-APP:POST@1.0.7` "PROVED-CHECKED".

**Corollary 6L.** A run that produces output returns, besides the reported model, a list of at most $40p+1$ distinct models with their unnormalised log posterior weights (the best-scored models met by the run). The method prints three further summaries. On a run that uses the sampler they are computed from this list: the inclusion probabilities $\hat p^{\,\mathrm{list}}_j$ of the posterior renormalised to the list, their median model $\hat S^{\mathrm{list}}=\{j:\hat p^{\,\mathrm{list}}_j>\tfrac12\}$ and the list evidence $\hat Z^{\mathrm{list}}$ (the sum of the list's weights). On a small problem solved by exact enumeration they are the exact inclusion probabilities, the exact median model and, where it is printed, the evidence of the enumeration's list. Write $\varepsilon_n:=1-\pi(S_0\mid y)$. Under the assumptions of Theorem 6, on the same data events $\mathcal G_n$, every run that produces output, whatever its seed and calibration outcome, reports $\hat S=S_0$ and has $S_0$ in its list (on the sampler; on exact enumeration, in the enumeration's list where it is returned), and
$$
\max_j\big|\hat p^{\,\mathrm{list}}_j-\mathbf 1\{j\in S_0\}\big|\le\varepsilon_n,\qquad
\max_j\big|\hat p^{\,\mathrm{list}}_j-\mathrm{PIP}_j\big|\le\varepsilon_n,\qquad
1-\varepsilon_n\le\hat Z^{\mathrm{list}}/Z\le1\ \ \text{(where }\hat Z^{\mathrm{list}}\text{ is printed)},
$$
so that $0\le\log Z-\log\hat Z^{\mathrm{list}}\le-\log(1-\varepsilon_n)$; and $\hat S^{\mathrm{list}}=\hat S=S_0$ when $\varepsilon_n<\tfrac12$. When $p\ge2$ for all large $n$, $\varepsilon_n=O_P(\sqrt{\log n/n})$, so the two PIP errors and the log-evidence error $|\log\hat Z^{\mathrm{list}}-\log Z|$ (where printed) are $O_P(\sqrt{\log n/n})$ on output, and without "on output" under the delivery conventions (S4).

*Remark.* This covers every design inside Theorem 6, including AR and block designs that satisfy Theorem 6's conditions, on which the sampler's averaged PIPs, median model and evidence are not covered (Theorem 10 needs no leakage outside the true model). The list quantities are deterministic functions of the run's output; they speak about the posterior restricted to the list, which on Theorem 6's data event holds at least the mass of $S_0$. *Relation to Corollary 9C (D121):* 6L supplies Cor 9C's list-mass premise pathwise on the part of the stated event where $\pi(S_0\mid y)\ge n^{-cM/2}$ (there the list holds at least that mass); the probability form under Cor 9C's law needs the raw-scale bridge (open). Tag vs Theorem 6: **STRONGER** (added conclusions, same hypotheses and event). Cor 9C's status is unchanged.

### 11.3 Corollary FAMC (block and AR designs whose true coefficients do not cancel)
`W3-FAMC:Cor-FAMC@1.0.0`, main 8b4d3101 [REG-8b4d], status verbatim **"PROVED-CHECKED; council R5, MANIFEST b32ee9df…, sol=10.0 PASS, opus=9.5 PASS"**. Reader text (verbatim, `Theory_work/Dept/writing_answers/FAMC_NOTE_2026-11-17.md` on dept/theory; checked for faithfulness against `Theory_work/Wave3/W3-FAMC/STATEMENT.md` §1):

> **Corollary (block and autoregressive designs).** In the setting of Theorem 6, suppose that, for all large n, the predictors are correlated either in independent blocks of bounded size (uniformly well conditioned) or autoregressively with a fixed ρ ∈ (−1, 1), and that a fixed number of true coefficients have absolute values bounded away from 0 and ∞.
> Suppose also that the true predictors cannot cancel one another. One of the following holds:
> - one true predictor per block;
> - signs aligned with the correlation. For AR: equal signs if ρ > 0, and signs alternating with the column index if ρ < 0. For a block with several truths: after flipping some columns' signs, all its partial correlations are ≥ 0 and the flipped true coefficients share one sign;
> - (AR only) the truths are spread apart by an explicit separation bound;
> - the coefficient vector stays a fixed distance from a closed set B of cancelling directions. B is null for AR designs, and possibly not null for general block designs.
>
> Then, on data events of probability tending to one, every admissible run that returns a result reports exactly the true model, whatever its seed. Under Theorem 6's delivery conventions, every run returns a result with probability one. So the true model is recovered with probability tending to one, with Theorem 6's qualifications (lifted integer limits, bounded domain, time guard).
> Not covered: coefficients that cancel. For example, two adjacent autoregressive true predictors with coefficients 1 and −2 at correlation 0.5.

It is an assembly of recorded results (Lemma VIS, TRACK_B B9/B10, RM2 E2, C-GROW); it changes no theorem and adds no assumption. Every condition is class 2b (typical designs), supported by class-2a lemmas (`W3-FAMC/STATEMENT.md` §2). For block and AR designs whose true coefficients do not cancel, it replaces Theorem 6's (A3)–(A6) by primitive conditions. It covers every fixed AR correlation $\rho\in(-1,1)$; the constants degrade as $|\rho|\to1$ (`W3-FAMC/STATEMENT.md` §1b(iv)).
