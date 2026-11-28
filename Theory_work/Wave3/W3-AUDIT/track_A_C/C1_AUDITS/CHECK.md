# C1 · Check of C-DLV:P1-Inventory and C-DLV:L2-S3 — CHECK (Tier B per PROTOCOL_v4 §2, §2A NORMAL)

Status (lead's label): **PROVED; Sol LOCK; line checks: Claude CLC1 (1 C → amendment A-7, all applied), Sol CSL1
VERIFIED WITH AMENDMENTS (2 E, applied); council pending.** Verdict on the registered audits: both hold at pin 4676af6
after amendments A-1–A-7; A-7 (row B1′, SMC LS0 worst-case preflight) is the one coverage defect; no correctness break
on row 3.1 (DLV-0's (E2) excludes the B1′ exit by 𝒜_n's P̄_LS0; Sol CSL1 confirmed). Consumer table for HQ:
`../P1_CONSUMERS.md`.

Frozen text (sha256, first 12 hex, 2026-11-16 20:19 CST, for council C-R1): STATEMENT `e4ec41131924`, PROOF `3d2d820fb467`.
Code of record: `Scripts/SMC_BVS/core/` at 4676af6 (= HEAD for the core).

| Tier B step | who (NORMAL) | state | record |
|---|---|---|---|
| 1 statement lock | Sol, fresh | **LOCK** (CSL1) | `../reviews/CSL1_reply_sol.md` |
| 2 better-theorem review | — | not applicable (verdict on registered audits; no new theorem) | — |
| 3 line check | Claude stand-in (blind) | CLC1 **NOT VERIFIED** (1 C, 1 S, 3 E) → all accepted, v2 | `../reviews/CLC1_reply_opus.md`, `CLC1_disposition.md` |
| 3 line check (Sol) | Sol | **VERIFIED WITH AMENDMENTS** (2 E, applied, PROOF v2.1); A7-complete = yes; DLV0-E2-excludes = yes | `../reviews/CSL1_reply_sol.md` |
| 6 citation check | script | **0 bad** (225 citations) | `CITECHECK.txt` |
| 7 council C-R1 | Sol + Opus, blind | MANIFEST 221ca4e1: Sol 9.3 PASS (no findings); Opus 8.5 FAIL (1 F: A4's two terms; 6 E) → all applied (STATEMENT v2.1, PROOF v2.2) | `../reviews/CR1_council_{sol,opus}.md`, `CR1_disposition.md` |
| 7 diff round C-R2 | Opus (D91: diff-only re-check) | pending | `../reviews/MANIFEST_CR2.txt`, `DIFF_CR1_to_CR2.patch` |

Reuse: T10 (`Theory_work/Wave3/W3-AUDIT/track_A/T10_P1S3/`, council-bound R2) for the re-located map and S.3 steps.
**Note for the `C-DLV:L1-R` / `:Cor-R` / FIN M_G owners (C-R1 Opus E5; not C1's claim):** at the pin the SMC branch
builds a second (timing) context in the LS0 preflight (`v3_fit.R:12` via `v3_fit.R:47`), m = min(p, max(64, K)) columns,
so an m × m Gram and an n × m copy (`cpp/v3_score.h:41-52`); m can be about n/2. An X5 instance (coverage unaffected);
whether the word/memory envelopes count it on the SMC branch is for those owners.
Lean target: no.
