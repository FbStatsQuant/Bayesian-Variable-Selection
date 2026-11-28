# Audit PB-T8-s1: PB-T8
claims: W3-RM2-R:RM2-F-plus, W3-RM2-R:RM0-plus, W3-RM2-R:DLV-0
stop_reason: end_turn

**Findings**

I found no error in the probabilistic and combinatorial parts: `Q1_sandF_c.md`, `Q2_TL_c.md`, `Q4_core_plus.md` (a), (a′), (b), (b⁺), (c⁺), and `Q6_assembly.md` §1. The constants M_V⁰ and c_TL⁰, the ladder, the 𝓩 / 𝒵⁺_n / ℬ_n event bookkeeping, identity (4.1), the down-closed re-reading of L1.1/L1.2, and the reader-level constants of Theorem 7 Remark (a) all check. Two steps of the delivery lemma are not justified on the page.

**1. GAP — `Q5_dlv0.md:59-67` (E2), with `Q5_dlv0.md:24-27` and `STATEMENT.md:76-79, 149-154, 160-162`. The resource-exit exclusion is not covered by the consumed Lemma R / Corollary R.**

- **What the step claims.** (E2) says no preflight, guard or `resource_limit` exit fires: "this is Corollary R with the envelopes and preflight bounds of FIN `s6_delivery.tex:33-44`".
- **Why the consumed result does not give it.** Corollary R (`L1_resources.md:129-143`) is stated for the envelopes W̄, M̄ of Lemma R. All local-search terms in those envelopes carry the old cap ℓ: `(ℓ+1)T̄²(40p+2)`, `K(ℓ+3)²`, `2(ℓ+1)·min(40p+1,10⁴)(K+3)`. The shipped search has cap ℓ_n + |S̃₀|, with up to 1 + (ℓ_n+K+1)(p + p²/4) score requests (Q5:63). That is of order K·p², far above the ℓ·p-type counts in W̄, and the stated order of W̄ is not shown to dominate the resulting operation count.
- **What is missing.** The step therefore rests entirely on FIN's amended envelopes (W_G, M_G, P̄_LS0, P_e + A), which the proof imports by reference without stating or deriving them. They are also absent from the lemma's own list of law-free inputs "cited (and only these)" (STATEMENT:149-154).
- **Contradiction with the statement's own description.** STATEMENT:160-161 says "the proof re-audits … the resource bounds against the code as pinned". (E2) contains no such re-audit. The seven C-ENG commits since 39db138 are examined only for new exits in (E5)–(E8), not for operation or word counts.
- **Repair.** State the amended Lemma R explicitly for the pinned code: an operation bound W_G and word bound M_G valid for every valid input, seed and uniform realisation, including the LS0 archive, the new guard check at `v3_core.cpp:480`, and a deterministic bound under MACH on the measured ŝ_K used in the LS0 preflight. Define 𝒜_n by those envelopes, and register this as a consumed claim or prove it. The LS0 count already given in Q5:63 is one ingredient.

**2. GAP — `Q5_dlv0.md:100-103` (E6), with `STATEMENT.md:144-145, 149-154` and `Q6_assembly.md:28`. Lemma E4 is used outside its stated hypotheses, and DLV-0 does not state them.**

- **What the step claims.** The tie-DP throw "no tight path" (`v3_start.h:261`) is excluded "by Lemma E4, on every accepted input … and under EX-A".
- **Hypotheses dropped.** E4 as stated (`W3-RM/STATEMENT.md:219-230`) also assumes (H1) strengthened (`st.blk`, `st.pos` inverse maps of the ordered actual blocks on every branch, valid `D.p`) and (H4) (execution bounds for enumeration and fallback). (E6) invokes neither, and does not verify them for the `Start` object that production `v3_setup` builds.
- **Not in DLV-0's premises.** DLV-0's hypothesis list (Q5:33-36; STATEMENT:144-145) does not include "the hypotheses of Lemma E4", whereas RM0-plus (STATEMENT:119) does. E4 is also not among the inputs "cited (and only these)".
- **Circularity risk.** E4's integration sentence gives [E4] only "on every completed SMC output run". Here it is used before completion is known, to prove completion.
- **Partial-correctness wording.** E4 claims "the returned set is a maximiser". That the routine does not throw on an accepted input is read into it; the step should cite the part of E4's proof showing that a tight path exists under EX-A.
- **Repair.** Add the E4 hypotheses (H1 strengthened, H4) to DLV-0's premises, or verify them for the production call under IDEAL-W / TDP-IMPL, and cite the tight-path existence step. With them stated in DLV-0, (c⁺) is covered, since RM0-plus already assumes them.
- **Related bookkeeping slip (MINOR).** (C1⁺) at STATEMENT:166-167 lists only "premises and configuration of §1". Q6:28 identifies E4's hypotheses with those premises without showing that (H1) and (H4) are among them. (C1⁺) should carry "and the hypotheses of Lemma E4" as (C0⁺) does.

AUDIT W3-RM2-R:RM2-F-plus FINDINGS=0
AUDIT W3-RM2-R:RM0-plus FINDINGS=0
AUDIT W3-RM2-R:DLV-0 FINDINGS=2