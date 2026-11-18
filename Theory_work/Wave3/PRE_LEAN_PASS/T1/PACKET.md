# PRE-LEAN PASS, T1: PACKET for the Astra "break it" call

Target: **Thm 3(a), the rate lower bound on every design = `W3-PSHARP:B@1.0.0` (Corollary B)**, with its only dependency
`W3-PSHARP:S@1.0.0` (Lemma S, items 1 and 2, and the Lemma V it uses). Lean shortlist item 1.
Snapshot: origin/main as fetched 2026-11-18 (all paths below are repo-relative, on the branch `theory/PRE-LEAN`, which is origin/main).

## Registry cells (verbatim, `Theory_work/INFRA/registry/claims.tsv`)
| id | line | version | status (verbatim) |
|---|---|---|---|
| `W3-PSHARP:B` | 410 | 1.0.0 | PROVED-CHECKED; council R2, MANIFEST 4513e05a40ddc3bf8baeebf04d7156d3c0ac84442dbe0d9b2c6c59244afdac14, sol=9.2 PASS, opus=9.3 PASS; correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md, per-claim addenda: ACCEPT) |
| `W3-PSHARP:S` | 408 | 1.0.0 | PROVED-CHECKED; council R2, MANIFEST 4513e05a40ddc3bf8baeebf04d7156d3c0ac84442dbe0d9b2c6c59244afdac14, sol=9.2 PASS, opus=9.3 PASS; correct:PASS(reviews/R2_council_sol.md, reviews/R2_council_opus.md, per-claim addenda: ACCEPT) |

Registry `depends_on` of B: `W3-PSHARP:S@proof:S(1),S(2)`. Not used in the proof (context only): `W3-POST2:A2@1.0.7`, `W3-POST:Prop-LB@1.0.0`.
The frozen round manifest (`Theory_work/Wave3/W3-PSHARP/reviews/MANIFEST_R2.txt`) verified OK locally before this call.

## Spans (read these, nothing else; long files in chunks of 120 lines)
1. NOTATION (the coded target pi, the sets Omega, K, w, D_S, Q_S, nu, b0): `Theory_work/Wave3/W3-PSHARP/STATEMENT.md:16-30`.
2. STATEMENT of Lemma S: `Theory_work/Wave3/W3-PSHARP/STATEMENT.md:32-44`.
3. STATEMENT of Corollary B (display, constants c(p,s0), consequences B1, B2, B3, remark): `Theory_work/Wave3/W3-PSHARP/STATEMENT.md:90-114`.
4. PROOF of Corollary B: `Theory_work/Wave3/W3-PSHARP/lemmas/B_sparsity.md:1-59` (statement :6-10; proof :12-28 with the constants at :25-28; consequences B1, B1-critical, B2, B3 :29-47; remarks :49-59).
5. PROOF of Lemma S and Lemma V: `Theory_work/Wave3/W3-PSHARP/lemmas/S_one_step.md:1-63` (Lemma V :7-15; Lemma S :17-57, items 1-2 :17-43, items 3-4 :44-57; remarks :59-63).

(Aids, optional, only if you need to check a numeric claim: `Theory_work/Wave3/W3-PSHARP/numerics/b_check_out.txt`.)

## What the claim says (paraphrase; the spans above are authoritative)
For every n >= 3, every standardised design with p >= 2, every data set and every S0 subset of [p] with 0 <= s0 <= K-1 (K = min(p, floor(n/2))), deterministically:
delta_n/(1-delta_n) >= O^lb_n := sum_{j=1}^{K-s0} C(s0+j, j) n^{-j/2} prod_{i<j} (p-s0-i)/(2p-1-s0-i) >= c(p,s0)/sqrt(n),
so pi(S0) <= 1/(1+O^lb_n) <= sqrt(n)/(sqrt(n)+c(p,s0)), with c(p,s) = (s+1)(p-s)/(2p-1-s); c >= (s0+1)/3 if s0 <= p/2.
Consequences: (B1) pi(S0) <= [1+(s0+1)/(3 sqrt n)]^{-1} surely; critical scale limsup pi(S0) <= e^{-lambda/2}; (B2) rate r_n forces s0 = O(sqrt(log n)).
The proof: pi(S_J)/pi(S0) >= [w(s0+j)/w(s0)] n^{-j/2} from Lemma S(1) (D ratio <= n^{|J|}) and Lemma S(2) (Q_{S_J} <= Q_{S0}), then sum over all J with |J| = j <= K-s0.

## The single question
**Is there any genuine flaw in the Corollary B statement (STATEMENT.md:90-114) or its proof (B_sparsity.md, with Lemma S(1),(2) and Lemma V of S_one_step.md)? Break it.**

Role: Astra, "break it". Look for: a wrong step; an unstated hypothesis or an edge case in the stated domain (n = 3, K = 1, s0 = 0, p = 2, s0 = K-1, j = K-s0, p = s0+1, s0 = p/2 exactly, ties, rank-deficient or duplicated columns, S = emptyset in Lemma S); a wrong constant or a wrong direction of an inequality; a limit statement not justified (critical scale; c(p,s0)/(s0+1) -> 1/2); a step that would not compile in Lean (an implicit existence or nonemptiness, a division by something not shown nonzero, a hidden measurability or probability fact, a statement that quantifies over data in a way that needs more than the deterministic core). Lean scope: the deterministic core is the display, the constants, (B1) and the critical scale; (B2)/(B3) are readings with a probabilistic hypothesis and are context.
Do NOT: rewrite the result, propose generalisations, comment on style, or report nitpicks (typos, notation preferences). Report only (a) genuine flaws we missed or (b) changes needed to compile in Lean, each with the exact line and a minimal fix. If you find nothing, say so explicitly.

## Required output format
First line: `MODEL: <your model id> (codex, reasoningEffort high)`.
Then: `VERDICT: NO-FLAW | FLAWS-FOUND | LEAN-ONLY-POINTS`, then a numbered list; for each point: id (T1-1, ...), class (FLAW / LEAN-COMPILE / OBSERVATION), file:line, what is wrong, why, minimal fix, severity (blocking / local / cosmetic).
Finish with one line: `COUNT: <number of points>`.
