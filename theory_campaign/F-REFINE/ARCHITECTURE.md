# F-REFINE — ARCHITECTURE: the paper's theorem architecture after waves 1–4

Lead: F-REFINE (Fable 5.1), 2026-11-02, branch `theory/F-REFINE`. Read with `CARDS.md` (statements, evidence,
sources, probabilities) and `NEXT_TASKS.md` (what to run next). Nothing here is adopted.

> **Amended 2026-11-02 (E-SPINE, wording only; no status word changed).** This draft no longer implies that tempering,
> or "the sampler", is *needed*. W7-SEP (858004e · `REPORT.md` · Prop. GU, Cor. GU-LH) shows that on LH, start-only
> discovery plus the production local search scores S₀. What the theory supports is **"moving off the start is needed"**.
> Also: LS0 is effective (O-LS0 02348e2: 0/2,394 HPM changes); S-ELS counts; no-LS0 masked candidates pending A-REV7;
> the "favourable from n ≈ …" figure is dropped. See `main:Docs/Theory/AMENDMENTS_20261102.md` (branch `theory/E-SPINE`).

## 1. The story, as it can honestly be told now

What SMC-BVS reports is consistent because the truth gets **scored** and the posterior **ranks** it first. The
reported HPM is the best model ever scored (every scan, both Gibbs configurations, rejected proposals, LS0 if used).
So the error decomposes, for every n and every data set, as

  P(output and Ŝ ≠ S₀) ≤ 2E₀[1 − π(S₀)] + P(output-potential run never scores S₀)        (Thm 4, exact)

and the paper proves the two terms vanish in two different ways:
- the **posterior** term by Thm 1 (T03♯: anchored, size-restricted sparse eigenvalue conditions and beta-min);
- the **discovery** term either because the start already finds the truth (Thm 2 favourable regime + iid draws:
  Thm 5(a)), or because the start lands *near* the truth (Thm 2 masked regime, reference S°) and a deterministic
  greedy repair from that reference scores it (Thm 3 + LS0: Thm 5(b1)).

**What discovery needs (amended 2026-11-02).** In the masked regime the run must **move off its start**: iid start
draws alone fail (Thm 2 masked start / T27; W7-SEP Theorem SEP(A), Q* = p^c n^{c/2}). v3's moves supply this: bridge
Gibbs, the terminal rounds (O-BGIBBS BG3 on LH, p fixed) and the local search incl. LS0 (W7-SEP Prop. GU). The tempering
bridge is one of several sufficient discovery routes, not the uniquely necessary one. Its own role is the calibrated
evidence and PIPs (Prop 2, Thm 6) and the HPM ledger.

Thm 6 (evidence and PIPs) and Prop 2 (frozen-run identities, 95% bound) say the *other* reported quantities are
consistent in the favourable regime and unbiased for every n. Prop 1 says the HPM is the right decision and names the
one error no size prior can fix.

What the story can **not** say: anything numerical at n = 200. The study's start is dilution-masked (6–12 of 14
truths missing at every signal scale), its misses are posterior misses, the sampler delivers the HPM through Gibbs
flips (a route with no completed theorem), and the T03 proof thresholds begin near n ≈ 2·10⁶. The theorems explain
the mechanism; the simulations are evidence in their own right.

## 2. Dependency graph

Node labels: [L] locked; [P] campaign PROVED, same-family VERIFIED; [p] campaign PROVED, unverified; [S] PROOF
SKETCH; [C] CONJECTURE/OPEN; [I] implementation fact; [X] COUNTEREXAMPLE (retired). "⇒" is a proof dependency.

