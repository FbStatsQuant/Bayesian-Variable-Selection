# V2.1 status check: D2 "What we prove" and the assumptions section, against the frozen registry (Opus, 2026-11-17)

Sources: `.rc_tmp/claims_freeze.tsv`, byte-identical to `Theory_work/INFRA/registry/claims.tsv` at `theory-v2026-11-freeze` (d40c9780); card v1.13; pre-freeze registry a7fc for comparison only. Both PDFs match their current .tex.

Only non-OK rows are listed.

| id | location | document says | registry or card says | verdict |
|---|---|---|---|---|
| S1 | D2 `appendices.tex:64-65` (App. C, Convention C2) | "Theorems 5.3 and A.11 use (i)–(iv) on the domain 𝔇 where neither limit is reached." | Card 3.1 [T14-REP]: the 𝔇 form moves out of row 3.1. Theorem 5.3 in v2.1 states delivery under (C2p) only; the new App. C paragraph (l. 39-40) says only Theorem A.11 states the 𝔇 form. | STALE |
| S2 | D2 `appendices.tex:23` (notation table) | 𝔇 "delivery domain", pointing to §5 (`sec:reported`) and App. C | 𝔇 no longer appears in §5. It now appears only in App. C and Theorem A.11 (`supplement.tex:190`). | STALE |
| S3 | D2 `appendices.tex:115` (App. E, "What changed") | "Theorem A.7 no longer depends on another result" | `W3-DIST:Thm-B@1.0.1` "PROVED-CHECKED; council R2, …". The status condition was dropped (a7fc@1.0.0: "…conditional on W3-POST:Thm-1…"), but `depends_on` still lists `SOP:TH09@stmt` and the W3-DIST lemmas. Suggested wording: "no longer carries a condition". | WRONG |
| S4 | D2 `s1_results.tex:43-44` (Table 1, Result 4) | Consistency is conditional on "two results on the coded sampler that are themselves proved and checked" | `W1-N1:B@1.0.0` and `W1-N1:F@1.0.0`: "PROVED under the named premises of STATEMENT §2 — cross-family checked …". The table drops "under named premises". The status box (`\samplerconds`), §4 of the assumptions and the ledger all include it. | MISSING |
| S5 | `STATUS_LEDGER_FREEZE.md` / `.tex`, row "Theorem A.11" | Masters: only `RM2-F-plus@1.0.1` and `RM2-F@1.0.3`. Label: "no open condition". | Card 3.2 also lists `RM0-plus@1.0.1` and `DLV-0@1.0.1`, plus the two audits `C-DLV:L2-S3@1.0.1` and `C-DLV:P1-Inventory@1.1.1` ("CODE-CHECKED (second seat, code reading; …)"). The "no open condition" label depends on these rows, which are listed for Theorem 5.3 but not for A.11. | MISSING |
| S6 | Assumptions `assumptions.tex:296-297` (§4) | "the integer limits that the delivery convention lifts cannot be reached on any input R can represent (checked)" | Card 3.1: "in the default configuration neither can be reached on any input R can represent". `W3-AUDIT-AX:REP@1.0.0` ("PROVED-CHECKED; …") excludes non-default options under "Not claimed": a user setting `v3.ls0_ell` > 10⁶ triggers the limit. The qualifier is missing. | MISSING |
| S7 | Assumptions `assumptions.tex:288` (§4, posterior bullet) and l. 294-295 | Corollary A.8 is named only for "output description … checked against the code". The sampler conditions are attributed only to Theorem 6.2. | `W3-DIST:Cor-C@1.0.1`: "PROVED-CHECKED, conditional on W1-N1:B, W1-N1:F, EX-A (exact arithmetic); …". This is new at the freeze (a7fc@1.0.0: "conditional on EX-A"). `W3-SAMP:LT#@2.0.5` (worst-island bound) carries the same two conditions. | MISSING |

## Checked and OK (no rows)
- **A.** All the focus items match the frozen statuses.
  - Theorem 3.2's expectation bound: Prop-LB is the only unchecked condition. Lemma-1a′ is now PROVED-CHECKED. `W2-APP:POST` is a further condition, itself checked, and is not named, which is acceptable.
  - Theorem 6.2, Corollary A.8 and Remark 6.3(iii): conditional on B and F. The box text describes B and F correctly ("each island realises the frozen run", "conditioning on the frozen calibration preserves its identities").
  - Theorems 5.3 and A.11: no open condition.
  - Theorem A.7: unconditional.
  - Pooled evidence: PoolZ and FR are both PROVED-CHECKED.
  - Remark A.13: `TR@2.1.5` is PROVED-CHECKED, and the P-OVL∞ premise is open.
  - Theorem A.3's expectation bound correctly inherits Prop-LB: Claim E says "Claim C applies", and C is case (iii).
- **B.** Theorem 5.3's delivery clause and the sentence after it match card row 3.1 (T14-REP), in its one-sentence form. Nothing says "IDEAL-W⁺ = IDEAL-W".
  - The moved App. C sentence is correct. With n, p_raw ≤ 2³¹−1: ⌈log₂(n+p_raw+1)⌉ ≤ 32 ≤ 10⁶, and 32+⌊n/2⌋ ≤ 2³⁰+31 < 2³¹−1, so 𝔇 contains every representable input.
  - `DLV-0` states the 𝔇 form without the lift ("without the representability lift of IDEAL-W⁺, the same holds … in the supported domain 𝔇").
- **C.** Apart from S1, S2, S6 and S7, the grep finds no remaining "await/pending/not yet/revision/to be recorded/verified/unchecked". The hits that remain are correct: Prop-LB, the open A.13 premise, and "independently verified" for the two C-MIS lemmas, whose status is "R02 VERIFIED…".
- **D.** App. E "What changed" agrees with the a7fc→freeze diff, except S3. "What remains" agrees with the registry: Prop-LB is unchecked; RM2-R and RM2-F are still ACTIVE with supersession deferred (card 3.1/3.2); P-OVL∞ is open.
- **E.** All 55 key@version strings in the ledger match the registry: in `.md` (prefix + "…") and in `.tex` (mid-string `\ldots` elision). The map from column 1 to column 3 agrees with card rows 1.1–4.1, except S5.

## Notes (not counted)
- In App. C (l. 65), "C2p is the idealised machine of (i) with these two limits lifted" could be read as dropping (ii)–(iv). §2 (`s2_setting.tex:132`, "C2p *also* lifts") settles it. Rewording to "C2 with (i) so modified" would make App. C self-contained, now that Theorem 5.3 cites only C2p.
- The status box of Theorem 5.3 (`s5_reported.tex:91`) also lacks "in the default configuration". The sentence right after the theorem has it, so this is minor.
- App. E "What remains", item 2: "superseded masters … are retired" is in the present tense. The registry has them ACTIVE with an empty `superseded_by`. Suggested wording: "are to be retired".
- The internal App. E ledger quotes registry strings verbatim, so the PDF contains "council" 49 times. This is acceptable only because the appendix is internal and removed for submission.

STATUS-CHECK: ISSUES (7)
