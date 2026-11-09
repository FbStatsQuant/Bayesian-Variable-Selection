# R05 — Exhaustive sweep, W2-UNI

Reviewer: Codex GPT-6.1 Sol, xhigh. Reviewed locked STATEMENT v1.1.1, every UNI lemma and numerical script/output, CITECHECK and its script, R01–R04 and dispositions, the cited proof chain, and the three protocols. Also checked REPORT.md, which is now present and is cited by STATEMENT §2. This is an asymptotic review of the fixed method, conditional on its named implementation premises.

No counterexample to the concrete UNI-0 or UNI-1 theorem under its complete assumptions was found. The metric toolkit, general-Ψ orthogonal decomposition, localisation, entropy bound, sample coupling, and concrete assembly arguments survive this sweep. The principal substantive overclaim is the asserted containment of the entire fixed-design FAC-L theorem. The accepted mathematical amendments from R01–R04 are present; item 4 below concerns an overclaim reintroduced in the report.

Independent in-memory Python 3.13/NumPy check: a non-block covariance on eight indices with zero distances and small positive distances, heterogeneous signed loadings, all 1,024 `(T,l)` pairs including empty T, four Gaussian draws, and three localisation radii. Across 4,096 pairs, maximum decomposition error was 1.33e-15, maximum LOCL variance-identity error was 1.34e-16, and there were zero violations of the deterministic U-LOC bound. These are algebraic falsification checks, not substitutes for asymptotic proofs. An additional high-precision check of the first n2 iterated CT rate agreed to approximately 1.5e-9 relative error; I do not flag the very small positive CT constants as a defect. Only this review file was written; no git commands were used.

1. **MAJOR — Full FAC-L containment drops FAC-L's weaker signal regime.**

   **Locations:** `STATEMENT.md:121–123`, `:178`; `lemmas/L4_k1.md:64–67`; `lemmas/C_corollaries.md:25`; `REPORT.md:40`.

   UNI-1 requires the fixed positive coefficient floor θ_lo. FAC-A's fixed-design Theorem L4.1 instead assumes H0/BM-∞ and TV, which permit vanishing signals (`W2-FAC-A/STATEMENT.md:86–95`, `:115–118`; `lemmas/L3_NA_TL.md:7–9`). Thus structural containment and preservation of κ do not establish containment of that entire theorem. For example, take exact-Gram CS with ρ=1/2, p_n=floor(n^(1/10)), one truth, and θ*_n=n^(-1/4). Its energy is bounded by Mn, BM-∞ holds because nθ*_n²/log n→∞, and every required truth increment has δ²≥(n−1)θ*_n²/2, so TV holds with a diverging envelope. It meets FAC-L's fixed-design assumptions and exponent, but violates UNI-1's fixed θ_lo. No change to UNI-1 is needed to repair this overclaim.

   **Exact fix:** everywhere above say: “UNI-1 contains the fixed-positive-beta-min subclass of FAC-L, with the same structural representation, κ, exponent, and TV/TV-pop qualifications. FAC-L's fixed-design BM-∞ relaxation remains a separate imported result.” Retain the unqualified structural-class containment statement only when clearly distinguished from theorem containment.

2. **MINOR — The principal PLR summary does not state its inherited row and signal hypotheses.**

   **Location:** `STATEMENT.md:91–97`.

   The summary lists relevance-set conditions, sandwich, NA-R's R1–R3, and the additional LSF clause, but does not explicitly say that this is the random-row setting with fixed sparsity and fixed positive beta-min. These are used by the imported theorem: LOC2 `lemmas/L5_assembly.md:13` invokes its setting and fixed θ_lo, and LOC2 `lemmas/L1_toolkit.md:33–36` expressly limits its TL consequence to that signal regime. R1–R3 alone do not replace those hypotheses. The enclosing setting also introduces an E branch, whereas NA-R's proof is a random-row proof. A principal abstract theorem should not require readers to reconstruct this scope from the cited ticket.

   **Exact fix:** begin (i′): “Under setting (R), fixed s₀, the coefficient bounds of (A3) without PTV, and the method premises of §1, let Σ_n be any population correlation sequence …”. Retain the present C-i/C-ii split. Do not present this PLR statement as an E-design theorem.

