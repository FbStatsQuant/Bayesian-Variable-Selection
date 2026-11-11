# R-AUD1 — review of C-DLV:Prop-F

**Verdict: CONFIRMED-WORDING.** The standalone wording at `Theory_work/Wave1C/C-DLV/lemmas/L4_delivery.md:83-84` should explicitly retain the statistical hypotheses. In context, however, “on the classes above” refers to the statistically qualified classes immediately described in Corollary D′, and “unconditionally” refers to the probability law, not to removal of those hypotheses. I do not confirm a substantive missing-proof GAP for the intended registered result. No registered consumer inspected relies on the over-strong reading.

## Statement scope and proof

1. Theorem D's setting (`L4_delivery.md:7-9`) alone does not imply statistical consistency. Removing a no-output path cannot establish either posterior concentration or LS0 discovery. If F were read as assuming only that setting, fixed truth size and polynomial dimension, its second conclusion would indeed be unsupported.
2. F does not stop at “under the premises of Theorem D”: it separately says **“on the classes above”** (`L4_delivery.md:83-84`). Immediately above, D′ identifies the two limits, their respective classes and their hypotheses (`:53-63`): GEN, including the exact-Gram LH instance, uses (H0)–(H2); LH-iid uses the W1-PXN hypotheses, explicitly naming SIZE, p_n → ∞ and (OP). F then expressly invokes that corollary (`:88-89`). This is meaningful incorporation by reference, albeit unnecessarily terse.
3. The ticket's formal claim C2 makes the restriction unambiguous: “under their hypotheses” (`Theory_work/Wave1C/C-DLV/STATEMENT.md:75-76`). The registered F row (`Theory_work/INFRA/registry/claims.tsv:125`) depends on `C-DLV:Cor-Dp`, records the scope as the classes “via Cor-Dp”, lists statistical assumptions (including beta-min, energy, sparse eigenvalues, relevance size and block visibility), and consumes `P:POST-CONC` and `P:LS0-DISCOVERY`. The registry therefore does not present a computational-premises-only consistency theorem.
4. D′ itself explains “unconditioned”: its bounds are under the original data law, without conditioning on delivery or calibration success (`L4_delivery.md:70-77`). This is compatible with requiring statistical hypotheses. The chapter's current transcription removes the ambiguity explicitly: `Theory_work/Wave1C/FINAL/sections/s6_delivery.tex:19` states the statistical restrictions for D′, and `:46` retains “the respective statistical hypotheses and inherited dependency qualifications” for F, under the “original unconditioned data law”. That supports the intended reading; it does not retroactively make the original wording self-contained.

Thus the repair is a scope clarification, not a new statistical theorem. The finite-n delivery conclusion P(𝒰_n)=0 remains separate from the asymptotic statistical conclusion.

## Exact statistical inputs and minimal restatement

The minimal inputs to the displayed consistency argument are eventual feasibility of S₀ and

    P(𝒦_nᶜ) → 0,    E[1 − π(S₀ | y)] → 0,

where 𝒦_n is the prescribed deterministic LS0 discovery event of D′. Together with F's delivery conclusion, the pathwise argument gives

    P(Ŝ⁺ ≠ S₀) ≤ 2E[1 − π(S₀ | y)] + P(𝒦_nᶜ) → 0.

For the cited sufficient conditions:

- **GEN:** retain W1-GEN (H0)–(H2), the specified method/search and eventual cap/onset conditions. (H0) supplies posterior concentration; (C1)+(C2) supply discovery. Sources: `Theory_work/Wave1/W1-GEN/STATEMENT.md:48-75,84-85,99-110`; `lemmas/L5_assembly.md:21-38`. The logarithmic cap eventually exceeds the bounded path length. The favourable and random-design variants can instead be used under their own hypotheses (`STATEMENT.md:112-120`).
- **LH exact Gram:** retain the actual instance hypotheses, including SIZE, and its inherited input qualification; these are not just the name “LH” (`W1-GEN/STATEMENT.md:123-128`; `C-DLV/lemmas/L4_delivery.md:61-63`). No upgrade of SAME-FAMILY-ONLY is warranted.
- **LH-iid:** retain the full family/score/search specification and SIZE, including p_n → ∞ (`Theory_work/Wave1/W1-PXN/STATEMENT.md:13-37`), with the operational search requirements used in D′. W1-PXN explicitly identifies (S), (E), (T), (P) as data/deterministic-search conclusions (`:52-63`); the repaired discovery theorem is `lemmas/LS_P6_repair.md:29-35`.

Do **not** repair F by importing all of (OP) unchanged: W1-PXN's (OP) lists CAL (`STATEMENT.md:45-48`), whereas D′ replaces the CAL-bearing assembly with its pathwise argument (`L4_delivery.md:65-77`). CAL is unnecessary for the data-level concentration/discovery transfer. W1-GEN's centre and descent clauses are likewise statements about the data and deterministic search, rather than successful calibration.

