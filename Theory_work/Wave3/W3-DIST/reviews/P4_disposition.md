# W3-DIST — disposition of pre-check P4 (`reviews/P4_opus_precheck_B.md`; Claude Opus 5.5, Claude Third; filter, not a review layer)
Object: `work/B_transfer/H.md`, `T.md`, `DIST3.md`. Verdict: VERIFIED-WITH-AMENDMENTS; 0 CRITICAL, 0 MAJOR, 2 MINOR, 2 NIT.
Lemma H VERIFIED; Lemma T VERIFIED (as stated, same range and remainder, failure probability δ/2, no external result);
DIST-3 VERIFIED-WITH-AMENDMENTS (c = 1).
| finding | sev. | disposition |
|---|---|---|
| DIST-3's statement does not quantify n₀ and its constant C must depend on C_T | MINOR | ADOPT in STATEMENT (queued, tag EQUAL): n₀ = n₀(s₀^r, σ*², M, B, κ₀); C = C(s₀^r, σ*², M, B, C_T, κ₀); c = 1 |
| STATEMENT §3 route text of Lemma T cites the ratio inequality 4S(2n)e^{−nη²/4}, which no proof relies on | MINOR (editorial) | ADOPT (queued): point to `work/B_transfer/T.md` Proposition R (one-sided inequality, proved in the file) |
| T.md header understates the slack | NIT | no change to the proof file |
| DIST3.md Step 1, event of probability 1 | NIT | no change |
Stream B's three wording clarifications (rename (TR₀)'s direction u → w; record c = 1 and n₀'s dependence; M, B, C_T fixed
in the corollary): judged justified; queued for the next STATEMENT version.
Comparison: T.md, API T-a-1 and T-c-1 all prove the stated η²_n(d, δ) on the same range; T-a-1 relies on an external
theorem that would need a source check; T.md needs none and is the proof of record.
