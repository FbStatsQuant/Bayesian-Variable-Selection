# Plan Council: Round 1 brief (Wave 1 plan package, Lead-A), 2026-11-28

You are one of three independent council seats: Opus 5.5, Sol 6.2 and Gemini 4 Neon, all at effort high (Company
Handbook v2.0, `POLICIES.md` §3). **You review and score only. You never edit any file except your own review file.**
Do not commit. Lead-A commits your file.

**POLICIES §14 (mandatory):** Codex agents (Sol 6.2, Astra 6.2) must NEVER delete files and must NEVER write or
redirect outside /home/fb31/BVS-wt/THEORY-DEPT (scratch goes in /home/fb31/BVS-wt/THEORY-DEPT/.rc_tmp/).
The same rule binds every seat: no `/tmp`, no TMPDIR changes, no deletions, no writes outside the worktree.

## The item under review
Worktree `/home/fb31/BVS-wt/THEORY-DEPT`, branch `dept/theory`, at the commit named in your dispatch message. The
package is in `Theory_work/Dept/wave1_plan/`:

| File | What it is | Bar |
|---|---|---|
| `LOCKED_STATEMENTS.md` ([LS]) | final assumptions A1–A10 (with A7′, A9′), in math and plain English; final theorems Thm D, Thm S(a)/(b), Cor S1, Thm M(i)–(iii), Cor M1 | **8.5** (theorem statements, Handbook rule 9) |
| `MASTER_PROOF_PLAN.md` | shared-lemma interface contract (§1); KEY-step routes for Lead-S (§2), Lead-M (§3) and Lead-D (§4); common requirements | 8.0 (plan) |
| `LEAN_PLAN.md` | Lean 4 modules, build order, named axioms G1, P1–P6, acceptance | 8.0 (plan) |
| `TRANSCRIPTION_CHECKLIST.md` | T-1 … T-24 | 8.0 (plan) |
| `RECONCILIATION.md` | proof-file header statuses vs registry and check records (worker W1; for context, and to check that the plan uses it correctly) | not scored separately |

Inputs the package is built from (read as needed; you need not read all):
- HQ curated packet `Theory_work/Wave3/HQ_ADVISORS_2026-11-28/CURATED_PACKET.md`, with the adviser memos in the same
  folder.
- The current assumption definitions `Theory_work/Dept/song_assumptions/THEOREM_DEFINITIONS.md` (v1.4.1).
- Proof sources:
  - `Theory_work/Wave3/W3-DIST/STATEMENT.md` (Theorem A, Lemma H, bridges B0–B3) and `W3-DIST/work/E_bridges/B3.md`;
  - `Theory_work/Wave3/W3-T03ACC/sources/W1-T03R/PROOF.md` §6 (T03♯);
  - `Theory_work/Wave3/W3-POST/STATEMENT.md` (Thm 1);
  - `Theory_work/Wave3/W3-POST2/lemmas/C_expectation.md`.
- The SMC-BVS engine conventions: g = n g-prior with unit ridge, truncated BB(1,p) prior, cap K = min(p,⌊n/2⌋),
  IG(0.01,0.01), MPM reporting. Song & Liang (2015) is the reference paper (Thms 1–4, Cor 2).

## What to check
1. **Assumptions (A1–A10).** Is each one correct and well quantified (order of quantifiers, which constants are fixed
   and which may vary with n)? Is it no stronger than the proofs need, and sufficient for them? Is the plain English
   faithful to the math? Pay particular attention to A4/A5 (the "for every fixed c > 0 there is n_c" form), A7′(a)
   (anchored), A7′(b) (φ b_min ≥ C_β √(log(p√n)/n)), A8 (one fixed law, finite candidate set) and A9′.
2. **Theorem statements.** Is each one correct, and provable by the route in the plan? Look for overclaims, missing
   hypotheses, and constants whose dependence is misstated (C_sel = 4√c₀, with c₀ = max{4C_*, 32[s₀(A+1)+2]}). Do the
   plain-English versions say the same thing as the math? Check the notes under Thm S and Thm M.
3. **Interface consistency (plan §1).** For each shared lemma: does the owner's promised statement give each consumer
   exactly what the consumer's step uses? Check hypotheses, events and constants.
4. **KEY steps.** Spot-check the soundness of:
   - S-2 (the fixed-c beta-min arithmetic, giving c = C_β²/16 > c₀);
   - S-3/S-3′ (B3′: the window tightened to s₀ + j₀, BM-∞ → BM(c));
   - S-4 (random-design transfer, or the alternative per-n spine);
   - M-3/M-4 (misspecification under A8: the tied supersets; the raw-Z Hartman–Wintner LIL bound giving an
     O(log log n) gain);
   - D-2 (the density bridges).
   Say whether the effort and risk ratings are realistic.
5. **Lean plan.** Is the axiom list complete for the proofs as planned, and stated no stronger than needed? Is the
   order sensible, and the acceptance criterion adequate?
6. **Checklist.** Are there transcription hazards that T-1 … T-24 miss?
7. **Open items ([LS] §5).** Give a verdict on each of the three: anchored vs all-subsets A7′(a); whether the
   non-nesting of Cor S1 with the old Thm 3.2 is acceptable; and whether C_sel goes in the main text or only the
   supplement.

## Output (required format)
Write exactly one file, `Theory_work/Dept/wave1_plan/council/R1_<SEAT>.md`, with `<SEAT>` = `OPUS`, `SOL` or `NEON`
as named in your dispatch. It contains:

```
# Plan Council R1 — <SEAT> (<model>, high)
Commit reviewed: <hash>
SCORE_STATEMENTS: x.x / 10   (LOCKED_STATEMENTS.md; bar 8.5)
SCORE_PLAN:       x.x / 10   (MASTER_PROOF_PLAN + LEAN_PLAN + CHECKLIST; bar 8.0)
BLOCKING findings: <count>

## Findings
| ID | Severity | Location (file:line) | Finding | Suggested fix |
|---|---|---|---|---|
| <SEAT>-1 | BLOCKING / NON-BLOCKING | ... | ... | ... |

## Open items (LS §5)
1. ... 2. ... 3. ...

## What would raise each score to the bar (if below it)
```

Use BLOCKING only for an error that makes a statement false or unprovable as stated, a gap in an interface that a
proof relies on, or a mis-stated assumption. Use NON-BLOCKING for everything else. Be concrete: quote the line, and
give a counterexample or calculation where you can. Your final chat message should give only the two scores, the
blocking count, and the file path.
