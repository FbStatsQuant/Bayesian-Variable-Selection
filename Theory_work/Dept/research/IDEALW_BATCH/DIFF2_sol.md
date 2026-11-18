# IDEAL-W⁺ batch — fresh second diff review

Ran `git fetch -q origin` first. Reviewed all 20 current patches, the complete TR1 finding, the final A:IDEAL-W⁺ definition, the code, the F-UNI v2 patch and its review, and the first batch review. Independently checked the affected statements and their delivery, allocation and statistical assembly chains. Fetched `origin/main` is `8431b575`; its difference from `967313dd` is confined to `Theory_work/Wave3/HQ_DECISIONS.md`, outside every patch target. The target contents are identical at those two bases.

**(a) Truth and proof — PASS for the established claims, with their existing qualifications; XA:X4 remains unproved.** This is acceptance of the corrected diff, not certification that all 19 rows are proved theorems.

For the standard shipped cap, the sufficient domain gives

    le = ℓ_n ≤ ℓ_raw ≤ 10⁶,
    cap_ll = ℓ_n + |S̃₀| ≤ ℓ_raw + K_n ≤ ℓ_raw + ⌊n/2⌋ ≤ 2³¹ − 1.

Thus both additional rejection predicates are false on 𝔇 under plain IDEAL-W. Under A:IDEAL-W⁺ they are false by the explicit code idealisation. Configuration and the other existing premises still supply the remaining validator conditions. The exact branch returns before either validator (`Scripts/SMC_BVS/core/v3_fit.R:120-131`). The amended exit walk then combines input/scorer regularity, sufficient allocation and complete frozen tier-1 fallback to exclude no-output exits. The cited code ranges in `v3_run.R:93-101`, `cpp/v3_core.cpp:465-476` and `v3_fit.R:120-131` agree at the base and both method pins `4676af6` and `493579a`.

The claims use their own chains rather than deriving discovery from a small delivery-free error term:

- FAC-A L7 explicitly imports the complete raw-dimension allocation, including `W_G`, `M_G`, `P_e + A` and `P̄_LS0`. Its Steps 1–3 supply Lemma S inputs, the resource/exit argument, and discovery on Sand ∩ NA ∩ TL, together with the appropriate fixed-design or joint-law posterior expectation limit. FAC-L (D) repeats these premises. LOC2 L7 imports the same allocation and checks its own Gaussian-column/response regularity and its LOC-d, LOC-BF and polynomial-decay statistical inputs.
- FAC-B L5.1–L5.2 prove posterior concentration and discovery through its CS start/path events. Its L5.4 imports the full head preflight allocation. S5 L5 substitutes its BCS eigenvalue and path bounds: on the enlarged space, `P₀(𝒦_nᶜ) ≤ P̃(CC_n(δ)ᶜ) + o(1)`. Its imported delivery premises include those same preflight terms. The patch puts the unconditional error bound in (b), without asserting that CC itself has probability tending to one.
- FAC-X X6 proves the joint-law posterior expectation limit through common-constant design events and an every-sequence argument, and discovery through its own start/deletion path. X6.4 supplies input regularity and the full allocation. X10 supplies the corresponding fixed-Gram and iid general-loading chains, conditional on its recorded path inputs; its narrowed (G4) assembly agrees with the edited premise in `STATEMENT_T2.md:61-62`.
- UNI L5 states the complete FAC-A allocation. Its Instances supply UNI-0's local-covariance events/posterior inputs and UNI-1's full-lattice events/posterior inputs. The accepted F-UNI v2 supplies the corrected delivery reading. UNI-1's new assumption affects only its delivery conclusion; its data/path and output-intersected conclusions are preserved.
- FAC-PK L4.2 explicitly recharges the larger cap: at most `ℓ_n + 2K + 1` scans, enlarged work/memory envelopes and archive, and a measured-score preflight bound covering the whole timed interval. Its own PATH theorem supplies discovery, and L4.1 supplies the posterior input. Its delivery remains conditional on the proposed plumbing and inherited audit qualifications; see (e).

For consistency, D′ gives the pathwise bound

    P(output and wrong) ≤ 2E[1 − π(S₀)] + P(𝒦_nᶜ).

The relevant chain controls each term, with the S5 centre-condition remainder retained. Combining with unrestricted delivery in (b) gives the claimed asymptotic conclusion. Every edited asymptotic delivery conclusion, including S5's error bound, is under (b) only. Bounded 𝔇 supplies no asymptotic argument. XA:X4 has neither a completed discovery chain nor a proof upgrade: its original statement calls it a research target, its checkpoint leaves X2 open, and L8 §5 expressly does not assemble discovery or delivery consistency. The repaired note accurately preserves that status. A2/A3 are qualified in (f).

