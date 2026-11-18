"""Build AUDIT2: a blind Claude Fable 5.2 batch review of the comparison labels that W3-AUDIT TRACK_B changed in v1.3,
after Song–Liang's on-line supplement was read (HQ rule: a label flip gets a new blind audit; 2026-11-16).
No API call is made here.

  python Theory_work/Wave3/API_AUDIT/audit2_build.py build      # write audit2/{requests.json, REQ_audit2.md, SYSTEM.md, ...}
  python Theory_work/Wave3/API_AUDIT/audit2_build.py verdicts   # after `audit_batch.py wait audit2`: parse AUDIT2 lines

Submission uses audit_batch.py unchanged (count / submit / wait <outdir>); see audit2/README.md.
Scope (one request, two samples): only what changed in v1.3 —
  (1) B4 coefficient size "same as the setting of their proofs"; (2) B5 "not ordered", B6 "weaker" against Theorem S;
  (3) sampler output "a weaker counterpart"; (4) the new headline sentence (WRITING_DELTA_v1.3 blockquote);
  (5) Theorem S against our cores 1 and 3 (TRACK_B §S): the label per item and "our rate implies it".
Sources are read at pinned commits (git show), so a rebuild is byte-identical while the pins hold:
  W3-AUDIT worktree  @ f98cf498 (TRACK_B.md v1.3, AUDIT.md v1.3, WRITING_DELTA_v1.3.md)
  W3-READER worktree @ 7eb818e6 (READER_VERSIONS.md: the reader statements the dossiers compare, as in AUDIT1)
  this worktree      @ e8b5351c (master STATEMENT.md files, as in AUDIT1)
  audit1_build.py    @ 37935108 (its Song–Liang main-text transcriptions are reused verbatim)
Song–Liang supplement passages are transcribed below from the page images (pdftoppm -r 110; key displays re-read at
200–220 dpi); the PDFs and any full-text dump are never copied.
"""
import hashlib, json, re, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUT = HERE / "audit2"
WT_AUDIT = Path("/home/fb31/BVS-wt/W3-AUDIT")
WT_READER = Path("/home/fb31/BVS-wt/W3-READER")
REV_AUDIT = "f98cf498"
REV_READER = "7eb818e6"
SRC_REV = "e8b5351c"
A1_REV = "37935108"  # dept/theory commit whose audit1_build.py supplies the main-text SL transcriptions
SL_PDF = Path("/home/fb31/SMC_Theory_Department/refs/Song_Liang_2015.pdf")  # not in git
SUPP_PDF = Path("/home/fb31/SMC_Theory_Department/refs/Song_Liang_2015_supplement.pdf")  # not in git
MODEL = "claude-fable-5-2"
MAX_TOKENS = 32000
SAMPLES = 2
TAG = "AUDIT2"

SRC = {  # key -> (worktree, rev, path)
    "TB": (WT_AUDIT, REV_AUDIT, "Theory_work/Wave3/W3-AUDIT/TRACK_B.md"),
    "AU": (WT_AUDIT, REV_AUDIT, "Theory_work/Wave3/W3-AUDIT/AUDIT.md"),
    "WD": (WT_AUDIT, REV_AUDIT, "Theory_work/Wave3/W3-AUDIT/WRITING_DELTA_v1.3.md"),
    "RV": (WT_READER, REV_READER, "Theory_work/Wave3/W3-READER/READER_VERSIONS.md"),
    "POST": (ROOT, SRC_REV, "Theory_work/Wave3/W3-POST/STATEMENT.md"),
    "A1": (ROOT, A1_REV, "Theory_work/Wave3/API_AUDIT/audit1_build.py"),
}
_cache = {}


def raw(key):
    if key not in _cache:
        wt, rev, path = SRC[key]
        _cache[key] = subprocess.run(["git", "-C", str(wt), "show", f"{rev}:{path}"], capture_output=True,
                                     check=True).stdout
    return _cache[key]


def label(key):
    wt, rev, path = SRC[key]
    return f"`{path}` @ {rev}"


# ---- the main-text transcriptions of AUDIT1, loaded from the pinned audit1_build.py (no re-typing) ----
def a1_namespace():
    ns = {"__name__": "audit1_build_pinned", "__file__": str(HERE / "audit1_build.py")}
    exec(compile(raw("A1").decode("utf-8"), "audit1_build.py@" + A1_REV, "exec"), ns)
    return ns


A1 = a1_namespace()
SL = dict(A1["SL"])
SCRUB = list(A1["SCRUB"])
BANNED = A1["BANNED"]

# Song & Liang (2015), main text p. 951: the posterior (7) that Theorem S's conclusion (24) refers to.
SL["SL-P7"] = (951, "§2.1.1, the posterior of ξ, (7)", """To facilitate computation, we integrate out β_ξ and σ² from the posterior distribution (5). The resulting posterior distribution of ξ is given by
    π(ξ|D_n) ∝ (r_n/P_n)^{|ξ|} (1 − r_n/P_n)^{P_n−|ξ|} √det(V_ξ^{−1}) / √det(X_ξ^T X_ξ + V_ξ^{−1})
               × {2b_0 + y^T(I − X_ξ(X_ξ^T X_ξ + V_ξ^{−1})^{−1} X_ξ^T)y}^{−n/2−a_0} I(|ξ| ≤ r̄_n).    (7)""")


def scrub(t):
    for a, b in SCRUB:
        t = re.sub(a, b, t)
    t = re.sub(r"\(audit Fable, 2026-11-16\)", "(2026-11-16)", t)
    m = BANNED.search(t)
    if m:
        raise SystemExit(f"status word left in excerpt: {m.group(0)!r} in: {t[max(0, m.start()-80):m.end()+80]!r}")
    return t


