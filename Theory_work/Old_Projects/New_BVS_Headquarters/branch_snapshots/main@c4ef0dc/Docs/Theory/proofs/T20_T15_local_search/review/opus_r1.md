# Stage B Opus 5.5 (xhigh) reviewer, round 1, on PROOF_v2 — reply saved verbatim by the lead (2026-10-22)

# Proof review: T20 (T15), clauses (i)–(ii), local-search semantics (PROOF_v2.tex)

**Verdict: verified.** I checked every step of PROOF_v2.tex against STATEMENT.md §§1–4. The proof establishes each claim of §§3–4 under the hypotheses stated there. I found no fatal error and no unrepaired gap. All ten findings are exposition or scope notes. I read only the four files in `review_B_opus\`, and ran no commands.

## Findings

**F1.** Location: STATEMENT (ii-C)3; proof §5, step 3. Severity: **exposition**.
- Claim: (ii-C) lists only "method's F" and H03. Its item 3 says conclusions (ii-A)1–4 hold with probability at least P₀(E_n). But (ii-A) is stated under EX-A and EXEC, and proof step 3 uses it without restating them.
- Evidence: in the formal procedure of §2 (and proof §1) a scan always scores all of 𝒩(c_k), so within the model the claim is true. As a statement about the implementation, though, the bound would only be P(E_n ∩ {EXEC}) if EXEC could fail with positive probability. EX-A and EXEC should be named in (ii-C)3.

**F2.** Location: STATEMENT (i-b); proof §1 ("The move order") and the (i-b) paragraph. Severity: **exposition**.
- Claim: (i-b) replaces F by F′ but does not say which move order the F′-run uses. The proof settles this by fixing a tie order τ that does not depend on F.
- Evidence: the claim depends on ▷′ agreeing with ▷ on each I_k ⊆ 𝒮_end.
  - With a fixed τ, ▷_{F′,τ} and ▷_{F,τ} agree on 𝒮_end because F′ = F there. This includes τ := ▷.
  - If ▷′ were any strict total order merely compatible with F′, two models in I_k with F(N) = F(N′) could be ordered differently, and c′_{k+1} could differ from c_{k+1}.
  - The statement's phrase "fixed deterministic rule" supports the proof's reading, but (i-b) should say it explicitly.
- I checked the proof's lemma that every ▷ with F(S) > F(T) ⇒ S ▷ T equals ▷_F when τ := ▷. If S ▷ T, then F(S) < F(T) is impossible (it would give T ▷ S), so S ▷_F T. Both are strict total orders, so they are equal.

**F3.** Location: STATEMENT (i-b), the parenthetical "in particular it does not certify global maximality". Severity: **exposition**.
- Claim: as worded, this is not true when 𝒮_end = Ω.
- Evidence: if 𝒮_end = Ω then R = best(Ω) is the global maximiser by eq. (1), so on cert = 1 global maximality does hold. The proof correctly adds the condition "if Ω∖𝒮_end ≠ ∅"; the statement should carry it too.

**F4.** Location: STATEMENT (i-a), "neighbours with F(N) = F(R) are permitted"; proof (i-a), second paragraph. Severity: **exposition** (bears on fidelity).
- Claim: only some equal-score neighbours are compatible with cert = 1.
- Evidence: if cert = 1 then 𝒩(R) ⊆ 𝒮_end and R = best(𝒮_end), so every equal-score neighbour N satisfies R ≻ N. That means |N| > |R|, or |N| = |R| with a lexicographically later index list.
  - Example: a centre c_m with an equal-score deletion neighbour c_m∖{i} is never certified. That neighbour becomes R, and R ∉ 𝒞.
  - The proof states R ≻ N. The statement and the original wording ("equal-score neighbours are allowed") do not show this restriction. §5.1 covers it only indirectly.
- The claim as worded ("permitted", meaning "not excluded") is true and can actually occur. Example: 𝒮⁻ = {R}, and 𝒩(R) contains R∪{j} with an equal score while every other neighbour scores lower. Then NOIMP, R = c_0, cert = 1.

**F5.** Location: proof Lemma 2(d), and the uses of max_{𝒩(c_m)}F. Severity: **exposition**.
- Claim: the proof never states that 𝒩(c) ≠ ∅.
- Evidence: it is true, since p ≥ 1 and K ≥ 1. For c = ∅ an addition exists; for c ≠ ∅ a deletion exists. It is needed for max_{𝒩(c_m)}F to be well defined in (d), unless one uses the convention max ∅ = −∞.

**F6.** Location: proof (ii-C), step 2 (log C and M = max{0, log(2C)}). Severity: **exposition**.
- Claim: C > 0 is assumed but not stated.
- Evidence: the O_P definition only gives C < ∞. The gap is harmless: C can be enlarged, and on a nonempty B_n we have C r_n ≥ 1 − π(S₀) > 0 by Lemma 4.

**F7.** Location: STATEMENT (ii-A), closing sentence; proof §4, last paragraph. Severity: **exposition**.
- Claim: "S₀ is the running HPM from scan k on" holds only from the moment scan k scores S₀, not from the start of scan k.

**F8.** Location: STATEMENT (i-c); proof (i-c). Severity: **exposition / scope**.
- Claim: (i-c) holds by construction of the formal model, so it checks nothing about the implementation.
- Evidence: in §2, `𝒮 := 𝒮 ∪ 𝒩(c_k)` and R := best(𝒮_end) make "all scanned candidates enter the HPM comparison" true by definition. The step R = Ŝ for the final search rests on §2's claims about the method: Ŝ is the best model over everything scored, and nothing is scored after the final search. The proof correctly cites these as given. I could not check them against METHODOLOGY_v3, which is outside the packet. **Unverified.**

**F9.** Location: STATEMENT §§2, 4 and the H03 hypothesis. Severity: **scope (unverified source dependence)**.
- Claim: several premises link the statement to sources outside the packet, and I could not check any of them:
  - (a) H03, including the rate r_n = √(log n/n), is the conclusion of T03(i). STATEMENT itself says T03(i) is only "conjectured", so (ii-C) is conditional on it, and the statement says so.
  - (b) The source's own definition of E_n, which §0 does not quote.
  - (c) The method facts in §2:
    - c_0 = best(𝒮⁻);
    - the move rule;
    - ℓ = ⌈log₂(n+p+1)⌉;
    - the method's "only when" for the flag, read as "iff";
    - every phase feeds the running HPM;
    - nothing is scored after the final search.
- Evidence: none of this can be checked from the packet. The proof uses only the statement's formalisation, so the proof's correctness does not depend on these items. Only the bridge from the statement to the method and to T03 does.

**F10.** Location: STATEMENT (i-d) and §5.5. Severity: **exposition** (fidelity).
- Claim: the source's "a model first discovered by the final extra scan **can be** the reported HPM without a certificate" is formalised only as a conditional ("on LIMIT, …"). No instance is given.
- Evidence:
  - For an arbitrary F an instance is trivial: ℓ = 0, 𝒮⁻ = {c_0}, and some neighbour of c_0 scores higher.
  - For the method's F with the method's ℓ, nothing is shown. §5.5 says so openly.
  - There is a second route the statement does not mention. On NOIMP, an equal-score neighbour N ≻ c_m that scan m scores for the first time becomes R. Then R ∉ 𝒞 and both flags are 0. This does not contradict (i-d) or (i-e), since (i-e) excludes ties.

## Step-by-step checks

(Abridged by the lead only in layout; content as received.) Setting: ≻ strict total order, eq. (1), c ∉ 𝒩(c), 𝒩(c) ⊆ Ω — correct. Lemma 1 (symmetry) — correct. Lemma 2 (invariant) (a)–(e) — correct. Lemma 3 — correct. (i-a) including the earlier-search clause — correct. (i-b) induction, R′ = R, cert test on 𝒩(R) ⊆ 𝒮_end, F′ = F(R)+1 example — correct (subject to F2). (i-d) — correct. (i-e) — correct. (ii-A) items 1–4 and Corollary 3 — correct ("On E_n a scan centred at a neighbour of S₀ cannot occur once S₀ has been scored, because F(c_k) = max over the scored set ≥ F(S₀)"). Lemma 4 (finiteness, thin SVD, Q_S ≥ yᵀy/(n+1), |Ω| ≥ 2) — correct. (ii-B) — correct. (ii-C): O_P definitions standard; on B_n, π(S₀) ≥ 1−Cr_n > ½, E_n holds; λ_n ≥ ½log n − ½log log n − log(2C); Y_n ≤ max{0, log 2C} on B_n; step 3 P(A_n) ≥ P₀(E_n), inner-probability caveat acceptable; E_n measurable (F continuous in the standardised y, and standardisation is a.s. continuous in the Gaussian errors — a minor point the proof does not mention). "All correct, apart from F1 and F6."

## Is STATEMENT §§3–4 a faithful, precise reading of §0?

Largely yes. Within the packet the readings are faithful, and the remaining choices are declared in §5. Point by point:

- **"Certifies exactly that the returned model was itself scanned as a centre and had no strictly improving feasible flip or swap":** faithful. The flag is defined by exactly this condition. (i-a) adds the useful characterisation NOIMP ∧ R = c_m and makes "scanned as a centre" independent of which search did the scanning.
- **"Within the cap":** ambiguous. Both the size cap K and the move cap ℓ are called "cap" in §§1–2, and §5.3 picks K. The choice does no harm: cert = 1 implies NOIMP at m ≤ ℓ, so (i-a) implies the move-cap reading as well.
- **"Equal-score neighbours are allowed; weak local maximality only":** captured by (i-a) and (i-b). The restriction to HPM-later ties (F4) and the qualifier for 𝒮_end = Ω (F3) should be stated.
- **"All scanned candidates … enter the running HPM":** (i-c) holds by construction of the model (F8).
- **"Can be the reported HPM without a certificate":** rendered as a conditional on LIMIT, with no existence claim (F10). Disclosed in §5.5.
- **Clause (ii), first sentence:** (ii-A)1–4 is faithful. "If the subsequent scan executes" becomes EXEC (§5.6), and "if a move remains" becomes k < ℓ.
- **Clause (ii), second sentence:** faithful. "Under T03" becomes the explicit hypothesis H03, and the margin chain is (ii-B) plus (ii-C)2, with "−O_{P₀}(1)" made precise as (A−λ_n)⁺ = O_{P₀}(1).
- **Not checkable from §0** (F9): the definition of E_n as "S₀ is the unique maximiser of F on Ω", the identification of H03 with T03(i), and the method facts in §2. These readings are consistent with the clause's own phrase "a sufficient global margin is min_{S≠S₀}{F(S₀)−F(S)} …", but they are **unverified**.
- **Process claim:** STATEMENT says "no hypothesis was changed or added". That is accurate up to recasting T03 as the explicit hypothesis H03 and source-execution as EXEC, both of which the source names.

## Verdict

**Verified.** The proof correctly proves every claim of STATEMENT.md §§3–4 under the hypotheses stated there. All findings are exposition or scope notes (F1–F10). The links to METHODOLOGY_v3 and T03 (F9) are outside the packet and remain unverified.
