# W3-DIST — council diff round R2, seat astra

**Verdict summary:** ACCEPT on the frozen R2 manifest `c5cd9cdd30ecfe06a39b06ee0aa8b86f70d4b08425a98e9f4d09023de5282ddc`. R1-astra-01 is resolved: the affected per-claim statuses now carry the SOP:TH09 condition, with matching hypothesis edges. R1-opus-01 is repaired correctly: the rate gloss fixes A and preserves the actual radius and TC3. The diff introduces no correctness, strength or faithfulness finding. All six gates PASS and all 20 claims are ACCEPT at their stated conditional assurance levels. This is a diff review with the unchanged R1 conclusions carried forward, not a fresh audit of every proof or an upgrade of any external input.

Paths below are relative to `Theory_work/Wave3/W3-DIST/` unless stated otherwise.

## My R1 findings

- **R1-astra-01 — RESOLVED.** `REPORT.md` §1, rows S, X and X′, and their registry blocks now explicitly say “PROVED (by this seat), line-checked, conditional on SOP:TH09”. Their dependency edges are `SOP:TH09@hyp`. The same qualification is consistently applied to V and NEC. `REPORT.md` §5 identifies the locked T01 results as the conditional inputs and does not promote SOP:TH09 to PROVED-CHECKED. The source changes in `mkreport.py` and `REPORT_extra.md` produce precisely these exported statuses. The mathematical statements and proofs of these five claims are unchanged.
- **R1-astra-02 — RESOLVED for this round's recording requirement.** `ERRATA.md` E2 records the fixed-p numerical-language issue and the requested correction, including NEC's fixed-design, in-sample scope. The editorial correction remains unapplied, as required by the brief; this is not a claim that the original numerical prose has been corrected. It has no gate or score effect. The other seat's E-01 through E-06 are also recorded as E3 through E8.

## Does the diff break anything?

**1. Rate wording, proof paragraph and TARGET P3: no.** I read every hunk in `STATEMENT.md`, `lemmas/DIST12.md` and `TARGET.md`, then checked the constants and the dependent interfaces. The changed sentence does not alter (1.1), its t-range, its remainder, or any constant definition. Consequences (a), (b), (d) and (e) still follow from the same display; (c) now describes its fixed-A rate accurately. The bracket in `DIST12.md:70–72` correctly gives `C_X ≥ 4Λ ≥ 128[34(A + 1) + 2]` and `C_T = 4[34(A + 7) + 8]`. It does not claim that the displayed radius is linear in A.

DIST-2's proof in D.6 continues to use X′, the d₂ transfer event and the radius `C₂√(tℓ_n/n)`; none depends on the removed gloss. Reader Theorem A consumes the theorem displays, with constants allowed to depend on A: `work/E_bridges/ASSEMBLY.md:48–59` explicitly substitutes `t = M log n/C_⋆²`, while §2 makes the corresponding substitution for DIST-2. Thus its fixed-parameter rate and its version without (A4) remain valid. Corollary C consumes Theorem A's probability bound and divides posterior mass by the store mass (`work/D_output/COR_C.md:95–115`); it needs no uniform-in-A assertion. DIST-C likewise consumes (1.1) or (1.2) with their existing constants and radii, retaining its delivery premises, completed-run restriction and EX-A. The TARGET P3 comparison remains justified for fixed A and fixed sparsity, as in the stated setting. **R1-opus-01 is RESOLVED in my judgement.**

**2. REPORT, its source and its generator: no.** I checked every hunk, including the review-trail entries, §5, the file list, the DIST-1 rate field, all five changed status rows and all five changed registry blocks. The new hypothesis edges disclose the same inputs rather than discharge them. The detailed provenance remains in the proofs and the expanded DEPS `uses` cells. The other theorem statuses already carry SOP:TH09; their additional conditions are retained. V and NEC's added qualifications conservatively make their assurance explicit without weakening a target clause. The DIST-1 registry field correctly states the unsquared rate `sqrt((1 + s₀^r) log n/n)` with `(A, σ*², M, M′)` fixed. I generated REPORT entirely in memory and compared it byte-for-byte with the frozen file: they agree. The R1 review-trail entry agrees with the two R1 records; later review-trail assertions were not used as substitutes for this review's own diff checks.

