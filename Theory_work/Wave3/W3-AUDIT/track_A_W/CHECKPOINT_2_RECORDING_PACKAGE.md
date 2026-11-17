# CHECKPOINT 2 — Recording package — discharge of "conditional on W1-N1:B, W1-N1:F" (track A_W; for the recorder's dry run → HQ GO)

Lead: W3-AUDIT track A lead (Opus 5.5). Branch `theory/W3-AUDIT` @ __COMMIT__. Registry read: origin/main 029bb748.
Code of record 4676af6. Owner standard D106: hardened (blind Opus line check + Sol lock/line check + council), stated at the
pin, Lean targets tagged; API blind-audit card ready for HQ (`track_A_W/API_CARD/`).

## 1. New claims to register (both Tier B, key lemma; ticket W3-AUDIT-AW)
| id | kind | file | lines | sha256 (file) | status (proposed) | depends_on |
|---|---|---|---|---|---|---|
| `W3-AUDIT-AW:ISL` | lemma | `Theory_work/Wave3/W3-AUDIT/track_A_W/W1_ISL/STATEMENT.md` | 41-61 | 2edc44e5d34be9285484442b67fac7dba22ce1e4cc1dec83be7f2a636371bd7c | PROVED-CHECKED; council W-R1/W-R2 (§5) | W3-AUDIT-A:GW@proof:(GW-i) guard bodies; C-DLV:L2-S3@proof:X2 class at the pin (C1); W3-AUDIT-A:CAL-C@stmt:(CAL-c); W3-AUDIT-A:START-X@stmt:(S); W3-AUDIT-A:KER@stmt:(KER-c),(KER-d); W3-AUDIT-AX:FR@proof:Part 1 |
| `W3-AUDIT-AW:FRZ` | lemma | `Theory_work/Wave3/W3-AUDIT/track_A_W/W2_FRZ/STATEMENT.md` | 28-49 | c94e45ae1477421dade7d87532c5c0883cb8dd2b48eda9c99f30da1d7fd925bb | PROVED-CHECKED; council W-R1/W-R2 (§5) | W3-AUDIT-AW:ISL@stmt:(ISL-0),(ISL-st),(ISL-d); W3-AUDIT-A:CAL-C@stmt:(CAL-a)–(CAL-d); W3-AUDIT-A:GW@proof:potential run; W3-AUDIT-A:START-X@stmt:(Z); W3-AUDIT-AX:FR@stmt:(FR-b),(FR-c); C-DLV:L2-S3@proof:X2 class as checked at the pin (track_A_C C1, bound c27fb00e); W3-AUDIT-AX:REP@stmt:(REP-a) |
Lean target: ISL yes for (ISL-st) abstract form; FRZ yes for (FRZ-a), (FRZ-d); no for the code facts.

