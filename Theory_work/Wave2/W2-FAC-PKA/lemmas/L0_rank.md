# L0: realizability frontier

Status: PROVED (by this seat), lemma check R02 VERIFIED (reviews/R02_lemmas_claude.md). Target T0. Not PROVED-CHECKED.

For n>=3, rho in (0,1), a real centered n by p matrix with X'X=(n-1)[(1-rho)I+rho11'] exists iff p<=n-1.

Necessity: centered columns lie in the (n-1)-dimensional subspace orthogonal to 1. Thus rank(X'X)<=n-1. The proposed Gram has eigenvalues (n-1)(1-rho), multiplicity p-1, and (n-1)(1+(p-1)rho), multiplicity one; all positive, so its rank is p.

Sufficiency: choose n by p orthonormal Q with columns in 1-perp (possible when p<=n-1), and positive definite square root R of Sigma. Put X=sqrt(n-1) Q R. Then 1'X=0 and X'X=(n-1)Sigma. Each column has squared norm n-1, so sample variance 1 and is nonconstant. Take raw X equal to X. Column sign conjugation does not alter rank or existence.

Consequences: a sequence with p/n->infinity cannot have this exact sample Gram. This does not preclude population CS, singular deterministic factor designs, or a method-consistency theorem in those settings. The feasible saturated range K<p<=n-1 remains nonempty.

Falsification script: numerics/n2_checks.py; output numerics/N2_checks.json.