def lines(key, a, b):
    L = raw(key).decode("utf-8").splitlines()
    return [(i, L[i - 1]) for i in range(a, b + 1)]


def q(key, *spans, note=""):
    """Verbatim, line-numbered excerpt of one source; spans = (a, b) pairs."""
    parts = []
    for a, b in spans:
        body = "\n".join(f"{i:5d}| {t}" for i, t in lines(key, a, b))
        parts.append(f"{label(key)}, lines {a}–{b}{note}:\n```\n{scrub(body)}\n```")
    return "\n".join(parts) + "\n"


def au(*rows, note=""):
    """AUDIT.md table rows: only the cells 'Assumption' and 'Song–Liang (2015)' are quoted (as in AUDIT1)."""
    out = []
    for a in rows:
        for i, t in lines("AU", a, a):
            cells = re.split(r"(?<!\\)\|", t.strip())
            if t.startswith("|") and len(cells) >= 6:
                c = [x.strip() for x in cells[1:-1]]
                t = f"| {c[0]} | {c[3]} |"
            out.append(f"{i:5d}| {t}")
    return (f"{label('AU')}, lines {', '.join(str(r) for r in rows)}, cells 'Assumption' and 'Song–Liang (2015)' "
            f"only{note}:\n```\n" + scrub("\n".join(out)) + "\n```\n")


