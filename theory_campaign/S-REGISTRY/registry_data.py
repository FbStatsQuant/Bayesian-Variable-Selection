# -*- coding: utf-8 -*-
"""Claims registry data (S-REGISTRY). One row per named result.

Field conventions
  st   author-stated status: PROVED | PROVED-UNDER | PROOF SKETCH | COUNTEREXAMPLE | CONJECTURE | OPEN | REFEREE
       (PROVED-UNDER = author wrote "PROVED given/under <named inputs>"; REFEREE = repair or counterexample supplied by
        a cross-family referee without a PROVED label.  Statuses are copied, never upgraded.)
  sf   same-family verification   "CODE|text"   CODE in V (VERIFIED), V* (VERIFIED after repair / with qualification),
       G (GAP), E (ERROR), N (none)
  cf   cross-family verification  "CODE|text"   same codes (A-REV1 / A-REV2 only)
  rs   repair state when sf/cf is G or E: none | applied | pending   (pending = awaits W6-FIXREV1 / W6-FIXREV2, not landed)
  kind result | claim (flagged sub-claim, not counted among named results)
"""

ROWS = []


def r(id, tgt, src, st, sf, cf, rep, prem, mean, kind="result", rs="none", flags=""):
    ROWS.append(dict(id=id, tgt=tgt, src=src, st=st, sf=sf, cf=cf, rep=rep, prem=prem, mean=mean,
                     kind=kind, rs=rs, flags=flags))


N = "N|none"

# ---------------------------------------------------------------------------------------------------------------
# W1-T03R / W2-VT03R / A-REV2  (Theorem 1)
# ---------------------------------------------------------------------------------------------------------------
S03 = "W1-T03R · REPORT.md"
V03 = "W2-VT03R · REPORT.md verdict table"
A2 = "A-REV2 · REVIEW.md §2"

r("E1", "Thm 1 (T02 lemma)", S03 + " §1 · Lemma E1", "PROVED",
  "V|" + V03 + " rows 1–4, VERIFIED (exact rational check, 2,779 triples)", "V|" + A2 + " S03 Lemma E1(a)–(d) VERIFIED",
  "none needed", "p ≥ 2; (c) needs s₀ ≥ 1, m ≤ K−1",
  "The BB(1,p) model-size prior is exactly geometric with ratio (p−i)/(2p−1−i); the per-model 1/p penalty is cancelled by the C(p,k) multiplicity, so the tail beyond m is explicit.")
r("E2", "Thm 1 (T02 lemma)", S03 + " §1 · Lemma E2", "PROVED",
  "V|" + V03 + " rows 6–7, VERIFIED", "V|" + A2 + " S03 Lemma E2(i)–(iii) VERIFIED",
  "none needed", "s₀ ≥ 1 (or s₀ = 0 with n ≥ 5)",
  "The exact-tail cutoff m♯ is at most min(K, old cutoff) and has a closed-form bound of order s₀ log n.")
r("E3-T03", "Thm 1 (T02 lemma)", S03 + " §1 · Prop. E3", "PROVED",
  "V|" + V03 + " row 8, VERIFIED", "V*|" + A2 + " S03 Proposition E3 VERIFIED, only as a barrier for this cutoff/envelope route",
  "none needed", "Scope: Markov-numerator / S₀-denominator technique only",
  "Any size-tail bound of the T02(i) form needs a cutoff at least ≈ s₀ log n above s₀; the technique cannot do better (not a posterior lower bound).")
r("den′", "Thm 1 (T02 lemma)", S03 + " §2 · Lemma den′", "PROVED",
  "V|" + V03 + " row 9, VERIFIED", "V|" + A2 + " S03 den′ and T02(i♯) VERIFIED (constant c♯ = κ²/(c_IG σ²), no stray 4)",
  "none needed", "G, R", "The locked denominator lemma, kept before the S₀ prior lower bound is inserted, so the exact class ratio R_m can be factored out.")
r("T02(i♯)", "Thm 1", S03 + " §1 · Theorem T02(i♯)", "PROVED",
  "V|" + V03 + " row 10, VERIFIED", "V|" + A2 + " S03 den′ and T02(i♯) VERIFIED; quantifier is sup_m P(Θ>L), not P(sup_m Θ>L)",
  "none needed", "G, R; cutoff must be deterministic", "Posterior mass on models larger than m♯ is O_P(e^{−ω_n}) with explicit non-asymptotic constants.")
r("LemmaI-B", "Thm 1", S03 + " §1 · Lemma I (interlacing), Lemma B (B1–B3)", "PROVED",
  "V|" + V03 + " row 13, VERIFIED (9,000 random pairs)", "V|" + A2 + " S03 Lemmas I/B VERIFIED",
  "none needed", "fixed g₀ > 0 (g₀,n → 0 not covered)", "Anchored eigenvalue conditions on S₀∪J are equivalent (by interlacing) to conditions on every set with ≤ m columns outside S₀.")
r("T02(ii♯)", "Thm 1", S03 + " §1 · Theorem T02(ii♯)", "PROVED",
  "V|" + V03 + " row 14, VERIFIED", "V|" + A2 + " S03 Lemmas I/B and T02(ii♯) VERIFIED",
  "none needed", "R1, G, R, SE_w(m♯; g₀)", "Posterior mass on strict supersets of S₀ is O_P(√(log n/n)) under unnormalised non-degeneracy alone.")
r("T03♯", "Thm 1", S03 + " §1 · Theorem T03♯ (i)–(v)", "PROVED",
  "V|" + V03 + " rows 12, 15–26, VERIFIED; no GAP/ERROR in the mathematics", "V|" + A2 + " S03 T03♯(i)–(v) VERIFIED under exactly its fixed-design, fixed-s₀ hypotheses",
  "none needed (finite-n disclosure sentence replaced: thresholds ≈ 2·10⁶, not 1.2·10⁵; see flagged claim T03-1.2e5)",
  "R1, G, R, SE_λ(j₀), SE_w(m♯; g₀), BM-∞ or BM(c>c₀); fixed s₀; asymptotic only; proof thresholds n ≳ 2·10⁶; beta-min constant ≥ 43× above executed signals",
  "Selection consistency: 1−π(S₀)=O_P(√(log n/n)), PIPs and MPM consistent, HPM error ≤ 2E₀δ₁ → 0, under anchored sparse-eigenvalue and beta-min conditions.")
r("PropD-T03", "supplement (negative result)", S03 + " §1 · Prop. D", "COUNTEREXAMPLE",
  "V|" + V03 + " row 11, VERIFIED (reproduced analytically and numerically)", "V|" + A2 + " S03 Proposition D VERIFIED (G and R only; violates even size-two SE)",
  "none needed", "Scope: G and R alone, duplicated columns", "With duplicated columns the posterior size-tail does not vanish at cutoff s₀+O(1): the target 'm_n = s₀+O(s₀ log n/log p)' is false without SE.")
r("PropD′-T03", "Thm 1 (remark)", "W2-VT03R · REPORT.md §2 · Prop. D′", "PROVED",
  "N|authored by W2-VT03R (the verifier); no second same-family check", "N|A-REV2 §3.5 restates it without a verdict row",
  "none needed", "T03♯ hypotheses", "Under T03♯ the posterior mass above size s₀ is at most 1−π(S₀), so the large cutoff is an artefact of the SE-free Markov route.")
r("LemmaA1", "Thm 1 (remark)", "W2-VT03R · REPORT.md §2 · Lemma A1", "PROVED",
  "N|authored by W2-VT03R (the verifier)", "N|A-REV2 §3.3 states the same equivalence without a verdict row",
  "none needed", "—", "'Anchored' SE is equivalent to the unanchored condition on every column set up to s₀ columns: anchoring is cosmetic, the real savings are the cutoff and normalisation.")
r("PropW-SIG", "Thm 1 (optional weakening)", "W2-VT03R · REPORT.md §2 · Prop. W", "PROOF SKETCH",
  "N|authored by W2-VT03R", "N|not in A-REV2's table", "none needed", "SIG(c) direct signal-separation condition; (iv) per-coordinate version unwritten",
  "SE_λ(j₀)+beta-min can be replaced by unnormalised SE plus a direct signal-separation condition.")

# ---------------------------------------------------------------------------------------------------------------
# W1-T37R / W3-VT37R / A-REV2  (Theorem 3, part A)
# ---------------------------------------------------------------------------------------------------------------
S37 = "W1-T37R · REPORT.md"
V37 = "W3-VT37R · REPORT.md verdict table"
r("Prop1-TD", "Thm 3 (negative result → supplement)", S37 + " §2 · Prop. 1", "PROVED",
  "V|" + V37 + " row 1, VERIFIED (720 designs, literal TD(2,0) in 0/720)", "V|" + A2 + " S37 Proposition 1 and swap identity VERIFIED",
  "none needed", "s₀ ≥ 1, d ≥ 1, s₀+1 ≤ K", "The literal truth-dominance condition TD(d,m) is self-contradictory for every d ≥ 1: at S₀−j+l the swap l→j and the addition of j cannot both behave as T37 requires.",
  flags="retires literal T37")
r("V1-TDfails", "Thm 3 (negative result → supplement)", "W3-VT38E · REPORT.md §3.4 · Prop. V1", "PROVED",
  "N|authored by W3-VT38E (the verifier)", "N|A-REV1 does not itemise it; A-REV2 verifies the related Prop. 1",
  "none needed", "s₀ ≥ 1, p ≥ s₀+1, s₀+1 ≤ K", "On T03's own event {π(S₀) > ½} literal TD(d,m) fails for every d ≥ 1 and every m, in every design (proxies play no role).")
r("Lemma0(a,c)", "Thm 3", S37 + " §2 · Lemma 0 (a),(c)", "PROVED",
  "V|" + V37 + " rows 2, 2e, VERIFIED", "V|" + A2 + " S37 Lemma 0(a),(c) VERIFIED (initial-centre-is-truth case trivial)",
  "none needed", "EX-A; completed scans", "The local search only climbs strictly; if it stops certified at S₀, every model it scored is ≤ S₀, so the reported best is S₀ without any π(S₀)>½ premise.")
r("Lemma0(b)", "Thm 3", S37 + " §2 · Lemma 0(b)", "PROVED",
  "G|" + V37 + " rows 2b/2c/2d: inclusion VERIFIED; 'in particular on every posterior miss' ERROR (CEX-2); repaired by W3-VT37R R2",
  "E|" + A2 + " §4.2: 'Lemma 0(b) as written' ERROR (post-search competitor ≠ initial beat); V37 R2 repair also ERROR",
  "W3-VT37R R2 (itself ERROR per A-REV2); A-REV2 three-way partition F_pre/F_post proposed — W6-FIXREV2 PENDING", "per-fit F(S₀)−F(S_c) data for the 541 fits still unextracted (OPEN)",
  "A new delivery of S₀ by the final search is possible only if S₀ is unscored and beats the pre-search best; the extra claim that every miss is a posterior miss does not follow.",
  rs="pending", flags="CONFLICT")
r("Lemma2-T37", "Thm 3", S37 + " §2 · Lemma 2", "PROVED",
  "V|" + V37 + " row 3, VERIFIED (193 designs)", N, "none needed", "—", "Progress moves keep the lattice region closed; under NA∧TL, S₀ is a local max and extras are deleted first.")
r("Lemma3-T37", "Thm 3", S37 + " §2 · Lemma 3", "PROVED",
  "V|" + V37 + " row 4, VERIFIED", N, "none needed", "SE on S∪S₀", "At a state missing truths the best truth-addition gain is bounded below by a Schur-complement/Cauchy–Schwarz argument.")
r("TheoremA", "Thm 3 (Theorem A)", S37 + " §2 · Theorem A (A1)–(A4)", "PROVED",
  "V|" + V37 + " rows 5–8, VERIFIED (720 designs × 632 states, 0 violations; 'ℓ ≥ a+d is sufficient, exact need is τ(S_c)')",
  "V*|" + A2 + " S37 Theorem A(A1)–(A4) VERIFIED; A4 necessity must keep its quantifier; 'ℓ ≥ a+d' sufficient not necessary",
  "none needed for A1–A4 (A5(a) separate)", "EX-A; finite family 𝓡; production tie-broken greedy map",
  "Finite-n exact result: the production local search repairs from every centre iff the greedy path stays in the region and ends at S₀; path length τ = m+e−#swaps ≤ Φ.")
r("A5(b)", "Thm 3", S37 + " §2 · Theorem A (A5) second implication", "PROVED",
  "V|" + V37 + " row 10, VERIFIED (TD′_∞ in 198/200, TD′_P in 0/200 at n=3000)", "V|" + A2 + " S37 TD′_P ⇒ TD′_∞; converse fails VERIFIED",
  "none needed", "region closure", "TD′_P implies TD′_∞; the converse fails (combination-proxy example).")
r("R1-POS", "Thm 3", "W3-VT37R · REPAIRS.md · R1", "PROVED",
  "N|authored by W3-VT37R (the verifier)", "V|" + A2 + " §4.1 POS repair VERIFIED", "this is a repair",
  "positivity clause POS on the designated move", "Adding a positive-gain clause makes strict literal dominance imply TD′_P at d = 0 (it cannot rescue the contradictory d ≥ 1 premise).")
r("ThmB-T37(incl)", "supplement (finite-n union bound)", S37 + " §2 · Theorem B (inclusions and union bound)", "PROVED",
  "V|" + V37 + " row 12, VERIFIED (R6: headline '2^Φ states, no 2^{s₀}' only for a data-independent centre)", "V|" + A2 + " S37 Theorem B union-bound use VERIFIED; response-selected centre needs a covering class",
  "R6 wording (W3-VT37R) applied; random-centre wording pending W6-FIXREV2", "data-independent class 𝒞 ⊆ R_{a,d}; ℓ ≥ max Φ",
  "Search failure probability is at most the sum of: centre outside the class, NA/TL failure, and per-lattice-state one-step dominance failures — a union bound with no 2^{s₀} factor.", rs="pending")
r("ThmB-T37(events)", "supplement", S37 + " §2 · Theorem B (form of each single event)", "PROOF SKETCH",
  "V|" + V37 + " row 12 (ridge O(1/n) correction owed)", "N|not separately reviewed", "none", "ridge correction O(1/n) unstated", "Each single comparison is a ≤ 4-dimensional non-central event given an independent χ² (exact only without the ridge).")
r("ThmC-C1", "Thm 3 (asymptotic, superseded by W3-PGD)", S37 + " §2 · Theorem C (C1)", "PROOF SKETCH",
  "G|" + V37 + " rows 13–13c: TL sketch plausible; NA_d containment miscomputed; exceptional nulls unfinished; repaired at sketch level (R4)", "G|" + A2 + " Theorem C extensions GAP; V37 R4 printed expression ERROR (see flagged R4-excess)",
  "W3-VT37R R4 (sketch); W6-FIXREV2 PENDING", "LD* strengthened dependence premise; plain union needs p^d = o(√(n log n))",
  "TL_d holds w.p. → 1; NA_d holds under a local-dependence condition on the nulls.", rs="pending")
