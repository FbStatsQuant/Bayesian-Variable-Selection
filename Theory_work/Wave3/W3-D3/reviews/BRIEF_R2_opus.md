# BRIEF R2 (diff round after R1; Opus-only per the ticket) — council seat `opus`, W3-D3 (saved before launch)

Seat: Opus 5.5 high (providerInstanceId claudeAgent_personal), fresh agent (new thread). Manifest: `reviews/MANIFEST_R2.txt` = MANIFEST f559960469015b9c993e17cc82b3955ceee2890db189b8ae23e2aa2f1f4840a6.

---

You are the `opus` seat of diff round R2 for ticket W3-D3, checkout `/home/fb31/BVS-wt/W3-D3` (read-only for you except the
one reply file below). Write no file outside the worktree; no TMPDIR; scratch only in `/home/fb31/BVS-wt/W3-D3/.rc_tmp/`,
deleted at the end. No git state changes. Do not read LOG.md, CHECKPOINT_*.md, or any disposition file.

**Context.** Round R1 (`reviews/MANIFEST_R1.txt`, MANIFEST de19cf54f91f81defa8bc75a5b174e01a697ea75c3984f70106efaa23a39b768): both
seats accepted all three claims (W3-D3:Thm2SG, W3-D3:B3w, W3-D3:ExSG). Both failed the gates on one S finding (S1) in prose
outside the registered spans (card text REPORT §3; REPORT §2; READER_DELTA): the centring qualifier for the Song–Liang
implication and the common-constant qualifier for the feature mixtures were dropped. The Opus seat also gave E1–E6. By the
ticket's rule this diff round is run by the Opus seat only, and it must judge the Sol seat's findings too. Read the two R1
reviews: `reviews/R1_council_sol.md` and `reviews/R1_council_opus.md`.

**Scope (exactly).** The diff since R1: `reviews/R2_diff_since_R1.txt` (all ticket files except reviews/ and LOG). Check with
`reviews/MANIFEST_R1.txt` and `reviews/MANIFEST_R2.txt` which files changed. Read every changed hunk and its DEPS dependents.
DEPS.tsv rows S:B3w (STATEMENT §2), S:ExSG (§3), P:B3w (`lemmas/B3w.md`), P:ExSG (`lemmas/ASSEMBLY.md` "Proposition ExSG") and
R:registry (REPORT §6; statement line ranges moved) are STALE and will name this review as their check: verify each of those
spans' content in full against STATEMENT and the sources. Search the whole frozen ticket (not only the diff) for any other
place where the Song–Liang implication, the NH14 relation or the feature-mixture examples are stated without the qualifiers
of STATEMENT §§4–5. Do not re-review unchanged mathematics; do not add E findings.

**Answer.** (a) For each R1 finding (Sol S1; Opus S1, E1–E6): RESOLVED / NOT RESOLVED, one line of reason; (b) does the diff
introduce any C, S or F finding (with file:line)? Claim span STATEMENT §1 must be unchanged; the §2 (c) and §3 (b) changes must
be the EQUAL clarifications recorded in the changelog (confirm or contest each 1.3 row's tag); (c) per-claim table
`| id | decision |` (ACCEPT / REJECT / NOT-EXAMINED) for W3-D3:Thm2SG, W3-D3:B3w, W3-D3:ExSG; (d) the six gates — correct,
strength, faithful, statuses, sweep, reader — PASS/FAIL, one line each, on manifest R2; (e) a score 0.0–10.0 (C, S, F only)
and the verdict line below. **You must give `gates=FAIL` if you hold any C, S or F finding of your own, whatever severity you
would give it.**

Write your full reply to `Theory_work/Wave3/W3-D3/reviews/R2_council_opus.md` (create it; write nothing else anywhere),
and return the same content as your final message.

## Verdict line (mandatory, machine-checked)

You are reviewing the content frozen as `MANIFEST f559960469015b9c993e17cc82b3955ceee2890db189b8ae23e2aa2f1f4840a6` (round R2, seat `opus`). End your review with
exactly ONE line of its own, in exactly this form (no other text on the line; backticks around it are allowed):

```
COUNCIL-VERDICT round=R2 manifest=f559960469015b9c993e17cc82b3955ceee2890db189b8ae23e2aa2f1f4840a6 seat=opus score=<x.y> gates=PASS|FAIL
```

- `score` is your overall score (one decimal, 0.0–10.0); `gates=PASS` only if EVERY gate passes on exactly this
  manifest; otherwise `gates=FAIL`.
- Write no other line containing `COUNCIL-VERDICT` (not for an older or newer manifest, not as an example, not in
  prose). If you did not review exactly the content of this manifest, write `gates=FAIL`.
- Quoting the digest elsewhere in the review does not count as a verdict; this line is what CP3 acceptance and
  `manifest.py bind` read, and they refuse a review with zero, several, malformed or contradictory verdict lines.