# ---- Song & Liang (2015), on-line supplement (20 pages): passages transcribed from the page images ----
# Notation as printed. Bold t (the true model) and italic t (one true predictor) are both written t, as in the
# main-text excerpts. "…" marks omitted text; [as printed] marks a printed slip kept as it is.
SUPP = {
    "SS-ORG": ("1", "organisation; §1.1 opening", """This supplementary material is organized as follows. §1 gives the proofs of the main theoretical results of this paper. §2 describes the SAMC algorithm and its implementation for high dimensional regression, §3 studies properties of the MAP model under our prior setting, and §4 presents a comparison study for the performance of the horseshoe prior and the prior used in this paper.
1 Proofs of Main Theoretical Results
1.1 Proofs of Theorem 2.1 and Theorem 2.2
Let 𝒫 denote a set of probability densities which form the support of the prior. In case of Theorem 2.1 and Theorem 2.2, 𝒫 = {f(x, y|ξ, β_ξ, σ²) : |ξ| ≤ r̄_n, β_ξ ∈ ℝ^{|ξ|}, σ² > 0}. …"""),
    "SS-T23": ("5–6", "§1.2, proof of Theorem 2.3 (complete)", """1.2 Proof of Theorem 2.3
Proof of Theorem 2.3. Assume that a model ξ does not include the true predictor x_t, f is conditional density corresponding to this mode ξ with some arbitrary β_ξ and σ_2². Then, for the Hellinger distance between true f* and f, we have
    d²(f*, f) = 1 − √( 2σ*σ_2/(σ*² + σ_2²) ) ∫_x exp{ −Δh²/(4(σ*² + σ_2²)) } ν_x(dx),
where Δh = β_ξ^T x_ξ − β*_t^T x_t is a linear function of the vector x. Recall that x represents a generic observation of P_n predictors, x_t denotes a generic observation of the true predictors, t ∈ t, and x_t denotes a generic observation of the predictor x_t. Since t ∈ t and t ∉ ξ, we can write Δh = −β*_t x_t + Σ_{i≠t} Δβ_i x_i. Thus, by condition (B_1),
    ∫_x exp(−Δh²/β*_t²) ν_x(dx) ≤ 1 − δ_n.
If 4(σ*² + σ_2²)/β*_t² ≤ 1, then
    ∫_x exp{ −Δh²/(4(σ*² + σ_2²)) } ν_x(dx) ≤ 1 − δ_n, and thus d²(f*, f) ≥ δ_n.
If 4(σ*² + σ_2²)/β*_t² > 1, by Jensen's Inequality,
    ∫_x exp{ −Δh²/(4(σ*² + σ_2²)) } ν_x(dx) ≤ (1 − δ_n)^{β*_t²/(4σ_2² + 4σ*²)} ≤ 1 − β*_t²/(4(σ_2² + σ*²)) · δ_n.
One can show that
    √( 2σ*σ_2/(σ*² + σ_2²) ) ∫_x exp{ −Δh²/(4(σ*² + σ_2²)) } ν_x(dx) ≤ max{ √(4/5), 1 − β*_t²/(20σ*²) · δ_n },
[p. 6] which implies d²(f*, f) ≥ min{ δ_n, β*_t² δ_n/20σ*², 1 − √0.8 }. Combining with the facts that δ_n ≻ ε_n² and ε_n → 0, we conclude d(f*, f) > ε_n, i.e., all the models which do not include the true predictor x_t are outside the ε_n-ball of f*. Because P*{π[d(f, f*) > ε_n | D_n] > e^{−c_1 nε_n²}} < e^{−c_1 nε_n²},
    P*{π[t ∈ ξ | D_n] < 1 − e^{−c_1 nε_n²}} < e^{−c_1 nε_n²}.    □"""),
    "SS-P9": ("9–10", "§2.1, SAMC weight estimates, (13)", """Let θ_{ti} denote the working estimate of log(ω_i/π_i) obtained at iteration t, let θ_t = (θ_{t1}, …, θ_{tm})^T, and let {a_t} denote a positive, non-increasing sequence satisfying the conditions … (9) …
Under mild conditions, Liang et al. (2007) showed that as t → ∞,
    θ_{ti} → Const + log(ω_i) − log(π_i + π̄_0), if E_i ≠ ∅;   θ_{ti} → −∞, if E_i = ∅,    (13)
[p. 10] where π̄_0 = Σ_{j∈{i:E_i=∅}} π_j/(m − m_0) and m_0 is the number of empty subregions, and Const represents an arbitrary constant. The subregion E_i is called an empty subregion if ω_i = 0."""),
    "SS-P10": ("10", "§2.1, importance weights, (14)–(15)", """Furthermore, Liang (2009) showed that SAMC is invariant with respect to an importance weight. Mathematically, this can be explained as follows. Let (x_1, w_1), …, (x_N, w_N) denote a set of samples collected at the sampling step of SAMC, where
    w_t = Σ_{i=1}^m e^{θ_{ti}} I(x_t ∈ E_i).    (14)
Let y_1, …, y_{N′} denote the distinct samples among x_1, …, x_N. If we generate a random sample Y such that
    P(Y = y) = Σ_{t=1}^N w_t I(x_t = y) / Σ_{t=1}^N w_t,   y ∈ {y_1, …, y_{N′}},
then Y is asymptotically distributed with respect to the density f(x). This property implies that SAMC can be used as a usual importance sampling algorithm. For any integrable function h(x), the expectation E_f h(x) = ∫ h(x) f(x) dx can be estimated by
    Ê_f h(x) = Σ_{t=1}^N w_t h(x_t) / Σ_{t=1}^N w_t,    (15)
and, as n → ∞ [as printed], Ê_f h(x) → E_f h(x) almost surely for the same reason that the usual importance sampling estimate converges."""),
    "SS-P12": ("12–13", "§2.4, estimated inclusion probabilities, (21)", """2.4 Estimation of Marginal Inclusion Probability
Suppose that the sample space of the posterior π(ξ|D^n) has been partitioned according to the energy function U(ξ) into m subregions. Let (ξ_1, w_1), …, (ξ_T, w_T) denote a set of models collected in a run of SAMC, where w_t is as defined in (14). Then the marginal inclusion probability can be estimated by
    q̂_j = Σ_{t=1}^T w_t I(j ∈ ξ_t) / Σ_{t=1}^T w_t,   j = 1, …, P_n,    (21)
[p. 13] where I(·) is the indicator function. It follows from Liang (2009) that q̂_j → q_j almost surely as N → ∞, where q_j denotes the true marginal inclusion probability of variable x_j and has been defined in Section 3.1 of the main text."""),
    "SS-TS": ("13", "§3.1, Theorem S, (22)–(25)", """3 MAP Model and Its Consistency
3.1 MAP Model
Many Bayesian studies suggest that the MAP model is potentially a good estimator of the true model, see e.g., Freeman and Smith (2011) and Gupta (2008). In what follows, we establish the consistency of the MAP model with two different choices of V_ξ: V_ξ^{−1} = I and V_ξ^{−1} = X_ξ^T X_ξ/n.
Theorem S. (Consistency of the MAP model) Let D_n be a dataset generated from model (1) of the main text with a sparse true model t. Assume condition (12) of the main text and the following eigen-structure conditions hold: For any model ζ with size |ζ| = min{|t| + r̄_n, n}, there exist a non-increasing sequence {l_n} and a non-decreasing sequence {l′_n} such that
    n l_n < ch′_1(X_ζ^T X_ζ) ≤ ch_1(X_ζ^T X_ζ) < n l′_n,    (22)
    r̄_n log P_n ≺ n l_n.    (23)
If, further, one of the following two condition holds:
  1. n l_n ≻ log l′_n, log(√(n l_n)/r_n) ≻ √(log P_n), and we set V_ξ^{−1} = I for any ξ; or
  2. n l_n ≻ l′_n, log(√n/r_n) ≻ √(log P_n), and we set V_ξ^{−1} = X_ξ^T X_ξ/n for any ξ,
then, for any model k, the posterior probability (7) of the main text satisfies:
    max_{k≠t} π(k|D_n)/π(t|D_n) →_p 0.    (24)
Proof. Under the eigen-structure condition of X, V_ξ^{−1}'s eigenvalues are bounded by two values λ_1 and λ_2. For example, λ_1 = l_n, λ_2 = l′_n in the case V_ξ^{−1} = X_ξ^T X_ξ/n; and λ_1 = λ_2 = 1 in the case V_ξ^{−1} = I. Define R_ξ = y^T(I − X_ξ(X_ξ^T X_ξ + V_ξ^{−1})^{−1} X_ξ^T)y and R*_ξ = y^T(I − X_ξ(X_ξ^T X_ξ)^{−1} X_ξ^T)y. Let β̂_ξ denote the OLS estimator of β_ξ. Then we have R*_ξ < R_ξ < R*_ξ + ω_ξ, where ω_ξ = λ_2 β̂′_ξ β̂_ξ.
For any model k and the true model t,
    π(k|D_n)/π(t|D_n) ≤ (r_n/(P_n − r_n))^{|k|−|t|} · K_2^{|t∖k|}/K_1^{|k∖t|} · {(2b_0 + R_t)/(2b_0 + R_k)}^{n/2+a_0}
                      ≤ (r_n/(P_n − r_n))^{|k|−|t|} · K_2^{|t∖k|}/K_1^{|k∖t|} · {(1 + 2b_0/R*_t + ω_t/R*_t)/(R*_k/R*_t)}^{n/2+a_0},    (25)
where K_1 = K_2 = √(n + 1) if V_ξ^{−1} = X_ξ^T X_ξ/n; and K_1 = √(n l_n + 1), K_2 = √(n l′_n + 1) if V_ξ = I [as printed]."""),
    "SS-P14": ("14", "proof of Theorem S, continued", """Since R*_t follows σ*²χ²_{n−|t|}, we have R*_t = σ*² n(1 + ε_n) as n becomes large, where ε_n = o_p(1), since R*_t/(n − |t|) →^{a.s.} 1. The OLS estimator β̂_t follows a normal distribution with mean β*_t and covariance matrix (X_t^T X_t)^{−1}. Since the eigenvalue of (X_t^T X_t)^{−1} is smaller than 1/(n l_n), we have Var(ω_t) is of smaller order than λ_2²/n² l_n² and ω_t = λ_2 Σ_{i∈t} |β*_i|² + o_p(1). Therefore, {1 + 2b_0/R*_t + ω_t/R*_t}^{n/2+a_0} = O_p(1).
For the rest terms, we first consider the case that t ⊂ k and |k| − |t| = d. … By log(K_1/r_n) ≻ √(log(P_n)) and [display omitted] →_p 0, we conclude that sup_{t⊂k} π(k|D_n)/π(t|D_n) →_p 0.
Now we consider the case k ⊄ t. Let u = t ∪ k and d′ = |u| − |k| = |t∖k| < |t|, then
    R*_t/R*_k = (R*_t/R*_u)(R*_u/R*_k)."""),
    "SS-P15": ("15", "proof of Theorem S, end; remark on (22) and (26)", """It suffices to show
    max_{k⊄t} [R*_u/R*_k]^{n/2+a_0} (P_n K_2/r_n)^{d′} = o_p(1).
We know that (R*_k − R*_u)/σ*² and R*_u/σ*² are independent. The former follows χ²_{d′}(C), and the latter follows χ²_{n−|u|}, where the noncentrality parameter C = β*_t^T X_t^T (P_{X_u} − P_{X_k}) X_t β*_t = β*_t^T X_t^T (I − P_{X_k}) X_t β*_t ≥ n l_n c², P. is the projection matrix, n l_n is the lower bound of the eigenvalues of X_u^T X_u, and c = min_{i∈t} |β*_i|. Therefore,
    R*_u/R*_k = R*_u/(R*_u + (R*_k − R*_u)) ≤ R*_t/(R*_t + (R*_k − R*_u)).
By Theorem 2.1 of Inglot (2010), with probability (1 − 2e_2),
    max_{k⊄t} (R*_k − R*_u)/σ² > { √(n l_n c²) − √(2 log(r̄_n P_n^{r̄_n}/e_2)) }².
Because n l_n ≻ log r̄_n + r̄_n log P_n, we have max_{k⊄t} (R*_k − R*_u)/σ² > n l c²(1 + o(1)) [as printed]. Therefore, with probability (1 − 2e_2),
    max_{k⊄t} (K_2 P_n/r_n)^{d′} (R*_u/R*_k)^{n/2+a_0} ≤ exp{ −(n/2 + a_0) log[1 + l_n c² (1 + o(1))/(1 + ε_n)] + d′ log P_n − d′ log r_n + d′ log K_2 }.
Since n l_n ≻ log P_n + log K_2, we conclude that max_{k⊄t} [R*_u/R*_k]^{n/2+a_0} = o_p{(r_n/K_2 P_n)^{d′}}.
In summary, we have max_{k≠t} π(k|D_n)/π(t|D_n) →_p 0.    □
This theorem implies that the true model t can be identified asymptotically by just finding out the MAP model under the posterior (7) of the main text. Regarding the eigen-structure condition (22) and the choice of V_ξ, we have the following remarks:
• It is worth noting that the eigenvalue condition (22) is hardly satisfied, although similar conditions have been used in the literature, see e.g., Johnson and Rossel (2012). A feasible condition can be as follows: There exist two sequences {l_n} and {l′_n} and a constant C such that for any model |ζ| = r̄_n + |t|,
    Pr{ n l_n > ch′_1(X_ζ^T X_ζ) or ch_1(X_ζ^T X_ζ) > n l′_n } < e^{−nC}.    (26)
Since the condition r̄_n ln P_n ≺ n holds, (26) implies that, for sufficiently large n,
    Pr{ ∃ |ζ| = r̄_n + |t|, n l > ch′_1(X_ζ^T X_ζ) or ch_1(X_ζ^T X_ζ) > n l′ } < e^{−nC/2}  [subscripts of l, l′ as printed].
Hence, if (22) is replaced by (26), Theorem S still holds. The condition (26) does not require the eigenvalues of the sample covariance matrix to be bounded, but restricts the tail distribution of eigenvalues. Hence, it is more reasonable and acceptable."""),
    "SS-P16": ("16–17", "remarks; Corollary S_1; §3.2 and Lemma S_2", """• The condition (26) is similar to but somewhat weaker than the concentration condition used in Fan and Lv (2008). The concentration condition constrains the eigen-structure of any n × p̃ subdata matrix for any p̃ > cn for some constant c, while the condition (26) only constrains the eigen-structure of n × (r̄_n + |t|) subdata matrix. In particular, condition (26) holds when x follows a Gaussian process, and the eigenvalues of Var(x) are bounded by l_n and l′_n (see Appendix A.7 of Fan and Lv (2008)). For a further study of the limit behavior of the spectral structure, see e.g. Silverstein (1985), Bai and Yin (1993), and Ledoux (2007).
• Choosing V_ξ^{−1} as a function of the sample covariance matrix makes use of the data information in the prior, and as a result, a slightly weaker condition is required for the consistency of variable selection. It follows from the theory of least square regression, a natural choice of V_ξ^{−1} is V_ξ^{−1} = X_ξ^T X_ξ/n. However, for binary data, even if n > |ξ|, one may still encounter the problem of singularity of X_ξ^T X_ξ. To address this issue, we set V_ξ^{−1} = (X_ξ^T X_ξ + τI)/n for some small τ in our simulations. It can be shown that this choice leads to the same consistency result as with the sample covariance matrix (see Lemma A.2 of the Appendix). This choice also automatically meets the eigenvalue condition of V_ξ in Corollary 2.1 of the main text for a standardized dataset.
Corollary S_1 Consider a linear regression with a sparse true model t. Assume that P_n < n^{κ log n} for some κ ∈ (0, 1/4), and the prior in Section 2.1.1 of the main text is used with V_ξ^{−1} = X_ξ^T X_ξ/n or V_ξ^{−1} = X_ξ^T X_ξ/n + τI/n. Let
    r̄_n ≺ log^{k_1}(n), or r̄_n ≺ n^q,
for some k_1 > 0 or q ≤ 1/2 − √κ, and
    l′_n = l_n^{−1} = √n/log^{k_2}(n),
for some k_2 > 0. Then the consistency of the MAP model holds.
3.2 Search for the MAP model
To search for the MAP model, a straightforward algorithm is simulated annealing (Kirkpatrick et al., 1983). However, as known by many people, simulated annealing can get trapped into a local mode due to the use of a non-logarithmic cooling schedule. Since SAMC has been applied to simulate from the posterior distribution for estimating the marginal inclusion probability, it is natural to use the sampled highest posterior probability model to estimate the MAP model. It follows from the following lemma that this estimator is consistent. In the context of MAP model searching, the function g(·) in Lemma S_2 can be interpreted as the posterior probability of a subset model.
Lemma S_2 Let X, X_1, …, X_n denote a sequence of random variables drawn from a sample space 𝒳. Let g : 𝒳 → R be a Borel function. Suppose that g is continuous with P_X probability 1, where P_X is the probability measure induced by the random variable X.
[p. 17] (i) If X_n ⇒ X, then g(X_n) ⇒ g(X), where ⇒ denotes convergences in distribution (Serfling, 1980, p.24).
(ii) If there exists a subsequence {X_{n_k}} such that {g(X_{n_k})} are mutually independent, then max_n g(X_n) → g* = sup{x : Pr(g(X) > x) > 0} in probability.
Proof. Part (i) is a partial restatement of a Theorem in Serfling (1980, p.24). Part (ii) can be proved as follows. … which concludes the proof of part (ii).    □"""),
}
SUPP_INDEX = """[Preparer's note, not a quotation.] The supplement has 20 pages: §1 proofs of the main results (pp. 1–8: Theorems
2.1–2.4, Lemmas 1.1, 1.2), §2 the SAMC algorithm and its implementation (pp. 8–13), §3 the MAP model (pp. 13–17:
Theorem S, Corollary S_1, Lemma S_2), §4 a simulation comparison with the horseshoe prior (pp. 17–19), references
(pp. 19–20). It numbers the main-text results as Theorems 2.1–2.4 and refers to conditions (A_1), (A_2), (B_1) without
defining these labels; matching by content, Theorem 2.3 is the main text's Theorem 3 (same conclusion, p. 956) and
(B_1) is used as the main text's Condition 3 (p. 955) is. "Lemma A.2 of the Appendix" (p. 16) is not in the
supplement. Statements about what the sampler returns: the preparer searched the text of all 20 pages for "converg"
and "consisten" and read each hit; those on the sampler are on pp. 9–10, 12–13, 16–17 and are all excerpted above."""