r("ThmC-C2", "Thm 3 (asymptotic, superseded by W3-PGD)", S37 + " §2 · Theorem C (C2)", "PROOF SKETCH",
  "G|" + V37 + " row 14: noise-variance inequality ERROR (201× and 1,896× violations); repaired at sketch level (R5)", "G|" + A2 + " V37 R4/R5 remain sketches; no asymptotic TD′ theorem upgraded",
  "W3-VT37R R5 (sketch); W6-FIXREV2 PENDING", "PGD(η); uniform log-linearisation with ridge term (owed)", "Under PGD, TD′_P holds w.p. → 1 on R_{a,d}.", rs="pending")
r("C3-PGD", "Thm 3 (negative result → supplement)", S37 + " §2 · Theorem C (C3)", "COUNTEREXAMPLE",
  "V|" + V37 + " row 15, VERIFIED (exact population values R⁺=0.090, R⁰=0.130)", "V|" + A2 + " §4.1 combination-proxy example independently reproduced",
  "none needed", "—", "SE and beta-min do not imply progress-greedy dominance: a null that looks like a combination of two truths is added first.")
r("C4", "Thm 3", S37 + " §2 · Theorem C (C4)", "CONJECTURE", "N|" + V37 + " row 16, not assessed beyond EXP3-R consistency", N, "none", "bounded number of regressive null additions",
  "Without PGD the uncapped path still reaches S₀ on a slightly enlarged region.")
r("CEX1", "supplement (negative result)", "W3-VT37R · REPORT.md §4.1 · CEX-1", "COUNTEREXAMPLE",
  "V|authored by W3-VT37R; reproduced in-run", "V|" + A2 + " §4.1 independently reproduced (gain −2.2977998984)", "none needed", "—",
  "At d = 0 literal strict TD can hold while the best addition from ∅ has negative gain: positivity is missing, so the original T37(i) is false even at d = 0.")
r("CEX2", "supplement (negative result)", "W3-VT37R · REPORT.md §4.2 · CEX-2", "COUNTEREXAMPLE",
  "V|authored by W3-VT37R; production rerun 233/234", "V|" + A2 + " §4.2 independently reproduced (−2.2862503005, +7.2109846558)", "none needed", "—",
  "A search can start below S₀, climb to a superset and certify it: a final-search failure does not imply the initial centre already beat S₀.")
r("CEX-ties(A2)", "supplement (negative result)", "A-REV2 · REVIEW.md §4.3", "COUNTEREXAMPLE",
  "N|none (found by the cross-family referee)", "V|A-REV2 (author)", "this is a finding; fix = W6-FIXREV2 PENDING", "—",
  "With duplicate columns (exact ties) TD′_P holds but the strict-separation event D_S fails: D_S is sufficient, not necessary.", rs="pending")
r("CEX-localmax(A2)", "supplement (negative result)", "A-REV2 · REVIEW.md §4.2", "COUNTEREXAMPLE",
  "N|none (found by the cross-family referee)", "V|A-REV2 (author)", "this is a finding; fix = W6-FIXREV2 PENDING", "—",
  "A suppressor design (and a production-table-compatible variant) ends certified at an inferior local maximum: failures of delivery are not exhausted by 'posterior miss' or 'never in E_LS'.", rs="pending")

# ---------------------------------------------------------------------------------------------------------------
# W1-EXP / W3-VEXP / A-REV2  (Theorem 2)
# ---------------------------------------------------------------------------------------------------------------
SE = "W1-EXP · REPORT.md"
VE = "W3-VEXP · REPORT.md verdict table"
r("EXP′", "Thm 2 (ii)", SE + " §Refined · Thm 1", "PROVED",
  "V|" + VE + " rows 1–5, VERIFIED (reproduced at p=8–24, n up to 1.6·10⁶)", "V*|" + A2 + " SEX Theorem 1 VERIFIED (exact expansion and bound); limiting constant 0.52 → 0.51 (flagged claim EXP-const)",
  "constant correction pending W6-FIXREV1/2; finite-n certificate R1-cert replaces κ_EXP at the study size", "G, R-lite(A,M), SE-blk; fixed X; uniform over a polynomial family; κ_EXP ≈ 100–1,700 nats at study SNR",
  "Every within-block log-Bayes-factor addition equals −½log(n+1) − ν·log(1−x) plus a bounded remainder, with an explicit deterministic bound, on an event of probability → 1.")
r("R1-cert", "Thm 2 (ii)", "W3-VEXP · REPAIRS.md · R1", "PROVED",
  "N|authored by W3-VEXP (the verifier)", "V|" + A2 + " VEX R1 data-computable EXP′ certificate VERIFIED", "this is a repair", "SE-blk on realised blocks; y ∉ span X_{C_b}",
  "A data-computable remainder bound (0.59–1.52 nats on study-like designs) holds at any n, replacing the vacuous κ_EXP.")
r("Thm2-BO", "Thm 2 (iii)", SE + " §Refined · Thm 2 (favourable regime, BO)", "PROOF SKETCH",
  "V|" + VE + " row 10 and REPAIRS R2: verbatim corollary of locked T22(iii), 'no step remains open'; author label left as PROOF SKETCH", N,
  "none", "G, R, SE-blk, BO, BM-blk", "In the block-orthogonal benchmark the start puts mass → 1 near the truth: 1−π₀(S₀)=O_P(2^B√(log n)n^{−1/2}).")
r("Prop2.1-2.2", "Thm 2 (iii)", SE + " §Refined · Props. 2.1/2.2", "PROOF SKETCH",
  "V|" + VE + " rows 7–8, VERIFIED", N, "none", "—", "The leakage hypothesis NL_η weakens to NL_C and the reference S₀ may be any feasible S° (support of θ* never used).")
r("Lemma2.3", "Thm 2", SE + " §Proofs · Lemma 2.3", "PROVED", "V|" + VE + " row 9, VERIFIED", N, "none needed", "—", "Block leakage bounds the discrepancy, and visibility follows from block gain.")
r("Thm6-EXP", "Thm 2 (iii)", SE + " §Refined · Thm 6", "PROVED",
  "V|" + VE + " row 11, VERIFIED (flat √n(1−π₀(S°)) ≈ 1.6)", N, "none needed", "G, R-lite, SE-blk, ZL(S°), SPREAD, VIS-lin(S°)", "Under exact zero leakage the start concentrates near a reference S° (favourable if S°=S₀, masked if not) at rate 2^B n^{−1/2}.")
r("Thm3-EXP", "Thm 2 (iv)", SE + " §Refined · Thm 3", "PROVED",
  "V|" + VE + " row 12, VERIFIED (needs a deterministic chain)", "V|" + A2 + " SEX Theorem 3 VERIFIED (1.01 multiplier valid for n ≥ 400; not for a response-selected chain)",
  "none needed", "fixed deterministic chain, bounded chain leakage CL(L)", "Along a chain of single additions with bounded leakage the start-table ratio law is two-sided: ≈ n^{−1/2} up to an O_P(1) factor.")
r("Thm4-EXP", "Thm 2 (iv)", SE + " §Refined · Thm 4", "PROVED",
  "V|" + VE + " row 13, VERIFIED", "V|" + A2 + " SEX Theorem 4 (fixed CL, normalised H3) VERIFIED", "none needed", "H3 (π₀ of the chain's first set ≥ c₀ w.p. → 1) stays an explicit premise",
  "Under bounded chain leakage the start mass of S₀ is p^{−c}n^{−c/2}e^{O_P(1)} (T27(i) from checkable inputs).")
r("Thm4-growL", "Thm 2 (iv)", SE + " §Refined · Thm 4 (growing L_n)", "PROVED",
  "V|" + VE + " row 13 (wording)", "V|" + A2 + " §5.3 growing-leakage bound VERIFIED as sufficiency", "none needed", "bound is sufficient only", "With growing leakage the upper multiplier gains e^{O(L_n²)}; masking persists when η < 1/2.02.")
r("LimitLaw", "Thm 2 (iv)", SE + " §Refined · limit law of the masking statistic", "PROOF SKETCH",
  "V|" + VE + " row 14, VERIFIED as sketch", "N|A-REV2 §5.3: remains a sketch; needs convergence of v or subsequences", "none", "signal variance v convergence", "The masking statistic converges in law to a constant plus (L+Z)²σ²/(2v).")
r("Lemma4.1-4.2", "Thm 2 (v)", SE + " §Proofs · Lemmas 4.1–4.2 (LH algebra, partition = groups)", "PROVED",
  "V|" + VE + " rows 16–17, VERIFIED; |ψ|<ρ boundary sharp in effect", N, "none needed", "|ψ| < ρ; g ≤ B < 2g", "In the linked-hub family the method's partition equals the groups, so the cancelling hubs sit in different blocks.")
r("Thm5-LH", "Thm 2 (v)", SE + " §Refined · Thm 5 (a)(b)(c)(e) [+ (d) by locked T03]", "PROVED",
  "V|" + VE + " rows 18–21, VERIFIED (config A/B reproduced)", N, "none needed", "exact Gram (p ≤ n−1); |ψ|<ρ; g ≤ B < 2g; fixed coefficients",
  "One explicit family is masked at the start (π₀(S₀)=p^{−c}n^{−c/2}e^{O_P(1)}) while the start still concentrates on S₀∖M and the posterior concentrates on S₀.")
r("R3-LHiid(VEXP)", "Thm 2 (v)", "W3-VEXP · REPAIRS.md · R3", "PROOF SKETCH",
  "N|authored by W3-VEXP", "G|" + A2 + " VEX random-design / actual-packing extensions GAP (fixed-surrogate sound in its restricted regime)", "none", "uniform LLN for VIS-lin unwritten; B ≥ 2g packing GAP",
  "iid-Gaussian LH: on the event 'blocks = groups' the partition is fixed and null/masked residuals have an exact Beta law, giving the start rate with √(log n).", rs="pending")
r("PropD-dilution", "supplement (n=200 disclosure)", "W3-VEXP · REPAIRS.md §D · Prop. D", "PROVED",
  "N|authored by W3-VEXP", N, "none", "truths alone in their block", "A deterministic ceiling π₀(S₀) ≤ prior factor × ∏BF({j}) explains the study's dilution masking at n = 200.")
r("DilThreshold", "supplement (n=200 disclosure)", "W3-VEXP · REPAIRS.md §D", "PROOF SKETCH",
  "N|authored by W3-VEXP (numerically confirmed)", N, "none", "population limit", "A truth enters the start mode only if (n/2)log(1/(1−θ²/v)) ≳ log((2p−s₀)/s₀)+½log n; no signal scale removes the masking at fixed n.")
r("InSample-fav", "Thm 2 (relevance)", "W3-VEXP · REPORT.md row 24", "CONJECTURE",
  "N|W3-VEXP: 'G (not fixable here)'; empirically true, high confidence", N, "none", "partition–noise decoupling for ≥ 2 groups per block",
  "For iid S1/S3/S4/S6 the start is favourable in-sample once n ≳ 800–1600.")
r("WeakSignal", "none (retired)", SE + " §Needs escalation 3", "CONJECTURE",
  "E|W3-VEXP row 27 and W3-PXN Prop. W: 'evidence against' (wrong mechanism; dilution, L² ≈ 50–200)", N, "retired in favour of dilution", "—",
  "W1-EXP's guess that the study's n = 200 start masking is weak-signal masking with bounded leakage; rejected by both W3 runs.", flags="retired claim")

# ---------------------------------------------------------------------------------------------------------------
# W2-PREM / A-REV1 / A-REV2  (Theorem 3 supplement: premises of Theorem B)
# ---------------------------------------------------------------------------------------------------------------
PR = "W2-PREM · REPORT.md"
r("IND-T", "supplement (Thm B′/B♯)", PR + " §1 · Theorem IND-T", "PROVED",
  "N|authored by W2-PREM; no same-family verifier", "V*|A-REV1 §5: VERIFIED for the uninterrupted process (stopping-time argument); completion conditioning / fresh-score sets not covered",
  "none needed", "EX-S, EX-A; H′ = L+5 rounds after the last resampling", "Terminal trajectories of different particles are conditionally independent even though the engine reads one shared random stream.")
r("LemmaU-PREM", "supplement (premise table; shares proof with EXP′)", PR + " §3 · Lemma U", "PROVED",
  "N|authored by W2-PREM; no same-family verifier",
  "V*|A-REV1 §3.4/§5 finite uniform expansion VERIFIED; A-REV2 §6 (U) VERIFIED on an explicitly budgeted family (extra-set quantifier GAP; limit constant ERROR; C3 lower bound ERROR — see flagged claims)",
  "W6-FIXREV1 (constant) and W6-FIXREV2 (family budget, C3 lower bound) PENDING", "SE on every set of the family; deterministic family of size ≤ n^{A′}; L > 4A′",
  "A uniform log-Bayes-factor expansion with explicit remainder holds simultaneously over any polynomial family of bounded-size additions (EXP′ is its within-block instance).", rs="pending")
r("C3-upper", "supplement", PR + " §3 · Lemma U, C3 zero-leakage upper bound", "PROVED",
  "N|authored by W2-PREM", "V|" + A2 + " §2 SU C3 zero-leakage upper bound VERIFIED", "none needed", "residual floor", "At zero leakage the log-odds of adding a null is at most Z²/2 plus bounded terms.")
r("PropT2-PREM", "supplement", PR + " §3 · Prop. T2", "PROVED", N, N, "none", "SE(s₀+a+2), BM-∞", "Truth removal at supersets by Gibbs, uniform swap or neighbour swap has super-polynomially small probability.")
r("NL0(0)/UDEL(1)", "supplement", PR + " §2 table · NL0(0), UDEL(1)", "PROVED", N,
  "N|A-REV1 §4 notes W2-PREM §0 correctly redefines NL0 as the sum of suprema (no verdict row)", "none", "—", "Leakage at S₀ itself and single-extra deletability are O_P(log n/√n) with no design condition.")
