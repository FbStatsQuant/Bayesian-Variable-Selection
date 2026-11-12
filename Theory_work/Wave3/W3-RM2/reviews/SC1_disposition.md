# SC1 disposition (lead) — statement-change check by Codex gpt-6.1-sol (high)

Review: `SC1_statement_change_sol.md`, manifest 9af7889ee7da1292df93b4e802ce07e440a12e18c115428c33749bfd9fdae3dc
(STATEMENT v1.3 as first written; copies of the reviewed texts: `STATEMENT_v1.3_as_reviewed_by_SC1.md`,
`ASSUMPTION_MAP_as_reviewed_by_SC1.md`; the locked v1.2: `STATEMENT_v1.2_LOCKED.md`).
Verdict: **ACCEPT WITH CHANGES.** 14 diff hunks, none outside [CP1-P1], [CP1-P2] or the record items. The reviewer
re-derived by hand and passed: (BM-Q) ⇒ (BM-W) with the constants; (W-δ) ⇒ (W) and the chains of (C3)(c), (C4);
(C3)(a) with the rate and c*; (C3)(b) including the v1.2 converse as a special case; the truth-removal identity of
(P2) and the treatment of pairs with |T| = K; (W-R), (P8), (P9). "No CRITICAL defect or mathematical refutation was
found."

Four required changes, all on records; all accepted and applied (markers [SC1-#]):

| # | class | required | action |
|---|---|---|---|
| 1 | MAJOR | (C6) limits remark: say that the observation concerns the validated LS0 re-implementation from the start mode, that the sampler, the posterior input and the full method's reported model were not tested, that no asymptotic failure follows; exact start-size range 522–743 | remark replaced by the reviewer's text (file typography) |
| 2 | MAJOR | ASSUMPTION_MAP, first "unharvested" bullet still promised a polynomial rate under bare (W) | replaced by the reviewer's text: the rate is harvested in (C3)(a); polynomial only under (W-δ) |
| 3 | MINOR | registry A:W-R field still referred to the removed event 𝒲_n; ASSUMPTION_MAP's W-conv bullet used the removed 𝔴⁺ notation | both replaced by the reviewer's text |
| 4 | MINOR | registry binding of A:W, sharpness of A:W-R, ASSUMPTION_MAP binding bullet: must not read as a necessity theorem | replaced by the reviewer's text ("gap → +∞ forces failure; gap → −∞ sufficient; bounded gap undetermined; no necessity for reporting claimed") |

Also added: one sentence in the STATEMENT header recording this check. No hypothesis, claim, bridge statement,
constant or code pin differs between the text SC1 reviewed and the current v1.3. Per PROTOCOL rule 15 the diff
(record-only) is attested by an independent Sol reviewer in the next round (lemma check LC1-A, task 0).

One point where the lemma files follow the reviewer rather than the statement's wording: the reviewer bounds
a⁺ + a⁰ by 2√((2A + 3) log n) "eventually"; `lemmas/L2_width.md` uses 2√((2A + 4) log n) for all n ≥ 2 — a weaker
constant in the corollary only; nothing in STATEMENT depends on it.