**(b) Scope — PASS.** The in-place edits restrict delivery or correct the identified implementation description. They preserve the other hypotheses, statistical laws and non-delivery conclusions. FAC-PK's explicit plumbing restriction concerns delivery only. The appended notes explain the restrictions and retain existing qualifications; the repaired XA note adds no theorem.

Reconstructed all 20 results in memory without applying any patch. Hunk contexts and counts agree with the base; existing edits are line-for-line, and additional lines occur only after the old last line. Reproduced all 20 before/after whole-file hash pairs, all 99 affected claim hashes and their stored base hashes, and all 142 listed citation-span changed/unchanged checks in `LINES_CHECK.md`. The affected-claim enumeration covers every registry row whose statement or premise file is touched. Exactly **17 batch claim hashes plus W1C-FINAL:Lemma-CAP** change: 16 batch statements and X10 through its premise. FAC-B:L5 and S5:L5 retain both their statement and premise hashes. No existing span moves; A2's BOM is preserved. All 15 appended full definition paragraphs match `FUNI_NARROW/A_IDEALW_PLUS.md:10` verbatim, and the original IDEAL-W paragraph is unchanged.

**(c) Tags — PASS with the corrections in (h).** WEAKER, with a major bump, is appropriate for the 17 changed guarantees/targets: the old unrestricted delivery conclusion now needs stronger premises, while plain IDEAL-W retains only a sufficient restricted-domain guarantee. For XA this is a weaker target, not a proved result. The two unchanged registered consistency statements are UNCHANGED and keep version 1.0.0.

| id | (a) true & proved? | (b) scope OK? | (c) tag |
|---|---|---|---|
| W2-FAC-A:Prop-F-FAC | Yes; L7 Steps 1–3, inherited qualifications | Yes | WEAKER; major |
| W2-FAC-A:Thm-FAC-L | Yes; (D) imports the full F-FAC chain | Yes | WEAKER; major |
| W2-LOC2:F-LOC2 | Yes; own regularity, events and posterior inputs | Yes | WEAKER; major |
| W2-LOC2:F-LOC2.exp | Yes; exponential class and narrowed L7 premise | Yes | WEAKER; major |
| W2-LOC2:F-LOC2.poly | Yes; polynomial class and narrowed L7 premise | Yes | WEAKER; major |
| W2-FAC-B:Thm-FAC-CS | Yes; L5.1–L5.2 and restricted L5.4 | Yes | WEAKER; major |
| W2-FAC-B:L5 | Yes; registered (C3) chain unchanged | Yes; delivery edit outside its spans | UNCHANGED; keep 1.0.0 |
| W2-FAC-PK:Thm-FAC-PK | Yes, conditional on stated plumbing; (e) | Yes | WEAKER; major |
| W2-FAC-S5:Thm-FAC-BCS-R | Yes; S5 L5, retaining CC remainder | Yes | WEAKER; major |
| W2-FAC-S5:L5 | Yes; registered (C3-R) chain unchanged | Yes; delivery is the separate row below | UNCHANGED; keep 1.0.0 |
| W2-FAC-S5:L5.C4-R | Yes; full allocation and S5 discovery bound | Yes | WEAKER; major |
| W2-FAC-X:Thm-FAC-CS-iid | Yes; X6 joint-law chain | Yes | WEAKER; major |
| W2-FAC-X:Thm-FAC-GL | Yes, conditional on recorded path inputs | Yes | WEAKER; major |
| W2-FAC-X:X10 | Yes; same chain with narrowed (G4) premise | Yes | WEAKER; major |
| W2-FAC-XA:X4 | Not established; X2 discovery remains open | Yes; R1 preserves target status | WEAKER target only; major; retain PARTIAL |
| W2-UNI:UNI-0 | Yes; UNI-0 inputs and F-UNI v2 | Yes | WEAKER; major |
| W2-UNI:UNI-1 | Yes; UNI-1 inputs and F-UNI v2 | Yes | WEAKER; major |
| HQ_AUDIT-W1C:A2 | Yes for the specified method/allocation; (f) | Yes | WEAKER; major |
| HQ_AUDIT-W1C:A3 | Yes as qualified restatement of A2; (f) | Yes | WEAKER; major |

