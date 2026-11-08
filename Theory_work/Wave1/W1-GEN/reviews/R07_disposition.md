# Disposition of R07 (Codex Sol) on L6: (a)-(c) VERIFIED-WITH-AMENDMENTS; (d) GAP

All amendments applied in L6 v2.
(a) citation T38_PROOF.md:267; fixed phi0^2 = (1-max|psi|)(1-rho+), g0 = phi0^2; empty minima omitted.
(b) raw model y = X^r theta + eps stated; Beta laws proved for the deterministic GROUP families first, then intersected
    with partition recovery (Lemma T discipline); the X-event A_n is defined by explicit inequalities (N_n is the
    intersection of both NL inequalities; VS_n by the explicit gain bound); fixed constants and envelopes listed
    (eps0 = 1, c_S = 1/2, g0 = lambda0/2, vbar_y = sigma^2 + 2M); notation L (block cap) vs Z (Beta).
(c) exact spectrum of Sigma_n (3/4, 3-9eps, 3+(p-9)eps) for both eps variants; fixed phi0^2 = g0 = 1/2; sharper cross
    covariance 3eps/(3+q) <= eps; null-block factor corrected (16/3).
(d) GAP addressed by a new selection-uniform argument (Lemma SEL in L6(d)): reduce any selected T to
    T0 = T cap (l's group cup signal groups) (deterministic family of constant size 2^75 per l), prove the fixed-pair
    Beta law on T0, and control the change T0 -> T by the exact recursive partial-correlation formula with uniform
    O(sqrt(log p/n)) partial correlations to the extra null regressors (R07 item 9's repair route). VIS made uniform via
    the Gram event (item 8); the false v_U bound replaced by v_U <= 1 + 2M on {||mu||^2/n <= M}.
    S5 argument restated via NL_C failure for every bounded S* (item 10; SEP sentence deleted). S2 argument restated to
    the right of the last truth with nonzero q and D_n = min(p_n - j_max, alpha log_4 n) (item 11).
    STATUS: L6(d) v2 is a NEW proof step, not yet re-checked -> included in the exhaustive sweep.
