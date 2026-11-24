# PRE-LEAN PASS, T2: PACKET for the Astra "break it" call

Target: **posterior summaries `C-PACK:SL0@1.0.1`** (Lemma SL0) **and the pooling bound LT-d, a clause of `W3-SAMP:LT#@2.0.6`** (Theorem LT♯). Lean shortlist item 2.
Snapshot: origin/main 668b413f (branch `theory/PRE-LEAN`). All paths repo-relative.
Scope of the Lean core: SL0 (i)-(v) (deterministic, any probability on a finite Omega); LT-d first clause (convex combination of four island vectors) and its last clause (Shat = S0 on {completed} ∩ {delta < 1/2} ∩ {S0 in M}). The probabilistic middle clause of LT-d (the MPM bound with 152·o1) is context, but check its arithmetic too.

## Registry cells (verbatim, `Theory_work/INFRA/registry/claims.tsv`)
| id | line | version | status (verbatim) |
|---|---|---|---|
| `C-PACK:SL0` | 71 | 1.0.1 | PROVED-CHECKED |
| `W3-SAMP:LT#` | 353 | 2.0.6 | PROVED-CHECKED; council R1, MANIFEST 68480a7293820d034240a1096cfc7cfa441d5ee6a8c57b344172e92928d13d40, astra=9.1 PASS, opus=8.8 PASS |
| `W3-SAMP:PC` (used by LT-d's HPM clause) | 349 | 2.1.3 | PROVED-CHECKED; council R1, MANIFEST 68480a7293820d034240a1096cfc7cfa441d5ee6a8c57b344172e92928d13d40, astra=9.1 PASS, opus=8.8 PASS |

SL0 council cell (registry `council` field): `R1; MANIFEST 807c2a602421307395862c8bcf2cd2c74917f2f96b1a6e3fa247b8261ffc9cf4; sol=9.0 PASS(reviews/C1r_record_sol.md); opus=8.7 PASS(reviews/C1r_record_opus.md)`; evidence in the registry: `reviews/R34_item4_check_sol.md: ERROR-as-written (0 FATAL/2 MAJOR/7 MINOR, SL0(i)–(v), SL1, SL1′, SL2 re-derived, all fixes applied)`.
Registry `depends_on` of LT#: W3-SAMP:MR@proof:MR-b, MR-c; W3-SAMP:ST@proof:ST-b, ST-c; W3-SAMP:PC@proof:ledger/completed records (LT-d); W3-SAMP:CC@proof:CC3; W3-POST:Thm-1@stmt:P-CONC (LT-e).
Both frozen manifests verify OK locally (807c2a60… for C-PACK, 68480a72… for W3-SAMP).

## Spans (read these, nothing else; long files in chunks of 120 lines)
SL0:
1. `Theory_work/Wave1C/C-PACK/lemmas/I4_SL_corollaries.md:11-30` (premises/conventions §0 and Lemma SL0 (i)-(vi) statement) and the proof of SL0 at `:32-37` (the paragraph beginning "*Proof.*" after (vi)). Read `:1-10` for the header only if you need the aliases.
LT-d (W3-SAMP):
2. `Theory_work/Wave3/W3-SAMP/STATEMENT.md:20-60` (objects, conventions, island and output definitions, incl. pip_primary := (1/4) Σ_r p̂_r at :58 and CC3 at :57), `:62-84` (premises), `:86-95` (Lemma CC, Lemma PC), `:126-140` (Theorem LT♯: LT-a, LT-b, LT-b', LT-c, **LT-d at :134-135**).
3. `Theory_work/Wave3/W3-SAMP/lemmas/LT_theorem.md:1-23` (notation), `:34-60` (Step 2′ = LT-b′, Step 3 = LT-a/b/c, **Step 4 = LT-d at :53-60**).
4. `Theory_work/Wave3/W3-SAMP/lemmas/D_theorem.md:38-59` (§3, the reported HPM: the deterministic step "Shat = S0 on {completed} ∩ {delta < 1/2} ∩ {S0 in M}") and `Theory_work/Wave3/W3-SAMP/lemmas/PC_completed.md:1-end`.

## What the claims say (paraphrase; the spans are authoritative)
SL0, for every data set, every n, any posterior pi on a finite Omega = {S : |S| <= K}, delta := 1 - pi(S0) (pi(S0) := 0 if s0 > K): (i) |PIP_j - 1{j in S0}| <= delta; (ii) |pi({S : A ⊆ S}) - 1{A ⊆ S0}| <= delta and, if S0 in Omega, |pi(h) - h(S0)| <= delta·osc(h), with sup over [0,1]-valued h equal to TV(pi, point mass at S0) = delta; (iii) delta < min(q, 1-q) ⇒ xi_q = S0, in particular delta < 1/2 ⇒ MPM = S0; (iv) delta < 1/2 ⇒ S0 is the unique maximiser (HPM = S0 for every tie rule); (v) pi({|S| = s0}) >= 1 - delta.
LT-d: ‖pip_primary − 1_{S0}‖_∞ ≤ max_r ‖p̂_r − 1_{S0}‖_∞; if o1 ≤ 1/4: P(MPM ≠ S0 | C) ≤ Σ_{r≤4}[8δ/η + 152·o1 + P(W_r < η | C)]; with Lemma PC, on {completed} ∩ {δ < 1/2} ∩ {S0 ∈ M}, Shat = S0.

## The single question
**Is there any genuine flaw in SL0 (statement and proof) or in the LT-d clause of Theorem LT♯ (statement :134-135, proof Step 4 :53-60, and its use of LT-b, Lemma PC and D_theorem §3)? Break it.**

Role: Astra, "break it". Look for: a wrong step; an unstated hypothesis or edge case in the stated domain (s0 > K, S0 outside Omega, S0 = empty, p = 1 or K = 0, ties at 1/2, q at the boundary of (0,1), delta = 0, h not defined at S0, osc(h) = 0, an empty maximum, pi(S) = 0 for some S); an inequality in the wrong direction; a constant that does not follow (the 8 and 152 in the MPM bound: check κ0 + 2ε ≤ 1/2 with ε = 1/8, and 8δ/η + 152·o1 from (LT-b) with λ0 ≤ 19·o1; check that delta/(1-delta) = o1 is what is used); a step that would not compile in Lean (a definition of PIP/HPM/MPM/xi_q on a general finite Omega, the zero extension pi(S0) := 0, hidden nonemptiness of Omega or of M, "any tie rule" for Shat, a sup over all h that needs boundedness, conditioning on C that is implicit, measurability of the events); a mismatch between what Step 4 uses (pip_primary = 1/4 Σ p̂_r, MPM defined from pip_primary, Shat defined as the hpm_better maximum over M) and the definitions on STATEMENT.md:20-60 and Lemma PC.
Lean scope: the deterministic core, i.e. SL0 (i)-(v), the convex-combination inequality of LT-d, and the HPM clause "Shat = S0 on {delta < 1/2, S0 in M}" as a statement about finite sets and a maximiser. The Markov/union-bound parts are context.
Do NOT: rewrite the result, propose generalisations, comment on style, or report nitpicks. Report only (a) genuine flaws we missed or (b) changes needed to compile in Lean, each with the exact line and a minimal fix. If you find nothing, say so explicitly.

## Required output format
First line: `MODEL: <your model id> (codex, reasoningEffort high)`.
Then: `VERDICT: NO-FLAW | FLAWS-FOUND | LEAN-ONLY-POINTS`, then a numbered list; for each point: id (T2-1, ...), class (FLAW / LEAN-COMPILE / OBSERVATION), file:line, what is wrong, why, minimal fix, severity (blocking / local / cosmetic).
Finish with one line: `COUNT: <number of points>`.