3. **MINOR — The report incorrectly removes the upper spectral condition from UNI-0.**

   **Location:** `REPORT.md:91–93`.

   “For k=0 … no condition on λ_max” contradicts LOC_M, whose spectrum must lie in a fixed [c,C] (`STATEMENT.md:48–49`). UNI-0 uses C through conditional decay and its derived constants; `lemmas/L2_k0.md:182–187` explicitly audits that dependence. It is UNI-P, and the full Σ in UNI-1, that permit an unbounded upper eigenvalue without this restriction.

   **Exact fix:** replace the sentence with: “For k=0 the LOC_M spectral bounds and decay, polynomial dimension, and PTV suffice; no prescribed ordering or relation to the method's partition is required. The bound λ_max(Σ_n)≤C is part of LOC_M.”

4. **MINOR — The report reintroduces an unsupported exclusivity claim beyond α₀.**

   **Location:** `REPORT.md:98–99`.

   “Beyond α₀ only the path route works” is not established. SHARP rules out full-lattice NA for exact CS when liminf log p/log n>1/6; it does not prove necessity of α₀(κ̄) for general local Ψ or rule out every other proof. R03 item 6 required precisely this distinction, and the corrected wording is present in `lemmas/L4_k1.md:69–71` and `lemmas/L6_frontier.md:28–30`.

   **Exact fix:** replace it with: “For exact CS above 1/6, SHARP rules out full-lattice NA, while FAC-B supplies a path proof. Necessity of α₀(κ̄) for other representations, and exclusivity of a path approach, have not been established.”

5. **MINOR — The locked statement's LS0 move-count conclusion omits its event and execution convention.**

   **Location:** `STATEMENT.md:118–120`; compare `lemmas/L4_k1.md:50–52`.

   The sentence “LS0 reaches S₀ after exactly … deletions” is unqualified, whereas the proof establishes this on Sand∩NA∩TL for the prescribed deterministic search. A production run may enumerate instead, or fail to deliver before executing LS0. The cited FAC-A statement explicitly distinguishes the uninterrupted deterministic search from actual execution (`W2-FAC-A/STATEMENT.md:119–122`). This qualification remains necessary for asymptotic statements about a random algorithmic path.

   **Exact fix:** say: “On Sand_n∩NA(𝓛)∩TL(𝓛), the prescribed deterministic LS0, viewed as uninterrupted on these data, reaches S₀ after exactly |S̃₀\S₀| deletion moves. A delivered SMC run executes that search; enumeration scores S₀ directly.” The event has probability tending to one.

6. **MINOR — A nearly full start is asserted for general UNI-1 without a theorem or adequate qualification.**

   **Locations:** `REPORT.md:4–5`, `:35–37`.

   The flag “start mode ≈ [p]” is attached to UNI-1 generally. UNI-1 proves only that every start maximiser contains S₀; it does not prove a nearly full start. A2-1 expressly permits a vanishing common loading scale, so pervasive null visibility cannot be presumed throughout this class. Even the report's theorem synopsis says only “start mode ⊆ [p]”, which is tautological. A cap needed uniformly over a class does not mean every member needs order-p moves.

   **Exact fix:** replace the flag with: “The merged cap suffices uniformly; admitted factor subclasses can require order-p deletion paths.” In the synopsis say “every start maximiser contains S₀, and on Sand∩NA∩TL LS0 removes its extras by pure deletions.” Cite FAC-B's full-start theorem under FS if a specific order-p example is desired; do not assert a full-start theorem for general UNI-1.

7. **MINOR — The S5 signal scale collides with the spectral-floor notation.**

   **Location:** `lemmas/C_corollaries.md:26`.

   This file declares STATEMENT §2 notation, where c is the lower spectral bound. The displayed S5 certificates τ₀=c²·7/2080 and c²·2023/32500 instead use FAC-A's c for the multiplier of the study coefficient pattern. That multiplier is not defined here. The R04 layout labels are now present, but they do not resolve this remaining collision. For arbitrary signal scale, substituting the spectral c gives no certified visibility lower bound.

   **Exact fix:** introduce c_sig>0 with θ*=c_sig times the specified unit-scale coefficient pattern, and write τ₀=c_sig²·7/2080 for the 14-truth layouts and c_sig²·2023/32500 for the diagnostic layout. State that c retains its spectral meaning.

8. **MINOR — The diagonal-Ψ κ formula is wrong for negative loadings of one sign.**

   **Location:** `lemmas/C_corollaries.md:33–35`.

   “Of one sign” allows all-negative λ, but κ′ is displayed as max λ_j/sqrt(1−λ_j²), and the final max/min formula also omits absolute values. κ′ cannot be negative. For λ=(-0.4,-0.7), Ψ=diag(1−λ_j²), the stated signed max/min ratio is approximately 0.4453, whereas the defined κ is approximately 2.2459. These constants determine the exponent.

   **Exact fix:** define q_j=|λ_j|/sqrt(1−λ_j²), and write κ′=max_j q_j, c_𝒢=min_j q_j², κ=max_j q_j/min_j q_j. Alternatively restrict the sentence explicitly to 0<λ_lo≤λ_j≤λ_hi<1; the absolute-value form covers both signs without an unnecessary restriction.

