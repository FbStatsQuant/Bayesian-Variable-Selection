# BRIEF R1 — council seat `sol`, W3-D3 (saved before launch)

Seat: Sol (codex, gpt-6.1-sol, reasoningEffort high), fresh agent (OpenAI seat). Manifest: `reviews/MANIFEST_R1.txt` = MANIFEST de19cf54f91f81defa8bc75a5b174e01a697ea75c3984f70106efaa23a39b768.

---

You are the `sol` seat of council round R1 (blind first read) for ticket W3-D3 (Tier B), checkout
`/home/fb31/BVS-wt/W3-D3` (read-only for you except the one reply file named below). You have not reviewed this ticket before.

**Files and scratch.** Write no file outside the worktree; set no TMPDIR. Scratch only in `/home/fb31/BVS-wt/W3-D3/.rc_tmp/`
(git-ignored), deleted at the end. Never write inside `Theory_work/Wave3/W3-D3/` except your reply file. No git state changes.
Do not read `LOG.md`, `CHECKPOINT_*.md`, or anything in `Theory_work/Wave3/W3-D3/reviews/` other than this brief,
`reviews/MANIFEST_R1.txt`, `reviews/INPUTS_R1.txt` and `reviews/CITECHECK.txt`. Python with numpy, if you want to compute:
`/home/fb31/SMC_Theory_Department/ci/venv-numerics/bin/python`.

