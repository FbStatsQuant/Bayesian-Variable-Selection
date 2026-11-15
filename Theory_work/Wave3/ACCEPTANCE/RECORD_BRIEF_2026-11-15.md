# Recording brief — supersessions (cards 1, 3), MIS headline move (card 2), W3-POST2 acceptance (HQ, 2026-11-15)

You act **for HQ** (Claude Opus 5.5, effort high, Claude Third, on Owls). You may change git state only as below:
commits to `main` pushed as fast-forwards from your own worktree. Never force-push, never rewrite history, never touch
other branches or the root clone `/home/fb31/Bayesian-Variable-Selection`, where other agents work.

Setup: `cd /home/fb31/Bayesian-Variable-Selection && git fetch origin && git worktree add -b hq/record-1115
/home/fb31/BVS-wt/record-1115 origin/main`. Work there. Push with `git push origin HEAD:main`; if main moved, rebase
your commits onto it first.

Read first:
- `Theory_work/INFRA/LIFECYCLE.md` §0, §3 and §5 (supersession, `implies`, headline flags, re-points), and
  `Theory_work/INFRA/README.md`;
- `Theory_work/Wave3/PROTOCOL_v4.md` §7–§8 and amendments **H2(c), H5**. Under H5, headline changes need the HQ
  consultant's AGREE, which replaces the owner approval in LIFECYCLE §0. Cite H5 and the consultant's verdict wherever
  a tool or record asks for the approver;
- the consultant's verdicts, quoted at the end of this brief.

`HOLDS.md` must have no HOLD on any claim involved.

## Tasks (dry run first for each, in a disposable `git clone --no-hardlinks` under /tmp; real run only on 0 problems)
1. **Card 1, W3-RM → W3-RM2 (AGREE).**
   - `propagate.py supersede` W3-RM:RM-F by W3-RM2:RM2-F, and RM-R by RM2-R. Record the `implies` edges (Y ⇒ X) with
     the evidence pointers: Cont-F / Cont-R accepted by both council seats, and (C4) covering both hypothesis routes of
     RM-F. Find the exact review files on main (W3-RM2/reviews/).
   - Move the headline flag to RM2-F / RM2-R, and add their sharpness/binding rows. Model them on RM's rows; mark them
     `headline-strength pending` if the gates aren't recorded.
   - Keep RM-0 and E4 ACTIVE.
   - The tombstones must stay citable, because Cont-F/R and W3-RM:Examples cite them.
   - Add a note on the RM tombstone: the old cap ℓ_n under (N-χ) remark is not carried to RM2 (a non-shipped
     configuration).
2. **Card 3, 8 W3-START rows → W3-START2 (AGREE).**
   - Supersede exactly the eight rows START2 lists (STATEMENT l.213–224, the 8th is BR), each with its `implies` edge
     and its evidence: both seats checked each implication, e.g. Sol R1 l.47 and Opus R1 l.21 for NEC.
   - The superseded rows keep their acceptance and frozen files, and patch propagation must still reach START2.
     Verify this with a `propagate.py patch … --dry-run` on one row; write nothing.
   - START:MIS, EX, F1, F3 and F4 stay ACTIVE.
3. **Card 2, C-MIS / W3-MISR (OBJECT → consultant's alternative, adopted by HQ).** No supersession.
   - Move the headline flag from C-MIS:Thm-MIS(i)/(ii) to W3-MISR's main rows (MIS(i), MIS(ii); MIS(i′) if C-MIS's
     inclusion clause was headline).
   - Keep C-MIS:Thm-MIS(i)/(ii) ACTIVE, de-headlined, with a note of exactly what MISR implies and what it does not:
     main clauses yes; the inclusion clause only for c > c₁ via MIS(i′); for c₀ < c ≤ c₁ only through the unchecked
     Remark P, which consumes the parent; and GD(b) → Thm-MIS(ii) is a live premise of Cor-G(b).
4. **W3-POST2 acceptance (PROTOCOL v4 §7 checklist).** POST2 passed council C1 (both seats 8.6, all gates PASS; see
   `Theory_work/Wave3/W3-POST2/REPORT.md` and reviews/). Its rows still read "PROVED (by this seat, unchecked)". MISR is
   conditional on them.
   - Run the acceptance on main:
     - `manifest.py verify` / `bind` for the C1 round;
     - consumed claims valid (`check.py --consumed-vs` if available);
     - citecheck 0 MISS;
     - staged ingest of REPORT's registry block (its CHECKPOINT/REPORT blocks), then `check.py --acceptance <ids>`
       with 0 ERROR;
     - every "checked" sentence names a review file.
   - Note `eb1f9da` ("POST2 D(b) suspect + repair pending check"). The repair passed council, so confirm the passing
     manifest contains the repaired D(b).
   - **A failure of form** (table layout, line ends, a status file outside the manifest): under v4 §7, fix the record
     (carrier file, addendum), not the mathematics, and say what you did.
   - **A failure of substance** (verify mismatch on a mathematical file; a seat that did not ACCEPT a claim): stop for
     POST2 and report it.
5. After all real runs: `check.py --quiet` with 0 ERROR, and `test_lifecycle.py` passing (report the count).
   Append one entry to `Theory_work/Wave3/HQ_DECISIONS.md` that lists what was recorded, with the commit hashes.

## Report
Final message, at most 15 lines: per task, what was recorded (ids), commit hashes, check.py totals, test count, or the
exact refusal (check id + message). No other agents.

## Consultant verdicts (2026-11-15, verbatim summary)
- Card 1 AGREE: the implication is itself a checked claim (Cont-F/R accepted by both seats; (C4) covers both
  hypothesis routes of RM-F). Conditions match in substance (TH09 / W2-APP:POST). Move the headline flag; add RM2
  sharpness/binding rows. W2-APP:POST@1.0.1 is now visibly unchecked, the weak point. The ℓ_n (N-χ) remark is not
  carried over; note it on the tombstone. RM-0 and E4 stay ACTIVE; the tombstones stay citable.
- Card 2 OBJECT: MISR's checked claims do not imply the full parents (STATEMENT l.249–252: main clauses only; the
  inclusion clause for c > c₁ via MIS(i′); for c₀ < c ≤ c₁ only via the unchecked Remark P, which consumes the parent;
  GD(b) uses Thm-MIS(ii)). No implication was checked for Cor-H or Cor-G. Instead: move the headline flag to MISR,
  keep C-MIS(i)/(ii) ACTIVE and de-headlined with a note, supersede later. Record POST2's acceptance first.
- Card 3 AGREE: all eight rows (the 8th is BR) at STATEMENT l.213–224, each implication checked by both seats. The
  superseded rows keep acceptance and frozen files; patch propagation must still reach START2. MIS, EX, F1, F3 and F4
  stay ACTIVE; restating them under START2's hypotheses is a cheap rider. Record the `implies` edges with evidence.
