# BRIEF LC2 — line check, W3-START2-R: R3_RATE, R4_TRANSFER_COR, R5_EX (Sol, gpt-6.1-sol, high; fresh agent)

You are an independent line checker. You have not seen this ticket before. Read only the files listed; do **not** read
`LOG.md`, any `CHECKPOINT_*.md`, or anything under `reviews/` except this brief. **Do not edit, create or delete any
file; change no git state.** Return your review as your final message (the lead saves it verbatim to
`reviews/LC2_line_check_sol.md`).

Repository root: `/home/fb31/BVS-wt/W3-START2-R`. Ticket folder: `Theory_work/Wave3/W3-START2-R/` (here "T/").

## Files
- Target statement (locked): `T/STATEMENT.md` v1.5 — clauses [BR], [START-R], [IF-START] (§3.2), [TRANSFER], [F1]–[F3],
  [OVL], [MIS], [EX] (§3.1), and (D4), (D5) of §2.
- **Under check:** `T/lemmas/R3_RATE.md`, `T/lemmas/R4_TRANSFER_COR.md`, `T/lemmas/R5_EX.md`.
- Consumed by them (read the cited lines; these parent files were checked before and are not under review, but every
  citation into them is): BASE = `Theory_work/Wave3/W3-START/` — `STATEMENT.md`, `lemmas/L3_LEAK.md`, `lemmas/L6_COROLLARIES.md`,
  `lemmas/L8_TRANSFER.md`, `lemmas/L9_BR.md`, `lemmas/L10_INTERFACES.md`, `lemmas/L11_EXAMPLES.md`; PARENT =
  `Theory_work/Wave3/W3-START2/` — `STATEMENT.md`, `lemmas/P1_LEADING.md`, `lemmas/P2_OVL.md`, `lemmas/P4_BR.md`;
  `Theory_work/Wave1C/C-MIS/STATEMENT.md:36-60`.
- Sibling files of this ticket that R4/R5 cite (`T/lemmas/R1_VIS.md`, `T/lemmas/R2_NEC.md`) are checked in a separate
  review: treat their **stated** results (START-F⁺⁺ with its uniform form (d) and L6.0/L6.0′ under (D3); F4⁺⁺) as given,
  but flag any use of them beyond what STATEMENT v1.5 states.

## What to check
1. Line by line: every step correct; every citation points to lines that say what is claimed; constants and thresholds
   depend only on what is said; quantifiers (for all large n, uniformity in Q, ε-dependence) right.
2. Each file proves exactly its STATEMENT clauses — no more, no less; no unstated hypothesis.
3. In particular, try to break: R3.3 (the bound 𝔏^♯_n = O_P(√log n) under (FL-R16) and (L-gain-0) only — the conditional
   law with U₀ = U ⊊ S₀, the shift d̄⁰_n, the event E⁰, Markov); R3.6 (composition with PARENT P1.7 / Proposition P1.4);
   R3.1–R3.2 (N̄_n and C_B with 15κ_H; P(Eᶜ) → 0); R4.1 (conditional probabilities, maxima of constants over s₀ ≤ s̄,
   random rates, the split A_n + B_n); R4.4 (Gaussian (GR)); R5.2 (the (V-mp) verification, the F4⁺⁺ premise with c_n,
   the rate and the A > 3/4 range).

## Output format
- Per file: `| file | verdict |` with PASS / PASS WITH FIXES / FAIL.
- Findings, numbered, each tagged **C** (a step is wrong or unproved), **S** (claims more than proved, or uses an
  unstated hypothesis), **F** (unfaithful to STATEMENT or to a cited source/line) or **E** (editorial), each with
  file:line, what fails, and a proposed fix.
- Final line: `LC2-VERDICT: PASS | PASS WITH FIXES | FAIL`.
