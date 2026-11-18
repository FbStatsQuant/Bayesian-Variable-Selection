"""Build AUDIT1: a blind Claude Fable 5.2 batch review of W3-AUDIT TRACK_B's Song–Liang comparisons and
inside/outside verdicts for core theorems 1–3 (HQ, 2026-11-16). No API call is made here.

  python Theory_work/Wave3/API_AUDIT/audit1_build.py build      # write audit1/{requests.json, REQ_core*.md, SYSTEM.md, ...}
  python Theory_work/Wave3/API_AUDIT/audit1_build.py verdicts   # after `audit_batch.py wait audit1`: parse AUDIT1 lines

Submission uses audit_batch.py unchanged (count / submit / wait <outdir>); see audit1/README.md.
Sources are read at pinned commits (git show), so a rebuild is byte-identical while the pins hold:
  W3-AUDIT worktree  @ 56dafbdd (TRACK_B.md, AUDIT.md v1.1; track_C/RESULTS.md, unchanged since 4f0f9a82)
  W3-READER worktree @ 7eb818e6 (READER_VERSIONS.md: the reader statements the dossiers compare)
  this worktree      @ SRC_REV  (master STATEMENT.md files and design sources)
Song–Liang (2015) passages are transcribed below from the page images (the PDF's text layer drops ≺, ≻, ≠, ε and
other symbols); the PDF itself is never copied.
"""
import hashlib, json, re, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUT = HERE / "audit1"
WT_AUDIT = Path("/home/fb31/BVS-wt/W3-AUDIT")
WT_READER = Path("/home/fb31/BVS-wt/W3-READER")
REV_AUDIT = "56dafbdd"
REV_READER = "7eb818e6"
SRC_REV = "e8b5351c"  # dept/theory at build time (statement files identical to main eb6f12b3 for the paths used)
P1M = Path("/home/fb31/Bayesian-Variable-Selection/Docs/Experiments/P1M/EXPERIMENT_PLAN.md")  # untracked
SL_PDF = Path("/home/fb31/SMC_Theory_Department/refs/Song_Liang_2015.pdf")  # not in git
MODEL = "claude-fable-5-2"
MAX_TOKENS = 32000
SAMPLES = 2

SRC = {  # key -> (worktree, rev, path); rev None = file on disk (untracked)
    "TB": (WT_AUDIT, REV_AUDIT, "Theory_work/Wave3/W3-AUDIT/TRACK_B.md"),
    "AU": (WT_AUDIT, REV_AUDIT, "Theory_work/Wave3/W3-AUDIT/AUDIT.md"),
    "TC": (WT_AUDIT, REV_AUDIT, "Theory_work/Wave3/W3-AUDIT/track_C/RESULTS.md"),
    "RV": (WT_READER, REV_READER, "Theory_work/Wave3/W3-READER/READER_VERSIONS.md"),
    "POST": (ROOT, SRC_REV, "Theory_work/Wave3/W3-POST/STATEMENT.md"),
    "POST2": (ROOT, SRC_REV, "Theory_work/Wave3/W3-POST2/STATEMENT.md"),
    "PSHARP": (ROOT, SRC_REV, "Theory_work/Wave3/W3-PSHARP/STATEMENT.md"),
    "DIST": (ROOT, SRC_REV, "Theory_work/Wave3/W3-DIST/STATEMENT.md"),
    "RM": (ROOT, SRC_REV, "Theory_work/Wave3/W3-RM/STATEMENT.md"),
    "RM2": (ROOT, SRC_REV, "Theory_work/Wave3/W3-RM2/STATEMENT.md"),
    "GEN": (ROOT, SRC_REV, "Scripts/Data_generators/gen_dev_data.R"),
    "RERUN": (ROOT, SRC_REV, "Theory_work/Pause_2026-11/RERUN_SPEC.md"),
    "P6": (ROOT, SRC_REV, "Theory_work/Wave3/W3-P6/DESIGN.md"),
    "P1M": (None, None, str(P1M)),
}
_cache = {}


def raw(key):
    if key not in _cache:
        wt, rev, path = SRC[key]
        if rev is None:
            _cache[key] = Path(path).read_bytes()
        else:
            _cache[key] = subprocess.run(["git", "-C", str(wt), "show", f"{rev}:{path}"], capture_output=True,
                                         check=True).stdout
    return _cache[key]


def label(key):
    wt, rev, path = SRC[key]
    if rev is None:
        return f"`{path}` (untracked file)"
    return f"`{path}` @ {rev}"


# ---- status / score words are stripped from every excerpt (as audit_batch does: judge the text, not the label) ----
SCRUB = [
    (r"This description of the output was code-checked by independent reviewers\. ", ""),
    (r"\(HQ ruling, 11-16\)\. Track C results \(internal\) will be cited in the \"Designs\" lines when they land\.", ""),
    (r"\s*[—–]?\s*checked \(AUDITCALC_check_opus\.md[^)]*\)", ""),
    (r"; checked, AUDITCALC_check_opus\.md[^)]*\)", ")"),
    (r"CODE-CHECKED[^\"]*", "[status omitted]"),
    (r"\"PROVED[^\"]*\"", "[status omitted]"),
    (r"PROVED-CHECKED[^;,.)\]]*", "[status omitted]"),
    (r"PROVED(?: \(by this seat, unchecked\))?", "[status omitted]"),
    (r"VERIFIED[^;,.)\]]*", "[status omitted]"),
    (r"council[^;,.)\]]*", "[review omitted]"),
    (r"\bPASS\b", "[review omitted]"),
]
BANNED = re.compile(r"AUDITCALC|checked \(|PROVED|CHECKED|[Cc]ouncil|\bPASS\b|VERIFIED|\bOpus\b|\bFable\b|\bAstra\b|\bseat\b")


def scrub(t):
    for a, b in SCRUB:
        t = re.sub(a, b, t)
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


def au(*spans, note=""):
    """AUDIT.md table rows: only the cells 'Assumption' and 'Song–Liang (2015)' (columns 1 and 4) are quoted verbatim;
    the 'Track' and 'Status or dossier' cells are withheld (blind review). Non-table lines are quoted whole."""
    parts = []
    for a, b in spans:
        out = []
        for i, t in lines("AU", a, b):
            cells = re.split(r"(?<!\\)\|", t.strip())
            if t.startswith("|") and len(cells) >= 6:
                c = [x.strip() for x in cells[1:-1]]
                if set(c[0]) <= set("-: "):
                    continue
                t = f"| {c[0]} | {c[3]} |"
            out.append(f"{i:5d}| {t}")
        parts.append(f"{label('AU')}, lines {a}–{b}, cells 'Assumption' and 'Song–Liang (2015)' only{note}:\n```\n"
                     + scrub("\n".join(out)) + "\n```")
    return "\n".join(parts) + "\n"


