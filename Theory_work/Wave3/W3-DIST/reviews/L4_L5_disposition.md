# W3-DIST — dispositions of the cross-family line checks L5 (Astra; S, V) and L4 (Sol; bridges and assembly)

## L5 — `reviews/L5_astra_SV.md` (gpt-6-astra, codex, high; S.md 45f03a2d7c719720, V.md dffd4ca5f2889158)
Verdict: VERIFIED-WITH-AMENDMENTS; 0 CRITICAL, 0 MAJOR, 2 MINOR, 1 NIT. **Lemma S VERIFIED** (the stronger n ≥ 3, t > 0 form),
**Corollaries S.1, S.2 VERIFIED**, **Lemma V (a), (b), (c) VERIFIED**.
| id | sev. | finding | disposition |
|---|---|---|---|
| L5-01 | MINOR | the bracket-event simulation in `c_checks.py` draws two dependent quantities independently; its frequencies are not estimates of P(𝓑_nᶜ) | ADOPT: numerical-validation claim withdrawn (S.md amendment A-5); the proof (Step 6) is unaffected |
| L5-02 | MINOR | STATEMENT's Lemma S writes R^T_m without its upper limit; with the sum to p, "m = m_n(t) qualifies" is false at the cap (p = 2^n family), though the probability bound is not | ADOPT: STATEMENT v1.4.1 writes the sum to K; S.md amendment A-6 |
| L5-03 | NIT | Toolbox (G) needs s > 0 | ADOPT: S.md amendment A-7 |

## L4 — `reviews/L4_sol_E.md` (gpt-6.1-sol, codex, high; hashes in its first line)
Verdict: VERIFIED-WITH-AMENDMENTS; 0 CRITICAL, 0 MAJOR, 5 MINOR. **B0, B1, B2-core VERIFIED**; B2, B3, ASSEMBLY/Theorem A,
ASSEMBLY/Theorem B VERIFIED-WITH-AMENDMENTS. Conditional on the given master displays, DIST-3, Lemma X′ and W3-POST
Theorem 1, which L4 did not review.
| id | sev. | finding | disposition |
|---|---|---|---|
| E-01 | MINOR | STATEMENT's B2 phrase "q_n ≥ m_n(M log n) + s" false when the window is capped by p | already applied in STATEMENT v1.4 (L4 read the earlier text) |
| E-02 | MINOR | B3 Step 4 repeats the capped-window error | ADOPT: B3.md amendment A-1 |
| E-03 | MINOR | ASSEMBLY §2: the common exceptional set is not proved for the statement without (A4) | ADOPT: ASSEMBLY amendment A-6 (joint event; n ≥ 10^{1/c}) |
| E-04 | MINOR | "c₃ ≥ 1" unjustified | ADOPT: ASSEMBLY amendment A-7 (c₃ > 0) |
| E-05 | MINOR | "R1 holds by (A2)": p_ret ≥ 2 only on the event of B1 | ADOPT: B3.md amendment A-2, ASSEMBLY A-8 (intersect with {p_ret = p}; completion argument) |
L4 on the law-free reading of the master displays: supported by STATEMENT's list of permitted dependencies; the
explicit sentence (added in v1.4 §0) is useful.

## DEPS consequence
V, B0, B1, B2-core, B2: OK (files unchanged since their check). S, B3, R/Theorem-A, R/Theorem-B: verified at their
checked hashes, then amended as the checkers prescribed → marked STALE until one cross-family diff check confirms the
amendments (to be batched with the STATEMENT v1.3.1 → v1.4.1 diff check).