def sl_main(*ids):
    out = []
    for k in ids:
        page, lab, text = SL[k]
        out.append(f"Song & Liang (2015), p. {page}, {lab} [{k}; transcribed from p. {page} image]:\n```\n{text}\n```")
    return "\n".join(out)


def sl_supp(*ids):
    out = []
    for k in ids:
        page, lab, text = SUPP[k]
        imgs = " and ".join(f"supp p. {x}" for x in page.split("–")) + (" images" if "–" in page else " image")
        out.append(f"Song & Liang (2015), on-line supplement, supp p. {page}, {lab} [{k}; transcribed from {imgs}]:"
                   f"\n```\n{text}\n```")
    return "\n".join(out)


# ---------------------------------------------------------------- material ----------------------------------------
def statements():
    return "\n".join([
        "Standing assumptions (S1)–(S3) of the reader versions:", q("RV", (28, 31)),
        "Reader statement of Theorem 1 and Theorem 1′ (fixed design; row 1.1):", q("RV", (103, 134)),
        "Reader statement of Theorem 2 (Gaussian rows; row 1.2), with its remark:", q("RV", (269, 285)),
        "Reader statement of Theorem 6 (the coded method reports the model; row 3.1):", q("RV", (666, 697)),
        "Reader version of Theorem 9 (the posterior finds the distribution; row 2.1), its assumptions:", q("RV", (1031, 1042)),
        "Reader statement of Corollary 9C (the output of the sampler):", q("RV", (1081, 1099)),
        "Master: our posterior π (prior, standardisation, outputs) and the truth:", q("POST", (18, 34)),
        "Master Theorem 1 (fixed design), regime, hypotheses and conclusions 1–4:", q("POST", (63, 75), (80, 86)),
    ])