# ---- Song & Liang (2015), J. R. Statist. Soc. B 77(5), 947–972: passages, transcribed from the page images ----
# Every passage was checked against the page image (pdftoppm -r 110, displays re-read at -r 200); wording was also
# compared with `pdftotext -layout`. Ellipses "…" mark omitted text inside a passage. Notation as printed.
SL = {
    "SL-M1": (947, "§1, model (1)", """Consider the problem of variable selection for the linear regression model:
    y = Xβ* + ε,    (1)
where y = (y_1, …, y_n)^T ∈ ℝ^n is the response vector, n is the sample size, X = (x_1, …, x_{P_n}) ∈ ℝ^{n×P_n} is the design matrix, P_n is the number of explanatory variables (which are also known as predictors), β* is the vector of unknown regression coefficients and ε = (ε_1, …, ε_n)^T ∼ N_n(0, σ*²) is Gaussian random error. In this paper, we use the bold letter x_i to denote an n-vector realization of the ith predictor. The subscript n in P_n means that P_n is a non-decreasing function of n. … In this paper, our study of variable selection will focus on the scenario P_n ≫ n, i.e. the column dimension of X is ultrahigh."""),
    "SL-M2": (950, "§2.1, density (2)", """Let D_n = {y; x_1, …, x_{P_n}} denote a data set of n observations drawn from model (1). Let x = (x_1, …, x_{P_n})^T denote a generic observation of the P_n predictors, and let y denote a generic observation of the response variable corresponding to x. Let ν_x denote the probability measure of x. Then the true probability density of (y, x) is given by
    f*(y, x) dx dy = (1/(√(2π) σ*)) exp{−(y − x^Tβ*)²/(2σ*²)} ν_x(dx) dy = φ(y; x^Tβ*, σ*) ν_x(dx) dy,    (2)
where φ(·; μ, σ) denotes a Gaussian density function with mean μ and standard deviation σ."""),
    "SL-M3": (950, "§2.1, growth of P_n; sparsity conditions (3) and (4)", """As in conventional studies of high dimensional variable selection, we consider the asymptotics of the SAM approach under the assumption that P_n increases as n increases. To be specific, we assume that P_n ≻ n^θ for some θ > 0, where b_n ≻ a_n means lim_{n→∞}(a_n/b_n) = 0. In addition, we assume that the true model is sparse. Two sparseness conditions are considered in this paper. One states that most components of β* are very small such that
    lim_{n→∞} Σ_{j=1}^{P_n} |β*_j| < ∞,    (3)
where β*_j denotes the jth entry of β*. The other one is stronger but more usual, which requires that most components of β* are 0 such that
    lim_{n→∞} Σ_{j=1}^{P_n} 1{β*_j ≠ 0} < ∞.    (4)
Let ξ ⊂ {1, …, P_n} denote a subset model, which includes the indices of all selected predictors. Let |ξ| denote the number of predictors included in ξ. Thus, the strict sparsity condition (4) implies that the true model t = {i : β*_i ≠ 0, 1 ≤ i ≤ P_n} has a finite model size."""),
    "SL-P6": (951, "§2.1.1, prior (6)", """For the model ξ, we assume that each predictor has a prior probability λ_n = r_n/P_n, independent of other predictors, to be included in the model ξ. Further, we impose a constraint on the model size such that |ξ| ≤ r̄_n, where the upper bound r̄_n is prespecified. Then the prior probability of ξ can be expressed as
    π(ξ) ∝ λ_n^{|ξ|} (1 − λ_n)^{P_n−|ξ|} I(|ξ| ≤ r̄_n).    (6)
… We let the variance σ² be subject to an inverse gamma prior distribution with the hyperparameters a_0 and b_0, i.e. σ² ∼ IG(a_0, b_0). Conditioned on the model ξ and σ², we let β_ξ be subject to a Gaussian prior:
    β_ξ | ξ, σ² ∼ N_{|ξ|}(0, σ² V_ξ),
where V_ξ is a positive definite matrix depending on ξ. … In this paper, we assume that λ_n → 0 as P_n → ∞, which corresponds to condition (13) in theorem 1."""),
    "SL-H": (952, "§2.1.2, Hellinger distance; eigenvalue notation; B(r_n), B̃_n, Δ(p)", """In what follows, we study the asymptotics of the posterior distribution with respect to the Hellinger distance under appropriate conditions of r_n, r̄_n and V_ξ. For two density functions f_1(x, y) and f_2(x, y), the Hellinger distance is defined as
    d(f_1, f_2) = √( ∫∫ {f_1^{1/2}(x, y) − f_2^{1/2}(x, y)}² dx dy ).
For a matrix Σ, we let ch_i(Σ) denote the ith largest eigenvalue, and let ch′_i(Σ) denote the ith smallest eigenvalue. Define B(r_n) = sup_{ξ:|ξ|=r_n} ch_1(V_ξ^{−1}), B̄(r_n) = sup_{ξ:|ξ|=r_n} ch_1(V_ξ), B̃_n = sup_{ξ:|ξ|≤r̄_n} ch_1(V_ξ) and Δ(p) = inf_{ξ:|ξ|=p} Σ_{i∉ξ} |β*_i|.
Theorem 1 follows from Jiang (2007). Here we consider the simple situation that all predictors have been standardized and uniformly bounded, and the sparsity condition (3) holds."""),
    "SL-T1": (952, "Theorem 1 and conditions (8)–(15)", """Theorem 1 (posterior consistency). Assume that the data set D_n is drawn from model (1) and all predictors |x_i| ≤ 1. If there is a sequence {ε_n} ∈ (0, 1) such that nε_n² ≻ 1, and the following conditions hold,
    Δ(r_n) ≺ ε_n,    (8)
    r̄_n ln(1/ε_n²) ≺ nε_n²,    (9)
    r̄_n ln(P_n) ≺ nε_n²,    (10)
    r̄_n ln(nε_n² B̃_n) ≺ nε_n²,    (11)
    1 ≤ r_n ≤ r̄_n < P_n,    (12)
    r_n ≺ P_n,    (13)
    B(r_n) ≺ nε_n²,    (14)
then the posterior consistency holds, i.e. there is a constant c_1 > 0 such that
    P*[π{d(f, f*) > ε_n | D_n} > exp(−c_1 nε_n²)] < exp(−c_1 nε_n²),    (15)
for sufficiently large n, where the Hellinger distance is
    d²(f, f*) = ∫∫ |φ^{1/2}(y; x^Tβ*, σ*) − φ^{1/2}(y; x^Tβ, σ)|² ν_x(dx) dy,
f* is as defined in expression (2), f is the density function for a model simulated from the posterior and P* denotes the probability measure of data generation."""),
    "SL-V": (953, "choices of V_ξ; 'ridge prior'", """The validity of this theorem depends on the choice of the prior covariance matrix V_ξ or, more precisely, the largest eigenvalues of V_ξ and V_ξ^{−1}. For most choices of V_ξ, B(r_n) ≤ B r_n^v and B̃_n ≤ B r_n^v hold for some positive constants B and v. For example, if V_ξ = c I_{|ξ|}, where I_p is an identity matrix of order p, then both B(r_n) and B̃_n are constants. One can also set V_ξ^{−1} = c E(x_ξ^T x_ξ) as in Zellner (1986) and Liang et al. (2008), where the expectation is replaced by its sample empirical estimator. If all x_i s are standardized with zero mean and equal variance, then B(r_n) ≤ r_n. Furthermore, if x_i has some specific covariance structure, then B̃_n can be shown to be bounded. For example, if all pairwise covariances cov(x_i, x_j) = ρ ∈ (0, 1), then B̃_n = 1 − ρ; if x_i is generated from a finite order auto-regressive or moving average model without root for the characteristic polynomial on the unit circle, then B̃_n is also bounded by some constant (Bickel and Levina, 2004). In general, for standardized x_i s, we can choose a 'ridge prior' as suggested by Gupta and Ibrahim (2009): let V_ξ^{−1} = E(x_ξ^T x_ξ) + c_n I_{|ξ|}; then B(r_n) ≤ r_n + c_n and B̃_n ≤ c_n^{−1}, where c_n is proportional to 1/n, i.e. c_n ∝ n^{−1}."""),
    "SL-C1": (953, "Condition 1 and the two sufficient cases", """Theorem 1 assumes that all the predictors are uniformly bounded. However, this condition might not be satisfied for continuous predictors. In what follows, we relax this condition.
Condition 1. There are some constants M > 0 and δ > 0 such that for any subvector of x, (x_{j_1}, …, x_{j_r})^T with 1 ≤ j_1 < … < j_r ≤ P_n, r ≤ r̄_n, and |a_i| ≤ δ for i = 1, …, r, we have
    E[ exp{ ( Σ_{i=1}^r a_i x_{j_i} / r )² } ] ≤ exp(M),
where the expectation is taken with respect to the distribution of the random variables x_{j_i}.
Condition 1 controls the tail distribution of x such that the marginal distribution of y does not change dramatically in the sense of d_1-divergence (which is defined in the on-line supplementary material) with respect to the change of β. If x has a heavy tail distribution, the prior information around f* will be too weak to induce good posterior asymptotics. If all the variables are bounded by some constant m, as assumed in theorem 1, then
    E[ exp{ ( Σ_{i=1}^r a_i x_{j_i} / r )² } ] ≤ exp(δ² m)
and thus condition 1 holds. If x follows a Gaussian process with zero mean and var(x_i) = 1, then (Σ_{i=1}^r a_i x_{j_i})² follows the sχ²_1-distribution, where the scale s ≤ δ² r². Therefore, by the moment-generating function of the χ²_1-distribution,
    E[ exp{ ( Σ_{i=1}^r a_i x_{j_i} )² / r² } ] ≤ (1 − 2δ²)^{−1/2},
condition 1 holds."""),
    "SL-T2": (953, "Theorem 2 (pp. 953–954, with the note on (8))", """Theorem 2. Assume that the data set D_n is generated from model (1) and all the predictors satisfy condition 1. Given a sequence {ε_n}, ε_n → 0, and nε_n² → ∞, if the conditions (9)–(14) of theorem 1 hold, the model is strictly sparse, i.e. condition (4) holds, and r_n ≻ 1, then the posterior consistency still holds, i.e. there is a constant c_1 > 0 such that, for sufficiently large n,
    P*[π{d(f, f*) > ε_n | D_n} > exp(−c_1 nε_n²)] < exp(−c_1 nε_n²).
Note that condition (8) of theorem 1 is redundant here as, for large n, r_n > |t| and Δ(r_n) = 0 hold under the sparseness condition (4). [the last words, from 'hold under', are on p. 954]"""),
    "SL-CO1": (954, "Corollary 1", """Corollary 1. Consider a strict sparse model, i.e. condition (4) holds. Suppose that P_n < exp(Cn^α) for some α ∈ (0, 1), and the prior specification in Section 2.1.1 is used such that B(r_n) ≤ B r_n^v and B̃_n ≤ B n^v for some positive constants B and v. Take
    r_n < r̄_n ≺ log^k(n),
or
    r_n < r̄_n ≺ n^q,
for some k > 0 or some 0 < q < min{1 − α, 1/v}. Then the convergence rate in theorem 2 can be taken as
    ε_n = O{n^{−(1−α)/2} log^{k/2}(n)},
or
    ε_n = O(n^{−(min{1−α−q, 1−vq})/2})."""),
    "SL-C2": (954, "§2.1.3, Condition 2 and result (16)", """Condition 2. There are some constants M > 0 and δ > 0 such that, for any subvector of x, (x_{j_1}, …, x_{j_r})^T with 1 ≤ j_1 < … < j_r ≤ P_n, r ≤ r̄_n, and |a_i| ≤ δ for i = 1, …, r, we have
    E( Σ_{i=1}^r a_i x_{j_i} / r )² ≤ M.
Condition 2 imposes conditions on only the second moments of predictors. If all predictors have uniformly bounded second moments, then condition 2 holds. It is shown in the on-line supplementary material that, if condition 2 holds, a slightly weaker result of theorem 2 can be obtained as follows:
    lim_{n→∞} P*[π{d(f, f*) > ε_n | D_n} > exp(−c_1 nε_n²)] = 0.    (16)"""),
    "SL-C3": (955, "§2.2, marginal inclusion probability; Condition 3", """Let q_j denote the marginal inclusion probability of the predictor x_j, which is given by
    q_j = π(j ∈ ξ | D_n) = Σ_{ξ∈{ξ̃: j∈ξ̃}} π(ξ | D_n).
… Therefore, to select true predictors consistently, it is necessary to control the severeness of multicollinearity. For this purpose, we introduce the following identifiability condition which controls the severeness of multicollinearity through the sequence {ε_n}.
Condition 3. A predictor x_k is said to be identifiable among all other predictors, if, for any 1 ≤ j_1, …, j_{r̄_n} ≤ P_n (j_i ≠ k for all i) and b_i ∈ ℝ,
    E[ exp{ −( x_k + Σ_{i=1}^{r̄_n} b_i x_{j_i} )² } ] ≤ 1 − δ_n,    δ_n ≻ ε_n²,
where x_l denotes a generic observation of the predictor x_l.
This condition states that, if a predictor x_k is identifiable, then there does not exist a linear combination of other predictors in X which can mimic it."""),
    "SL-C3S": (955, "sufficient forms of Condition 3 (pp. 955–956)", """If all the predictors have mean 0 and are bounded with |x_i| ≤ 1, then
    E[ exp{ −( x_k + Σ_{i=1}^{r̄_n} b_i x_{j_i} )² } ] ≤ E[ 1 − ( 1 − exp{ −(1 + Σ_i |b_i|)² } ) / (1 + Σ_i |b_i|)² · ( x_k + Σ_i b_i x_{j_i} )² ]
        ≤ 1 − {1 − exp(−1)} var( x_k + Σ_i b_i x_{j_i} ) / (1 + Σ |b_i|)²
        ≤ 1 − (1 − exp(−1))/(r̄_n + 1) · ch′_1{var(x̃)},
where x̃ = (x_k, x_{j_1}, …, x_{j_{r̄_n}})^T, and ch′_1{var(x̃)} is the smallest eigenvalue of the covariance matrix of x̃. Hence, if ch′_1{var(x̃)} ≻ r̄_n ε_n² for any choice of x̃, x_t is identifiable. Furthermore, if ch′_1{var(x)} ≻ r̄_n ε_n², then all the predictors are identifiable, where x = (x_1, …, x_{P_n})^T denotes a generic observation of all predictors.
If all the predictors follow the standard normal distribution, by the moment-generating function of the χ²-distribution, we have
    E[exp{−(x_k + Σ b_i x_{j_i})²}] = { 1 + 2 var( x_k + Σ_i b_i x_{j_i} ) }^{−1/2} < max{ 0.5, 1 − var( x_k + Σ_i b_i x_{j_i} )/8 }.
Thus, if var(x_k + Σ_i b_i x_{j_i}) ≻ ε_n², then the identifiability condition is satisfied. Since [p. 956]
    var( x_k + Σ_i b_i x_{j_i} ) ≥ var(x_k | x̃∖x_k) ≥ ch′_1{var(x̃)} ≥ ch′_1{var(x)},
by the same arguments, all predictors are identifiable if ch′_1{var(x)} ≻ ε_n². Further, it can be shown (in the proof of theorem 3) that, if a true predictor x_t is identifiable, then d(f*, f) ≥ ε_n for any density f that does not select x_t. Therefore, we have the following sure screening property."""),
    "SL-T3": (956, "Theorem 3 (sure screening) and the paragraphs after it", """Theorem 3 (sure screening). Assume that all the conditions of theorem 2 hold. If a true predictor x_t (t ∈ t) is identifiable, then P*[π{t ∈ ξ | D_n} < 1 − exp(−c_1 nε_n²)] < exp(−c_1 nε_n²), where ξ denotes a model sampled from the posterior distribution. Furthermore, if condition 2 holds, then the weaker convergence holds: lim_n P*[π{t ∈ ξ | D_n} < 1 − exp(−c_1 nε_n²)] = 0.
The proof of theorem 3 can be found in the on-line supplementary material. Let ξ_q = {i : 1 ≤ i ≤ P_n, q_i > q} denote a model including all the predictors with the marginal inclusion probability greater than a threshold value of q ∈ (0, 1). Then it follows from theorem 3 that π(t ⊂ ξ_q) →^p 1 if all true predictors are identifiable. … Theorem S in the on-line supplementary material establishes the consistency of MAP models. Thus, we have two criteria for variable selection, by either marginal inclusion probabilities or the MAP model. Although theorem 3 states only the sure screening property (the sensitivity is asymptotically 1, but the specificity is not controlled), we suggest the use of marginal inclusion probabilities as the criterion for variable selection."""),
    "SL-MIS": (956, "§2.3 (pp. 956–957): subset model, (17), Condition 4, Theorem 4, β_0, Corollary 2", """Let D_n^s = {y, X_s} denote a fixed subset of observations, where s ⊂ {1, 2, …, P_n} and X_s contains only s = |s| < P_n predictors with the indices belonging to s. Assume that X_s does not include all of the true predictors of model (1). Therefore, the model
    y = X_s β_s + ε
is misspecified. … Let P_s denote a set of parameterized densities for all possible models formed with X_s. It is obvious that f* ∉ P_s. Let f_0 denote the minimization point of the Kullback–Leibler divergence in P_s, i.e.
    f_0 = arg min_{f∈P_s} ∫ ln(f*/f) f*.    (17)
… [p. 957] Condition 4. There is a constant δ > 0 such that for any a = (a_1, …, a_s)^T ∈ ℝ^s, with |a_i| ≤ δ for i = 1, …, s, we have
    E{(a^T x_s)²} < ∞,
where x_s denote a generic observation of the predictors included in X_s.
Theorem 4. (posterior consistency for misspecified models). Assume that condition 4 holds for a given subset s. Under the prior setting as described above, for any ε > 0,
    π[{f ∈ P_s : d(f_0, f) > ε} | D_n^s] → 0,    almost surely,    (18)
as n → ∞, where f_0 is as defined in equation (17), and f is a parameterized density proposed from posterior.
It follows from lemma 1.2 (in the on-line supplementary material) that f_0 = φ(y; β_0^T x_s, σ_0) ν(x_s), where ν(x_s) denotes the probability measure of x_s, and β_0 is given by
    β_0 = arg min_{β_s} E(β_s^T x_s − β*^T x)²,
i.e. β_0^T x_s is the projection of β*^T x. Let s̃ denote the subset of s corresponding to non-zero entries of β_0. Following the proof of theorem 3, we have the following corollary.
Corollary 2. Assume that the conditions of theorem 4 hold. If x_s does not have exact multicollinearity between variables, i.e. there does not exist a non-zero vector a ∈ ℝ^s such that P(a^T x_s = 0) = 1, then for the posterior probability of model ξ, conditioned on the subset D_n^s, we have
    π(s̃ ⊂ ξ | D_n^s) →^p 1."""),
    "SL-C5": (957, "eq. (19); Condition 5 and remark (a) (pp. 957–958)", """Corollary 2 implies that the marginal inclusion probability criterion is still applicable for selection of predictors in X_s. For any true predictor x_t with t ∈ t ∩ s, it will be asymptotically selected under this criterion if and only if β_{0,t} ≠ 0, where β_{0,t} is the entry of β_0 corresponding to x_t. Let y denote a generic observation of the response variable, let x_t denote a generic observation of the true predictors and let β*_t denote the regression coefficient vector of the true predictors. Since
    β_0 = Σ_s^{−1} Σ_{s,t} β*_t = Σ_s^{−1} cov(x_s, y),    (19)
where Σ_s = var(x_s) and Σ_{s,t} = cov(x_s, x_t), s̃ is determined by the correlation structure of x_s and x_t and the value of the true regression coefficients. However, when t ⊄ s, it is unclear whether β_{0,t} is exactly 0 or not. Following from equation (19), if cov(x_s, y) ≠ 0, then β_0 ≠ 0 and thus at least one predictor in s will be selected according to the marginal inclusion probability criterion. This motivates us to propose an iterative variable selection method for the subset data, provided that the following condition holds.
[p. 958] Condition 5. |cov(x_t, y)| > 0 for any true predictor x_t.
The iterative variable selection method can be described as follows: first select predictors from X_s based on the marginal inclusion probabilities estimated from the posterior π(ξ | D_n^s); denote the set of unselected predictors by X_{s′}, and then select predictors again from X_{s′} based on the marginal inclusion probabilities estimated from the posterior π(ξ | y, X_{s′}); keep running the iterative procedure until no predictors can be selected. Denote all the selected predictors by X_{s̃}. Under assumption 5, this procedure ensures that all true predictors that are contained in X_s will be selected.
There are a few remarks on this iterative procedure.
(a) Other than true predictors, how many other predictors will be selected? Generally speaking, all the predictors that are correlated with X_t will be selected, because they are correlated with y, where X_t denotes the set of all true predictors in D_n. This means that, if all the predictors are linearly correlated, it is futile to apply this iterative procedure, as all the predictors will be selected. The rationale underlying the SAM strategy lies in the belief that, for a big data set, there are only a small proportion of predictors that are linearly correlated with X_t. It is easy to show that if there are p_n predictors correlated with the true predictor X_t, p_n ≺ P_n, then there are at most c p_n predictors to be selected into X_{s̃} for some constant c."""),
    "SL-SAM": (959, "§3.1 (SAM steps) and §3.2 (sampler)", """3.1. Split-and-merge approach
Based on the priors given in Section 2, the SAM approach can be summarized as follows.
(a) Split P_n predictors into K_n groups, s_1, …, s_{K_n}, with max_{i=1,…,K_n} |s_i| ≤ s for a prespecified value of s.
(b) Stage 1: apply the iterative procedure, proposed in Section 2.3, to select predictors from each subset D_n^{s_i} = {y, X_{s_i}}, i = 1, …, K_n, at an FDR level of α_1. At each iteration, the Bayesian variable selection is subject to the prior setting π(σ) ∼ IG(a_0, b_0), π(ξ) = λ_s^{|ξ|}(1 − λ_s)^{|s|−|ξ|} I(|ξ| ≤ s̄) and π(β_ξ | ξ, σ) ∼ N{0, σ²(X_ξ^T X_ξ + τI)/n}, where s̄ denotes the upper bound of the size of the models that are considered for each subset of data. Let s̃_1, …, s̃_{K_n} denote the sets of indices of the selected predictors from the K_n subsets.
(c) Stage 2: merge the sets s̃_1, …, s̃_{K_n} into a single set S̃ = ∪_{i=1}^{K_n} s̃_i, and define p_n = |S̃|. Perform Bayesian variable selection on the subset data D_n^{S̃} = {y, X_{S̃}} at an FDR level of α_2. The Bayesian variable selection is subject to the prior setting π(σ) ∼ IG(a_0, b_0), π(ξ) = (r_n/p_n)^{|ξ|}(1 − r_n/p_n)^{p_n−|ξ|} I(|ξ| ≤ r̄_n) and π(β_ξ | ξ, σ) ∼ N{0, σ²(X_ξ^T X_ξ + τI)/n}.
Clearly, it follows from the theory that was developed in Section 2 that the SAM approach will lead to a consistent selection of true predictors. In step 3, the predictors can also be selected according to the MAP model.
3.2. Simulation and hyperparameter setting
Since different predictors can be highly correlated, the posterior (7) can have a rugged energy landscape for some problems. Conventional MCMC algorithms, such as the Metropolis–Hasting algorithm, tend to become trapped in a local mode in simulations. To avoid this problem, the stochastic approximation Monte Carlo (SAMC) algorithm (Liang et al., 2007) was used in this paper. … Refer to the on-line supplementary material for the details of implementation of this algorithm."""),
}
SL_INDEX = """[Index compiled by the preparer, not a quotation.] The formal results stated in the main text of Song and Liang (2015)
are: Theorem 1 (p. 952), Theorem 2 (p. 953), Corollary 1 (p. 954), Theorem 3 (p. 956), Theorem 4 (p. 957), Corollary 2
(p. 957); Theorem S (consistency of MAP models) is in the on-line supplement, cited on p. 956, and was not read by the
audit. The main text also contains result (16) (p. 954). Sections 4–7 (pp. 959–971) are numerical studies, a
time-complexity analysis and a discussion; the preparer found no further theorem, corollary or lemma statement there."""


