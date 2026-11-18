# BLIND_TRIAGE — the pre-Lean blind API batch: two findings on `W3-RM2-R:DLV-0`

For HQ, via the Theory manager. Author: the pre-Lean Fable, 2026-11-18. Sources read at origin/main e5f8d140; code at the tag's core tree 61b0a582 (`cpp/` identical to pin 4676af6). I edited no file.

Batch: `Theory_work/Wave3/API_AUDIT/prelean_blind_results/` (12 requests, two blind samples per target). Every audited claim has FINDINGS=0 in both samples except **PB-T8-s1 on DLV-0, FINDINGS=2** (sample 2 found 0 on the same claim).

## 0. Verdict

Both findings are **genuine as gaps in the written proof and in DLV-0's list of cited inputs; neither is a gap in the mathematics, and neither needs a new assumption.** Each closes with a correction of a few sentences that cites results already proved and recorded. DLV-0's conclusion and premises do not change, so this is **not a NARROW**.

| Finding | Genuine? | New assumption? | Fix | Kind |
|---|---|---|---|---|
| (1) resource exits not covered by Lemma R / Corollary R | Yes, as a missing written step | No | Write the three-line amended count in (E2); complete the inputs list | Correction |
| (2) Lemma E4 used outside DLV-0's stated hypotheses | Yes, as a citation gap; already on record as `W3-RM2-R/ERRATA.md` E4 | No: **proved** for the production call | Cite ENC and TDP in (E6); complete the inputs list | Correction |

## 1. Finding (1): the resource-exit exclusion (`Q5_dlv0.md:59-67`, step (E2))

### (a) Genuine or not

**Genuine, local.** Evidence at main:
- (E2) says no preflight, guard or `resource_limit` exit fires because "this is Corollary R with the envelopes and preflight bounds of FIN `s6_delivery.tex:33-44`" (`Q5_dlv0.md:62-63`).
- The registered `C-DLV:L1-R` and `C-DLV:Cor-R` are for the envelopes W̄, M̄, in which LS0 has cap ℓ: one local search is charged "(ℓ + 1)(p + p²/4) + 1" requests (`C-DLV/lemmas/L1_resources.md:43, 47-51`). The pinned code runs LS0 with cap ℓ_n + |S̃₀| (`cpp/v3_core.cpp:473-476`). So Corollary R as registered does not cover it; the auditor is right about that.
- The proof does have the right envelopes: its sources name FIN `s6_delivery.tex:29-46` and take the allocation 𝒜_n from A1's W_G, M_G and A4's additions (`Q5_dlv0.md:24-27`), and (D) defines 𝒜_n as the envelopes "re-derived for the shipped code" (`STATEMENT.md:76-79`). What is missing is the step that says **why the pinned fit stays within W_G and M_G**. That step exists, in HQ audit A1 (finding 1), but (E2) does not write it, and the registry note on DLV-0 says the allocation comes from FIN and is "not a registry claim".
- DLV-0's statement says its inputs are "cited (and only these)" and lists Lemma R and Corollary R but not FIN's A1/A4 envelopes (`STATEMENT.md:149-155`). It also says "the proof re-audits … the resource bounds against the code as pinned" (`:160-161`), which (E2) does not do in writing.

Sample 2 found nothing here, which fits: with FIN's allocation read as given, the exit walk is sound.

### (b) Overlap with T6-1 / b″-1, and what exactly Lemma R / Corollary R do not cover

**No overlap in content.** T6-1 and b″-1 concern the list helper of the tagged method, which runs after the last guard; HQ's option (C) scopes that. Finding (1) concerns the pinned core fit itself, before the last guard.

What the registered Lemma R / Corollary R do not cover, exactly three things, all inside the pinned core:
1. **LS0's work under the shipped cap:** up to ℓ_n + K + 1 scans instead of ℓ + 1, that is at most K·q(p) more score requests, q(p) = p + p²/4, and K more archived scan models.
2. **The LS0 terms of the shipped preflight:** the time charge 2(ℓ_n + K + 1)·q(p)·ŝ_K and the `ls0_archive` bytes.
3. **The guard consultation added for LS0** (`cpp/v3_core.cpp:480`).