```
                                   ┌──────────────────────────────────────────────────┐
                                   │ Thm 4 (T21) exact composition, every n   [L]+[P] │
                                   │  P(𝒪, Ŝ≠S₀) ≤ 2E₀δ₁ + P(𝒪̄, S₀∉𝒮̄)                 │
                                   │  Lemma RO [p] · GUARD [I] · SR [I]               │
                                   └───────────┬──────────────────────┬───────────────┘
                     posterior term            │                      │   discovery term
                                               ▼                      ▼
   ┌────────────────────────────┐    ┌──────────────────┐   ┌─────────────────────────────────────────────┐
   │ Thm 1 (T03♯) [P]           │    │ Prop 1 (T07) [L]+│   │ Thm 5 (T38): routes for the discovery term   │
   │  T02(i♯) exact tail [P]    │    │  [p] sharp       │   │  (0) composition [P]                         │
   │  SE_λ(j₀)+SE_w(m♯;g₀)+BM   │    │  ceiling;        │   │  (a) favourable  ⇐ Thm 2(ii)(iii) + T11(iii)│
   │  ⇒ δ₁→0 =: (P)             │    │  certificate     │   │  (b1) LS0 ⇐ (M1)(M2)(M3)  [P, unreviewed]   │
   └──────────┬─────────────────┘    └──────────────────┘   │  (b1′) D2 ⇐ Dep, NB′, π₀(x°)>1/10 [P|S]     │
              │ (P) also feeds Thm 6 and Thm 5(0)           │  (b2) envelope ⇐ TRACK, Γ, REP   [p|C]      │
              ▼                                             │  (c) cost ⇐ T32(i) [C]                       │
   ┌────────────────────────────┐                           └──────┬──────────────┬───────────────┬────────┘
   │ Thm 6 (T26 i–ii) [p]       │                                  │              │               │
   │  (P1): (T_n+1)Δ_n → 0      │        ┌─────────────────────────┘              │               │
   │  Δ_n = max{1−π₀(S₀), δ₁}   │        ▼                                        ▼               ▼
   │  ⇐ (P) + Thm 2(iii)        │  ┌────────────────────────────┐  ┌──────────────────────┐  ┌─────────────────────┐
   └────────────────────────────┘  │ Thm 2 (T22+T27)            │  │ Thm 3 repair         │  │ W4-SHARE envelope   │
                                   │ (i) deterministic [L]      │  │ A: TD′ exact [P]     │  │ D4/D5/B2-W4 [p]     │
   ┌────────────────────────────┐  │ (ii) EXP′ theorem [P]      │  │ LS-score [P]         │  │ Prop M: no barrier  │
   │ Prop 2 (T12+T31i) [L]+[p]  │  │ (iii) favourable (F1/F2/F3)│  │ B: finite-n union [P]│  │   near truth [p|S]  │
   │  islandwise identities;    │  │     [L cond]+[P]           │  │ W: PGD+LD♭ ⇒ TD′ [p] │  │ C1: bridge mass ⇏   │
   │  pooled×pooled ≠ identity; │  │ (iv) CL(L) ⇒ T27(i) [P]    │  │ M + LH-LAT margins[P]│  │   delivery [X]      │
   │  Lemma RO; VAL-FP          │  │ (v) LH joint family [P];   │  │ B′/B♯ Gibbs path [P] │  │ SHARE, LT retired   │
   └────────────────────────────┘  │     LH-iid p≫n [p]         │  │ IND-T [p]; H24 [X]   │  └─────────────────────┘
                                   └────────────────────────────┘  │ literal TD [X]       │
                                                                   └──────────────────────┘
```

Edges that matter for review order:
- (P) is used by Thm 4, Thm 5(0) and Thm 6. Thm 1 is the root of everything on the posterior side.
- Thm 2(ii) EXP′ is used by Thm 2(iii), Thm 5(a), Thm 6 (via (P1)), Thm 3-W (Lemma U is its general-set form), and
  Thm 5(b1-LH) (through W1-EXP Thm 5/6 at the reference S°).
- Thm 3-A and LS-score are used by Thm 5(b1); Thm 3-W is the *general* sufficient condition for (M2) but Thm 5(b1-LH)
  uses the direct margin Prop. LH-LAT instead. Thm 3-B′ is used by Thm 4 (e′) and Thm 5(b2) REP.
- W4-SHARE D4/D5 replaces the open inputs SHARE/LT of Thm 5(b2) by checkable ones; no instance yet.
- Prop 1 and Prop 2 are leaves (no theorem depends on them).

## 3. Joint families (Astra's requirement: one family must satisfy every premise used together)

