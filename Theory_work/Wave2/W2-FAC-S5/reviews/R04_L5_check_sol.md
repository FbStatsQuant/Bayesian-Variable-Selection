# R04 — Cross-family check of L5

**Verdict: VERIFIED-WITH-AMENDMENTS.**

Reviewed the locked STATEMENT v2 and every line of `lemmas/L5_assembly.md`, assuming this folder's L1–L4 as stated. One required mathematical correction: CC_n is generally **not data-measurable**. This does not invalidate (C3-R), (C4-R), or the conditional Tier-2 corollary: the locked statement already places CC_n on the enlarged probability space, where the union bound is valid. No counterexample to those conclusions was found under their full listed premises. No claim that KL is proved is endorsed here. Only this review file was written.

Paths below are relative to the repository root; unqualified L5 line numbers refer to `Theory_work/Wave2/W2-FAC-S5/lemmas/L5_assembly.md` as reviewed.

1. **REQUIRED AMENDMENT — false measurability/transfer assertion (L5:24–26).**

   K_n is data-measurable: finite deterministic start-mode computation, a finite data-dependent integer cap, exact finite comparisons with deterministic tie breaking, and finite scans determine whether S_0 is scored. As in FINAL `s7_impl.tex:36–48`, this deterministic search is defined even on branches that do not execute it.

   CC_n is different. It contains e_R = h - E[h | g_R], where h = sqrt(rho_b) eta is a latent common factor. Measurability in (eta, zeta, xi) does **not** imply measurability in the observed data. In particular,

   Var(h | g_[p]) = [rho_b^(-1) + sum_g q_g/(d + b q_g)]^(-1) > 0

   for every finite p. Knowing r does not remove this latent uncertainty. The data-dependent choice of the path Pi likewise does not reveal h.

   A counterexample to the measurability assertion is already available inside the locked class: p = s_0 = q_1 = 1, positive fixed truth coefficient, and the singleton method block. Then S* = S_0 and Pi consists only of its terminal set. We have e_{S_0} = h - rho_b g_1, independent of g_1 with variance rho_b(1-rho_b) > 0. For all sufficiently large n,

   CC_n(delta) = {|e_{S_0}| <= a_n},
   a_n = [sqrt((1-delta)(log n - 2 log 2)) - H_q]/kappa_0 > 0.

   Its conditional probability given the original data is strictly between zero and one. Thus this event cannot be a data event, even though it is measurable on the enlarged space. This example concerns CC_n's measurability, not failure of the consistency claim.

   **Fix:** replace L5:24–26's transfer sentence by: "K_n is data-measurable, so its original-law probability equals its probability on L1's enlarged space. E_n and CC_n(delta) are measurable on that enlarged space; probabilities of CC_n below refer to that space, as specified in STATEMENT section 3." If P_0 denotes the original law and P_tilde the enlarged law, write the proof explicitly as

   D_n <= P_0(K_n^c) = P_tilde(K_n^c)
       <= P_tilde(E_n^c) + P_tilde(CC_n(delta)^c)
       = P_tilde(CC_n(delta)^c) + o(1).

   This uses an ordinary union bound, not independence, and transfers only the probability of the data event K_n. No change to the locked statement or new hypothesis is needed.

