# W3-DIST — disposition of pre-check P2 (`reviews/P2_opus_precheck_X.md`; Claude Opus 5.5, Claude Third; filter, not a review layer)
Object: `lemmas/X.md` v0.2. Verdict: VERIFIED-WITH-AMENDMENTS; 0 CRITICAL, 0 MAJOR, 2 MINOR, 4 NIT. All applied in v0.3.
| id | sev. | finding | disposition |
|---|---|---|---|
| F1 | MINOR | n₀ defined as the least n where (a)–(g) hold; the proof needs them for every n ≥ n₀ | ADOPT: "least integer such that for every n ≥ n₀ …" |
| F2 | MINOR | §9: C₁′, C_v′, C, M₀′, n₀′ undefined; the v-step needs C_v′n^{−κ₀/2} ≤ 1; n₀′ must not contain condition (d) (c_D) | ADOPT: constants and a c_D-free n₀′ defined as proposed |
| F3 | NIT | interlacing order unstated | ADOPT |
| F4 | NIT | Σ_{k>m}q_k ≤ 2^{−m} is a line of the proof of `lem:prior`(c), not its statement | ADOPT: re-derived inline |
| F5 | NIT | list of uses of p ≤ n^A incomplete | ADOPT |
| F6 | NIT | §8 contains unproved remarks | ADOPT: §8 labelled commentary |
Comparison notes kept for the line checker: X-b-2's bound on s_y² is wrong when M > 1 (X.md's (E2) is right).
Not checked by P2: external tail inequalities against printed sources; §8 R1; the file X-b-1.md itself.
