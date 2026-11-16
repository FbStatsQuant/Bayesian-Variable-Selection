## W3-RM2-R council R1 review (seat opus)

`manifest.py verify` returned `OK MANIFEST 4c2183ce…cd402` at the start and again at the end. Everything below was read at that manifest. Besides the frozen ticket files, I checked the parent lemmas L0/L1/L2 of W3-RM2, RM L0 and STATEMENT, GROW L1, C-DLV STATEMENT and L2, FIN s6, W2-UNI L5, the TH09 card, the W3-POST statement and the pinned core (`v3_fit.R`, `v3_preprocess.R`, `v3_run.R`, `v3_calib.R`, `v3_exact.R`, `cpp/v3_core.cpp`, `cpp/v3_start.h`).

One process note: I briefly ran `citecheck.py` to see its output. It tries to write `reviews/CITECHECK.txt`, but it failed on a relative path before creating anything. `git status` is clean and the manifest still verifies.

### 1. Per-claim table

| id | decision |
|---|---|
| W3-RM2-R:RM0-plus | ACCEPT |
| W3-RM2-R:DLV-0 | ACCEPT |
| W3-RM2-R:RM2-F-plus | ACCEPT |
| W3-RM2-R:RM2-R-plus | ACCEPT |
| W3-RM2-R:SAND-F-c | ACCEPT |
| W3-RM2-R:TL-F-c | ACCEPT |
| W3-RM2-R:Ex-Proxy-d | ACCEPT |
| W3-RM2-R:Cont-plus | ACCEPT |

All are judged conditional on SOP:TH09 (Form F), W2-APP:POST (Form R) and the C-DLV P1/S.3 audits.

**What I checked and found correct:**
- **Q1 Step 2(a).** The step (|δ| − σ|Z|)² ≥ (√(M_V log n) − σz̄_n)² is valid, with 0 ≤ e_n = O(√(log n·log log n)). The bracket is positive iff M_V > M_V⁰.
- **Q2.** The γ > 0 condition is equivalent to c_TL > c_TL⁰. Implications (a)–(c) into (BM-W⁺) hold. The bound P(𝒵⁺ᶜ) ≤ P(𝒵ᶜ) + 2/n holds.
- **Q4 (a′).** It uses NA/TL only at C, C∖{e} and S₀. All of these lie in 𝓛′ by down-closure.
- **Q4 (b⁺).** It uses only the strict F-maximality of S₀.
- **Q7.** P1's residual form is right (‖(I−P_P)e₁‖² = (1−r²)/(1+(t−1)r²)). The d_n bound is right. In (c), c = κ′/2 > c₀, M_V ∈ (M_V⁰, κ′σ²/2), c_TL ∈ (c_TL⁰, κ′/2), and 4(d+√(2L))² ≤ 9L < 16L ≤ λ_n.
- **DLV-0 against the code.** The input validators are at `v3_fit.R:88-94` and `v3_preprocess.R:99-115`. The only fixed upper bounds are `v3_run.R:96` (`le > 1e6`) and `v3_core.cpp:474` (`cap_ll > INT_MAX`); I grepped the core and found no others. The tier-1 fallback logic is at `v3_calib.R:122-125, 163-168`. The LS0-worst-case preflight is at `v3_fit.R:43-47, 65`, and is covered by A4's P̄_LS0.

### 2. Findings

**F1 (F) — REPORT/REGISTRY conditions disagree with STATEMENT.**
- `STATEMENT.md:234` says SOP:TH09@1.0.0 is a condition "for (C1⁺) and Ex-Proxy-d", carried into the statuses. REPORT's own flag (`REPORT.md:10`) says the same.
- But the Ex-Proxy-d status (`REPORT.md:34`) and its registry block (`REPORT.md:119-121`) omit the condition.
- Conversely, REPORT gives TL-F-c the Q3 row and "§6 conditional on SOP:TH09@1.0.0", plus `depends_on SOP:TH09@hyp` (`REPORT.md:33, 111-112`). STATEMENT defines TL-F-c as the truth-removal bridge only (`STATEMENT.md:28, 189, 223`) and does not list TH09 for it.
- **Fix:** make the conditions agree. Either add "conditional on SOP:TH09@1.0.0" to Ex-Proxy-d's status and `depends_on`, or (since Q7 Remark 2 shows Q7 uses no TH09 conclusion) amend `STATEMENT.md:234` through a changelog row. Point TL-F-c at the Q2 row (`STATEMENT.md:189`) and Q2 §4 only, drop SOP:TH09 from it, and record POST/MODE-F (Q2 §6) under RM2-F-plus, which already carries TH09.

