# W3-SCR-R2 — second SCR council round on the current tree (Theory Department, 2026-11-16; HQ + consultant, H5 card 7)

Coordinator: Claude Opus 5.5 high (Claude Third), child agent of the Theory Department. This is a **review round**, not a
proof ticket: no mathematical edits to W3-SCR. Worktree `/home/fb31/BVS-wt/W3-SCR-R2` (branch `theory/W3-SCR-R2`).
Write the round's files in `Theory_work/Wave3/W3-SCR-R2/` (this folder). The only allowed write to the W3-SCR folder is
the frozen manifest `Theory_work/Wave3/W3-SCR/reviews/MANIFEST_R2.txt` (new file; no existing W3-SCR file is edited).

## Why
W3-SCR passed council C1 on its v3.3 text. Post-pass v3.4 edits (never re-scored) narrowed W3-SCR:A1 and SCR-G
(fixed-in-n κ, b, M, σ) and touched M4, the M6 prose and the ASSUMPTION_MAP construction. A fresh Sol PC read
(`reviews/PC_SCR_sol.md`, copied here) found A1-SUBSTANTIVE but the current proof valid. The v3.3 base is missing, so a
true diff round is impossible. A1 is headline row 3.7 (abstract). The consultant requires a short council round on the
**current** tree before acceptance. Target: done by **Thu 11-19 18:00 CT** (W3-READER's CP3 is Fri morning).

## Steps
1. `python Theory_work/Wave3/tools/manifest.py freeze Theory_work/Wave3/W3-SCR Theory_work/Wave3/W3-SCR/reviews/MANIFEST_R2.txt`
   (from the worktree root; TMPDIR under /home/fb31/SMC_Theory_Department/tmp/). Commit and push your branch right away.
2. Two seats, both fresh, both bound to that manifest. Briefs saved in this folder **before** launch, each carrying the
   block from `Theory_work/INFRA/templates/COUNCIL_BRIEF.md` (round R2, the manifest digest, its seat name).
   - **Opus seat** (claudeAgent_claude_third, Opus 5.5 high). Two tasks: confirm or reject each SUBSTANTIVE hunk named in
     PC_SCR_sol.md (A1, SCR-G, M4, the M6 prose, ASSUMPTION_MAP construction); give a per-claim table `| id | decision |`
     (ACCEPT / REJECT / NOT-EXAMINED) for **all 21 W3-SCR rows**. C/S/F/E tags; it must give gates=FAIL on its own C/S/F.
     It may read PC_SCR_sol.md, since this is a targeted round.
   - **OpenAI seat**: Sol (codex gpt-6.1-sol, high), a **fresh** agent. It re-issues the A1 proof-chain walk as a verdict on
     the same manifest, with a per-claim table for all 21 rows. Astra (gpt-6-astra) may be used instead, reading A1's
     chain. Same brief block.
   - Each seat ends with exactly one `COUNCIL-VERDICT round=R2 manifest=<digest> seat=<seat> score=<x.y> gates=PASS|FAIL`.
3. `python Theory_work/Wave3/tools/manifest.py bind Theory_work/Wave3/W3-SCR/reviews/MANIFEST_R2.txt <sol/astra review> <opus review>`
   must print bind: OK.
4. `CHECKPOINT.md` in this folder: both verdicts, per-claim tables, bind output, and any C/S/F findings with the
   disposition you propose (no edits to W3-SCR; findings go to the manager). End your run. The manager and HQ decide the
   record; the recorder replaces the interim label.
5. Short note `SCR_R1_NOTE.md`: is the post-freeze rider SCR-R1 (drop "fixed"; n-dependent bounds) a short corollary of
   the master SCR-A (W3-SCR STATEMENT)? Answer yes or no with a 5–10 line argument and file:line. No new proof.

Rules: never cancel agents; settle your own finished reviewers; timestamps from `date`; temp under
/home/fb31/SMC_Theory_Department/tmp/<YYYYMMDD>-W3-SCR-R2-<what>; nice; ≤ 16 cores; statuses verbatim.
