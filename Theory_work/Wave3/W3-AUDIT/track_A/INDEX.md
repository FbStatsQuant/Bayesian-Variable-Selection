# W3-AUDIT track A — lemma tickets (Tier B), index

Order: CHECKPOINT_1 annex of the audit Fable (`../CHECKPOINT_1.md`; statements `../AUDIT.md` §6 T1–T10), per the
manager 2026-11-16. Code of record for code-facing items: `Scripts/SMC_BVS/core/` at 4676af6 (= HEAD for the core).
"Claude LC" = blind Claude line check (Opus), the stand-in for Sol while Codex is held for the gate.

| # | item | blocks | folder | lemma | state | Lean |
|---|---|---|---|---|---|---|
| T1 | GUARD-W | 3.1, 3.5, 3.6 | `T1_GW/` | GW (i)–(v) | PROVED; Claude LC VERIFIED WITH AMENDMENTS (applied); Sol: LOCK WITH CHANGES + VERIFIED WITH AMENDMENTS, applied (v5) | no |
| T2 | blocks ≤ 16 | 3.1, 3.6 | `T2_BLK/` | BLK (a)–(c) | PROVED; Claude LC VERIFIED WITH AMENDMENTS (applied); Sol: LOCK WITH CHANGES + VERIFIED WITH AMENDMENTS, applied (v5) | yes (BLK-b) |
| T3 | OP-LS0 | 3.1 | `T3_OPC/` | OPC (a)–(d) | PROVED; Claude LC2→LC4 VERIFIED WITH AMENDMENTS (applied); OpenAI pending | no |
| T4 | start-table encoding | 3.1 | `T4_ENC/` | ENC (a)–(c) | PROVED; Claude LC2→LC4 VERIFIED; OpenAI pending | no |
| T5 | CAL | 3.5, 3.6 | `T5_CAL/` | CAL-C (a)–(d) + 𝒜° flag | PROVED; Claude LC2→LC4 VERIFIED WITH AMENDMENTS (applied); OpenAI pending | no |
| T6 | START | 3.5, 3.6 | `T6_START/` | START-X (Z), (S), (S′) | PROVED; Claude LC3→LC4 VERIFIED; OpenAI pending | yes |
| T7 | KERNEL | 3.5, 3.6 | `T7_KER/` | KER (a)–(d) | PROVED; Claude LC3→LC4 VERIFIED; OpenAI pending | math half |
| T8 | P-OVL | 3.6 (Thm D) | `T8_OVL/` | OVL (a)–(c), under (A5) | PROVED; Claude LC3→LC4 VERIFIED WITH AMENDMENTS (applied); OpenAI pending | yes |
| T9 | start-mode DP | 3.1 delivery | `T9_TDP/` | TDP (a)–(e) | PROVED; Claude LC3→LC4 VERIFIED WITH AMENDMENTS (applied); OpenAI pending | yes |
| T10 | P1 / S.3 | 3.1 delivery | `T10_P1S3/` | re-audit (P1′), (S.3′), (D1) | AUDITED (second seat); Claude LC2→LC4 VERIFIED WITH AMENDMENTS (applied); OpenAI pending | no |
| T11 | P-OVL∞ | 3.6 remark (TR) | — | — | no ticket: kept as a named open premise (manager 11-16) | — |
| T12, T13 | SCORE-EXP, START-CENTRE | none | — | — | no ticket: not used by any core row (historical `W1-GEN` route only) | — |
| X1–X5 | (AUDIT §6) | | — | — | after T1–T10; the Fable marks relabelling-only items | |

States after the council round R1 (batch T1–T10): see `reviews/` and `CHECKPOINT_3.md` (this file is frozen in
`reviews/MANIFEST_R1.txt`).

Shared: `citecheck.py` (citation check), `reviews/` (briefs, verbatim replies, dispositions), `LOG.md`, `CHECKPOINT_k.md`.