r("NL0(a)/UDEL(a≥2)", "supplement", PR + " §2 table", "PROVED-UNDER", N, N, "none", "partner-graph condition PG(a); false without it (see EQ)", "Superset leakage and multi-extra deletability decay under bounded partial-correlation degree.")
r("EQ", "supplement (negative result)", PR + " §3 · Counterexample EQ", "COUNTEREXAMPLE", N, N, "none", "equicorrelated nulls, p = n^β, rβ > ½", "With equicorrelated nulls NL0(1) fails and ε_del(2) → 1 even though G, R, SE, BM-∞ hold.")
r("B1′-PREM+PA", "supplement", PR + " §4 · Prop. B1′, Prop. PA", "PROVED", N, N, "none", "pointwise addability (proved under SE, BM-∞)", "Phase-1 progress holds with constant ≥ 1/|M(x)| from pointwise addability alone, so BTP is unnecessary.")
r("TS", "supplement", PR + " §6.1 · TS", "PROVED-UNDER", N, N, "none", "coefficient non-cancellation TS(𝒲); COUNTEREXAMPLE under a cancellation pair", "Gibbs truth removal at incomplete states is negligible only without cancellation.")
r("FS/TL♯/ULR", "supplement", PR + " §6.2–6.4", "PROVED-UNDER", N, N, "none", "FS(D′,c₀)+p/log n→∞; ZJL+CS(g₀); ULR(c₀); random designs OPEN", "Swap-truth removal, junk additions and look-alike retention are controlled under explicit conditions.")
r("FamilyDefect", "supplement (negative result)", PR + " §5.1", "COUNTEREXAMPLE", N, N, "fix = Theorem B♯", "LH family", "W1-T24G's repair family built from the neighbour graph has O(1) exit probability on LH (useless look-alikes).")
r("ThmB♯", "supplement (Thm B′/B♯)", PR + " §5.2 · Theorem B♯", "PROVED", N, N, "none", "monotone look-alike map; closure (F3) flagged for review", "Theorem B holds with a repaired start-adapted family built from a monotone look-alike map (proof device).")
r("IND-M", "supplement", PR + " §7 · Prop. IM / IND-M", "PROVED-UNDER", N, N, "none", "SCR(S°)+GS(S°), starts x ⊇ S°; superset starts OPEN", "Independence-proposal bad acceptance is o_P(1/log n) when the start concentrates on a subset reference.")
r("TheoremL", "supplement", PR + " §8 · Theorem L", "PROOF SKETCH", N, N, "none", "two finite population inequalities only numerical (config B)", "On LH exact Gram every premise of Theorem B♯ holds (all but two numerical population inequalities proved).")
r("CorA-PREM", "supplement", PR + " §9 · Corollary A", "PROVED-UNDER", N, N, "none", "premises of the table", "Under the premise table sup over eligible starts of P(S₀ unscored in L+5 rounds) → 0.")

# ---------------------------------------------------------------------------------------------------------------
# W1-T24G / W2-VT24G / A-REV1  (Theorem 4 route (e′) / supplement)
# ---------------------------------------------------------------------------------------------------------------
S24 = "W1-T24G · REPORT.md"
V24 = "W2-VT24G · REPORT.md verdict table"
A1 = "A-REV1 · REVIEW.md §2"
r("ThmB-T24", "supplement (Thm B′/B♯); Thm 4 route (e′)", S24 + " §1 · Theorem B (restated T24)", "PROVED",
  "V*|" + V24 + " rows 'Theorem B': VERIFIED after Lemma F′ repair", "V*|" + A1 + " Theorem B, restated T24, finite inequality VERIFIED after F′ repair; statistical application remains GAP",
  "Lemma F′ applied (W2-VT24G); boundary conventions (H=0, a=0, c*≤0) to W6-FIXREV1 — PENDING", "EX-A, EX-S, SR, φ=1, H terminal rounds without resampling, s₀+a ≤ K; usefulness asymptotic only (vacuous at n=200)",
  "A particle near the truth fails to score S₀ within H terminal rounds with probability ≤ P(Bin(H,c*) < v) + Hη, with no factorial; replaces the false H24 input of T21 route (e).", rs="pending")
r("LemmaF", "supplement", S24 + " §1 · Lemma F", "PROVED",
  "V*|" + V24 + " row Lemma F: GAP (closure hypothesis) fixed by F′", "V|" + A1 + " Lemma F as a standalone first-failure lemma VERIFIED; W1's use in B2 slot argument GAP repaired",
  "F′ (W2-VT24G)", "closure of the family under non-failure (not satisfied in two uses)", "A union bound over first-failure steps, valid when non-failing steps stay in a family.", rs="applied")
r("LemmaF′", "supplement", "W2-VT24G · REPORT.md §3 · Lemma F′", "PROVED",
  "N|authored by W2-VT24G (the verifier)", "V|" + A1 + " Lemma F′ VERIFIED", "this is a repair", "—", "The first-failure union bound with no closure hypothesis, via a permutation bijection.")
r("LemmaO", "supplement", S24 + " §1 · Lemma O", "PROVED", "V|" + V24 + " Lemma O VERIFIED", "V|" + A1 + " Lemma O(i)–(iii) VERIFIED", "none needed", "—", "Order facts for the uniformly random label order of one round.")
r("LemmaC", "supplement", S24 + " §1 · Lemma C", "PROVED", "V|" + V24 + " Lemma C VERIFIED (exact rational check)", "V|" + A1 + " Lemma C and the block bound VERIFIED", "none needed", "—", "Adapted binomial domination: P(Bin(H,c) < v) ≤ v(1−c)^{⌊H/v⌋}.")
r("LemmaP", "supplement", S24 + " §1 · Lemma P", "PROVED", "V|" + V24 + " Lemma P VERIFIED", "V*|" + A1 + " Lemma P exact formula and single-target bound VERIFIED; informal multi-target sentence GAP (explicit version supplied)",
  "A-REV1's explicit multi-target bound → W6-FIXREV1 draft landed (CONSOLIDATED.md, unreviewed)", "—", "Exact first-change progress probability within one round, integrated over the target's arrival time.", rs="pending")
r("PropU", "supplement", S24 + " §1 · Prop. U (undo)", "PROVED",
  "V|" + V24 + " Prop. U VERIFIED as bookkeeping ('it only relocates the problem into η')", "E|" + A1 + " Proposition U as written ERROR (independence moves can remove a truth; extra-for-extra swap can leave the phase-1 family)",
  "corrected classification — W6-FIXREV1 draft landed (CONSOLIDATED.md, unreviewed); Theorem B unaffected (uses the full §0 'bad' definition)", "—",
  "Every undo of Gibbs progress is either 'bad' (charged to η) or neutral (charged to the slot term); the printed shortcut equivalence drops the truth-removal alternative.", rs="pending", flags="CONFLICT")
r("PropB1-B2", "supplement", S24 + " §1 · Props. B1, B2", "PROVED",
  "V|" + V24 + " Prop. B1 VERIFIED; B2 VERIFIED after F′", "V*|" + A1 + " B1 VERIFIED; B2 VERIFIED after F′", "F′ applied", "—", "Per-round progress constants: phase 1 (add a missing truth) and phase 2 (delete extras, c₂ ≥ 1/(B+3) − ε_del).")
r("B1′/B2′-VT24G", "supplement", "W2-VT24G · REPORT.md §3 · Props. B1′/B2′ (Theorem B′)", "PROVED",
  "N|authored by W2-VT24G (the verifier)", "V|" + A1 + " B1′/B2′ scoring refinements VERIFIED with empty-supremum convention", "this is a repair/sharpening", "—", "At Hamming distance one the scoring Gibbs evaluation needs no deletability premise: c′₂ ≥ 1/(B+3).")
r("PropD-drift", "supplement", S24 + " §1 · Prop. D (drift form)", "PROVED", "V|" + V24 + " Prop. D VERIFIED", N, "none needed", "—", "A drift form of the Theorem B bound needing only η → 0 for internal bad steps.")
r("CorB-unif", "supplement", S24 + " §1 · Cor. B-unif", "PROVED", "V|" + V24 + " Cor. B-unif VERIFIED", N, "none needed", "eligible set fixed before selection", "Theorem B holds uniformly over a data-independent eligible set.")
r("CorB-M", "supplement; Thm 4 route (e-M)", S24 + " §1 · Cor. B-M", "PROVED",
  "V*|" + V24 + " Cor. B-M VERIFIED; wording GAP ('no η→0 needed' misleading)", "V*|" + A1 + " Corollary B-M VERIFIED under IND-T; does not prove eligible particles exist", "wording fix → W6-FIXREV1 draft landed (CONSOLIDATED.md, unreviewed)",
  "(R5)=IND-T; past-measurable selection", "The failure probability for the whole terminal population is the product of the per-particle bounds.", rs="pending")
r("CorP1", "supplement", S24 + " §1 · Cor. P1", "PROVED",
  "V|" + V24 + " Cor. P1 VERIFIED (numerics only at B=4)", "V|" + A1 + " Corollary P1 VERIFIED", "none needed", "a₁ ≥ 0.14 shown only at B = 4; production B=14 order factor ≈ 1/17 unmeasured",
  "A particle at Hamming distance one scores S₀ in the next round with probability ≥ a₁(x); N₁ such particles all fail with probability ≤ ∏(1−a₁).")
r("PropA-sweep", "supplement", S24 + " §1 · Prop. A", "PROVED", "V|" + V24 + " Prop. A VERIFIED (proof); vacuous numerically", N, "none needed", "—", "One-round sweep bound (vacuous: extra-for-null swaps are accepted with O(1) probability).")
r("CE1", "supplement (negative result)", S24 + " §0 headline 3 · CE1 (H24 uniform exit fails)", "COUNTEREXAMPLE",
  "V*|" + V24 + " CONFIRMED (MC 0.62–0.98 in S2–S6; exact lower bound ≥ 0.39); wording GAP: 'H24's asymptotic input (L+4)η_n → 0 is false'", "V*|" + A1 + " deterministic exit lower bound and finite obstruction VERIFIED; broad asymptotic wording GAP",
  "narrow explicit sequence (A-REV1 §5) → W6-FIXREV1 draft landed (CONSOLIDATED.md, unreviewed)", "—", "At boundary states a look-alike of a missing truth exits with probability ≥ (1−o(1))/(B+d+4), so H24's uniform exit input cannot be discharged.", rs="pending")
r("LemmaE", "supplement", "W2-VT24G · REPORT.md · Lemma E", "PROVED", "N|authored by W2-VT24G (the verifier)", "V|" + A1 + " W2's Lemma E correct", "this is a repair", "two limits (o*→1, Q_T→0) are PROOF SKETCH", "Rigorous lower bound on the first elementary-state exit probability at a boundary state.")
r("CE2", "supplement (negative result)", S24 + " §0 headline 4 · CE2", "COUNTEREXAMPLE", "V|" + V24 + " CE2 CONFIRMED (fails in 395/1050 exact cases)", N, "none needed", "—", "The brief's exponent (1−c′)^{⌊H/(s₀+d)⌋} is invalid; v(1−c)^{⌊H/v⌋} is the right form.")
r("AsymPremises-T24", "supplement", S24 + " §4 · asymptotic premises table (NL0, UDEL, TS, TL, BTP, IND)", "PROOF SKETCH",
  "G|" + V24 + " rows §6: NL0 inflation constant ERROR inside the sketch (see flagged NL0-inflation); other rows not upgraded", "G|" + A1 + " 'W1 §6 premises imply Hη→0' GAP (sup of a sum ≠ sum of sups)",
  "W2-PREM redefines NL0 correctly but adds genuine assumptions; W6-FIXREV1 draft landed (CONSOLIDATED.md, unreviewed)", "named extra premises (see W2-PREM rows)", "Conditions under which Theorem B's per-round constants hold asymptotically.", rs="pending")
r("T21-e′", "Thm 4 (route e′)", "W2-VT24G · REPORT.md §6; W2-BOOK · REPORT.md Thm 4(e′)", "PROVED",
  "V|" + V24 + " T21 (e′)/(e-M) drop-in VERIFIED as an implication, three edits required", "N|A-REV1 verified the analogous implication in T38(b)-R route (b2) (given uniform REPAIR; B on R_d needs an eligible set); W2-BOOK's Thm 4 (e′) itself not reviewed",
  "three statement edits (W2-VT24G §6) applied in W2-BOOK; eligible-set interface → W6-FIXREV1 draft landed (CONSOLIDATED.md, unreviewed)", "conditional on Theorem B; availability", "Replacing the false H24 by β_H(x)=P(Bin(H,c*)<v)+Hη keeps T21's route (e) as a valid implication.", rs="pending")

# ---------------------------------------------------------------------------------------------------------------
# W1-T38E / W3-VT38E / A-REV1  (Theorem 5)
# ---------------------------------------------------------------------------------------------------------------
S38 = "W1-T38E · REPORT.md"
V38 = "W3-VT38E · REPORT.md verdict table"
r("LemmaA-T38E", "Thm 5 (supplement)", S38 + " · Lemma A", "PROVED", "V|" + V38 + " Lemma A VERIFIED (2,048,000 cases)", N, "none needed", "—", "Gibbs change probabilities at any bridge temperature are bounded by the larger endpoint odds.")
r("C0", "supplement (negative result)", S38 + " · COUNTEREXAMPLE C0", "COUNTEREXAMPLE", "V|" + V38 + " C0 VERIFIED (exact: 9.08·10⁻⁵)", N, "none needed", "—", "The endpoint bridge bound does not transfer from single states to sets.")
r("LemmaB-T38E", "Thm 5 (supplement)", S38 + " · Lemma B", "PROVED", "V|" + V38 + " Lemma B VERIFIED (deterministic; 3,255 cases)", N, "none needed", "asymptotic reading PROOF SKETCH", "Structured bridge-mass bound on near-truth regions.")
r("LemmaS-ineq", "Thm 5 (b1′)", S38 + " · Lemma S (ESS share inequality)", "PROVED",
  "V|" + V38 + " Lemma S VERIFIED (300,000 cases)", "V|" + A1 + " Lemma S ESS share inequality VERIFIED", "none needed", "ESS ≥ eH", "A subset of fraction f keeps weighted share ≥ f − √(f(1−f)(1/e−1)) when weights have ESS ≥ eH.")
r("D2", "Thm 5 (b1′)", S38 + " · Theorem D2", "PROVED",
  "V*|" + V38 + " Theorem D2 VERIFIED after the r* repair (NB′ weaker event)", "V|" + A1 + " Theorem D2 with r*=(11+2√10)/9 VERIFIED as a finite uninterrupted-pilot bound",
  "r* and NB′ applied (W3-VT38E); asymptotic margins (D2-∞) and execution terms → W6-FIXREV1 draft landed (CONSOLIDATED.md, unreviewed)", "SR; x°ΔS₀={j}; π₀(x°) ≥ b > 1/10; Dep; NB′ (statistical instance unproved for any masked family)",
  "If a one-flip neighbour of S₀ has start mass > 1/10, the pilot's first round scores S₀ with probability ≥ 1 − e^{−2Ht²} − P(NB′ᶜ) − exp{−H(1−Dep)g(b−t)/(k_D+B+3)}.", rs="pending")
r("D2-∞", "Thm 5 (b1′)", "A-REV1 · REVIEW.md §6/§7.1", "REFEREE",
  "N|none", "V|A-REV1 (author): VERIFIED under fixed b₀ > 0.1, bounded k_D, Dep ≤ 1−c₀, P(NB′ᶜ)→0", "this is a repair/clarification", "—", "D2's finite bound tends to zero when the pilot margins are bounded away from their thresholds.")
r("D2-instance", "Thm 5 (b1′)", S38 + " + W3-PXN §2 · P7 (LH, c = 1)", "PROOF SKETCH",
  "G|" + V38 + " D2 'covers p ≫ √n masking' GAP (overstated); CF(1) instances are not masked; W3-PXN: D2-a,b,c PROVED, D2-d (NB) sketch", N, "none", "Dep, NB′, π₀(x°)>1/10 w.p. → 1 on a masked family; NB unfinished even on LH c=1; c ≥ 2 OPEN",
  "The statistical instance of the no-method-change pilot route: only LH with one cancellation, and its no-blow-up step is still a sketch.")