**3. DEPS, ERRATA and PINS: no.** The DIST-1/2 proof hashes match v0.3 of `lemmas/DIST12.md`. The six expanded `uses` cells name the relevant locked inputs for DIST-3, S, V, X, X′ and NEC; I compared them with the import/use passages in those proofs. In particular, X′ retains the inherited size-tail inputs, V records its re-derived identities, and the prior-tail proof references are distinguished from the weaker printed statement. These bookkeeping changes introduce no new proof premise. The stretch rows receive the current statement hash and remain unchecked/open. PINS changes only its two current-version labels; statement lines used by the pins have not shifted. ERRATA parks editorial findings without changing any proof or theorem. Reverse reconstruction verified these changes against the R1 hashes, including the version-only PINS change.

**4. External W3-MISR input: no.** The external diff changes the version header and the KL interpretation in Corollary H. B0 consumes R′(a) and R′(a′), not that interpretation. I checked B0's quoted passages against the frozen source and verified that W3-MISR statement lines 70–72 and 75–77 are byte-for-byte identical to R1. B0's rescaling and its use by the reader assembly therefore retain their previous justification. W3-DIST's truth in `STATEMENT.md:19–22` has the deterministic intercept α*. No new restriction enters W3-DIST through the unused KL sentence.

## Named confirmations

**3(a) — TC3 unchanged and proved as written: CONFIRMED.** `TARGET.md:53` is byte-for-byte unchanged:

> Best radius ε_n² = C²M₀ log n/n with M₀ = O((1 + s₀^r)(A + 1)).

In `lemmas/X.md:34–40`, C_X is independent of s, and

`M₀ = max{16, (A + 1)s, log C₅} ≤ 16 + 4(1 + s)(A + 1) + 3(M + M′)/(2σ²)`.

For fixed `(σ², M, M′)` and A ≥ 1, this proves the stated O-bound. In `lemmas/DIST12.md` D.1, `M₀ ≥ (A + 1)s ≥ 2s` gives `d₁ log n ≤ 34t`, so `C_T = 4[34(A + 7) + 8]` is independent of s. D.4 then uses `C² = C_X² + C_X/2 + 1 + C_T` and `t = M₀ log n`. This proves exactly TC3, with s equal to the raw sparsity and with the existing asymptotic quantifiers. It does not assert a common n₀ for growing sparsity.

**3(b) — New fixed-parameter gloss exactly matches the proved rate: CONFIRMED.** For fixed `(A, σ*², M, M′)`, C is a positive constant independent of s. The displayed upper bound on M₀ is a constant times `(1 + s)`, and `M₀ ≥ max{16, (A + 1)s}` supplies a positive constant times `(1 + s)` lower bound. Thus the chosen squared radius is of order `(1 + s₀^r) log n/n`, including s₀^r = 0. This is the order of the proved radius, not a minimax lower bound. The remaining explicit A-factor is in the M₀ bound; the gloss makes no additional quantitative or uniform claim about A-dependence of the full rate. I agree with the v1.4.10 changelog tags: **EQUAL on TC3; WEAKER on the descriptive sentence only**. For fixed A, `log p_raw = A log n` when `p_raw = n^A` has the same n-order; fixing A removes the unsupported stronger reading of the old sentence.

## Gate table

