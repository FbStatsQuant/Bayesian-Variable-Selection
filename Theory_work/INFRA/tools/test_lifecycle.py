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
                        and any(e_["id"] == "R03:W2" and e_["after"].startswith(f"v{st('R03:W2')['version']} fp:")
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

finally:
    SB.__exit__(None, None, None)
for name, ok in results:
    print("PASS" if ok else "FAIL", name)
sys.exit(0 if results and all(ok for _, ok in results) else 1)