def sl(*ids):
    out = []
    for k in ids:
        page, lab, text = SL[k]
        out.append(f"Song & Liang (2015), p. {page}, {lab} [{k}; transcribed from p. {page} image]:\n```\n{text}\n```")
    return "\n".join(out)


# ---------------------------------------------------------------- shared context ----------------------------------
def conventions():
    return "\n".join([
        "Meaning of inside / outside (the audit's convention):",
        q("TB", (55, 57)),
        "Track C = internal proxy computations on simulated designs (no proofs, no fits of the method). Legend of its table:",
        q("TC", (13, 18)),
    ])


def designs():
    return "\n".join([
        "The audit's summary of our designs:", q("TB", (40, 48)),
        "Generator of the 2,400-fit study (scenarios S1–S6 = cases 1–6; truth):", q("GEN", (18, 41)),
        "Study specification (designs, truth, signal):", q("RERUN", (37, 42)),
        "P6 designs:", q("P6", (13, 17)),
        "1M plan designs and truth:", q("P1M", (84, 92)),
    ])


def trackc_table():
    return q("TC", (21, 41))


# ---------------------------------------------------------------- items -------------------------------------------
# Each item: id, title, our (a), SL ids (b), verdicts (c) as a list of (verdict_id, text), track C (d) or None.
def core1():
    stmts = "\n".join([
        "Standing assumptions (S1), (S2) of the reader versions:", q("RV", (28, 29)),
        "Reader statement of Theorem 1 and Theorem 1′ (row 1.1):", q("RV", (103, 134)),
        "Reader statement of Theorem 2 (row 1.2):", q("RV", (269, 285)),
        "Reader statement of Theorem 3 (row 1.3):", q("RV", (333, 356)),
        "Master: the target posterior π and the truth (prior, standardisation, outputs):", q("POST", (18, 34)),
        "Master Theorem 1 (hypotheses, conclusions 1–4, random-design item 6):", q("POST", (63, 75), (80, 86), (95, 100)),
        "Master Corollary 1R (Gaussian rows, LSF):", q("POST", (106, 112)),
        "Master Theorem 1′ (Claim E):", q("POST2", (126, 133)),
        "Master Corollary B (Theorem 3(a)):", q("PSHARP", (92, 100)),
    ])
    items = [
        ("B1", "Gaussian linear model with independent Gaussian errors",
         [q("RV", (28, 28)), q("POST", (31, 31))], ["SL-M1", "SL-M2"],
         [("B1.SL", q("TB", (63, 63)) + au((34, 36))), ("B1.IO", q("TB", (242, 244)))], None),
        ("B2", "Dimension p ≤ n^A",
         [q("RV", (29, 29)), q("POST", (63, 64))], ["SL-M1", "SL-M3", "SL-CO1"],
         [("B2.SL", q("TB", (69, 70)) + au((34, 35), (37, 37))), ("B2.IO", q("TB", (242, 243), (245, 245)))], None),
        ("B3", "Exact sparsity with s₀ fixed",
         [q("RV", (105, 105), (272, 273), (338, 338)), q("POST", (63, 63))], ["SL-M3", "SL-H", "SL-T2"],
         [("B3.SL", q("TB", (78, 79)) + au((34, 35), (39, 39))), ("B3.IO", q("TB", (242, 243), (246, 246)))], None),
        ("B4-UP", "Signal bounded above (Thm 1 (A3); master (E))",
         [q("RV", (106, 106)), q("POST", (67, 67))], ["SL-M3", "SL-H", "SL-T1"],
         [("B4-UP.SL", q("TB", (89, 92)) + au((34, 35), (40, 40))), ("B4.IO", q("TB", (242, 243), (247, 247)))],
         None),
        ("B4-LO", "Signal bounded below: beta-min at √(log n/n) (Thm 1 (A6)); fixed nonzero signals (Thm 2 (A2))",
         [q("RV", (111, 113), (272, 273)), q("POST", (74, 75))], ["SL-C3", "SL-C3S", "SL-T3"],
         [("B4-LO.SL", q("TB", (89, 92)) + au((34, 35), (43, 43)))], q("TC", (45, 45))),
        ("B5", "Eigenvalue floor on small sets (Thm 1 (A4), Thm 1′ (A4′), Thm 2 (A3))",
         [q("RV", (107, 108), (128, 131), (274, 276)), q("POST", (68, 70), (106, 109)), q("POST2", (126, 130))],
         ["SL-T1", "SL-T2", "SL-C3", "SL-C3S", "SL-T3"],
         [("B5.SL", q("TB", (101, 101)) + au((34, 35), (41, 41))), ("B5.IO", q("TB", (242, 243), (248, 248)))],
         q("TC", (43, 44), (49, 55), (57, 60))),
        ("B6", "No near-exact collinearity among O(log n) columns (Thm 1 (A5); master (F_w))",
         [q("RV", (109, 110)), q("POST", (71, 73))], ["SL-H", "SL-T1", "SL-V", "SL-T3"],
         [("B6.SL", q("TB", (125, 126)) + au((34, 35), (42, 42))), ("B6.IO", q("TB", (242, 243), (249, 249)))],
         q("TC", (46, 47))),
        ("B7", "Law of the rows: i.i.d. Gaussian (Thm 2)",
         [q("RV", (269, 270)), q("POST", (106, 107))], ["SL-C1"],
         [("B7.SL", q("TB", (140, 140)) + au((34, 35), (44, 44))), ("B7.IO", q("TB", (242, 243), (250, 250)))],
         None),
        ("DR", "Fixed-to-random design transfer",
         [q("POST", (95, 100))], ["SL-M2", "SL-T1"],
         [("DR.SL", au((34, 35), (45, 45), note=" (Song–Liang column only is under test)"))], None),
        ("SUM", "HPM, MPM, PIPs from 1 − π(S₀ | y)",
         [q("RV", (114, 123)), q("POST", (80, 86))], ["SL-C3", "SL-T3"],
         [("SUM.SL", au((34, 35), (46, 46), note=" (Song–Liang column only is under test)"))], None),
        ("PRIOR", "The prior as coded (a setting, not an assumption)",
         [q("POST", (18, 30))], ["SL-P6", "SL-T1", "SL-V"],
         [("PRIOR.SL", au((34, 35), (38, 38), note=" (Song–Liang column only is under test)"))], None),
        ("ROW13", "Theorem 3 (row 1.3): lower bound; witness designs",
         [q("RV", (333, 352)), q("PSHARP", (92, 100))], ["SL-T1", "SL-T2", "SL-CO1", "SL-T3"],
         [("ROW13.SL", au((117, 121)) + q("TB", (235, 236)) + q("TB", (242, 243), (255, 255)))], None),
        ("SCOPE", "Core-level verdict for the posterior theorems",
         [], [],
         [("SCOPE.IO", q("TB", (14, 17)) + q("TB", (24, 26)))], None),
    ]
    return ("core1", "rows 1.1, 1.2, 1.3 (Theorems 1, 1′, 2, 3: the posterior finds the true model; the rate)",
            stmts, items, True)


