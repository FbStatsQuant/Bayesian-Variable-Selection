"""Population block-projection leakage lambda_b(S0)/(n-1) for the study scenarios S1-S6 (p=500, truth() of
gen_dev_data.R), blocks = single groups of 5 and = pairs of consecutive groups (what next-fit packing at B=14
produces when the leaf order follows group order). lambda_b/(n-1) > 0 means the favourable-regime leakage
condition fails linearly in n (population level)."""
import numpy as np
def cov(s, p):
    grp = np.arange(p) // 5; H = (grp[:, None] == grp[None, :]).astype(float); I = np.eye(p)
    if s == 1: return I
    if s == 2: return 0.5 ** np.abs(np.subtract.outer(np.arange(p), np.arange(p)))
    if s == 3: return 0.7 * H + 0.3 * I
    if s == 4: return 0.85 * H + 0.15 * I
    if s == 5: return 0.3 * np.ones((p, p)) + 0.4 * H + 0.3 * I
    rho = 0.4 + 0.1 * (grp % 6); S = H * rho[:, None]; np.fill_diagonal(S, 1); return S
def truth(p=500):
    s0, step = 14, 7; pos = [3, 2, 4, 1, 5, 3]; pat = [1.4, -1.0, 1.8, -1.2, 0.8, -1.6]
    k = np.arange(s0); block = 1 + step * k
    act = 5 * (block - 1) + np.array([pos[i % 6] for i in k]) - 1
    th = np.zeros(p); th[act] = [pat[i % 6] for i in k]; return th
if __name__ == '__main__':
    p = 500; th = truth(p); S0 = set(np.flatnonzero(th))
    for s in range(1, 7):
        Sig = cov(s, p); c = Sig @ th; tot = th @ c
        for width in (5, 10):
            lams, maxnull = [], 0.0
            for start in range(0, p, width):
                C = list(range(start, min(p, start + width))); U = [j for j in C if j in S0]
                SC = Sig[np.ix_(C, C)]; gam = np.linalg.solve(SC, c[C]); full = c[C] @ gam
                part = c[U] @ np.linalg.solve(Sig[np.ix_(U, U)], c[U]) if U else 0.0
                lams.append(full - part)
            lams = np.array(lams)
            print(f"S{s} blocks of {width:2d}: max lambda_b/(n-1) = {lams.max():.4f}, #blocks with lambda>1e-10: {(lams>1e-10).sum()}/{len(lams)}, theta'Sigma theta={tot:.2f}")
