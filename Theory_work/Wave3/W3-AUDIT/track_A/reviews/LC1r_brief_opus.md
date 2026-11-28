# LC1r brief — re-check of the repaired lemmas T1 (GW) v2 and T2 (BLK) v2 (Claude Opus 5.5, high; new agent)

PROTOCOL_v4 §2A "re-check of a repaired lemma": a new agent of the finder's family sees the repair. You did not write
LC1; it is given to you as input. Workspace (read only; write nothing): `/home/fb31/BVS-wt/W3-AUDIT`.

Read:
- `Theory_work/Wave3/W3-AUDIT/track_A/reviews/LC1_reply_opus.md` (the line check of v1) and
  `.../reviews/LC1_disposition.md` (what the lead changed).
- The repaired files: `.../track_A/T1_GW/STATEMENT.md`, `.../T1_GW/PROOF.md`, `.../T2_BLK/STATEMENT.md`,
  `.../T2_BLK/PROOF.md` (v1 is not kept; the changelog tables at the foot of each STATEMENT list the changes).
- The code of record `Scripts/SMC_BVS/core/` (pin 4676af6 = HEAD for the core) and any source the files cite.

Answer, trying to break the repair:
1. For each LC1 finding: RESOLVED / NOT RESOLVED (with what is still wrong).
2. The new or rewritten parts — T1: the definitions (𝒱_op, statistical state, P° executing check bodies), (GW-i) as
   restated, (GW-iv) + Step 4, (GW-v) + Step 5, the termination paragraph; T2: the partition map C(X), the setting-R
   paragraph, the binary64 section, the downstream list. Are they correct (C), no stronger than proved (S), faithful to
   the code and the cited premises (F)? Pay attention to (GW-iv)'s claim 𝒜 = 𝒜° ∩ {no calibration check fires} and to
   (GW-v)'s claim that no check runs inside a search.
3. Does the repair break anything that LC1 had verified?
Reply: numbered findings tagged C / S / F / E with file:line; last line
`LC1r-VERDICT: T1=<VERIFIED|VERIFIED WITH AMENDMENTS|NOT VERIFIED>; T2=<…>`.
