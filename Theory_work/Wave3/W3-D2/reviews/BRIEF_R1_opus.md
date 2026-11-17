# BRIEF R1 — council seat `opus`, W3-D2 (saved before launch)

Seat: Opus 5.5 high (claudeAgent_claude_third), fresh agent (Claude seat). Manifest: `reviews/MANIFEST_R1.txt` = MANIFEST 6f8c05aa83e3063f9b48d8cf42c52c3f49261e0db36b6268419159bc95f06243.

---

You are the `opus` seat of council round R1 (blind first read) for ticket W3-D2 (Tier B), checkout
`/home/fb31/BVS-wt/W3-D2` (read-only for you except the one reply file named below). You have not reviewed this ticket before.

**Files and scratch.** Write no file outside the worktree; set no TMPDIR. Scratch only in `/home/fb31/BVS-wt/W3-D2/.rc_tmp/`
(git-ignored), deleted at the end. Never write inside `Theory_work/Wave3/W3-D2/` except your reply file. No git state changes.
Do not read `LOG.md`, `CHECKPOINT_*.md`, or anything in `Theory_work/Wave3/W3-D2/reviews/` other than this brief,
`reviews/MANIFEST_R1.txt`, `reviews/INPUTS_R1.txt` and `reviews/CITECHECK.txt`.

**What the ticket claims.** Theorem 2 of the paper (claims card row 1.2: posterior concentration for random Gaussian
designs) is re-derived from the omitted-variables master `W3-MISR-R:CorGb-plus@1.0.1` with no omitted columns, so that the
eigenvalue floor is asked on sets of size 3(A+1)(s₀+1) log n (instead of 5(A+1)(s₀+1) log n) and the conclusions hold in
expectation. Claims: `W3-D2:Thm2X` (STATEMENT §1, reader statement + clause (E)) and `W3-D2:Cor2X` (STATEMENT §2); deterministic
facts §3 inside Thm2X. HQ decision: the new form **coexists** with row 1.2 (row 1.2 unchanged); card sentence in REPORT §3.

**Read (the frozen content).** `Theory_work/Wave3/W3-D2/`: STATEMENT.md, PROOF.md, REPORT.md, TARGET.md, READER_DELTA.md,
DEPS.tsv, numerics/ (script + output), citecheck.py, API_CARD.md (+ api_request_build.py), PLAN.md. Sources (the
manifest's external inputs, `reviews/INPUTS_R1.txt`): read what the proof cites, in particular W3-MISR-R STATEMENT §§1–3
(:1-108) and `lemmas/G2_corr.md`; W3-MISR STATEMENT §0 and §2 (:17-123); W3-POST STATEMENT §0 (:16-39); W3-READER
`lemmas/R1_set_sizes.md`; READER_VERSIONS :26-30 and :257-282 (recorded Theorem 2); NOTATION §1; L1_POST.md :8-33.
Registry rows (quoted; do not open registry files): `W3-MISR-R:CorGb-plus@1.0.1` "PROVED-CHECKED, conditional on W3-POST2:C,
W3-POST2:E, W3-POST2:A1, W3-POST2:A0, C-MIS:GDb, C-MIS:Prop-P; council R3, MANIFEST 052ea6dffa0495584b051435b1e82d6b7c598d965e3b13ddc067545728728069, sol=10.0 PASS, opus=9.6 PASS";
`W3-READER:R1@1.0.2` "PROVED-CHECKED; council R3, MANIFEST 7aebdf2eb126058719114df656d0eaf416adb1ae3d21138cb11b51d7075d2263, sol=9.5 PASS, opus=9.4 PASS";
`W3-POST2:C@1.0.6` "PROVED-CHECKED, conditional on W3-POST:Prop-LB, W2-APP:POST"; `W3-POST:Prop-LB@1.0.0` "PROVED (by this seat, unchecked)".
Take the consumed claims as true as stated; check that their hypotheses hold where used.

**Break it.** Check every step of PROOF against STATEMENT and the sources: the q = 0 instance of the master; identity of the
posteriors; the floor step (B4.1's domain, thresholds in n); constants and quantifiers of clause (E); the deterministic
facts; Markov steps; the corollary's reduction and its quotation of the recorded Theorem 2; whether any hypothesis is used
but not stated. Sweep duties (Tier B): STATEMENT copies vs PROOF; each step's scope vs its use; REPORT and its registry blocks
vs STATEMENT (REPORT must restate nothing beyond STATEMENT; HEURISTIC/OPEN labels); DEPS rows spot-checked against the
review files named there; the STRONGER tag and the two caveats (STATEMENT §7). **Interpretive sentences:** list every
"hence …", "this means …", "reading" or "interpretation" sentence inside the registered spans (STATEMENT §1 lines 29-48, §2
lines 50-58, §3 lines 60-63) and give each a verdict (checked / must move out / false).

**Return.** (a) per-claim table `| id | decision |` (ACCEPT / REJECT / NOT-EXAMINED) for W3-D2:Thm2X, W3-D2:Cor2X;
(b) findings, each tagged **C** (a step is wrong or unproved), **S** (claims more than proved, or uses an unstated hypothesis),
**F** (unfaithful to the code, a cited source or STATEMENT) or **E** (editorial; never blocks), with `file:line` and what fails;
(c) the interpretive-sentence list; (d) the six gates — correct, strength, faithful, statuses, sweep, reader — PASS/FAIL with
one line each; (e) a score 0.0–10.0 (reflecting C, S and F only) and the verdict line below. "A stronger theorem is provable"
is not a finding: list it separately as a better-theorem proposal.
**You must give `gates=FAIL` if you hold any C, S or F finding of your own, whatever severity you would give it.**

Write your full reply to `Theory_work/Wave3/W3-D2/reviews/R1_council_opus.md` (create it; write nothing else anywhere),
and return the same content as your final message.

## Verdict line (mandatory, machine-checked)

You are reviewing the content frozen as `MANIFEST 6f8c05aa83e3063f9b48d8cf42c52c3f49261e0db36b6268419159bc95f06243` (round R1, seat `opus`). End your review with
exactly ONE line of its own, in exactly this form (no other text on the line; backticks around it are allowed):

```
COUNCIL-VERDICT round=R1 manifest=6f8c05aa83e3063f9b48d8cf42c52c3f49261e0db36b6268419159bc95f06243 seat=opus score=<x.y> gates=PASS|FAIL
```

- `score` is your overall score (one decimal, 0.0–10.0); `gates=PASS` only if EVERY gate passes on exactly this
  manifest; otherwise `gates=FAIL`.
- Write no other line containing `COUNCIL-VERDICT` (not for an older or newer manifest, not as an example, not in
  prose). If you did not review exactly the content of this manifest, write `gates=FAIL`.
- Quoting the digest elsewhere in the review does not count as a verdict; this line is what CP3 acceptance and
  `manifest.py bind` read, and they refuse a review with zero, several, malformed or contradictory verdict lines.