def core2():
    stmts = "\n".join([
        "Reader version, Theorem 9 / 9B / Corollary 9C (row 2.1), setting through the corollary:", q("RV", (996, 1099)),
        "Master §1R (setup, prior, assumptions, Theorems A, B, Corollary C):", q("DIST", (136, 162), (164, 238)),
    ])
    items = [
        ("B1", "(A1) Gaussian linear model, any noise level",
         [q("RV", (1034, 1035)), q("DIST", (174, 175))], ["SL-M1", "SL-M2"],
         [("B1.SL", q("TB", (63, 63)) + au((56, 58))), ("B1.IO", q("TB", (242, 244)))], None),
        ("B3", "(A2) at most s nonzero coefficients",
         [q("RV", (1036, 1036)), q("DIST", (176, 176))], ["SL-M3", "SL-H", "SL-T1", "SL-T2"],
         [("B3.SL", q("TB", (78, 79)) + au((56, 57), (59, 59))), ("B3.IO", q("TB", (242, 243), (246, 246)))],
         None),
        ("B2", "(A2) dimension 2 ≤ p ≤ n^A",
         [q("RV", (1036, 1036)), q("DIST", (176, 176))], ["SL-M1", "SL-M3", "SL-CO1"],
         [("B2.SL", q("TB", (69, 70)) + au((56, 57), (59, 59), note=" (\"p as in row 1\")")),
          ("B2.IO", q("TB", (242, 243), (245, 245)))], None),
        ("B7", "(A3) sub-Gaussian predictors on sparse directions",
         [q("RV", (1037, 1039)), q("DIST", (177, 178))], ["SL-C1"],
         [("B7.SL", q("TB", (140, 140)) + au((56, 57), (60, 60))),
          ("B7.LEMMA", au((181, 182), note=" (the implication proposed as a lemma; under test as stated)")),
          ("B7.IO", q("TB", (242, 243), (250, 250)))], None),
        ("B6", "(A4) no near-exact collinearity, floor c_ψ/n on O(log n) sets",
         [q("RV", (1040, 1041), (1067, 1071)), q("DIST", (179, 179), (200, 202))], ["SL-H", "SL-T1", "SL-V", "SL-T2"],
         [("B6.SL", q("TB", (125, 126)) + au((56, 57), (61, 61))), ("B6.IO", q("TB", (242, 243), (249, 249)))],
         q("TC", (46, 47))),
        ("B4", "(A5) bounded standardised signal",
         [q("RV", (1042, 1042)), q("DIST", (180, 180))], ["SL-M3", "SL-T1"],
         [("B4.SL", q("TB", (89, 92)) + au((56, 57), (62, 62))), ("B4.IO", q("TB", (242, 243), (247, 247)))],
         q("TC", (45, 45))),
        ("A6-9B", "(A6) of Theorem 9B: fixed floor on bounded sets; beta-min (parametric rate)",
         [q("RV", (1073, 1079)), q("DIST", (209, 215))], ["SL-T1", "SL-T2", "SL-CO1", "SL-T3"],
         [("A6-9B.SL", au((56, 57), (63, 63), note=" (Song–Liang column only is under test)") + "\n" + SL_INDEX),
          ("A6-9B.IO", q("TB", (242, 243), (247, 248)))], q("TC", (43, 45))),
        ("H", "Hellinger distance (averaged conditional = joint; d² = 2d_H²)",
         [q("RV", (1009, 1023)), q("DIST", (154, 159))], ["SL-H", "SL-T1"],
         [("H.SL", au((56, 57), (64, 64), note=" (Song–Liang column only is under test)"))], None),
        ("C9C", "Corollary 9C: the sampler's returned list",
         [q("RV", (1081, 1099)), q("DIST", (217, 238))], ["SL-SAM"],
         [("C9C.SL", au((56, 57), (65, 65), note=" (Song–Liang column only is under test)") + "\n" + SL_INDEX)],
         None),
        ("SCOPE", "Core-level verdict for the posterior theorems",
         [], [],
         [("SCOPE.IO", q("TB", (14, 17)) + q("TB", (24, 26)))], None),
    ]
    return ("core2", "row 2.1 (Theorem 9, 9B, Corollary 9C: the posterior finds the true distribution)",
            stmts, items, True)


