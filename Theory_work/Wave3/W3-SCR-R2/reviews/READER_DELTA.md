# READER_DELTA.md — row 3.7 (Theorem 8, certified screening), from W3-SCR-R2 (CP3 package; RIDER_RULES §5, PROTOCOL_v4 H6)

Written 2026-11-16 by the W3-SCR-R2 coordinator, **after** the R3 bind (`bind: OK`, MANIFEST_R3 `19847f54…`, see
`../CHECKPOINT_2.md`). This file is for HQ → W3-READER, through the H5 card that goes with the CP3 package (HQ_DECISIONS,
11-16 overnight: "Then W3-READER states 'κ, b, M, σ fixed in n' in row 3.7's reader version, through an H5 card with the
CP3 package"). Nothing is written in W3-READER's folder, and no W3-SCR file is touched by this delta. The frozen manifests
are unaffected (this file is in W3-SCR-R2/reviews/, outside the W3-SCR tree).

**Read-only source.** `/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/READER_VERSIONS.md`, §8 "Theorem 8 —
Certified screening", row thm8, lines 727–816 (`<!-- ROW thm8 BEGIN/END -->`), section version 0.5. Branch
`theory/W3-READER`, file last changed at e20d287f (pushed); sha256 of lines 727–816:
`8b956c02cd7e935bdf17b770cfedb95282c2d81548ac94c3ae0efb6e9aeee074`. Card row: `CLAIMS_CARD.md:60` and `:100-104`.
**Masters.** `W3-SCR:A1@1.0.0` (`Theory_work/Wave3/W3-SCR/STATEMENT.md:158-163`) for Theorem 8; `W3-SCR:A-inf@1.0.0`
(`STATEMENT.md:87-90`, definitions at §1 `:49-63`) for Theorem 8′. Both were ACCEPTed by both seats in R2 (MANIFEST_R2
`96488f34…`) and in R3 (MANIFEST_R3 `19847f54…`), with all gates PASS in R3. STATEMENT.md is unchanged between the two
manifests.

## 1. Current reader text (thm8 v0.5): what it already says
- Theorem 8 (A1)–(A3), lines 731–747: the floor κ, signal minimum b₀, ℓ¹ bound M and noise variance σ*² are **named as
  fixed in n** ((A1) "a constant κ > 0 fixed in n"; (A2) "κ, b₀, M and the noise variance σ*² do not depend on n").
  Conclusion: P(output, Ŝ certified, |Ŝ| ≤ q_n, S₀ ⊄ Ŝ) → 0. n-varying signals are excluded (open item SCR-R1).
- Placements, lines 749–762: the abstract clause names all four constants as fixed in n. The body carries Theorem 8′.
  Forms: **(a)** plain if the second SCR round passes; **(b1)** a pending-review label; (b2) body only.
- Theorem 8′, lines 764–782: master A-inf in words. Its form depends on the R2 per-claim table: plain if A-inf is ACCEPTed,
  otherwise the (b1) label.

**Fidelity check against the masters, done for this delta.** I compared lines 731–747 and the abstract clause with
STATEMENT.md:158–163, and Theorem 8′ with STATEMENT.md:87–90 and :49–63.
- The four fixed-in-n constants, c₁ = κ²b²/(200(M²+σ²)), the q_n range, the conclusion event and the p ≤ n^A consequence
  all match. Theorem 8′'s ratio, τ_n² and Γ_n match. Nothing in the reader text claims more than the master.
- One harmless wording point. The reader calls γ(t|S) "the decrease" of the quadratic form. STATEMENT:54–56 defines
  γ = ((n+1)/n) × that decrease. The factor tends to 1, so the liminf condition is unchanged.

## 2. What changes (nothing in the mathematics; the form choice and the label lines only)
1. **Form (a) is selected** for row 3.7. The abstract clause stays, **plain**, still naming κ, b, M and σ as fixed in n
   (HQ card 7 ruling). The (b1) label and the (b2) option are removed.
2. **Theorem 8′ is plain.** A-inf is ACCEPTed by both seats in R2 and R3, so the (b1) label is not used.
3. **Gating.** Changes 1–2 take effect **only after acceptance**: HQ accepts the R3 result and the recorder replaces the
   registry's INTERIM LABEL on `W3-SCR:A1` and `W3-SCR:SCR-G` with the R3 council cell. Until then the reader keeps form
   **(b1)** for row 3.7, as now. The status string quoted in the reader stays verbatim from the registry (now
   "PROVED-CHECKED"; the label sits in the evidence field, not in the status).
4. **Optional honest-limit line** (proposed; W3-READER decides). The row's "Honest limits: None" could add the master's
   own exclusion: the theorem bounds the probability of an intersection. It does **not** claim that a run certifies a
   small model with probability → 1 (STATEMENT.md:217–218). The reader statement is already written as an intersection,
   so this line only makes that explicit.

## 3. New reader text (proposed, to apply after acceptance)
**Abstract clause (form (a), plain; unchanged wording except that c₁ is defined in place):** *"Certified screening: if
the design has a sparse eigenvalue floor κ on models of size q_n+s₀, the true coefficients satisfy θ*_min ≥ b and
‖θ*‖₁ ≤ M, the constants κ, b, M and the noise variance σ*² are fixed in n, and (q_n+1) log p + log n ≤ c₁n with
c₁ = κ²b²/(200(M²+σ*²)), then the probability that a run produces output, certifies a reported model of size at most
q_n, and that model misses a true predictor tends to zero — with no visibility, leakage, start or block condition."*
(If the abstract has no room for c₁, write "for an explicit constant c₁ depending only on κ, b, M, σ*". Either
way, c₁ must not be left undefined.)

**Theorem 8 (body):** keep lines 731–747 as they are (they already name the four constants as fixed in n).

**Placements block (replaces lines 749–762):**
- **Abstract:** the clause above, form (a), plain (second SCR council round passed: R2 + diff round R3, MANIFEST_R3
  `19847f54…`, both seats PASS; HQ acceptance of <date>).
- **Body:** Theorem 8′ (n-varying signals; master `W3-SCR:A-inf`), plain.

**Theorem 8′:** keep lines 764–778; replace the "Form dependency" paragraph (lines 779–782) with: *"Reviewed together
with Theorem 8 in the second SCR council round; A-inf ACCEPTed by both seats (stated plain)."*

**Honest limits (optional add, §2 item 4):** "The theorem does not claim that a run certifies a small model with high
probability; whether it does is reported from numerics."

**Update log line:** `v0.6 <date>: [W3-SCR-R2 CP3] form (a) for row 3.7 (second SCR council round passed, R3 bind OK
19847f54…); Theorem 8′ plain (A-inf ACCEPT); c₁ defined in the abstract clause (EQUAL).`

## 4. Bridges needed
None. Theorem 8 is the master A1 with the floor named in standard terms. Theorem 8′ is A-inf in words, with no new
argument. The changelog tag is EQUAL throughout: no hypothesis or conclusion moves. No new statement-change check is
needed, because the fixed-in-n wording was already in v0.3–v0.5 and matches STATEMENT:158–160, which R2 and R3 scored.

## 5. Not part of this delta
- SCR-R1 (dropping "fixed"): stays a post-freeze rider. `../SCR_R1_NOTE.md` answers YES (a short corollary of SCR-A with
  one side condition); it is not proved here.
- A1° (beta-min at rate σ√(𝐋_n/n)): a separate claim with different hypotheses (STATEMENT:165–169). The reader already
  keeps it out of Theorem 8.
- The registry INTERIM LABEL itself: the recorder replaces it after HQ acceptance, not this file.