r("D1", "Thm 5 (supplement)", S38 + " · Theorem D1", "PROVED", "V|" + V38 + " Theorem D1 VERIFIED", N, "none needed", "locked T15 evidence tail (fails in the masked regime)", "Delivery to a near-truth region follows from the locked evidence lower tail.")
r("D3", "Thm 5 (b2, superseded)", S38 + " · Prop. D3", "PROVED-UNDER",
  "V|" + V38 + " Prop. D3 VERIFIED (SHARE is nearly the conclusion)", "G|" + A1 + " §7.2: requires the sum of SHARE and EXIT-end rates to vanish, not just their listing", "superseded by W4-SHARE D4/D5", "SHARE(ζ), EXIT-end(η)", "Terminal delivery given per-stage share and exit hypotheses.", rs="pending")
r("E1-T38E", "Thm 5 (supplement)", S38 + " · Prop. E1", "PROVED", "V|" + V38 + " Prop. E1 VERIFIED (deterministic); margin = PROOF SKETCH", N, "none needed", "—", "F(S∪P) ≥ F(S) − |P|[log 2p + ½log(n+1)]: under omission masking some state outside R_d beats the reference, so the brief's eligibility condition fails.")
r("E3-core", "Thm 5 (b1)", S38 + " · Theorem E3 (i),(iii) and cost", "PROVED",
  "V|" + V38 + " Theorem E3 VERIFIED", "V*|" + A1 + " Theorem E3 core deterministic implication VERIFIED with centre scoring, completed scans, +1 centre evaluation in the score count",
  "none needed for (i),(iii); cost count clarification", "TD′ on the greedy region; T27-H3 constant > ½; LS0 emits its centre", "A start-mode centre in a greedy basin makes one local search (LS0) score S₀; a start mass > ½ identifies the mode; cost ≤ 1+(ℓ+1)max_k[p+k(p−k)] scores.")
r("T38b-R(b1)", "Thm 5 (b1)", S38 + " · Theorem T38(b)-R route (b1)", "PROVED-UNDER",
  "V|" + V38 + " T38(b)-R composition VERIFIED ((b1) 'nearly a restatement of TD′')", "V|" + A1 + " route (b1), direct ELIG+TD′+OP VERIFIED", "none needed", "ELIG (S̃₀ in the basin), TD′ at S̃₀, OP-LS0; LS0 method change",
  "With LS0, masked-regime consistency holds whenever the start mode lies in a repair basin.")
r("T38b-R(b1′)", "Thm 5 (b1′)", S38 + " · Theorem T38(b)-R route (b1′)", "PROVED-UNDER",
  "V|" + V38 + " T38(b)-R VERIFIED", "G|" + A1 + " §7.1 route (b1′) omits asymptotic rate margins (needs D2-∞)", "A-REV1 §7.1 repair → W6-FIXREV1 draft landed (CONSOLIDATED.md, unreviewed)", "D2 hypotheses with rate margins", "No-method-change route through D2's first-round pilot scoring.", rs="pending")
r("T38b-R(b2)", "Thm 5 (b2)", S38 + " · Theorem T38(b)-R route (b2)", "PROVED-UNDER",
  "V|" + V38 + " T38(b)-R VERIFIED", "G|" + A1 + " §7.2 uniform REPAIR on R_d is an assumption, not a consequence; needs an eligible set X_n and the binomial bound; DELIV OPEN", "A-REV1 §7.2 → W6-FIXREV1 draft landed (CONSOLIDATED.md, unreviewed)", "DELIV (OPEN; C1) + REPAIR", "Gibbs-path route: delivery of an eligible particle to the terminal rounds plus a per-particle repair bound.", rs="pending")
r("T38b-R(whole)", "Thm 5", S38 + " · Theorem T38(b)-R as supplied", "PROVED-UNDER",
  "V|" + V38 + " T38(b)-R composition VERIFIED", "G|" + A1 + " T38(b)-R entire supplied statement GAP; central composition inequality and liminf VERIFIED; repaired formulation (§7.4) VERIFIED as a conditional implication",
  "A-REV1 §7 repaired formulation; W6-FIXREV1 draft landed (CONSOLIDATED.md, unreviewed)", "named inputs; execution/usability qualifications; K = min(p,⌊n/2⌋)", "Composition: liminf P(U^c, Ŝ⁺=S₀) ≥ 1−limsup P(U) once the discovery term vanishes.", rs="pending", flags="CONFLICT")
r("C1-T38E", "supplement (negative result)", S38 + " · COUNTEREXAMPLE C1", "COUNTEREXAMPLE",
  "V*|" + V38 + " C1 VERIFIED after kernel repair (reversible kernel: extinction 0.56 at N=10⁵, 1.00 at N=10⁶); W4-SHARE reproduces", "N|A-REV1 §7.2 notes the set/particle distinction remains essential; no verdict row", "kernel repaired (W3-VT38E)", "—",
  "Start mass, uniform bridge mass and zero exits do not imply delivery: all particles in A can die in most islands.")
r("CF-compat", "Thm 5 (relevance)", S38 + " headline 6 · CF(c) compatibility", "CONJECTURE",
  "G|" + V38 + " 'CF satisfies jointly…' GAP (status): H3, ELIG, TD′ verified only at n ∈ {400,1600}", N, "none", "asymptotic H3, ELIG, TD′ w.p. → 1 on CF(c); p = n^{3/4} < n", "A family meeting every (b1)+LS0 premise: numerics only; superseded by LH.")
r("Cost-T38", "Thm 5 (c)", S38 + " · Cost corollary", "PROVED-UNDER", "V|" + V38 + " cost corollary VERIFIED as a loose valid upper bound", N, "none needed", "T32(i) (CONJECTURE)", "Scores ≤ T32(i)'s ceiling + LS0's (ℓ+1)max_k[p+k(p−k)].")
r("T32(i)", "Thm 5 (c)", "F-REFINE · CARDS.md Card 6 (T32(i) bookkeeping)", "CONJECTURE", N, N, "W5-LOCKBOOK commits a 'T32(i) score-evaluation ceiling, proof and count script' but has pushed no REPORT.md", "—", "A deterministic polynomial ceiling on the number of scored models of a fit.")

# ---------------------------------------------------------------------------------------------------------------
# W2-BOOK (Theorem 4, Props 1–2)
# ---------------------------------------------------------------------------------------------------------------
BK = "W2-BOOK · REPORT.md"
r("LemmaRO", "Thm 4 / Prop 2 (run/output split)", BK + " §2 · Lemma RO", "PROVED", N, N, "none", "GUARD (implementation fact: stop-only coupling)", "Every reported output equals that of the potential uninterrupted run on the event the run is not stopped; guarantees are stated by intersecting, never conditioning on completion.")
r("CEX-guard", "Prop 2 (negative result)", BK + " §0.3 · exact counterexample", "COUNTEREXAMPLE", N, N, "none", "—", "A guard that stops 0.22% of runs makes E[Ẑ | output] = 0.974Z: unbiasedness does not survive conditioning on completion.")
r("Prop2(a,b,d,e)", "Prop 2", BK + " §2 · Prop. 2 (a),(b),(d),(e)", "PROVED", N, N, "none", "GUARD; EX-A, EX-S, CAL, START", "Islandwise and pooled-island-product unbiasedness; 95% lower-bound level ≤ 0.05; output-level bound without a completion assumption.")
r("Prop2(c)", "Prop 2", BK + " §2 · Prop. 2 (c)", "PROVED", N, N, "none", "—", "Pooled Ẑ × pooled PIP is not an identity: bias −¾Cov(PIP̂₁ⱼ, Ẑ₁) ≠ 0 (exactly reproduced).")
r("Prop2(f)", "Prop 2", BK + " §2 · Prop. 2 (f)", "PROVED-UNDER", N, N, "none", "VAL-FP(η, ε), unmeasured (needs an R/C++ replay)", "The 95% bound survives floating point at level 0.05e^η + ε.")
r("Prop1-T07", "Prop 1", BK + " §2 · Prop. 1 (T07 + T06(i); (i′),(iii′) new)", "PROVED", N, N, "none",
  "locked parts (T07(i)–(iii), T06(i)(a)); size-prior retuning can still move different-size errors",
  "HPM and MPM are Bayes rules; some size-only prior recovers S₀ iff the best size-s₀ model is S₀; a scored same-size better model certifies that no size prior can fix the error.")
r("Thm4-C1", "Thm 4", BK + " §2 · Theorem 4 (C1), routes (a),(d)", "PROVED",
  "N|W4-T38FULL (0) re-derives the same inequality (author's own assembly, not a verifier)", "N|A-REV1 §7.4 verifies the same set-inclusion argument inside T38(b)-R; W2-BOOK's Theorem 4 not itself reviewed",
  "none", "EX-A, EX-S, CAL, SR, GUARD", "For every n, P(output and Ŝ≠S₀) ≤ 2E₀δ₁ + P(discovery fails): HPM errors split into a posterior term and a discovery term.")
r("RO-splits", "supplement", BK + " §2 · run/output split for T11(iii), T14(i), T15, T23(ii), T25(iv), T31, T34", "PROVED", N, N, "none", "GUARD", "One-line statement edits move locked final-run results onto the potential uninterrupted run.")
r("T34-(v)", "supplement", BK + " §2 · T34 clause (v)", "PROVED", N, N, "none", "rest of T34 stays CONJECTURE", "Every output guarantee pays P(resource_limit) additively.")

# ---------------------------------------------------------------------------------------------------------------
# W2-T26 (Theorem 6)
# ---------------------------------------------------------------------------------------------------------------
T26 = "W2-T26 · REPORT.md"
r("T26-Lemma1", "Thm 6", T26 + " §2 · Lemma 1", "PROVED", N, N, "none", "—", "The worst bridge deficit equals max{1−π₀(S₀), 1−π(S₀)} exactly.")
r("T26-Lemmas2-3", "Thm 6", T26 + " §2 · Lemmas 2, 3", "PROVED", N, N, "none", "Lemma 3's use of T15 at a terminal-round prefix flagged for review", "Occupancy off S₀ is re-controlled at every measured-round start, making the frozen second premise redundant.")
r("T26-ThmA", "Thm 6", T26 + " §2 · Theorem A", "PROVED", N, N, "none", "EX-A, EX-S, CAL, START, OUT, (Ω), one premise (P1): (T_n+1)Δ_n → 0", "Evidence and PIP estimates are consistent in the favourable regime under a single premise, in output form (never conditioning on completion).")
r("T26-ThmB", "Thm 6", T26 + " §2 · Theorem B", "PROVED-UNDER", N, N, "none", "T03's G,R,SE,BM and T22(iii)'s (F1); deterministic-budget form vacuous below n ~ 10⁸", "Discharges (P1) in the deterministic-budget form by composition with T03 and EXP′.")
r("T26-PropC", "Thm 6 / Thm 5(a)", T26 + " §2 · Prop. C (ORTH family)", "PROOF SKETCH", N, N, "none", "p ≤ n−1, X′X=(n−1)I", "On the exactly orthogonal family every premise of Theorem B holds jointly.", flags="CONFLICT")

# ---------------------------------------------------------------------------------------------------------------
# W3-PXN  (all unverified)
# ---------------------------------------------------------------------------------------------------------------
PX = "W3-PXN · REPORT.md §2"
for pid, st, prem, mean in [
    ("PXN-P1", "PROVED", "Gaussian correlation concentration (cited, Lemma C1)", "In the iid-Gaussian linked-hub family the method's partition equals the groups w.p. → 1."),
    ("PXN-P2", "PROVED", "C1", "G, R, locked SE, SE-blk, anchored SE and BM-∞ hold w.p. → 1 on LH-iid."),
    ("PXN-LemmaB", "PROVED", "—", "Block statistics at the reference have exact Beta laws independent of the response."),
    ("PXN-P3", "PROVED", "W1-EXP Thm 1 (EXP′), locked T22(i)", "1−π₀(S°)=O_P(√(log n/n)) at p ≫ n, without the 2^B factor."),
    ("PXN-P4", "PROVED", "locked T22(ii-a), P3", "The masking statistic has an exact limit law; π₀(S₀)=p^{−c}n^{−c/2}e^{O_P(1)}."),
    ("PXN-P5", "PROVED", "P3", "The exact start mode equals S° w.p. → 1 (eligibility for LS0)."),
    ("PXN-P6", "PROVED", "W1-EXP Lemmas 1.1,1.2,1.4; W1-T37R Thm A(A3)", "The repair-lattice condition holds at S° so LS0 scores and certifies S₀ in c moves (certification margin fails with probability ≈ (s₀+1)/√(2π(n+1)t_n))."),
    ("PXN-P8", "PROVED", "locked T03 + design de-randomisation lemma", "The posterior concentrates on S₀ on LH-iid."),
    ("PXN-Cor", "PROVED", "above + W1-T38E T38(b)-R", "T38(b) holds on LH-iid at p ≫ n through LS0 for every c; for c = 1 also without LS0 (modulo NB sketch)."),
]:
    r(pid, "Thm 2 (v) / Thm 5 (b1-LH-iid)", PX + " · " + pid.replace("PXN-", ""), st, "N|none (W5-VMASK planned; no report)", N, "none", prem, mean)
r("PXN-P7", "Thm 5 (b1′)", PX + " · P7 (D2 on LH, c = 1)", "PROVED", "N|none", N, "none", "D2-d (NB) is a PROOF SKETCH in the same report", "For one masked variable the original method scores S₀ in the first pilot round (hypotheses a, b, c proved; no-blow-up step sketched).")
r("PXN-Q", "supplement", PX + " · Prop. Q", "PROOF SKETCH", "N|none", N, "none", "—", "If a linked unit fits in half a block (2g ≤ B, e.g. the study's groups of 5), complete linkage co-blocks the cancelling variables and the masking disappears.")
r("PXN-W", "supplement (n=200 disclosure)", PX + " · Prop. W", "PROOF SKETCH", "N|none", N, "none", "block-orthogonal population", "Under fixed s₀ and beta-min, dilution masking vanishes: no fixed-s₀ theorem describes the n = 200 numbers.")
r("PXN-W′", "supplement", PX + " · Conjecture W′", "CONJECTURE", "N|none", N, "none", "needs a sharp-constant T03 for π(S₀)→1", "A fixed-s₀ local-alternative family has π₀(S₀) → 0 with the start still mis-ranked.")

