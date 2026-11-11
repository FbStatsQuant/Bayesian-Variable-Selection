# PC2 — adversarial repair check (Sol)

Reviewed 2026-11-11. Paths are relative to `Theory_work/Wave3/W3-POST2/` unless otherwise stated. Ran `git diff -- Theory_work/Wave3/W3-POST2` and checked its five changed files against PC1 P1–P3 and their proof dependencies. Read-only review except for this output file; no git state changes or subagents.

## P1 — repaired cutoff and dependent proof: PASS

The chain in `lemmas/D_hellinger.md:53-55` is now correct, including when K is smaller than the nominal cardinality bound:

1. By `lemmas/D_hellinger.md:50-51`, S ∈ 𝔉 implies S₀ ⊄ S and |S∖S₀| ≤ j₀. Consequently |S∩S₀| ≤ s₀−1, and |S| = |S∩S₀| + |S∖S₀| ≤ s₀+j₀−1.
2. Also S ∈ Ω, hence |S| ≤ K. `STATEMENT.md:15-16` explicitly inherits Ω and K from W3-POST §0; `../W3-POST/STATEMENT.md:21` defines Ω = {S ⊆ [p] : |S| ≤ K}, K = min(p, floor(n/2)). Thus |S| ≤ min(s₀+j₀−1,K). This combines two bounds on |S|; it does not claim s₀+j₀−1 ≤ K.
3. Monotonicity of the minimum gives min(s₀+j₀−1,K) ≤ min(s₀+j₀,K), without any restriction on which argument is smaller.
4. Apply E0 (`lemmas/E_visibility.md:16-20`) with B = s₀+j₀. `STATEMENT.md:21` gives j₀ = ceil((2A+1)s₀)+1. In inherited R1, s₀ ≥ 1 and A ≥ 1 are fixed (`../W3-POST/STATEMENT.md:63-66`); therefore B is a fixed integer and B ≥ s₀+1. E0 yields min(s₀+j₀,K) ≤ m♯_n for all sufficiently large n, uniformly over the allowed p. B depends only on s₀,A, so this invocation adds no parameter dependence to C_H and no new hypothesis.

**Independent check of E0.** The inherited cutoff has threshold n^{−(s₀+2)/2}, minimizes over integers m ≥ s₀, and is at most K (`../W3-POST/STATEMENT.md:36-38`). For s₀ ≤ m < min(B,K), the positive term q_{m+1}/w(s₀) belongs to R_m. The ratio product in E0 is exactly [T03R] `PROOF.md:22,32` (under the inherited ARC alias). Every factor (p−i)/(2p−1−i) is positive. For p ≥ 2B it is at least 1/4; for p < 2B it is at least 1/(4B). There are m−s₀+1 ≤ B factors, and C(p,s₀) ≥ 1. Thus R_m ≥ (4B)^{−B}. Taking n₀ strictly larger than (4B)^{2B/(s₀+2)} excludes every such m. If K < B, the conclusion is m♯_n = K because R_K = 0. If K = s₀ the conclusion follows immediately from the cutoff's domain. E0's hypotheses and proof cover all these cases.

**Counterexample attempts.** PC1's p=K=2, s₀=A=1 case has j₀=4 and B=5. Here R_1=1 and R_2=0, so m♯_n=2 for n≥4. With S₀={1}, the underfits are ∅ and {2}, of sizes 0 and 1. The repaired chain reads |S| ≤ min(4,2)=2 ≤ min(5,2)=2 = m♯_n. The false comparison 4≤2 has disappeared. The same reasoning covers K<s₀+j₀−1, K=s₀, p=s₀ (only deletion underfits), empty S, and K≥s₀+j₀ (including growing p). In the last case E0 eventually puts the entire bounded-excess family below the cutoff. As a supplementary finite check, an in-memory Python sweep tested 87,307 feasible cardinality tuples with 2≤p≤16, 1≤s₀≤p, A∈{1,1.25,2,5}, s₀≤K≤p, and every feasible intersection/excess size; all first two inequalities passed. E0's product lower bounds also passed on this grid. The uniform argument above, rather than this finite sweep, establishes the asymptotic last inequality.

**Remaining D3, checked through the conclusion.**