| Gate | Verdict | Basis on this manifest |
|---|---|---|
| G1 — correctness of every step | PASS | Carried from R1 for unchanged arguments; the changed rate explanation and its dependent substitutions checked above introduce no invalid step. |
| G2 — hypotheses used = hypotheses stated | PASS | Carried from R1; fixed A is already in (RD), and the amended statements add no mathematical premise. |
| G3 — no hidden assumptions | PASS | Carried from R1; no implicit uniformity in A is needed, and the external KL edit leaves the consumed rescaling input unchanged. |
| G4 — imports and assurance | PASS | Re-decided: R1-astra-01 is resolved in both table and registry statuses, with `@hyp` edges and consistent generated sources. Existing conditional theorem statuses remain in force. |
| G5 — constants and rates | PASS | Re-decided for the changed gloss and the other seat's finding; explicit M₀, C_X and C_T accounting confirms TC3 and the fixed-A rate. Unchanged constant calculations carried from R1. |
| G6 — code and scope fidelity | PASS | Re-decided for assurance and scope: the unqualified-status defect is repaired and the rate language no longer overclaims. Unchanged code, output and NEC scope checks carried from R1. |

## Per-claim table

ACCEPT is conditional on each claim's disclosed inputs. Re-decided for the changed rate/status objects and affected dependents: DIST-1, DIST-2, DIST-3 (dependency record), DIST-C, Thm-A, Cor-C, S, V, X, X′, NEC and B0. All other decisions are carried from R1; B0's unchanged consumed input also preserves Thm-B's dependency path. S, X and X′ change from REJECT to ACCEPT because the assurance defect has been repaired.

| id | decision |
|---|---|
| W3-DIST:DIST-1 | ACCEPT |
| W3-DIST:DIST-2 | ACCEPT |
| W3-DIST:DIST-3 | ACCEPT |
| W3-DIST:DIST-C | ACCEPT |
| W3-DIST:Thm-A | ACCEPT |
| W3-DIST:Thm-B | ACCEPT |
| W3-DIST:Cor-C | ACCEPT |
| W3-DIST:H | ACCEPT |
| W3-DIST:T | ACCEPT |
| W3-DIST:S | ACCEPT |
| W3-DIST:V | ACCEPT |
| W3-DIST:X | ACCEPT |
| W3-DIST:X' | ACCEPT |
| W3-DIST:NEC | ACCEPT |
| W3-DIST:P6 | ACCEPT |
| W3-DIST:B0 | ACCEPT |
| W3-DIST:B1 | ACCEPT |
| W3-DIST:B2core | ACCEPT |
| W3-DIST:B2 | ACCEPT |
| W3-DIST:B3 | ACCEPT |

**New findings (C / S / F only): none.**

**Overall score: 9.3 / 10.** The repaired package is acceptable as checked mathematics at its stated conditional assurance levels. Editorial findings do not affect this score.

**Checks performed.** Read the full R2 brief first, then my full R1 review, the other seat's findings and the disposition. Read every diff hunk and the new ERRATA file. Verified the exact R2 manifest with `manifest.py verify`. A small inline Python check reversed every explicit diff in memory and matched the reconstructed content to its R1 manifest hash; separately verified PINS' version-only change and ERRATA's addition. The resulting coverage equals all ten changed manifest entries. Compared TC3 and the consumed W3-MISR lines byte-for-byte across rounds. Compared REPORT to its generator output entirely in memory, and checked the five conditional registry statuses and edges. Examined the targeted constants, dependency records and downstream interfaces described above. All computation used `nice -n 10`, one process and no parallel workers.

**Not checked.** Unchanged proofs and code were not independently re-audited; their R1 decisions are carried as permitted. I did not audit SOP:TH09 as a whole, re-audit W3-MISR's unused KL argument, rerun numerical experiments or sampler code, or independently authenticate the historical D5/D6 review-trail descriptions. No external input is promoted. No agents, cluster jobs, git operations or scratch files were used. This review is the sole file written.

COUNCIL-VERDICT round=R2 manifest=c5cd9cdd30ecfe06a39b06ee0aa8b86f70d4b08425a98e9f4d09023de5282ddc seat=astra score=9.3 gates=PASS