# ---------------------------------------------------------------------------------------------------------------
# W3-PGD  (PROOF.md only; REPORT.md is a stub)  -- Theorem 3 asymptotic clause
# ---------------------------------------------------------------------------------------------------------------
PG = "W3-PGD · PROOF.md (REPORT.md is a stub)"
for pid, lab, st, prem, mean in [
    ("PGD-L1.1", "Lemma 1.1", "PROVED", "—", "Move algebra: residual reductions and the swap identity."),
    ("PGD-L1.2", "Lemma 1.2", "PROVED", "SE_λ", "Best truth addition has a population gap ≥ ηNφ₀⁴θ²_min."),
    ("PGD-L1.3", "Lemma 1.3", "PROVED", "ERC", "An exact-recovery-type condition controls null leakage."),
    ("PGD-P1", "Prop. P1", "PROVED", "GERC, TRC", "PGD follows from a checkable exact-recovery condition plus truth retention."),
    ("PGD-P2", "Prop. P2 / Cor. P2′", "PROVED", "equicorrelated groups", "Exact block reduction: PGD margin is explicit, η*(d)=min{min_g(1−ρ_g²), …}, for the study's covariance families."),
    ("PGD-P3", "Prop. P3", "PROVED", "—", "Sufficient conditions for truth retention."),
    ("PGD-P4", "Prop. P4", "PROVED", "—", "PGD is sharp: a reverse margin forces failure."),
    ("PGD-P5", "Lemma P5", "PROVED", "—", "PGD, SE and LD♭ are stable under Gram perturbations."),
    ("PGD-P6", "Cor. P6", "PROVED", "a cited concentration bound", "Gaussian random designs inherit PGD(η/2) from their population covariance."),
    ("PGD-LQ", "Lemma Q (Gaussian maxima)", "PROVED", "standard", "Gaussian maxima."),
    ("PGD-LR", "Lemma R (score representation)", "PROVED", "—", "Representation of the score difference of a move."),
    ("PGD-LG", "Lemma G (population-gap comparisons)", "PROVED", "—", "Noise stays below population gaps at states missing a truth."),
    ("PGD-LU", "Lemma U (supersets of S₀)", "PROVED", "—", "Superset states: population gap is zero, everything is a χ² tail vs the penalty."),
    ("PGD-LLD", "Lemma LD (local/far decomposition)", "PROVED", "—", "Splits the nulls near and far from a state."),
    ("PGD-LS", "Lemma S (superset states)", "PROVED", "—", "Superset states are handled by the local/far decomposition."),
    ("PGD-LA′", "Lemma A′", "PROVED", "—", "Theorem A(A2–A3) holds for progress-closed regions."),
    ("PGD-CorW′", "Cor. W′", "PROVED", "—", "Checkable design conditions imply Theorem W's hypotheses."),
]:
    r(pid, "Thm 3 (asymptotic clause)", PG + " · " + lab, st, "N|none (W5-VPGD planned; no report)", N, "none", prem, mean)
r("ThmW", "Thm 3 (asymptotic clause)", PG + " · Theorem W (refined T37(iii))", "PROVED",
  "N|none — no verifier; REPORT.md is a stub (W5-VPGD planned)", N, "none", "EX-A, G, R, SE_λ(d+1), BM-∞, PGD(η) on R_{a,d}(𝒟), and one of (H1) d≤1, (H2), (H3) LD♭",
  "Under population greedy dominance and local dependence of nulls, the greedy map is progress-only on the region w.p. → 1, so the search repairs from every centre in it for ℓ_n ≥ a+d.")
r("C-LD", "supplement (negative result)", PG + " · Prop. C-LD", "COUNTEREXAMPLE", "N|none", N, "none", "equicorrelated nulls r > ½", "LD cannot be dropped for d ≥ 2 with unrestricted extras: TD′_P(R_{0,2}) fails w.p. → 1.")

# ---------------------------------------------------------------------------------------------------------------
# W4-T38FULL
# ---------------------------------------------------------------------------------------------------------------
T38F = "W4-T38FULL · REPORT.md"
r("T38-(0)", "Thm 5 (0) / Thm 4", T38F + " §2 · Theorem 5 (0) (= W1-T38E T38(b)-R composition)", "PROVED",
  "V|W3-VT38E T38(b)-R composition VERIFIED; W4-T38FULL re-derives the strict-maximiser step", "V*|" + A1 + " §7.4 repaired composition proof VERIFIED (same set argument as locked T21(C1)); the printed T38(b)-R as a whole is GAP (execution/usability terms, K=min(p,⌊n/2⌋))",
  "W6-FIXREV1 to supersede W4's T38_STATEMENT/PROOF (execution/usability qualifications; K = min(p,⌊n/2⌋)) — PENDING", "GUARD, EX-A, EX-S, CAL, SR; (P): δ₁ → 0 (T03)",
  "For every n, P(output and Ŝ⁺≠S₀) ≤ 2E₀δ₁ + D_n; if the discovery term D_n → 0 then liminf P(output, Ŝ⁺=S₀) ≥ 1 − limsup P(U).", rs="pending")
r("T38-(a)", "Thm 5 (a)", T38F + " §2 · Theorem 5 (a)", "PROVED-UNDER",
  "V*|inputs VERIFIED (W3-VEXP); ORTH composition unreviewed", N, "none", "(F1)/(F2)/(F3); T11(iii); ORTH joint family (see ORTH-joint)", "In the favourable regime the iid final draws find S₀ w.p. → 1, with or without LS0.")
r("LS-score", "Thm 3 / Thm 5 (b1)", T38F + " §2 · Lemma LS-score", "PROVED",
  "V|" + T38F + " §6a: fresh same-family subagent VERIFIED (not an independent run)", N, "none", "D_S on the lattice, ℓ ≥ Φ(C₀)−1, centre emitted", "If every lattice state has a strictly dominant progress move, the production search from the centre scores S₀ (certification not needed).")
r("LemmaM", "Thm 5 (b1)", T38F + " §2 · Lemma M", "PROVED", "V|" + T38F + " §6a: same-family subagent VERIFIED", N, "none", "SE on the compared sets; margin m_n ≥ M_n√(log n/n)", "A population margin turns into a finite-sample score ordering uniformly over all small model pairs w.p. → 1.")
r("Thm-b1", "Thm 5 (b1)", T38F + " §2 · Theorem b1", "PROVED-UNDER", "V|" + T38F + " §6a: same-family subagent VERIFIED", N, "none", "(M1) π₀(S°)>½, (M2) POP-LAT margin, (M3) SE(S°∪S₀), OP-LS0; LS0 method change", "With LS0, masked-regime consistency holds on any family with a bounded-distance reference and a population lattice margin.")
r("LH-LAT", "Thm 3 (part C) / Thm 5 (b1-LH)", T38F + " §2 · Prop. LH-LAT", "PROVED", "V|" + T38F + " §6a: same-family subagent VERIFIED (20 brute-force cases, m₀ sharp)", N, "none", "|ψ|<1 for the algebra; |ψ|<ρ for partition and (M1)", "On the linked-hub family the lattice margin is explicit and sharp: m₀=min{(1−κ)R_min, min β²(1−ψ²)², min θ_h²}.")
r("T38-b1-LH", "Thm 5 (b1-LH)", T38F + " §2 · Theorem 5 (b1-LH)", "PROVED",
  "V*|inputs VERIFIED by W3-VEXP; assembly by W4's same-family subagent; no independent assembly review", "N|cross-family review of the masked instance pending (F-REFINE item 1)", "none", "LH exact Gram (p ≤ n−1), |ψ|<ρ, g ≤ B < 2g; LS0 method change (Felipe: conditionally approved)",
  "On the explicit linked-hub family with LS0, every premise is proved and the reported HPM is consistent: no open statistical input.")
r("T38-b1′", "Thm 5 (b1′)", T38F + " §2 · Theorem 5 (b1′)", "PROVED-UNDER", "V|D2 verified by W3-VT38E", "G|A-REV1 route (b1′) GAP (see T38b-R(b1′))", "W6-FIXREV1 draft landed (CONSOLIDATED.md, unreviewed)", "D2 hypotheses; NB′ (LH c=1 instance PROOF SKETCH)", "No-method-change masked route through the pilot's first stage.", rs="pending")
r("T38-b2", "Thm 5 (b2)", T38F + " §2 · Theorem 5 (b2)", "PROVED-UNDER", "N|none", "G|A-REV1 §7.2 (see T38b-R(b2))", "W6-FIXREV1 draft landed (CONSOLIDATED.md, unreviewed)", "DELIV (OPEN; C1) and REP (B♯ premises)", "Gibbs-path delivery route; no explicit family has the inputs verified.", rs="pending")
r("ORTH-joint", "Thm 5 (a) / Thm 6", T38F + " §2 + W2-T26 Prop. C", "PROOF SKETCH",
  "N|W2-T26 Prop. C = PROOF SKETCH; W4-T38FULL: 'new composition, checked line by line here', no verifier", N, "none", "p ≤ n−1, orthogonal Gram",
  "On the exactly orthogonal family Thm 1, Thm 2(iii), Thm 5(a) and Thm 6 hold jointly (rates √(log n/n)).", flags="CONFLICT")

# ---------------------------------------------------------------------------------------------------------------
# W4-SHARE (all unverified)
# ---------------------------------------------------------------------------------------------------------------
SH = "W4-SHARE · REPORT.md §2"
for pid, lab, st, prem, mean in [
    ("SHARE-D4", "Theorem D4", "PROVED", "(TRACK); predictable stopping and θ=∞ convexity flagged for review", "The W-count of an island dominates a branching chain, so delivery holds unless an explicit envelope fails."),
    ("SHARE-D5", "Cor. D5", "PROVED", "confinement sets, oscillation Γ", "Delivery holds when Γ+Ση ≤ log(Nπ₀(h₀)/T) − ω(1): no LT, no SHARE, no bridge-mass hypothesis."),
    ("SHARE-G", "Prop. G", "PROVED", "—", "Fitness oscillation is at most max κ for every grid: no ESS-grid condition can imply delivery."),
    ("SHARE-SH", "Prop. SH", "PROVED", "—", "The log N threshold is sharp up to a factor 2."),
    ("SHARE-X", "Prop. X", "PROVED", "—", "Gate obstruction: crossing a posterior barrier is a rare gate event."),
    ("SHARE-M(a)", "Prop. M (a)", "PROVED", "λ_min(R_{T∪M}) > 0", "Every truth subset has a missing truth with discrepancy ≥ (n−1)λ²θ²_min."),
    ("SHARE-M(b)", "Prop. M (b)", "PROOF SKETCH", "G,R,SE,BM-∞; explicit-remainder gain expansion", "In T03's regime the masked case has no posterior barrier: the path to S₀ is downhill for φ ≥ φ_n → 0."),
    ("SHARE-PD", "Lemma PD", "PROVED", "—", "Start mass × fitness = posterior: a takeover needs an outsider that is posterior-better."),
    ("SHARE-B2W4", "Theorem B2-W4", "PROVED-UNDER", "(TRACK), (OSC), confinement, REPAIR on W", "Route (b2) assembly: failure ≤ [ε_E + exp{…}]⁴ + ε_rep."),
    ("SHARE-TRACK", "(TRACK)+(OSC) for BVS", "CONJECTURE", "occupancy-weighted exits near 𝓡_d boundary", "The BVS-level inputs of the envelope route (numerically supported)."),
    ("SHARE-BGD", "Bridge-Gibbs discovery", "CONJECTURE", "Prop. M(b); order-compatibility constant", "In T03's regime S₀ is scored during the bridge w.p. → 1 (500/500 islands); would make (b2) unnecessary."),
    ("SHARE-PB", "Posterior-barrier design PB", "COUNTEREXAMPLE", "finite n, reproducible", "A posterior barrier defeats (b2), LS0 and T39 alike: no method change helps."),
    ("SHARE-C1BVS", "C1-type extinction in BVS", "CONJECTURE", "—", "C1-type extinction is possible only where REPAIR on the occupied region already fails."),
]:
    r(pid, "Thm 5 (b2)", SH + " · " + lab, st, "N|none (REPORT.md present; no verifier assigned)", N, "none", prem, mean)

# ---------------------------------------------------------------------------------------------------------------
# Referee-supplied repairs (A-REV1) — statuses are theirs: VERIFIED/GAP/ERROR on others' claims; repairs unlabelled
# ---------------------------------------------------------------------------------------------------------------
r("AREV1-LemmaS-sharp", "Thm 5 (b1′)", "A-REV1 · REVIEW.md §3.2", "REFEREE", "N|none", "V|A-REV1 (author)", "repair to Lemma S's attainment sentence; W6-FIXREV1 draft landed (CONSOLIDATED.md, unreviewed)", "f > 1−e for attainment",
  "ω(A) ≥ max(0, f − √(f(1−f)(1/e−1))), attained by two-level positive weights only when f > 1−e; D2 uses f > 0.1, e = 0.9, inside the valid range.", rs="pending")
r("AREV1-T38-repair", "Thm 5", "A-REV1 · REVIEW.md §7.4", "REFEREE", "N|none", "V|A-REV1 §7.4 (author): 'VERIFIED as a conditional implication'", "to be adopted by W6-FIXREV1 — PENDING", "eligible set; execution event E; U = no usable HPM", "Repaired composition: P(U or wrong) ≤ P(U) + 2E₀δ₁ + P(U^c ∩ M) with explicit terms for pilot, Gibbs and LS0 routes.", rs="pending")
r("AREV1-CE1-seq", "supplement", "A-REV1 · REVIEW.md §5", "REFEREE", "N|none", "V|A-REV1 (author): explicit sequence p_n=⌈n^{1/3}⌉, S₀={1}, corr(x₁,x₂)=r", "to be adopted by W6-FIXREV1 — PENDING", "narrow: one explicit design sequence", "An explicit correlated-design sequence on which H24's vanishing-exit premise fails (η_n ≥ (1−o_P(1))/21).", rs="pending")

# ---------------------------------------------------------------------------------------------------------------
# Flagged sub-claims (ERROR / GAP verdicts; not counted among named results)
# ---------------------------------------------------------------------------------------------------------------
def claim(id, parent, src, sf, cf, rep, rs, mean, flags=""):
    r(id, parent, src, "—", sf, cf, rep, "—", mean, kind="claim", rs=rs, flags=flags)

claim("T03-1.2e5", "T03♯ (disclosure)", "W1-T03R · REPORT.md headline 4/§3/§5 (proof thresholds 'n ≈ 1.2·10⁵')",
      "E|W2-VT03R row 29 ERROR (binding condition q_n ≤ ½ first holds at n ≈ 2.1·10⁶ / 2.5·10⁶)", "E|A-REV2 §3.5 confirms: q ≈ 5.5·10²², 7.9·10²⁸ at n=130,328",
      "W2-VT03R R1 replacement sentence (n ≳ 2·10⁶); W6-FIXREV2 'confirm' PENDING", "applied", "A numerical claim in the finite-n disclosure was wrong (strengthens the disclosure).")
claim("A5(a)", "Theorem A (A5(a))", S37 + " §2 · A5(a): strict literal TD(d,0) ⇒ TD′_P",
      "E|W3-VT37R row 9 ERROR (CEX-1, no positivity clause)", "E|A-REV2 §4.1 ERROR (suppressor counterexample); POS repair VERIFIED",
      "R1-POS (W3-VT37R; verified by A-REV2); consolidated statement W6-FIXREV2 PENDING", "applied", "Literal strict TD does not imply progress-greedy dominance without a positivity clause; hence the original T37(i) is false even at d = 0.")