- `lemmas/D_hellinger.md:52-59`: the three sets cover Ω∖𝒮_n. The repaired bound additionally puts every near underfit below the cutoff, as required for the conditional event bounds. Tail and strict-superset masses use T02(i♯) and A1 5(a), respectively, with only (E),(F₀),(OS). For a far underfit with excess ≤j₀, exclusion from 𝒰_near forces L_S≥c₂σ*²log n. E1(b) is applicable at c₂=c₁+1 without assuming a global identifiability condition. For excess >j₀, the unconditional comparison and amplified OS sum apply. The E2 assembly (`lemmas/E_visibility.md:61-65`) remains valid for this subfamily: multiplicity is bounded by 2^{s₀}, and comparison unions may leave Ω, as already allowed by `STATEMENT.md:33-34`. Thus mass outside 𝒮_n is O_P(r_n).
- `lemmas/D_hellinger.md:60-65`: |S|≤s₀+j₀ and L_S≤c₂σ*²log n hold on 𝒮_n for large n, including S₀ because its ridge loss is bounded by ρ̄. The repaired cutoff gives |S|≤m♯_n for near models, and m♯_n≥s₀ handles S₀; hence (G2*) covers every model used. The cross-term event covers 𝒰_near, and the separate displayed projection argument covers S₀. D1 then yields the stated fitted-mean and residual bounds uniformly. Empty models cause no problem: their noise projection is zero.
- `lemmas/D_hellinger.md:66-71`: with ν−1=n/2−0.99 and N=n−1, subtracting σ*² from (2b+Q^c_S)/(n−1.98) gives exactly the displayed +0.98σ*² term. The bounded b term is absorbed by the log n envelope eventually. The IG variance is O(1/n) uniformly on the good event. Crucially the common χ²_N fluctuation is O_P(√n); together with O(log n) model-dependent residual error, this yields the stronger uniform O_P(n^{−1/2}) posterior-mean error, sufficient for every diverging M_n.
- `lemmas/D_hellinger.md:72-79`: C_H=4m_n^{fit}/log n+1 depends only on s₀,A,σ*². The mean split and Markov bound have the stated constants; Chebyshev gives the 16/M_n² variance tail. Adding the O_P(r_n) discarded mass proves the joint contraction, and M_n=√log n proves the fixed C_H′ Hellinger bound. Neither beta-min, (F_λ), (G4), nor (ID) has been silently reintroduced.

**Statements and intercept.** `STATEMENT.md:112-119`, `REPORT.md:94-100,240-242`, and `ASSUMPTION_MAP.md:16,38,46,59-61` remain supported by this proof. The report's rate shorthand is read in its explicitly stated posterior-contraction sense. The random-design transfer in `STATEMENT.md:117` still uses the inherited common-constant event interface; the repair introduces no additional design condition.

For `lemmas/D_hellinger.md:84-88`, inherited truth `../W3-POST/STATEMENT.md:31` gives the raw mean error ε̄1+(μ̂−μ). Orthogonality yields squared norm nε̄²+‖μ̂−μ‖², so the displayed intercept-inclusive Hellinger upper bound is valid and nε̄²/σ*² has the χ²₁ law. D(a) survives since this adds a sampling-tight term to n times the squared-distance bound. For D(b), retaining exactly C_H′ requires slack: use D3's variance result with M_n=√(log n/2). Outside vanishing posterior mass its squared variance contribution is ≤log n/(2n), while ε̄²/(4σ*²)=o_P(log n/n) fits in the remaining log n/(2n). The mean contribution stays ≤C_H log n/(4nσ*²). Therefore the same C_H′ works, not merely a larger unspecified constant. No independence between these bounds is needed.

## P2 — N2 qualification: PASS

Searched REPORT, STATEMENT, ASSUMPTION_MAP, every lemma, and additionally all non-review ticket files for N2, duplicate-null wording, strict weakening/separation, and sharpness wording (PowerShell Select-String fallback because rg is unavailable).

- `lemmas/A_occam.md:33-34` now says “appears to allow,” explicitly “finite-n evidence only,” and “no asymptotic proof.”
- `ASSUMPTION_MAP.md:14` now qualifies the ADG-to-OS N2 evidence as finite-n, with no asymptotic proof; its numerical row at `:27` already gives the same qualification.
- `REPORT.md:143-150` explicitly limits the observations to finite n and gives no asymptotic proof; `:193` still lists explicit-design asymptotic strictness as open.
- `STATEMENT.md:35-38,46,54-66` states the sufficient interfaces and proved implications, without claiming that N2 establishes asymptotic strictness. Other lemmas contain no unqualified N2 separation assertion. The numerical script/output N2 labels assert failure of F_λ/DG/ADG, not asymptotic satisfaction of OS; those labels do not undo the qualification.

No remaining unqualified N2 assertion of asymptotic OS satisfaction or strict separation was found in the current claim documents. Historical reviews retain quoted superseded wording and are not current theorem assertions.

## P3 — predictive sharpness qualification: PASS

The literal phrase “cannot be improved” remains once among the current claim documents, at `lemmas/D_hellinger.md:98`. Read with `:96-97`, it is explicitly an argument with “no lower bound is proved,” not a proved sharpness claim. `ASSUMPTION_MAP.md:59-61` now says “argued, not proved” and “no lower bound proved.” Both match `REPORT.md:161-162`. D(b)'s log n/n evidence remains numerical, with no proved lower bound (`lemmas/D_hellinger.md:98-101`, `ASSUMPTION_MAP.md:60-61`, `REPORT.md:191`). STATEMENT gives upper contraction results only (`STATEMENT.md:107-119`); no new lower-bound theorem is asserted there or elsewhere in the lemmas.

## New claims introduced by this repair diff

No new theorem, extension, numerical result, hypothesis, rate, constant, or asymptotic example is introduced. The D3 edit supplies the correct explicit cardinality inference needed by the existing theorem (`lemmas/D_hellinger.md:53-55`). P2 and P3 reduce the asserted evidential strength of existing remarks (`lemmas/A_occam.md:33-34`, `ASSUMPTION_MAP.md:14,59-61`, `lemmas/D_hellinger.md:96-98`). E0 and the intercept extension predate this repair diff; both were rechecked above. The new minimum bound is a justified proof repair, not an expansion of D(b)'s domain or conclusion.

Verdict: REPAIRED (D(b)'s proof is now correct and P2/P3 are consistently propagated).
