"""test_lifecycle.py — regression scenarios for the lifecycle tools (reviews R01-R05).

Never touches the live registry: it runs inside a CI Sandbox (ci/run_ci.py: a disposable detached git worktree of
HEAD, a strict child of the tool's sandbox root, owned through a held lock file), copies the CURRENT
Theory_work/INFRA folder (working copy) into it, runs real propagate.py / registry.py operations there, and removes
the sandbox at the end (also on errors; a killed run leaves a stale sandbox that the next Sandbox cleans up).
Run: python Theory_work/INFRA/tools/test_lifecycle.py   (exit code 1 if any scenario fails)"""
import importlib.util, os, shutil, subprocess, sys
sys.dont_write_bytecode = True  # never write __pycache__

LIVE_INFRA = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIVE_ROOT = os.path.abspath(os.path.join(LIVE_INFRA, "..", ".."))
sys.path.insert(0, os.path.join(LIVE_INFRA, "ci"))
sys.argv = sys.argv[:1]
import run_ci  # noqa: E402

results = []
SB = run_ci.Sandbox()
SB.__enter__()
try:
    TMP = SB.path
    INFRA = os.path.join(TMP, "Theory_work", "INFRA")
    shutil.rmtree(INFRA, ignore_errors=True)
    shutil.copytree(LIVE_INFRA, INFRA, ignore=shutil.ignore_patterns("out", "issues", "__pycache__", "*.tmp"))
    _spec = importlib.util.spec_from_file_location("bvsreg_test", os.path.join(INFRA, "tools", "bvsreg.py"))
    R = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(R)
    assert os.path.normcase(R.ROOT) == os.path.normcase(os.path.abspath(TMP)), (R.ROOT, TMP)

    def run(*a, ok=True):
        extra = ["--apply"] if a[0] == "propagate.py" else []
        p = subprocess.run([sys.executable, os.path.join(INFRA, "tools", a[0]), *a[1:], *extra, "--actor", "TEST"],
                           capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=TMP)
        if ok and p.returncode != 0:
            print("UNEXPECTED FAILURE", a, p.stdout[-600:], p.stderr[-600:])
        return p.returncode, p.stdout + p.stderr


    def st(cid):
        return R.index(R.load_claims())[cid]


    results = []
    if True:
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
        # ---------------- R03 scenarios ----------------
        # N1: a validated status change persists its new source
        src_line = next(i for i, l in enumerate(open(os.path.join(TMP, "Theory_work/Wave2/W2-FAC-PK/REPORT.md"),
                                                     encoding="utf-8").read().splitlines(), 1) if "PARTIAL" in l)
        run("propagate.py", "downgrade", "W2-FAC-PK:Thm-PATH", "--status", "PARTIAL", "--status-source",
            f"Theory_work/Wave2/W2-FAC-PK/REPORT.md:{src_line}", "--reason", "t")
        t = st("W2-FAC-PK:Thm-PATH")
        results.append(("R03-N1 downgrade persists status_source with the status",
                        t["status"] == "PARTIAL" and t["status_source"].endswith(f":{src_line}")))
        # N2: a self-bound consumes is reported as a self-edge
        run("registry.py", "set", "W2-LOC2:PLR", "consumes=P:SAND@W2-LOC2:PLR", "--reason", "t")
        g_ = R.Graph(R.load_claims())
        results.append(("R03-N2 self-bound property recorded as self-edge",
                        any(c == "W2-LOC2:PLR" for c, _ in g_.self_edges)))
        # F6 variants: negated / borrowed statuses
        fx = os.path.join(TMP, "neg_fixture.md")
        open(fx, "w", encoding="utf-8").write("Status: Not yet PROVED-CHECKED.\nX: OPEN\nY: PROVED-CHECKED\n")
        results.append(("R03-F6 'Not yet' is negated", R.status_at("PROVED-CHECKED", "neg_fixture.md:1") == "negated"))
        results.append(("R03-F6 status starting on a later line is not borrowed",
                        R.status_at("PROVED-CHECKED", "neg_fixture.md:2") != "ok"))
        # F10: the same route written two ways counts once
        results.append(("R03-F10 canonical span keys", R.span_key("Theory_work/INFRA/README.md:1") ==
                        R.span_key("Theory_work/INFRA/README.md:01")))
        # ---------------- R04 scenarios ----------------
        open(fx, "w", encoding="utf-8").write("A: NOT-PROVED-CHECKED\nB: PROVED-CHECKEDNESS\nC: PROVED-CHECKED.\n")
        results.append(("R04 'NOT-PROVED-CHECKED' is not PROVED-CHECKED", R.status_at("PROVED-CHECKED", "neg_fixture.md:1") != "ok"))
        results.append(("R04 'PROVED-CHECKEDNESS' is not PROVED-CHECKED", R.status_at("PROVED-CHECKED", "neg_fixture.md:2") != "ok"))
        results.append(("R04 plain token still accepted", R.status_at("PROVED-CHECKED", "neg_fixture.md:3") == "ok"))
        # R04-F8: D binds the same property to X and (independently) to YB; supersede X by YB, confirm, retract YB:
        # D must end with BOTH bindings back (X restored, independent YB kept) and be invalidated by YB's retraction
        XB, DB = "C-GROW:L1.1", "C-GROW:L6.6"
        run("registry.py", "add", "TEST:YB", "--file", STM, "--lines", "13-15", "--kind", "lemma", "--name", "YB",
            "--status", "PROVED-CHECKED", "--source", "Theory_work/Wave2/W2-FAC-A/REPORT.md:20",
            "--field", f"implies={XB}", "--field", f"gates={st(XB)['gates']}", "--reason", "t")
        run("registry.py", "set", DB, f"consumes=P:SAND@{XB}; P:SAND@TEST:YB", "--reason", "t")
        run("propagate.py", "supersede", XB, "--by", "TEST:YB", "--reason", "free")
        run("propagate.py", "confirm-repoint", DB, "--from", XB, "--to", "TEST:YB", "--checked-by", "t", "--reason", "t")
        after_confirm = R.split_list(st(DB)["consumes"])
        run("propagate.py", "retract", "TEST:YB", "--reason", "t")
        cons = R.split_list(st(DB)["consumes"])
        results.append(("R04-F8 confirm keeps one binding to YB (no duplicate)", after_confirm == ["P:SAND@TEST:YB"]))
        results.append(("R04-F8 revert restores X and keeps the independent YB binding; D SUSPECT",
                        f"P:SAND@{XB}" in cons and "P:SAND@TEST:YB" in cons and st(DB)["state"] == "SUSPECT"))
        # ---------------- R05 (HQ): nothing is written without --apply ----------------
        import hashlib
        def tree_digest():
            h = hashlib.sha256()
            for base in (R.REG, os.path.join(INFRA, "DECISIONS.md"), os.path.join(INFRA, "FAILED_ROUTES.md")):
                paths = [base] if os.path.isfile(base) else sorted(os.path.join(dp, f) for dp, _, fs in os.walk(base)
                                                                    for f in fs)
                for pth in paths:
                    h.update(pth.encode()); h.update(open(pth, "rb").read())
            return h.hexdigest(), sorted(os.listdir(os.path.join(INFRA, "issues"))) if os.path.isdir(
                os.path.join(INFRA, "issues")) else []
        before = tree_digest()
        for args in (["retract", "C-GROW:Thm-GROW", "--reason", "t"], ["suspect", "W1-GEN:L1", "--reason", "t"],
                     ["fail-route", "W2-LOC2:PLR", "--assumption", "A:P-POLY", "--route",
                      "Theory_work/INFRA/README.md:1 t", "--reason", "t"]):
            subprocess.run([sys.executable, os.path.join(INFRA, "tools", "propagate.py"), *args, "--actor", "TEST"],
                           capture_output=True, text=True, cwd=TMP)
        results.append(("R05 propagate without --apply writes nothing", tree_digest() == before))
        rc_ = subprocess.run([sys.executable, os.path.join(INFRA, "tools", "propagate.py"), "suspect", "W1-GEN:L1",
                              "--reason", "t", "--apply", "--issues-dir", TMP], capture_output=True, cwd=TMP).returncode
        results.append(("R05 --issues-dir outside INFRA/issues refused", rc_ != 0))

        # ---------------- R05 scenarios ----------------
        # F4: alias spelling of the pre-existing destination binding
        with open(os.path.join(R.REG, "aliases.tsv"), "a", encoding="utf-8", newline="\n") as fh:
            fh.write("YB2ALIAS\tTEST:YB2\ttest alias\n")
        XB2, DB2 = "C-GROW:L1.2", "C-GROW:L6.7"
        run("registry.py", "add", "TEST:YB2", "--file", STM, "--lines", "16-18", "--kind", "lemma", "--name", "YB2",
            "--status", "PROVED-CHECKED", "--source", "Theory_work/Wave2/W2-FAC-A/REPORT.md:20",
            "--field", f"implies={XB2}", "--field", f"gates={st(XB2)['gates']}", "--reason", "t")
        run("registry.py", "set", DB2, f"consumes=P:NA-TL@{XB2}; P:NA-TL@YB2ALIAS", "--reason", "t")
        run("propagate.py", "supersede", XB2, "--by", "TEST:YB2", "--reason", "free")
        run("propagate.py", "confirm-repoint", DB2, "--from", XB2, "--to", "TEST:YB2", "--checked-by", "t",
            "--reason", "t")
        run("propagate.py", "retract", "TEST:YB2", "--reason", "t")
        cons2 = R.split_list(st(DB2)["consumes"])
        results.append(("R05-F4 alias-spelled destination: revert restores X and keeps the alias binding",
                        f"P:NA-TL@{XB2}" in cons2 and "P:NA-TL@YB2ALIAS" in cons2))
        # F5: no __pycache__ written by the tools
        results.append(("R05-F5 no __pycache__ under tools/ after all runs",
                        not os.path.isdir(os.path.join(INFRA, "tools", "__pycache__"))))
        # F6: destinations outside INFRA are refused by the write guard
        try:
            R.safe_dest(os.path.join(TMP, "outside.txt"))
            ok6 = False
        except SystemExit:
            ok6 = True
        results.append(("R05-F6 write guard refuses a destination outside Theory_work/INFRA", ok6))
        # F2: foreign worktree under the sandbox root (no lock manifest) is never removed; a stale tool sandbox is
        foreign = os.path.join(run_ci.SANDBOX_ROOT, "sb-foreign-test")
        subprocess.run(["git", "-C", LIVE_ROOT, "worktree", "add", "--detach", foreign, "HEAD"], capture_output=True)
        code = ("import sys,os; sys.dont_write_bytecode=True; sys.path.insert(0, r'" + os.path.join(LIVE_INFRA, "ci")
                + "'); sys.argv=sys.argv[:1]; import run_ci; sb=run_ci.Sandbox(); sb.__enter__(); "
                "print(sb.path, flush=True); os._exit(0)")
        stale = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True).stdout.strip()
        probe = run_ci.Sandbox()
        probe.__enter__()
        probe.__exit__(None, None, None)
        results.append(("R05-F2 foreign worktree under the root (no manifest) is left untouched",
                        os.path.isdir(foreign)))
        results.append(("R05-F2 stale tool sandbox (owner dead, valid manifest) is removed",
                        bool(stale) and not os.path.exists(stale)))
        subprocess.run(["git", "-C", LIVE_ROOT, "worktree", "remove", "--force", foreign], capture_output=True)
        shutil.rmtree(foreign, ignore_errors=True)
        # Job: a script that spawns a long-lived child; after run_in the child must be gone
        spawn = os.path.join(TMP, "Theory_work", "INFRA", "tmp_spawn.py")
        open(spawn, "w").write("import subprocess,sys,time\n"
                               "c=subprocess.Popen([sys.executable,'-c','import time; time.sleep(120)'])\n"
                               "open('child.pid','w').write(str(c.pid))\nsys.exit(0)\n")
        logdir = os.path.join(TMP, "logs")
        os.makedirs(logdir, exist_ok=True)
        subprocess.run(["git", "-C", TMP, "add", "-f", "Theory_work/INFRA/tmp_spawn.py"], capture_output=True)
        subprocess.run(["git", "-C", TMP, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "t"],
                       capture_output=True)
        pidfile = os.path.join(TMP, "Theory_work", "INFRA", "child.pid")
        killed = None
        if os.name == "nt":
            import time as _t
            job = run_ci.Job()
            p = subprocess.Popen([sys.executable, spawn], cwd=os.path.dirname(spawn),
                                 creationflags=subprocess.CREATE_NEW_PROCESS_GROUP | 0x4)
            job.add(p)
            job.resume(p)
            p.wait(timeout=60)
            _t.sleep(1)
            cpid = int(open(pidfile).read())
            job.close()
            out = subprocess.run(["tasklist", "/FI", f"PID eq {cpid}", "/NH"], capture_output=True, text=True).stdout
            killed = str(cpid) not in out
        results.append(("R05-Job a child spawned by the script is killed with the Job (Windows)", killed is not False))

finally:
    SB.__exit__(None, None, None)
for name, ok in results:
    print("PASS" if ok else "FAIL", name)
sys.exit(0 if results and all(ok for _, ok in results) else 1)