claim("R2-dichotomy", "Lemma 0(b) repair", "W3-VT37R · REPAIRS.md · R2 (E_LS^c or E_LS with terminal score ≥ F(S₀))",
      "N|authored by W3-VT37R", "E|A-REV2 §4.2 ERROR (omits an inferior local maximum and capped searches ending below the truth)",
      "A-REV2 three-way partition F_pre/F_post (referee proposal) — W6-FIXREV2 PENDING", "pending", "The proposed exhaustive failure dichotomy for the final search is not exhaustive.", flags="CONFLICT")
claim("TDP-iff-DS", "Theorem A (definition of D_S)", S37 + " §2 · 'TD′_P ⇔ (L) and all D_S'",
      "V|W3-VT37R rows 6–7 VERIFIED (exhaustive; ties measure zero)", "E|A-REV2 §4.3 ERROR (exact ties: n=100, p=2, x₁=x₂; strict D_S is sufficient, not necessary)",
      "D_S as a sufficient event or D_S^lex — W6-FIXREV2 PENDING", "pending", "With exact ties the one-state strict-dominance event is only sufficient for TD′_P.", flags="CONFLICT")
claim("Weakest-prose", "Theorem A (prose)", S37 + " §2 · 'TD′_P is the weakest among ≤Φ-move conditions'",
      "E|W3-VT37R row 11 ERROR (PHI-REACH: 23/360 designs)", "E|A-REV2 §4.3 ERROR; V37 R3 correction retained",
      "W3-VT37R R3 (verified by A-REV2)", "applied", "A neutral step can be compensated by a swap, so total length ≤ Φ does not require every move to reduce Φ.")
claim("R4-excess", "Theorem C (V37 R4)", "W3-VT37R · REPAIRS.md · R4 printed expression pP(|Z| ≥ u)",
      "N|authored by W3-VT37R", "E|A-REV2 §4.4 ERROR (excess-above-multiplicity form: the printed tail does not vanish; at p=n it grows like √(n/log n))",
      "put the original threshold t, not the excess u, in the Gaussian tail — W6-FIXREV2 PENDING", "pending", "A repair step in the asymptotic Theorem C sketch has a wrong tail expression.")
claim("EXP-const", "EXP′ / Lemma U limiting constant", SE + " Thm 1 and W2-PREM §3: κ → 0.52/c_*",
      "V|W3-VEXP row 5 VERIFIED Thm 1 (limit constant not flagged)", "E|A-REV1 §3.4 and A-REV2 §5.1 ERROR: limit is 0.51/c_* (0.52/c_* + o(1) is a valid looser bound); finite bound unaffected",
      "replace the arrow by →0.51/c_* — W6-FIXREV1 draft landed (unreviewed) / W6-FIXREV2 PENDING", "pending", "An arithmetic slip in the displayed asymptotic limit of the EXP′ remainder constant.", flags="CONFLICT")
claim("Thm4-iff", "Thm4-EXP (growing leakage)", SE + " Thm 4 'masking persists iff η < 1/2.02'; W3-VEXP R4 'p^{−c} alone forces vanishing mass whatever η'",
      "G|W3-VEXP R4: 'iff … sufficient' self-contradictory (wording)", "E|A-REV2 §5.3: 'iff' ERROR; VEXP's additional 'whatever η' claim not justified",
      "'η < 1/2.02 suffices' / exponent condition a+½−1.01η > 0 — W6-FIXREV2 PENDING", "pending", "An 'iff' gloss on a one-sided sufficient bound, and a verifier's over-correction.", flags="CONFLICT")
claim("SEX-4.3-normal", "LH-iid sketch", SE + " §4.3: masked projection is exactly normal",
      "N|none", "E|A-REV2 §5.4: normalised Gaussian column direction is spherical, not Gaussian; δ=O_P(1) still follows from the second moment",
      "correct the sentence — W6-FIXREV2 PENDING", "pending", "A minor exact-law misstatement in a sketch.")
claim("LemmaU-quant", "Lemma U", PR + " §3 · 'every V of size ≤ k used below'",
      "N|none", "G|A-REV2 §6.2 GAP (cardinality budget must include the extra sets; counter-scenario p=n−1 orthogonal)",
      "explicit auxiliary family H, L > 4max(A′,a_H) — W6-FIXREV2 PENDING", "pending", "Lemma U's extra quantifier has no cardinality premise tied to the union bound.")
claim("C3-lower", "Lemma U (C3 matching lower bound)", PR + " §3 · C3 'matching lower bound under δ = 0'",
      "N|none", "E|A-REV2 §6.3 ERROR (n=10⁶, p=2: actual 16.25 vs claimed bound 19.56; Z²/4 vs Z²/2−12.24)",
      "require μ ∈ span(X_T) — W6-FIXREV2 PENDING", "pending", "Zero leakage does not give a matching lower bound when omitted signal remains outside T.")
claim("Kantorovich-1.925", "D2 (NB)", S38 + " · ratio ≤ 1.925 ⇒ ESS ≥ 0.9H",
      "E|W3-VT38E ERROR (cosmetic): 4r/(1+r)²=0.8999927 at r=1.925", "V|A-REV1 §3.2: corrected r*=(11+2√10)/9 VERIFIED",
      "r* applied by W3-VT38E; A-REV1 agrees", "applied", "The constant in the no-blow-up ratio was a hair too small.")
claim("LemmaS-attain", "Lemma S", S38 + " §3 + W3-VT38E: 'bound attained by two-level weights', 'tight'",
      "V|W3-VT38E Lemma S VERIFIED, 'tight' (2-level weights attain the bound)", "E|A-REV1 §3.2 ERROR (positive weights need f > 1−e; at f=0.05, e=0.9 the weight is negative)",
      "domain restriction + sharpened inequality (A-REV1) — W6-FIXREV1 draft landed (CONSOLIDATED.md, unreviewed)", "pending", "The inequality is right everywhere; the claim that it is attained holds only for f > 1−e.", flags="CONFLICT")
claim("E3(ii)", "Theorem E3 (ii)", S38 + " · E3(ii) start-law lower bound without q < 1",
      "V|W3-VT38E Theorem E3 VERIFIED ((ii) 'cites locked T22(i) correctly')", "E|A-REV1 §3.3 ERROR (omits locked q<1; p=2: claimed 1.98·10²³ vs actual 9.44·10⁻¹⁴)",
      "insert 0 ≤ q < 1; check downstream uses (W4-T38FULL, W3-PXN) — W6-FIXREV1 draft landed (CONSOLIDATED.md, unreviewed)", "pending", "An unrestricted start-mass lower bound used a locked theorem without its hypothesis q < 1.", flags="CONFLICT")
claim("NL0-inflation", "W1-T24G §6 premise table", S24 + " §4/§6 · NL0 row 'inflation 1.86, fails for p ≳ n^{0.58}'",
      "E|W2-VT24G ERROR (inside a PROOF SKETCH): inflation is 1+r=1.3; threshold p ≫ n^{5/3} (n^{1/(2r)})", N,
      "corrected remark in W2-VT24G", "applied", "Quantitative error in the equicorrelated-null leakage estimate; the conclusion 'NL0 needs a design condition' stands.")
claim("NL0-quantifier", "W1-T24G §6", S24 + " §6 · NL0 as sup_W Σ_l o_l(W)",
      "N|W2-PREM §0 redefines NL0 as the sum of suprema", "G|A-REV1 §4 GAP (sup of a sum ≠ sum of sups; array example)",
      "stronger premise already in W2-PREM; downstream cost → W6-FIXREV1 draft landed (CONSOLIDATED.md, unreviewed)", "pending", "The leakage premise had its quantifiers in the wrong order.")
claim("T38-text", "T38 statement", S38 + " · text (limit form, cost formula, ℓ_n<s₀+d, K=⌊n/2⌋)",
      "V*|W3-VT38E: limit form and cost formula flagged and corrected", "G|A-REV1 §7.3 K must be min(p,⌊n/2⌋); T11(vii) citation → locked T21(C1)",
      "W6-FIXREV1 draft landed (CONSOLIDATED.md, unreviewed)", "pending", "Wording-level corrections to T38's printed conditions.")

# ---------------------------------------------------------------------------------------------------------------
# Implementation facts and retired claims (premises, not results)
# ---------------------------------------------------------------------------------------------------------------
IMPL = [
    ("GUARD", "Stop-only resource guard: on 𝒪 every reported output equals the potential uninterrupted run's.", "W2-BOOK (code reading of v3_runtime.h, v3_engine.h, v3_core.cpp); W5-LOCKBOOK audit in progress, no REPORT",
     "IMPLEMENTATION FACT — independent code check pending"),
    ("SR", "Both Gibbs configurations (held and flipped) are scored and offered to the HPM store.", "HQ SR_AUDIT.md (holds in engine, file:line evidence); W3-VT38E, W2-VT24G agree",
     "IMPLEMENTATION FACT — HQ read of the code; W5-LOCKBOOK audit supersedes if different"),
    ("OUT / STREAM / emit_centre", "OUT: no failure mode returns a partial Ẑ or PIP. STREAM: sequential stream reading (IND-T). emit_centre: LS0 must emit its centre as a score event.", "W2-T26, W2-PREM, W3-VT38E; W5-LOCKBOOK audit in progress",
     "IMPLEMENTATION FACT — unaudited"),
]
RETIRED = [
    ("Literal T37 / TD(d,m)", "false for d ≥ 1 on any design (Prop1-TD, V1-TDfails); false at d = 0 without positivity (CEX1)", "replaced by Theorem A + POS, Theorem W"),
    ("H24 (uniform exit hypothesis of T24/T21(e))", "its asymptotic input (L+4)η_n → 0 is false in correlated designs (CE1, LemmaE)", "replaced by Theorem B / B♯ (route e′)"),
    ("The brief's (1−c′)^{⌊H/(s₀+d)⌋} form", "invalid (CE2)", "v(1−c)^{⌊H/v⌋}"),
    ("Brief's T38 eligibility condition F(S°) > sup_{𝓡_d^c} F", "fails w.p. → 1 under omission masking (E1-T38E)", "LS0 route / start-mode eligibility"),
    ("'m_n = s₀+O(s₀ log n/log p)'", "false under G, R alone (PropD-T03)", "exact tail m♯ ≈ s₀ log n"),
    ("'E[Ẑ | completed] = Z' and 'pooled Ẑ × pooled PIP is unbiased'", "both false (CEX-guard, Prop2(c))", "islandwise identities; output-level bounds"),
    ("W1-EXP weak-signal masking explains n = 200", "evidence against (dilution)", "dilution masking (PropD-dilution, PXN-W)"),
    ("SHARE / LT as route-(b2) hypotheses", "superseded; LT not necessary (C1, PB)", "W4-SHARE D4/D5 envelope"),
]


# ===============================================================================================================
# LATE-LANDING BRANCHES (second fetch): W5-LOCKBOOK, W5-VPGD, W5-VMASK (draft), O-CERT, O-SWAP, A-DRAFT (full),
# F-DRAFT (NEW_TARGETS.md), W6-FIXREV1 (CONSOLIDATED.md draft), W6-FIXREV2 (STATEMENTS.md draft)
# ===============================================================================================================
def upd(id, **kw):
    for row in ROWS:
        if row["id"] == id:
            row.update(kw)
            return
    raise KeyError(id)


LB = "W5-LOCKBOOK · REPORT.md verdict tables"
VP = "W5-VPGD · REFEREE.md"

# ---- W5-LOCKBOOK refereed W2-BOOK and W2-T26 (same-family) --------------------------------------------------
upd("LemmaRO", sf="V|" + LB + " (W2-BOOK): CORRECT; 𝒪 = 𝒢ᶜ ∩ 𝒪̄ verified in code")
upd("CEX-guard", sf="V|" + LB + ": CONFIRMED, reproduced exactly; also under the engine-faithful cost rule (bias can be upward)")
upd("Prop2(a,b,d,e)", sf="V|" + LB + ": CORRECT (T12(iii); output level; exact branch contributes 0)")
upd("Prop2(c)", sf="V|" + LB + ": CORRECT; ¾Cov/Z = 0.130481, relative bias −0.131716 reproduced to 10⁻⁵⁸")
upd("Prop2(f)", sf="G|" + LB + ": GAP (wording, fixable): VAL-FP must require the exact run to share status and 𝓒",
    rep="VAL-FP restated in W5-LOCKBOOK STATEMENTS.tex (same-family)", rs="applied")
upd("Prop1-T07", sf="V*|" + LB + ": (i′) sharpness CORRECT; (iii′) certificate CORRECT with amendment 'strict beyond numerical error'",
    rep="amendment written in W5-LOCKBOOK STATEMENTS.tex")
upd("Thm4-C1", sf="V*|" + LB + ": (C1′), routes (a), (d) CORRECT, needs the convention 𝒢 ⊆ U (stopped fits return an incomplete HPM, G1)",
    prem="EX-A, EX-S, CAL, SR, GUARD; U must contain every stopped fit and abort (G1, G3)")
upd("T21-e′", sf="V*|W2-VT24G §6 VERIFIED as an implication; " + LB + ": (e′)/(e-M) CONSISTENT with VT24G's three edits, CORRECT given Lemma STREAM; eligibility = feasibility s₀+a(x) ≤ K")
upd("RO-splits", sf="V*|" + LB + ": T11(iii), T14(i), T15, T25(iv), T31, T34 edits CORRECT; T23(ii-d) output corollary GAP (false on the exact branch; restrict to SMC branch)",
    rep="T23(ii-d) restricted to the SMC branch in W5-LOCKBOOK STATEMENTS.tex", rs="applied")
upd("T34-(v)", sf="V|" + LB + ": split edit for T34 CORRECT")
upd("T26-Lemma1", sf="V|" + LB + " (W2-T26): CORRECT (grid check 66/66)")
upd("T26-Lemmas2-3", sf="V|" + LB + ": CORRECT, including the flagged Lemma 3 step (T15 at a terminal-round prefix = T12(i.b))")
upd("T26-ThmA", sf="V|" + LB + ": CORRECT; (A-0) constants 3x/27x/108x checked; OUT verified in code")
upd("T26-ThmB", sf="V|" + LB + ": CORRECT as a conditional composition")
upd("T26-PropC", sf="N|" + LB + ": PROOF SKETCH kept; algebra re-done, no error found; constants not written out")
upd("T32(i)", st="PROVED", src="W5-LOCKBOOK · REPORT.md §1.4 + PROOF.md §T32 (F-REFINE CARDS.md, written earlier, lists it as CONJECTURE)",
    sf="N|authored by W5-LOCKBOOK; no second same-family check", cf="N|none", rep="none",
    prem="the code-to-count mapping (re-check on any engine change); LS0 adds 1+(ℓ+1)M_p",
    mean="The number of scored models of a fit is bounded by an explicit polynomial count, so Thm 5(c) is a theorem rather than a conjecture.",
    flags="status moved CONJECTURE→PROVED by W5-LOCKBOOK")