def core3():
    stmts = "\n".join([
        "Standing assumptions (S1)–(S3) of the reader versions:", q("RV", (28, 31)),
        "Reader statement of Theorem 6 (row 3.1):", q("RV", (666, 703)),
        "Master Setting R (W3-RM) and constants (Form R, W3-RM2):", q("RM", (41, 44)), q("RM2", (112, 116)),
        "Master conditions inherited from W3-RM (T1-R), (FL-R), (V-R):", q("RM", (129, 136)),
        "Master §3.2 (Gaussian rows) and the theorem (C2):", q("RM2", (172, 202), (215, 218)),
        "Master sufficient form (W-loc) for the width condition (referred to by (A6)):", q("RM2", (159, 168)),
    ])
    items = [
        ("B7", "Rows i.i.d. Gaussian; (S1), (S2)",
         [q("RV", (666, 669)), q("RM", (41, 44))], ["SL-M1", "SL-M2", "SL-M3", "SL-C1"],
         [("B7.SL", q("TB", (140, 140)) + au((74, 76))),
          ("B1.SL", q("TB", (63, 63))), ("B2.SL", q("TB", (69, 70))),
          ("B7.IO", q("TB", (242, 245), (250, 250)))], None),
        ("A2", "(A2) s₀ fixed, fixed nonzero signals",
         [q("RV", (670, 671)), q("RM", (41, 44))], ["SL-M3", "SL-C3", "SL-T3"],
         [("A2.SL", q("TB", (78, 79), (89, 92)) + au((74, 75), (77, 77))),
          ("A2.IO", q("TB", (242, 243), (246, 247)))], q("TC", (45, 45))),
        ("B8", "(A3) visibility given ≤ 15 columns",
         [q("RV", (672, 673)), q("RM", (135, 136))], ["SL-MIS", "SL-C5"],
         [("B8.SL", q("TB", (155, 156)) + au((74, 75), (78, 78))),
          ("B8.LEMMA", au((183, 183), note=" (the implication proposed as a lemma; under test as stated)")),
          ("B8.IO", q("TB", (242, 243), (251, 251)))],
         q("TC", (21, 23), (36, 40), (49, 55), (61, 64))),
        ("B9", "(A4) leakage set |Q| ≤ n^b, no leak outside, locality",
         [q("RV", (674, 681)), q("RM2", (176, 184))], ["SL-C5", "SL-SAM"],
         [("B9.SL", q("TB", (175, 175)) + au((74, 75), (79, 79))),
          ("B9.IO", q("TB", (242, 243), (252, 252)))], q("TC", (65, 68))),
        ("A5", "(A5) population floor on O(log n) sets and on Q ∪ {l}",
         [q("RV", (682, 683)), q("RM", (129, 134))], ["SL-C3", "SL-C3S", "SL-T3"],
         [("B5.SL", q("TB", (101, 101)) + au((74, 75), (80, 80), note=" (first part)")),
          ("B10-FL.SL", q("TB", (199, 200)) + au((74, 75), (80, 80), note=" (second part)")),
          ("A5.IO", q("TB", (242, 243), (248, 248), (253, 253)))], q("TC", (43, 44), (49, 55), (57, 60))),
        ("A6", "(A6) local regressions inside Q",
         [q("RV", (684, 688)), q("RM2", (159, 168))], [],
         [("A6.SL", q("TB", (199, 200)) + au((74, 75), (81, 81))),
          ("A6.IO", q("TB", (242, 243), (253, 253)))], q("TC", (65, 68))),
        ("SCOPE", "Core-level verdict for the reported-model theorem",
         [], [],
         [("SCOPE.IO", q("TB", (18, 20)) + q("TB", (24, 25), (27, 27)))], None),
    ]
    return ("core3", "row 3.1 (Theorem 6: the coded method reports the true model)", stmts, items, True)


