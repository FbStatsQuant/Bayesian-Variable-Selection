"""test_lifecycle.py — regression scenarios for the lifecycle tools (reviews R01-R05, INFRA R05-R06).

Never touches the live registry: it runs inside a CI Sandbox (ci/run_ci.py: a disposable detached git worktree of
HEAD, a strict child of the tool's sandbox root, owned through a held lock file), copies the CURRENT
Theory_work/INFRA folder (working copy) into it, runs real propagate.py / registry.py operations there, and removes
the sandbox at the end (also on errors; a killed run leaves a stale sandbox that the next Sandbox cleans up).
Run: python Theory_work/INFRA/tools/test_lifecycle.py   (exit code 1 if any scenario fails)"""
import importlib.util, os, shutil, subprocess, sys, unicodedata
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
    # the manifest tool (Wave 3 rule 15) is part of the acceptance path: test the working copy, not HEAD's
    shutil.copy2(os.path.join(LIVE_ROOT, "Theory_work", "Wave3", "tools", "manifest.py"),
                 os.path.join(TMP, "Theory_work", "Wave3", "tools", "manifest.py"))
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

        # ---------------- pipeline review (Wave 3 R01): R02-R06 ----------------
        import json as _json

        def tool(script, *args):  # tools without --actor (ingest, check)
            p = subprocess.run([sys.executable, os.path.join(INFRA, "tools", script), *args], capture_output=True,
                               text=True, encoding="utf-8", errors="replace", cwd=TMP)
            return p.returncode, p.stdout + p.stderr

        def findings(*extra):
            out_json = os.path.join(TMP, "chk.json")
            if os.path.exists(out_json):
                os.remove(out_json)  # never read a stale result
            rc_, out_ = tool("check.py", "--quiet", "--json", out_json, *extra)
            if not os.path.exists(out_json):
                return [("ERROR", "TOOL-FAILED", "-", out_[-300:])]
            return [(o["severity"], o["check"], o["id"], o["message"])
                    for o in _json.load(open(out_json, encoding="utf-8"))["findings"]]

        def put(rel, text):
            fp = os.path.join(TMP, rel)
            os.makedirs(os.path.dirname(fp), exist_ok=True)
            open(fp, "w", encoding="utf-8", newline="\n").write(text)
            return fp

        def frag(name, objs):
            return put(f"frag_{name}.jsonl", "".join(_json.dumps(o, ensure_ascii=False) + "\n" for o in objs))

        reg_digest = lambda: tree_digest()[0]  # noqa: E731
        FIX = "Theory_work/WaveT/FIX"
        put(f"{FIX}/STATEMENT.md", "## Lemma BR\nLemma BR. Property SAND holds.\n## Theorem THM\nTheorem THM. Under "
            "P:SAND the posterior concentrates.\n## Lemma W\nLemma W-hyp. A weak lemma.\n## Theorem H\nTheorem H. "
            "Then Z holds.\n## Theorem H2\nTheorem H2. Assume Lemma W-hyp holds. Then Z holds.\n## Other\nOther.\n")
        put(f"{FIX}/REPORT.md", "# Fixture report\nPROVED-CHECKED\n\nPROVED (by this seat, unchecked)\n"
            "PROVED-CHECKED conditional on Lemma W-hyp\n")
        TRA = "Theory_work/WaveT/TR-A"
        put(f"{TRA}/STATEMENT.md", "## Lemma L\nLemma L. X holds.\n")
        put(f"{TRA}/REPORT.md", "# TR-A report\nPROVED-CHECKED\n")
        base = subprocess.run(["git", "-C", TMP, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
        subprocess.run(["git", "-C", TMP, "add", "-f", TRA], capture_output=True)
        subprocess.run(["git", "-C", TMP, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "fixture"],
                       capture_output=True)
        sha = subprocess.run(["git", "-C", TMP, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
        ok_ck = dict(status="PROVED-CHECKED", status_source=f"{FIX}/REPORT.md:2")
        weak = dict(status="PROVED (by this seat, unchecked)", status_source=f"{FIX}/REPORT.md:4")

        # R03: bridge (JSONL) + consumer (REPORT.md REGISTRY block) round-trip consumes / method pins / binding rows
        rc, out = tool("ingest.py", "claims", frag("br", [dict(ticket="TT-A", local_id="BR", kind="lemma",
                                                               name="Lemma BR", file=f"{FIX}/STATEMENT.md",
                                                               lines=[1, 2], **ok_ck)]), "--apply")
        results.append(("R03 bridge lemma ingested", rc == 0 and "TT-A:BR" in R.index(R.load_claims())))
        blk = put(f"{FIX}/BLOCK.md", "# report\n\n```\nREGISTRY\n"
                  "claim: TT-B:THM | kind: theorem | statement: STATEMENT.md:3-4 | premises: STATEMENT.md:1-2\n"
                  "status: PROVED-CHECKED | status_source: REPORT.md:2\n"
                  "assumptions: A:P-POLY\nconsumes: P:SAND@TT-A:BR\n"
                  "conclusion: posterior: concentrates | rate: r_n | scope: fixture\n"
                  f"depends_on: none\nmethod_commit: {sha} | method_components: core\n"
                  "binding: A:P-POLY forced by TT-A:BR via union bound [artefact-threshold]\n"
                  "gates: correct:PASS(reviews/x.md)\n```\n")
        rc_c, out_c = tool("ingest.py", "convert", blk)
        conv = _json.loads(out_c.splitlines()[0]) if rc_c == 0 else {}
        results.append(("R04 REPORT REGISTRY block converts to ingest JSONL (paths repo-relative)",
                        conv.get("file") == f"{FIX}/STATEMENT.md" and conv.get("premises") == [f"{FIX}/STATEMENT.md:1-2"]
                        and conv.get("consumes") == ["P:SAND@TT-A:BR"] and conv.get("headline") == ""))
        rc, out = tool("ingest.py", "claims", blk, "--apply")
        b = R.index(R.load_claims()).get("TT-B:THM", {})
        bind = [x for x in R.load_binding() if x["headline"] == "TT-B:THM"]
        results.append(("R03 ingest keeps consumes binding, method_commit, method_components, binding row",
                        rc == 0 and b.get("consumes") == "P:SAND@TT-A:BR" and b.get("method_commit") == sha
                        and b.get("method_components") == "core" and len(bind) == 1
                        and bind[0]["binding_claim"] == "TT-A:BR"))
        results.append(("R03 bound bridge creates the proof-use edge",
                        "proof:P:SAND" in R.Graph(R.load_claims()).uses.get(("TT-B:THM", "TT-A:BR"), set())))
        run("propagate.py", "suspect", "TT-A:BR", "--reason", "t")
        results.append(("R03 ingested bridge consumer becomes SUSPECT when its bridge is suspected",
                        st("TT-B:THM")["state"] == "SUSPECT"))
        d0 = reg_digest()
        rc, out = tool("ingest.py", "claims", frag("unk", [dict(ticket="TT-U", local_id="X", kind="lemma",
                                                                file=f"{FIX}/STATEMENT.md", lines=[11, 12],
                                                                bogus_field=1, **ok_ck)]), "--apply")
        results.append(("R03 unknown field rejected (exit 1, nothing written)",
                        rc != 0 and "bogus_field" in out and reg_digest() == d0))
        bad_blk = put(f"{FIX}/BAD.md", "REGISTRY\nclaim: TT-U:Y | kind: lemma | statement: STATEMENT.md:11-12\n"
                      "colour: blue\n")
        rc, out = tool("ingest.py", "convert", bad_blk)
        results.append(("R04 unknown REGISTRY-block field rejected by the converter", rc != 0 and "colour" in out))
        gap_blk = put(f"{FIX}/GAP.md", "REGISTRY\nclaim: TT-U:Z | kind: lemma | statement: STATEMENT.md:11-12\n\n"
                      "gates: correct:PASS(c.md)\n\nshade: grey\n\nSome prose after the block.\n")
        rc, out = tool("ingest.py", "convert", gap_blk)
        results.append(("Sol-4 blank lines inside a block: later fields kept, unknown field after a gap reported",
                        rc != 0 and "shade" in out and "correct:PASS(c.md)" in out and "Some prose" not in out))
        # Sol-1: a failure while replacing the 2nd file restores the 1st (transactional write_many)
        f1, f2 = os.path.join(R.REG, "zz_t1.tsv"), os.path.join(R.REG, "zz_t2.tsv")
        for f_ in (f1, f2):
            open(f_, "w", encoding="utf-8").write("h\nold\n")
        real_replace = R.os.replace

        def flaky(src, dst):
            if dst.endswith("zz_t2.tsv"):
                raise OSError("injected")
            return real_replace(src, dst)
        R.os.replace = flaky
        try:
            R.write_many([(f1, ["h"], [{"h": "new"}]), (f2, ["h"], [{"h": "new"}])])
            raised = False
        except OSError:
            raised = True
        finally:
            R.os.replace = real_replace
        left = [f_ for f_ in os.listdir(R.REG) if f_.startswith("zz_t") and not f_.endswith(".tsv")]
        results.append(("Sol-1 write_many: a failed 2nd replacement restores the 1st; no .tmp/.bak left",
                        raised and open(f1).read() == "h\nold\n" and not left))
        for f_ in (f1, f2):
            os.remove(f_)
        # Sol-6: BVS_STAGE_INFRA must be a tool-made disposable stage
        p6 = subprocess.run([sys.executable, os.path.join(INFRA, "tools", "check.py"), "--quiet"], cwd=TMP,
                            capture_output=True, text=True, env=dict(os.environ, BVS_STAGE_INFRA=TMP))
        results.append(("Sol-6 BVS_STAGE_INFRA pointing at the repository is refused",
                        p6.returncode != 0 and "refusing BVS_STAGE_INFRA" in p6.stdout + p6.stderr))

        # R04: all-or-nothing (claims and splits), staged check on a copy
        good = dict(ticket="TT-G", local_id="G", kind="lemma", file=f"{FIX}/STATEMENT.md", lines=[11, 12], **ok_ck)
        badrow = dict(ticket="TT-G", local_id="H", kind="lemma", file=f"{FIX}/STATEMENT.md", lines=[11, 12],
                      depends_on=["NO-SUCH:CLAIM"], **ok_ck)
        fg = frag("mixed", [good, badrow])
        rc_d, _ = tool("ingest.py", "claims", fg)
        rc_a, out = tool("ingest.py", "claims", fg, "--apply")
        results.append(("R04 one bad row: nothing written, exit 1 (dry run and --apply)",
                        rc_d != 0 and rc_a != 0 and reg_digest() == d0 and "TT-G:G" not in R.index(R.load_claims())))
        sp = put("split_bad.tsv", "kind_of_row\tparent\tid\tfield\tvalue\tevidence\n"
                 f"part\tTT-A:BR\tTT-A:BR.a\tlines\t1-2\t\npart\tTT-A:BR\tTT-A:BR.a\tfile\t{FIX}/STATEMENT.md\t\n"
                 "repoint\t\tTT-B:THM\tedge\tNOPE@stmt => TT-A:BR.a@stmt\t\n")
        rc_d, _ = tool("ingest.py", "splits", sp)
        rc_a, _ = tool("ingest.py", "splits", sp, "--apply")
        results.append(("R04 split spec with a problem: nothing written, exit 1 (dry run and --apply)",
                        rc_d != 0 and rc_a != 0 and reg_digest() == d0))
        rc, out = tool("ingest.py", "claims", frag("good", [good]), "--staged")
        results.append(("R04 --staged runs the full check on a copy; live registry untouched",
                        "STAGED check.py on the proposed registry" in out and "introduced by this claims fragment: 0"
                        in out and reg_digest() == d0 and "TT-G:G" not in R.index(R.load_claims())))
        rc, out = tool("ingest.py", "claims", frag("mixed2", [good, badrow]), "--staged")
        results.append(("R04 --staged with a bad row: refused before staging, exit 1", rc != 0 and reg_digest() == d0))

        # R02: rollback of a merged ticket keeps tombstones; dependents end SUSPECT; no dangling ids
        rc, out = tool("ingest.py", "claims", frag("tr", [
            dict(ticket="TR-A", local_id="L", kind="lemma", name="Lemma L", file=f"{TRA}/STATEMENT.md", lines=[1, 2],
                 status="PROVED-CHECKED", status_source=f"{TRA}/REPORT.md:2"),
            dict(ticket="TR-B", local_id="T", kind="theorem", file=f"{FIX}/STATEMENT.md", lines=[11, 12],
                 depends_on=["TR-A:L@stmt"], **ok_ck),
            dict(ticket="TR-C", local_id="U", kind="corollary", file=f"{FIX}/STATEMENT.md", lines=[11, 12],
                 depends_on=["TR-B:T"], **ok_ck)]), "--apply")
        results.append(("R02 fixture: claim A (ticket TR-A), B depends on A, C on B", rc == 0))
        rc, _ = run("propagate.py", "retract", "TR-A:L", "--archive", base, "--reason", "t", ok=False)
        results.append(("R02 tombstone archive lacking the statement refused", rc != 0 and
                        st("TR-A:L")["state"] == "ACTIVE"))
        rc, _ = run("propagate.py", "rollback-ticket", "TR-A", "--reason", "t", ok=False)
        results.append(("R02 rollback-ticket --apply without --archive refused",
                        rc != 0 and st("TR-A:L")["state"] == "ACTIVE"))
        run("registry.py", "set", "TR-A:L", f"tex={TRA}/STATEMENT.md:1-2", "--reason", "t")  # Sol-5: tex in ticket
        d1 = reg_digest()
        rc, out = tool("propagate.py", "rollback-ticket", "TR-A", "--archive", sha, "--reason", "t")
        results.append(("R02 rollback-ticket dry run prices on the current graph and writes nothing",
                        rc == 0 and "TR-B:T | ACTIVE | SUSPECT" in out and reg_digest() == d1))
        rc, out = run("propagate.py", "rollback-ticket", "TR-A", "--archive", sha, "--reason", "t")
        shutil.rmtree(os.path.join(TMP, TRA))  # = reverting the ticket's non-registry files, keeping the rows
        F = findings()
        tr_err = [f for f in F if f[0] == "ERROR" and f[2].startswith("TR-")]
        a_ = st("TR-A:L")
        results.append(("R02 rolled-back claim kept as a RETRACTED tombstone on the archive",
                        rc == 0 and a_["state"] == "RETRACTED" and f"archive:{sha}" in a_["evidence"]))
        results.append(("R02 dependents SUSPECT (direct and transitive)",
                        st("TR-B:T")["state"] == "SUSPECT" and st("TR-C:U")["state"] == "SUSPECT"))
        results.append(("R02 after the revert: no dangling ids, tombstone (statement, status, tex) verified at its "
                        "archive (no TR ERROR)",
                        not tr_err and not [f for f in F if f[1].startswith("C3-dangling")]))
        run("registry.py", "set", "TR-A:L", f"evidence=archive:{base}", "--reason", "t")
        results.append(("R02 tombstone with a wrong archive is a check ERROR",
                        any(f[:3] == ("ERROR", "C2-tombstone", "TR-A:L") for f in findings())))

        # R05 / R06: check.py --acceptance
        rc, out = tool("ingest.py", "claims", frag("ac", [
            dict(ticket="AC", local_id="W", kind="lemma", name="Lemma W-hyp", file=f"{FIX}/STATEMENT.md",
                 lines=[5, 6], **weak),
            dict(ticket="AC", local_id="H", kind="theorem", file=f"{FIX}/STATEMENT.md", lines=[7, 8],
                 depends_on=["AC:W@stmt"], headline="yes", strength=dict(conclusion="posterior: z",
                                                                          gates="correct:PASS(reviews/c.md)"), **ok_ck),
            dict(ticket="AC", local_id="H2", kind="theorem", file=f"{FIX}/STATEMENT.md", lines=[9, 10],
                 depends_on=["AC:W@stmt"], **ok_ck)]), "--apply")

        def acc_err(cid, chk):
            return [f for f in findings("--acceptance", cid) if f[0] == "ERROR" and f[1] == chk and f[2] == cid]
        results.append(("R05 acceptance: headline without lit/necessity/better is an ERROR",
                        rc == 0 and len(acc_err("AC:H", "A1-gates")) == 3))
        G = "correct:PASS(c.md); lit:PASS(l.md); necessity:PASS(n.md); better:PASS(b.md)"
        run("registry.py", "set", "AC:H", f"gates={G}; better-proposal:P1(b.md)", "--reason", "t")
        e1 = acc_err("AC:H", "A2-better")
        run("registry.py", "set", "AC:H", f"gates={G}; better-proposal:P1(b.md); better-disposition:P1=deferred(x)",
            "--reason", "t")
        e2 = acc_err("AC:H", "A2-better")
        run("registry.py", "set", "AC:H", "gates=correct:PASS(c.md); lit:PASS(l.md); necessity:PASS(n.md); "
            "better:PASS(b.md, proposal C+ adopted, approval pending)", "--reason", "t")
        e3 = acc_err("AC:H", "A2-better")
        run("registry.py", "set", "AC:H", f"gates={G}; better-proposal:P1(b.md); "
            "better-disposition:P1=declined(DECISIONS.md)", "--reason", "t")
        e4 = acc_err("AC:H", "A2-better") + acc_err("AC:H", "A1-gates")
        results.append(("R05 better proposal without disposition / with a deferral / only in PASS text: ERROR",
                        len(e1) == 1 and len(e2) == 1 and len(e3) == 1))
        results.append(("R05 every gate passed and the proposal declined with evidence: no gate ERROR", not e4))
        run("registry.py", "set", "AC:H", f"gates={G}; lit:FAIL(l.md); not-lit:PASS(x)", "--reason", "t")
        e5 = acc_err("AC:H", "A1-gates")
        results.append(("Sol-3 `lit:FAIL; not-lit:PASS` does not pass the lit gate (contradiction ERROR)",
                        any("lit" in f[3] for f in e5)))
        run("registry.py", "set", "AC:H", "acks=AC:W", "--reason", "t")
        results.append(("R06 PROVED-CHECKED on an author-only input: ERROR, not waived by an ack",
                        len(acc_err("AC:H", "A3-assurance")) == 1))
        run("registry.py", "set", "AC:H", "depends_on=AC:W@hyp", "--reason", "t")
        results.append(("Sol-2 declared @hyp but not named in the statement: still ERROR",
                        len(acc_err("AC:H", "A3-assurance")) == 1))
        results.append(("Sol-2 named in the statement but not declared @hyp (incidental mention): ERROR",
                        len(acc_err("AC:H2", "A3-assurance")) == 1))
        run("registry.py", "set", "AC:H2", "depends_on=AC:W@hyp", "--reason", "t")
        # since R02 item 5 the waiver also needs the status to carry the condition ("conditional on ...")
        run("registry.py", "correct-status", "AC:H2", "--status", "PROVED-CHECKED conditional on Lemma W-hyp",
            "--source", f"{FIX}/REPORT.md:5", "--reason", "t")
        results.append(("R06 input declared @hyp, stated as a hypothesis in the statement, status 'conditional on' "
                        "it: no ERROR",
                        not acc_err("AC:H2", "A3-assurance")))
        rc, out = tool("check.py", "--quiet", "--acceptance", "AC:H")
        results.append(("R05/R06 acceptance exits 1 and says REFUSED", rc != 0 and "REFUSED" in out))

        # ---------------- pipeline review R02 (Wave 3): F1 F2 F3 F6, R04-R07, R10, Sol-1 Sol-2 Sol-4 ----------------
        def git_commit(paths, msg):
            subprocess.run(["git", "-C", TMP, "add", "-f", *paths], capture_output=True)
            subprocess.run(["git", "-C", TMP, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", msg],
                           capture_output=True)
            return subprocess.run(["git", "-C", TMP, "rev-parse", "HEAD"], capture_output=True,
                                  text=True).stdout.strip()

        def acc_errs(cid, *more):
            return [f for f in findings("--acceptance", cid, *more) if f[0] == "ERROR" and f[2] == cid
                    and (f[1].startswith("A") or f[1] == "TOOL-FAILED")]

        Q = "Theory_work/WaveT/Q"
        MANP = os.path.join(TMP, "Theory_work", "Wave3", "tools", "manifest.py")

        def man(*a):  # the Wave 3 manifest tool (freeze / verify / bind), run from the sandbox root
            p = subprocess.run([sys.executable, MANP, *map(str, a)], capture_output=True, text=True,
                               encoding="utf-8", errors="replace", cwd=TMP)
            return p.returncode, p.stdout + p.stderr

        def vline(d, seat, score="8.5", res="PASS", rnd="R1"):  # the council verdict line (LIFECYCLE 4.1)
            return f"COUNCIL-VERDICT round={rnd} manifest={d} seat={seat} score={score} gates={res}\n"
        put(f"{Q}/STATEMENT.md", "## Lemma X\nLemma QX. X holds.\n## Lemma Y\nLemma QY. Y holds.\n## Lemma Weak\n"
            "Lemma Weak. A weak lemma.\n## Theorem H\nUnlike Lemma Weak, this result assumes nothing.\n## Theorem E\n"
            "Theorem QE. Then E holds.\n## Other\nOther text.\n")
        put(f"{Q}/REPORT.md", "# Q report\nPROVED-CHECKED\nPARTIAL\nPROVED-CHECKED conditional on Lemma Weak\n"
            "PROVED-CHECKED not conditional on Lemma Weak\n"
            "PROVED-CHECKED conditional on Other. Unlike Lemma Weak, no assumption is needed.\n"
            "PROVED-CHECKED conditional on Lemma Weak Extra\n")
        os.makedirs(os.path.join(TMP, Q, "reviews"), exist_ok=True)
        man("freeze", Q, f"{Q}/reviews/MANIFEST_R1.txt")  # R03-N2: a real frozen manifest of the ticket folder
        DG = open(os.path.join(TMP, Q, "reviews", "MANIFEST_R1.txt"), encoding="utf-8").readline().split()[1]
        for s_, sc_ in (("sol", "8.5"), ("opus", "8.2")):
            put(f"{Q}/reviews/R1_{s_}.md", f"Council round 1 ({s_}).\nReviewed MANIFEST {DG}\nScore {sc_}, all gates "
                f"PASS\n\n{vline(DG, s_, sc_)}")
        put(f"{Q}/reviews/R1_stale.md", "Council round 1 on another snapshot.\nMANIFEST " + "0" * 64 + "\n")
        put(f"{Q}/reviews/gate.md", "gate review\n")
        qsha = git_commit([Q], "Q fixture")
        COUNCIL = f"R1; MANIFEST {DG}; sol=8.5 PASS(reviews/R1_sol.md); opus=8.2 PASS(reviews/R1_opus.md)"
        qck = dict(status="PROVED-CHECKED", status_source=f"{Q}/REPORT.md:2")
        qpart = dict(status="PARTIAL", status_source=f"{Q}/REPORT.md:3")
        qcond = dict(status="PROVED-CHECKED conditional on Lemma Weak", status_source=f"{Q}/REPORT.md:4")

        def qrow(loc, lines, **kw):
            return dict(ticket=kw.pop("ticket", "Q"), local_id=loc, kind=kw.pop("kind", "lemma"),
                        file=f"{Q}/STATEMENT.md", lines=lines, **kw)

        # F1: an ack must not restore acceptance (or allow CLEAR) while a consumed claim is not ACTIVE
        rc, out = tool("ingest.py", "claims", frag("q1", [
            qrow("X", [1, 2], name="Lemma QX", council=COUNCIL, **qck),
            qrow("Y", [3, 4], name="Lemma QY", depends_on=["Q:X@stmt"], council=COUNCIL, **qck)]), "--apply")
        results.append(("R10 valid council record (R<k>, MANIFEST, 2 seats >= 8.0 PASS, reviews quote it): accepted",
                        rc == 0 and not acc_errs("Q:X", "Q:Y")))
        run("propagate.py", "suspect", "Q:X", "--reason", "known gap")
        run("registry.py", "set", "Q:Y", "acks=Q:X", "--reason", "ack gap")
        rc, out = run("propagate.py", "clear", "Q:Y", "--reason", "ack permits clear", ok=False)
        results.append(("F1 clear refused while an input is SUSPECT, even with an ack",
                        rc != 0 and st("Q:Y")["state"] == "SUSPECT"))
        results.append(("F1 acceptance of the dependent refused", bool(acc_errs("Q:Y"))))
        rc, out = tool("ingest.py", "claims", frag("q2", [
            qrow("Z", [3, 4], depends_on=["Q:X@stmt"], council=COUNCIL, **qck),
            qrow("Z2", [3, 4], depends_on=["Q:Z@proof:E_n"], council=COUNCIL, **qck)]), "--apply")
        run("registry.py", "set", "Q:Z", "acks=Q:X", "--reason", "t")
        results.append(("F1 acceptance: ACTIVE claim on a SUSPECT (acked) input refused (A0-inputs)",
                        rc == 0 and any(f[1] == "A0-inputs" for f in acc_errs("Q:Z"))))
        results.append(("F1 acceptance: SUSPECT input reached transitively through @proof refused",
                        any(f[1] == "A0-inputs" and "Q:X" in f[3] for f in acc_errs("Q:Z2"))))
        run("propagate.py", "clear", "Q:X", "--reason", "repaired")
        rc, _ = run("propagate.py", "clear", "Q:Y", "--reason", "input repaired")
        results.append(("F1 clear allowed once the input is ACTIVE again", rc == 0 and st("Q:Y")["state"] == "ACTIVE"))

        # R06 / Sol-2: @hyp needs a conditional status, carried by every descendant
        rc, out = tool("ingest.py", "claims", frag("q3", [
            qrow("W", [5, 6], name="Lemma Weak", **qpart),
            qrow("H", [7, 8], kind="theorem", depends_on=["Q:W@hyp"], council=COUNCIL, **qck),
            qrow("HC", [7, 8], kind="theorem", depends_on=["Q:W@hyp"], council=COUNCIL, **qcond)]
            + [qrow(f"HN{k}", [7, 8], kind="theorem", depends_on=["Q:W@hyp"], council=COUNCIL,
                    status=stx, status_source=f"{Q}/REPORT.md:{k + 4}")
               for k, stx in ((1, "PROVED-CHECKED not conditional on Lemma Weak"),
                              (2, "PROVED-CHECKED conditional on Other. Unlike Lemma Weak, no assumption is needed."),
                              (3, "PROVED-CHECKED conditional on Lemma Weak Extra"))]), "--apply")
        results.append(("Sol-R1 negated / other-sentence / longer-name 'conditional on' does not carry the condition "
                        "(A3 ERROR each)", all(any(f[1] == "A3-assurance" for f in acc_errs(f"Q:HN{k}"))
                                               for k in (1, 2, 3))))
        results.append(("R06/Sol-2 'Unlike Lemma Weak, this result assumes nothing.' + @hyp + unconditional "
                        "PROVED-CHECKED: ERROR", rc == 0 and any(f[1] == "A3-assurance" for f in acc_errs("Q:H"))))
        results.append(("R06 @hyp + named + status 'conditional on Lemma Weak': no A3 ERROR",
                        not [f for f in acc_errs("Q:HC") if f[1].startswith("A3")]))
        rc, out = tool("ingest.py", "claims", frag("q4", [
            qrow("E", [9, 10], kind="corollary", depends_on=["Q:HC@stmt"], council=COUNCIL, **qck),
            qrow("EC", [9, 10], kind="corollary", depends_on=["Q:HC@stmt"], council=COUNCIL, **qcond)]), "--apply")
        results.append(("R06 descendant of a conditional result with an unconditional status: ERROR",
                        rc == 0 and any(f[1] == "A3-condition" for f in acc_errs("Q:E"))))
        results.append(("R06 descendant carrying 'conditional on Lemma Weak': no A3 ERROR",
                        not [f for f in acc_errs("Q:EC") if f[1].startswith("A3")]))
        results.append(("R06 accepting the conditional result flags its unconditional descendant",
                        any(f[1] == "A3-condition" and "Q:E" in f[3] for f in acc_errs("Q:HC"))))
        run("propagate.py", "suspect", "Q:W", "--reason", "t")
        rc_hc, _ = run("propagate.py", "clear", "Q:HC", "--reason", "conditional result stands", ok=False)
        rc_h, _ = run("propagate.py", "clear", "Q:H", "--reason", "t", ok=False)
        results.append(("R06 clear over a non-ACTIVE @hyp input: allowed only with a conditional status",
                        rc_hc == 0 and st("Q:HC")["state"] == "ACTIVE" and rc_h != 0 and st("Q:H")["state"] == "SUSPECT"))
        run("registry.py", "set", "Q:HN1", "acks=Q:W", "--reason", "t")
        rc_n = [run("propagate.py", "clear", f"Q:HN{k}", "--reason", "t", ok=False)[0] for k in (1, 2, 3)]
        results.append(("Sol-R1 clear over a SUSPECT @hyp input refused for the negated / misplaced / longer-name "
                        "conditions (ack included)", all(rc_ != 0 for rc_ in rc_n)
                        and all(st(f"Q:HN{k}")["state"] == "SUSPECT" for k in (1, 2, 3))))

        # F2 / R05: gate evidence must resolve; correctness evidence for every checked claim; R10 council format
        G4 = "; ".join(f"{k}:PASS(does-not-exist.md)" for k in ("correct", "lit", "necessity", "better"))
        rc, out = tool("ingest.py", "claims", frag("q5", [
            qrow("QH", [11, 12], kind="theorem", headline="yes", strength=dict(conclusion="posterior: z", gates=G4),
                 **qck),
            qrow("QL", [11, 12], **qck)]), "--apply")
        e = acc_errs("Q:QH")
        results.append(("F2 headline gates citing a nonexistent file: one ERROR per gate",
                        rc == 0 and len([f for f in e if f[1] == "A1-evidence"]) == 4))
        results.append(("R10 checked headline without a council record: ERROR", any(f[1] == "A4-council" for f in e)))
        e = acc_errs("Q:QL")
        results.append(("F2 non-headline checked lemma without correctness evidence: ERROR",
                        any(f[1] == "A1-correct" for f in e) and any(f[1] == "A4-council" for f in e)))
        run("registry.py", "set", "Q:QL", f"gates=correct:PASS(reviews/gate.md@{base})", "--reason", "t")
        e_pin_bad = [f for f in acc_errs("Q:QL") if f[1] == "A1-evidence"]
        run("registry.py", "set", "Q:QL", f"gates=correct:PASS(reviews/gate.md@{qsha})", "--reason", "t")
        e_pin_ok = [f for f in acc_errs("Q:QL") if f[1] == "A1-evidence"]
        results.append(("F2 evidence pinned to a commit must exist at that commit", bool(e_pin_bad) and not e_pin_ok))
        later_ok = []
        for gv in (f"Theory_work/WaveT/Q/reviews/gate.md missing@name.md", "reviews/gate.md missing.longextension",
                   f"reviews/gate.md@{qsha}", f"reviews@{qsha}"):
            run("registry.py", "set", "Q:QL", f"gates=correct:PASS({gv})", "--reason", "t")
            if not [f for f in acc_errs("Q:QL") if f[1] == "A1-evidence"]:
                later_ok.append(gv)
        results.append(("Sol-R3/R4 later path-like tokens (x@y.md, x.longextension) and a pinned directory are "
                        "validated", later_ok == [f"reviews/gate.md@{qsha}"]))
        run("registry.py", "set", "Q:QL", f"gates=correct:PASS(reviews/gate.md@{qsha})", "--reason", "t")
        bad_councils = {
            "seat below 8.0": f"R1; MANIFEST {DG}; sol=7.9 PASS(reviews/R1_sol.md); opus=8.2 PASS(reviews/R1_opus.md)",
            "a seat with a failed gate": f"R1; MANIFEST {DG}; sol=8.5 FAIL(reviews/R1_sol.md); "
                                         "opus=8.2 PASS(reviews/R1_opus.md)",
            "no MANIFEST": "R1; sol=8.5 PASS(reviews/R1_sol.md); opus=8.2 PASS(reviews/R1_opus.md)",
            "review not quoting the digest": f"R1; MANIFEST {DG}; sol=8.5 PASS(reviews/R1_sol.md); "
                                             "opus=8.2 PASS(reviews/R1_stale.md)",
            "one seat": f"R1; MANIFEST {DG}; sol=8.5 PASS(reviews/R1_sol.md)",
            "same review file for both seats": f"R1; MANIFEST {DG}; sol=8.5 PASS(reviews/R1_sol.md); "
                                               "opus=8.5 PASS(reviews/R1_sol.md)",
            "legacy free text": "Codex 8.6 / Opus 8.3, round 1",
            "missing review file": f"R1; MANIFEST {DG}; sol=8.5 PASS(reviews/nope.md); opus=8.2 PASS(reviews/R1_opus.md)",
            "same file in another case (Sol-R2)": f"R1; MANIFEST {DG}; sol=8.5 PASS(reviews/R1_sol.md); "
                                                  "opus=8.5 PASS(reviews/R1_SOL.md)",
            "same file once pinned (Sol-R2)": f"R1; MANIFEST {DG}; sol=8.5 PASS(reviews/R1_sol.md); "
                                              f"opus=8.5 PASS(reviews/R1_sol.md@{qsha})",
        }
        bad_ok = []
        for lab, cval in bad_councils.items():
            run("registry.py", "set", "Q:QL", f"council={cval}", "--reason", "t")
            if not any(f[1] == "A4-council" for f in acc_errs("Q:QL")):
                bad_ok.append(lab)
        results.append(("R10 malformed / failing council records are ERRORs: " + ", ".join(bad_councils),
                        not bad_ok))
        run("registry.py", "set", "Q:QL", f"council={COUNCIL}", "--reason", "t")
        results.append(("R10 valid council alone supplies the correctness evidence of a lemma",
                        not acc_errs("Q:QL")))

        # F3 / R04: --staged also runs acceptance on the ids it ingests
        d0 = reg_digest()
        rc, out = tool("ingest.py", "claims", frag("q_nogates", [
            qrow("NOGATES", [11, 12], kind="theorem", headline="yes", strength=dict(conclusion="posterior: z"),
                 **qck)]), "--staged")
        results.append(("F3 --staged runs --acceptance on the ingested ids: A1 ERRORs printed, exit 1, live untouched",
                        rc != 0 and "A1-gates" in out and "Q:NOGATES" in out and "acceptance" in out
                        and reg_digest() == d0))

        # Sol-4: one grammar inside a REGISTRY block
        g0 = put(f"{Q}/gap0.md", "REGISTRY\nclaim: T:X | kind: theorem | statement: STATEMENT.md:1-1\n\n"
                 "gates:correct:PASS(c.md)\nshade: grey\n")
        rc, out = tool("ingest.py", "convert", g0)
        try:
            conv = _json.loads(out.splitlines()[0])
        except (ValueError, IndexError):
            conv = {}
        results.append(("Sol-4 zero-space field after a blank line kept; unknown field after it reported",
                        rc != 0 and "shade" in out and (conv.get("strength") or {}).get("gates") == "correct:PASS(c.md)"))
        g1 = put(f"{Q}/gap1.md", "```\nREGISTRY\nclaim: T:X | kind: theorem | statement: STATEMENT.md:1-1\n\n"
                 "Some prose inside the fence.\ngates: correct:PASS(c.md)\n```\n")
        rc, out = tool("ingest.py", "convert", g1)
        try:
            conv = _json.loads(out.splitlines()[0])
        except (ValueError, IndexError):
            conv = {}
        results.append(("Sol-4 a non-field line inside a fenced block is an error and does not end the block",
                        rc != 0 and "Some prose" in out and (conv.get("strength") or {}).get("gates") == "correct:PASS(c.md)"))

        g2 = put(f"{Q}/gap2.md", "~~~\nREGISTRY\nclaim: T:X | kind: theorem | statement: STATEMENT.md:1-1\n\n"
                 "# heading\nshade:grey\n~~~\n")
        rc, out = tool("ingest.py", "convert", g2)
        results.append(("Sol-R6 tilde-fenced block: a heading inside it and an unknown zero-space field are reported",
                        rc != 0 and "heading" in out and "shade" in out))
        g3 = put(f"{Q}/gap3.md", "````\nREGISTRY\nclaim: T:X | kind: theorem | statement: STATEMENT.md:1-1\n```\n"
                 "gates:correct:PASS(c.md)\n````\n")
        rc, out = tool("ingest.py", "convert", g3)
        results.append(("Sol-R6 a shorter inner fence does not close a longer fence (reported, block continues)",
                        rc != 0 and "```" in out and "correct:PASS(c.md)" in out))
        # self-review hardening: negated / embedded "conditional on"; pinned evidence must be a file; path case
        nm_ = ["Q:W", "Lemma Weak"]
        results.append(("R06 'unconditional on X' / 'not conditional on X' do not carry the condition; the plain "
                        "clause does", not R.conditional_on("PROVED-CHECKED, unconditional on Lemma Weak", nm_)
                        and not R.conditional_on("PROVED-CHECKED (not conditional on Lemma Weak)", nm_)
                        and R.conditional_on("PROVED-CHECKED conditional on Lemma Weak", nm_) == "Lemma Weak"))
        qrow_ = {"file": f"{Q}/STATEMENT.md", "status_source": f"{Q}/REPORT.md:2"}
        results.append(("F2 pinned evidence naming a directory (git tree) does not resolve; a pinned file does",
                        R.resolve_evidence(f"reviews@{qsha}", qrow_)[2] is not None
                        and R.resolve_evidence(f"reviews/gate.md@{qsha}", qrow_)[2] is None))
        results.append(("F6 post-revert path keys ignore case on Windows",
                        os.name != "nt" or R._pcase("Theory_work\\WaveT\\A.md") == R._pcase("theory_work/wavet/a.md")))

        # F6: a surviving dependent whose premise span lives in the rolled-back ticket's files
        F6, F6D, F6U = "Theory_work/WaveT/F6T", "Theory_work/WaveT/F6D", "Theory_work/WaveT/F6U"
        put(f"{F6}/STATEMENT.md", "## Lemma F6X\nLemma F6X. X holds.\n## Setting\nThe setting S used by Y.\n")
        put(f"{F6}/REPORT.md", "# F6T report\nPROVED-CHECKED\n")
        put(f"{F6D}/STATEMENT.md", "## Lemma F6Y\nLemma F6Y. Y holds in setting S.\n")
        put(f"{F6D}/REPORT.md", "# F6D report\nPROVED-CHECKED\n")
        put(f"{F6U}/STATEMENT.md", "## Lemma F6UX\nLemma F6UX. X holds.\n## Lemma F6Z\nLemma F6Z (another ticket).\n")
        put(f"{F6U}/REPORT.md", "# F6U report\nPROVED-CHECKED\n")
        f6sha = git_commit([F6, F6D, F6U], "F6 fixture")
        rc, out = tool("ingest.py", "claims", frag("f6", [
            dict(ticket="F6T", local_id="X", kind="lemma", file=f"{F6}/STATEMENT.md", lines=[1, 2],
                 status="PROVED-CHECKED", status_source=f"{F6}/REPORT.md:2"),
            dict(ticket="F6D", local_id="Y", kind="lemma", file=f"{F6D}/STATEMENT.md", lines=[1, 2],
                 premises=[f"{F6}/STATEMENT.md:3-4"], depends_on=["F6T:X@stmt"], status="PROVED-CHECKED",
                 status_source=f"{F6D}/REPORT.md:2"),
            dict(ticket="F6U", local_id="X", kind="lemma", file=f"{F6U}/STATEMENT.md", lines=[1, 2],
                 status="PROVED-CHECKED", status_source=f"{F6U}/REPORT.md:2"),
            dict(ticket="F6E", local_id="Z", kind="lemma", file=f"{F6U}/STATEMENT.md", lines=[3, 4],
                 depends_on=["F6U:X@stmt"], status="PROVED-CHECKED", status_source=f"{F6U}/REPORT.md:2")]), "--apply")
        rc, out = run("propagate.py", "rollback-ticket", "F6T", "--archive", f6sha, "--reason", "t")
        y_ = st("F6D:Y")
        results.append(("F6 rollback-ticket: dependent SUSPECT, its premise span re-read at the archive (provenance)",
                        rc == 0 and y_["state"] == "SUSPECT" and f"@archive:{f6sha}" in y_["premises"]
                        and "Post-revert" in out))
        shutil.rmtree(os.path.join(TMP, F6))  # = the documented revert of the ticket's files
        F = findings()
        results.append(("F6 after the revert the final check has no ERROR for the ticket or its dependent",
                        not [f for f in F if f[0] == "ERROR" and f[2].startswith(("F6T:", "F6D:"))]))
        d1 = reg_digest()
        rc, out = run("propagate.py", "rollback-ticket", "F6U", "--archive", f6sha, "--reason", "t", ok=False)
        results.append(("F6 rollback refused when the post-revert tree breaks a surviving claim (statement in the "
                        "ticket's files); nothing written", rc != 0 and "F6E:Z" in out and reg_digest() == d1
                        and st("F6U:X")["state"] == "ACTIVE"))

        if os.name == "nt":  # Sol-R5: the same file spelled in another case (Windows file systems ignore case)
            F6C = "Theory_work/WaveT/F6C"
            put(f"{F6C}/STATEMENT.md", "## Lemma F6CX\nLemma F6CX. X holds.\n## Lemma F6K\nLemma F6K (another ticket).\n")
            put(f"{F6C}/REPORT.md", "# F6C report\nPROVED-CHECKED\n")
            f6c = git_commit([F6C], "F6C fixture")
            tool("ingest.py", "claims", frag("f6c", [
                dict(ticket="F6C", local_id="X", kind="lemma", file=f"{F6C}/STATEMENT.md", lines=[1, 2],
                     status="PROVED-CHECKED", status_source=f"{F6C}/REPORT.md:2"),
                dict(ticket="F6K", local_id="Z", kind="lemma", file="Theory_work/WaveT/f6c/STATEMENT.md", lines=[3, 4],
                     depends_on=["F6C:X@stmt"], status="PROVED-CHECKED", status_source=f"{F6C}/REPORT.md:2")]),
                 "--apply")
            d2 = reg_digest()
            rc, out = run("propagate.py", "rollback-ticket", "F6C", "--archive", f6c, "--reason", "t", ok=False)
            results.append(("Sol-R5 rollback refused when a survivor's statement is the ticket's file in another case",
                            "F6K:Z" in R.index(R.load_claims()) and rc != 0 and "F6K:Z" in out and reg_digest() == d2))

        # Sol-1: a failed restore locks the registry until `bvsreg.py recover`
        f1, f2 = os.path.join(R.REG, "zz_l1.tsv"), os.path.join(R.REG, "zz_l2.tsv")
        for f_ in (f1, f2):
            open(f_, "w", encoding="utf-8").write("h\nold\n")
        lock = os.path.join(R.REG, ".TXN_FAILED")
        real_replace = R.os.replace

        def fail(src, dst):  # the reviewers' probe: replacement of the 2nd file AND the restore both fail
            if str(dst) == str(f2) or str(src).endswith((".bak", ".rst")):  # .rst: restore copies the backup
                raise OSError("injected replacement/rollback failure")
            return real_replace(src, dst)
        R.os.replace = fail
        try:
            R.write_many([(f1, ["h"], [{"h": "new"}]), (f2, ["h"], [{"h": "new"}])])
        except OSError:
            pass
        finally:
            R.os.replace = real_replace
        try:
            lk = _json.load(open(lock, encoding="utf-8"))
        except (OSError, ValueError):
            lk = {}
        results.append(("Sol-1 failed restore writes .TXN_FAILED with the backup locations and recovery steps",
                        any(x.get("backup", "").endswith("zz_l1.tsv.bak") and os.path.exists(x["backup"])
                            for x in lk.get("restore", [])) and "recover" in " ".join(lk.get("recovery", []))))
        rc_c, out_c = tool("check.py", "--quiet")
        rc_s, out_s = run("registry.py", "set", "Q:X", "notes=x", "--reason", "t", ok=False)
        rc_p, out_p = run("propagate.py", "suspect", "Q:X", "--reason", "t", ok=False)
        rc_i, out_i = tool("ingest.py", "claims", frag("lk", [qrow("LK", [11, 12], **qck)]), "--apply")
        results.append(("Sol-1 check.py and every writing tool refuse while the lock exists",
                        all(rc_ != 0 and "TXN_FAILED" in o_ for rc_, o_ in ((rc_c, out_c), (rc_s, out_s),
                                                                            (rc_p, out_p), (rc_i, out_i)))))
        rc_r, out_r = tool("bvsreg.py", "recover")
        results.append(("Sol-1 bvsreg.py recover restores the backup and removes the lock",
                        rc_r == 0 and not os.path.exists(lock) and open(f1).read() == "h\nold\n"
                        and open(f2).read() == "h\nold\n" and tool("check.py", "--quiet")[1].find("TXN_FAILED") < 0))
        if os.path.exists(lock):
            os.remove(lock)
        for f_ in (f1, f2, f1 + ".bak", f2 + ".bak"):
            if os.path.exists(f_):
                os.remove(f_)

        # R07: consumed claims compared with the registry at another ref (current main)
        rc, out = tool("ingest.py", "claims", frag("cv", [
            qrow("A", [1, 2], ticket="CVX", council=COUNCIL, **qck),
            qrow("B", [3, 4], ticket="CVX", council=COUNCIL, **qck),
            qrow("C", [11, 12], ticket="CV", depends_on=["CVX:A@stmt", "CVX:B@stmt"], council=COUNCIL, **qck)]),
            "--apply")
        orig = open(R.CLAIMS, encoding="utf-8", newline="").read()
        same = git_commit([R.CLAIMS], "registry as here")
        rows_ = R.load_claims()
        by_ = R.index(rows_)
        by_["CVX:A"].update(state="SUSPECT", state_reason="suspected on main")
        by_["CVX:B"]["version"] = "2.0.0"
        R.save_claims(rows_)
        ahead = git_commit([R.CLAIMS], "main moved on")
        open(R.CLAIMS, "w", encoding="utf-8", newline="").write(orig)
        F_same = [f for f in findings("--consumed-vs", same, "--tickets", "CV") if f[0] == "ERROR"
                  and f[1].startswith(("R7", "TOOL"))]
        F_main = [f for f in findings("--consumed-vs", ahead, "--tickets", "CV") if f[0] == "ERROR"
                  and f[1].startswith("R7")]
        results.append(("R07 --consumed-vs: identical registry at the ref gives no ERROR", rc == 0 and not F_same))
        results.append(("R07 --consumed-vs: consumed claim non-ACTIVE at the ref, or at a higher major there: ERROR",
                        any("CVX:A" in f[3] for f in F_main) and any("CVX:B" in f[3] for f in F_main)))

        # ---------------- pipeline review R03 (Sol reconciliation): N1 N2 N3 N4 ----------------
        # Fixtures follow the reviewer's probes (probes.py / more.py / cycle.py in the R03 scratch root). The section
        # starts from a fresh copy of the live registry (0 ERROR), as HQ would: an acceptance PASS (and --record)
        # needs 0 ERROR in the whole registry, and the earlier scenarios deliberately leave ERRORs behind.
        shutil.rmtree(R.REG)
        shutil.copytree(os.path.join(LIVE_INFRA, "registry"), R.REG, ignore=shutil.ignore_patterns("*.tmp"))
        N = "Theory_work/WaveT/R03"
        STM_N = ("Lemma Weak. W holds.\nTheorem Y. Y follows from W.\nLemma W2. W2 holds.\n"
                 "Theorem Y2. Y2 follows from W2.\nTheorem Y3. Y3 follows from a legacy claim.\nTheorem D. D holds.\n")
        put(f"{N}/STATEMENT.md", STM_N)
        put(f"{N}/REPORT.md", "PROVED-CHECKED\nPARTIAL\n")
        EXT = "Theory_work/WaveT/R03-external.md"
        put(EXT, "old external premise\n")
        put(f"{N}/reviews/INPUTS.txt", EXT + "\n")
        MAN1, MAN2 = f"{N}/reviews/MANIFEST_R1.txt", f"{N}/reviews/MANIFEST_R2.txt"
        REV = (f"{N}/reviews/sol.md", f"{N}/reviews/opus.md")

        def freeze(out=MAN1):
            man("freeze", N, out, "--extra", f"{N}/reviews/INPUTS.txt")
            return open(os.path.join(TMP, out), encoding="utf-8").readline().split()[1]

        def reviews(sol_text, opus_text):
            put(REV[0], sol_text)
            put(REV[1], opus_text)

        def cn(d, sol="8.5", opus="8.5"):
            return f"R1; MANIFEST {d}; sol={sol} PASS(reviews/sol.md); opus={opus} PASS(reviews/opus.md)"

        def nrow(loc, line, **kw):
            base_ = dict(status="PROVED-CHECKED", status_source=f"{N}/REPORT.md:1")
            base_.update(kw)
            return dict(ticket="R03", local_id=loc, kind=base_.pop("kind", "lemma"), file=f"{N}/STATEMENT.md",
                        lines=[line, line], **base_)

        def a_set(errs):
            return {f[1] for f in errs}
        A4C = {"A4-council", "A1-correct"}  # an invalid council also leaves a checked claim without correctness evidence

        dgA = freeze()
        reviews("Council R1 (sol). Score 8.5, all gates PASS.\n\n" + vline(dgA, "sol"),
                "Council R1 (opus). Score 8.5, all gates PASS.\n\n" + vline(dgA, "opus"))

        # N1: Y -> W (checked-labelled, never accepted) -> V (PARTIAL)
        rc, out = tool("ingest.py", "claims", frag("n1", [
            nrow("W", 1, name="Lemma Weak"),
            nrow("Y", 2, kind="theorem", depends_on=["R03:W@stmt"], council=cn(dgA))]), "--apply")
        e_w = acc_errs("R03:W")
        e_y = acc_errs("R03:Y")
        results.append(("N1 fixture: the unaccepted checked-labelled W is refused on its own (A1-correct, A4-council)",
                        rc == 0 and {"A1-correct", "A4-council"} <= a_set(e_w)))
        results.append(("N1 Y consuming the never-accepted checked W is refused: A5-accepted on Y naming W (and "
                        "nothing else)", any(f[1] == "A5-accepted" and "R03:W" in f[3] for f in e_y)
                        and a_set(e_y) == {"A5-accepted"}))
        rc, out = tool("ingest.py", "claims", frag("n1v", [
            nrow("V", 1, status="PARTIAL", status_source=f"{N}/REPORT.md:2")]), "--apply")
        run("registry.py", "set", "R03:W", "depends_on=R03:V@stmt", "--reason", "probe")
        e_y = acc_errs("R03:Y")
        results.append(("N1 Y -> W (unaccepted, checked-labelled) -> V (PARTIAL): Y refused (A5-accepted)",
                        rc == 0 and any(f[1] == "A5-accepted" and "R03:W" in f[3] for f in e_y)))
        # the durable record: check.py --acceptance ... --record writes `accept` events only on a PASS
        rc, out = tool("ingest.py", "claims", frag("n1r", [
            nrow("W2", 3, council=cn(dgA)),
            nrow("Y2", 4, kind="theorem", depends_on=["R03:W2@stmt"], council=cn(dgA))]), "--apply")
        before_y2 = a_set(acc_errs("R03:Y2"))
        rc_bad, _ = tool("check.py", "--quiet", "--acceptance", "R03:W", "--record")
        rc_rec, out_rec = tool("check.py", "--quiet", "--acceptance", "R03:W2", "--record")
        evs = [e_ for e_ in R.read_tsv(R.EVENTS)[1] if e_.get("action") == "accept"]
        results.append(("N1 --record: a refused acceptance writes no accept event; a PASS writes one with the id, "
                        "version and fingerprint",
                        rc_bad != 0 and not any(e_["id"] == "R03:W" for e_ in evs) and rc_rec == 0
                        and any(e_["id"] == "R03:W2" and e_["after"].startswith(f"v{st('R03:W2')['version']} fp2:")
                                for e_ in evs)))
        rc_only, _ = tool("check.py", "--quiet", "--acceptance", "R03:W", "--only", "A5", "--record")
        ev_only = [e_ for e_ in R.read_tsv(R.EVENTS)[1] if e_.get("action") == "accept" and e_.get("id") == "R03:W"]
        results.append(("Sol-toolfix3 N1.a --only with --acceptance / --record is refused: no accept event, the "
                        "consumer stays refused", rc_only != 0 and not ev_only
                        and any(f[1] == "A5-accepted" for f in acc_errs("R03:Y"))))
        results.append(("N1 the consumer passes once its checked input carries a valid accept record",
                        before_y2 == {"A5-accepted"} and not acc_errs("R03:Y2")))
        run("registry.py", "set", "R03:W2", "depends_on=R03:V@stmt", "--reason", "edge added after acceptance")
        stale = acc_errs("R03:Y2")
        run("registry.py", "set", "R03:W2", "depends_on=", "--reason", "edge removed again")
        results.append(("N1 an accept record goes stale when the input changes after acceptance (consumer refused); "
                        "valid again once the accepted content is restored",
                        any(f[1] == "A5-accepted" and "R03:W2" in f[3] for f in stale) and not acc_errs("R03:Y2")))
        # the frozen legacy boundary (claims PROVED-CHECKED on main at tag theory-v2.0-pre)
        LEG = os.path.join(INFRA, "LEGACY_ACCEPTED.tsv")
        leg_txt = open(LEG, encoding="utf-8").read() if os.path.exists(LEG) else ""
        legacy = R.load_legacy()[2] if hasattr(R, "load_legacy") else set()
        cur_ = R.index(R.load_claims())
        g_ = R.Graph(R.load_claims(), R.load_aliases())
        leaf = next((i for i, v, h in sorted(legacy) if i in cur_ and cur_[i]["state"] == "ACTIVE"
                     and cur_[i]["version"] == v and cur_[i]["sha256"] == h and not g_.deps.get(i)), None)
        rc, out = tool("ingest.py", "claims", frag("n1l", [
            nrow("Y3", 5, kind="theorem", depends_on=[f"{leaf}@stmt"], council=cn(dgA))]), "--apply")
        results.append(("N1 a checked input inside the frozen legacy boundary needs no accept event",
                        leaf is not None and rc == 0 and not acc_errs("R03:Y3")))
        w_ = st("R03:W")
        if leg_txt:
            open(LEG, "a", encoding="utf-8", newline="\n").write(f"R03:W\t{w_['version']}\t{w_['sha256']}\n")
        forged_chk = [f for f in findings() if f[0] == "ERROR" and f[1] == "L1-legacy"]
        forged_acc = acc_errs("R03:Y")
        if leg_txt:
            open(LEG, "w", encoding="utf-8", newline="\n").write(leg_txt)
        results.append(("N1 a hand-added legacy-boundary row is an ERROR (recomputed from the tag) and admits nothing",
                        bool(leg_txt) and bool(forged_chk) and any(f[1] == "A5-accepted" for f in forged_acc)))
        # Sol toolfix3 N1.b: a self-consistent boundary regenerated from a LATER commit (that contains the
        # never-accepted W) must not be trusted: the boundary is the registry at theory-v2.0-pre only
        later = git_commit([R.CLAIMS], "registry with the never-accepted R03 claims")
        rows_l, _ = R.legacy_rows_at(later)
        if leg_txt:
            open(LEG, "w", encoding="utf-8", newline="\n").write(
                "".join(l_ + "\n" for l_ in leg_txt.splitlines() if l_.startswith("#"))
                + f"tag\t{later}\t{later}\nid\tversion\tsha256\n" + "".join(f"{i}\t{v}\t{h}\n" for i, v, h in sorted(rows_l)))
        sub_chk = [f for f in findings() if f[0] == "ERROR" and f[1] == "L1-legacy"]
        sub_acc = acc_errs("R03:Y")
        if leg_txt:
            open(LEG, "w", encoding="utf-8", newline="\n").write(leg_txt)
        results.append(("Sol-toolfix3 N1.b a boundary regenerated from another (later) commit is an L1-legacy ERROR "
                        "and admits nothing", bool(leg_txt) and any(r_[0] == "R03:W" for r_ in rows_l or ())
                        and bool(sub_chk) and any(f[1] == "A5-accepted" for f in sub_acc)))

        # ---------------- pipeline review R04 (Sol reconciliation): N1 N2 ----------------
        # An accepted checked input W (ticket R04W) and its consumer Y (ticket R04Y, own manifest and council). After
        # W's acceptance, any change to W's cited evidence, council verdict, statement-file provenance or reviewed
        # ticket content must refuse Y's acceptance (A5 naming W; --record writes nothing) until W is accepted again.
        WD, YD = "Theory_work/WaveT/R04W", "Theory_work/WaveT/R04Y"
        put(f"{WD}/STATEMENT.md", "Lemma R04W. W holds.\n")
        put(f"{WD}/REPORT.md", "PROVED-CHECKED\n")
        put(f"{WD}/PROOF.md", "Proof of W.\n")
        put(f"{YD}/STATEMENT.md", "Theorem R04Y. Y follows from Lemma R04W.\n")
        put(f"{YD}/REPORT.md", "PROVED-CHECKED\n")

        def r04_council(d_):
            os.makedirs(os.path.join(TMP, d_, "reviews"), exist_ok=True)
            man("freeze", d_, f"{d_}/reviews/MANIFEST_R1.txt")
            dg_ = open(os.path.join(TMP, d_, "reviews", "MANIFEST_R1.txt"), encoding="utf-8").readline().split()[1]
            for s_ in ("sol", "opus"):
                put(f"{d_}/reviews/{s_}.md", f"Council R1 ({s_}).\n\n" + vline(dg_, s_))
            return f"R1; MANIFEST {dg_}; sol=8.5 PASS(reviews/sol.md); opus=8.5 PASS(reviews/opus.md)"
        cW, cY = r04_council(WD), r04_council(YD)
        EV_TXT = "Correctness review of W: PASS.\n"
        WEV = put(f"{WD}/reviews/evidence.md", EV_TXT)
        WSOL = os.path.join(TMP, WD, "reviews", "sol.md")
        rc, out = tool("ingest.py", "claims", frag("r04", [
            dict(ticket="R04W", local_id="W", kind="lemma", name="Lemma R04W", file=f"{WD}/STATEMENT.md",
                 lines=[1, 1], status="PROVED-CHECKED", status_source=f"{WD}/REPORT.md:1", council=cW),
            dict(ticket="R04Y", local_id="Y", kind="theorem", file=f"{YD}/STATEMENT.md", lines=[1, 1],
                 status="PROVED-CHECKED", status_source=f"{YD}/REPORT.md:1", council=cY,
                 depends_on=["R04W:W@stmt"])]), "--apply")
        run("registry.py", "set", "R04W:W", "gates=correct:PASS(reviews/evidence.md)", "--reason", "R04 fixture")

        def n_acc(cid):
            return sum(1 for e_ in R.read_tsv(R.EVENTS)[1] if e_.get("action") == "accept" and e_.get("id") == cid)

        def y_refused(why=""):
            """Y's acceptance names only A5 on W (with `why` in the message), and Y's --record run is refused and
            writes no accept event."""
            e_ = acc_errs("R04Y:Y")
            n0 = n_acc("R04Y:Y")
            rc_, out_ = tool("check.py", "--quiet", "--acceptance", "R04Y:Y", "--record")
            return (a_set(e_) == {"A5-accepted"} and all("R04W:W" in f[3] and why in f[3] for f in e_)
                    and rc_ != 0 and "nothing recorded" in out_ and n_acc("R04Y:Y") == n0)
        rc_w, out_w = tool("check.py", "--quiet", "--acceptance", "R04W:W", "--record")
        results.append(("R04 control: W accepted and recorded with an fp2 identity; Y consuming it passes",
                        rc == 0 and rc_w == 0 and " fp2:" in out_w and not acc_errs("R04Y:Y")))
        # N1 evidence: W's cited gate evidence deleted, or its content changed
        os.remove(WEV)
        ev_del = (a_set(acc_errs("R04W:W")) >= {"A1-evidence"}, y_refused("stale"))
        put(f"{WD}/reviews/evidence.md", EV_TXT)
        ev_back = not acc_errs("R04Y:Y")
        put(f"{WD}/reviews/evidence.md", "Correctness review of W: PASS (rewritten after acceptance).\n")
        ev_edit = y_refused("stale")
        rc_re, _ = tool("check.py", "--quiet", "--acceptance", "R04W:W", "--record")  # a fresh passing acceptance
        ev_re = rc_re == 0 and not acc_errs("R04Y:Y")
        put(f"{WD}/reviews/evidence.md", EV_TXT)
        results.append(("R04-N1 evidence: W's gate evidence deleted -> W refused (A1-evidence) and Y refused (A5, "
                        "--record writes nothing); restored -> Y passes", all(ev_del) and ev_back))
        results.append(("R04-N1 evidence: W's evidence content changed -> Y refused (A5 stale); after a fresh "
                        "passing acceptance of W, Y passes", ev_edit and ev_re and not acc_errs("R04Y:Y")))
        # N1 verdict: W's council review withdraws its verdict (gates=FAIL)
        sol_txt = open(WSOL, encoding="utf-8").read()
        open(WSOL, "w", encoding="utf-8", newline="\n").write(sol_txt.replace("gates=PASS", "gates=FAIL"))
        vd = (a_set(acc_errs("R04W:W")) >= {"A4-council"}, y_refused())
        open(WSOL, "w", encoding="utf-8", newline="\n").write(sol_txt)
        results.append(("R04-N1 verdict: W's council verdict withdrawn (gates=FAIL) -> W refused (A4) and Y refused "
                        "(A5, --record writes nothing); restored -> Y passes", all(vd) and not acc_errs("R04Y:Y")))
        # N1 revalidation: W's reviewed ticket content changes (identity fields unchanged): the frozen manifest no
        # longer verifies, so W fails its own acceptance and Y is refused
        put(f"{WD}/PROOF.md", "Proof of W (changed after the round).\n")
        rv = (a_set(acc_errs("R04W:W")) >= {"A4-council"}, y_refused("no longer passes acceptance"))
        put(f"{WD}/PROOF.md", "Proof of W.\n")
        results.append(("R04-N1 revalidation: W's reviewed ticket content changed after acceptance -> Y refused (A5: "
                        "W no longer passes acceptance); restored -> Y passes", all(rv) and not acc_errs("R04Y:Y")))
        # N2: documented statement relocation (registry.py set file=...) of the accepted input, identical text
        put("Theory_work/WaveT/r04-relocated.md", "Lemma R04W. W holds.\n")
        rc_mv, _ = run("registry.py", "set", "R04W:W", "file=Theory_work/WaveT/r04-relocated.md", "--reason", "R04")
        mv = (rc_mv == 0, bool(acc_errs("R04W:W")), y_refused("stale"))
        run("registry.py", "set", "R04W:W", f"file={WD}/STATEMENT.md", "--reason", "R04 restore")
        results.append(("R04-N2 relocation: W's statement file relocated via registry.py set file= -> W refused and Y "
                        "refused (A5, --record writes nothing); restored -> Y passes", all(mv) and not acc_errs("R04Y:Y")))
        # migration: a record in the pre-R04 stamp format (`fp:`) never matches; the message says to re-accept
        ev_raw = open(R.EVENTS, "rb").read()
        h_, evs_ = R.read_tsv(R.EVENTS)
        for e_ in evs_:
            if e_.get("action") == "accept" and e_.get("id") == "R04W:W":
                e_["after"] = f"v{st('R04W:W')['version']} fp:0123456789abcdef"
        R.write_tsv(R.EVENTS, h_, evs_)
        old_fmt = y_refused("predates")
        open(R.EVENTS, "wb").write(ev_raw)
        results.append(("R04 an accept record in the old `fp:` format is not trusted (A5: re-accept on the current "
                        "tree); the fp2 record restored -> Y passes", old_fmt and not acc_errs("R04Y:Y")))

        # N3: every better-proposal / better-disposition reference, and every gate reference whatever its result,
        # must resolve (staged acceptance, as in the reviewer's probe)
        G3 = "; ".join(f"{k}:PASS(reviews/sol.md)" for k in ("correct", "lit", "necessity"))

        def disp(loc, tail, headline="yes"):
            return tool("ingest.py", "claims", frag(f"n3{loc}", [
                nrow(loc, 6, kind="theorem", council=cn(dgA), headline=headline,
                     strength=dict(conclusion="posterior: probe", gates=f"{G3}; {tail}"))]), "--staged")

        def acc_line(out_, cid):
            return next((l_ for l_ in out_.splitlines() if l_.strip().startswith(f"acceptance ({cid}")), "")
        rc_d, out_d = disp("D", "better-proposal:P(reviews/sol.md); "
                                "better-disposition:P=declined(reviews/DOES_NOT_EXIST.md)")
        rc_p, out_p = disp("DP", "better-proposal:P(reviews/NOPE.md); better-disposition:P=declined(reviews/sol.md)")
        rc_f, out_f = disp("DF", "better:FAIL(reviews/NOPE2.md); better-proposal:P(reviews/sol.md); "
                                 "better-disposition:P=declined(reviews/opus.md)")
        rc_n, out_n = disp("DN", "lit:PENDING(reviews/NOPE3.md)", headline="")
        rc_ok, out_ok = disp("DOK", "better-proposal:P(reviews/sol.md); better-disposition:P=declined(reviews/opus.md)")
        results.append(("N3 declined(reviews/DOES_NOT_EXIST.md): staged acceptance REFUSED with A1-evidence",
                        rc_d != 0 and "REFUSED" in acc_line(out_d, "R03:D") and "DOES_NOT_EXIST" in out_d
                        and "A1-evidence" in out_d))
        results.append(("N3 a better-proposal citing a missing file, and FAIL / PENDING gates citing missing files, are "
                        "A1-evidence ERRORs", all("REFUSED" in acc_line(o_, c_) and m_ in o_ for o_, c_, m_ in (
                            (out_p, "R03:DP", "NOPE.md"), (out_f, "R03:DF", "NOPE2.md"), (out_n, "R03:DN", "NOPE3.md")))))
        results.append(("N3 control: the same headline with existing disposition evidence passes staged acceptance",
                        "PASS" in acc_line(out_ok, "R03:DOK") and "REFUSED" not in acc_line(out_ok, "R03:DOK")))

        # N2: a review must bind an OUTCOME to the digest. M fixture (more.py): stronger statement, fresh freeze,
        # replies say the new digest is NOT REVIEWED, the cell says 8.5 PASS on it.
        run("registry.py", "set", "R03:Y", "depends_on=", "--reason", "isolate N2 from N1")
        put(f"{N}/STATEMENT.md", STM_N.replace("Theorem Y. Y follows from W.",
                                               "Theorem Y. A strictly stronger Y holds for all parameters."))
        run("registry.py", "rehash", "R03:Y", "--bump", "major", "--reason", "stronger statement fixture")
        dgM = freeze()
        reviews(f"Scored OLD text: 8.5 PASS.\nMANIFEST {dgM}: new stronger text NOT REVIEWED; gates FAIL pending "
                "review.\n", f"Scored OLD text: 8.5 PASS.\nMANIFEST {dgM}: new stronger text NOT REVIEWED; gates "
                "FAIL pending review.\n")
        run("registry.py", "set", "R03:Y", "council=" + cn(dgM), "--reason", "probe record")
        rc_v, _ = man("verify", N, MAN1)
        rc_b, out_b = man("bind", MAN1, *REV)
        e_m = acc_errs("R03:Y")
        results.append(("N2 M fixture (current digest quoted only as NOT REVIEWED): verify OK, bind REFUSED, "
                        "acceptance A4-council", rc_v == 0 and rc_b != 0 and "A4-council" in a_set(e_m) <= A4C))
        bad_verdicts = {
            "gates=FAIL for the digest": vline(dgM, "sol", res="FAIL"),
            "two verdict lines for the digest (PASS and FAIL)": vline(dgM, "sol") + vline(dgM, "sol", res="FAIL"),
            "the same verdict line twice": vline(dgM, "sol") * 2,
            "verdict only for another digest": vline(dgA, "sol"),
            "a contradictory verdict line for another digest": vline(dgM, "sol") + vline(dgA, "sol", res="FAIL"),
            "seat differs from the cell": vline(dgM, "opus"),
            "score differs from the cell": vline(dgM, "sol", score="8.1"),
            "round differs from the cell": vline(dgM, "sol", rnd="R2"),
            "malformed verdict line": vline(dgM, "sol").replace("gates=PASS", "gates=PASS extra"),
            "verdict line inside prose": "As agreed, " + vline(dgM, "sol"),
        }
        bad_left = []
        for lab, txt in bad_verdicts.items():
            reviews("Council R1 (sol).\n" + txt, "Council R1 (opus).\n" + vline(dgM, "opus"))
            rc_b, _ = man("bind", MAN1, *REV, "--council", cn(dgM))
            if rc_b == 0 or "A4-council" not in a_set(acc_errs("R03:Y")):
                bad_left.append(lab)
        results.append(("N2 verdict-line violations refuse both bind and acceptance: " + ", ".join(bad_verdicts),
                        not bad_left))
        run("registry.py", "set", "R03:Y", "council=" + cn(dgM, sol="7.5", opus="7.5"), "--reason", "t")
        reviews(vline(dgM, "sol", score="7.5"), vline(dgM, "opus", score="7.5"))
        low_b = man("bind", MAN1, *REV)[0]
        low_a = a_set(acc_errs("R03:Y"))
        run("registry.py", "set", "R03:Y", "council=" + cn(dgM), "--reason", "t")
        reviews("Council R1 (sol). Score 8.5.\n\n" + vline(dgM, "sol"), "Council R1 (opus).\n" + vline(dgM, "opus"))
        rc_b, out_b = man("bind", MAN1, *REV, "--council", cn(dgM))
        rc_bx, _ = man("bind", MAN1, *REV, "--council", cn(dgM, opus="8.6"))
        results.append(("N2 consistent verdicts below 8.0 refused; the matching PASS verdicts bind (bind prints the "
                        "cell) and pass acceptance; a cell that differs from the verdicts is refused by bind",
                        low_b != 0 and "A4-council" in low_a and rc_b == 0 and cn(dgM) in out_b
                        and not acc_errs("R03:Y") and rc_bx != 0))
        # Sol toolfix3 N3.a: a malformed gate entry on a NON-headline cannot hide a missing evidence file
        run("registry.py", "set", "R03:Y", "gates=lit:PENDING(reviews/DOES_NOT_EXIST.md) trailing", "--reason", "t")
        e_mal = acc_errs("R03:Y")
        run("registry.py", "set", "R03:Y", "gates=", "--reason", "t")
        results.append(("Sol-toolfix3 N3.a an unparsable gate entry on a non-headline is an A1-gates ERROR (the "
                        "well-formed claim passes again)", any(f[1] == "A1-gates" and "unparsable" in f[3] for f in e_mal)
                        and not acc_errs("R03:Y")))
        # the verified manifest must cover the claim itself: a statement outside the ticket folder, not in INPUTS.txt
        hdr_t, trows = R.read_tsv(R.TICKETS)
        for t_ in trows:
            if t_["ticket"] == "R03":
                t_["folder"] = N
        R.write_tsv(R.TICKETS, hdr_t, trows)
        put("Theory_work/WaveT/R03-outside.md", "Theorem Z. Z holds (text outside the ticket folder).\n")
        rc, out = tool("ingest.py", "claims", frag("n2z", [dict(
            ticket="R03", local_id="Z", kind="theorem", file="Theory_work/WaveT/R03-outside.md", lines=[1, 1],
            status="PROVED-CHECKED", status_source=f"{N}/REPORT.md:1", council=cn(dgM))]), "--apply")
        e_z = acc_errs("R03:Z")
        results.append(("N2 a verified manifest that does not cover the claim's statement file (outside the ticket, not "
                        "in INPUTS.txt) is refused (A4); the in-folder claim still passes",
                        rc == 0 and any(f[1] == "A4-council" and "does not cover" in f[3] for f in e_z)
                        and not acc_errs("R03:Y")))
        # P fixture (probes.py): the content changes after the round; the council keeps the reviewed digest while a
        # NEW digest is frozen, verified and quoted (as unreviewed) in the same files
        put(EXT, "changed external premise\n")
        e_p1 = a_set(acc_errs("R03:Y"))
        dgP = freeze(MAN2)
        reviews(vline(dgM, "sol") + f"New MANIFEST {dgP} is unreviewed; FAIL pending review.\n",
                vline(dgM, "opus") + f"New MANIFEST {dgP} is unreviewed; FAIL pending review.\n")
        rc_vP, _ = man("verify", N, MAN2)
        rc_bP, _ = man("bind", MAN2, *REV)
        e_p2 = a_set(acc_errs("R03:Y"))
        os.remove(os.path.join(TMP, MAN2))
        freeze(MAN1)  # the reviewer's exact variant: re-frozen over the same file; no manifest with the cell digest
        e_p3 = a_set(acc_errs("R03:Y"))
        results.append(("N2 P fixture: content changed after the round -> A4 (manifest no longer verifies); new digest "
                        "verified but bind REFUSED (no verdict for it); old manifest kept -> A4; re-frozen in place "
                        "-> A4 (no MANIFEST_*.txt with the cell digest)",
                        all("A4-council" in e_ <= A4C for e_ in (e_p1, e_p2, e_p3)) and rc_vP == 0 and rc_bP != 0))

        # ---------------- INFRA R05: a ticket's own CHECKPOINT_<k>.md as (uncovered) status source ----------------
        # Ticket R05T: an earlier line-check round LC1 (own manifest), the acceptance round R1 (manifest, two seats
        # with per-claim tables), status lines and REGISTRY blocks in CHECKPOINT_3.md (never in a manifest).
        TD = "Theory_work/WaveT/R05T"
        CK = f"{TD}/CHECKPOINT_3.md"
        put(f"{TD}/STATEMENT.md", "Lemma A. A holds.\nLemma B. B holds.\nLemma Z. Z holds.\n")
        put(f"{TD}/PROOF.md", "Proofs of A, B and Z (draft).\n")
        put(f"{TD}/LOG.md", "Lemma A. A holds.\nPROVED-CHECKED\n")
        os.makedirs(os.path.join(TMP, TD, "reviews"), exist_ok=True)

        def mhead(rel):
            return open(os.path.join(TMP, rel), encoding="utf-8").readline().split()[1]
        man("freeze", TD, f"{TD}/reviews/MANIFEST_LC1.txt")
        dgL = mhead(f"{TD}/reviews/MANIFEST_LC1.txt")
        LC1 = f"{TD}/reviews/LC1_A_line_check.md"
        LC1_TXT = f"Line check LC1-A on MANIFEST {dgL}: VERIFIED.\n"
        put(LC1, LC1_TXT)
        put(f"{TD}/PROOF.md", "Proofs of A, B and Z (final).\n")  # the round's content changes before the council
        man("freeze", TD, f"{TD}/reviews/MANIFEST_R1.txt")
        dg5 = mhead(f"{TD}/reviews/MANIFEST_R1.txt")
        cell5 = f"R1; MANIFEST {dg5}; sol=8.5 PASS(reviews/R1_council_sol.md); opus=8.5 PASS(reviews/R1_council_opus.md)"
        SOLR, OPUSR = f"{TD}/reviews/R1_council_sol.md", f"{TD}/reviews/R1_council_opus.md"

        def r05_review(seat, decisions, head_="| id | decision |", dg_=None):
            return (f"Council R1 ({seat}).\n\n{head_}\n|---|---|\n" + "".join(f"| {i} | {d_} |\n" for i, d_ in decisions)
                    + "\n" + vline(dg_ or dg5, seat))
        GOOD_SOL = r05_review("sol", [("A", "accepted"), ("B", "Accepted")])
        GOOD_OPUS = r05_review("opus", [("R05T:A", "accepted"), ("B", "accepted")], "| Id | Disposition |")
        put(SOLR, GOOD_SOL)
        put(OPUSR, GOOD_OPUS)

        def r05_blk(loc, ln, sl):
            return ("```\nREGISTRY\n"
                    f"claim: R05T:{loc} | kind: lemma | statement: STATEMENT.md:{ln} | premises: none\n"
                    f"name: Lemma {loc}\nstatus: PROVED-CHECKED | status_source: CHECKPOINT_3.md:{sl}\n"
                    f"council: {cell5}\n```\n")

        def r05_ckpt(a_cite="LC1-A: VERIFIED.", z=False):
            return ("# R05T checkpoint 3\n\n"
                    f"- R05T:A — PROVED-CHECKED — Lemma A. Line check: {a_cite}\n"
                    "- R05T:B — PROVED-CHECKED — Lemma B. Line check: LC1-A (arithmetic, L1.2): VERIFIED; R1: accepted.\n"
                    + ("- R05T:Z — PROVED-CHECKED — Lemma Z. Line check: LC1-A: VERIFIED.\n" if z else "\n") + "\n"
                    + r05_blk("A", 1, 3) + "\n" + r05_blk("B", 2, 4) + ("\n" + r05_blk("Z", 3, 5) if z else ""))

        def acc_l(out_):
            return next((l_ for l_ in out_.splitlines() if l_.strip().startswith("acceptance (")), "")
        # staged: an extra claim id (Z: in the checkpoint, accepted by no seat) and an unresolvable round id are refused
        put(CK, r05_ckpt(z=True))
        rc_x, out_x = tool("ingest.py", "claims", os.path.join(TMP, CK), "--staged")
        put(CK, r05_ckpt(a_cite="LC9-A: VERIFIED."))
        rc_u, out_u = tool("ingest.py", "claims", os.path.join(TMP, CK), "--staged")
        # Sol R05FIX B1: a citation carried by a status that continues past the stated line must be checked too
        put(CK, "# R05T checkpoint 3\n\nPROVED-CHECKED\nLC9-A: VERIFIED\n"
            "- R05T:B — PROVED-CHECKED — Lemma B. Line check: LC1-A: VERIFIED.\n\n"
            + r05_blk("A", 1, 3).replace("status: PROVED-CHECKED |", "status: PROVED-CHECKED LC9-A: VERIFIED |")
            + "\n" + r05_blk("B", 2, 5))
        rc_c, out_c = tool("ingest.py", "claims", os.path.join(TMP, CK), "--staged")
        CK_TXT = r05_ckpt()
        put(CK, CK_TXT)
        rc_g, out_g = tool("ingest.py", "claims", os.path.join(TMP, CK), "--staged")
        results.append(("R05 staged: a checkpoint carrying a claim id no seat accepted (extra id) is REFUSED (A4)",
                        rc_x != 0 and "REFUSED" in acc_l(out_x) and "did not accept" in out_x and "R05T:Z" in out_x))
        results.append(("R05 staged: a status line citing an unresolvable round id (LC9-A) is REFUSED (A4)",
                        rc_u != 0 and "REFUSED" in acc_l(out_u) and "LC9-A" in out_u and "resolves to no file" in out_u))
        results.append(("R05FIX B1 staged: a round citation carried by a status continued past its stated line "
                        "(LC9-A, unresolvable) is REFUSED (A4)",
                        rc_c != 0 and "REFUSED" in acc_l(out_c) and "LC9-A" in out_c and "resolves to no file" in out_c))
        results.append(("R05 control (staged): own CHECKPOINT_3.md as status source, outside the manifest, passes "
                        "acceptance (0 ERROR)", rc_g == 0 and "PASS" in acc_l(out_g) and "REFUSED" not in acc_l(out_g)))
        rc_ap, _ = tool("ingest.py", "claims", os.path.join(TMP, CK), "--apply")
        sha_ok = all(st(c_)["status_sha256"] and st(c_)["status_sha256"] == R.status_sha(st(c_)["status_source"])
                     for c_ in ("R05T:A", "R05T:B"))
        r05_clean = lambda: not acc_errs("R05T:A", "R05T:B") and not acc_errs("R05T:B", "R05T:A")  # noqa: E731

        def r05_has(cid, frag_, chk="A4-council"):
            return any(f[1] == chk and frag_ in f[3] for f in acc_errs(cid))
        results.append(("R05 ingest records the checkpoint's sha256 in status_sha256; both claims pass acceptance; "
                        "status_sha256 is not settable by registry.py set",
                        rc_ap == 0 and sha_ok and r05_clean()
                        and run("registry.py", "set", "R05T:A", "status_sha256=" + "0" * 64, "--reason", "t", ok=False)[0] != 0))
        # (3) a later edit of the checkpoint: check.py C12 ERROR (routine run and CI) and acceptance refused
        put(CK, CK_TXT + "\nA late note.\n")
        c12 = {f[2] for f in findings() if f[0] == "ERROR" and f[1] == "C12-checkpoint"}
        ed = r05_has("R05T:A", "changed after ingest")
        put(CK, CK_TXT)
        results.append(("R05 checkpoint edited after ingest: check.py C12-checkpoint ERROR for both claims and A4 "
                        "refusal; restored -> clean", c12 >= {"R05T:A", "R05T:B"} and ed and r05_clean()
                        and not [f for f in findings() if f[1] == "C12-checkpoint"]))
        # (3) no recorded checkpoint digest -> no exemption
        rows_ = R.load_claims()
        keep = next(r_ for r_ in rows_ if r_["id"] == "R05T:A")["status_sha256"]
        for r_ in rows_:
            if r_["id"] == "R05T:A":
                r_["status_sha256"] = ""
        R.save_claims(rows_)
        nosha = r05_has("R05T:A", "records no status_sha256")
        rows_ = R.load_claims()
        for r_ in rows_:
            if r_["id"] == "R05T:A":
                r_["status_sha256"] = keep
        R.save_claims(rows_)
        results.append(("R05 a checkpoint status source without a recorded status_sha256 is refused (A4); restored -> "
                        "clean", nosha and r05_clean()))
        # (2) unbound reviews: a council seat whose verdict is bound to another manifest; an earlier round's review that
        # quotes no frozen manifest digest (none at all, or a digest that is no MANIFEST_*.txt of the ticket)
        put(OPUSR, r05_review("opus", [("A", "accepted"), ("B", "accepted")], dg_=dgL))
        ub_c = r05_has("R05T:A", "no COUNCIL-VERDICT line for MANIFEST") and r05_has("R05T:B", "COUNCIL-VERDICT")
        put(OPUSR, GOOD_OPUS)
        put(LC1, "Line check LC1-A: VERIFIED (no digest quoted).\n")
        ub_e1 = r05_has("R05T:A", "quotes no digest")
        put(LC1, f"Line check LC1-A on MANIFEST {'0' * 64}: VERIFIED.\n")
        ub_e2 = r05_has("R05T:B", "quotes no digest")
        # Sol R05FIX B2: a header-only / corrupted historical manifest is not a frozen manifest
        BADM = put(f"{TD}/reviews/MANIFEST_corrupt.txt", f"MANIFEST {'0' * 64}\nnot a manifest row\n")
        ub_e3 = r05_has("R05T:A", "quotes no digest")
        os.remove(BADM)
        put(LC1, LC1_TXT)
        results.append(("R05 unbound reviews refused (A4): a council seat bound to another manifest; an earlier round "
                        "(LC1-A) quoting no digest, or a digest that is no frozen manifest of the ticket; restored -> "
                        "clean; a corrupted historical manifest with that header does not count (Sol R05FIX B2)",
                        ub_c and ub_e1 and ub_e2 and ub_e3 and r05_clean()))
        # (4) claim ids: a seat that did not accept B; a seat that accepted an id the checkpoint lacks
        put(SOLR, r05_review("sol", [("A", "accepted"), ("B", "not accepted (gap in step 2)")]))
        id_x = r05_has("R05T:A", "did not accept") and r05_has("R05T:B", "R05T:B")
        put(SOLR, GOOD_SOL)
        put(OPUSR, r05_review("opus", [("A", "accepted"), ("B", "accepted"), ("Z", "accepted")]))
        id_m = r05_has("R05T:A", "lacks claim id(s) this seat accepted")
        put(OPUSR, "Council R1 (opus). All accepted.\n\n" + vline(dg5, "opus"))
        id_t = r05_has("R05T:A", "no per-claim table")
        put(OPUSR, GOOD_OPUS)
        results.append(("R05 checkpoint ids must equal each seat's accepted ids: a not-accepted id, an accepted id "
                        "missing from the checkpoint, and a review without a per-claim table are refused (A4); restored "
                        "-> clean", id_x and id_m and id_t and r05_clean()))
        # (5) ambiguous round id: two review files for LC1-A
        put(f"{TD}/reviews/LC1_A_line_check_v2.md", LC1_TXT)
        amb = r05_has("R05T:A", "resolves to 2 review files")
        os.remove(os.path.join(TMP, TD, "reviews", "LC1_A_line_check_v2.md"))
        results.append(("R05 a cited round id that resolves to two review files (ambiguous) is refused (A4); restored "
                        "-> clean", amb and r05_clean()))
        # (1) only the ticket's OWN CHECKPOINT_<k>.md is exempt: LOG.md, a CHECKPOINT in a sub-folder and another
        # ticket's CHECKPOINT (all outside the manifest) as status source are refused for coverage
        put(f"{TD}/sub/CHECKPOINT_3.md", CK_TXT)
        put("Theory_work/WaveT/R05U/CHECKPOINT_3.md", CK_TXT)
        arb = []
        for src_ in (f"{TD}/LOG.md:2", f"{TD}/sub/CHECKPOINT_3.md:3", "Theory_work/WaveT/R05U/CHECKPOINT_3.md:3"):
            rc_cs, _ = run("registry.py", "correct-status", "R05T:A", "--status", "PROVED-CHECKED", "--source", src_,
                           "--reason", "R05 probe")
            arb.append(rc_cs == 0 and r05_has("R05T:A", f"does not cover {src_.rpartition(':')[0]}"))
        run("registry.py", "correct-status", "R05T:A", "--status", "PROVED-CHECKED", "--source", f"{CK}:3",
            "--reason", "R05 restore")
        results.append(("R05 an arbitrary uncovered status file (LOG.md, a sub-folder CHECKPOINT, another ticket's "
                        "CHECKPOINT) is refused (A4 coverage); the own checkpoint restored -> clean",
                        all(arb) and len(arb) == 3 and r05_clean()))
        # (1) statement files stay covered: a statement relocated to an uncovered file (LOG.md, same text) is refused
        run("registry.py", "set", "R05T:A", f"file={TD}/LOG.md", "--reason", "R05 probe")
        unc = r05_has("R05T:A", f"does not cover {TD}/LOG.md")
        run("registry.py", "set", "R05T:A", f"file={TD}/STATEMENT.md", "--reason", "R05 restore")
        results.append(("R05 an uncovered statement file is still refused (A4) with a checkpoint status source; "
                        "restored -> clean", unc and r05_clean()))

        # N4: crash-safe transactions (journal registry/.TXN_INPROGRESS; recover rolls back, restartably)
        c1, c2 = os.path.join(R.REG, "zz_c1.tsv"), os.path.join(R.REG, "zz_c2.tsv")
        for f_ in (c1, c2):
            open(f_, "w", encoding="utf-8", newline="\n").write("old\n")
        JOURNAL = os.path.join(R.REG, ".TXN_INPROGRESS")
        TOOLS_SB = os.path.join(INFRA, "tools")
        kid = put("crash_child.py", "import os, sys\nsys.dont_write_bytecode = True\n"
                  f"sys.path.insert(0, {TOOLS_SB!r})\nimport bvsreg as R\nreal = os.replace\n"
                  f"def kill(src, dst):\n    if str(dst) == {c2!r}:\n        os._exit(73)\n    return real(src, dst)\n"
                  f"os.replace = kill\nR.write_many([({c1!r}, 'new\\n'), ({c2!r}, 'new\\n')])\n")
        rc_k = subprocess.run([sys.executable, kid], cwd=TMP, capture_output=True).returncode
        mixed = (open(c1, encoding="utf-8").read(), open(c2, encoding="utf-8").read())
        try:
            jr = _json.load(open(JOURNAL, encoding="utf-8"))
        except (OSError, ValueError):
            jr = {}
        baks = [x.get("backup", "") for x in jr.get("restore", [])]
        results.append(("N4 a process killed between two replacements leaves the journal registry/.TXN_INPROGRESS "
                        "(written before the first replacement, with the backup locations)",
                        rc_k == 73 and mixed == ("new\n", "old\n") and len(baks) == 2
                        and all(b_ and os.path.exists(b_) for b_ in baks)))
        rc_c, out_c = tool("check.py", "--quiet")
        rc_s, out_s = run("registry.py", "set", "Q:X", "notes=x", "--reason", "t", ok=False)
        rc_p, out_p = run("propagate.py", "suspect", "Q:X", "--reason", "t", ok=False)
        rc_i, out_i = tool("ingest.py", "claims", frag("lk2", [qrow("LK2", [11, 12], **qck)]), "--apply")
        results.append(("N4 check.py and every writing tool refuse while the journal exists",
                        all(rc_ != 0 and "TXN_INPROGRESS" in o_ for rc_, o_ in ((rc_c, out_c), (rc_s, out_s),
                                                                               (rc_p, out_p), (rc_i, out_i)))))
        locked_man = [man("verify", N, MAN1), man("bind", MAN1, *REV),
                      man("freeze", N, f"{N}/reviews/MANIFEST_LOCKED.txt")]
        results.append(("Sol-toolfix3 N4.a manifest.py freeze / verify / bind refuse while the journal exists",
                        all(rc_ != 0 and "TXN_INPROGRESS" in o_ for rc_, o_ in locked_man)
                        and not os.path.exists(os.path.join(TMP, N, "reviews", "MANIFEST_LOCKED.txt"))))
        BVS_SB = os.path.join(TOOLS_SB, "bvsreg.py")
        kid2 = put("crash_recover.py", "import os, sys, runpy\nsys.dont_write_bytecode = True\n"
                   "def kill(src, dst):\n    os._exit(74)\nos.replace = kill\n"
                   f"sys.argv = [{BVS_SB!r}, 'recover']\nrunpy.run_path({BVS_SB!r}, run_name='__main__')\n")
        rc_k2 = subprocess.run([sys.executable, kid2], cwd=TMP, capture_output=True).returncode
        still = os.path.exists(JOURNAL) and tool("check.py", "--quiet")[0] != 0
        rc_r, out_r = tool("bvsreg.py", "recover")
        left = [f_ for f_ in os.listdir(R.REG) if f_.startswith("zz_c") and f_.endswith((".tmp", ".bak", ".rst"))]
        results.append(("N4 a crash during recover leaves the journal (tools still refuse); recover restarts, rolls "
                        "both files back, removes the journal and the leftovers",
                        rc_k2 == 74 and still and rc_r == 0 and not os.path.exists(JOURNAL)
                        and open(c1, encoding="utf-8").read() == "old\n" and open(c2, encoding="utf-8").read() == "old\n"
                        and not left and "TXN_" not in tool("check.py", "--quiet")[1]))
        rc_w = 0
        try:
            R.write_many([(c1, "new\n"), (c2, "new\n")])
        except BaseException:
            rc_w = 1
        results.append(("N4 a normal transaction commits both files and leaves no journal or backups",
                        rc_w == 0 and open(c1, encoding="utf-8").read() == "new\n" and not os.path.exists(JOURNAL)
                        and not [f_ for f_ in os.listdir(R.REG) if f_.startswith("zz_c") and not f_.endswith(".tsv")]))
        for f_ in (c1, c2):
            if os.path.exists(f_):
                os.remove(f_)

        # ---------------- INFRA R06: line-ending-independent manifest hashes ----------------
        import hashlib as _hl
        import tempfile as _tf
        _sm = importlib.util.spec_from_file_location("bvs_manifest_r06", MANP)
        MT = importlib.util.module_from_spec(_sm)
        _sm.loader.exec_module(MT)
        TE = "Theory_work/WaveT/R06E"
        EXT6 = "Theory_work/WaveT/R06E-ext.md"
        os.makedirs(os.path.join(TMP, TE, "reviews"), exist_ok=True)

        def putb(rel, data):
            fp = os.path.join(TMP, rel)
            os.makedirs(os.path.dirname(fp), exist_ok=True)
            open(fp, "wb").write(data)
            return fp

        def getb(rel):
            return open(os.path.join(TMP, rel), "rb").read()

        def flip(rel):  # LF <-> CRLF of every line of a file
            d_ = getb(rel)
            putb(rel, d_.replace(b"\r\n", b"\n") if b"\r\n" in d_ else d_.replace(b"\n", b"\r\n"))
        E_FILES = {f"{TE}/a.md": b"Lemma A. A holds.\nProof. Trivial.\n",
                   f"{TE}/b.md": b"Lemma B. B holds.\r\nProof. Trivial.\r\n",
                   f"{TE}/mixed.md": b"line one\r\nline two\nline three\r\n",
                   f"{TE}/bin.dat": b"\x00\x01binary\r\nrow\n",
                   EXT6: b"external premise\r\nsecond line\r\n"}
        for k_, v_ in E_FILES.items():
            putb(k_, v_)
        put(f"{TE}/reviews/INPUTS.txt", EXT6 + "\n")
        ME = f"{TE}/reviews/MANIFEST_R1.txt"
        man("freeze", TE, ME, "--extra", f"{TE}/reviews/INPUTS.txt")
        rows_e = {l_[66:]: l_[:64] for l_ in MT.read_manifest(os.path.join(TMP, ME))[2]}
        lfh = lambda b_: _hl.sha256(b_.replace(b"\r\n", b"\n")).hexdigest()  # noqa: E731
        results.append(("R06 freeze records the LF-normalised sha256 of a text file (CRLF, LF and mixed files) and the "
                        "raw sha256 of a file with a NUL byte",
                        rows_e.get("b.md") == lfh(E_FILES[f"{TE}/b.md"]) and rows_e.get("a.md") == lfh(E_FILES[f"{TE}/a.md"])
                        and rows_e.get("mixed.md") == lfh(E_FILES[f"{TE}/mixed.md"])
                        and rows_e.get(f"EXT:{EXT6}") == lfh(E_FILES[EXT6])
                        and rows_e.get("bin.dat") == _hl.sha256(E_FILES[f"{TE}/bin.dat"]).hexdigest()))
        for k_ in (f"{TE}/a.md", f"{TE}/b.md", f"{TE}/mixed.md", EXT6):
            flip(k_)
        rc_f, out_f = man("verify", TE, ME)
        dg_flip = MT.digest(MT.ticket_entries(os.path.join(TMP, TE)) + MT.extra_entries(TMP, [EXT6]))
        results.append(("R06 every text file's line endings flipped (LF <-> CRLF, a mixed file made uniform): verify OK, "
                        "and a re-freeze gives the same digest", rc_f == 0 and "verify: OK" in out_f
                        and dg_flip == MT.read_manifest(os.path.join(TMP, ME))[0]))
        a_crlf = getb(f"{TE}/a.md")
        putb(f"{TE}/a.md", a_crlf.replace(b"A holds", b"B holds"))
        rc_1, out_1 = man("verify", TE, ME)
        putb(f"{TE}/a.md", a_crlf.replace(b"\r\n", b"\r", 1))  # a lone CR is a content change, not an EOL variant
        rc_2, out_2 = man("verify", TE, ME)
        putb(f"{TE}/a.md", a_crlf + b"\r\n")  # one more (empty) line
        rc_3, out_3 = man("verify", TE, ME)
        putb(f"{TE}/a.md", a_crlf)
        results.append(("R06 a one-byte content edit (CRLF checkout), a lone CR and an extra line still fail verify "
                        "(CHANGED a.md)", all(rc_ != 0 and "CHANGED a.md" in o_ for rc_, o_ in
                                              ((rc_1, out_1), (rc_2, out_2), (rc_3, out_3)))))
        flip(f"{TE}/bin.dat")
        rc_b, out_b = man("verify", TE, ME)
        putb(f"{TE}/bin.dat", E_FILES[f"{TE}/bin.dat"])
        rc_b0, _ = man("verify", TE, ME)
        results.append(("R06 a file with a NUL byte is hashed raw: its CRLF -> LF conversion fails verify; restored -> OK",
                        rc_b != 0 and "CHANGED bin.dat" in out_b and rc_b0 == 0))
        # a legacy (pre-R06) manifest: raw-byte hashes of a mixed LF / CRLF tree
        for k_, v_ in E_FILES.items():
            putb(k_, v_)
        legacy_rows = sorted(f"{_hl.sha256(getb(p_)).hexdigest()}  {n_}" for p_, n_ in
                             [(f"{TE}/{x_}", x_) for x_ in ("a.md", "b.md", "bin.dat", "mixed.md")])
        legacy_rows = [l_ for _, l_ in sorted((l_[66:], l_) for l_ in legacy_rows)]
        legacy_rows.append(f"{_hl.sha256(getb(EXT6)).hexdigest()}  EXT:{EXT6}")
        ML = f"{TE}/reviews/MANIFEST_LEG.txt"
        put(ML, f"MANIFEST {MT.digest(legacy_rows)}\n#EXTRA {EXT6}\n" + "\n".join(legacy_rows) + "\n")
        rc_l0, _ = man("verify", TE, ML)
        for k_ in (f"{TE}/a.md", f"{TE}/b.md", EXT6):
            flip(k_)
        rc_l1, out_l1 = man("verify", TE, ML)
        putb(f"{TE}/b.md", getb(f"{TE}/b.md").replace(b"B holds", b"C holds"))
        rc_l2, out_l2 = man("verify", TE, ML)
        results.append(("R06 a legacy raw-byte manifest of a mixed tree verifies on the frozen tree and after an LF <-> "
                        "CRLF flip; a one-byte edit still fails", rc_l0 == 0 and rc_l1 == 0 and "verify: OK" in out_l1
                        and rc_l2 != 0 and "CHANGED b.md" in out_l2))

        # Sol R06FIX F1: a lone CR (CR CR LF) is content, never an EOL variant: legacy raw manifest and fresh freeze
        TC = "Theory_work/WaveT/R06CR"
        os.makedirs(os.path.join(TMP, TC, "reviews"), exist_ok=True)
        putb(f"{TC}/a.md", b"a\r\n")
        rows_c = [f"{_hl.sha256(b'a' + bytes([13, 10])).hexdigest()}  a.md"]
        MC = f"{TC}/reviews/MANIFEST_LEG.txt"
        put(MC, f"MANIFEST {MT.digest(rows_c)}\n" + "\n".join(rows_c) + "\n")
        rc_c0, _ = man("verify", TC, MC)
        putb(f"{TC}/a.md", b"a\r\r\n")
        rc_c1, out_c1 = man("verify", TC, MC)
        MC2 = f"{TC}/reviews/MANIFEST_R1.txt"
        man("freeze", TC, MC2)
        rec_c2 = MT.read_manifest(os.path.join(TMP, MC2))[2][0][:64]
        rc_c2, _ = man("verify", TC, MC2)
        putb(f"{TC}/a.md", b"a\n")
        rc_c3, out_c3 = man("verify", TC, MC2)
        putb(f"{TC}/a.md", b"a\r\n")
        rc_c4, out_c4 = man("verify", TC, MC2)
        results.append(("R06FIX F1 a lone CR is content: CR CR LF does not verify against a legacy raw CR LF hash; a "
                        "fresh freeze of CR CR LF records the raw hash and refuses LF and CR LF",
                        rc_c0 == 0 and rc_c1 != 0 and "CHANGED a.md" in out_c1
                        and rec_c2 == _hl.sha256(bytes([97, 13, 13, 10])).hexdigest() and rc_c2 == 0
                        and rc_c3 != 0 and "CHANGED a.md" in out_c3 and rc_c4 != 0 and "CHANGED a.md" in out_c4))

        # every MANIFEST_*.txt of HEAD and of the ticket branches, on an LF and a CRLF clone (git -c core.autocrlf=...)
        def lgit(*a, cwd=LIVE_ROOT, check=True):
            p_ = subprocess.run(["git", "-C", cwd, *a], capture_output=True, text=True, encoding="utf-8",
                                errors="replace")
            if check and p_.returncode:
                raise RuntimeError(f"git {a[:3]}: {p_.stderr[:300]}")
            return p_.stdout
        refs6 = {"HEAD": lgit("rev-parse", "HEAD").strip()}
        missing6 = []
        for b_ in ("theory/W3-START", "theory/W3-PSHARP", "theory/W3-MISR", "theory/W3-RM2"):
            for full_ in (f"refs/heads/{b_}", f"refs/remotes/origin/{b_}"):
                c_ = lgit("rev-parse", "--verify", "-q", full_ + "^{commit}", check=False).strip()
                if c_:
                    refs6[b_] = c_
                    break
            else:  # an absent branch counts only if HEAD carries its ticket folder (merged)
                if not lgit("ls-tree", "-d", "--name-only", refs6["HEAD"], f"Theory_work/Wave3/{b_.split('/')[1]}/reviews").strip():
                    missing6.append(b_)
        jobs6 = []  # (label, commit, manifest path)
        for lab_, c_ in refs6.items():
            for f_ in lgit("ls-tree", "-r", "--name-only", c_, "--", "Theory_work").splitlines():
                if "/reviews/MANIFEST_" in f_ and f_.endswith(".txt"):
                    jobs6.append((lab_, c_, f_))
                    last_ = lgit("log", "-1", "--format=%H", c_, "--", f_).strip()
                    if last_ and last_ != c_:
                        jobs6.append((lab_ + "@freeze", last_, f_))
        pats6 = {"/.gitattributes", "/Theory_work/", "/Docs/", "/Scripts/SMC_BVS/"}
        for _, c_, f_ in jobs6:
            for ln_ in lgit("show", f"{c_}:{f_}").splitlines():
                if ln_.startswith("#EXTRA "):
                    pats6.add("/" + ln_[7:].strip())
        old_src = lgit("show", "3ce2e27:Theory_work/Wave3/tools/manifest.py")  # the pre-R06 (raw-byte) tool
        OLDP = put("r06_old_manifest.py", old_src)
        _so = importlib.util.spec_from_file_location("bvs_manifest_pre_r06", OLDP)
        MO = importlib.util.module_from_spec(_so)
        _so.loader.exec_module(MO)
        CROOT = _tf.mkdtemp(prefix="bvs_r06_")
        ver6, old6, fp6 = {}, {}, {}
        FP_SCRIPT = ("import os, sys\nsys.dont_write_bytecode = True\nsys.path.insert(0, sys.argv[1])\n"
                     "import bvsreg as R\nrows = R.load_claims()\nby = R.index(rows)\ng = R.Graph(rows)\n"
                     "al = R.load_aliases()\nf = R.ticket_folders()\nout = []\nfor r in rows:\n"
                     "    out.append('\\t'.join([r['id'], R.claim_hash(r) or '-', R.status_sha(r.get('status_source', '')),"
                     " R.accept_stamp(r['id'], by, g, al, f)]))\n"
                     "open(sys.argv[2], 'w', encoding='utf-8').write('\\n'.join(out))\n")
        try:
            for mode_, ac_ in (("LF", "false"), ("CRLF", "true")):
                d_ = os.path.join(CROOT, mode_)
                subprocess.run(["git", "-c", f"core.autocrlf={ac_}", "clone", "-q", "--shared", "--no-checkout",
                                "-c", f"core.autocrlf={ac_}", "-c", "core.longpaths=true", LIVE_ROOT, d_],
                               check=True, capture_output=True)
                lgit("config", "core.eol", "crlf" if ac_ == "true" else "lf", cwd=d_)
                lgit("sparse-checkout", "set", "--no-cone", *sorted(pats6), cwd=d_)
                for lab_, c_, f_ in jobs6:
                    lgit("checkout", "-q", "--force", c_, cwd=d_)
                    td_ = os.path.join(d_, os.path.dirname(os.path.dirname(f_)))
                    mp_ = os.path.join(d_, f_)
                    try:
                        ver6[(mode_, lab_, f_)] = MT.verify_problems(td_, mp_, d_)[1]
                    except MT.ManifestError as e_:
                        ver6[(mode_, lab_, f_)] = [f"ERROR {e_}"]
                    try:
                        old6[(mode_, lab_, f_)] = MO.verify_problems(td_, mp_, d_)[1]
                    except MO.ManifestError as e_:
                        old6[(mode_, lab_, f_)] = [f"ERROR {e_}"]
                # registry fingerprints (sha256, status_sha256, fp2) on this checkout of HEAD, with the working tools
                lgit("checkout", "-q", "--force", refs6["HEAD"], cwd=d_)
                for src_ in (os.path.join(INFRA, "tools"), os.path.join(TMP, "Theory_work", "Wave3", "tools")):
                    rel_ = os.path.relpath(src_, TMP)
                    for fn_ in os.listdir(src_):
                        if fn_.endswith(".py"):
                            shutil.copy2(os.path.join(src_, fn_), os.path.join(d_, rel_, fn_))
                fpo_ = os.path.join(CROOT, f"fp_{mode_}.tsv")
                subprocess.run([sys.executable, "-c", FP_SCRIPT, os.path.join(d_, "Theory_work", "INFRA", "tools"),
                                fpo_], capture_output=True, cwd=d_)
                fp6[mode_] = open(fpo_, encoding="utf-8").read() if os.path.exists(fpo_) else ""
        finally:
            shutil.rmtree(CROOT, ignore_errors=True)
        keys6 = sorted({k_[1:] for k_ in ver6})
        same6 = [k_ for k_ in keys6 if ver6.get(("LF",) + k_) == ver6.get(("CRLF",) + k_)]
        print(f"R06 clones: {len(keys6)} (manifest, commit) checks on {len(refs6)} refs "
              f"({', '.join(sorted(refs6))}); missing refs: {missing6 or 'none'}")
        for k_ in keys6:
            if k_ not in same6:
                print("  LF/CRLF differ:", k_, ver6.get(("LF",) + k_)[:3], ver6.get(("CRLF",) + k_)[:3])
        results.append((f"R06 every MANIFEST_*.txt of HEAD and the ticket branches ({len(keys6)} manifest x commit "
                        "checks, branch heads and the commit that wrote each manifest) gives the same verify result "
                        "on an LF and on a CRLF clone", len(keys6) >= 40 and same6 == keys6 and not missing6))
        must6 = [("theory/W3-START", "Theory_work/Wave3/W3-START/reviews/MANIFEST_R2.txt"),
                 ("theory/W3-PSHARP", "Theory_work/Wave3/W3-PSHARP/reviews/MANIFEST_R2.txt"),
                 ("theory/W3-MISR", "Theory_work/Wave3/W3-MISR/reviews/MANIFEST_R2.txt"),
                 ("theory/W3-RM2", "Theory_work/Wave3/W3-RM2/reviews/MANIFEST_R1.txt"),
                 ("theory/W3-START@freeze", "Theory_work/Wave3/W3-START/reviews/MANIFEST_BT1.txt"),
                 ("theory/W3-START@freeze", "Theory_work/Wave3/W3-START/reviews/MANIFEST_MP1.txt"),
                 ("theory/W3-START@freeze", "Theory_work/Wave3/W3-START/reviews/MANIFEST_R1.txt"),
                 ("theory/W3-PSHARP@freeze", "Theory_work/Wave3/W3-PSHARP/reviews/MANIFEST_R1.txt"),
                 ("theory/W3-MISR@freeze", "Theory_work/Wave3/W3-MISR/reviews/MANIFEST_R1.txt"),
                 ("theory/W3-RM2@freeze", "Theory_work/Wave3/W3-RM2/reviews/MANIFEST_BT1.txt"),
                 ("theory/W3-RM2@freeze", "Theory_work/Wave3/W3-RM2/reviews/MANIFEST_RC4.txt")]
        must6 = [k_ for k_ in must6 if k_[0].split("@")[0] in refs6]  # a merged, deleted branch: covered via HEAD
        ok_must = [k_ for k_ in must6 if ver6.get(("LF",) + k_) == [] and ver6.get(("CRLF",) + k_) == []]
        old_fail = [k_ for k_ in must6 if old6.get(("LF",) + k_) or old6.get(("CRLF",) + k_)]
        for k_ in must6:
            if k_ not in ok_must:
                print("  expected OK:", k_, (ver6.get(("LF",) + k_) or [])[:3], (ver6.get(("CRLF",) + k_) or [])[:3])
        results.append(("R06 the council / acceptance manifests (START R2, PSHARP R2, MISR R2, RM2 R1 at the branch "
                        "heads; START BT1/MP1/R1, PSHARP R1, MISR R1, RM2 BT1/RC4 where they were written) verify on "
                        "both clones; the pre-R06 raw-byte tool fails each of them on at least one clone",
                        ok_must == must6 and old_fail == must6))
        n_fp = len([l_ for l_ in fp6.get("LF", "").splitlines() if l_.strip()])
        results.append((f"R06 registry fingerprints (sha256, status_sha256, fp2 accept stamp) of all {n_fp} claims are "
                        "identical on the LF and the CRLF clone", n_fp > 100 and fp6.get("LF") == fp6.get("CRLF")))

        # ---------------- INFRA R06: per-claim tables by dated addendum (R05 safeguard 4) ----------------
        T6 = "Theory_work/WaveT/R06T"
        CK6 = f"{T6}/CHECKPOINT_3.md"
        put(f"{T6}/STATEMENT.md", "Lemma A. A holds.\nLemma B. B holds.\nLemma C. C holds.\n")
        put(f"{T6}/PROOF.md", "Proofs of A, B and C.\n")
        put(f"{T6}/REPORT.md", "# R06T report\nPROVED-CHECKED\nPROVED-CHECKED\n")
        os.makedirs(os.path.join(TMP, T6, "reviews"), exist_ok=True)
        man("freeze", T6, f"{T6}/reviews/MANIFEST_R1.txt")
        dg6 = mhead(f"{T6}/reviews/MANIFEST_R1.txt")
        cell6 = f"R1; MANIFEST {dg6}; sol=8.6 PASS(reviews/R1_council_sol.md); opus=8.4 PASS(reviews/R1_council_opus.md)"
        S6, O6 = f"{T6}/reviews/R1_council_sol.md", f"{T6}/reviews/R1_council_opus.md"

        def r06_review(seat, score, adds=(), body_table=None, extra=""):
            txt = f"Council R1 ({seat}). Score {score}, all gates PASS.\n\n"
            if body_table:
                txt += "| id | decision |\n|---|---|\n" + "".join(f"| {i} | {d_} |\n" for i, d_ in body_table) + "\n"
            txt += vline(dg6, seat, score)
            if adds:
                txt += ("\n## Addendum 2026-11-12: per-claim table (fresh thread, same seat model, frozen manifest and "
                        "own review; no rescoring)\n\n| id | decision |\n|---|---|\n"
                        + "".join(f"| {i} | {d_} |\n" for i, d_ in adds))
            return txt + extra
        ADD6 = [("A", "ACCEPT"), ("B", "ACCEPT"), ("C", "NOT-EXAMINED")]
        put(S6, r06_review("sol", "8.6", ADD6))
        put(O6, r06_review("opus", "8.4", ADD6))

        def r06_blk(loc, ln, sl, status="PROVED-CHECKED", council=True):
            return ("```\nREGISTRY\n"
                    f"claim: R06T:{loc} | kind: lemma | statement: STATEMENT.md:{ln} | premises: none\n"
                    f"name: Lemma {loc}\nstatus: {status} | status_source: CHECKPOINT_3.md:{sl}\n"
                    + (f"council: {cell6}\n" if council else "") + "```\n")

        def r06_ckpt(c_checked=False):
            return ("# R06T checkpoint 3\n\n"
                    "- R06T:A — PROVED-CHECKED — Lemma A. Council R1 (addendum): ACCEPT.\n"
                    "- R06T:B — PROVED-CHECKED — Lemma B. Council R1 (addendum): ACCEPT.\n"
                    + ("- R06T:C — PROVED-CHECKED — Lemma C.\n" if c_checked else
                       "- R06T:C — PROVED (by this seat, unchecked) — Lemma C, NOT-EXAMINED by the council.\n") + "\n"
                    + r06_blk("A", 1, 3) + "\n" + r06_blk("B", 2, 4) + "\n"
                    + (r06_blk("C", 3, 5) if c_checked else
                       r06_blk("C", 3, 5, "PROVED (by this seat, unchecked)", council=False)))
        put(CK6, r06_ckpt())
        rc_a1, out_a1 = tool("ingest.py", "claims", os.path.join(TMP, CK6), "--staged")
        put(CK6, r06_ckpt(c_checked=True))
        rc_a2, out_a2 = tool("ingest.py", "claims", os.path.join(TMP, CK6), "--staged")
        put(CK6, r06_ckpt())
        results.append(("R06 4a: per-claim tables appended as a dated addendum after the COUNCIL-VERDICT line (ACCEPT / "
                        "NOT-EXAMINED) pass the checkpoint acceptance; the NOT-EXAMINED id stays in the checkpoint "
                        "without a checked label",
                        rc_a1 == 0 and "PASS" in acc_l(out_a1) and "REFUSED" not in acc_l(out_a1)))
        results.append(("R06 4a: the NOT-EXAMINED id with a checked label in the checkpoint is REFUSED (A4: carries a "
                        "checked-labelled id the seat did not accept)",
                        rc_a2 != 0 and "REFUSED" in acc_l(out_a2) and "did not accept" in out_a2 and "R06T:C" in out_a2))
        # a second verdict line in the addendum (same digest; another digest) is refused; the original line binds
        put(O6, r06_review("opus", "8.4", ADD6, extra="\n" + vline(dg6, "opus", "9.5")))
        rc_v1, out_v1 = tool("ingest.py", "claims", os.path.join(TMP, CK6), "--staged")
        put(O6, r06_review("opus", "8.4", ADD6, extra="\n" + vline(dgL, "opus", "9.5")))
        rc_v2, out_v2 = tool("ingest.py", "claims", os.path.join(TMP, CK6), "--staged")
        rc_bd, out_bd = man("bind", f"{T6}/reviews/MANIFEST_R1.txt", S6, O6)
        put(O6, r06_review("opus", "8.4", ADD6))
        rc_bg, out_bg = man("bind", f"{T6}/reviews/MANIFEST_R1.txt", S6, O6, "--council", cell6)
        results.append(("R06 4a: an addendum carrying a second COUNCIL-VERDICT line (same digest, new score; or another "
                        "digest) is REFUSED (A4 and manifest.py bind); the original verdict binds (bind OK, cell match)",
                        rc_v1 != 0 and "2 COUNCIL-VERDICT lines" in out_v1 and rc_v2 != 0
                        and "contradictory COUNCIL-VERDICT" in out_v2 and rc_bd != 0 and rc_bg == 0))
        # an addendum contradicting the body table (body: B not accepted) is refused
        put(S6, r06_review("sol", "8.6", ADD6, body_table=[("A", "accepted"), ("B", "not accepted (gap)")]))
        rc_c6, out_c6 = tool("ingest.py", "claims", os.path.join(TMP, CK6), "--staged")
        put(S6, r06_review("sol", "8.6", ADD6))
        results.append(("R06 4a: an addendum ACCEPT contradicting a body-table 'not accepted' is REFUSED (contradictory "
                        "decisions)", rc_c6 != 0 and "contradictory decisions" in out_c6 and "R06T:B" in out_c6))

        # ---------------- INFRA R07: a valid addendum supersedes the body table (body read only for negatives) -------
        R07_REAL = ["accepted with non-blocking remarks (Issue 5: the η = 0 sentence is read under the premise of F1(ii))",
                    "accepted with non-blocking remarks (Issue 3)",
                    "accepted with non-blocking remarks (Issue 2: wording of the P-OVL row in `STATEMENT.md` §4, not "
                    "of OVL itself)",
                    "accepted (F-1, F-2, F-3, G-1, G-2 verified; UNI-0 and AR(1) correctly not claimed)"]
        H7 = "| id | decision |\n|---|---|\n"
        V7 = "\n" + vline("a" * 64, "sol", "9.0") + "\n## Addendum\n\n"
        A7 = H7 + "| A | ACCEPT |\n| B | ACCEPT |\n"

        def r07(body, add=A7, cid="T:A"):
            return R.seat_table(body + "\n" + V7 + add, "T")[0].get(cid)
        # positives: the four real Opus cells, the Sol Basis column (negative words only there), free text, extra cols
        R07_POS = [H7 + f"| A | {c_} |\n| B | accepted |\n" for c_ in R07_REAL] + [
            "| Id | Disposition | Basis |\n|---|---|---|\n| A | accepted | an earlier draft failed; the gap was rejected "
            "and withdrawn, then fixed |\n| B | accepted | x |\n",
            H7 + "| A | looks fine (conditional on nothing) |\n| B | ok |\n",
            H7 + "| A | accepted | stray |\n| B | accepted |\n", "", "No body table.\n"]
        # negatives in the body decision column (any case / emphasis / dash / spacing / invisible-character variant)
        R07_NEG = ["accepted (withdrawn)", "rejected", "Rejected", "REJECT", "not accepted", "**NOT** accepted",
                   "not  accepted", "NOTACCEPTED", "not-accepted", "NOT-EXAMINED", "not examined", "Not_Examined",
                   "refused", "Refusal", "failed", "proof fails", "withdraw", "with\u200bdrawn", "re\u00adject",
                   "ＲＥＪＥＣＴ", "accepted, then withdrawn", "accepted (status: NOT\u2011EXAMINED)"]
        r07_pos_bad = [i_ for i_, b_ in enumerate(R07_POS) if r07(b_) is not True]
        r07_neg_bad = [d_ for d_ in R07_NEG if r07(H7 + f"| A | {d_} |\n| B | accepted |\n") is not False]
        # structural: a negative split / continued into another line, after a separator, behind an escaped pipe
        R07_STRUCT = {"split": H7 + "| A | accepted\nwithdrawn |\n", "continued": H7 + "| A | accepted |\n| | rejected |\n",
                      "u2028": H7 + "| A | accepted |\u2028| | rejected |\n",
                      "escaped": "| id | decision | basis |\n|---|---|---|\n| A | accepted \\| rejected | x |\n",
                      "missing_from_addendum": H7 + "| A | accepted |\n| B | accepted |\n"}
        # Sol R07 rule-2 F1: a separator before / inside the header line block; F2: any Unicode dash (Pd)
        for sp_ in ["\r", "\x0b", "\x0c", "\x1c", "\x1d", "\x1e", "\x85", "\u2028", "\u2029"]:
            R07_STRUCT[f"hdr_sep_{ord(sp_):x}"] = sp_.join(["| id | decision |", "|---|---|", "| A | reject |", ""])
        R07_STRUCT["intro_u2028"] = "Intro\u2028" + H7 + "| A | reject |\n"
        for dc_ in [chr(c_) for c_ in range(0x110000) if unicodedata.category(chr(c_)) == "Pd"]:
            R07_STRUCT[f"dash_{ord(dc_):x}"] = H7 + f"| A | not{dc_}accepted |\n"
        r07_struct_bad = [k_ for k_, b_ in R07_STRUCT.items()
                          if r07(b_, add=(H7 + "| B | ACCEPT |\n" if k_ == "missing_from_addendum" else A7))]
        # Sol R07 rule-2 F3: a blank line made of separators ends the body table like LF (later free text ignored)
        R07_POS += [H7 + "| A | accepted |\n" + sp_ + sp_ + "rejected\n"
                    for sp_ in ["\r", "\x0b", "\x0c", "\x1c", "\x1d", "\x1e", "\x85", "\u2028", "\u2029", "\n"]]
        r07_pos_bad = [i_ for i_, b_ in enumerate(R07_POS) if r07(b_) is not True]
        # no valid addendum: the strict R06 reading of the whole file, unchanged (form cells, Basis column refused)
        r07_noadd = [c_ for c_ in R07_REAL + ["accepted (withdrawn)"]
                     if R.seat_table(H7 + f"| A | {c_} |\n", "T")[0].get("T:A")]
        r07_badadd = R.seat_table(H7 + "| A | accepted |\n" + V7 + "| **id** | decision |\n|---|---|\n| A | ACCEPT |\n",
                                  "T")[0].get("T:A")
        r07_noverd = R.seat_table(H7 + f"| A | {R07_REAL[1]} |\n\n## Addendum\n\n" + A7, "T")[0].get("T:A")
        print(f"R07 addendum: positives refused {r07_pos_bad}; negatives accepted {r07_neg_bad}; structural accepted "
              f"{r07_struct_bad}; no-addendum form cells accepted {r07_noadd}; malformed addendum {r07_badadd}; "
              f"addendum without a verdict line {r07_noverd}")
        results.append(("R07 addendum supersedes body: the four real Opus cells, a Basis column with negative words, "
                        "free text and extra columns in the body + addendum ACCEPT -> accepted; a closed-list negative in "
                        "the body decision column (case / emphasis / dash / spacing / invisible / full-width variants, "
                        "split, continued, U+2028, escaped pipe) or a body id missing from the addendum -> NOT accepted",
                        not r07_pos_bad and not r07_neg_bad and not r07_struct_bad))
        results.append(("R07 without a valid addendum (none, malformed header, or no COUNCIL-VERDICT line before it) the "
                        "strict R06 reading applies unchanged: remark-form body cells are NOT accepted",
                        not r07_noadd and r07_badadd is False and r07_noverd is False))
        # staged: Basis column body + addendum PASS; body 'accepted (withdrawn)' / 'rejected' / id missing -> REFUSED
        BASIS7 = ("| Id | Disposition | Basis |\n|---|---|---|\n| A | accepted | the first attempt failed and was "
                  "withdrawn |\n| B | accepted with non-blocking remarks (Issue 3) | ok |\n| C | accepted | x |\n\n")

        def r07_review(seat, score, body, adds=ADD6):
            return (f"Council R1 ({seat}). Score {score}, all gates PASS.\n\n" + body + vline(dg6, seat, score)
                    + "\n## Addendum 2026-11-12\n\n| id | decision |\n|---|---|\n"
                    + "".join(f"| {i} | {d_} |\n" for i, d_ in adds))
        st7 = {}
        for nm_, sb_, ob_, ad_ in (
                ("basis_pass", BASIS7, H7 + f"| A | {R07_REAL[0]} |\n| B | {R07_REAL[3]} |\n\n", ADD6),
                ("withdrawn", BASIS7, H7 + "| A | accepted (withdrawn) |\n| B | accepted |\n\n", ADD6),
                ("rejected", BASIS7, H7 + "| A | accepted |\n| B | rejected |\n\n", ADD6),
                ("missing", BASIS7, H7 + "| A | accepted |\n| B | accepted |\n\n",
                 [("A", "ACCEPT"), ("C", "NOT-EXAMINED")])):
            put(S6, r07_review("sol", "8.6", sb_))
            put(O6, r07_review("opus", "8.4", ob_, ad_))
            rc_v, out_v = tool("ingest.py", "claims", os.path.join(TMP, CK6), "--staged")
            st7[nm_] = (rc_v, acc_l(out_v), out_v)
        put(S6, r06_review("sol", "8.6", ADD6))
        put(O6, r06_review("opus", "8.4", ADD6))
        print("R07 staged:", {k_: (v_[0], v_[1].split(":")[-1].strip()[:30]) for k_, v_ in st7.items()})
        results.append(("R07 staged checkpoint: Sol Basis-column body + Opus remark-form body + addenda -> PASS; body "
                        "'accepted (withdrawn)' (A) or 'rejected' (B) + addendum ACCEPT -> REFUSED naming the claim; "
                        "a body id missing from the addendum (B) -> REFUSED",
                        st7["basis_pass"][0] == 0 and "PASS" in st7["basis_pass"][1]
                        and all(st7[k_][0] != 0 and "REFUSED" in st7[k_][1] and c_ in st7[k_][2]
                                for k_, c_ in (("withdrawn", "claim R06T:A: listed with contradictory decisions"),
                                               ("rejected", "claim R06T:B: listed with contradictory decisions"),
                                               ("missing", "claim R06T:B: listed in the body table but not in the "
                                                           "seat's addendum")))))

        # ---------------- INFRA R06: registry blocks from a carrier file outside the frozen manifest ----------------
        CAR = f"{T6}/reviews/CARRIER_R1.jsonl"  # reviews/ is never in a manifest
        hdr_t6, trows6 = R.read_tsv(R.TICKETS)  # the ticket folder locates the frozen manifest (tickets.tsv folder)
        if not any(t_["ticket"] == "R06T" for t_ in trows6):
            trows6.append({**{h_: "" for h_ in hdr_t6}, "ticket": "R06T", "folder": T6})
            R.write_tsv(R.TICKETS, hdr_t6, trows6)

        def c6row(loc, line, **kw):
            base_ = dict(ticket="R06T", local_id=loc, kind="lemma", name=f"Lemma {loc}", file=f"{T6}/STATEMENT.md",
                         lines=[line, line], premises=[], status="PROVED-CHECKED",
                         status_source=f"{T6}/REPORT.md:{1 + line}", council=cell6)
            base_.update(kw)
            return base_

        def carrier(rel, objs):
            return put(rel, "".join(_json.dumps(o, ensure_ascii=False) + "\n" for o in objs))
        put(CK6, "# R06T checkpoint 3 (status lines only)\n\n- R06T:A — PROVED-CHECKED — Lemma A.\n"
            "- R06T:B — PROVED-CHECKED — Lemma B.\n")
        carrier(CAR, [c6row("A", 1), c6row("B", 2)])  # status lines in a covered file (REPORT.md)
        rc_cv, _ = man("verify", T6, f"{T6}/reviews/MANIFEST_R1.txt")
        rc_k1, out_k1 = tool("ingest.py", "claims", os.path.join(TMP, CAR), "--staged")
        carrier(CAR, [c6row("A", 1, status_source=f"{CK6}:3"), c6row("B", 2, status_source=f"{CK6}:4")])
        rc_k3, out_k3 = tool("ingest.py", "claims", os.path.join(TMP, CAR), "--staged")  # status lines: own checkpoint
        MDC = f"{T6}/reviews/CARRIER_R1.md"  # the REGISTRY-block form, paths written from Theory_work/
        put(MDC, "```\nREGISTRY\n"
            f"claim: R06T:A | kind: lemma | statement: {T6}/STATEMENT.md:1 | premises: none\n"
            f"name: Lemma A\nstatus: PROVED-CHECKED | status_source: {T6}/REPORT.md:2\ncouncil: {cell6}\n```\n")
        rc_k2, out_k2 = tool("ingest.py", "claims", os.path.join(TMP, MDC), "--staged")
        results.append(("R06 4b: ingest takes registry rows from a carrier outside the frozen manifest (reviews/*.jsonl; "
                        "REGISTRY-block .md), status in a covered file or the own checkpoint: PASS; the manifest still "
                        "verifies", rc_cv == 0 and rc_k1 == 0 and "PASS" in acc_l(out_k1) and "REFUSED" not in
                        acc_l(out_k1) and rc_k2 == 0 and "PASS" in acc_l(out_k2) and rc_k3 == 0
                        and "PASS" in acc_l(out_k3) and "REFUSED" not in acc_l(out_k3)))
        put(f"{T6}/reviews/STATEMENT_extra.md", "Lemma A. A holds.\n")
        carrier(CAR, [c6row("A", 1, file=f"{T6}/reviews/STATEMENT_extra.md")])
        rc_u1, out_u1 = tool("ingest.py", "claims", os.path.join(TMP, CAR), "--staged")
        carrier(CAR, [c6row("A", 1, premises=[f"{T6}/reviews/STATEMENT_extra.md:1-1"])])
        rc_u2, out_u2 = tool("ingest.py", "claims", os.path.join(TMP, CAR), "--staged")
        carrier(CAR, [c6row("A", 1, file=CAR, lines=[1, 1])])
        rc_u3, out_u3 = tool("ingest.py", "claims", os.path.join(TMP, CAR), "--staged")
        results.append(("R06 4b: a carrier row whose statement or premise file is outside the manifest (incl. the carrier "
                        "itself) is REFUSED (A4 coverage)",
                        rc_u1 != 0 and f"does not cover {T6}/reviews/STATEMENT_extra.md" in out_u1
                        and rc_u2 != 0 and f"does not cover {T6}/reviews/STATEMENT_extra.md" in out_u2
                        and rc_u3 != 0 and "REFUSED" in acc_l(out_u3) and f"does not cover {CAR}" in out_u3))
        carrier(CAR, [c6row("C", 3, status_source=f"{T6}/REPORT.md:3")])
        rc_n1, out_n1 = tool("ingest.py", "claims", os.path.join(TMP, CAR), "--staged")
        carrier(CAR, [c6row("D", 3, status_source=f"{T6}/REPORT.md:3")])
        rc_n2, out_n2 = tool("ingest.py", "claims", os.path.join(TMP, CAR), "--staged")
        put(O6, r06_review("opus", "8.4"))  # one seat without any table, the other with one
        carrier(CAR, [c6row("A", 1)])
        rc_n3, out_n3 = tool("ingest.py", "claims", os.path.join(TMP, CAR), "--staged")
        put(O6, r06_review("opus", "8.4", ADD6))
        results.append(("R06 4b: through a carrier, a checked claim the seats marked NOT-EXAMINED, or that is missing from "
                        "their tables, or lacks one seat's table, is REFUSED (A4)",
                        rc_n1 != 0 and "R06T:C" in out_n1 and "decision is not ACCEPT" in out_n1
                        and rc_n2 != 0 and "missing from the per-claim table" in out_n2
                        and rc_n3 != 0 and "has no per-claim table" in out_n3))

        # INFRA R06 decision reader: STRICT WHITELIST, fail closed (HQ ruling after Sol R06FIX recheck 2). Sol's 95
        # cases (R06FIX/decision_cases.json: exact tables) are read as `expected`; Sol's 13 positive controls with
        # remarks / other spellings are refused by design (`whitelist_refuses`); every refusal other than an exact
        # NOT-EXAMINED carries a problem naming the claim
        DCF = _json.load(open(os.path.join(INFRA, "R06FIX", "decision_cases.json"), encoding="utf-8"))
        d_bad, d_silent = [], []
        for c_ in DCF["cases"]:
            dec_, pr_ = R.seat_decisions(c_["text"], "REV")
            got_ = bool(dec_.get("REV:A"))
            if got_ != c_["expected"]:
                d_bad.append(c_["n"])
            if not got_ and c_["input"] != "NOT-EXAMINED" and not any(p_.startswith("claim REV:A:") for p_ in pr_):
                d_silent.append(c_["n"])
        dev_ = sorted(c_["n"] for c_ in DCF["cases"] if c_["expected"] != c_["sol_expected"])
        print(f"R06 decision cases: {len(DCF['cases'])}; mismatches {d_bad}; refused without a claim message {d_silent}; "
              f"whitelist refuses Sol positives {dev_}")
        results.append(("R06FIX decision reader (strict whitelist): Sol's 95 recheck-2 cases read as expected; all "
                        "refusals but an exact NOT-EXAMINED name the claim; only the 13 listed Sol positive controls "
                        "are refused by design",
                        len(DCF["cases"]) == 95 and not d_bad and not d_silent and dev_ == DCF["whitelist_refuses"]
                        and all(c_["sol_expected"] for c_ in DCF["cases"] if c_["n"] in dev_)))
        GOOD_D = ["ACCEPT", "accepted", "Accepted", "ACCEPTED", " ACCEPT ", "\tACCEPT\t"]
        BAD_D = ["NOT-EXAMINED", "not accepted", "acceptable", "accepted-ish", "ACCEPT=NO", "ACCEPT/NOT-EXAMINED",
                 "ACCEPT not", "accepted, no", "accepted no", "accept: no", "", "accept", "Accept", "aCcEpTeD",
                 "**ACCEPT**", "`accepted`", "ACCEPT.", "ACCEPT" + chr(0xA0), chr(0x2003) + "ACCEPT", "ＡＣＣＥＰＴ",
                 "accepted (not accepted)", "ACCEPT : NO", "accepted with remarks; withdrawn",
                 "ACCEPT" + chr(0x2028) + "NOT-EXAMINED", "accepted (no)", "accepted (conditional)",
                 "accepted with non-blocking remarks (Issue 2)", "accepted (F-1, F-2 verified)"]
        dec_ok = lambda d_: R.seat_table(f"| id | decision |\n|---|---|\n| A | {d_} |\n", "T")[0].get("T:A")  # noqa: E731
        results.append(("R06FIX whitelist: exactly ACCEPT / accepted / Accepted / ACCEPTED (surrounding spaces and "
                        "tabs trimmed) accept; other case, emphasis, punctuation, Unicode spaces / full-width, remarks "
                        "and NOT-EXAMINED do not",
                        all(dec_ok(d_) for d_ in GOOD_D) and not any(dec_ok(d_) for d_ in BAD_D)))
        # Sol recheck 2's five staged carrier variants (and two more structural ones) are REFUSED; ACCEPT passes
        HDR6 = "| id | decision |\n|---|---|\n"
        VAR6 = [("conditional", HDR6 + "| A | accepted (conditional) |\n"),
                ("no_in_remark", HDR6 + "| A | accepted (decision: NO) |\n"),
                ("line_split", HDR6 + "| A | ACCEPT\nNOT-EXAMINED |\n"),
                ("continuation", HDR6 + "| A | ACCEPT |\n| | NOT-EXAMINED |\n"),
                ("negative_remarks_column", "| id | decision | remarks |\n|---|---|---|\n| A | ACCEPT | withdrawn |\n"),
                ("no_leading_pipe_row", HDR6 + "| A | ACCEPT |\nA | NOT-EXAMINED |\n"),
                ("escaped_pipe", HDR6 + "| A | ACCEPT \\| NOT-EXAMINED |\n")]

        def r06_tab_review(seat, score, table):
            return f"Council R1 ({seat}). Score {score}, all gates PASS.\n\n" + vline(dg6, seat, score) + "\n" + table
        carrier(CAR, [c6row("A", 1)])
        var_res = {}
        for nm_, tb_ in VAR6 + [("positive", HDR6 + "| A | ACCEPT |\n")]:
            put(S6, r06_tab_review("sol", "8.6", tb_))
            put(O6, r06_tab_review("opus", "8.4", tb_))
            rc_v, out_v = tool("ingest.py", "claims", os.path.join(TMP, CAR), "--staged")
            var_res[nm_] = (rc_v, acc_l(out_v), "R06T:A" in out_v and "not accepted" in out_v.lower())
        put(S6, r06_review("sol", "8.6", ADD6))
        put(O6, r06_review("opus", "8.4", ADD6))
        print("R06 staged variants:", {k_: (v_[0], v_[1].split(":")[-1].strip()[:30]) for k_, v_ in var_res.items()})
        results.append(("R06FIX staged carrier: Sol's five recheck-2 variants (conditional, decision: NO in a remark, "
                        "line split, continuation row, negative remarks column) and a pipe-less / escaped-pipe row are "
                        "REFUSED with a message naming the claim; a plain ACCEPT table passes",
                        all(var_res[k_][0] != 0 and "REFUSED" in var_res[k_][1] and var_res[k_][2] for k_, _ in VAR6)
                        and var_res["positive"][0] == 0 and "PASS" in var_res["positive"][1]))
        NO6 = [("A", "ACCEPT=NO"), ("B", "ACCEPT"), ("C", "NOT-EXAMINED")]
        put(S6, r06_review("sol", "8.6", NO6))
        put(O6, r06_review("opus", "8.4", NO6))
        carrier(CAR, [c6row("A", 1)])
        rc_f1, out_f1 = tool("ingest.py", "claims", os.path.join(TMP, CAR), "--staged")
        put(CK6, r06_ckpt())
        rc_f2, out_f2 = tool("ingest.py", "claims", os.path.join(TMP, CK6), "--staged")
        NN6 = [("A", "accepted (not accepted)"), ("B", "ACCEPT"), ("C", "NOT-EXAMINED")]
        put(S6, r06_review("sol", "8.6", NN6))
        put(O6, r06_review("opus", "8.4", NN6))
        rc_f4, out_f4 = tool("ingest.py", "claims", os.path.join(TMP, CK6), "--staged")
        put(S6, r06_review("sol", "8.6", ADD6))
        put(O6, r06_review("opus", "8.4", ADD6))
        rc_f3, out_f3 = tool("ingest.py", "claims", os.path.join(TMP, CK6), "--staged")
        results.append(("R06FIX F2 staged: both seats' 'ACCEPT=NO' for A is REFUSED on the carrier path and on the "
                        "own-checkpoint path, 'accepted (not accepted)' on the checkpoint path; restored ACCEPT -> PASS",
                        rc_f1 != 0 and "REFUSED" in acc_l(out_f1) and rc_f2 != 0 and "REFUSED" in acc_l(out_f2)
                        and rc_f4 != 0 and "REFUSED" in acc_l(out_f4)
                        and "R06T:A" in out_f2 and rc_f3 == 0 and "PASS" in acc_l(out_f3)))

        # Sol R06FIX parser test: 116 more direct cases (R06FIX/decision_cases_parser.json), review files read RAW (a
        # text-mode read would turn CR / NEL / U+2028 ... into line breaks), strict header + delimiter row
        DCP = _json.load(open(os.path.join(INFRA, "R06FIX", "decision_cases_parser.json"), encoding="utf-8"))
        p_bad = [c_["n"] for c_ in DCP["cases"]
                 if bool(R.seat_decisions(c_["text"], "REV")[0].get("REV:A")) != c_["expected"]]
        p_dev = sorted(c_["n"] for c_ in DCP["cases"] if c_["expected"] != c_["sol_expected"])
        print(f"R06 parser cases: {len(DCP['cases'])}; mismatches {p_bad}; refused by design {p_dev}")
        results.append(("R06FIX parser test: Sol's 116 further cases read as expected (header aliases exact, delimiter "
                        "row directly below the header, separator-shaped lines validated); only case 110 (no delimiter "
                        "row) is refused by design", len(DCP["cases"]) == 116 and not p_bad
                        and p_dev == DCP["whitelist_refuses"] == [110]))
        SEPS = ["\r", "\x0b", "\x0c", "\x1c", "\x1d", "\x1e", "\x85", "\u2028", "\u2029"]
        loaded = []
        for k_, sp_ in enumerate(SEPS):
            rel_ = f"{T6}/reviews/sepfile_{k_}.md"
            putb(rel_, ("| id | decision |\n|---|---|\n| A | ACCEPT |" + sp_ + " \n").encode("utf-8"))
            loaded.append(bool(R.seat_table(R.evidence_raw_text(rel_), "REV")[0].get("REV:A")))
            os.remove(os.path.join(TMP, rel_))
        putb(f"{T6}/reviews/crlf_ok.md", b"| id | decision |\r\n|---|---|\r\n| A | ACCEPT |\r\n")
        crlf_ok = bool(R.seat_table(R.evidence_raw_text(f"{T6}/reviews/crlf_ok.md"), "REV")[0].get("REV:A"))
        os.remove(os.path.join(TMP, T6, "reviews", "crlf_ok.md"))
        results.append(("R06FIX parser test: review files are read raw: a row followed by CR, VT, FF, FS, GS, RS, NEL, "
                        "U+2028 or U+2029 in the FILE reads as NOT accepted; a CRLF file still reads ACCEPT",
                        not any(loaded) and len(loaded) == 9 and crlf_ok))
        STG = [("file_u2028", HDR6 + "| A | ACCEPT |\u2028 \n"), ("file_lone_cr", HDR6 + "| A | ACCEPT |\r \n"),
               ("bare_separator", HDR6 + "| A | ACCEPT |\n---\n"),
               ("emphasis_header", "| **id** | decision |\n|---|---|\n| A | ACCEPT |\n"),
               ("double_pipe_header", "|| id | decision ||\n|---|---|\n| A | ACCEPT |\n")]
        carrier(CAR, [c6row("A", 1)])
        stg_res = {}
        for nm_, tb_ in STG:
            for fp_, seat_, sc_ in ((S6, "sol", "8.6"), (O6, "opus", "8.4")):
                putb(fp_, r06_tab_review(seat_, sc_, tb_).encode("utf-8"))
            rc_v, out_v = tool("ingest.py", "claims", os.path.join(TMP, CAR), "--staged")
            stg_res[nm_] = (rc_v, acc_l(out_v))
        put(S6, r06_review("sol", "8.6", ADD6))
        put(O6, r06_review("opus", "8.4", ADD6))
        print("R06 parser staged:", {k_: (v_[0], v_[1].split(":")[-1].strip()[:30]) for k_, v_ in stg_res.items()})
        results.append(("R06FIX parser test staged: separators in the review FILE (U+2028, lone CR), a bare '---' line "
                        "after a row, an emphasized or double-pipe header: carrier acceptance REFUSED",
                        all(v_[0] != 0 and "REFUSED" in v_[1] for v_ in stg_res.values()) and len(stg_res) == 5))

finally:
    SB.__exit__(None, None, None)
for name, ok in results:
    print("PASS" if ok else "FAIL", name)
sys.exit(0 if results and all(ok for _, ok in results) else 1)