Items 1 and 3 are covered by A1's envelopes W_G, M_G; item 2 by A4's two inequalities (P̄_LS0 and P_e + A). The tie-aware start-mode routine, the only other count that changed since Lemma R was written, is within Lemma R's own charge by `W3-AUDIT-A:TDP` (TDP-d).

**One boundary to keep in the A re-pin, because of (C).** At the tag, `v3_fit` returns only after the list helper. If the re-pinned DLV-0 says "`v3_fit` returns", it would again claim the helper's allocation, which (C) leaves unclaimed. The re-pinned conclusion should be about the pinned computation: the fit reaches `finish` with `estimates_available = TRUE` (`v3_fit.R:173`; `:131` on the exact branch). I flag this for HQ; I do not have the text of the (C) ruling, so I propose no wording for it.

### (d) Minimal fix (correction; no new assumption)

**F1-a. `W3-RM2-R/lemmas/Q5_dlv0.md`, (E2).** Insert before "These are deterministic bounds for every valid input, seed and uniform realisation (Lemma R's form).":

> *The amended counts.* Lemma R's bound is a sum of (count) × (cost per item) (DLV `lemmas/L1_resources.md:82-83`). At the pin one count differs from the code Lemma R was written for: LS0 runs with move cap ℓ_n + |S̃₀| ≤ ℓ_n + K (`cpp/v3_core.cpp:473-476`), so it makes at most ℓ_n + K + 1 scans of at most q(p) = p + p²/4 models each, at most K·q(p) score requests more than the (ℓ + 1)(p + p²/4) + 1 that Σ̄ charges for one search (`L1_resources.md:43, 47-51`). Each request costs at most C[n³ + p(n + 2)] operations (`:32-39`), and the K extra scan models add at most K(K + 1) words to the search archive (`:90-91`). Hence, for every valid input, seed and uniform realisation, the pinned fit performs at most W_G := W̄ + C·K·q(p)[n³ + p(n + 2)] operations and holds at most M_G := M̄ + C·K(K + 1) words: A1's envelopes (FIN `s6_delivery.tex:33-36`; `Theory_work/Wave1C/HQ_AUDIT/A1_propF_redteam.md`, finding 1). The coded tie-aware start mode stays within Lemma R's charge for it (`W3-AUDIT-A:TDP` (TDP-d)). Corollary R's argument (`L1_resources.md:129-137`) then applies with (W_G, M_G) in place of (W̄, M̄), the guard site added for LS0 (`cpp/v3_core.cpp:480`) being one more consultation bounded by τW_G + τ₀.

**F1-b. `W3-RM2-R/STATEMENT.md:152-153`, the inputs list of (C-D).** Old: "Lemma R and Corollary R ("for every valid input, every seed and every realisation", `lemmas/L1_resources.md:70-81, 129-143`);"
New: "Lemma R and Corollary R ("for every valid input, every seed and every realisation", `lemmas/L1_resources.md:70-81, 129-143`), with the LS0 count re-derived for the shipped cap in `lemmas/Q5_dlv0.md` (E2), which gives the envelopes W_G, M_G and the preflight additions of FIN `s6_delivery.tex:33-44` (HQ audits A1, A4, as consumed by `W2-UNI:F-UNI`);"

**Kind and consumers.** Correction. F1-b is wording inside DLV-0's span (`:144-162`), so DLV-0 takes a patch bump; no premise and no conclusion changes. Consumers (RM0-plus (c⁺), the delivery clauses of RM2-F-plus and RM2-R-plus, LIST-R (iii), rows 3.1, 3.2, 3.1L) are unaffected in content and get a CITATION-ONLY cascade. Registry: `W2-UNI:F-UNI@proof` and `C-DLV:Prop-F@proof` are already in DLV-0's depends_on; add `W3-AUDIT-A:TDP@stmt:TDP-d`.

