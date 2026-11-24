# Cor 9C note check — reply of the checker (Claude Opus 5.5, effort high, Claude Personal), verbatim
<!-- received 2026-11-17 via delegate_task; brief BRIEF_COR9C_check_opus.md; note at b589aa6a -->

**Cor 9C note check: accept with changes. N1 and N2 hold, and N3 is right. The §4 recording entry is the part that needs fixing: it drops a hypothesis that N2 needs.**

I worked read-only in `/home/fb31/BVS-wt/W3-D5P` (HEAD b589aa6a) and wrote nothing. The cited W3-DIST, W3-RM, W3-RM2(-R), W3-READER and L1_POST files show no diff against origin/main (7e7fafaa). The registry entry for `W3-DIST:Cor-C` (`Theory_work/INFRA/registry/claims.tsv:490`) matches the status the note quotes in §4, word for word.

**Quotation and objects.**
- The premise quote at `W3-DIST/STATEMENT.md:227-231`, the sentence at :237-238, the exclusion at :219, the "n independent copies" at :136 and the statement span :217-238 are all correct.
- (A1)–(A5) themselves sit at :174-180; :185-187 is Theorem A's preamble that fixes M.
- The objects are the same. DIST's own code facts (`W3-DIST/STATEMENT.md:273-283`) pin the same core, 4676af6. They also define 𝒯 = `top_store`, with values F(S) = log ϖ + log m (CC2), and π_𝒯 ∝ e^F. LIST-CODE (iii) and §1 match this, including Ω = {|S| ≤ min(p_ret, ⌊n/2⌋)} against DIST's cap min(r, ⌊n/2⌋). "Completed" means the same in both: LIST-CODE (i) gives status `completed` if and only if `estimates_available` is TRUE on the sampler branch, and that branch is DIST's scope.

**N1: IMPLIES.**
- LIST-CODE (i) (proof B2–B4) shows that on 𝒦_n every completed run's LS0 is 𝒦_n's deterministic search, so S₀ is offered to the final-run ledger.
- (v) (proof F, with the TopStore invariant D2) shows that on 𝓜_n, S₀ is the best offered model and so is kept in the list.
- Since π ≥ 0, π(𝒯) ≥ π(S₀ | y). Each step holds for every seed, N_e, R′ and calibration outcome, and the case s₀ > K is covered by the stated convention.
- The scope is narrower than "law-free" suggests: it also rests on LIST-CODE's code-level premises (see F2).

**N2: IMPLIES.**
- Take the intersection of Corollary C's good data event with 𝓜_n ∩ 𝒦_n ∩ {π(S₀ | y) ≥ n^{−cM/2}}, apply N1, and use a union bound. All four sets are data events.
- The last term goes to 0 because, once n^{−cM/2} ≤ ½, {π < n^{−cM/2}} ⊆ {π < ½}. Hypothesis (c) is stronger than needed but enough.
- Hypothesis (c) cannot be dropped. Theorem A has no beta-min condition, and even on 𝓜_n Theorem A (ii) only gives π(S₀) ≳ n^{−A(s + C₁M)}, which is far below n^{−cM/2}.

**N3: AGREE.**
- The two laws are disjoint when s₀ ≥ 1. A cleaner argument than the note's: under an i.i.d. (A1) law with Gaussian rows, Cy^r given X^r is N(X·D_x·β*, σ²C), where D_x holds the sample standard deviations. Setting R would need X·D_x·β* = Xθ* almost surely with θ* fixed. That fails because sd_n(x_j) has a continuous law whenever β*_j ≠ 0. This covers both RM's form Y = Xθ* + Cε and READER's y^r = α1 + Xθ* + ε.
- No recorded result closes the gap:
  - **B6.7** (`READER_VERSIONS.md:762, :1404`) says the raw-scale version would need a new bridge and is not proposed.
  - **W3-RM2 / W3-RM2-R** have no raw-scale or uniform-over-design statements. They state SAND-R, NA and TL under the joint law with θ* fixed (`W3-RM2/lemmas/L4_sandR_b.md:21-41`).
  - **Setting F** (`W3-RM2/STATEMENT.md:50`; RM :34-40) is the one candidate. It is a raw-scale model and, conditional on X^r, it is exactly Theorem A's law. But its design hypotheses are deterministic, and no recorded result shows random designs meet them. Its leakage condition (L-gain), δ²_{U,l} ≤ η·τ²_U·log n with η < η_A ≈ 1/(8A), should typically fail for Gaussian designs with about n^A null columns. That is my own rough calculation, not a recorded result: the largest null δ²_{∅,l} is about 2A·‖θ*‖²·log n. So this route is not a free closure.
  - **L1_POST** gives (c) on the raw scale only as a parenthetical [R02-3] (`L1_POST.md:12-18`), and under POST's extra hypotheses (see F5).

**Findings.**

