# Council round 1 — result and disposition

Seats (fresh, independent, effort high, launched 2026-11-09 15:25 CST):
* Seat A — Codex gpt-6-astra, high: `reviews/C1_council_astra.md` — **GATES: G1 PASS, G2 PASS, G3 PASS, G4 PASS, G5 PASS, G6 PASS; SCORE: 9.0**
* Seat B — Claude Opus 5.5, high, on claude-personal: `reviews/C1_council_opus.md` — **GATES: G1 PASS, G2 PASS, G3 PASS, G4 PASS, G5 PASS, G6 PASS; SCORE: 8.9**

**Round 1 PASSES** (both ≥ 8.0, all six gates, same round). Neither seat raised a FATAL, MAJOR or blocking issue. Both seats
reviewed STATEMENT v1.1.3. The non-blocking items below were applied after the vote. They change wording, evidence records or
citation tooling only; no hypothesis or conclusion changed. STATEMENT v1.1.3 → v1.1.4 (NIT-3 status wording in (i′)).
Markers [C1-…].

| Item | Class | Disposition |
|---|---|---|
| A-1 | MINOR | FIXED. L2_k0 §11 self-citations made explicit (`W2-UNI/STATEMENT.md:22-23`, `:103`); they now resolve to W2-UNI and pass the content assertions. Resolver hardened: the previous-line rule no longer applies to bare top-level ticket files (STATEMENT.md/REPORT.md/…), so a mis-attribution now fails the self-citation content assertion. A scan of CITECHECK.txt found no other bare self-citation resolved to another ticket. |
| A-2 | MINOR | FIXED. "Exact/certified κ" → "exhaustive numerical estimates (ordinary floating point, no rounding enclosure)" in C_corollaries, L4_k1 Remark (2), REPORT §6. The algebraic κ = 1 for (block) CS is unaffected. |
| B MINOR-1 | MINOR | FIXED. `reviews/CITECHECK_AUDIT.md` written: a manual content audit of every citation and quoted status from `CITECHECK_excerpts.md`, by a separate auditor seat, before the REPORT's CITECHECK line was filled. |
| B MINOR-2 | MINOR | FIXED. REPORT headline: "Every family result listed in lemmas/C_corollaries.md (STATEMENT §5) is an instance, a separate extension, or a marked partial version; GEN's masked-truth theorems (LH, LH-iid, W), PXN and FAC-L's BM-∞ relaxation remain separate imported results". "banded/ARMA" moved to the §6 examples. |
| B MINOR-3 | MINOR (sharpening; seat B: "the theorem as stated is correct") | NOT INCORPORATED into the locked statement, by decision. Replacing κ by the joint ratio κ_J := max{1, sup κ′_{l,T}√(h_𝒢(T)/s_T)} ≤ κ would strengthen a locked statement that has already been swept and passed by the council, and that strengthening has not been through the lemma check. It is recorded in REPORT §7 as the first open item, with seat B's two-line argument and its p = 9 numbers (`reviews/C1_scratch_opus/joint.py`). Status there: "suggested by council seat B; unchecked". |
| B MINOR-4 | MINOR | FIXED. L4_k1 item 5: FACA L5.1 uses fixed θ* only through M = s₀θ_hi², the BM-∞ envelope and the TV-pop Lipschitz constant (FACA `L5_random_instances.md:12`), so it applies to coefficient sequences in [θ_lo, θ_hi]. Verified at the source. |
| B NIT-1 | NIT | FIXED. L6 header: I([p]) range "for p ≤ 800 (not computed at p = 3200)". |
| B NIT-2 | NIT | FIXED. L4 Remark (1): "K := 1 (|Ψ_jk| ≤ √(Ψ_jjΨ_kk) ≤ 1), any a > 0". |
| B NIT-3 | NIT | FIXED. STATEMENT (i′) heading: LOC2 L5 "PROVED (by this seat, unchecked)", R04 VERIFIED-WITH-AMENDMENTS, inside W2-LOC2 "PROVED-CHECKED" (verified at `W2-LOC2/lemmas/L5_assembly.md:3-5`). |
| B NIT-4 | NIT | FIXED. REPORT §5 states that R03, R04 and R05a ran at xhigh before the binding effort cap of 2026-11-09 was issued; every review after resumption (R05b, C1 A/B) ran at high. |
| B NIT-5 | NIT | FIXED. REPORT UNI-1 headline: "(R): TV-pop (sufficient: PTV); (E): TV on the actual blocks". |
| B NIT-6 | NIT | FIXED. L2_k0: GROW L6 quoted with R07 Sol "VERIFIED" and R06 Opus "VERIFIED-WITH-AMENDMENTS" (APP `L3_LOC.md:3-5`). |
