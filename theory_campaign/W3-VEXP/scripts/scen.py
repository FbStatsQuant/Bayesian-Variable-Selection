"""Scenario covariances and truth, ported from Scripts/Data_generators/gen_dev_data.R."""
import numpy as np


def scenario_cov(sc, p):
    group = (np.arange(p) // 5) + 1
    H = (group[:, None] == group[None, :]).astype(float)
    I = np.eye(p)
    if sc == 1: return I
    if sc == 2: return 0.5 ** np.abs(np.subtract.outer(np.arange(p), np.arange(p)))
    if sc == 3: return 0.7 * H + 0.3 * I
    if sc == 4: return 0.85 * H + 0.15 * I
    if sc == 5: return 0.3 * np.ones((p, p)) + 0.4 * H + 0.3 * I
    rho = 0.4 + 0.1 * ((group - 1) % 6)
    S = H * rho[:, None]; np.fill_diagonal(S, 1.0); return S


def truth(p):
    s0 = {500: 14, 1000: 14}[p]; step = {500: 7, 1000: 13}[p]
    pos = [3, 2, 4, 1, 5, 3]; pat = [1.4, -1.0, 1.8, -1.2, 0.8, -1.6]
    k = np.arange(s0); block = 1 + step * k
    active = 5 * (block - 1) + np.array([pos[i % 6] for i in k]) - 1  # 0-based
    return active, np.array([pat[i % 6] for i in k])
