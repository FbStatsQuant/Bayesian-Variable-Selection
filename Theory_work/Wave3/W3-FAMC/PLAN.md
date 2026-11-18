# W3-FAMC — PLAN (v0.2; v0.2 = DP1–DP3 resolved, P7 staffing; 2026-11-17; lead Claude Opus 5.5 high, claudeAgent_personal)

Brief: `Theory_work/Dept/briefs/W3-FAMC_LEAD_BRIEF.md` (dept/theory). This is a Tier B assembly with no new lemma.
Budget: 1–2 lead-days, KILL at 3. Folder template: W3-D3. Branch: `theory/W3-FAMC` from origin/main f0b8246c.

## Step 0 — already recorded? Result: NOT recorded as a corollary; pieces exist (details in LOG.md, 11-17)

| source | what it has | registry id / status | gap for W3-FAMC |
|---|---|---|---|
| W2-APP `L4_families.md:165-180` (family map) | rows (c) AR(1) and (e) bounded blocks: "covered under PTV (automatic if ≤1 truth/block)" | `W2-APP:Family-map@1.1.0` "derived entries: PROVED (by this seat, unchecked)" | old LOC route (polylog Q); PTV assumed for AR; unchecked |
| W3-RM2 `lemmas/L6_examples.md` E1 | inherited UNI-0 (incl. banded/AR, bounded blocks, PTV assumed) and LOC-BF (≤ 1 truth per group, PTV automatic) | no own row; `W3-RM:Examples` SUSPECT; `W2-LOC2:LOC-BF` "PROVED (by this seat, unchecked)" | not checked; no sign or generic-position routes |
| W3-RM2 E2 (Ex-PolyR) | polynomial covariance decay on a line, α > 2, PTV **assumed** | `W3-RM2:Ex-PolyR@1.0.3` "PROVED; line-checked LC2-C; Astra seat ACCEPT; not examined by the Opus seat …" | visibility not primitive; AR not named |
| W3-RM2 Ex-Equi, Ex-Proxy | one equicorrelated group (b < 3/10), weak proxies | PROVED-CHECKED (council R1) | one-truth constructions, not families |
| C-GROW (C5)(a),(c) | AR(1) with separation ⇒ GROW's conclusion P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0 (iid rows, p ≤ n^A) | `C-GROW:C5a`, `C5c` @1.0.0 "PROVED-CHECKED" | older master (GROW; per-run, no common data event, no delivery); separation only |
| TRACK_B B8 / B9 / B10 | B8: "Corollary (primitive)" (blocks ⇒ (A3)); B9: "candidate, not proved" block corollary of Thm 6; B10 included | dossier text, no claim row | exactly this ticket's block half |
| Lemma VIS | (A3) from sign or generic-position routes, all families | `W3-AUDIT-V:VIS@1.0.0` PROVED-CHECKED | not assembled with (A4)–(A6) |

## Deliverables (PROTOCOL_v4; W3-D3 template)
- `STATEMENT.md` v1.0 (done; **to the manager before any review**).
- `lemmas/A_assembly.md`: the proof of §3 written out, with (BLK) items B.0–B.W in full, and (AR) as an E2 instantiation
  plus the visibility routes. The only computations are B.0 (Schur complement of a block-diagonal matrix) and
  β̄_{T,l} = β̄_{T∩N_l,l} (normal equations); everything else is a citation with line spans.
- `TARGET.md` (one page: target clause TC1 = Corollary FAMC; assumption map; parity row vs Theorem 6).
- `DEPS.tsv`, `citecheck.py` (copied from W3-D3, retargeted), `LOG.md`, `reviews/`.

## Steps
| # | step | who | gate |
|---|---|---|---|
| P1 | STATEMENT v1.0 + PLAN → manager (HQ sees the draft) | lead | **manager release** |
| P2 | `lemmas/A_assembly.md` + TARGET | lead | — |
| P3 | pointer and status table check: every path:line, version and verbatim status | Sonnet subagent (claudeAgent_personal; mechanical) | — |
| P4 | Sol line check R1 (gpt-6.2-sol, codex, reasoningEffort high; model-id header); triage against the acceptance filter; 1 line in `Dept/SOL62_QUALITY.md` (sent to the manager) | Sol | after release |
| P5 | class-1 search for (BLK)/(AR) as theorem conditions in BVS papers already in the record (TRACK_B citations only; no new reading list) | Sonnet subagent | optional; 2b stands otherwise |
| P6 | fixes, then diff round R2 | lead + Sol | — |
| P7 | council R3: Sol (gpt-6.2-sol, high) + a fresh Opus seat (claudeAgent_personal, high) that did not author the text, bound to one manifest (`reviews/MANIFEST_R3.txt`) | lead launches (brief step 4) | 2 distinct seats, bind |
| P8 | manifest.py v2 freeze (no registry files, no live logs); citecheck; CHECKPOINT; recorder dry run | lead / recorder | real run on HQ GO only |

## Decision points for the manager
- **DP1 (AR status) — RESOLVED (HQ, 11-17): AR half unconditional, on an independent Opus E2 check (PASS,
  `reviews/E2_check_opus_R1.md`).** Original options, kept for the record: The AR half has no new lemma; it is an E2 instantiation. E2 (`W3-RM2:Ex-PolyR`) is not fully
  checked (Opus seat not examined), and its inputs BC and IR are "PROVED (by this seat, unchecked)". Options:
  (a) record the AR half with the inherited conditional status (D126 expansion);
  (b) ask W3-RM2's owner for the pending Opus-seat examination of E2 (+ BC, IR) — not this ticket's files;
  (c) present AR as track-C evidence only (the brief's kill fallback).
  Recommendation: (a), with (b) requested in parallel. Option (c) would discard a proof that needs no new lemma.
- **DP2 — RESOLVED (HQ): keep every fixed ρ ∈ (−1, 1) and remark (iv).** Original text: v1.0 states every fixed ρ ∈ (−1, 1), with no uniformity in ρ. This is stronger than
  "moderate" and is what the masters give. Alternative: restrict to |ρ| ≤ ρ̄ < 1 for presentation only.
- **DP3 — RESOLVED (manager): reading confirmed.** Original text: The rule text is not in the repo ("recorded in the notes"). v1.0 reads it as: quote every
  input status verbatim and expand each "conditional on X" to X's current status. Please confirm.

## Risks
- E2's Q is a polynomial-radius neighbourhood (α = 3 ⇒ b ≥ 1/6). Exponential AR decay would allow a logarithmic Q, but
  that would need a new verification, which is not done (no new lemma).
- (BLK-g) and (AR-g) depend on B, which is defined over the whole design sequence; the statement quotes VIS's definition
  rather than restating it.

## Standing rules added during the ticket
- HQ (2026-11-17): run `ingest.py convert REPORT.md` (0 PROBLEM lines) locally before any Sol council call, so a format
  failure never costs a Codex call. `manifest.py` skips `reviews/`, so a review file a status rests on must be an #EXTRA input.