2. **VERIFIED — input identities and status quotations (L5:3–12).**

   - SoP `Theory_work/State_of_Project/sections/04_theory.tex:492` gives exactly T38-(0) "PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))". The bound in L5:8 is the corrected expectation form in that source's lines 480–483, with the composition clause in line 487. The deterministic posterior threshold is pointwise, not a threshold on its expectation.
   - SoP line 84 defines D_n exactly as P(O_bar intersect {S_0 not in S_bar^+}); the bar on O is the **potential output event**, not the complement of output. L5's use is consistent with that definition. It does not confuse this bar with CC_n^c.
   - FINAL `Theory_work/Wave1C/FINAL/sections/s3_posterior.tex:5–16` states T03-sharp and contains the quoted status fragment "PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)". It is an algorithm-free fixed-design result; no LH-only result or SAME-FAMILY-ONLY T01–T03 claim is substituted for it.
   - `Theory_work/Wave1/W1-GEN/STATEMENT.md:169–171` gives exactly [OP] "PROVED (by this seat, unchecked)" and the claimed inclusion. The enclosing Theorem GEN's "PROVED-CHECKED" is confirmed by `W1-GEN/REPORT.md:20`; it does not upgrade [OP]'s individual status.
   - FINAL `s7_impl.tex:45–64` gives CAP(a)'s prefix/certification statement and "PROVED (by this seat)"; line 64 supports council-checked, final round 3 passed, with the fidelity amendments applied.
   - FINAL `s6_delivery.tex:28–49` contains A1's corrected Proposition F, its total fallback, MR1 cap, enlarged allocation and status history. FINAL lines 53–58 give F-GROW's exact status "PROVED (A2), checked by A3". `Theory_work/Wave1C/HQ_AUDIT/A2_propF_GROW.md:55–67` supplies precisely the direct discovery-event/posterior/pathwise argument reused here, including the warning that discovery cannot be inferred from D_n tending to zero.
   - `Theory_work/Wave2/W2-FAC-B/REPORT.md:30` confirms Theorem FAC-CS "PROVED-CHECKED". Its L5 is a checked assembly pattern, not a theorem already covering BCS; S5 L5:3–5 correctly keeps the present extension unchecked.

   **Fix:** none to these quotations. For explicit provenance, expand L5:39's generic qualification sentence to name [OP]'s unchecked status, the e4/N3 qualification, and S.3's code-reading audit. Council approval of corrected F/F-GROW applies to the d315c1e statements; the later preflight addition is separately A4 "OK-WITH-FIXES", fixes applied (FINAL s6:49,58; `HQ_AUDIT/A4_postcouncil_check.md:27–35`). The new BCS extension does not inherit that council approval.

3. **VERIFIED — all H0 hypotheses, including constants (L5:14–18).**

   Read these lines in L1.0's sign-corrected coordinates (L1:11–13). In original coordinates the normalized Gram is Upsilon Sigma Upsilon; its principal eigenvalues are unchanged. In those coordinates

   ||mu||^2 = (n-1) vartheta^T Sigma_{S_0 S_0} vartheta
            <= (n-1) s_0 ||vartheta||^2 < M n

   for the proposed fixed M > (1+s_0)||vartheta||^2. This bound is uniform over varying truth positions and group incidences. L1.2(a)'s floor d > 0 supplies phi_0^2 = d for R and SE_lambda(j_0), with the required j_0 = ceil((2A+1)s_0)+1 = 3s_0+1 at A = 1. SE_w is an **unnormalized** condition: (n-1)d >= g_0 = d for n >= 3. The all-principal-submatrix bound therefore covers every anchored S_0 union J at the actual cutoff m_n^sharp; R_K = 0 ensures that cutoff exists with s_0 <= m_n^sharp <= K. No bound on the cutoff's growth is needed here.

   Eventually p <= n/2 <= n^1, K = p, and s_0 <= p since S_0 is a support in [p]. The minimum absolute truth coefficient is the fixed positive min|vartheta_j|, so BM-infinity with phi_0^2 = d holds. G and fixed s_0 are assumed. These exhaust FINAL s3:6–11. T03-sharp gives posterior convergence in probability; boundedness 0 <= 1-pi(S_0) <= 1 then gives its expectation tending to zero. No expectation rate is inferred from O_P.

   **Fix:** none needed mathematically; explicitly prefix L5.1 with "after L1.0's sign correction" and display j_0 and the cutoff check above for clarity.

4. **VERIFIED — discovery event and cap (L5:20–24).**

   Unlike FACB's separate start event, this folder's E_n already includes E_S (L3:9–15), and L2:43–48 asserts unique start mode on E_n. Thus no additional start-error probability was dropped. Assumed L4:13–20 supplies the exact m_0-step path and terminal completed scan on E_n intersect CC_n. MR1 gives a_n = ell_n + |S*| >= m_0 and also a_n >= ell_n, as required by CAP. CAP(a) applies to this finite measurable cap and certifies the deterministic search; S_0 is scored. No nondegeneracy event beyond the assumed lemmas is needed: Pi and production use the same deterministic tie rule. L3.1 supplies P_tilde(E_n^c) = o(1).

   **Fix:** use item 1's probability-space wording. Define K_n explicitly on every admissible data set, including the exact-branch convention of CAP; execution on an interrupted run is not assumed.

