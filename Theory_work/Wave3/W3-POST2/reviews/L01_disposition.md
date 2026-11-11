# L01 (statement lock, gpt-6.1-sol high) — disposition

Verdict LOCK-WITH-AMENDMENTS; 0 FATAL / 3 MAJOR / 2 MINOR / 1 NIT. All applied → STATEMENT v1.1 (locked).

| # | finding | action |
|---|---|---|
| 1 MAJOR | statuses claimed before proof files existed | Statuses now tied to the proof files (`lemmas/A_occam.md` … `E_visibility.md`, written 19:35–20:05 during the lock), "PROVED (by this seat, unchecked)" until each check record says otherwise; inherited statuses kept separate. |
| 2 MAJOR | 𝒢_n dropped (G4), needed by [P3] lem:signalgain | Events split: 𝒢^sup = (G1–G3), 𝒢^sel = 𝒢^sup ∩ (G4), 𝒢⁵ (Claim E cross terms), with exceptional probabilities 4/n, 5/n, 1/n. A1 assembly, C (cases i–ii) and D(b) use 𝒢^sel; E and C(iii) use 𝒢^sup ∩ 𝒢⁵ (no (G4)). |
| 3 MAJOR | C's uniform n₀ vs eventual hypotheses | C restated as a per-n bound: hypotheses at that n, n₀ depending only on constants (every step is a single-n bound). (OS) defined at a given n. Random-design expectation transfer adds P(𝒜_nᶜ). |
| 4 MINOR | (OS) is not "the weakest"/near-characterisation; second inequality absent from A2 | A2 text rewritten: (OS) is a sufficient envelope used by this proof; the j > j₀ amplified inequality has no counterpart in A2; fixed vs random design versions of A2's necessity separated. |
| 5 MINOR | pressure points | e^{jε_n} absorbed per j by the 2^{|J|/2} factor in a_J (lead correction LC-1; no m♯ε_n → 0 needed); union coverage by the range j ≤ min(m♯_n, p − s₀) (LC-2); d_J = 0 handled in Lemma M; Λ tail from the deterministic [L1a′] reference with explicit λ = λ₀ + 2√(2 log n) (C_expectation.md); θ zero-padded (D(a)); D(b) bounds uniform over 𝒮_n; E comparison written in full in Lemma E1(b), using Q_{S′} ≤ Q_{S₀}, (F₀), (G3′) and the separate event 𝒢⁵, not the lower half of [P3] cor:diff. |
| 6 NIT | relations/qualifications | Added: E supersedes via a fixed c′ ∈ (c₁, c); r_n = o(min(q_n, 1 − q_n)) restored in E; D described as an in-sample marginal Hellinger analog; Song–Liang scope difference recorded in ASSUMPTION_MAP. |
