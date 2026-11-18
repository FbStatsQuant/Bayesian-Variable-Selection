# LC1 — disposition (lead), 2026-11-17

LC1 (`reviews/LC1_line_check_opus.md`): VERIFIED-WITH-AMENDMENTS, no correctness defect. All 13 findings ACCEPTED and applied
(markers [LC1-#] in the files). Note: during LC1 the lead fixed 4 citation-form errors in L2 found by citecheck
(L2 at a91eb7cb → 22fde420: bare `:a` continuations made explicit, `v3_engine.h:379-424` → `:379-419`); LC1 independently
reported the same ranges (LC1-8). All post-LC1 edits are in the diff a91eb7cb..HEAD of STATEMENT.md and lemmas/.

| finding | tag | where applied |
|---|---|---|
| LC1-1 reason for "right sides → 0" incomplete | F | STATEMENT (C3)(ii) (changelog v1.1); L3 Step 2 already correct (via (0.1)) |
| LC1-2 n with s₀ > K | S | STATEMENT §1 convention (𝓜_n = 𝒦_n := ∅, ε_n = 1); L3 (0.3) sentence |
| LC1-3 reader-form sentence inside the claim span | F | moved to STATEMENT §5 remark 5 (D109 wording) |
| LC1-4 identity of LS0 with 𝒦_n's search: cite the code pins | F | L2 B4 cites W3-RM2 `STATEMENT.md:60-67` via RM2R `:39-41`; E4 marked context only |
| LC1-5 p_ret = p a.s. | E | L3 (0.3a) |
| LC1-6 output only on two branches | E | L3 Step 1 |
| LC1-7 SPEC §4 exceptional rows do not fire | E | L3 Step 1 |
| LC1-8 line ranges | E | L2 (all eight) |
| LC1-9 canonical sorted vectors; p_ret ≥ 1; first offer | E | L2 D2 |
| LC1-10 R′ not tied to 4 | S | L2 B2 |
| LC1-11 scored set = 𝓜^run citations | E | L2 Step C |
| LC1-12 order of (c)/(e); F real-valued | E | L1 (0.5) and Setting; STATEMENT (C1) hypothesis (changelog v1.1) |
| LC1-13 cite (b⁺) not (a′) | E | L3 (0.1); STATEMENT (C3) preamble |

STATEMENT changelog row v1.1: all EQUAL (to be confirmed by the council seats). Repairs re-checked by a targeted Opus
re-check of the diff (LC1R, fresh agent) before the council freeze.