**(d) Errata — PASS.** E1 identifies the actual stop sites and distinguishes the base-cap validator from the non-stopping start-mode enumeration cap. Its threshold `n + p ≥ 2^(10⁶)` is correct for `ℓ_n > 10⁶`; X8 depends on the start-mode size. Their class (d) exclusion under A:IDEAL-W⁺, or their exclusion on 𝔇, agrees with the code and TR1. R2 makes the summary's uniqueness assertion conditional on excluding both validators.

E2 may append the new sites while preserving the historical S.3 registered span: it expressly states that no internal invariant excludes them, that the old S.4 union does not contain them, and that a shipped-method exit walk must exclude them separately. It does not silently enlarge S.4's null-event assertion. E3 correctly distinguishes IDEAL-W from the stronger assumption and the specified C-DLV method from the later shipped LS0 validators. The specified method has no such tests; the unchanged C-DLV claims do not establish an unrestricted shipped transfer. E4 correctly repairs that same distinction in s7, retaining Lemma-CAP's specified-method scope. Its premise hash changes through line 39, so the indicated erratum/patch bump is appropriate despite its unchanged statement span.

**(e) FAC-PK — PASS; admissible conditional use of the same guard, not a widening.** The registered definition identifies the lifted disjunct as the code predicate `cap_ll > numeric_limits<int>::max()`, with `int` read as unbounded. The displayed `ℓ_n + |S̃₀|` is its shipped assignment. The PK statement separately requires the proposed plumbing to retain that guard, evaluated at `cap_ll = a(data)`, and explicitly identifies that evaluation in (b). Thus the assumption removes the same code rejection disjunct; it is not being used to remove an unspecified new validator or to derive a numerical allocation bound. The cap rule, its evaluation cost and the preflight changes remain separate premises. Another range check would require its own premise.

For (a), `a(data) ≤ ℓ_n + 2K_n ≤ ℓ_raw + 2⌊n/2⌋`, so the explicitly stronger 𝔇_PK suffices; the note's final PK-specific qualification supplies this distinction from the common standard-cap explanation. For (b), the lifted guard plus the recharged preflight/allocation supports every-admissible-n delivery. PATH and D′ then give consistency. This is conditional mathematics about the plumbed method, not a claim that the present head can select these cap rules. No extra premise or repair is required for the stated formulation.

**(f) A2/A3 — PASS for their specification; shipped transfer remains unresolved by these patches.** A2 imports A1's specified v3.1 + LS0 method, MR1 cap and total frozen fallback. Its allocation contains the enlarged execution envelopes and Corollary R's original preflight bounds. Its own Steps 1–3 re-establish Lemma S inputs, exclude the specified exits, and supply GROW's data-event discovery and posterior inputs for D′. Adding a domain restriction in (a) and an idealisation in (b) preserves those conclusions. A3's edited verdict restates precisely the narrowed result while retaining its amendment qualifications.

A2's displayed allocation does not explicitly require A4's additional shipped LS0 preflight bounds `mem_n ≥ P_e + A` and `time_n ≥ P̄_LS0`. The patched notes accurately identify that limitation and do not claim to add the missing premises. Consequently this diff alone does not prove the shipped-method interpretation. As the brief requires, the pre-existing specification-versus-shipped question is for HQ and is not itself a defect of this diff. Nothing in these patches misstates that limitation.

**(g) Repairs — PASS.** R1 and R2 are exactly the first review's proposed one-physical-line replacements. Compared with `4b7150fe`, only those two patch lines change. R1 removes the promotion of XA:X4 to a proved conclusion, names the missing discovery argument and makes D′'s consistency implication conditional on the missing inputs. R2 excludes X7–X8 before the unchanged “only random no-output path” sentence, removing the contradiction concerning data-dependent X8. Neither introduces a new defect. Both refreshed whole-file after-hashes reproduce; neither changes a registered claim hash or span.

**(h) Tag corrections — ACCEPT.** FAC-B:L5 and S5:L5 register unchanged consistency statements, so `UNCHANGED; keep 1.0.0; delivery metadata correction only` is correct. XA:X4's stronger proposed delivery premises justify `WEAKER target only; retain PARTIAL`, with the proposed major version change and no proof-status promotion. These corrections also resolve the first brief's blanket tag proposal. No concrete batch defect remains and no same-line-count repair is needed.

Only this reply file was written. No patch was applied, no registry or other worktree was modified, and no commit was made. All reconstruction and verification used memory; no scratch files or scratch directory were created and no TMPDIR was set.

DIFF: PASS
