R2 diff review, seat `sol`. I reviewed the five changed files against my R1 review and their permitted masters/dependencies. Both manifests contain 28 files; exactly `DEPS.tsv`, `ERRATA.md`, `READER_DELTA.md`, `REPORT.md`, and `deps_hand.py` changed. All 28 current file hashes match MANIFEST_R2. The unchanged formal-proof conclusions and sweep results are carried forward from R1.

Disposition of my R1 findings:

1. **F1 — RESOLVED:** [READER_DELTA.md:61](/home/fb31/BVS-wt/W3-MISR-R/Theory_work/Wave3/W3-MISR-R/READER_DELTA.md:61) now labels (A0) sufficient and discusses necessity at contrast level; the replacement introduces the separate finding below.
2. **F2 — RESOLVED:** [READER_DELTA.md:42](/home/fb31/BVS-wt/W3-MISR-R/Theory_work/Wave3/W3-MISR-R/READER_DELTA.md:42) assumes invertibility for the displayed inverse, and line 47 supplies the Moore–Penrose version for singular covariance, consistent with CorG-min(E1).
3. **F3 — RESOLVED:** [READER_DELTA.md:55](/home/fb31/BVS-wt/W3-MISR-R/Theory_work/Wave3/W3-MISR-R/READER_DELTA.md:55) separates individual-array contraction from uniform contraction and explicitly requires uniform selection convergence, common constants, and bounded support size; B4.4 names (UP).
4. **E4 — Deferred.**

The diff introduces one substantive finding:

**F-R2-1 — The new necessity sentence omits subtraction of the omitted contribution's linear candidate component.** [READER_DELTA.md:64-65](/home/fb31/BVS-wt/W3-MISR-R/Theory_work/Wave3/W3-MISR-R/READER_DELTA.md:64) says the residual-contrast property holds “if and only if the omitted part has the same property given the candidates.” CorG-min requires this property of the omitted part **minus** its linear candidate predictor: [STATEMENT.md:57-59](/home/fb31/BVS-wt/W3-MISR-R/Theory_work/Wave3/W3-MISR-R/STATEMENT.md:57), with necessity at lines 71–74. The unadjusted omitted contribution generally has different conditional means in different contrast coordinates, so its coordinates are not identically distributed.

For example, let candidate rows be iid N₂(0,I₂), let the omitted contribution be Z = bX₁ + ζ with b ≠ 0 and ζ iid N(0,τ²) independent of the candidates, and set y = Z + ε with independent iid N(0,σ²) noise, τ²,σ² > 0. Take β^𝒞 = (b,0). Given the candidates, Uᵀ(y − Xβ^𝒞) is N(0,(τ²+σ²)I), exactly the required residual law. But UᵀZ is N(bUᵀX₁,τ²I); for n ≥ 3 its coordinate means differ almost surely. Thus the omitted part itself fails the asserted iid property, although the exact reduction holds. This is already the master's linear-plus-Gaussian-noise example, and it satisfies the reader's energy, floor, and diverging signal conditions with fixed b and appropriate fixed M₀.

**Required correction:** describe both contrast laws as centred Gaussian, and state that the omitted contribution *after subtracting its linear candidate component* has conditionally centred spherical Gaussian contrasts; allow its variance to be zero. Keep the total residual variance positive, as in (OV^c).

No further new C, S, or F finding was found in the diff. The REPORT additions retain the lemma status strings, add the population-signal assumption, and restrict the additional Gaussian-row assumption ids to clause (G). The DEPS edge additions agree with the cited masters. Executing `deps_hand.py` with its sole output write redirected to memory reproduced the frozen TSV exactly: all ten rows are OK. A reversed-row-order check with a simulated stale notation hash propagated DOWNSTREAM through every dependent row. No checker output was written to disk.

| id | decision |
|---|---|
| W3-MISR-R:CorG-min | ACCEPT |
| W3-MISR-R:CorGb-plus | ACCEPT |
| W3-MISR-R:CorH-plus | ACCEPT |
| W3-MISR-R:CorH-U | ACCEPT |

These decisions retain the formal claims' stated conditional inputs; they do not approve the defective reader sentence or promote unchecked inputs.

- **correct: PASS** — the four formal claims and proofs are unchanged; the diff does not invalidate their R1 acceptance.
- **strength: FAIL** — the replacement reader sentence asserts an incorrect necessary condition, F-R2-1.
- **faithful: FAIL** — the reader drops the linear candidate subtraction required by (OV^c).
- **statuses: PASS** — registry status strings remain verbatim and declared conditional inputs remain visible.
- **sweep: FAIL** — the R1 sweep is carried forward and the permitted diff checks are complete, but F-R2-1 remains.
- **reader: FAIL** — the reader's new contrast-level necessity explanation still departs from its master.

Score: **8.6/10.0**, assessing C, S, and F only. The original three substantive findings are resolved, but the replacement necessity explanation introduces one substantive faithfulness defect.

COUNCIL-VERDICT round=R2 manifest=227720d3d5b3ef95adbc1e91f7835058d7858986ef4b173a4044f65ad49879ea seat=sol score=8.6 gates=FAIL
