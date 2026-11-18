# CSL1 brief — statement lock + line check of track-A_C item C1 (Codex gpt-6.1-sol, high)

The gate read for C1 (PROTOCOL_v4 §2, Tier B, NORMAL: Sol lock + Sol line check in one read, manager's GO 11-16).
**Blind first read:** you get the files below and nothing else. Do not open any LOG, CHECKPOINT, INDEX, CHECK or
`reviews/` file. Read only; write no files; change no git state.

Workspace: `/home/fb31/BVS-wt/W3-AUDIT` (branch `theory/W3-AUDIT`).
- The item: `Theory_work/Wave3/W3-AUDIT/track_A_C/C1_AUDITS/STATEMENT.md` (v2) and `.../C1_AUDITS/PROOF.md` (v2).
- The registered claims it checks: `Theory_work/Wave1C/C-DLV/STATEMENT.md` (lines ~20-60), `Theory_work/Wave1C/C-DLV/INVENTORY.md`,
  `Theory_work/Wave1C/C-DLV/lemmas/L2_degenerate.md`.
- Inputs it cites (to see what is assumed; review them only where the item leans on them): `Theory_work/Wave3/W3-AUDIT/track_A/T10_P1S3/{STATEMENT,PROOF}.md`,
  `.../track_A/T2_BLK/STATEMENT.md`, `.../track_A/T4_ENC/STATEMENT.md`, `.../track_A/T9_TDP/STATEMENT.md`, `.../track_A_X/T14_REP/STATEMENT.md`.
- The consumer, Lemma DLV-0 (not on this branch; read with git):
  `git -C /home/fb31/BVS-wt/W3-AUDIT show e78a1055:Theory_work/Wave3/W3-RM2-R/STATEMENT.md` (lines ~140-165, 225-235) and
  `git -C /home/fb31/BVS-wt/W3-AUDIT show e78a1055:Theory_work/Wave3/W3-RM2-R/lemmas/Q5_dlv0.md` (whole; (E2) at lines 59-64),
  plus the FIN delivery section it imports for 𝒜_n (`s6_delivery.tex:29-46`; locate it with `git grep -l s6_delivery` /
  `find Theory_work -name s6_delivery.tex`).
- Code of record: `Scripts/SMC_BVS/core/` (registry method pin 4676af6; confirm with
  `git diff --quiet 4676af6 HEAD -- Scripts/SMC_BVS/core`). Read the code yourself; do not trust the line quotes or T10's map.

Context: C1 gives a verdict on two registered "AUDITED (code reading)" claims — `C-DLV:P1-Inventory` ("every exit of
`v3_fit` without estimates is one of the listed sites") and `C-DLV:L2-S3` (D2 and the internal-invariant sites X2 are
unreachable) — at the pin, as consumed by DLV-0 (deterministic delivery of the shipped fit; row 3.1, the main theorem).
They were written before LS0 shipped. A blind Claude line check found one uncovered trigger: the default SMC preflight's
LS0 worst-case time / archive terms (now amendment A-7, row B1′).

**Part 1 — statement lock.** Right target (does C1 give DLV-0 exactly what DLV-0 takes from the two audits?), faithful to
the code and the registered texts, every hypothesis and option explicit, no clause stronger than proved. Verdict:
LOCK / LOCK WITH CHANGES (list) / DO NOT LOCK.

**Part 2 — line check.** Every step against the code; try to break it. Verdict: VERIFIED / VERIFIED WITH AMENDMENTS /
NOT VERIFIED. **Check explicitly:**
1. **A-7 is complete:** no other trigger of a no-estimates exit is missing at the pin in the default configuration —
   in particular every term and every `exceeds` condition of `v3_preflight` on both branches and at every tier
   (initial and escalation), the timing benchmark itself, and any other option-dependent check.
2. **DLV-0's (E2) with 𝒜_n's term P̄_LS0 really rules this exit out** (`Q5_dlv0.md:59-64` @ e78a1055, FIN A4): the
   inequality it uses matches the coded test (strict ">", the factor 2, (ℓ_n + K + 1)(p + p²/4), the measured ŝ_K at
   size K, the `ls0_archive` bytes with the memory components, the order "memory first, then timing"), at (n, p_raw)
   vs the retained p, at both tiers; and say what premise bounds the measured ŝ_K (MACH?).
3. The rest: the §1.1 table (only places `estimates_available` becomes TRUE), the §1.2 grep list, the §1.3 nodes, each
   S.3 verdict (D2, (i)–(vii), `get_holder`, `start_mode` throws, implicit errors), X7/X8 for R-representable inputs,
   and (C1-c)'s statement that the `C-DLV:L1-R` scope is exact-branch preflight seconds only.

If you find a reachable exit without estimates that no row (with A-7) covers, or one DLV-0 does not exclude, say so
first and tag it **C**.

**Reply format** (plain markdown, as your final message): Part 1 verdict with required changes; Part 2 verdict; numbered
findings tagged **C**, **S**, **F** or **E** with file:line, what fails, and the fix. Last line:
`CSL1-VERDICT: C1 lock=<…>, check=<…>; A7-complete=<yes/no>; DLV0-E2-excludes=<yes/no>`.
