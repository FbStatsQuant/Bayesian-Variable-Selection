# W3-FAMC — E2 coverage note (for the recorder's RM2-side check-status update; lead, 2026-11-17)

Source of evidence: `reviews/E2_check_opus_R1.md` (claude-opus-5-5, claudeAgent_personal, high; seat "Opus E2 check",
round R1; not an author of E2, BC or IR; committed 2ba7730a; sha256 6c65796c31897a3a03881946cf19b907690e91d388de236c1d56d3726f85679d;
bound in W3-FAMC council manifests R4 and R5 as an #EXTRA input). Below, "report :N" means a line of that file.
**Rule (HQ):** the recorder covers only what the seat covered. This note claims nothing beyond the report's own verdict
rows. Where the report is silent, the item is listed as not covered.

**Scope of the whole check (report :3-8, :70-72).** The seat checked E2 *as far as W3-FAMC consumes it*. It worked on one
instance: Σ_lk = ρ^|l−k| with fixed ρ ∈ (−1, 1), π = id, α = 3, b = 1/4, ϱ = 1/120. (V-R)/PTV(a₀) is explicitly out of
scope (report :8). The seat says "I re-derived every step below by hand" (report :8).

Paths: POLY = `Theory_work/Wave2/W2-LOC2/lemmas/L6_poly.md`; L6 = `Theory_work/Wave3/W3-RM2/lemmas/L6_examples.md`;
RM2S = `Theory_work/Wave3/W3-RM2/STATEMENT.md`; RMS = `Theory_work/Wave3/W3-RM/STATEMENT.md`;
L5R = `Theory_work/Wave3/W3-RM2/lemmas/L5_formR.md`. Line numbers are at main a1d55cef (identical at 2ba7730a).

## 1. Read and checked in full (verdict PASS in the report)

| registry claim | what was checked | span (file:line) | scope of the check | evidence (report) |
|---|---|---|---|---|
| `W2-LOC2:Lemma-BC@1.0.0` | statement (registered span POLY:78-84) and the whole proof | POLY:78-109 | **M = 15** (\|U\| ≤ 15, m = \|U\| + 2 ≤ 17) only, with "any positions"; the K_15 formula as restated at L6:45-56. The statement's "for every fixed integer M" is **not** covered for M ≠ 15 (POLY:111 records that only M = 15 is used) | :18 |
| `W2-LOC2:Lemma-IR@1.0.0` | statement (registered span POLY:118-129) and the whole proof, incl. (P2) and (P3) | POLY:118-167 (P3: :162-167) | verdict row labelled **α = 3**. The reasoning tracks constants depending on (c, K_dec, α) and summability needing α > 2, but the PASS is given for α = 3. The general α > 2 reading is **not** separately certified | :19, :20 |
| `W3-RM2:Ex-PolyR@1.0.3` (E2; registered statement RM2S:259-275, premises L6:164-263) | the §0 estimates E2 uses: regression identity, (0.1), (0.2), the choice r = ⌊√log n⌋ | L6:76-84 (identity at :79), L6:86-95, L6:97-101 | §0's estimates under §0's own hypotheses (spectrum [c, C], polynomial envelope); instance as above | :21, :22, :23, :24 |
| same | E2's verification list: R_Q and (2.2); (L-size^b); (L-feas); (L-gain-R); (L-loc-R); (T1-R); (FL-R); (D-loc^b) and its match to the input of `W3-RM2:D-to-W` | L6:176-201, :183-187, :180, :211-245 | **instance only:** α = 3, b = 1/4, ϱ = 1/120, π = id, AR spectrum. Not covered: E2's general class (other α > 2, other b ∈ [γ, ½), general injections π, general Σ with polynomial envelope) | :25–:32 |
| (supporting text read, not a registry claim) | the RM2/RM hypothesis definitions the items are checked against; the L5R requirements of Lemma D-loc^b and its spectral event | RM2S:178, :180-185, :194-202; RMS:126-133; L5R:108-117, :19-22 | as cited in each row | :27–:33 |

## 2. Used but NOT read or not re-derived by the seat (stays unchecked by this seat)

| item | how it enters | status of coverage |
|---|---|---|
| The implication (D-loc^b) ⇒ (D-R^b) ⇒ (W-R) (`W3-RM2:D-to-W@1.0.3`) | E2's last step | taken as given: the row reads "PASS (conditional on the stipulated RM2 implication)" (report :33); the seat checked only that E2 supplies its inputs (:32). That claim is already PROVED-CHECKED in the registry |
| `W3-RM2:RM2-R` (the theorem E2 instantiates) | E2's conclusion | not examined |
| `W2-APP:POST` (a condition of Ex-PolyR) | (T1-R) ⇒ [POST] | not examined (registry: PROVED-CHECKED) |
| The block-inverse/Rayleigh arguments that BC and IR cite: `APP/lemmas/L2_CT.md:55` (POLY:109; `W2-APP:CT`) and `LOC2/lemmas/L3_CTd.md:73` (POLY:165) | spectral claim in BC's proof; first part of (P3) | not opened (no citation in the report). The report checks the spectral conclusion of BC directly (:18; note 1 at :62-64) and (P3)'s formula directly (:20) |
| PTV(a₀) / (V-R) | E2's assumed hypothesis | out of scope by design (report :8) |
| L6 §0 lines not cited by any row: L6:33-44 (setting of §0), :57-75 (definitions of f, F, J, D from IR) | definitions behind rows :18 and :22 | used through those rows (the (0.1) row relies on J and D); **not separately verdicted**. The recorder should count them only as far as rows :18 and :22 reach |
| Rest of POLY (§0 and §§3–7: POLY:28-75, :172-477) and of L6 (header, E1, E2's old-cutoff ledger, E3–E5, table: L6:1-32, :104-163, :249-263, :264-573) | not consumed by FAMC | not read for this check |

## 3. Wording notes (non-blocking; no verdict change)

These are the report's three notes (:60-68). They are prepared as `reviews/RM2_wording.patch` (CORRECTION-ONLY; sha256s
in `reviews/RM2_wording.sha256`) with a PURE check in `reviews/RM2_wording_check_opus.md`.

## 4. AR-specific cross-check (not E2)

Report :37-58 closes the AR(1) case independently of BC and IR. It uses `C-GROW:C5a` (P1)–(P4) (PROVED-CHECKED) and an
explicit two-neighbour Markov regression. This supports W3-FAMC's AR half directly, but it is **not** a check of BC, IR or
E2 and must not be counted for them.