# ---------------------------------------------------------------- prompts -----------------------------------------
SYSTEM = """You are a blind, independent referee. A research project on the asymptotic theory of a Bayesian variable-selection
method (Gaussian linear regression, p ≤ n^A, often p ≫ n) has written an audit that compares the hypotheses of its
theorems with those of Song and Liang (2015, J. R. Statist. Soc. B 77, 947–972) and states which of its simulation
designs satisfy each hypothesis. You receive, for one group of theorems, verbatim excerpts: the project's theorem and
assumption texts (file and line numbers), the matching Song–Liang passages (journal page and display or condition
number), the design definitions, internal proxy computations (track C) and the verdicts under test. The audit's
reasoning and all earlier reviews are deliberately withheld; status labels have been removed from the excerpts.
Bracketed markers such as [H5-1] or [S1-F3] are editorial tags; ignore them.

Judge only the texts given. Do not rely on your memory of Song–Liang or of any other paper. All results are asymptotic;
a design is read as a sequence in n with its structure and s₀ fixed; explicit constants in the hypotheses are
conservative and not part of the judgement; finite-n behaviour is not a defect.

Your job is to break each verdict listed in the task. For each one either REFUTE it or say NO FINDING:
- REFUTED needs a concrete reason: a counterexample, a misread condition (wrong display, wrong page, a remark or an
  example read as a hypothesis, a sufficient condition read as the condition), or a quantifier or direction error
  (which statement implies which; for every / there exists; over which sets, sizes and sequences; fixed against
  vanishing levels; sample against population; correlation against unnormalised scale). State it with exact
  references (our file:line, or Song–Liang page and display number).
- For a design verdict (inside / outside / unclear), check the design definition against the hypothesis as stated,
  including signs and sizes of correlations and factor structure; one explicit computation that contradicts the verdict
  is enough to refute it. Track C lines are evidence, not proof.
- For an absence claim ("no counterpart", "SL prove nothing on …", "no lower bound in SL"), decide from the texts given.
- UNCLEAR is allowed only when the texts given cannot settle the verdict; then name the passage or fact you would need.
Do not report style, wording, presentation or possible improvements.

Output, in this order:
1. Findings only: for each REFUTED or UNCLEAR verdict, a short section headed by its verdict id with the problem, the
   exact references and the counterexample or the missing passage. Write nothing for a NO FINDING verdict.
2. Then exactly one line per verdict listed in the task, in the listed order, and nothing after the last one:
AUDIT1 <core>:<item> VERDICT=<NO-FINDING|REFUTED|UNCLEAR>"""


