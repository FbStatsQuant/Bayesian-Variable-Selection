"""check_render.py TABLES_DIR WORK_DIR : Sol R2 finding-9 check. Renders the headline from (a) the real tables (benchmarks pending),
(b) a copy with every benchmark row marked as run (complete), (c) a copy with one benchmark row run (partial), and asserts that the short
answer and the Q4 section agree in each case. Test data only (synthetic benchmark counts, never a result)."""
import sys, shutil, subprocess
from pathlib import Path
import pandas as pd
T, W = Path(sys.argv[1]), Path(sys.argv[2]); R = Path(__file__).resolve().parents[1] / "render_headline.py"
def render(tdir, out):
    subprocess.run([sys.executable, str(R), str(tdir), str(out)], check=True, capture_output=True); return out.read_text(encoding="utf-8")
ok = True
for state in ("pending", "complete", "partial"):
    d = W / state; d.mkdir(parents=True, exist_ok=True)
    for f in T.glob("*.csv"): shutil.copy(f, d / f.name)
    q4 = pd.read_csv(d / "Q4_recovery.csv"); b = ~q4.method_id.isin(["SMCBVS", "EXACT"])
    if state == "pending": q4.loc[b, "n_not_run"] = q4.loc[b, "n_pooled"]
    if state == "complete": q4.loc[b, "n_not_run"] = 0
    if state == "partial": q4.loc[b, "n_not_run"] = q4.loc[b, "n_pooled"]; q4.loc[q4.index[b][0], "n_not_run"] = 0
    q4.to_csv(d / "Q4_recovery.csv", index=False)
    md = render(d, d / "HEADLINE.md")
    short4 = [l for l in md.splitlines() if l.startswith("4. **Recovery")][0]
    pend_short, pend_q4 = "**pending**" in short4, "**Benchmarks: pending.**" in md
    table_q4 = "**All methods, pooled exact recovery /600 per p × c**" in md
    good = {"pending": pend_short and pend_q4 and not table_q4,
            "complete": (not pend_short) and (not pend_q4) and table_q4 and "Full table in Q4" in short4,
            "partial": (not pend_short) and (not pend_q4) and table_q4 and "**partial**" in short4}[state]
    print(f"{state}: short-answer pending={pend_short} Q4 pending={pend_q4} Q4 table={table_q4} -> {'OK' if good else 'FAIL'}")
    ok &= good
real = render(T, W / "HEADLINE_real.md"); cur = (T.parent / "HEADLINE_L.md").read_text(encoding="utf-8")
print("real-tables render identical to HEADLINE_L.md:", real == cur); ok &= real == cur
print("TEST_PASS" if ok else "TEST_FAIL"); sys.exit(0 if ok else 1)
