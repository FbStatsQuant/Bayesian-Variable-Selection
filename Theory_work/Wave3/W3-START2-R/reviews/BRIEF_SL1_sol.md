# BRIEF SL1 — statement lock, W3-START2-R (Sol, gpt-6.1-sol, reasoningEffort high; fresh, blind first read)

You are an independent cross-family reviewer. You have not seen this ticket before. Read only the files listed;
do not read LOG.md, CHECKPOINT files of this ticket, or anything under `reviews/` except this brief. **Do not edit,
create or delete any file, and change no git state.** Return your review as your final message (the lead saves it
verbatim to `reviews/SL1_statement_lock_sol.md`).

Repository root: `/home/fb31/BVS-wt/W3-START2-R`. Ticket folder: `Theory_work/Wave3/W3-START2-R/`.

## Files
- Under review: `Theory_work/Wave3/W3-START2-R/STATEMENT.md` (v1.5-draft0, a delta statement), `PLAN.md`,
  `BRIEF.md` (the department's brief: what is to be targeted), `TARGET.md` (context only).
- Parent statements (read-only, recorded): `Theory_work/Wave3/W3-START2/STATEMENT.md` (v1.4.1 = "PARENT"),
  `Theory_work/Wave3/W3-START/STATEMENT.md` (v1.3.4 = "BASE").
- Parent proof lines the plan relies on: BASE `lemmas/L4_VIS.md` (all), `lemmas/L7_NEC.md` (all), `lemmas/L3_LEAK.md`
  (L3.1, L3.2, L3.5), `lemmas/L6_COROLLARIES.md` (all), `lemmas/L8_TRANSFER.md` (all), `lemmas/L9_BR.md` (all),
  `lemmas/L10_INTERFACES.md` (L10.3), `lemmas/L11_EXAMPLES.md` (all); PARENT `lemmas/P1_LEADING.md` (P1.4–P1.8),
  `lemmas/P3_NEC.md`, `lemmas/P4_BR.md`.
- Motivation: `Theory_work/Wave3/API_AUDIT/sharp2/TRIAGE.md` rows W3-START:START-F, :F4, :NEC, :START-R, :EX, :MIS,
  W3-START2:START-F, :TRANSFER, :IF-START, :START-R, and §2 rows T8, T10; raw verdicts `sharp2/results/f04.md`–`f09.md`
  as needed.

## What to check (statement lock, PROTOCOL_v4 §3.1)
1. **Right target.** Does STATEMENT v1.5 state the BRIEF's targets T8, T10, item 3 (restatements) and item 4 (wording)?
   Anything missing or overstated relative to the brief?
2. **Faithful and explicit.** Every hypothesis each claim uses is stated; every by-reference clause points to the right
   parent lines; quantifiers and uniformity are right; ids and symbols are defined before use.
3. **Truth of the target (try to break it).** In particular:
   - (D3): the claimed implications (V-c) ⇒ (V-cp) and (V-m) ⇒ (V-mp) for n ≥ 256s₀²; whether the exact price
     π_n(d, a; Q) is what BASE `L4_VIS.md` Step 5 actually needs, including a > d and log(p/c_Q) < 0.
   - (D4)/(D5): (L-R⁺) ⇒ (L-R⁺⁺); the equivalence claimed for (L-gain-0) with C₀ = 0.
   - (B-R⁺⁺)(iii) and (T3⁺⁺)(b)(iii): o₀ = O_P(√(log n/n)) under Setting R, (FL-R16), (V-R), (L-R⁺⁺) with Q = S₀ and
     (L-gain-0). Is the route of PLAN §2 (BASE L9.5 at the reference sets U ⊊ S₀, mean shift d̄ = O(1/√log n), then the
     second display of (T1⁺⁺)(d)) sound? Does anything require (L-R⁺⁺) beyond what is stated?
   - (B-R⁺⁺)(ii)/(T3⁺⁺)(b)(ii) with the factor N̄_n; (i) with C_R depending on κ_H.
   - (C2⁺⁺), (N2⁺⁺), (N3⁺⁺): the pointwise level and the drifting clauses ((c_n − 1)√log n → ∞).
   - F4⁺⁺: the explicit bound with C_A = 2√(1 + 2A) + 1 for every c_n ≤ 1.
   - (T3⁺⁺)(a): (a1)–(a3) as stated (conditional probabilities, random rates, |S₀| ≤ s̄).
   - MIS⁺⁺ Gaussian instance; EX⁺⁺ rows, in particular F-2 ((V-mp) for every c_m < 1 + 2A; the rate
     n^{−(1+2A)/10+η}; (T1⁺⁺)(c) only for A ∈ (3/4, 1]).
4. **Supersession table** (§5): does each new claim imply the parent claim named?
5. **Plan viable** within ≈ 12 Opus hours and the Wed 2026-11-18 cut-off?

## Output format
- Verdict line: `SL1-VERDICT: LOCK | LOCK WITH CHANGES | NO LOCK`.
- Findings, numbered, each tagged **C** (a target clause is false or unprovable as stated), **S** (claims more than
  the plan can prove, or uses an unstated hypothesis), **F** (unfaithful to the brief or to a cited source/line), or
  **E** (editorial). Each finding names the STATEMENT line(s), says what fails, and proposes a fix.
- Optional: proposals for a strictly better statement that is cheap to prove (marked OPTIONAL).