## 2. Edges: how they are typed (recommendation: RETARGET, not rule (c))
W1/W2 are new statements proved at the pin; the old `W1-N1:B`/`:F` texts cite the v2.2.1 core's lines, so an LC-step line
(rule (c)) on `L1_bridge.md`/`L3_freezing.md` spans would certify text that was not what was checked. Retarget:
| consumer | before | after |
|---|---|---|
| W3-SAMP:D | `W1-N1:B@hyp` | `W3-AUDIT-AW:ISL@proof:(ISL-0),(ISL-st) control flow; (ISL-d) augmented record` ; `W3-AUDIT-AW:FRZ@proof:(FRZ-c) D-i freezing step` |
| W3-SAMP:MR | `W1-N1:B@hyp` | `W3-AUDIT-AW:ISL@proof:(ISL-d) MEAS, Step 2 coordinates` |
| W3-SAMP:MR | `W1-N1:F@hyp` | `W3-AUDIT-AW:FRZ@proof:(FRZ-a)–(FRZ-d), Steps 2–4` |
(MR's `W3-AUDIT-AX:FR@proof:code bridge L1 (B-a),(B-b)` and `SOP:TH110@stmt` stay.) Fallback if HQ prefers rule (c):
one LC-step line per edge naming the W1/W2 PROOF spans as the cited step, carrier `track_A_W/reviews/LC_edges_record.md`,
verdict line quoted from `reviews/WSL1_reply_sol.md` ("W1: VERIFIED …", "W2: VERIFIED …").

## 3. Rows that discharge (status before → after; tool-derived)
| row | before | after |
|---|---|---|
| W3-SAMP:D | PROVED-CHECKED, conditional on W1-N1:B; council R1 … | PROVED-CHECKED; council R1 … |
| W3-SAMP:MR | PROVED-CHECKED, conditional on W1-N1:B, W1-N1:F; council R1 … | PROVED-CHECKED; council R1 … |
| W3-SAMP:LT# | … conditional on W1-N1:B, W1-N1:F (via MR) | PROVED-CHECKED; council R1 … |
| W3-SAMP:C | … conditional on W1-N1:B, W1-N1:F (via MR, LT#) | PROVED-CHECKED; council R1 … |
| W3-READER:R4 (row 3.6) | … conditional on W1-N1:B, W1-N1:F (via SAMP:C) | PROVED-CHECKED; council R3 … |
| W3-DIST:DIST-C | … conditional on W1-N1:B, W1-N1:F, EX-A (exact arithmetic) | PROVED-CHECKED, conditional on EX-A (exact arithmetic); council R2 … |
| W3-DIST:Cor-C | same as DIST-C | PROVED-CHECKED, conditional on EX-A (exact arithmetic); council R2 … |
| W3-AUDIT-A:OVL | … conditional on W1-N1:B (via SAMP:D) | PROVED-CHECKED; council R2 … |
Untouched: W1-N1:Thm-N1, Cor-E (their own edges into B, F are unchanged).

## 4. Scope note to carry (Sol WSL1 finding "C — consumer scope"; HQ ruling needed, not a blocker of the discharge)
D's and MR's conditional identities (and so LT#, C, R4, DIST-C, Cor-C) are proved, at the pin, for the **potential pair**
(𝒜°, 𝓒°) of T1/T5; for the actual pair (𝒜, 𝓒) only T5's transfer rules apply (`track_A/T5_CAL/STATEMENT.md:45-54`): upper
bounds of the forms P(𝒪 ∩ A) ≤ P(𝒪° ∩ A°) and P(𝒜 ∩ A°) ≤ P(𝒜° ∩ A°) transfer; conditional identities given the actual
𝓒 do not. W3-SAMP §0 already states its claims "for the potential run"; its 𝒜 (`W3-SAMP/STATEMENT.md:39`) is the
potential fit's success event in that reading. Recommended record: a W3-SAMP erratum/reader note "𝒜, 𝓒 are the potential
fit's (𝒜°, 𝓒°) (W3-AUDIT-A:GW, :CAL-C)" — EQUAL in substance (it fixes the reading the proofs use); it was first flagged
11-16 (T1 CHECK "F flag for HQ"). Without it, the discharged rows should carry "read with (𝒜°, 𝓒°)" in their notes.

## 5. Evidence
Checks: WLC1 (Opus blind; VERIFIED WITH AMENDMENTS, applied), WSL1 (Sol: LOCK + VERIFIED both), council W-R1 W-R1/W-R2 (§5).
Bound manifest `track_A_W/reviews/MANIFEST_WR2.txt` (d4f64540…; verify OK). Frozen text: W1 STATEMENT/PROOF v1.2, W2 v1.2. API card: `track_A_W/API_CARD/README.md` (≈ $1, ≤ $5.4).

## 6. Residual notes (no effect on the discharge)
- Fixed data: like `W1-N1:B`/`:F`, W1/W2 are at fixed data. `W3-SAMP:D` (D-iii) integrates over the data under the joint law;
  that step is D's own (council-checked in W3-SAMP) and is unchanged by this discharge (W2 "Not claimed").
- Post-bind editorial items for the next manifest (W-R2 Opus N1–N7, all E): name the remaining X2-class exits in W2's "no
  error exit" paragraph; widen W2's configuration premise to T14/C1's; a locator for "S.2's EX-A argument"; tier ∈ {0, 1}
  check in (FRZ-b)(ii); a misplaced "Not claimed" bullet; the seed premise source; W1 v1.2 tag STRONGER as well. Not applied
  (manifest frozen); INDEX.md is also frozen in the manifest, so this checkpoint stands in for it.