9. **MINOR — The absorption rule reverses the implication needed for a corollary.**

   **Location:** `lemmas/L6_frontier.md:39–40`.

   To call a parallel theorem a corollary of a general theorem, the parallel theorem's hypotheses must imply the general theorem's hypotheses. The text instead says its hypotheses must be implied by A1–A3 plus an extra condition. That direction can show that an external theorem proves a newly proposed restricted general result, but does not show that the external theorem is a corollary of UNI. This distinction matters because several rows explicitly target regimes outside UNI-1.

   **Exact fix:** replace the rule by: “A source result is a corollary of an existing UNI theorem only after its hypotheses are shown to imply all hypotheses of that UNI theorem. To use a parallel result to prove an extension under A1–A3 plus a named population condition, show that those proposed hypotheses imply the parallel result's hypotheses; state and review the extension separately.”

10. **MINOR — CITECHECK does not perform the comprehensive content/status check its description promises.**

    **Locations:** `citecheck.py:1–5`, `:17`, `:25–61`, `:63–103`; `reviews/CITECHECK.txt:1–2`, `:90–108`, `:135–139`.

    The general citation loop tests only whether some candidate file has enough lines. It marks multiple resolutions OK, even when the first selected file is wrong; for example L2:161 resolves first to APP's STATEMENT rather than UNI's. The twelve hand-selected token tests are not attached to every cited claim or quotation, and the twelve substring status tests do not verify every quoted status in context. Shorthand citations such as `:72–75` in L2's G4 row are not extracted. Consequently “107 … 0 misses” is not evidence that all path:line claims match their text. The manually appended resolution note still accepts stale UNI statement ranges identified in item 11.

    **Exact fix:** resolve each citation to one explicit intended path, expand abbreviated ranges, require 1≤a≤b≤the actual line count, and associate each cited claim/quotation/status with a content assertion at that location. Treat unresolved ambiguity as a failed check. If comprehensive assertions are not supplied, accurately label the automated output as a file/range-existence check with a separate enumerated manual content audit. Re-run without hand-appending success resolutions that the checker cannot reproduce.

11. **MINOR — Several live references point to pre-amendment statement lines.**

    **Locations:** `lemmas/L1_metric.md:5`, `:151`; `lemmas/L2_k0.md:5–6`, `:190`, `:223`; `reviews/CITECHECK.txt:11`, `:23`, `:25–26`, `:106`, `:135–137`.

    In locked v1.1.1, R1 is at 135–143, R2 at 144–146, R3(b) at 150–153, and UNI-0 at 99–106. Thus L2's “R2 … 141–143” points to the LOCL specification, and L1's “R3(b) … 146–150” mostly points to R2/the opening of R3. The repeated 96–103 UNI-0 references begin in the PLR discussion and omit UNI-0's final conclusions. The bare :96 cited for UNI-0's unit diagonal is also no longer the theorem's location. This is substantive citation drift, despite the range checker passing.

    **Exact fix:** use `STATEMENT.md:135–143` for L1's R1 target; `:150–153` for its R3(b) use; `:99–106` for L2's UNI-0 target and final comparison; `:144–146` for its R2 target; and `:99` for the UNI-0 unit-diagonal theorem reference. Correct the manual CITECHECK note and regenerate the audit after these edits. Historical review reports may retain their original-version line numbers when that version is identified.

12. **MINOR — Generator citations miss the scenarios they purport to identify.**

    **Locations:** `lemmas/C_corollaries.md:21`, `:26`; `reviews/CITECHECK.txt:8–10`.

    The S5 row cites `gen_dev_data.R:26`, which actually contains S3's 0.7H+0.3I. S5 is at line 28. The S1/S3/S4/S6 row cites lines 18–28 for its covariance definitions, but S6 is defined at line 29. The covariance formulas themselves are correctly transcribed; their cited locations are not.

    **Exact fix:** cite `Scripts/Data_generators/gen_dev_data.R:28` for S5 and `:18–29` for the combined covariance definitions, retaining `:32–41` for the truth layout. Add claim-specific checks for S6 as well as S5.

