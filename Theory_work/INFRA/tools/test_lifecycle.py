"""test_lifecycle.py — regression scenarios for the lifecycle tools (reviews R01 and R02).

Never touches the live registry: it creates a disposable detached git worktree of HEAD in a temp directory, copies
the CURRENT Theory_work/INFRA folder (working copy) into it, runs real propagate.py / registry.py operations there,
and removes the worktree at the end (also on errors). If the process is killed, only a temp worktree is left
behind (`git worktree prune` / run_ci's stale-sandbox cleanup removes it).
Run: python Theory_work/INFRA/tools/test_lifecycle.py   (exit code 1 if any scenario fails)"""
import importlib.util, os, shutil, subprocess, sys, tempfile

LIVE_INFRA = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIVE_ROOT = os.path.abspath(os.path.join(LIVE_INFRA, "..", ".."))
TMP = tempfile.mkdtemp(prefix="bvs-test-")
os.rmdir(TMP)
subprocess.run(["git", "-C", LIVE_ROOT, "worktree", "add", "--detach", TMP, "HEAD"], check=True, capture_output=True)
INFRA = os.path.join(TMP, "Theory_work", "INFRA")
shutil.rmtree(INFRA, ignore_errors=True)
shutil.copytree(LIVE_INFRA, INFRA, ignore=shutil.ignore_patterns("out", "issues", "__pycache__", "*.tmp"))
_spec = importlib.util.spec_from_file_location("bvsreg_test", os.path.join(INFRA, "tools", "bvsreg.py"))
R = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(R)
assert R.ROOT == os.path.abspath(TMP), (R.ROOT, TMP)


def run(*a, ok=True):
    p = subprocess.run([sys.executable, os.path.join(INFRA, "tools", a[0]), *a[1:], "--actor", "TEST"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=TMP)
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
        "--status", "PROVED-CHECKED", "--source", "Theory_work/Wave2/W2-FAC-A/REPORT.md:20", "--state", "CANDIDATE", "--field", f"implies={X}", "--field", "headline=yes",
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
        "--status", "PROVED-CHECKED", "--source", "Theory_work/Wave2/W2-FAC-A/REPORT.md:20", "--field",
        f"implies={X}", "--field", "headline=yes", "--field", f"gates={gates}", "--field", "conclusion=delivery: z", "--reason", "t")
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
    # ---------------- R02 scenarios ----------------
    # F5: suspect --status refused; coexist needs incomparability + parity
    rc, _ = run("propagate.py", "suspect", "W2-LOC2:PLR", "--status", "PROVED-CHECKED", "--reason", "t", ok=False)
    results.append(("R02-F5 suspect --status refused", rc != 0))
    rc, _ = run("propagate.py", "coexist", "C-GROW:Thm-GROW", "--with", "W1-GEN:Thm-GEN", "--reason", "t", ok=False)
    results.append(("R02-F5 coexist without declared incomparability refused", rc != 0))
    # F3 chain: X -> Y -> Z re-points for D; retract Y (moved on: no change); retract Z -> D back on X; E (uses D) ok
    X2 = "C-GROW:Thm-GROW"
    g2 = st(X2)["gates"]
    for nm in ("Y2", "Z2"):
        run("registry.py", "add", f"TEST:{nm}", "--file", STM, "--lines", "7-9", "--kind", "theorem", "--name", nm,
            "--status", "PROVED-CHECKED", "--source", "Theory_work/Wave2/W2-FAC-A/REPORT.md:20", "--field",
            "headline=yes", "--field", f"gates={g2}", "--field", "conclusion=reported-model: t", "--reason", "t")
    run("registry.py", "set", "TEST:Y2", f"implies={X2}", "--reason", "t")
    run("registry.py", "set", "TEST:Z2", "implies=TEST:Y2", "--reason", "t")
    D2 = R.Graph(R.load_claims()).rdeps[X2][0]
    run("propagate.py", "supersede", X2, "--by", "TEST:Y2", "--reason", "free")
    run("propagate.py", "confirm-repoint", D2, "--from", X2, "--to", "TEST:Y2", "--checked-by", "t", "--reason", "t")
    run("propagate.py", "supersede", "TEST:Y2", "--by", "TEST:Z2", "--reason", "free")
    run("propagate.py", "confirm-repoint", D2, "--from", "TEST:Y2", "--to", "TEST:Z2", "--checked-by", "t", "--reason", "t")
    run("propagate.py", "retract", "TEST:Y2", "--reason", "t")
    d2 = st(D2)
    results.append(("R02-F3 retract of a moved-on link leaves D on Z, no X added",
                    "TEST:Z2" in d2["depends_on"] and X2 not in d2["depends_on"]))
    run("propagate.py", "retract", "TEST:Z2", "--reason", "t")
    d2 = st(D2)
    results.append(("R02-F3 retract Z restores D onto the latest VALID source (X), not dead Y",
                    X2 in d2["depends_on"] and "TEST:Y2" not in d2["depends_on"] and "TEST:Z2" not in d2["depends_on"]))
    # F3 dead predecessor + transitive: W uses V (supersedes dead U); retract V -> W keeps V edge, W and its users SUSPECT
    U, V = "W2-FAC-B:Thm-FAC-CS", "TEST:V3"
    g3 = st(U)["gates"]
    run("registry.py", "add", V, "--file", STM, "--lines", "10-12", "--kind", "theorem", "--name", "V3", "--status",
        "PROVED-CHECKED", "--source", "Theory_work/Wave2/W2-FAC-A/REPORT.md:20", "--field", "headline=yes",
        "--field", f"gates={g3}", "--field", f"implies={U}", "--field", "conclusion=delivery: v", "--reason", "t")
    Wd = R.Graph(R.load_claims()).rdeps[U][0]
    run("propagate.py", "supersede", U, "--by", V, "--reason", "free")
    run("propagate.py", "confirm-repoint", Wd, "--from", U, "--to", V, "--checked-by", "t", "--reason", "t")
    up = R.Graph(R.load_claims()).deps[U][0]
    run("propagate.py", "retract", up, "--reason", "kills U")
    run("propagate.py", "retract", V, "--reason", "t")
    gW = R.Graph(R.load_claims())
    users = gW.dependents(Wd)
    results.append(("R02-F3 dead predecessor: dependent SUSPECT and its users SUSPECT too",
                    st(Wd)["state"] == "SUSPECT" and all(st(u)["state"] in ("SUSPECT", "RETRACTED", "DEPRECATED")
                                                          for u in users)))
    # F4: clear refuses while an input is invalid
    rc, _ = run("propagate.py", "clear", Wd, "--reason", "t", ok=False)
    results.append(("R02-F4 clear refused while an input is retracted/suspect", rc != 0))
finally:
    subprocess.run(["git", "-C", LIVE_ROOT, "worktree", "remove", "--force", TMP], capture_output=True)
    subprocess.run(["git", "-C", LIVE_ROOT, "worktree", "prune"], capture_output=True)
    shutil.rmtree(TMP, ignore_errors=True)
for name, ok in results:
    print("PASS" if ok else "FAIL", name)

sys.exit(0 if all(ok for _, ok in results) else 1)