upd("Cost-T38", prem="T32(i): now PROVED by W5-LOCKBOOK (unreviewed)")

r("Lemma-STREAM", "supplement (Thm B′/B♯ via IND-T)", "W5-LOCKBOOK · AUDIT.md §4 (REPORT.md §3)", "PROVED",
  "N|authored by W5-LOCKBOOK", N, "none", "EX-S; read, not run; second reader requested", "An i.i.d. stream read at stopping times gives independent particle trajectories (strong-Markov argument); same fact as IND-T.")
r("Impl-lemmas", "supplement", "W5-LOCKBOOK · AUDIT.md §7 (GUARD, OUT, SR, STREAM, LS)", "PROVED",
  "N|authored by W5-LOCKBOOK (code reading; read, not run)", "N|cross-family read requested for the stop-site list and the cache/offer invariant", "caveats G1–G4 and emit_centre=true now written into the statements",
  "completeness of the stop-site list; cache-insertions-offered invariant; D61 same-seed replay not done", "The resource guard, output bookkeeping, SR scoring, stream discipline and scan-before-limit rule are confirmed by line-level code reading.")
claim("T23ii-d-scope", "Run/output split", "W2-BOOK §2 · T23(ii-d) output corollary", "G|" + LB + ": GAP (scope) — false on the exact branch as written", "N|none",
      "restrict to the SMC branch (W5-LOCKBOOK STATEMENTS.tex)", "applied", "An output-form corollary was stated for both branches but fails on the exact branch.")
claim("Stopped-HPM-G1", "Thm 4 (U)", "W2-BOOK Lemma RO / GUARD: 'every partial output hidden'", "G|" + LB + " §5: false literally — a stopped fit returns an incomplete HPM and the archive carries partial island evidences (G1, G2)", "N|none",
      "conventions 𝒢 ⊆ U and 'reported = estimate fields' written into W5-LOCKBOOK STATEMENTS.tex; Felipe to confirm", "applied", "The guard theorems need U to include every stopped fit; otherwise an incomplete HPM counts as output.")

# ---- W5-VPGD refereed W3-PGD PROOF.md (same-family) ---------------------------------------------------------
for pid, code, txt in [
    ("PGD-L1.1", "V", "§1 Lemma 1.1 VERIFIED"), ("PGD-L1.2", "V", "§1 Lemma 1.2 VERIFIED"), ("PGD-L1.3", "V", "§1 Lemma 1.3 VERIFIED"),
    ("PGD-P1", "V", "§1 Prop. P1 VERIFIED (the five non-progress types exhaust the moves)"), ("PGD-P2", "V", "§1 Prop. P2 (iff) and Cor. P2′ VERIFIED; brute force on block designs"),
    ("PGD-P3", "V", "§1 Prop. P3 VERIFIED"), ("PGD-P4", "V", "§1 Prop. P4 VERIFIED"),
    ("PGD-P5", "V*", "§1 Lemma P5 VERIFIED; the LD♭ stability sentence is a GAP (G3, minor): true with O(ε/φ₀⁸)"),
    ("PGD-P6", "V*", "§1 Cor. P6 VERIFIED given the cited concentration bound; GAP G2 (uniformity of Theorem W's o(1) over designs with the same constants) and covariance→correlation passage not re-derived"),
    ("PGD-LQ", "V", "§2 Lemma Q VERIFIED"), ("PGD-LR", "V", "§2 Lemma R VERIFIED"), ("PGD-LG", "V", "§2 Lemma G VERIFIED"), ("PGD-LU", "V", "§2 Lemma U VERIFIED"),
    ("PGD-LLD", "V", "§3 Lemma LD VERIFIED"), ("PGD-LS", "V", "§3 Lemma S VERIFIED (constant not sharp; W5-VPGD STAR.md proves a sharpening ★′)"),
    ("PGD-LA′", "V", "§4 Lemma A′ VERIFIED"),
    ("PGD-CorW′", "V*", "§4 Cor. W′(i),(ii) VERIFIED; random designs under (H3) GAP (G2/G3)"),
]:
    upd(pid, sf=code + "|" + VP + " " + txt)
upd("ThmW", sf="V|" + VP + " §4: Theorem W VERIFIED (m ≥ 1 part, m = 0 part and (L), data-dependent centres); 'up to exact ties' inherited from W1-T37R Lemma 0(c)",
    src=PG + " · Theorem W (refined T37(iii)); REPORT.md is a stub")
upd("C-LD", sf="V*|" + VP + " §5: construction and probability argument VERIFIED; 'same computation needs r > 1/(2A) at p ≍ n^A' is a PROOF SKETCH (G4: p > n cannot use the orthonormal construction); script illustrates direction only")
claim("PGD-G2-uniformity", "Cor. P6 / Cor. W′", PG + " · Cor. P6", "G|" + VP + " G2: uniformity of Theorem W's o(1) over designs with the same constants not stated", "N|none",
      "W5-VPGD REPAIRS R2 (file named in REFEREE.md; not read)", "applied", "The random-design corollary needs a uniform-in-design version of Theorem W's error.")
claim("PGD-G3-LDstab", "Lemma P5", PG + " · Lemma P5 LD♭ stability sentence", "G|" + VP + " G3 (minor): only asserted; true with O(ε/φ₀⁸)", "N|none",
      "W5-VPGD REPAIRS R3 (not read)", "applied", "Stability of the local-dependence condition under Gram perturbations.")
claim("PGD-G4-pgtn", "Prop. C-LD", PG + " · interpretation 'p ≍ n^A needs r > 1/(2A)'", "G|" + VP + " G4: PROOF SKETCH, not part of the counterexample", "N|none",
      "restate as sketch (W5-VPGD)", "applied", "A p > n version of the equicorrelated-null counterexample needs a random-design construction.")
claim("PGD-star-misleading", "Theorem W (remark)", PG + " · '(★) is off by a factor 3–4 from C-LD'", "G|" + VP + " §5: interpretive claim misleading (C-LD not extremal; ★′ proved in STAR.md)", "N|none",
      "W5-VPGD STAR.md (not read)", "applied", "The comparison of the LD♭ constant with the counterexample threshold is not meaningful.")

# ---- W5-VMASK (draft REPAIRS.md; no REPORT.md yet) ----------------------------------------------------------
VM = "W5-VMASK · REPAIRS.md (draft; REPORT.md not yet pushed)"
claim("PXN-LemmaU-U1", "W3-PXN Lemma U (U1)", PX + " / PROOF Lemma U (U1): ν log(1+a_A/RSS) ≤ 1", "E|" + VM + " R2 ERROR (cosmetic): the number is wrong, argument unaffected", "N|none",
      "repaired in W5-VMASK R2", "applied", "A wrong constant in a lemma of the p ≫ n family.")
claim("PXN-Lfail-numbers", "W3-PXN §9.3 / REPORT §6", PX + " · '(L) fails ≈ 4% at n=200, 1.2% at n=1600'", "E|" + VM + " R4 ERROR (numerical, cosmetic)", "N|none",
      "corrected numbers in W5-VMASK R4", "applied", "The quoted failure rate of the certification margin was off.")
claim("PXN-P7-NB", "W3-PXN P7 (D2-d)", PX + " · P7 NB with constant 1.925", "G|" + VM + " R1: step was a PROOF SKETCH, now PROVED (candidate, this run only); R3: inherited 1.925 constant (cosmetic)", "N|none",
      "R1 proof of NB on LH-iid c=1; R3 uses r* / NB′ — W5-VMASK draft, not a verdict-table review", "applied", "The no-first-stage-blow-up step of the no-method-change pilot route on LH-iid (c = 1) now has a written proof.")
claim("LH-LAT-sharp", "Prop. LH-LAT", T38F + " · 'm₀ … which is sharp'", "G|" + VM + " R5 GAP (overstatement), restated", "N|none",
      "restated in W5-VMASK R5", "applied", "The margin formula is a valid lower bound; sharpness was overstated (cf. W4-T38FULL's own 'attained in two cases').")
claim("LS0-cost-+1", "Cost (E3 / T38(c))", S38 + " / " + T38F + " · LS0 cost", "G|" + VM + " R7 GAP (cosmetic, +1 centre evaluation)", "V|A-REV1 §6 made the same point",
      "corrected in W5-VMASK R7", "applied", "LS0's score count needs +1 for the initial centre evaluation.")

# ---- A-DRAFT (full report; Astra; original-draft track) -----------------------------------------------------
AD = "A-DRAFT · REPORT.md"
for pid, lab, st, prem, mean in [
    ("ADRAFT-ThmA", "§2.2 Theorem A (fixed-data particle consistency)", "PROVED", "EX-A, EX-S, START, CAL; potential uninterrupted run; N → ∞ at fixed calibration", "For every bounded h the SMC estimators converge in probability and L² to the posterior functional, and Ẑ/Z → 1, at fixed data."),
    ("ADRAFT-CorA1", "§2.3 Corollary A1 (from locked T12)", "PROVED", "admissible terminal boundary", "Exact finite-N unbiasedness identities for the marked RB rewards."),
    ("ADRAFT-uniPIP", "§2.4 Uniform PIPs without (L+4)ρ*→0", "PROVED", "re-control each measured-round start via T12", "Uniform PIP consistency without the frozen second premise (independently supports W2-T26)."),
    ("ADRAFT-ThmD", "§2.4 Theorem D (n-indexed budgets)", "PROVED", "(P1) of W2-T26; bounded occupancy inequality; no proof of (P1) on masked designs", "Actual-budget bounded integrated-h consistency under T26's premise."),
    ("ADRAFT-CorD1", "§2.5 Corollary D1 (conditional statistical implication)", "PROVED", "full posterior concentrates about a generating θ*; uniformly locally continuous h", "Posterior-expectation consistency transfers to the generating parameter under continuity."),
    ("ADRAFT-CEXh", "§2.5 counterexample to unrestricted bounded h", "COUNTEREXAMPLE", "—", "h = 1{θ_j = θ*_j} has posterior expectation 0 under a continuous slab, so 'ground truth' consistency needs continuity of h."),
    ("ADRAFT-PropM", "§3.1 Proposition M (naive merging)", "COUNTEREXAMPLE", "identifiable cross-block proxy, fixed p; complete proof", "Naively merging local inclusion probabilities of two correlated predictors overcovers: both local inclusions → 1 while the full posterior excludes the proxy."),
    ("ADRAFT-v3exact", "§3.2 actual small-p v3", "PROVED", "exact scores; output availability", "At p = 2 v3 takes its exact branch, so its reported quantities are the full-posterior ones."),
    ("ADRAFT-SMCcomp", "§3.2 forced SMC component", "PROVED", "fixed n, N → ∞ (Theorem A)", "A forced SMC component converges to the full posterior as N → ∞ for each n."),
    ("ADRAFT-novelty", "§1 novelty audit (priority claim)", "OPEN", "six-paper audit cannot certify global priority; Lindsten et al. and binary-space SMC are direct precedents", "Whether the generic local-to-global SMC idea is novel; adverse evidence strong, reframe the contribution."),
    ("ADRAFT-uncert", "§1/§3.4 stronger uncertainty than complete Song–Liang", "OPEN", "needs a faithful comparator", "Whether v3's uncertainty beats the full two-stage Song–Liang method."),
    ("ADRAFT-maskedPIP", "§3.4 masked-regime PIP/evidence guarantees for unmodified v3", "OPEN", "T38 scores the truth but does not establish estimator guarantees; O-WSTAB separate", "Whether PIPs/evidence are accurate in the masked regime."),
]:
    r(pid, "none (original-draft track)", AD + " · " + lab, st, "N|none (author is the cross-family model; not a campaign verification)", N, "none", prem, mean)

# ---- F-DRAFT NEW_TARGETS.md (draft-to-v3 crosswalk; unverified) ---------------------------------------------
FD = "F-DRAFT · NEW_TARGETS.md (summary table)"
for pid, lab, st, prem, mean in [
    ("FD-W0", "W0 three faces of π/π₀", "PROVED", "EX-A; T13(i), T09(ii), T11(iii)", "The start-vs-posterior discrepancy has three equivalent faces: χ², sup ratio and π₀(S₀)."),
    ("FD-W1", "W1 exact d under block orthogonality", "PROVED", "block orthogonality", "Under BO the discrepancy d is exact; with known σ² the start equals the posterior."),
    ("FD-W2", "W2 null log-odds gap = dilution fraction × posterior gain", "PROVED-UNDER", "modulo EXP′ (candidate; now verified by W3-VEXP)", "Null-vs-truth log-odds at the start differ from the posterior by the dilution fraction."),
    ("FD-W3", "W3 cross-block covariance term", "PROOF SKETCH", "—", "Dropping BO adds a second additive cross-block covariance term to d (the draft's mechanism)."),
    ("FD-W(a)", "W(a) lower bound 1+χ² ≥ p^{R²−ε}/√n", "PROVED-UNDER", "modulo W2", "Weight instability lower bound in the favourable block-orthogonal regime."),
    ("FD-W(b)", "W(b) upper bound", "PROOF SKETCH", "second-moment aggregation", "Matching upper bound 1+χ² ≤ 1+p^{R²+ε}/√n+o(1)."),
    ("FD-W(c)", "W(c) sharp log log form", "CONJECTURE", "—", "log(1+χ²) = [R² log p − ½ log n]₊ + O_P(log log p)."),
    ("FD-W′", "W′ ideal-grid stage count", "CONJECTURE", "skeleton", "Number of adaptive stages ≈ ⌈log₂(1+1/g)⌉ + O(1)."),
    ("FD-W″-two", "W″ crossing cost, two-state case", "PROVED", "calculus", "A two-state masked crossing costs ≈ 3π stages."),
    ("FD-W″-window", "W″ crossing cost, general window", "CONJECTURE", "—", "A masked-regime crossing costs a bounded number of stages in general."),
    ("FD-W4", "W4 KL, TV small while χ² large", "PROOF SKETCH", "—", "Weight variance (χ²) can be large while KL and TV are small."),
    ("FD-NM", "NM naive merge fails (rigorous)", "PROVED-UNDER", "modulo T03/EXP′/Cor. P1", "Naive merge overcovers; the start inherits the error, the posterior does not; the correction is one flip (same phenomenon as ADRAFT-PropM)."),
    ("FD-P", "P partition as a random variable", "PROVED", "—", "Validity is partition-free; a mixture start and stochastic scheduling are valid if frozen before the final run."),
    ("FD-H", "H general h(θ)", "PROVED", "—", "Consistency extends from PIPs and Z to general h in one line."),
]:
    r(pid, "none (original-draft track)", FD + " · " + lab, st, "N|none", N, "none", prem, mean)

