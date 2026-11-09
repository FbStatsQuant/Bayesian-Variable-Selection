"""R04 independent exact singleton-CS LS0 simulator (rho=1/2, sigma=1). Own code; not cs_core.
Scores from D0: H=(n+1)G+I, Q=y'y-n z'H^-1 z, nu=.01+n/2, F=log w(k)-.5 log(detH/det(G+I))-nu log(.02+Q).
Shifted stats u_j=z_j-b avoid cancellation."""
import math, numpy as np
from scipy.special import gammaln

class Model:
    def __init__(s, n, p, s0, rng):
        s.n, s.p, s.s0 = n, p, s0
        h = n - 1.0; s.h = h
        s.K = n // 2
        eta = rng.standard_normal(); xi = rng.standard_normal(p)
        r = rng.chisquare(n - 1 - p) if n - 1 - p > 0 else 0.0
        theta = np.zeros(p); theta[:s0] = 1.0
        g = (eta + xi) / math.sqrt(2)
        gSg = 2 * (g @ g - g.sum() ** 2 / (p + 1))
        thSth = 0.5 * s0 + 0.5 * s0 ** 2
        s2 = (h * thSth + 2 * math.sqrt(h) * g[:s0].sum() + gSg + r) / h
        s.sd = math.sqrt(s2)
        s.eta, s.xi, s.r, s.e2 = eta, xi, r, gSg + r
        s.b = (h * s0 / 2 + math.sqrt(h / 2) * eta) / s.sd
        s.d = math.sqrt(h / 2) / s.sd
        s.f = h / (2 * s.sd)
        s.u = s.d * xi + s.f * theta          # z = b + u
        s.al = (n * n - 1) / 2 + 1; s.be = (n * n - 1) / 2
        s.al2 = h / 2 + 1; s.be2 = h / 2
        s.nu = .01 + n / 2
        k = np.arange(s.K + 2)
        s.lw = -math.log(2) - (gammaln(2 * p) - gammaln(k + 1) - gammaln(2 * p - k))
        km = np.maximum(k, 1)
        s.Lk = np.where(k > 0, (km - 1) * math.log(s.al / s.al2) + np.log((s.al + km * s.be) / (s.al2 + km * s.be2)), 0.)
    def F(s, k, U1, U2):
        k = np.asarray(k); gam = s.be / (s.al + k * s.be); om = s.al / (s.al + k * s.be)
        num = U2 - gam * U1 ** 2 + 2 * s.b * U1 * om + k * s.b ** 2 * om
        Q = s.h - s.n * num / s.al
        return s.lw[k] - .5 * s.Lk[k] - s.nu * np.log(.02 + Q), Q
    def start(s):
        # singleton BF increasing in z^2; z>0 checked by caller -> top K by z (all sizes K checked separately)
        z = s.b + s.u
        order = np.argsort(-z ** 2, kind='stable')
        # verify size: cumulative start score maximised at K
        n, h = s.n, s.h
        H1 = (n + 1) * h + 1
        logbf = -.5 * math.log(H1 / (h + 1)) - s.nu * (np.log(.02 + h - n * z ** 2 / H1) - math.log(.02 + h))
        vals = s.lw[:s.K + 1] + np.r_[0, np.cumsum(logbf[order[:s.K]])]
        kbest = int(np.argmax(vals))
        return order[:kbest], z, float(logbf.min())

def scan(m, inT):
    """Exact best neighbour of centre inT under production rules (value only, plus move descriptor list of maxima)."""
    u = m.u; k = int(inT.sum()); U1 = u[inT].sum(); U2 = (u[inT] ** 2).sum()
    FT, QT = m.F(k, U1, U2)
    iin = np.flatnonzero(inT); iout = np.flatnonzero(~inT)
    ui, uo = u[iin], u[iout]
    Fd, _ = m.F(np.full(len(iin), k - 1), U1 - ui, U2 - ui ** 2)
    res = dict(FT=float(FT), QT=float(QT), k=k)
    res['del'] = float(Fd.max()); res['del_arg'] = int(iin[np.argmax(Fd)])
    if k < m.K and len(iout):
        Fa, _ = m.F(np.full(len(iout), k + 1), U1 + uo, U2 + uo ** 2); res['add'] = float(Fa.max()); res['add_arg'] = int(iout[np.argmax(Fa)])
    else:
        res['add'] = -np.inf
    ext = np.unique([int(np.argmin(uo)), int(np.argmax(uo))])
    ul = uo[ext]
    Fs, _ = m.F(np.full((len(iin), len(ext)), k), (U1 - ui)[:, None] + ul[None, :], (U2 - ui ** 2)[:, None] + ul[None, :] ** 2)
    a, e = np.unravel_index(int(np.argmax(Fs)), Fs.shape)
    res['swap'] = float(Fs.max()); res['swap_arg'] = (int(iin[a]), int(iout[ext[e]]))
    tr = np.flatnonzero(iin < m.s0)
    res['truth_out'] = float(max(Fd[tr].max(), Fs[tr].max())) if len(tr) else -np.inf
    # multiplier M_T and centre x_T
    gam = m.be / (m.al + k * m.be)
    res['M'] = m.nu * m.n * m.d ** 2 / (m.al * (.02 + QT))
    zsum = k * m.b + U1
    res['xT'] = (gam * zsum - m.b) / m.d
    return res
