# K-AE (line check of A_occam.md and E_visibility.md, gpt-6.1-sol high) — disposition

Verdicts: A VERIFIED-WITH-AMENDMENTS, E VERIFIED-WITH-AMENDMENTS; 0 FATAL / 1 MAJOR / 4 MINOR / 1 NIT. All applied.

| # | finding | action |
|---|---|---|
| 1 MAJOR | (C5′)(a) left sum uncapped | Upper limit min(m♯_n, p − s₀) written explicitly, j₁ integer ≥ 0 (A_occam (C5′)(a)). All uses (C8′), E2 already had this range. |
| 2 MINOR | gap remark bound false for d_J = 0 | Replaced by 1 ≤ a_J ≤ (2eC_A log n)^{|J|/2} (Lemma A0(iii)). |
| 3 MINOR | strictness remark infers DG from an upper bound | Reworded as a compatibility observation; no example claimed. |
| 4 MINOR | A1's beta-min qualifications | Statement: "each with its beta-min qualification unchanged"; assembly "(i), under (BM)". |
| 5 MINOR | E3 necessity claims | "(ID) order-necessary" removed (no converse proved; N1 κ = 1 an illustration); (OS) described as having a necessary *unweighted capped* counterpart (A2). |
| 6 NIT | numerical summaries | Exact finite ranges quoted (N4: 0.58–1.18; N1 κ = 1 margins 0.38 → 0.22, δ 0.56–0.69), labelled finite-sample observations. |

Reviewer's positive checks recorded (K_AE_check_sol.md "Detailed checks"): (F_w) enters only via B1; Lemma M and a_J bound;
range covers unions; A2 verified; E1 every inequality verified (c₁ = 160.7706 at s₀ = A = 1; onset depends on c's slack);
no floor away from S₀ in E2; (F_λ) ∧ BM ⇒ (ID) verified.