13. **MINOR — N1's documentation promises a CT_M bound test that the script does not implement.**

    **Location:** `numerics/n1_metric.py:5–8`, `:108–121`; compare `numerics/n1_out.txt:10`, `:20`, `:30`, `:40`.

    The docstring says the script records the ratio |(A⁻¹)_ij|/[(2/α)exp(−t*δ_ij)] and checks that it is ≤1. The implementation instead fits slopes to observed inverse-entry envelopes. It never constructs the growth/decay constants or t*, and its output contains no such ratio. An empirical fitted decay slope is not a falsification check of the advertised CT_M constant. N2 does supply the missing ratio test, so this does not leave CT_M without any numerical probe.

    **Exact fix:** change N1's docstring to describe the fitted envelope slopes as exploratory observations and explicitly point to N2 for the analytic CT_M ratio check. Alternatively implement the promised ratio; do not describe the current fit as that check.

14. **MINOR — Sampled exposure ratios are presented as certified κ ranges.**

    **Locations:** `numerics/n3_uloc.py:74–78`, `:86–87`, `:100–102`; `lemmas/L4_k1.md:67–69`; `REPORT.md:98–99`.

    N3 takes a supremum and infimum over sampled/greedy sets plus singletons, not the complete domains defining κ′ and c_𝒢. Its sampled κ′ is ≤the true supremum, while its sampled c_𝒢 is ≥the true infimum; hence their reported ratio is a lower bound on the true κ, not a certified upper bound. The κ interval and corresponding exponent interval in the prose cannot be inferred for these larger designs. N3b really does enumerate the complete domains at p=10 and can support numerical κ values there. The proof uses the assumed κ̄ and is unaffected.

    **Exact fix:** label both N3's κ′ and κ output explicitly “sampled lower bound”, retain “sampled upper bound” for c_𝒢, and describe the larger-design observations accordingly. Restrict certified numerical κ/exponent ranges to N3b's exhaustive p=10 designs, distinguishing its block-diagonal design D from its non-block designs A–C. Do not infer an admissible theorem exponent from N3's sampled ratio.

15. **MINOR — The mandated numerical falsification record is incomplete for the new reduction/frontier lemmas.**

    **Locations:** `lemmas/L2_k0.md:207–209`; `lemmas/L6_frontier.md:3–13`; `STATEMENT.md:133`; `Theory_work/Wave1C/PROTOCOL.md:33–34`.

    The statement promises a numerical falsification attempt for each reduction, and the protocol requires one for every lemma before downstream use. L2 explicitly says its reduction was not probed on the newly admitted pseudometric designs, citing only toolkit checks and the separated-site source fixtures. None of the four UNI scripts probes OBS-k or its fixed-m information conclusion. The analytic reduction and pigeonhole proof remain valid; this is an unfulfilled validation/record obligation, not a statistical performance objection.

    **Exact fix:** add and save a small, local falsification check of the R2 interfaces on a zero-distance/small-positive-distance design, and a k≥2 information-matrix/pigeonhole check with fixed m, including m≥k. Record the precise checks and outputs in the relevant lemma headers. If relying on an existing external check instead, identify an output that actually covers the claimed new interface; do not substitute toolkit-only checks or claim that the present scripts test OBS-k.

16. **NIT — The reported N3 pair total is arithmetically wrong.**

    **Location:** `lemmas/L3_ULOC.md:3–4`; evidence `numerics/n3_out.txt:1–6`.

    The six recorded pair counts sum to 2·3186+4·5238=27,324, not 27,162. The identity-error and zero-violation claims otherwise match the output.

    **Exact fix:** replace “27 162” with “27 324”.

17. **NIT — OBS-k's proof divides by a loading bound that may be zero.**

    **Location:** `lemmas/L6_frontier.md:7`, `:10–12`.

    The hypotheses allow Λ_n≡0 and L=0, but the covering diameter η/L is then undefined. The theorem is immediate in that case, so this is a proof convention defect rather than an obstruction to OBS-k.

    **Exact fix:** take a strictly positive bound at the outset, for example L_*=max(1,L), and use η/L_* and L_* in the covering argument; alternatively dispose of L=0 before dividing.

18. **NIT — The report changes the midpoint finding classes.**

    **Location:** `REPORT.md:77–78`; compare `reviews/R04_midpoint_sol.md:19–33` and `reviews/R04_disposition.md:4–7`.

    R04 records one MAJOR, two MINOR, and one NIT. The report calls this one MAJOR plus three minor findings. The fixes are applied, but the stated review trail does not preserve the recorded classes.

    **Exact fix:** write “1 MAJOR, 2 MINOR, 1 NIT, applied”.

Counts: **FATAL 0; MAJOR 1; MINOR 14; NIT 3. Total 18.**
