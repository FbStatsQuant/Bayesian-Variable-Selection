# Amendments of 2026-11-02 to the frozen theory documents

**By:** E-SPINE (Opus 5.5), branch `theory/E-SPINE`, for Felipe's review. **Basis:** the 2026-11 theory campaign, as summarised in `theory/W8-SYNTH` · `theory_campaign/W8-SYNTH/SYNTHESIS.md` and `BRIEF.md`.

**Scope.**
- This is a wording correction only. Nothing was recomputed, no status word is changed and nothing is upgraded.
- Every new result cited here is a **candidate**: an author's proof, sometimes checked by a same-family run. Cross-family (XF) review is noted where it exists.
- The frozen documents keep their original wording wherever it is still defensible. Each changed passage is marked in place with *"Amended 2026-11-02"*.

Evidence branch heads at the time of writing:

| Branch | Head |
|---|---|
| W7-SEP | 858004e |
| W8-SYNTH | 6876a9a |
| S-ELS | 90423b1 |
| O-BGIBBS | 55679ee |
| O-LS0 | 02348e2 |
| F-SIGMA | e2a3481 |
| O-DILUTE | abedf99 |

---

## 1. The spine: "moving off the start is needed", not "tempering is needed"

### The finding
W7-SEP (`theory/W7-SEP` · `REPORT.md` §1, §5; `PROOF.md` §4.2) tested the planned claim that "start-only methods fail; the tempering bridge is needed". On the paper's own masked family LH, that claim is **false**.
- **Proposition GU (greedy universality)** is PROVED (candidate; not XF reviewed; it uses W4-T38FULL Lemma M, which is same-family VERIFIED only). Its setting: exact-Gram designs with an isolated relevant set R, SE on R and fixed signals. Its conclusion: the production local search, started at **any** C ⊆ R, reaches, scores and certifies S₀ with probability → 1, in a bounded number of moves.
- **Corollary GU-LH** (COUNTEREXAMPLE to the task's claim (a), by proof). On LH, start-only discovery plus the production local search (that is, LS0) scores S₀ with probability → 1. The same held numerically in 386/386 replicates.
- W7-SEP §1 item 4: on LH there is **no separation between the tempering bridge and a single greedy search from the start mode**.

### What is still true, and is the defensible claim
**Moving off the start is needed.**
- iid start draws alone fail in the masked regime: T27(i); R-T20(i).
- W7-SEP Theorem SEP(A)/(B) (PROVED, candidate) makes this sharp on LH. iid discovery, and one-shot importance reweighting, need Q* = p^c n^{c/2} draws.

**v3's moves provide the move off the start.** Each of the following is a sufficient discovery route; none is shown to be uniquely necessary:
- bridge Gibbs flips;
- the terminal rounds (O-BGIBBS Theorem BG3: PROVED for the original method on LH with p fixed; Prop. LH-lock is a PROOF SKETCH);
- the local search, including LS0 (W7-SEP Prop. GU; T38(b1-LH)).

**The bridge's own role** is to produce calibrated evidence and PIPs (T12, T26) and the HPM ledger.

### Consistent facts
- **S-ELS** (`theory/S-ELS` · `REPORT.md` §1, §3), on the 2,394 completed fits:
  - the final local search made **0 moves** in every fit;
  - every error is a posterior miss (565), with **0 search misses**;
  - S₀ was scored in every completed fit.
- **O-BGIBBS** (`theory/O-BGIBBS` · `REPORT.md` §1 · Theorem BG3): the original method's terminal Gibbs rounds score S₀ on LH, for fixed p.

### Changes made (main, `Docs/`)

| File | Passage | Change | Evidence |
|---|---|---|---|
| `Docs/THEORY_PRIORITIES.md` | header | Amendment banner pointing here | this note |
| `Docs/THEORY_PRIORITIES.md` | §1 Story | Added "What (b) needs": move off the start; the bridge is one of several sufficient routes; its own role is Ẑ/PIPs and the ledger | W7-SEP Thm SEP(A), Prop. GU, Cor. GU-LH; T27; R-T20(i) |
| `Docs/THEORY_PRIORITIES.md` | Thm 2 Intuition / Why it matters | "That is exactly why the sampler exists" → "why the method must move off its start draws"; "motivation for the SMC machinery" → "motivates the moves that leave the start" | W7-SEP Prop. GU |
| `Docs/THEORY_PRIORITIES.md` | Thm 5 Why it matters | "explains the method's design (start, bridge, moves, local search)" → "explains why the method must move off its start"; "needed no sampler" → "needed no move off the start"; sufficient routes listed | W7-SEP Prop. GU; O-BGIBBS BG3 |
| `Docs/THEORY_PRIORITIES.md` | T39 risk | "must say what tempering contributes": answered | W7-SEP §1 item 4, Prop. GU |
| `Docs/THEORY_PRIORITIES.md` | §3 The hole | "the regime where the sampler is unnecessary" → "where no move off the start is needed" | W7-SEP Prop. GU |
| `Docs/THEORY_PRIORITIES.md` | §5 data, implication | S-ELS confirmations (0 moves; 541 forced by monotonicity; S₀ always scored); delivery may be argued by any move off the start | S-ELS §1; W7-SEP; O-BGIBBS |
| `Docs/THEORY.md` | header; §4.5 T38 note | Amendment banner; LS0 effective; no-LS0 candidates; spine | O-LS0; W8-SYNTH §4.2; W7-SEP |
| `Docs/PLAN.md` | pursuit order item 4 | LS0 now part of the method | O-LS0 |
| `Docs/Theory/one_pagers/T38.md` | new "Amendment" section | Spine, LS0 effective, no-LS0 candidates | W7-SEP; O-BGIBBS; O-LS0 |
| `Docs/Theory/one_pagers/T27.md` | new "Amendment" section | T27 motivates moving off the start, not tempering | W7-SEP Thm SEP(A)/(B), Prop. GU |
| `Docs/Theory/one_pagers/T39.md` | open obligations | Tempering's contribution answered | W7-SEP |

### Errata for hash-frozen files (not edited)
These files are listed in `Docs/Theory/PAPER_SELECTION_20261028/FROZEN.sha256`, so they are left byte-identical and corrected here. Where they disagree with this note, read them with these errata.
- **`new_conjectures/T38_two_regime_HPM_consistency.md`, "Why it is needed".**
  - The text "That regime does not need the sampler" should read: *"That regime needs no move off the start: iid start draws already score S₀. In the masked regime (T27) the run must move off its start draws, and any of v3's moves (bridge Gibbs, terminal rounds, local search incl. LS0) may deliver. W7-SEP Prop. GU shows that on LH the local search from the start mode suffices, so the main theorem must contain a delivery step, not a tempering step."*
  - The LS0 bullet "It is needed only if eligibility cannot be proved otherwise" is superseded: LS0 is now part of the method (§2 below).
- **`new_conjectures/T39_independent_repair_tracks.md`, "Role of tempering".** The question is answered as in the THEORY_PRIORITIES T39 risk above.
- **`FABLE_REVIEW.md` Change A** ("the only regime where the sampler does work") is a consultant's review record and is left as it was. Its point, that T26(iii) needs no move off the start, still stands. Its implication that the sampler is uniquely needed in the masked regime is superseded by W7-SEP Prop. GU.

---

## 2. Other 2026-11-02 campaign decisions that change the frozen wording

### 2.1 LS0 is effective (part of the method)
Felipe approved LS0 on 2026-11-02, conditional on O-LS0's data check. The check passed:
- source: `theory/O-LS0` @ 02348e2 · `REPORT.md` §1; `theory_campaign/LEDGER.md`, 20:33 UTC;
- LS0 changed the reported HPM in **0 of 2,394** completed fits;
- exact recovery is unchanged: 1,119/1,200 at c = 1 and 710/1,200 at c = 0.5;
- the cost is under 0.1% of a fit.

So the approval is effective. Where the frozen documents say "optional tweak", "addable after the fact" or "if needed", read "part of the method".

Corrected cost: LS0 costs 1 + (ℓ+1)·max_k[p + k(p−k)] scores (W6-FIXREV1; ≈ 1.7·10⁵ at p = 1,000), not "about ℓ·p".

Caveat (O-LS0 §1 item 6): most T38(b1) premises fail at n = 200, so LS0's theoretical value is asymptotic.

### 2.2 The common-σ² start is rejected
Two runs show that it floods the start in study-like designs, even with the oracle σ²:
- `theory/O-DILUTE` · `REPORT.md` §5: "Do not adopt it."
- `theory/F-SIGMA` · `REPORT.md` · Theorem S6: "should **not** be deployed as specified".

O-MIX's support comes from an exactly block-orthogonal toy only. The decision is recorded in W8-SYNTH §1, Decision 2, and §4.5.

If any start change is considered later, the candidate is residualised tables, and F-SIGMA's free post hoc Step 0 comes first. No main-branch document proposed the common-σ² start, so no main text changes.

### 2.3 Corrected n = 200 disclosure numbers
Source: W8-SYNTH §1, Decision 3, and §4.13.
- **Beta-min** fails by **at least 43×**, not "about 100×". The 100× figure predates T03♯. Sources: F-REFINE, W6-FIXREV2, F-REFEREE.
- **T03♯ thresholds** hold only from **n ≈ 2·10⁶** (W2-VT03R R1, confirmed by A-REV2 and W6-FIXREV2).
- **Search misses: 0.** S₀ was scored in all 2,394 completed fits, and the final local search never moved (S-ELS).
- **Stopped fits: 6** of 2,400 (S-ELS, W5-LOCKBOOK). O-SWAP's "4" is superseded.
- **Drop the "favourable from n ≈ …" figure.** The sources disagree: 590–730 (O-DILUTE), 800–1,600 (W3-VEXP) and 1,050–3,200 (W5-FAVIID). Quote none, or attribute the W5-FAVIID empirical first n to its source.

Edited on main: THEORY_PRIORITIES Thm 1 Risk, where the beta-min and threshold figures were corrected in place. The old-SE "215–229 columns" figure is kept and labelled. For T03♯, SE_w ranges over ≤ 114 columns because the cap K binds, and it is unverified on the realised designs (F-REFINE CARDS Card 1). No "favourable from n ≈" figure appears on main.

### 2.4 "No masked theorem without LS0" is out of date
W4-T38FULL, W6-FIXREV1 and F-REFINE said that without LS0 the paper has no masked-regime consistency theorem. That is superseded by: **"candidates on LH, pending cross-family review (A-REV7)"**. The candidates (W8-SYNTH §1 and §4.2) are:
- D2-LH, c = 1;
- W5-VMASK R1;
- B2-LH under STAB-LH;
- O-BGIBBS BG3 with LH-lock (PROOF SKETCH);
- F-SHARE F1/F2;
- W7-SEP Prop. GU.

None is XF reviewed, so "closed without LS0" would overstate.

---

## 3. Campaign-branch drafts amended the same way (not main)

| Branch | File | Changes |
|---|---|---|
| `theory/S-PAPER` | `theory_campaign/S-PAPER/theory_section.tex` | Story: added a "what discovery needs" paragraph (move off the start; the bridge is a sufficient route, not the necessary one; its role is Ẑ/PIPs and the ledger). LS0 definition: approval effective. Thm 5 Not claimed: "without LS0 … (OPEN)" → candidates on LH, pending A-REV7. Disclosure: "the masked regime the sampler is designed for" → "a masked regime in which the method must move off its start"; the "800–1600" favourable figure dropped; items 2, 5 and 6 updated with S-ELS and O-LS0; item 8 adds "(xiii) tempering/the sampler is needed for discovery". |
| `theory/F-REFINE` | `theory_campaign/F-REFINE/ARCHITECTURE.md` | §1 story: spine paragraph. §3: "designed for" wording. §4: no-LS0 candidates; LS0 effective. §6: overstatement item 15 ("tempering is needed"); item 7 updated with S-ELS. §7: "800–1600" figure dropped; numbers aligned. §8: items 2 and 7 marked done. |
| `theory/F-REFINE` | `theory_campaign/F-REFINE/CARDS.md` | Headline fact 2 and Card 6 "Not claimed" updated to no-LS0 candidates. Cards 4 and 6 updated with S-ELS and O-LS0 data. Card 3's "vanishes by n ≈ 800–1600" figure attributed and flagged as not for the paper. Card 6 Risk: spine note. |