F1 — §4 is not faithful to N2, the main problem (`COR9C_NOTE.md:59-61`, `:68-69`).
- *What fails:* the Edge line says LIST-CODE implies the premise "pathwise on 𝓜_n ∩ 𝒦_n", and makes the probability-level discharge "conditional on P(𝓜_n ∩ 𝒦_n) → 1". The notes-append sentence says "with probability → 1 under any data law carrying Theorem A's conditions and P(𝓜_n ∩ 𝒦_n) → 1". Both drop the condition π(S₀ | y) ≥ n^{−cM/2}, and hypothesis (c) with it. Without it, the premise does not follow (see N2).
- *Fix:*
  - Edge line: "pathwise on 𝓜_n ∩ 𝒦_n ∩ {π(S₀ | y) ≥ n^{−cM/2}}".
  - Both places: "conditional on P(𝓜_n ∩ 𝒦_n) → 1 and P(π(S₀ | y) < n^{−cM/2}) → 0 (e.g. π(S₀ | y) → 1 in probability)".

F2 — the code-level premises are missing from N1 and §4 (`:22-28`, `:62`).
- *What fails:* N1 and the Edge line say "law-free; no IMPL-LIST" but leave out what LIST-CODE does rely on: the code of record, the shipped configuration (`ls0 = TRUE`, cap `ell_n_plus_mode`, `ls0_ell` = ℓ_n, `ls0_tie_dp = TRUE`), EX-A, EX-S and SR, with "every completed run" read over admissible runs (RM `STATEMENT.md:55-65`). The registry lists A:EX-A as Cor-C's only implementation premise, so the edge adds EX-S, SR and the shipped configuration.
- *Fix:* add "under LIST-CODE's premises (core 4676af6 = DIST's pin, shipped configuration, EX-A, EX-S, SR; admissible runs)" to N1 and to the Edge and notes-append lines.

F3 — S₀ is not defined outside Setting R (`:22-24`, `:30-35`).
- *What fails:* S₀ = supp θ* is a Setting R object, but N1 and N2 are meant to apply under Theorem A's law.
- *Fix:* state that S₀ := {j : β*_j ≠ 0}, DIST's "true model" (:233), in retained indices, and that 𝓜_n and 𝒦_n (whose search part does not depend on S₀) are read with that S₀; the s₀ > K convention still applies.

F4 — the disjointness argument needs tightening (`:40-45`).
- *What fails:* the "pairs not independent" argument is heuristic. It also needs READER's raw form, because RM's Setting R fixes only Y = Cy^r. And ":45 (b) is not available under any law where (a) holds" reads as an impossibility claim.
- *Fix:* give the conditional-law argument above (or: independence would force E[y₁ | X^r] = E[y₁ | x₁], but under Setting R it depends on x₂ through x̄ and sd_n). Reword :45 to "is not supplied by any recorded result under a law where (a) holds".

F5 — the raw-scale (c) is overstated (`:48-50`).
- *What fails:* POST's raw-scale clause is a parenthetical [R02-3] that needs Gaussian rows, unit population variances, LSF, fixed s₀ and |β_j| ∈ [b_lo, b_hi]. Theorem A's conditions alone do not give it.
- *Fix:* "under POST's raw-scale hypotheses, (c) is recorded …; within that class only P(𝒦_n) → 1 is open."

F6 — the Setting F route is not mentioned (around `:45-48`).
- *Fix:* add one sentence on why RM2-F does not close the gap: its fixed-design hypotheses are not shown to hold with probability → 1 for random designs, and its leakage condition is expected to fail at η < η_A.

F7 — weak source for the object identification (`:17-18`).
- *Fix:* cite DIST `STATEMENT.md:273-283` (same core pin, 𝒯 = `top_store`, values F, π_𝒯 ∝ e^F) alongside D5P §1.

F8 — nits.
- `:35`: "M ≥ M₀ > 0" should be "M ≥ 1 (DIST :164)".
- `:15`: the (A1)–(A5) span is :174-180.
- Outside the note, advisory only: D5P `STATEMENT.md:136-137` (remark 3, "designs that satisfy both Theorem 9 and Theorem 6") describes an empty set when s₀ ≥ 1, by N3. Reword it at the next statement revision.

The card sentence in §4 (`:70-73`) is faithful.

N1: IMPLIES — on 𝓜_n ∩ 𝒦_n, LIST-CODE (i) and (v) put S₀ in every completed run's list, so π(𝒯) ≥ π(S₀ | y); this holds under LIST-CODE's code-level premises (F2).
N2: IMPLIES — correct union bound over Corollary C's good event, 𝓜_n, 𝒦_n and {π(S₀ | y) ≥ n^{−cM/2}}; hypothesis (c) is essential.
N3: AGREE — the i.i.d. raw-β* law and Setting R are disjoint for s₀ ≥ 1, and no recorded result (B6.7, RM2, RM2-R, RM2-F, POST) supplies raw-scale P(𝒦_n) → 1.
COR9C-CHECK: ACCEPT-WITH-CHANGES
