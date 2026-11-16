# T6 · Lemma START-X — PROOF v1 (code reading at pin 4676af6; paths relative to `Scripts/SMC_BVS/core/`)

An independent derivation, then a comparison with N9's proof. Blocks are indexed b = 0, …, J − 1 as in the code;
m_b := |C_b| ≤ K (T2 BLK-a), so top_b := min(m_b, K) = m_b.

## Step 1 — what `build_start` computes (EX-A)
- `logprof[b][j]` = log e_b(j), e_b(j) := Σ_{U⊆C_b, |U|=j} r_b(U), j = 0..m_b: the loop over `codes_by_size[b][j]` (all
  size-j codes, T4) collects `logr[b][c]` and takes `log_sum_exp` (`cpp/v3_start.h:115-117`). e_b(0) = r_b(∅) = 1 and
  e_b(j) > 0 for j ≤ m_b (all r_b > 0).
- `sub_cum[b][j]` is the cumulative of r_b(U)/e_b(j) over the size-j codes in increasing order
  (`cpp/v3_start.h:118`; `cumulative_from_logs`, `cpp/v3_start.h:21-32`: under EX-A c_i = Σ_{t≤i} e^{lp_t − m}/Σ_t e^{lp_t − m},
  and setting the tail after the last positive entry to 1 changes nothing because that value is already 1).
- `logF[b][k]` = log F_b(k) for b = 0..J, k = 0..K, with F_0(k) = 1{k = 0} (`cpp/v3_start.h:122-123`) and
  F_b(k) = Σ_{j ≤ min(m_{b−1}, k)} e_{b−1}(j) F_{b−1}(k − j) (`cpp/v3_start.h:124-131`; the `NEG_INF` test only drops zero
  terms). So F_b is the size generating sequence of blocks 0..b − 1, cut at K.
- `logZbar0` = log Σ_{k≤K} ϖ(k)F_J(k) (`cpp/v3_start.h:133-135`); `size_cum` is the cumulative of ϖ(k)F_J(k)/Z̄₀ over
  k = 0..K (`cpp/v3_start.h:138`).
- `cond_cum[b][r]`, r = 0..K, is the cumulative over j = 0..min(m_b, r) of e_b(j)F_b(r − j)/Σ_{j′} e_b(j′)F_b(r − j′)
  (`cpp/v3_start.h:140-149`), and Σ_{j≤min(m_b, r)} e_b(j)F_b(r − j) = F_{b+1}(r).

## Step 2 — (Z)
Fix k ≤ K. S ↦ (S ∩ C_b)_b is a bijection from {S : |S| = k} onto the tuples (U_b)_b with U_b ⊆ C_b, Σ_b |U_b| = k,
and ∏_b r_b(S ∩ C_b) = ∏_b r_b(U_b). Grouping by (|U_b|)_b gives Σ_{|S|=k} ∏_b r_b(S ∩ C_b) = Σ_{(j_b): Σj_b = k} ∏_b e_b(j_b)
= F_J(k): the k-th term of a convolution of nonnegative sequences uses only indices ≤ k, so cutting every F_b at K
loses nothing for k ≤ K. Since ϖ depends on S only through |S|,
Z̄₀ = Σ_{k≤K} ϖ(k) Σ_{|S|=k} ∏_b r_b(S ∩ C_b) = Σ_{k≤K} ϖ(k)F_J(k) = exp(`logZbar0`).
The reported value: `logZ = D.logm0 + st.logZbar0` at the start of every island (`cpp/v3_engine.h:299`);
`fit$log_Zbar0 <- setup$start$log_Zbar0` (`v3_fit.R:140`) and the final run's `out$log_Zbar0 <- raw$log_Zbar0`
(`v3_run.R:217`; `cpp/v3_core.cpp:515`), both `st.logZbar0`.

## Step 3 — (S)
*Categorical draws.* `cat_draw_gt(cum, u)` returns the smallest i with cum_i > u (`cpp/v3_start.h:18-20`). For
u ~ U[0, 1) and a cumulative with last entry 1, P(i) = cum_i − cum_{i−1} (cum_{−1} := 0); a zero-mass index i has
cum_i = cum_{i−1} and is never returned.

*The draw* (`cpp/v3_start.h:158-176`). Fix A ∈ Ω, k := |A|, k_b := |A ∩ C_b|, U_b := A ∩ C_b, and s_b := Σ_{c≤b} k_c
(so s_{J−1} = k, s_{−1} := 0). The call returns A iff (i) the size draw returns k (`cpp/v3_start.h:160`); (ii) for
b = J − 1, J − 2, … while the remaining size r > 0, the block-size draw at (b, r) returns k_b (`cpp/v3_start.h:163-166`);
the remaining size entering block b is r = s_b; once r = 0 the loop stops and the remaining k_b are 0, which agrees with
A because s_b = 0 forces k_c = 0 for c ≤ b; (iii) for every b with k_b > 0 the within-size draw returns code(U_b)
(`cpp/v3_start.h:169-172`; the code ↔ set map is T4's). These draws use distinct fresh uniforms, so under H-U
  P(A) = [ϖ(k)F_J(k)/Z̄₀] · ∏_{b: s_b > 0} [e_b(k_b)F_b(s_b − k_b)/F_{b+1}(s_b)] · ∏_{b: k_b > 0} [r_b(U_b)/e_b(k_b)].
For b with s_b = 0 the factor e_b(0)F_b(0)/F_{b+1}(0) equals 1 (all three are 1), so the middle product may run over all
b = J − 1, …, 0. As s_b − k_b = s_{b−1}, it telescopes: ∏_b F_b(s_{b−1})/F_{b+1}(s_b) = F_0(0)/F_J(k) = 1/F_J(k). With
e_b(0) = r_b(∅) = 1 the products over e_b cancel. Hence P(A) = ϖ(k)∏_b r_b(U_b)/Z̄₀ = π₀(A). Every denominator met has
positive mass (zero-mass categories are never returned), and the size never exceeds K (`size_cum` is over 0..K). The
number of uniforms is 1 + #(blocks visited) + #(nonempty blocks), a function of the draw. Sorting (`cpp/v3_start.h:174`)
does not change the set.

## Step 4 — (S′)
`Engine::draw_start` is `draw_pi0(st, *vs, S)` with the engine's `st` (`cpp/v3_engine.h:108`); it is the only π₀ draw in
the engine: initial draws (`cpp/v3_engine.h:289`, `init_states = nullptr` in every production call,
`cpp/v3_core.cpp:446, 632, 670`) and independence proposals (`cpp/v3_engine.h:184`). The engine's `st` is the object of
T4 (ENC-b). ∎

## Comparison with N9 (the re-check)
N9's Claim Z and Claim S (`Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/N9-KERNEL/PROOF.md:266-286`)
have the same structure. Checked line by line: its definitions of `logprof`, `sub_cum`, `logF`, `logZbar0`, `cond_cum`
match the code at the pin (lines unchanged since 39db138); its index convention ("F_b is the size profile of the first b
blocks (indices 0..b−1)", ":257-258") is the code's; the telescoping with r_b := Σ_{c≤b} k_c and r_{−1} = 0 is correct;
the early-stop remark ("cond_cum[b][0] puts mass 1 on j = 0") is correct. One precision: N9 writes the middle product
over all b = J−1..0 although the loop visits only blocks with remaining size > 0; the factors for unvisited blocks are 1
(Step 3), so the identity is unaffected. No error found.