# ---- O-CERT ---------------------------------------------------------------------------------------------------
OC = "O-CERT · REPORT.md §3"
for pid, lab, st, prem, mean in [
    ("OCERT-LemmaM", "Lemma M (Q_S ↓, D_S ↑ in S)", "PROVED", "—", "Adding variables decreases the residual quadratic form and increases the determinant ratio."),
    ("OCERT-C1", "Thm C1 (one-sided global certificate)", "PROVED", "EX-A, EX-S, CAL, START, GUARD; SC(η_F) for floating point", "The locked Markov bound gives an upper bound π(Ŝ) ≤ e^{F(Ŝ)}/max(Z_𝒯, 0.05Ẑ), simultaneously for every model, at no selection cost."),
    ("OCERT-C2", "Thm C2 (two-sided band)", "PROVED-UNDER", "PW2 (T25(iv)), not data-checkable", "Cantelli gives a two-sided band on π(Ŝ) conditional on PW2."),
    ("OCERT-C3", "Thm C3 (exact relative certificates)", "PROVED", "any fully scored region", "π(Ŝ | R) is exactly computable on scored regions; π(S)/π(Ŝ) ≤ e^{−g} for every scored S."),
    ("OCERT-C4", "Thm C4 (box certificate)", "PROVED", "—", "A branch-and-bound over 2^U certifies Ŝ is the exact HPM among all models built from U."),
    ("OCERT-C5", "Cor. C5 (posterior-miss certificate)", "PROVED", "S₀ ⊆ U", "Any miss on {S₀ ⊆ U} is certified a posterior miss."),
    ("OCERT-C6", "Thm C6 (per-fit certificate card)", "PROVED", "Lemma RO; GUARD", "P(output and some card item false) ≤ 0.05 at every n; certifies optimality and uncertainty, not confidence."),
]:
    r(pid, "none (new: post-hoc certificates; supplement/remark)", OC + " · " + lab, st, "N|none", N, "none", prem, mean)

# ---- O-SWAP ---------------------------------------------------------------------------------------------------
OS = "O-SWAP · REPORT.md §3 (headline placeholder not yet filled)"
for pid, lab, st, prem, mean in [
    ("OSWAP-L0", "Lemma 0 (projection approximation PA)", "PROVED", "—", "Projection approximation used for the one-move probabilities."),
    ("OSWAP-P1", "Prop. 1 (within-size swap)", "PROVED-UNDER", "PA", "Finite-n probability that a same-size swap beats S₀."),
    ("OSWAP-P2", "Prop. 2 (superset by one null)", "PROVED-UNDER", "PA", "Finite-n probability that adding one null beats S₀."),
    ("OSWAP-P3", "Prop. 3 (subset: a truth dropped)", "PROVED-UNDER", "PA", "Finite-n probability that dropping a truth beats S₀."),
    ("OSWAP-T4", "Theorem 4 (first-order bracket)", "PROVED", "exact F (no PA needed for the inequalities)", "max_e p_e ≤ P(posterior miss) ≤ Σ_e p_e over the one-move events."),
    ("OSWAP-P5", "Prop. 5 (swap ceiling is information-theoretic)", "PROVED", "standard two-point bound", "No selector, prior or method can beat the swap ceiling: it is an information limit."),
]:
    r(pid, "supplement (n=200 posterior-miss theory)", OS + " · " + lab, st, "N|none", N, "none", prem, mean)

# ---- W6 drafts (repairs; not reviewed) ---------------------------------------------------------------------
W1c = "W6-FIXREV1 · CONSOLIDATED.md"
for pid, lab, mean in [
    ("W6F1-PropU′", "§1 Proposition U corrected (agrees with A-REV1; counterexamples re-evaluated with φ=1 kernels)", "Corrected undo classification: all three 'bad' alternatives kept; Theorem B shown unaffected."),
    ("W6F1-ThmB-conv", "§2 Theorem B boundary conventions", "Conventions for H = 0, a = 0, c* ≤ 0 and the capped quantity β_H."),
    ("W6F1-LemmaP", "§3 Lemma P multi-target sentence", "Explicit multi-target first-change bound."),
    ("W6F1-LemmaS′", "§4 Lemma S corrected", "ESS share inequality with the attainment domain f > 1−e."),
    ("W6F1-D2inf", "§5 D2 and D2-∞ with explicit rates", "Pilot route with explicit margins."),
    ("W6F1-E3′", "§6 Theorem E3 corrected (q < 1 restored)", "Start-mass lower bound with its locked hypothesis."),
    ("W6F1-LemmaU′", "§7 Lemma U corrected limiting constant (0.51/c_E)", "Corrected asymptotic constant."),
    ("W6F1-NL0′", "§8 NL0 quantifier form and downstream cost", "Sum-of-suprema form of the leakage premise."),
    ("W6F1-CE1′", "§9 CE1 narrow wording", "Explicit sequence on which H24's exit premise fails."),
]:
    r(pid, "(repair of an A-REV1 finding)", W1c + " " + lab, "PROVED", "N|none (W6-FIXREV1 REPORT.md not yet pushed; draft)", "N|not yet reviewed by another model family",
      "this is the repair; supersedes the corresponding rows once reviewed", "—", mean)
r("W6F1-T38", "Thm 5", "W6-FIXREV1 · T38_STATEMENT.md / T38_PROOF.md", "PROVED-UNDER", "N|none (draft)", "N|not yet reviewed", "supersedes W4-T38FULL's T38 files once reviewed", "as W4 T38 with A-REV1 §7 qualifications",
  "A-REV1-compliant restatement of T38 (pilot rates for b1′, eligible-set interface for b2, execution/usability terms).")
W2s = "W6-FIXREV2 · STATEMENTS.md (draft; REPORT.md not yet pushed)"
for pid, lab, mean in [
    ("W6F2-LemmaT", "§2.2 Lemma T (tie lemma; replaces S37's 'TD′_P ⟺ (L) ∧ ⋂ D_S')", "Exact-ties-aware equivalence for TD′_P (new write-up of A-REV2 §4.3)."),
    ("W6F2-LemmaNT", "§2.2 Lemma NT (exact ties are null events under joint non-degeneracy)", "Exact ties have probability zero when the compared sets are jointly non-degenerate."),
    ("W6F2-Lemma0′", "§2.4 Lemma 0 corrected, (b′) (replaces S37 Lemma 0(b) and V37 R2)", "Corrected delivery-only-on-E_LS statement."),
    ("W6F2-PropF", "§2.4 Proposition F (exhaustive failure partition; A-REV2's F_pre/F_post categories)", "Every failed final search falls into one of three score-comparison categories."),
    ("W6F2-ThmA′", "§2.3 Theorem A (tie-aware, POS repair)", "Refined T37(i) restated with the exact-ties-aware definition of TD′."),
]:
    r(pid, "Thm 3 (repair of an A-REV2 finding)", W2s + " " + lab, "PROVED", "N|none (draft)", "N|not yet reviewed by another model family",
      "this is the repair; supersedes the corresponding rows once reviewed", "—", mean)
r("W6F2-rest", "Thm 1 / Thm 2", W2s + " §1 T03♯, §3 EXP′/Thm 3/Thm 4/Lemma U", "PROVED", "N|none (draft)", "N|not yet reviewed",
  "re-states the already-verified T03♯, EXP′ (0.51/c_*), R1-cert; Lemma U budgeted — items not separately extracted", "—",
  "Corrected paper-ready restatements of rows already in this registry (T03♯ etc.); not counted as new results beyond the draft flag.")


# ===============================================================================================================
# THIRD FETCH: W6-FIXREV1 REPORT.md (a7833f3) and W6-FIXREV2 REPORT.md (05073fd) have landed.  They are same-family
# repair runs; they agree with every A-REV finding (FIXREV2 adds two wording qualifications) and have NOT been
# reviewed by a second model family.  Repair state therefore becomes "applied (W6, unreviewed)".
# ===============================================================================================================
W1TXT = "applied in W6-FIXREV1 REPORT.md (same-family, not yet reviewed by a second family)"
W2TXT = "applied in W6-FIXREV2 REPORT.md (same-family, not yet reviewed by a second family)"
for row in ROWS:
    t = row["rep"]
    t = t.replace("W6-FIXREV1 draft landed (CONSOLIDATED.md, unreviewed)", W1TXT)
    t = t.replace("W6-FIXREV1 draft landed (unreviewed) / W6-FIXREV2 PENDING", "applied in W6-FIXREV1/2 REPORT.md (same-family, not yet reviewed)")
    t = t.replace("W6-FIXREV1 draft landed / W6-FIXREV2 PENDING", "applied in W6-FIXREV1/2 REPORT.md (same-family, not yet reviewed)")
    t = t.replace("W6-FIXREV2 PENDING", W2TXT)
    t = t.replace("W6-FIXREV1/2 PENDING", "applied in W6-FIXREV1/2 REPORT.md (same-family, not yet reviewed)")
    t = t.replace("W6-FIXREV2 'confirm' PENDING", "confirmed in W6-FIXREV2 REPORT.md (same-family)")
    row["rep"] = t
    if row["rs"] == "pending":
        row["rs"] = "applied"
        row["flags"] = row["flags"]  # unchanged

upd("ThmC-C1", rep="W3-VT37R R4 (sketch); W6-FIXREV2 carries the A-REV2 correction, status stays PROOF SKETCH (GAP stands)")
upd("ThmC-C2", rep="W3-VT37R R5 (sketch); W6-FIXREV2 keeps PROOF SKETCH (GAP stands)")
upd("R3-LHiid(VEXP)", rep="W6-FIXREV2 keeps PROOF SKETCH; B ≥ 2g packing GAP stands")
upd("Lemma0(b)", cf="E|" + A2 + " §4.2: 'Lemma 0(b) as written' ERROR; V37 R2 repair also ERROR. (W6-FIXREV2 qualifies A-REV2's table row 'initial-centre-is-truth trivial success': a search from S₀ moves away unless (L) holds at S₀.)")
upd("Lemma0(a,c)", cf="V*|" + A2 + " S37 Lemma 0(a),(c) VERIFIED; W6-FIXREV2 §3.1 disputes only A-REV2's table wording 'initial centre is the truth is trivial success' (needs (L) at S₀)")
upd("T38-(0)", cf="V*|A-REV1 §7.4 repaired composition proof VERIFIED (same set argument as locked T21(C1)). Scope: A-REV1 reviewed W1-T38E's T38(b)-R, not W4-T38FULL (W6-FIXREV1 §3.1); the printed T38(b)-R as a whole is GAP; fixed by W6-FIXREV1's T38 files")
for row in ROWS:
    if row["id"].startswith("W6F1-") or row["id"].startswith("W6F2-"):
        row["sf"] = "N|none (REPORT.md landed; same-family run; not reviewed)"
        row["src"] = row["src"].replace("(draft; REPORT.md not yet pushed)", "(REPORT.md landed)").replace("CONSOLIDATED.md", "REPORT.md + CONSOLIDATED.md") if row["id"].startswith("W6F1-") and "REPORT.md +" not in row["src"] else row["src"].replace("(draft; REPORT.md not yet pushed)", "(REPORT.md landed)")
        row["cf"] = "N|not yet reviewed by another model family"
upd("W6F1-T38", sf="N|none (REPORT.md landed; not reviewed)", cf="N|not yet reviewed", src="W6-FIXREV1 · REPORT.md + T38_STATEMENT.md / T38_PROOF.md")
upd("W6F2-rest", sf="N|none (REPORT.md landed; not reviewed)", cf="N|not yet reviewed", src="W6-FIXREV2 · REPORT.md + STATEMENTS.md §1, §3")


# ---- W5-B2ENV referee of W4-SHARE (same-family; REFEREE.md, fourth fetch) -------------------------------------
BV = "W5-B2ENV · REFEREE.md verdict table"
for pid, code, txt in [
    ("SHARE-D4", "V*", "D4 Steps 1–5 VERIFIED; citation GAP only (conditional-iid step should cite IND-T/Lemma S of W2-PREM)"),
    ("SHARE-D5", "V", "D5 bound (2.1), consequence and Remarks 2–3 VERIFIED"),
    ("SHARE-G", "V*", "Prop. G VERIFIED as an upper bound; wording GAP: it is not 'grid independence' of Γ"),
    ("SHARE-SH", "V*", "Prop. SH (i),(ii) and exact law VERIFIED; 'transition at log(Nπ₀(a)/π₀(o))' is a heuristic (label it); factor-2 sharpness holds in the two-state example only"),
    ("SHARE-X", "V*", "Prop. X main inequality VERIFIED; 'Moreover' clause GAP (needs a visit-form rate and an independence-proposal term N(T+L+4)π₀(S₀)); 'Use' clause GAP (calibration and final search not bounded)"),
    ("SHARE-M(a)", "V", "Prop. M(a) VERIFIED (20,000 random instances, 0 violations)"),
    ("SHARE-M(b)", "V*", "Prop. M(b) PROOF SKETCH as labelled, argument correct; W5-B2ENV upgrades it on LH to PROVED in its own PROOF.md §3 (Prop. M-LH; not read here)"),
    ("SHARE-PD", "V*", "Lemma PD identity VERIFIED; 'a takeover needs these two premises' is a mean-field heuristic"),
    ("SHARE-B2W4", "V", "Theorem B2-W4 VERIFIED given its inputs; note L+5 rounds after stage T"),
]:
    upd(pid, sf=code + "|" + BV + ": " + txt)
upd("SHARE-C1BVS", sf="N|none")
claim("PropX-moreover", "SHARE-X", SH + " · Prop. X 'Moreover' and 'Use' clauses", "G|" + BV + ": GAP (two missing terms; and not a bound on the method's miss probability)", "N|none",
      "repair stated in W5-B2ENV referee text (visit-form gate rate; independence term)", "applied", "The claim that the gate obstruction bounds the chance of scoring S₀ needs mid-round visits and the independence proposal accounted for.")
claim("PropG-wording", "SHARE-G", SH + " · Prop. G 'grid independence'", "G|" + BV + ": GAP (wording)", "N|none", "reword as an upper bound (W5-B2ENV)", "applied",
      "Γ ≤ max κ is grid-free as a bound, not as a value.")
claim("B2ENV-finding", "Thm 5 (b2) on LH", "W5-B2ENV · REFEREE.md closing finding (PROOF.md §4, not read)", "N|n/a", "N|none", "none", "none",
      "On LH the natural potential h_t = 1_𝒩 gives κ_t ≡ 0 and Γ = 0 so D5 collapses to Prop. X; the lattice-indicator potential fails at the v3 budgets (Γ ≳ log(N/T_e)).")


# final sweep: any remaining 'PENDING' wording in a repair that W6 has now written
import re as _re
for _row in ROWS:
    if "PENDING" in _row["rep"] and _row["rs"] == "applied":
        _row["rep"] = _re.sub(r"\s*—?\s*PENDING", " — now written in the W6-FIXREV REPORT.md (same-family, not yet reviewed)", _row["rep"])
        _row["rep"] = _row["rep"].replace("to be adopted by W6-FIXREV1 now written", "adopted").replace("fix = W6-FIXREV2 now written", "fix")
