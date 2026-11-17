# Registry consumers of C-DLV:P1-Inventory and C-DLV:L1-R vs the B1′ trigger (A-7) — for HQ (CORRECTION vs SUSPECT)

Registry: `Theory_work/INFRA/registry/claims.tsv` at origin/main d5e9eee7 (columns depends_on, consumes, status, premises,
assumptions, implies, gates searched). B1′ = the SMC preflight's LS0 worst-case seconds / `ls0_archive` bytes
(`Scripts/SMC_BVS/core/v3_fit.R:43-47, 61-66`), live only when `ls0` is on and `v3.ls0_cap` ≠ "ell_n" (`v3_fit.R:114`),
i.e. only under the C-GROW cap ℓ_n + |S̃₀|. C-DLV's own method has LS0 cap ℓ_n (`Theory_work/Wave1C/C-DLV/STATEMENT.md:11-12`).

| consumer (of) | relies on inventory completeness for B1′? |
|---|---|
| C-DLV:Cor-R (P1, L1-R) | No: method cap ℓ_n, under which B1′ is off; its "none of B1–B3 … fires" is about C-DLV's configuration. |
| C-DLV:Thm-D (P1, L1-R) | No: same method (cap ℓ_n); its exit walk is complete for that configuration. |
| W3-RM2-R:DLV-0 (P1 depends_on+status; L1-R) | No: its (E2) names B1′ ("on the SMC branch with the C-GROW cap also the LS0 archive and LS0 time") and excludes the LS0 seconds by FIN A4's time_n ≥ P̄_LS0 and the `ls0_archive` bytes by mem_n ≥ P_e + A, e = 0, 1 (`lemmas/Q5_dlv0.md` 59-65 @ e78a1055) — confirmed by Sol CSL1 (ii) and council C-R1/C-R2 (wording per C-R1 Opus F1). |
| W3-RM2-R:RM2-R-plus, RM2-F-plus, RM0-plus, Cont-plus (P1, status only) | No own use: the condition is inherited through DLV-0 (same answer as DLV-0). |
| C-ENG:Impl-DLV-A2 (L1-R) | No: TDP-IMPL operation/storage bounds; no preflight exit involved. |
| HQ_AUDIT-W1C:A2 (L1-R) | **Yes, in its registered span**: Step 2 extends Delivery to the C-GROW cap via Thm D's walk and Cor R with W_G, M_G, without the LS0 time term (`Theory_work/Wave1C/HQ_AUDIT/A2_propF_GROW.md:51-53`); the term is covered by the later HQ audit A4 (`Theory_work/Wave1C/HQ_AUDIT/A4_postcouncil_check.md:5-19`, not a registry claim). Status "EXTENDS". |
| second-hand (via Cor-R / Thm-D): C-DLV:Prop-F, Cor-Dp, C1-CondDelivery, O | No (cap ℓ_n configuration). |
| second-hand (via Thm-D): HQ_AUDIT-W1C:A1 | **Yes, as A2**: Prop F with the C-GROW cap and preflight bounds P_0, P_1, P̄_t only (`Theory_work/Wave1C/HQ_AUDIT/A1_propF_redteam.md:62-75`); the LS0 preflight term came later (ef33f91c) and is covered by HQ audit A4 (`Theory_work/Wave1C/HQ_AUDIT/A4_postcouncil_check.md:5-19`, `:33`: "checked separately in HQ audit A4"). |
| second-hand: W2-FAC-A:Prop-F-FAC | No: its allocation is "A1+A4", i.e. includes the LS0 preflight term. |

Reading: every consumer that uses the shipped C-GROW cap either names B1′ itself (DLV-0, Prop-F-FAC) or is covered by HQ
audit A4 (A1, A2); the cap-ℓ_n consumers never meet B1′. Lead's view: CORRECTION (amendment), pending CSL1 (ii).