| Family | p vs n | Carries jointly | Status |
|---|---|---|---|
| **ORTH** (X′X = (n−1)I, p ≤ n−1, fixed θ) | p < n | Thm 1 (locked T03); Thm 2(iii) via (F1)/(F2); Thm 5(a); Thm 6 (P1) | compositions PROVED/SKETCH (W2-T26 Prop. C, W4-T38FULL §2.3); rates √(log n/n) attained numerically |
| **LH, exact Gram** (linked hubs, \|ψ\| < ρ, g ≤ B < 2g) | p ≤ n−1 | Thm 1 (locked T03); Thm 2(v) masked start with b_n → 1 at S° = S₀∖M; Thm 3-C margins (LH-LAT); Thm 5(b1) with LS0; Thm 3-B′ premises (Theorem L, sketch) | all (b1) premises PROVED (W1-EXP + W4-T38FULL), same-family verified, **cross-family review pending** |
| **LH-iid** (iid Gaussian rows, n^a ≤ p ≤ n^A) | **p ≫ n** | same as LH plus the 2^B-free start rate, partition = groups, D2 for c = 1 | PROVED by W3-PXN, **unverified single run** |
| CF(c) (W1-T38E) | p = n^{3/4} | (b1)+LS0 numerically at n ∈ {400, 1600} | finite-n numerics only; superseded by LH |
| none | — | (b1′) for c ≥ 2; (b2) envelope inputs | OPEN |

The study's own designs (groups of 5, B = 14) are **outside** LH (co-blocking kills cancellation masking, W3-PXN
Prop. Q) and, at n = 200, outside every fixed-s₀ regime (dilution). The paper cannot present LH as the study's
masking; it presents it as a masked regime in which the method must move off its start (not one that requires
tempering: W7-SEP Prop. GU).

## 4. What the paper claims without LS0, and what LS0 adds

**Without LS0 (original method), all PROVED or PROVED-LOCKED, pending review:**
1. Thm 4 (C1) for every n; Thm 5(0) in the strong form P(𝒪, Ŝ ≠ S₀) ≤ 2E₀δ₁ + D_n.
2. Thm 1 (T03♯), Prop 1, Prop 2, Thm 6 in full.
3. Thm 2 in full: EXP′ as a theorem, favourable start under (F1)/(F2)/(F3) at any reference, masked start under
   CL(L), the LH family realising both.
4. Thm 3 in full as a statement about the local search *from a given centre* (Theorem A exact; Theorem W asymptotic;
   LH-LAT margins) and about the Gibbs path *from a given particle* (Theorem B′/B♯, P1, B-M).
5. Thm 5(a): favourable-regime HPM consistency, unconditional on ORTH.
6. Thm 5(b1′): one-flip masking repaired by the pilot's first stage, **conditional** on D2's statistical instance
   (NB′ unfinished even on LH with c = 1); Thm 5(b2): conditional on the envelope inputs (no instance).
7. The negative results: literal TD false; H24's asymptotic input false; bridge mass ⇏ delivery (C1); the brief's
   eligibility condition fails under omission masking (E1); pooled × pooled is not an identity; conditioning on
   completion biases Ẑ.

So without LS0 the paper has **no masked-regime consistency theorem whose premises are all proved on an explicit
family**. The main theorem's masked half would be a conditional theorem plus a family on which every premise except
delivery is proved. *(Amended 2026-11-02: out of date. There are now no-LS0 **candidates on LH, pending cross-family
review (A-REV7)**: D2-LH (c = 1), W5-VMASK R1, B2-LH under STAB-LH, O-BGIBBS BG3 + LH-lock (sketch), F-SHARE F1/F2 and
W7-SEP Prop. GU (W8-SYNTH §4.2). None is closed beyond a single run or a sketch.)*

**With LS0 (one deterministic extra local search from the exact start mode, centre emitted, ≈ (ℓ+1)max_k[p+k(p−k)]
scores, addable post hoc):**
8. Thm 5(b1) and (b1-LH): masked-regime HPM consistency with every premise proved on LH (p < n), and on LH-iid
   (p ≫ n) once W3-PXN is verified. This is the headline the frozen list asked for.