**Minimal replacement for F's concluding sentence:**

> Under the premises of Theorem D, P(𝒰_n)=0 for every n≥3. On the classes of Corollary D′, under the respective hypotheses of its cited posterior-concentration and deterministic-LS0-discovery results, P(Ŝ⁺=S₀)→1 under the original unconditioned data law, without conditioning on delivery or calibration success and without assuming CAL.

This preserves the original cap and allocation. It does not import the later GROW cap/resource amendments into the original proposition.

## Consumer audit

I searched `depends_on` and `consumes` in `claims.tsv` for the canonical ID, the legacy `EXT:Proposition F` reference and the exported property `P:NO-OUTPUT-ZERO`; I also searched chapter TeX sources under `Theory_work/` and inspected the relevant source statements/proofs. `rg` was unavailable, so searches used PowerShell `Select-String` and TSV parsing.

**No reliance on the over-strong reading was found.** The relevant registered consumers use delivery alone, explicitly retain statistical restrictions, or establish replacement statistical inputs:

| Consumer(s) | Evidence and use |
|---|---|
| `C-ENG:Impl-DLV-B` | Implementation of the fallback, not an assumption-free consistency deduction: `Theory_work/Wave1C/C-ENG/REPORT.md:51-55`. |
| `HQ_AUDIT-W1C:A1`, `A2`, `A4` | A1 explicitly says fixed truth size and polynomial p alone are insufficient and carries the original class hypotheses (`HQ_AUDIT/A1_propF_redteam.md:47-56,75`). A2 supplies GROW discovery and posterior inputs separately (`A2_propF_GROW.md:25,55-67`). A4 checks allocation and provenance rather than deleting statistical restrictions (`A4_postcouncil_check.md:27-39`). Paths in this row are under `Theory_work/Wave1C/`. |
| `W2-FAC-A:Thm-FAC-L`, `Prop-F-FAC` | Own class hypotheses and separate discovery/posterior proof: `Theory_work/Wave2/W2-FAC-A/lemmas/L7_delivery.md:18-24,39-49`. |
| `W2-FAC-B:Thm-FAC-CS` | C4 explicitly assumes the CS class conditions; proof supplies both limits: `Theory_work/Wave2/W2-FAC-B/STATEMENT.md:127-134`; `lemmas/L5_assembly.md:18-35,50-68`. |
| `W2-FAC-PK:Thm-FAC-PK` | Retains its class/cap hypotheses, recharges resources and expressly combines discovery with concentration: `Theory_work/Wave2/W2-FAC-PK/STATEMENT.md:73-87`. |
| `W2-FAC-S5:Thm-FAC-BCS-R`, `L5`, `L5.C4-R` | Retain a centre-condition failure term rather than asserting consistency for free: `Theory_work/Wave2/W2-FAC-S5/STATEMENT.md:121-124`; `lemmas/L5_assembly.md:39-55`. |
| `W2-FAC-S5F:C4` | Requires C3's hypotheses, including its centre condition, or the separately stated sufficient dimension regime: `Theory_work/Wave2/W2-FAC-S5F/STATEMENT.md:96-99`. |
| `W2-FAC-X:Thm-FAC-CS-iid`, `X6`, `X6.X6.4` | Retain the iid class hypotheses and use their own posterior/discovery inputs: `Theory_work/Wave2/W2-FAC-X/STATEMENT.md:76-95`; `lemmas/X6_assembly.md:58-70`. |
| `W2-FAC-X:Thm-FAC-GL`, `X10` | Retain the loading/design hypotheses; separately verify discovery and (H0) before invoking delivery: `Theory_work/Wave2/W2-FAC-X/STATEMENT_T2.md:49-62`; `lemmas/X10_assembly_T2.md:6-22`. |
| `W2-LOC2:F-LOC2` | Uses the fallback exit walk, then its own discovery/concentration inputs: `Theory_work/Wave2/W2-LOC2/lemmas/L7_delivery.md:14-35`. The registered exp/poly splits use this same qualified proof. |
| `W2-UNI:F-UNI` | Explicitly assumes discovery-enabling event (S) and posterior expectation limit (P): `Theory_work/Wave2/W2-UNI/lemmas/L5_delivery.md:15-34`. |

The chapter is especially clear: `Theory_work/Wave1C/FINAL/sections/s6_delivery.tex:46,54-56` distinguishes delivery from statistically qualified consistency, including the GROW extension. `s7_impl.tex:72` transfers the pathwise bound and retains the amended-allocation requirement. The generated registry transcription `Theory_work/INFRA/paper/generated/blocks/C-DLV_Prop-F.tex` also carries the chapter's explicit statistical qualification. Broader chapter summaries are references to these qualified results, not proofs of consistency under model G alone.

**Disposition:** clarify the original proposition's scope as above; do not propagate the automated finding as an established mathematical GAP or a demonstrated downstream failure. Only this review output was written; no git state was changed.