def render(core, title, stmts, items):
    vids = [f"{core}:{vid}" for it in items for vid, _ in it[4]]
    P = [f"# AUDIT1 — {core}: {title}",
         "",
         "Material for a blind review of the audit's Song–Liang comparisons and inside/outside verdicts. Every excerpt is",
         "verbatim with its file and line numbers; Song–Liang passages carry the journal page and display or condition",
         "number. Status labels have been replaced by [status omitted] or [review omitted].",
         "",
         "## 0. Conventions", conventions(),
         "", "## 1. Our theorem statements (verbatim)", stmts,
         "", "## 2. Our designs (verbatim)", designs(),
         "", "## 3. Track C table (internal proxy computations; verbatim)", trackc_table(),
         "", "## 4. Items under test"]
    for iid, ititle, ours, slids, verdicts, tc in items:
        P += ["", f"### {core}:{iid} — {ititle}"]
        P += ["**(a) Our assumption text.**", "\n".join(ours) if ours else "(core-level verdict; see §1 and the items above)"]
        P += ["**(b) Song–Liang text.**", sl(*slids) if slids else "(none cited by the audit for this item)"]
        P += ["**(c) Verdict(s) under test.**"]
        for vid, vtext in verdicts:
            P += [f"- `{core}:{vid}`", vtext]
        P += ["**(d) Track C evidence.**", tc if tc else "(none)"]
    task = ["Break the comparison; findings only.",
            "",
            f"Verdicts to judge ({len(vids)}), in this order; return one machine line for each:"] + vids
    return "\n".join(P) + "\n", "\n".join(task) + "\n", vids


