codex
The scan invariant, certificate claims, and posterior-margin argument check out. I found a false explanatory statement in §5 about when the returned HPM can differ from the last centre, and I’m checking the proof’s model-specific formulas against the supplied definitions.

codex
The core arguments establish STATEMENT.md §§3–4 for the formalized procedure, conditional on H03 for the statistical conclusions. However, the supplied document has an incorrect interpretive claim and an unjustified step in an auxiliary lemma.

The neighbourhood symmetry, running-score invariant, certificate characterization, invariance under changes to unscored values, ledger claims, LIMIT behavior, and unique-maximizer case check out. The deterministic conclusions concerning \(S_0\) also follow correctly. The posterior-odds inequality has the correct direction, and the \(O_{P_0}(1)\) argument requires no lower bound on \(1-\pi(S_0)\).

1. **Location:** STATEMENT.md §5, item 1, beginning “If one instead reads it as the last centre…”.

   **Severity:** fatal — this explanatory claim is false; it does not invalidate the formal conclusions in §§3–4.

   **Claim:** The running HPM \(R\) and the last centre \(c_m\) do not differ only in the presence of score ties. Unique attainment of the largest scored value does not ensure that they coincide.

   **Evidence:** Take \(p=1\), \(n=3\), hence \(K=1\), with
   \[
   \mathcal S^-=\{\varnothing\},\qquad \ell=0,\qquad
   F(\varnothing)=0,\quad F(\{1\})=1.
   \]
   Scan \(0\) scores \(\{1\}\) and stops with LIMIT. The last centre is \(c_m=\varnothing\), whereas \(R=\{1\}\). There are no score ties, and the scored maximum is unique. More generally, (i-d) itself establishes \(F(R)>F(c_m)\) on every LIMIT outcome. Thus the explanatory sentence contradicts a formal claim that the proof correctly establishes.

2. **Location:** PROOF_v1.tex, “Clause (ii), margin and statistical parts,” lemma labelled `lem:finite`, proof for nonempty \(S\).

   **Severity:** gap.

   **Claim:** The asserted lower bound on \(Q_S\) is not justified by definitions supplied in the permitted files.

   **Evidence:** The proof establishes
   \[
   n z_S^\top H_S^{-1}z_S\le \frac{n}{n+1}y^\top y
   \]
   and immediately concludes
   \[
   Q_S\ge \frac{y^\top y}{n+1}\ge0.
   \]
   However, neither supplied text defines \(Q_S\) for nonempty \(S\), or states an identity connecting it to the preceding quadratic form. Only \(Q_\varnothing\) is defined. Consequently this implication, and therefore this particular derivation of positivity of the displayed marginal likelihood, cannot be verified from the permitted files. The identification of those detailed formulas with the method’s marginal likelihood also relies on an external source whose contents are not supplied.

   This is an auxiliary derivational gap: the stated setting already assumes a real-valued score, and the subsequent posterior-odds calculation is correct.

3. **Location:** STATEMENT.md §5, item 2.

   **Severity:** exposition.

   **Claim:** “Having been a centre in any earlier local search” omits the current search and therefore does not accurately restate (i-a).

   **Evidence:** A returned model can be a centre in the first local search of a run, when no earlier local search exists. Both (i-a) and its proof correctly use searches “up to and including this one.” The explanatory wording drops that qualification.

Regarding faithfulness to the original clauses: §§3–4 give a faithful conditional formulation under the procedure specified in §2 and the explicitly stated interpretation of “Under T03” as assuming H03. The stronger conclusions about LIMIT and earlier centres are valid consequences of that procedure. The statistical proof establishes consequences of H03; it does not establish H03 from G, R, SE, or the signal assumptions. The principal problem with the stated readings is §5.1’s false assertion that the two meanings of “returned model” differ only through ties.

**Verdict: not verified.**