SL_MAIN_IDS = ["SL-M1", "SL-M3", "SL-P6", "SL-P7", "SL-H", "SL-T1", "SL-V", "SL-C1", "SL-T2", "SL-CO1", "SL-C3",
               "SL-C3S", "SL-T3", "SL-SAM"]
SUPP_IDS = ["SS-ORG", "SS-T23", "SS-P9", "SS-P10", "SS-P12", "SS-TS", "SS-P14", "SS-P15", "SS-P16"]
HDR = (293, 294)  # summary-table header of TRACK_B


# Items: (id, title, our text (a), SL passage ids (b), quotes of the verdicts under test (c), [(verdict id, claim)])
def items():
    return [
        ("item1", "B4: size of the nonzero coefficients",
         q("RV", (106, 106), (111, 112), (272, 273), (670, 671), (1042, 1042)),
         ["SL-M3", "SL-C3", "SL-T2", "SL-T3", "SS-T23", "SS-TS", "SS-P14", "SS-P15"],
         q("TB", (99, 109)) + q("TB", HDR, (298, 298)) + q("TB", (379, 380), (383, 383)) + au(49, 83)
         + q("WD", (16, 19)),
         [("B4.PROOFS", "\"same as the setting of their proofs\": their proofs treat the nonzero coefficients as "
                        "constants (supp pp. 5 and 15), so \"d(f*, f) ≥ ε_n\" needs β*_t bounded away from zero and the "
                        "proof of Theorem S uses c = min_{i∈t}|β*_i| as a constant (TRACK_B.md:104-107, :298, :383; "
                        "AUDIT.md:49, :83; WRITING_DELTA_v1.3.md:17-19)"),
          ("B4.STATED", "\"stronger than their statements, which give no size condition\": a coefficient of size 1/n "
                        "satisfies (4) and their stated conditions, violates ours and their conclusions; and our "
                        "fixed-design theorem allows signals down to √(log n/n), below their implicit level "
                        "(TRACK_B.md:101-108, :298; AUDIT.md:49; WRITING_DELTA_v1.3.md:17-19)")]),
        ("item2", "B5 and B6 against Theorem S",
         q("RV", (107, 110), (128, 131), (274, 276), (1040, 1041)) + q("POST", (68, 73)),
         ["SL-C3", "SL-C3S", "SL-T3", "SS-TS", "SS-P15", "SS-P16"],
         q("TB", (117, 121), (129, 133)) + q("TB", (147, 151), (154, 157)) + q("TB", HDR, (299, 300))
         + q("TB", (379, 380), (384, 385)) + au(47, 48) + q("WD", (20, 22)),
         [("B5.S", "B5 against Theorem S is \"not ordered\": ours is stronger only in asking a fixed level on bounded "
                   "sets, and weaker in having no upper bound, a floor of order 1/n on O(log n) columns and nothing on "
                   "larger sets (TRACK_B.md:129-132, :299, :384; AUDIT.md:47; WRITING_DELTA_v1.3.md:20-22)"),
          ("B6.S", "B6 against Theorem S is \"weaker\": their floor (22) covers every model of |t| + r̄_n columns, "
                   "null-only ones included, at a level l_n ≻ r̄_n log P_n / n far above ours, so \"additional on "
                   "null-only sets\" holds against their Theorem 3 only (TRACK_B.md:154-156, :300, :385; AUDIT.md:48)")]),
        ("item3", "What Song–Liang prove about their sampler's output",
         q("RV", (689, 697), (1088, 1099)),
         ["SL-T3", "SL-SAM", "SS-P9", "SS-P10", "SS-P12", "SS-P16"],
         q("TB", (367, 375)) + q("TB", (226, 229)) + q("TB", (379, 380), (389, 389)) + au(71)
         + q("WD", (26, 29)),
         [("SAMP.LABEL", "\"Song–Liang have a weaker counterpart, not none\": their statements on the sampler's output "
                         "are limits in the number of iterations N at fixed data (Lemma S_2 and a citation, supp "
                         "pp. 12–13, 16–17) (TRACK_B.md:367-373, :226-229, :389; AUDIT.md:71; "
                         "WRITING_DELTA_v1.3.md:26-29)"),
          ("SAMP.ABSENCE", "\"they prove nothing at a finite computational budget or jointly in n\" (TRACK_B.md:374; "
                           "AUDIT.md:71; WRITING_DELTA_v1.3.md:28-29)")]),
        ("item4", "The new headline sentence",
         "(our theorem statements: §1 above)\n",
         ["all of §2 and §3"],
         q("WD", (5, 14)) + "The same answer as worded in TRACK_B (context; the clauses on designs are not under test):\n"
         + q("TB", (14, 24)) + q("TB", (308, 312)),
         [("HEAD.ORDER", "\"Their assumptions are of the same kinds as Song–Liang's and are neither uniformly stronger "
                         "nor uniformly weaker\" (WRITING_DELTA_v1.3.md:8-9)"),
          ("HEAD.S", "\"Against their selection theorem (Theorem S of their supplement) we ask a narrower range of p "
                     "(n^A against n^{κ log n}) and a fixed eigenvalue floor on bounded sets; we ask less elsewhere: no "
                     "upper eigenvalue bound, only a 1/n-level floor on O(log n) columns and nothing on larger sets, no "
                     "tuning of the prior, and signals as small as √(log n/n) in the fixed-design theorem\" "
                     "(WRITING_DELTA_v1.3.md:9-12)"),
          ("HEAD.H", "\"Against their Hellinger theorems (1–2) we add the range of p, a c/n collinearity floor and a "
                     "row law\" (WRITING_DELTA_v1.3.md:12-13)"),
          ("HEAD.CONC", "\"Our conclusions are stronger\" (WRITING_DELTA_v1.3.md:13)")]),
        ("item5", "Theorem S against our cores 1 and 3 (TRACK_B §S)",
         "(our theorem statements and our posterior: §1 above)\n",
         ["SL-M1", "SL-M3", "SL-P6", "SL-P7", "SL-T1", "SL-T3", "SS-TS", "SS-P14", "SS-P15", "SS-P16"],
         q("TB", (340, 365)) + q("TB", (80, 82)) + au(52) + q("WD", (23, 25)) + "(The core 3 paragraph of §S, TRACK_B.md:367-375, is quoted under item3.)\n",
         [("S.QUOTE", "the audit's quotation of Theorem S, (26) and Corollary S_1 \"as printed\" "
                      "(TRACK_B.md:342-353) agrees with the supplement"),
          ("S.MODEL", "Model, sparsity: \"same\" (TRACK_B.md:359)"),
          ("S.PRIOR", "Prior: ours \"weaker (no condition on hyperparameters)\" (TRACK_B.md:360)"),
          ("S.DIM", "Dimension: ours \"stronger, by little\"; their condition 2 gives log P_n ≺ (log n)²/4 "
                    "(TRACK_B.md:361; TRACK_B.md:80-82 is the B2 wording)"),
          ("S.LOWER", "Lower eigenvalue bound: \"not ordered: stronger on bounded sets (fixed level), weaker on larger "
                      "sets\" (TRACK_B.md:362)"),
          ("S.UPPER", "Upper eigenvalue bound: ours \"weaker\" (none) (TRACK_B.md:363)"),
          ("S.SIGNAL", "Signal size: \"same as their implicit setting for fixed signals; weaker in Theorem 1\" "
                       "(TRACK_B.md:364)"),
          ("S.CONC", "Conclusion: ours \"stronger\", and \"ours implies (24)\" — 1 − π(S₀ | y) = O_P(√(log n/n)) "
                     "implies max_{k≠t} π(k | D_n)/π(t | D_n) →_p 0 (TRACK_B.md:365, :24; AUDIT.md:52; "
                     "WRITING_DELTA_v1.3.md:23-25)"),
          ("S.CORE3", "\"Theorem S adds no condition of the visibility or leakage kind\" (TRACK_B.md:375)")]),
    ]