What LS0 does **not** buy: any change at n = 200 (it cannot fix posterior misses; the start mode is 8–14 moves away
and ℓ = 10–11 binds in S4/S6; W3-PXN's post-hoc numbers are 113/128 scored when |S̃₀ Δ S₀| ≤ ℓ+1, 13/32 beyond), a
theorem for route (b2) (which is how the method actually finds the HPM at the study size), or evidence/PIP claims
in the masked regime.

**LS0 under the investment rule.** It is a method change, so (1) with it all or most key results must be provable:
yes, it closes the only hole; (2) a pilot must show the method still performs: O-LS0 (Owls) is running LS0 post hoc
on the 2,400 regenerated datasets; its only possible effect on the reported HPM is improvement (more scores), so the
performance question is cost. *(Amended 2026-11-02: O-LS0 has landed (02348e2): 0 of 2,394 reported HPMs changed,
exact recovery unchanged, cost < 0.1% of a fit. Felipe's approval is therefore effective, and LS0 is part of the method.)* Implementation requirements (W3-VT38E, W4-T38FULL): `emit_centre = true`; a fixed
argmax-π₀ tie rule (the HPM rule); provenance labels on refits; optionally let LS0 run to certification. One redeploy
carries all changes together.

## 5. Journal cuts

### JRSS-B main text (8), with the believed versions

| # | Result | Content (believed version) | Status | Main-text wording risk |
|---|---|---|---|---|
| Thm 1 | T03♯ (+T01, T02 lemmas) | posterior concentrates on S₀ under anchored, size-restricted SE + beta-min; exact BB tail | PROVED, VERIFIED | asymptotic only; thresholds ~2·10⁶ |
| Prop 1 | T07 + T06(i) | HPM/MPM Bayes rules; sharp size-prior ceiling; same-size-swap certificate | PROVED | within-size errors only |
| Thm 2 | T22 + T27 | deterministic start bounds; EXP′ theorem; favourable start at a reference; CL(L) masking law; LH realises both | PROVED, VERIFIED (exact Gram) | rates vacuous below n ~ 10⁹ (2^B); iid-draw bound only |
| Thm 3 | Theorem A + Theorem W (+ LH-LAT) | greedy repair ⇔ TD′ (exact, finite n); TD′ w.p. → 1 under PGD + LD♭; explicit margins on LH | A: PROVED, VERIFIED; W: PROVED, unverified | "works whenever the posterior allows"; not the n = 200 mechanism |
| Thm 4 | T21 | exact composition on R̄ under GUARD; routes (a), (d)/(d⁺), (e′)/(e-M) | PROVED | report P(U) |
| Thm 5 | T38 | two-regime HPM consistency; (b1) with LS0 on LH; (b1′), (b2) conditional | (0)(a)(b1) PROVED, same-family verified | LS0 dependency; dilution disclosure |
| Thm 6 | T26 (i)–(ii) | Ẑ and PIP consistency under (T_n+1)Δ_n → 0, favourable only, output form | PROVED, unverified | realised T_n, not T^max |
| Prop 2 | T12 + T31(i) | islandwise identities; pooled product; 95% bound at output level; VAL-FP | PROVED | never "given completion" |

Supplement: Theorem B′/B♯ (restated T24) with IND-T, P1, B-M and the premise table; the finite-n union bound
(Theorem B of W1-T37R); W4-SHARE D4/D5 as the conditional (b2) route; the negative results; T05 remark; T06, T33,
T34 (with the run/output clause); the n = 200 disclosure.

### Biometrika cut (5)
Thm 1 (T03♯); Thm 2 (T22 with EXP′ and the LH family; T27 as a remark); Thm 3 (Theorem A, with Theorem W as the
asymptotic clause); Thm 4 (T21); Thm 5 (T38 with (a) and (b1)+LS0 only; (b1′)/(b2) as remarks). T07, T26 and T12
become remarks. If LS0 is **not** adopted, Thm 5 shrinks to (0) + (a) and the masked regime becomes a conditional
remark; the paper then has no headline masked theorem and should lead with Thm 3 + Thm 4 as the finite-n contribution.

## 6. Overstatement watch (must not appear in the paper, or must be disclosed)

1. Literal T37 / TD(d, m) in any form; "exactly |S Δ S₀| moves"; the 2^{s₀} union bound; "T37 replaces GAIN, LK,
   EXIT" (it does so only for the local-search route and only on E_LS).
2. H24 or any uniform-over-𝓡_d exit hypothesis; the (1−c′)^{⌊H/(s₀+d)⌋} form; T24's factorial.
3. "The exact BB tail makes SE meaningful at n = 200": false; the cap K does, and only for the unnormalised SE_w;
   "anchored" SE is equivalent to unanchored up to s₀ columns (Lemma A1).
4. Any finite-n error rate at n = 200 from Thm 1, 2, 3(iii), 5 or 6. The single non-vacuous finite-n statements are
   exact inequalities: Thm 4 (C1), Theorem A, Lemma S, Cor P1 (at B = 4), Prop 2.
5. "The masked regime of Thm 5 is the study's masking": no; the study is dilution-masked, and LH's cancellation
   cannot survive the study's partition (groups of 5 ≤ B/2).
6. "The correlated-design advantage follows from T37's margin": contradicted at n = 200 by the c = 0.5 posterior
   misses in S4–S6; state the LH-LAT margin as the mechanism on LH, nothing about the study.
7. "The local search repairs": at the study size it repaired 0 fits; Gibbs flips deliver 98% of fresh scores.
   *(Amended 2026-11-02, S-ELS: the final local search made 0 moves in all 2,394 completed fits, and E_LS is empty
   (0/2,394); all 541 near-truth centres are forced by monotonicity.)*
8. "T27 is a lower bound for the method": it bounds iid start draws only.
9. "T26 with budgets indexed by n": the deterministic-budget form (T^max = 4,000) is vacuous below n ~ 10⁸; state
   (P1) with the realised T_n.
10. "E[Ẑ | completed] = Z" and "pooled Ẑ × pooled PIP is unbiased": both false.
11. The cost corollary as a theorem: T32(i) is a conjecture.
12. "VERIFIED" as if reviewed: all verification so far is same-family.
13. D2 "covers one-cancellation masking at p ≫ √n": conditional; its CF instances are not masked.
14. "No method change needed": true for everything except Thm 5(b1), which is the headline.
15. *(Added 2026-11-02.)* "Tempering is needed", "the sampler is needed" or "start-only methods fail" for discovery:
    false on LH, where a single local search from the start mode scores S₀ (W7-SEP Prop. GU, Cor. GU-LH). Say: the
    method must move off its start (iid start draws alone fail), and v3's moves provide this. The bridge's own role
    is calibrated evidence/PIPs and the HPM ledger.

## 7. The n = 200 disclosure (consolidated; one paragraph for the paper)

At the study's size (n = 200, p ∈ {500, 1000}, s₀ = 14) the theorems are statements about mechanism, not about the
reported numbers: (i) the block start is masked by dilution (each truth is scored against the other 13 as noise), so
the start mode misses 6–12 truths at every signal scale (no "favourable from n ≈ …" figure is quoted: the campaign's
estimates disagree, W8-SYNTH §4.13); (ii) every completed wrong HPM has F(S₀) < F(HPM) (565 of 2,394 fits; 0 search
misses; S₀ scored in every completed fit, and the final local search never moved: S-ELS; 6 resource stops, all in S5,
counted as misses); (iii) the sparse-eigenvalue premise of Theorem 1 now ranges over ≤ 114 columns because the
cap K = 100 binds, but it is unverified on the realised designs, the beta-min constant exceeds the executed signals
by ≥ 43×, and the proof's deterministic thresholds hold from n ≈ 2·10⁶; (iv) the start rates carry a 2^B factor that
is ≥ 10³ at B = 14 for n ≤ 10⁴; (v) the HPM at this size is found by Gibbs flips during the bridge and terminal
rounds, a route for which the paper proves exact finite-n inequalities but no rate.

## 8. Open items, ranked by value to the paper

1. Cross-family review of the masked instance: W4-T38FULL Lemma M / LS-score / LH-LAT and W3-PXN Lemma B / P3 / P6.
   Cheap; load-bearing.
2. The LS0 decision (Felipe) and the O-LS0 pilot. *(Done 2026-11-02: O-LS0 passed; approval effective.)*
3. Verification of W3-PGD Theorem W (Thm 3's asymptotic clause has no referee and its REPORT is a stub).
4. A no-method-change masked instance: NB′ for D2 on LH (c = 1), and the envelope route (b2) on LH via D5 + Prop M
   (the route that matches how the method behaves).
5. A 2^B-free favourable rate on iid designs with the actual partition (closes Thm 5(a) and Thm 6's relevance for
   study-like designs; W3-PXN's method).
6. GUARD / OUT / SR code audits; T32(i) proof; VAL-FP replay (operations).
7. The E_LS ledger extraction (per-fit F(S₀) − F(final centre)) and the same-size-swap count (data, Owls/R).
   *(E_LS done 2026-11-02 by S-ELS: empty in the data.)*