**F2 (F) — READER_DELTA bridge R7.2 is not implied as written (`READER_DELTA.md:61`).**
- It takes D := (2 + 4A + o(1)), which is not a fixed constant. It also uses a non-strict condition C_β²φ₀² ≥ max{c_TL, 8(1+√(D/2))²}.
- `STATEMENT.md:111-112` needs a fixed D and λ_n ≥ max{c_TL, 8(1+√(D/2))²}·log n. But (A1) only gives λ_n ≥ (1 − 1/n)C_β²φ₀² log n, so at equality (BM-W⁺)(i) can fail when d_n² ≈ D log n.
- The file itself flags R7.2 as needing a look (`READER_DELTA.md:66-68`), but the row is in the bridge table.
- **Fix:** "for a fixed D > 2 + 4A (so d_n² ≤ D log n for n ≥ n₀ under (A5)(a)), C_β²φ₀² > max{c_TL⁰, 8(1 + √(D/2))²}". Then choose c_TL strictly between c_TL⁰ and C_β²φ₀²(1 − 1/n₀).

**E1 — inverted wording.** `STATEMENT.md:80-81`: "two upper-bound predicates, which are treated as true: (i) `le > 1e6` …". Read literally, the rejection predicate always fires. Q5 (E5) reads it as intended. Fix: "the two bounds are treated as satisfied (the rejection predicates never fire)".

**E2 — stale status.** `lemmas/Q5_dlv0.md:3` still says "(re-check pending)", but `REPORT.md:29` records RC1 VERIFIED. Update the status line.

**E3 — incomplete `depends_on`.** The DLV-0 REGISTRY `depends_on` (`REPORT.md:95`) omits several inputs that STATEMENT (C-D) (`STATEMENT.md:154-157`) cites or the status names:
- C-DLV:Prop-F@1.0.0 (delivery half);
- the FIN s6 A1/A4 allocation that 𝒜_n is taken from;
- the AUDITED inputs C-DLV:P1-Inventory and C-DLV:L2-S3.

Add them, or state the convention that excludes them.

**E4 — Lemma E4 hypotheses not named for DLV-0.** (C-D) and Q5 (E6) rely on Lemma E4 ((H1⁺), (H2), (H4)) to exclude the "no tight path" throw at `v3_start.h:261`. They reach it only through §1's code pin, while (C0⁺) names "the hypotheses of Lemma E4" explicitly. Add that phrase to (C-D) and to Q5 §1.

**E5 — interval identity not written out.** The identity St_n(𝓛′) = {S₀ ⊆ S̃₀} ∩ {[S₀, S̃₀] ⊆ 𝓛′} (`STATEMENT.md:66-67`) is true by down-closure, but Q4 (a′) does not prove it. Add the one line.

**E6 — pointers.**
- `REPORT.md:32-33` point both SAND-F-c and TL-F-c at the whole bridge table (lines 183-194). Use the row lines 188 and 189, and use relative paths like the other rows.
- The registry sharpness evidence (`Q1:128`, `Q2:103`) points into proofs. Better targets are Q1 Remark 0 (`:159-162`) and Q2 Remark (4) (`:113-114`).

**E7 — missing "s₀ ≤ K" in (c⁺).** (c⁺) (`STATEMENT.md:135-142`) does not restate "for n with s₀ ≤ K", although 𝓜_n is defined only for such n. It is inherited from (b⁺); say so.

**E8 — TARGET wording.**
- `TARGET.md:10` says "order √(log n/n) necessary by numerics/heuristic". Write "believed necessary (heuristic/numerics; not proved)".
- `TARGET.md:3` still cites STATEMENT v0.1; the locked version is v1.0.

**E9 — naming mismatch.** (C1⁺) says the block-relative variant uses (FL_b), but Q6 §1 says (G3a). They are the same condition (PARENT `STATEMENT.md:169`). Use one name.

### 3. Sweep duties