# ---------------------------------------------------------------- prompts -----------------------------------------
SYSTEM = """You are a blind, independent referee. A research project on the asymptotic theory of a Bayesian variable-selection
method (Gaussian linear regression, p ≤ n^A, often p ≫ n) has written an audit that compares the hypotheses and
conclusions of its theorems with those of Song and Liang (2015, J. R. Statist. Soc. B 77, 947–972). After reading Song
and Liang's on-line supplement (its Theorem S on the posterior mode, its proofs, and its statements on the sampler), the
audit changed some comparison labels. Only those changed labels are under test here. You receive verbatim excerpts: the
project's theorem texts (file and line numbers), the Song–Liang passages (journal page, or supplement page "supp p.",
and display number), and the audit sentences under test. The audit's other reasoning and all earlier reviews are
deliberately withheld; status labels have been removed from the excerpts. Bracketed markers such as [H5-1] or [S1-F3]
are editorial tags; ignore them.

Judge only the texts given. Do not rely on your memory of Song–Liang or of any other paper. All results are asymptotic;
explicit constants in the hypotheses are conservative and not part of the judgement; finite-n behaviour is not a
defect. Clauses about the project's simulation designs are not under test.

Your job is to break each verdict listed in the task. For each one either REFUTE it or say NO FINDING:
- REFUTED needs a concrete reason: a counterexample, a misread or misquoted passage (wrong display, wrong page, a
  remark or a proof step read as a hypothesis, a sufficient condition read as the condition), or a quantifier or
  direction error (which statement implies which; for every / there exists; over which sets, sizes and sequences;
  fixed against vanishing levels; sample against population; one posterior against another; limits in n against
  limits in the number of sampler iterations). State it with exact references (our file:line, or Song–Liang page or
  supp page and display number).
- For a comparison label (same / stronger / weaker / not ordered / comparable / counterpart), check it in both
  directions against the texts given; one explicit case that contradicts the label is enough to refute it.
- For an absence claim ("no condition stated", "prove nothing at …"), decide from the texts given, including the
  preparer's index of the supplement.
- UNCLEAR is allowed only when the texts given cannot settle the verdict; then name the passage or fact you would need.
Do not report style, wording, presentation or possible improvements.

Output, in this order:
1. Findings only: for each REFUTED or UNCLEAR verdict, a short section headed by its verdict id with the problem, the
   exact references and the counterexample or the missing passage. Write nothing for a NO FINDING verdict.
2. Then exactly one line per verdict listed in the task, in the listed order, and nothing after the last one:
AUDIT2 <item>:<id> VERDICT=<NO-FINDING|REFUTED|UNCLEAR>"""


