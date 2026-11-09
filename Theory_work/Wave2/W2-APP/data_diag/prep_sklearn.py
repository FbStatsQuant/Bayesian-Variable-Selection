# prep_sklearn.py -- exports sklearn's bundled diabetes (quadratic model of Efron et al. 2004) and digits designs to data/*.csv
import itertools, numpy as np, pandas as pd, sklearn
from sklearn.datasets import load_diabetes, load_digits
d = load_diabetes(scaled=True)          # columns centred, each scaled to unit sum of squares
Xm = d.data; names = list(d.feature_names)   # age sex bmi bp s1..s6
n, p = Xm.shape
Z = (Xm - Xm.mean(0)) / Xm.std(0, ddof=1)            # unit-variance main effects
cols, cn = [Z[:, j] for j in range(p)], list(names)
for i, j in itertools.combinations(range(p), 2):
    cols.append(Z[:, i] * Z[:, j]); cn.append(f"{names[i]}:{names[j]}")
for j in range(p):
    if names[j] != "sex":                              # no square for the binary covariate
        cols.append(Z[:, j] ** 2); cn.append(f"{names[j]}^2")
Q = np.column_stack(cols); assert Q.shape == (442, 64), Q.shape
pd.DataFrame(Q, columns=cn).assign(y=d.target).to_csv("data/diabetes_quad.csv", index=False)
g = load_digits()
pd.DataFrame(g.data, columns=[f"px{i}" for i in range(64)]).assign(y=g.target).to_csv("data/digits.csv", index=False)
open("data/sklearn_version.txt", "w").write(f"sklearn {sklearn.__version__}; numpy {np.__version__}\n")
print("diabetes quad", Q.shape, "digits", g.data.shape, sklearn.__version__)