**What I did and did not verify.** I checked the arithmetic of the amended count against Lemma R's rows and read the cap lines at the tag. The K(K + 1) archive term is A1's; I did not read the archive struct (`cpp/v3_engine.h:46-52`).

## 2. Finding (2): Lemma E4 in step (E6) (`Q5_dlv0.md:100-103`)

### (a) Genuine or not

**Genuine as a citation gap; already recorded.** Evidence at main:
- (E6) excludes the throw "no tight path" (`cpp/v3_start.h:261`) "by Lemma E4 … `start_mode` returns a maximiser of γ₀ — in particular it returns" (`Q5_dlv0.md:101-102`).
- Lemma E4 assumes (H1) strengthened, (H2) and (H4), and claims only that the returned set is a maximiser (`W3-RM/STATEMENT.md:219-226`). (E6) checks none of the three and reads "does not throw" into a statement about the returned value.
- DLV-0's premise list does not name E4's hypotheses (`STATEMENT.md:144-145`), and its "cited (and only these)" list omits Lemma E4 (`:149-155`), although the proof's own sources list has it (`Q5_dlv0.md:28-29`).
- This is erratum E4 of the ticket, from the R1 Opus seat: "DLV-0 uses Lemma E4 (to exclude the tie-DP throw) but does not name 'the hypotheses of Lemma E4'" (`W3-RM2-R/ERRATA.md`, row E4). Its planned fix was to add the hypotheses. The owner's rule asks for more, and more is available.

### (c) The owner's rule: E4's hypotheses are PROVED for the production call

No new assumption is needed. Each hypothesis is discharged from recorded, PROVED-CHECKED text, for every run that reaches LS0 (so there is no circularity with completion):