def render():
    its = items()
    vids = [f"{iid}:{vid}" for iid, *_rest in its for vid, _ in _rest[-1]]
    P = ["# AUDIT2 — the comparison labels changed after reading Song–Liang's supplement",
         "",
         "Material for a blind review. Every excerpt of ours is verbatim with its file and line numbers; Song–Liang",
         "passages carry the journal page (main text) or the supplement page (\"supp p.\") and the display number, and",
         "are transcriptions of the printed pages. Status labels have been replaced by [status omitted] or [review omitted].",
         "",
         "## 1. Our theorem statements (verbatim)", statements(),
         "", "## 2. Song–Liang (2015), main text (transcribed)", sl_main(*SL_MAIN_IDS),
         "", "## 3. Song–Liang (2015), on-line supplement (transcribed)", sl_supp(*SUPP_IDS), "", SUPP_INDEX,
         "", "## 4. Items under test"]
    for iid, title, ours, slids, quotes, verdicts in its:
        P += ["", f"### {iid} — {title}"]
        P += ["**(a) Our text.**", ours]
        P += ["**(b) Song–Liang passages** (in §2–§3 above): " + ", ".join(slids)]
        P += ["**(c) The audit's sentences under test (verbatim).**", quotes]
        P += ["**(d) Verdicts under test.**"]
        for vid, claim in verdicts:
            P += [f"- `{iid}:{vid}` — {claim}"]
    task = ["Break the comparison; findings only.",
            "",
            f"Verdicts to judge ({len(vids)}), in this order; return one machine line for each:"] + vids
    return "\n".join(P) + "\n", "\n".join(task) + "\n", vids


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "SYSTEM.md").write_text(SYSTEM + "\n", encoding="utf-8")
    ctx, task, vids = render()
    req_md = OUT / "REQ_audit2.md"
    req_md.write_text(ctx + "\n---\n\n## Task (sent as a separate block)\n\n" + task, encoding="utf-8")
    rel = req_md.relative_to(ROOT).as_posix()
    reqs, rows = [], []
    for s in range(1, SAMPLES + 1):
        cid = f"audit2-s{s}"
        reqs.append({"custom_id": cid, "file": rel, "claims": vids, "params": {
            "model": MODEL, "max_tokens": MAX_TOKENS, "output_config": {"effort": "high"}, "system": SYSTEM,
            "messages": [{"role": "user", "content": [
                {"type": "text", "text": ctx, "cache_control": {"type": "ephemeral"}},
                {"type": "text", "text": task}]}]}})
        rows.append((cid, "v1.3 label changes (items 1–5)", len(vids), ";".join(vids)))
    (OUT / "requests.json").write_text(json.dumps(reqs, ensure_ascii=False), encoding="utf-8")
    with open(OUT / "REQUESTS.tsv", "w", encoding="utf-8") as f:
        f.write("custom_id\tscope\tn_verdicts\tverdict_ids\n")
        for r in rows:
            f.write("\t".join(str(x) for x in r) + "\n")
    with open(OUT / "MANIFEST.tsv", "w", encoding="utf-8") as f:
        f.write("source\tpath\tcommit\tsha256\n")
        for k, (wt, rev, path) in SRC.items():
            f.write(f"{k}\t{path}\t{rev}\t{sha_bytes(raw(k))}\n")
        f.write(f"SL\t{SL_PDF}\tnot in git (excerpts only)\t{sha_bytes(SL_PDF.read_bytes())}\n")
        f.write(f"SUPP\t{SUPP_PDF}\tnot in git (excerpts only)\t{sha_bytes(SUPP_PDF.read_bytes())}\n")
        f.write(f"SYSTEM\tTheory_work/Wave3/API_AUDIT/audit2/SYSTEM.md\tbuilt\t{sha_bytes((SYSTEM + chr(10)).encode())}\n")
    chars = len(SYSTEM) + len(ctx) + len(task)
    tin1 = round(chars / 3.5)
    tin = tin1 * SAMPLES
    tout_exp, tout_max = 16000 * len(reqs), MAX_TOKENS * len(reqs)
    cin = tin * 4 / 1e6
    L = ["AUDIT2 token and cost estimate (OFFLINE ESTIMATE: tokens ≈ characters / 3.5; not a count).",
         "Exact input counts: `python Theory_work/Wave3/API_AUDIT/audit_batch.py count Theory_work/Wave3/API_AUDIT/audit2`.",
         f"Model {MODEL}, effort high, max_tokens {MAX_TOKENS}, {SAMPLES} samples of one request, {len(reqs)} requests.",
         "Batch rates for Claude Fable 5.2: input $4.00 / MTok, output $20.00 / MTok (half of $8 / $40).", "",
         "request\tchars\test. input tokens\tverdicts",
         f"audit2\t{chars}\t{tin1}\t{len(vids)}", "",
         f"total est. input tokens ({len(reqs)} requests, no cache credit): {tin}  -> ${cin:.2f}",
         f"output, expected (≈16k tokens per request incl. thinking): {tout_exp} -> ${tout_exp*20/1e6:.2f}",
         f"output, worst case (every request hits max_tokens {MAX_TOKENS}): {tout_max} -> ${tout_max*20/1e6:.2f}",
         f"TOTAL: expected ≈ ${cin + tout_exp*20/1e6:.2f}; worst case ≤ ${cin + tout_max*20/1e6:.2f} (HQ scope ≈ $5).",
         "Cache reads of the shared context (sample 2) are billed lower; not credited above.",
         "Note: `audit_batch.py wait` overwrites this file with the billed usage after the run; the estimate is "
         "repeated in README.md."]
    (OUT / "USAGE.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


def verdicts():
    """Parse results/*.md written by `audit_batch.py wait` (it only collects 'AUDIT ' lines) into AUDIT2_VERDICTS.tsv."""
    res = OUT / "results"
    rows = []
    for p in sorted(res.glob("audit2-*.md")):
        cid = p.stem
        for line in p.read_text(encoding="utf-8").splitlines():
            m = re.match(r"\s*`?AUDIT2 (item\d):(\S+?) VERDICT=(NO-FINDING|REFUTED|UNCLEAR)`?\s*$", line)
            if m:
                rows.append((cid, f"{m.group(1)}:{m.group(2)}", m.group(3)))
    expected = {(r["custom_id"], v) for r in json.loads((OUT / "requests.json").read_text(encoding="utf-8"))
                for v in r["claims"]}
    got = {(c, v) for c, v, _ in rows}
    with open(OUT / "AUDIT2_VERDICTS.tsv", "w", encoding="utf-8") as f:
        f.write("custom_id\tverdict_id\tresult\n")
        for r in sorted(rows):
            f.write("\t".join(r) + "\n")
        for c, v in sorted(expected - got):
            f.write(f"{c}\t{v}\tMISSING\n")
    print(f"{len(rows)} verdict lines; {len(expected - got)} missing -> {OUT / 'AUDIT2_VERDICTS.tsv'}")


if __name__ == "__main__":
    {"build": build, "verdicts": verdicts}[sys.argv[1]]()