5. **VERIFIED — (C3-R) and the direction of operational closure (L5:28–32).**

   [OP] bounds D_n **above** by LS0 failure, exactly the direction needed. Its extension from the legacy cap to MR1 is justified by the cap-independent retention argument (`Theory_work/Wave1C/C-GROW/lemmas/L4_assembly.md:11–14`); exact enumeration only adds scored models. Applying item 1's chain gives D_n <= P_tilde(CC_n^c)+o(1). The any-X composition result [M5-0], with its implementation premises including CAL and the corrected posterior expectation, then gives the claimed joint-with-output bound. No bounded relevance set, CAL-success probability estimate, or conditional-on-output probability is used.

   **Fix:** none beyond item 1. Keep the full FACB section 1 implementation-premise convention, including its R' > 4 qualifications; the abbreviated S5 list does not remove them.

6. **VERIFIED — CAL-free delivery is a new class extension under all Proposition F premises (L5:34–39).**

   L5's invocation of "Exactly FACB L5.4 steps (1)–(3)" includes that paragraph's explicit adoption of F's method, total tier-1 fallback, all premises and allocation. Locked S5 (C4-R) likewise imports all FACB (C4) premises, not merely the shorter (C3-R) list. The relevant allocation includes W_G, M_G **and** the current-head LS0 preflight time/archive terms of FINAL s6:37–44. A valid but undersized allocation would not suffice.

   For fixed BCS designs under G, raw columns are nonconstant, the retained dimension equals p_raw, and the centered Gaussian response is nonzero almost surely. The all-set scorer bound Q_S >= y^T y/(n+1) > 0 uses only positive semidefiniteness, so A2 steps 1–2 carry over without a relevance-size condition. With the method's actual partition and construction invariants, the same ideal-machine resource/exit argument and total fallback give P(no output)=0 at every admissible n >= 3. This finite-n conclusion does not require the asymptotic path event.

   On output and K_n, the truth is in the all-scored set (or enumeration already scored every feasible model). If pi(S_0)>1/2, it strictly outranks every competitor. Therefore the D-prime pathwise inclusion yields

   P_0(output and wrong) <= 2 E_0[1-pi(S_0)] + P_0(K_n^c).

   P_0(output)=1 and items 1,3,4 give the stated unconditional error bound. This repeats A2:63–67 directly at cap a_n; it does not incorrectly use CAP(c)'s legacy-cap error bound to establish discovery at the larger cap. CAL, restricted-ESS success, IND-T as a new statistical input, and a bound on fallback probability are unnecessary for this argument. Fixed worker count, fixed declared R'=4k, EX-A's unit-cost interpretation, IDEAL-W, MACH, TDP-IMPL, GUARD-W, CONFIG and F's other named premises remain assumptions, with their original audit qualifications.

   **Fix:** no new hypothesis required. For self-contained readability, restate the imported F premises/allocation and say explicitly "extend Proposition F's delivery machinery to fixed BCS designs". Neither F's old class list nor FACB's council approval alone proves this extension. Random-row study S5 remains outside this claim.

7. **VERIFIED — Tier-2 corollary is conditional, not a KL proof (L5:41–44).**

   A fixed delta in (0,1), alpha_0 <= (1-delta)/2 < 1/2, and limsup log p/log n < alpha_0 place each sequence within an admissible P_alpha regime for L5.3/L5.4. If a checked KL gives P_tilde(CC_n(delta)) tending to one, item 1's corrected bounds give joint consistency and, under all delivery premises, P_0(Shat^+=S_0) tending to one. No inference from a numerical CC check or from H0 to KL is made. Without checked KL, only the reduction is justified, consistently with locked STATEMENT:119–122.

   **Fix:** interpret/write KL's probability on the enlarged space, as in item 1. No other amendment to the corollary is needed.