**(1) Statement copies against the lemmas.**
- (C0⁺) (a), (a′), (b⁺) and (c⁺) match Q4 word for word in substance. The one gap is the interval identity (E5).
- (C-D) matches Q5 §1.
- (C1⁺) and (C2⁺) match Q6 §§1–2. The only difference is the (FL_b)/(G3a) name (E9).
- The Q1 row matches Lemma SAND-F-c: (Q) includes |Q| ≤ K and (L-feas). The diff against the parent confirms that only Step 2(a) changed mathematically.
- The Q2 row matches Lemma TL-F-c.
- (C5⁺) (a)–(c) match Q7 §§1–3.
- (C4⁺) (i)–(v) match Q6 §3.

**(2) Quantifiers and uniformity.**
- (b⁺) is a common good data event, uniform over seed, N_e, R′ and calibration outcome, because LS0 reads no uniforms.
- DLV-0 holds for every valid input, every seed and every uniform realisation. The measured-time preflights (`v3_fit.R:34, 47`) are bounded under MACH by FIN s6's P̄_t and P̄_LS0.
- (c⁺) needs a.s. validity of the input. This is verified for Setting F (a constant y is a null event) and Setting R (columns are non-constant a.s., and Cε is nondegenerate on 1^⊥).
- The n₀ dependences are explicit: Q1 on (A, σ², M, M_V); Q2 on (A, M, σ², φ₀, c_TL) and the q log n/n sequence; Q7 (c) through a fixed κ′.

**(3) Each lemma's scope against its downstream uses.**
- Q4 (c⁺) uses Q5. Both the valid non-degenerate input and 𝒜_n are part of (D), so the scopes match.
- Q6 uses:
  - Q1 through B1, with (S0) supplied by (T1-F♭);
  - Q2 §4, which needs (F0) including q log n/n → 0 (from b < ½), and P(𝒵_n) → 1 (from NA-W);
  - Q2 §6;
  - Q4 with 𝓛′ = 𝓛, using Sand_n(Q) ⊆ St_n(𝓛);
  - Q7, only for Cont-plus (v).
- All of these are in scope.

**(4) REPORT and REGISTRY against STATEMENT.**
- Statement and premise line pointers are correct: 52-115, 71-93, 95-99, 101-105, 107-112, 118-143, 144-163, 166-176, 177-182 and 197-205.
- Cont-plus lists its targets under `implies`, not `depends_on`.
- The conditions are mismatched for Ex-Proxy-d and TL-F-c (F1). DLV-0's `depends_on` is incomplete (E3).

**(5) DEPS.tsv.** I recomputed the sha256 prefix for all 20 rows: 8 STATEMENT line ranges, 6 parent files and 6 lemmas. Every one equals both `sha` and `checked_sha`, so every row is OK.

**(6) READER_DELTA bridges.**
- R7.1 holds: c = C_β²φ₀² > c₀.
- R7.3 holds: with c > max{16, c_TL⁰}, take c_TL := c, which is exactly (BM-Q♭).
- R7.4 holds: U ∌ j, |U| ≤ 15, large n.
- R7.2 is not proved as stated (F2).

### 4. The six gates
- **correct:** PASS. Every claim's proof checks, relative to the stated conditions and audits.
- **strength:** FAIL. READER_DELTA R7.2 claims an implication that STATEMENT §2 does not give as written (F2).
- **faithfulness:** FAIL. The REPORT/REGISTRY conditions disagree with `STATEMENT.md:234` (F1), and R7.2 disagrees with `STATEMENT.md:111-112` (F2). The code re-reading itself is faithful.
- **lit:** PASS. The parity rows are fair and record where we are short (rich removal directions).
- **necessity:** PASS. TARGET and the numerics disclaim necessity; the only issue is wording (E8).
- **better:** PASS. Within T4/T2 (T4 is Form F only by the brief), the sharp-audit proposals are dispositioned in TARGET §4.

### 5. Verdict

The mathematics of all eight claims holds. I give `gates=FAIL` under the binding rule only because I hold two minor F findings, both in derived texts (REPORT/REGISTRY conditions and READER bridge R7.2); each needs a one-line fix.

COUNCIL-VERDICT round=R1 manifest=4c2183ce4a87dfa35cdf95977a06a85915d0c96b65b43f327de69102558cd402 seat=opus score=8.7 gates=FAIL
