# S3 disposition — diff check of the post-S2 edits and the S2 repairs (fresh Opus 5.5 high; HQ overnight rule)

Review: `reviews/S3_diffcheck_opus.md` on `reviews/S3_frozen/MANIFEST_S3.txt` (21 hashes verified by the reviewer).
Verdict: **"S3-VERDICT: FIXES-NEEDED"** (no FATAL; one MAJOR introduced by the F2 repair; F7 partly open).
Lead: all items ACCEPTED; S3's tags ADOPTED (tagging by statement strength: a restored premise makes a clause WEAKER).

| # | Sev. | Repair | Tag (S3) |
|---|---|---|---|
| S2-F1, F3, F4, F5, F6, F8, F9 | — | RESOLVED per S3 | Thms 6–7 delivery clauses **WEAKER** (restore C-DLV:28-46, FINAL s6:29-35); Thm 10 scope **WEAKER** (restores W3-SAMP:29-41, 90-95, 186); card 3.6 **WEAKER** (restores W3-SAMP:158-162; Thm 10's convention); Thm 1′ title EQUAL |
| S2-F2 | — | resolved except N1 below | Thm 10 via (S5) **WEAKER** (restores N1:73-86, W3-SAMP:64-70) |
| S2-F7 | MINOR | R4 header now lists each input's status: SAMP:C, IF-START, START-R "PROVED-CHECKED"; W2-APP:POST and W3-POST:Thm-1 item 6 with their own labels; R1 "PROVED (by this seat, unchecked)" | — |
| N1 | MAJOR | (S5): "the final run's stream for each island independent of the data and of the calibration's streams" (restores W3-SAMP:39-41; needed by PoolZ's joint-law form) | undoes the STRONGER part |
| N3 | MINOR | exact-branch remark **withdrawn** (it was a new claim, STRONGER, and cited reader Theorem 2 with the wrong coefficient convention); replaced by "the exact-enumeration branch is not covered by this theorem" | removes the STRONGER item |
| N4 | MINOR | open item scoped precisely in Thm 1 (vi), Thm 3, card 1.3: an expectation lower bound $\gtrsim\sqrt{\log n/n}$ under a floor on $S_0\cup\{j\}$ (POST2-R1); in probability $\sqrt{\log n}$ shown only when $\log p\asymp\log n$ | EQUAL (non-claim) |
| N5 | NIT | remark (vi): "has been shown to be attained on the witness designs …; on other designs it is not known" | EQUAL |
| N6 | NIT | section versions and logs aligned (thm1 0.7, thm3 0.3, thm4 0.3, thm6/7 0.4, thm10 0.6), logs in order, thm3 log line added; card v0.6 with a changelog carrying the tags | — |
| N7 | NIT | card 1.1: "$c>c_1(s_0,A)$, an explicit constant, not optimised" | EQUAL |
| N8 | NIT | (a) START and KERNEL statuses quoted separately; (b) D-17 path marked "on `main` at f237bfa3 or later" | — |
| N9 | NIT | Thm 10 "why": the moderate-$n$ mixture statement is about $\pi$ only | EQUAL |
| N10 | NIT | METHOD_INTUITION §3: $c<\tfrac12$ for no imitators; $c<\epsilon$ for an imitator set of size $n^{1/2-\epsilon}$ | EQUAL |

Card row 1.3 (H5-6 narrowing to the witness designs): **WEAKER**, restores W3-PSHARP:92-110 (S3). Everything else EQUAL.
Next (HQ, v4 §4.2): fresh Sol statement-change check on the S2 diff + S3's findings + these repairs (11-16 after
midday), then DEPS → OK, then the CP3 freeze.
