"""Population-level checks for SCENARIOS.md (no random draws).

For each p and scenario: block/position/S6-rho of each active index, positive
definiteness of Sigma, and nominal SNR beta' Sigma beta / sigma^2 at each scale.
Sigma mirrors scenario_covariance() in Experiments_October_14/scripts/design.R.
"""
import numpy as np

PATTERN = [1.4, -1.0, 1.8, -1.2, 0.8, -1.6]
POS = [3, 2, 4, 1, 5, 3]          # within-block position, cycled
S0 = {30: 5, 500: 14, 1000: 14}   # 14 = floor(sqrt(200))
STEP = {30: 1, 500: 7, 1000: 13}  # block spacing; STEP % 6 == 1 keeps the S6 rho cycle


def truth(p):
    k = np.arange(S0[p])
    blocks = 1 + STEP[p] * k
    active = 5 * (blocks - 1) + np.array(POS)[k % 6]
    beta = np.array(PATTERN)[k % 6]
    return active, beta


ACTIVE = {p: truth(p)[0].tolist() for p in S0}
SCALES = [1, .75, .50, .35, .25]


def sigma(s, p):
    g = np.ceil(np.arange(1, p + 1) / 5).astype(int)
    H = (g[:, None] == g[None, :]).astype(float)
    I = np.eye(p)
    if s == 1: return I
    if s == 2: return 0.5 ** np.abs(np.subtract.outer(np.arange(p), np.arange(p)))
    if s == 3: return 0.7 * H + 0.3 * I
    if s == 4: return 0.85 * H + 0.15 * I
    if s == 5: return 0.3 * np.ones((p, p)) + 0.4 * H + 0.3 * I
    rho = 0.4 + 0.1 * ((g - 1) % 6)
    S = H * rho[:, None]
    np.fill_diagonal(S, 1.0)
    return S


for p, act in ACTIVE.items():
    a = np.array(act)
    blocks = (a - 1) // 5 + 1
    pos = (a - 1) % 5 + 1
    rho6 = 0.4 + 0.1 * ((blocks - 1) % 6)
    print(f"p={p}: active={act} blocks={blocks.tolist()} pos={pos.tolist()} "
          f"S6 rho={np.round(rho6, 1).tolist()} beta={truth(p)[1].tolist()} distinct_blocks={len(set(blocks)) == len(a)} max_block={blocks.max()}/{p // 5}")
    for s in range(1, 7):
        Sg = sigma(s, p)
        mineig = np.linalg.eigvalsh(Sg).min()
        b = np.zeros(p); b[a - 1] = truth(p)[1]
        snr = b @ Sg @ b
        print(f"  S{s}: min eig={mineig:.4f}  SNR(c)=" +
              " ".join(f"{c}:{c * c * snr:.3f}" for c in SCALES) +
              f"  R2(c=1)={snr / (1 + snr):.3f}")