| E4 hypothesis | Proved by | Where |
|---|---|---|
| **(H1) strengthened** (the `Start` object encodes the ordered blocks, tables, prior and K; `st.blk`, `st.pos` inverse maps; valid `D.p`) | `W3-AUDIT-A:ENC@1.0.3` (ENC-a), and (ENC-c): "The hypotheses N3 (H1) strengthened of `W3-RM:E4` hold on every run that reaches LS0" | `W3-AUDIT/track_A/T4_ENC/STATEMENT.md:29-43` |
| **(H2)** (exact arithmetic in the routine) | EX-A, a premise of DLV-0 | `Q5_dlv0.md:33-36` |
| **(H4)** (execution: representable cap, integer ranges, block width ≤ 31, allocations, recursion of depth J) | DLV-0's premises (D): the cap is the literal 10⁶ (`cpp/v3_core.cpp:469`); IDEAL-W excludes integer overflow; blocks have at most 16 columns (ENC-a); allocations and the recursion succeed by MACH with 𝒜_n, since Lemma R counts the tie-enumeration store and the DP tables and puts the recursion under MACH's stack clause | `C-DLV/STATEMENT.md:24-31`; `L1_resources.md:93-97` |
| **The throw itself** (not part of E4's conclusion) | `W3-AUDIT-A:TDP@1.0.3` (TDP-e): the root check passes, "so the `runtime_error` at `cpp/v3_start.h:261` never fires when execution reaches it"; this is row X9 of the re-audited inventory (`W3-AUDIT-A:P1S3`) | `T9_TDP/STATEMENT.md`, (TDP-e); `T10_P1S3/STATEMENT.md:26, 32` |

ENC's own setting asks for executions with no integer overflow and successful allocations; under DLV-0 those are IDEAL-W and MACH with 𝒜_n, the same premises as for (H4).

The second option the brief names is also true: RM0-plus already carries "the hypotheses of Lemma E4" as premises (`W3-RM2-R/STATEMENT.md:119`), and W3-RM counts them among the execution premises of an admissible run (`W3-RM/STATEMENT.md:64-66`). I recommend the proof route anyway, because it adds nothing to DLV-0's premises.

I verified the two throw sites and the call at the tag: `cpp/v3_start.h:261, 272`; `cpp/v3_core.cpp:469`.

### (d) Minimal fix (correction; no new assumption)

**F2-a. `W3-RM2-R/lemmas/Q5_dlv0.md`, (E6).** Old: "The tie-DP throw "no tight path" (`cpp/v3_start.h:261`, C-ENG 9b9d234): by Lemma E4, on every accepted input (cap ≥ 2 when `tie_dp` is true) and under EX-A for the routine's arithmetic, `start_mode` returns a maximiser of γ₀ — in particular it returns, so no throw occurs."
New: "The tie-DP throw "no tight path" (`cpp/v3_start.h:261`, C-ENG 9b9d234) cannot fire: by `W3-AUDIT-A:TDP` (TDP-e) the root check passes whenever execution reaches it, under EX-A and for the `Start` object of `W3-AUDIT-A:ENC` (row X9 of the re-audited inventory `W3-AUDIT-A:P1S3`). The hypotheses of Lemma E4 hold for the production call, with no premise added: (H1) strengthened is `W3-AUDIT-A:ENC` (ENC-a), (ENC-c), on every run that reaches LS0; (H2) is EX-A; (H4) holds under (D), since the cap is the literal 10⁶ (`cpp/v3_core.cpp:469`), IDEAL-W excludes integer overflow, every block has at most 16 columns (ENC-a), and the routine's allocations and its recursion of depth J succeed by MACH with 𝒜_n (Lemma R counts the tie-enumeration store and the DP tables, DLV `lemmas/L1_resources.md:93-97`). So `start_mode` returns, and by Lemma E4 the returned set maximises γ₀."

**F2-b. `W3-RM2-R/STATEMENT.md:154-155`, the inputs list of (C-D).** After "("Under the premises of Theorem D, P(𝒰_n) = 0 for every n ≥ 3")" insert: "; and, for the start-mode routine (E6), Lemma E4 (`W3-RM:E4`) with its hypotheses discharged by `W3-AUDIT-A:ENC` and the premises (D), and `W3-AUDIT-A:TDP` (TDP-e)".

**F2-c. `W3-RM2-R/ERRATA.md`, row E4.** Mark it resolved by F2-a and F2-b, with the note "discharged for the production call, not added as a premise".

**F2-d (optional, wording).** The auditor's MINOR remark: (C1⁺) says "premises and configuration of §1" where (C0⁺) adds "and the hypotheses of Lemma E4" (`STATEMENT.md:166-167` against `:119`). Since W3-RM already counts E4's hypotheses among the execution premises of §1, nothing is missing; adding the same five words to (C1⁺) would only align the two. Both samples gave RM2-F-plus FINDINGS=0. I would apply it only because the A batch opens this file anyway.

**Kind and consumers.** Correction. F2-b is wording inside DLV-0's span; same patch bump as F1-b. Registry: keep `W3-RM:E4@stmt`; add `W3-AUDIT-A:ENC@stmt:ENC-a,ENC-c ; W3-AUDIT-A:TDP@stmt:TDP-e`. Consumers as in §1 (d): unaffected in content, CITATION-ONLY cascade. F2-d, if applied, touches RM2-F-plus's span in wording only.

## 3. Placement

Both corrections belong in the A re-pin batch, which re-reads DLV-0 at 61b0a582: `cpp/` is identical to the pin, so every line cited above is the same there (I checked `v3_core.cpp:469, 473-476` and `v3_start.h:261, 272` at that tree). `W3-AUDIT-A:ENC`, `:TDP` and `:P1S3` are recorded at pin 4676af6, the same core for these files.

## 4. The FINDINGS=0 results

**No action needed.** I read all eleven; ten state no caveat. The eleventh, PB-T9-s1, states one MINOR slip it calls harmless: `W3-READER/lemmas/R4_printed_outputs.md:36` uses e^{C_R√log n} ≥ √log n, which needs C_R > 0, while the cited clause only says C_R < ∞. It is harmless as the auditor says, and in fact C_R = C_B + 1 in START-R's proof (`W3-START2-R/lemmas/R3_RATE.md`, as the Theorem 5 walk records), so C_R ≥ 1.
