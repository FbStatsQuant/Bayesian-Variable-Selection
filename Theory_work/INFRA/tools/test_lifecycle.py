"""test_lifecycle.py — regression scenarios for the lifecycle tools (review R01 findings 3-7).

Runs real propagate.py / registry.py operations on the live registry with TEST:* claims, then restores every
registry data file byte for byte (and removes files and issue folders it created). Prints PASS/FAIL per scenario.
Run: python Theory_work/INFRA/tools/test_lifecycle.py   (exit code 1 if any scenario fails)"""
import os, shutil, subprocess, sys, tempfile
INFRA = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(INFRA, "tools"))
import bvsreg as R

FILES = [os.path.join(R.REG, f) for f in os.listdir(R.REG) if f.endswith((".tsv", ".log"))] + \
        [os.path.join(INFRA, "DECISIONS.md"), os.path.join(INFRA, "FAILED_ROUTES.md")]
bak = tempfile.mkdtemp()
for f in FILES:
    shutil.copy2(f, bak)
issues_before = set(os.listdir(os.path.join(INFRA, "issues"))) if os.path.isdir(os.path.join(INFRA, "issues")) else set()


def run(*a, ok=True):
    p = subprocess.run([sys.executable, os.path.join(INFRA, "tools", a[0]), *a[1:], "--actor", "TEST"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if ok and p.returncode != 0:
        print("UNEXPECTED FAILURE", a, p.stdout[-600:], p.stderr[-600:])
    return p.returncode, p.stdout + p.stderr


def st(cid):
    return R.index(R.load_claims())[cid]


results = []
try:
    X = "W2-FAC-A:Thm-FAC-L"
    gates = st(X)["gates"]
    STM = "Theory_work/Wave2/W2-FAC-A/STATEMENT.md"
    run("registry.py", "add", "TEST:Y", "--file", STM, "--lines", "1-3", "--kind", "theorem", "--name", "Y",
        "--status", "PROVED-CHECKED", "--state", "CANDIDATE", "--field", f"implies={X}", "--field", "headline=yes",
        "--field", f"gates={gates}", "--field", "conclusion=delivery: y", "--reason", "t")
    # promote requires a reference
    rc, out = run("propagate.py", "promote", "TEST:Y", "--reason", "t", ok=False)
    results.append(("promote without --parity-with refused", rc != 0))
    run("propagate.py", "promote", "TEST:Y", "--parity-with", X, "--reason", "t")
    # finding 3: Y depending on X must block supersede
    run("registry.py", "set", "TEST:Y", f"depends_on={X}", "--reason", "t")
    rc, out = run("propagate.py", "supersede", X, "--by", "TEST:Y", "--reason", "t", ok=False)
    results.append(("supersede refused when Y depends on X", rc != 0 and "depends on" in out))
    run("registry.py", "set", "TEST:Y", "depends_on=", "--reason", "t")
    # finding 4: D uses X and Y; confirm re-point; retract Y -> D must become SUSPECT, keep its own Y edge
    D = "W2-UNI:UNI-1"
    run("registry.py", "set", D, f"depends_on={X}@stmt; TEST:Y@stmt; W2-FAC-A:Prop-F-FAC", "--reason", "t")
    run("propagate.py", "supersede", X, "--by", "TEST:Y", "--reason", "free")
    results.append(("X SUPERSEDED-VALID", st(X)["state"] == "SUPERSEDED-VALID"))
    run("propagate.py", "confirm-repoint", D, "--from", X, "--to", "TEST:Y", "--checked-by", "t", "--reason", "t")
    run("propagate.py", "retract", "TEST:Y", "--reason", "t")
    d = st(D)
    results.append(("D SUSPECT after Y retracted (independent Y use kept)", d["state"] == "SUSPECT"
                    and "TEST:Y" in d["depends_on"] and X in d["depends_on"]))
    results.append(("X restored ACTIVE", st(X)["state"] == "ACTIVE" and not st(X)["superseded_by"]))
    # finding 5: superseded-valid claim invalidated by an upstream retraction is not restored later
    run("registry.py", "add", "TEST:Z", "--file", STM, "--lines", "4-6", "--kind", "theorem", "--name", "Z",
        "--status", "PROVED-CHECKED", "--field", f"implies={X}", "--field", "headline=yes",
        "--field", f"gates={gates}", "--field", "conclusion=delivery: z", "--reason", "t")
    run("propagate.py", "supersede", X, "--by", "TEST:Z", "--reason", "free2")
    up = R.Graph(R.load_claims()).deps[X][0]
    run("propagate.py", "retract", up, "--reason", "upstream")
    results.append(("superseded-valid X becomes SUSPECT when an input is retracted", st(X)["state"] == "SUSPECT"))
    run("propagate.py", "retract", "TEST:Z", "--reason", "t")
    results.append(("X not restored (it is SUSPECT)", st(X)["state"] == "SUSPECT" and not st(X)["superseded_by"]))
    # finding 7: downgrade cannot strengthen; status not settable
    rc, _ = run("propagate.py", "downgrade", "W2-LOC2:PLR", "--status", "PROVED-CHECKED", "--reason", "t", ok=False)
    results.append(("downgrade to a stronger status refused", rc != 0))
    rc, _ = run("registry.py", "set", "W2-LOC2:PLR", "status=PROVED-CHECKED", "--reason", "t", ok=False)
    results.append(("set status refused", rc != 0))
    rc, out = run("propagate.py", "coexist", "C-GROW:Thm-GROW", "--with", "C-GROW:Thm-GROW", "--reason", "t", ok=False)
    results.append(("coexist with itself refused", rc != 0))
finally:
    for f in FILES:
        shutil.copy2(os.path.join(bak, os.path.basename(f)), f)
    for f in os.listdir(R.REG):
        fp = os.path.join(R.REG, f)
        if f.endswith((".tsv", ".log")) and fp not in FILES:
            os.remove(fp)
    idir = os.path.join(INFRA, "issues")
    if os.path.isdir(idir):
        for x in set(os.listdir(idir)) - issues_before:
            shutil.rmtree(os.path.join(idir, x), ignore_errors=True)
        if not os.listdir(idir):
            os.rmdir(idir)
    shutil.rmtree(bak, ignore_errors=True)
for name, ok in results:
    print("PASS" if ok else "FAIL", name)

sys.exit(0 if all(ok for _, ok in results) else 1)