def sha_src(key):
    return hashlib.sha256(raw(key)).hexdigest()


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "SYSTEM.md").write_text(SYSTEM + "\n", encoding="utf-8")
    reqs, rows, est = [], [], []
    for fn in (core1, core2, core3):
        core, title, stmts, items, _ = fn()
        ctx, task, vids = render(core, title, stmts, items)
        req_md = OUT / f"REQ_{core}.md"
        req_md.write_text(ctx + "\n---\n\n## Task (sent as a separate block)\n\n" + task, encoding="utf-8")
        chars = len(SYSTEM) + len(ctx) + len(task)
        est.append((core, chars, len(vids)))
        rel = req_md.relative_to(ROOT).as_posix()
        for s in range(1, SAMPLES + 1):
            cid = f"audit1-{core}-s{s}"
            reqs.append({"custom_id": cid, "file": rel, "claims": vids, "params": {
                "model": MODEL, "max_tokens": MAX_TOKENS, "output_config": {"effort": "high"}, "system": SYSTEM,
                "messages": [{"role": "user", "content": [
                    {"type": "text", "text": ctx, "cache_control": {"type": "ephemeral"}},
                    {"type": "text", "text": task}]}]}})
            rows.append((cid, core, title, len(vids), ";".join(vids)))
    (OUT / "requests.json").write_text(json.dumps(reqs, ensure_ascii=False), encoding="utf-8")
    with open(OUT / "REQUESTS.tsv", "w", encoding="utf-8") as f:
        f.write("custom_id\tcore\trows\tn_verdicts\tverdict_ids\n")
        for r in rows:
            f.write("\t".join(str(x) for x in r) + "\n")
    with open(OUT / "MANIFEST.tsv", "w", encoding="utf-8") as f:
        f.write("source\tpath\tcommit\tsha256\n")
        for k, (wt, rev, path) in SRC.items():
            f.write(f"{k}\t{path}\t{rev or 'untracked'}\t{sha_src(k)}\n")
        f.write(f"SL\t{SL_PDF}\tnot in git (excerpts only)\t{hashlib.sha256(SL_PDF.read_bytes()).hexdigest()}\n")
        f.write(f"SYSTEM\tTheory_work/Wave3/API_AUDIT/audit1/SYSTEM.md\tbuilt\t"
                f"{hashlib.sha256((SYSTEM + chr(10)).encode()).hexdigest()}\n")
    # offline token estimate: chars / 3.5 (an estimate; HQ runs the free count endpoint for the exact figure)
    L = ["AUDIT1 token and cost estimate (OFFLINE ESTIMATE: tokens ≈ characters / 3.5; not a count).",
         "Exact input counts: `python Theory_work/Wave3/API_AUDIT/audit_batch.py count Theory_work/Wave3/API_AUDIT/audit1`.",
         f"Model {MODEL}, effort high, max_tokens {MAX_TOKENS}, {SAMPLES} samples per core, {len(reqs)} requests.",
         "Batch rates for Claude Fable 5.2: input $4.00 / MTok, output $20.00 / MTok (half of $8 / $40).", "",
         "core\tchars/request\test. input tokens/request\tverdicts"]
    tin = 0
    for core, chars, nv in est:
        t = round(chars / 3.5)
        tin += t * SAMPLES
        L.append(f"{core}\t{chars}\t{t}\t{nv}")
    tout_max = MAX_TOKENS * len(reqs)
    tout_exp = 16000 * len(reqs)
    cin = tin * 4 / 1e6
    L += ["", f"total est. input tokens (all {len(reqs)} requests, no cache credit): {tin}  -> ${cin:.2f}",
          f"output, expected (≈16k tokens per request incl. thinking): {tout_exp} -> ${tout_exp*20/1e6:.2f}",
          f"output, worst case (every request hits max_tokens {MAX_TOKENS}): {tout_max} -> ${tout_max*20/1e6:.2f}",
          f"TOTAL: expected ≈ ${cin + tout_exp*20/1e6:.2f}; worst case ≤ ${cin + tout_max*20/1e6:.2f} (budget $30: "
          f"2 samples per core fit).",
          "Cache reads of the shared context (sample 2 of each core) are billed lower; not credited above.",
          "Note: `audit_batch.py wait` overwrites this file with the billed usage after the run; the estimate is "
          "repeated in README.md."]
    (OUT / "USAGE.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


def verdicts():
    """Parse results/*.md written by `audit_batch.py wait` (it only collects 'AUDIT ' lines) into AUDIT1_VERDICTS.tsv."""
    res = OUT / "results"
    rows = []
    for p in sorted(res.glob("audit1-*.md")):
        cid = p.stem
        for line in p.read_text(encoding="utf-8").splitlines():
            m = re.match(r"\s*AUDIT1 (core\d):(\S+) VERDICT=(NO-FINDING|REFUTED|UNCLEAR)\s*$", line)
            if m:
                rows.append((cid, f"{m.group(1)}:{m.group(2)}", m.group(3)))
    expected = {(q["custom_id"], v) for q in json.loads((OUT / "requests.json").read_text(encoding="utf-8"))
                for v in q["claims"]}
    got = {(c, v) for c, v, _ in rows}
    with open(OUT / "AUDIT1_VERDICTS.tsv", "w", encoding="utf-8") as f:
        f.write("custom_id\tverdict_id\tresult\n")
        for r in sorted(rows):
            f.write("\t".join(r) + "\n")
        for c, v in sorted(expected - got):
            f.write(f"{c}\t{v}\tMISSING\n")
    print(f"{len(rows)} verdict lines; {len(expected - got)} missing -> {OUT / 'AUDIT1_VERDICTS.tsv'}")


if __name__ == "__main__":
    {"build": build, "verdicts": verdicts}[sys.argv[1]]()