**What the ticket claims.** Theorem 2 of the paper (claims card row 1.2: posterior concentration on a random design) with the
Gaussian row law replaced by sub-Gaussian predictors on sparse directions ((A4)), as a claim that **coexists** with row 1.2
(row 1.2 and its master `W2-APP:POST` unchanged). The proof reuses W3-DIST's population-to-sample bridges (B0, B1, B2-core,
B2 (a), B3's argument on Theorem 2's window) and W3-POST Theorem 1 item 6. Claims: `W3-D3:Thm2SG` (STATEMENT §1),
`W3-D3:B3w` (§2), `W3-D3:ExSG` (§3, families satisfying (A4), including bounded features via Hoeffding's lemma). The class of
the new hypothesis (owner rule D109) is ruled by HQ (STATEMENT §5, outside the registered spans; check its mathematics only).

**Read (the frozen content).** `Theory_work/Wave3/W3-D3/`: STATEMENT.md, lemmas/B3w.md, lemmas/ASSEMBLY.md, REPORT.md,
TARGET.md, READER_DELTA.md, PLAN.md, DEPS.tsv, numerics/ (scripts + outputs), citecheck.py, deps_hand.py, API_CARD.md
(+ api_request_build.py). Sources (`reviews/INPUTS_R1.txt`): read what the proofs cite, in particular W3-POST STATEMENT
:16-100 (target; Theorem 1, regime R1, item 6); W3-DIST STATEMENT :385-417 and `work/E_bridges/B0.md`, `B1.md`, `B2core.md`,
`B2.md`, `B3.md`; W3-READER `lemmas/R1_set_sizes.md` (B1.2, B1.3); READER_VERSIONS :26-30 and :257-290 (recorded Theorem 2);
NOTATION §§1–2; L1_POST.md (row 1.2's Gaussian bridge, for comparison).
Registry rows (quoted; do not open registry files): `W3-POST:Thm-1@1.0.1` "PROVED-CHECKED; council C3, MANIFEST
420c1cb0b13771355c19f3412ac6d03fe325de3c62ab851b978c9d32c0d85d22, astra=8.8 PASS, opus=8.7 PASS"; `W3-DIST:B0`, `B1`, `B2core`,
`B2` @1.0.1 "PROVED-CHECKED; council R2, MANIFEST 9719c81705729389283bcc99a31cdef06afe84bafef076cbfbadead951b9ed1a (= R2 c5cd9cdd
re-frozen CITATION-ONLY as R2r), astra=9.3 PASS, opus=9.2 PASS"; `W3-DIST:B3@1.0.1` "PROVED-CHECKED, conditional on
W3-POST:Thm-1 (for its last sentence); council R2, …"; `W3-READER:R1@1.0.2` "PROVED-CHECKED; council R3, MANIFEST
7aebdf2eb126058719114df656d0eaf416adb1ae3d21138cb11b51d7075d2263, sol=9.5 PASS, opus=9.4 PASS".
Take the consumed claims as true as stated; check that their hypotheses hold where used.

**Break it.** Check every step of the proofs against STATEMENT and the sources: that the window covers every set used and
that B2-core's size condition holds for n ≥ n₁(s₀, A, L); the constants after the scale reduction B0; the completed pair
(X°, θ°), supp θ° = S₀, measurability of 𝒜′_n, and every hypothesis of item 6 and regime R1; the transfer from completed to
actual outputs, including the conventions of STATEMENT §0 for removed columns; ExSG (a), (b) and the in-place proof of
Hoeffding's lemma; whether any hypothesis is used but not stated; whether each Gaussian step of row 1.2's bridge (L1_POST)
is really covered. Sweep duties (Tier B): STATEMENT copies vs lemma statements; each lemma's scope vs its use; REPORT and
its registry blocks vs STATEMENT (REPORT must restate nothing beyond STATEMENT; HEURISTIC/OPEN labels; the card text of
REPORT §3 claims nothing beyond STATEMENT); DEPS rows spot-checked against the review files named there; the STRONGER tag
(STATEMENT §8) and the changelog tags (§9). **Interpretive sentences:** list every "hence …", "so …", "in particular …",
"this means …", "reading" or "interpretation" sentence inside the registered spans (STATEMENT §1, §2, §3) and give each a
verdict (checked / must move out / false).

**Return.** (a) per-claim table `| id | decision |` (ACCEPT / REJECT / NOT-EXAMINED) for W3-D3:Thm2SG, W3-D3:B3w, W3-D3:ExSG;
(b) findings, each tagged **C** (a step is wrong or unproved), **S** (claims more than proved, or uses an unstated hypothesis),
**F** (unfaithful to the code, a cited source or STATEMENT) or **E** (editorial; never blocks), with `file:line` and what fails;
(c) the interpretive-sentence list; (d) the six gates — correct, strength, faithful, statuses, sweep, reader — PASS/FAIL with
one line each; (e) a score 0.0–10.0 (reflecting C, S and F only) and the verdict line below. "A stronger theorem is provable"
is not a finding: list it separately as a better-theorem proposal.
**You must give `gates=FAIL` if you hold any C, S or F finding of your own, whatever severity you would give it.**

Write your full reply to `Theory_work/Wave3/W3-D3/reviews/R1_council_sol.md` (create it; write nothing else anywhere),
and return the same content as your final message.

## Verdict line (mandatory, machine-checked)

You are reviewing the content frozen as `MANIFEST de19cf54f91f81defa8bc75a5b174e01a697ea75c3984f70106efaa23a39b768` (round R1, seat `sol`). End your review with
exactly ONE line of its own, in exactly this form (no other text on the line; backticks around it are allowed):

```
COUNCIL-VERDICT round=R1 manifest=de19cf54f91f81defa8bc75a5b174e01a697ea75c3984f70106efaa23a39b768 seat=sol score=<x.y> gates=PASS|FAIL
```

- `score` is your overall score (one decimal, 0.0–10.0); `gates=PASS` only if EVERY gate passes on exactly this
  manifest; otherwise `gates=FAIL`.
- Write no other line containing `COUNCIL-VERDICT` (not for an older or newer manifest, not as an example, not in
  prose). If you did not review exactly the content of this manifest, write `gates=FAIL`.
- Quoting the digest elsewhere in the review does not count as a verdict; this line is what CP3 acceptance and
  `manifest.py bind` read, and they refuse a review with zero, several, malformed or contradictory verdict lines.
