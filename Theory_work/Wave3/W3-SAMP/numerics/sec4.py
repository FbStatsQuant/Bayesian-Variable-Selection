# re-run section 4 of run_checks.py alone (same code path), seed 4
import runpy, sys
src = open("run_checks.py", encoding="utf-8").read()
head = src.split("# ---------------------------------------------------------------- 1.")[0]
s4 = src.split("# ---------------------------------------------------------------- 4.")[1].split("# ---------------------------------------------------------------- 5.")[0]
sys.argv = ["x", "4"]
exec(head + "#" + s4.replace("R = run_islands(M, [0, 1.0], N=4, L=5, I=4000", "R = run_islands(M, [0, 1.0], N=4, L=20, I=2000").replace("P(W<0.01)={(R['W']<0.01).mean():.3f}; P(RB err >= .1)", "P(W<0.01)={(R['W']<0.01).mean():.3f}; median W={np.median(R['W']):.2e}; P(RB err >= .1)"))
