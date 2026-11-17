"""test_cite_cwd.py — regression scenarios for the CI cite step (cwd and "did it really run" rules).

Background: step_cite used to run every citecheck.py with cwd = the script's own folder and accepted rc 0 or 1.
A citecheck that only works from the repository root (W3-RM2, W3-RM2-R) crashed with rc=1 and no MISS line, which
showed as "MISS 0 committed -> 0 now" = PASS. Now: cwd = repo root of the sandbox, rc must be 0/1, and rc=1 needs at
least one MISS/BAD/FAIL line.
Runs in a CI Sandbox (disposable detached worktree of HEAD); the fake citechecks are untracked files in it and are
removed by the sandbox reset after every run. The live tree is never touched.
Run: python Theory_work/INFRA/tools/test_cite_cwd.py   (exit code 1 if any scenario fails)"""
import os, sys, tempfile
sys.dont_write_bytecode = True  # never write __pycache__

LIVE_INFRA = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(LIVE_INFRA, "ci"))
sys.argv = sys.argv[:1]
import shlex  # noqa: E402
# the fake scripts must run with THIS interpreter whatever config.tsv says (it names the Windows launcher `py`)
os.environ["BVS_NUMERICS_PY"] = " ".join(shlex.quote(x) for x in [sys.executable])
import run_ci  # noqa: E402

results = []
SB = run_ci.Sandbox()
SB.__enter__()
LOG = tempfile.mkdtemp(prefix="cite-cwd-test-")
try:
    def put(rel, text):
        p = os.path.join(SB.path, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)

    FILES = {}  # every run_in ends with sb.reset() (git clean), which deletes the untracked fakes: re-create per run

    def put_f(rel, text):
        FILES[rel] = text

    def cite(rel, committed=None):
        """Run run_ci.cite_one on a fake ticket script (optionally with a committed CITECHECK.txt next to it)."""
        for r, t in FILES.items():
            put(r, t)
        if committed is not None:
            put(os.path.join(os.path.dirname(rel), "CITECHECK.txt"), committed)
        return run_ci.cite_one(SB, rel, LOG)

    T = "Theory_work/WaveT/T"
    # (a) exits 1 without any output (what a crash-before-printing / "did not really run" looks like)
    put_f(T + "A/citecheck.py", "import sys\nsys.exit(1)\n")
    good, line = cite(T + "A/citecheck.py")
    results.append(("(a) citecheck exiting rc=1 with no output -> FAIL", not good and "rc=1" in line and "did not run" in line))
    # (a') crashes with a traceback (rc=1), and rc=2 -> FAIL
    put_f(T + "A2/citecheck.py", "open('does/not/exist.md')\n")
    good, line = cite(T + "A2/citecheck.py")
    results.append(("(a') crash with a traceback (rc=1, no MISS line) -> FAIL", not good))
    put_f(T + "A3/citecheck.py", "import sys\nprint('OK  x:1-2')\nsys.exit(2)\n")
    good, line = cite(T + "A3/citecheck.py")
    results.append(("(a'') rc=2 -> FAIL even with output", not good and "rc=2" in line))

    # (b) a citecheck that needs the repository root (ROOT = os.getcwd(), repo-relative paths): runs and counts MISS
    put_f(T + "B/doc.md", "line 1\nline 2\nline 3\n")
    root_cc = ("import os, sys\nROOT = os.getcwd()\n"
               "n = len(open('Theory_work/WaveT/TB/doc.md', encoding='utf-8').read().split('\\n')) - 1\n"
               "miss = 0\nfor a in (1, 3, 9):\n"
               "    if a > n:\n        print('MISS  doc.md:%d  (file has %d lines)' % (a, n)); miss += 1\n"
               "    else:\n        print('OK    doc.md:%d' % a)\n"
               "print('checked 3; %d MISS' % miss)\nsys.exit(1 if miss else 0)\n")
    put_f(T + "B/citecheck.py", root_cc)
    good, line = cite(T + "B/citecheck.py")
    results.append(("(b) root-only citecheck runs (no crash) and its MISS is counted: 'MISS 0 committed -> 1 now (rc=1)'",
                    not good and "MISS 0 committed -> 1 now (rc=1)" in line and "did not run" not in line))
    good, line = cite(T + "B/citecheck.py", committed="MISS  doc.md:9\n")  # committed baseline already has that MISS
    results.append(("(b') same script, committed baseline with 1 MISS -> PASS (no new miss)",
                    good and "MISS 1 committed -> 1 now (rc=1)" in line))

    # (c) a normal citecheck (own-folder resolution via __file__, rc 0, prints OK lines) -> unchanged PASS
    put_f(T + "C/doc.md", "a\nb\n")
    put_f(T + "C/citecheck.py", "import os\nHERE = os.path.dirname(os.path.abspath(__file__))\n"
        "n = len(open(os.path.join(HERE, 'doc.md')).read().split('\\n')) - 1\nprint('OK    doc.md:1-%d' % n)\n")
    good, line = cite(T + "C/citecheck.py")
    results.append(("(c) normal __file__-relative citecheck, rc=0 -> PASS 'MISS 0 committed -> 0 now (rc=0)'",
                    good and "MISS 0 committed -> 0 now (rc=0)" in line))
    # (c') a normal citecheck with a real MISS and rc=1 -> FAIL as before (a > committed); equal to committed -> PASS
    put_f(T + "D/citecheck.py", "import sys\nprint('MISS  x.md:5')\nsys.exit(1)\n")
    good, line = cite(T + "D/citecheck.py")
    good2, line2 = cite(T + "D/citecheck.py", committed="MISS  x.md:5\n")
    results.append(("(c') ordinary rc=1 with 1 MISS: FAIL vs empty baseline, PASS vs baseline with 1 MISS",
                    not good and "MISS 0 committed -> 1 now" in line and good2))

    # miss_count / cite_verdict units
    results.append(("miss_count counts MISS/BAD/FAIL and TOKEN-MISS lines, not OK or prose",
                    run_ci.miss_count("OK a\nMISS b\n  BAD c\nFAIL (missing file) d\nTOKEN-MISS  e\n5 citations, 0 MISS\n") == 4))
    results.append(("cite_verdict: rc TIMEOUT / REFUSED / 127 -> FAIL; rc=0 with fewer misses than committed -> PASS",
                    not any(run_ci.cite_verdict(rc, "", "")[0] for rc in ("TIMEOUT", "REFUSED (x)", 127, 2))
                    and run_ci.cite_verdict(0, "MISS a\nMISS b\n", "MISS a\n")[0]))

    # falsify path unchanged: run_in default cwd is the script's own folder; at_root=True gives the repo root
    put_f(T + "E/pwd.py", "import os\nprint('CWD=' + os.getcwd())\n")
    put(T + "E/pwd.py", FILES[T + "E/pwd.py"])
    _, _, txt, _ = run_ci.run_in(SB, T + "E/pwd.py", [], 60, LOG)
    put(T + "E/pwd.py", FILES[T + "E/pwd.py"])
    _, _, txt_r, _ = run_ci.run_in(SB, T + "E/pwd.py", [], 60, LOG, at_root=True)
    results.append(("run_in default cwd = script folder (falsify unchanged); at_root=True -> sandbox root",
                    txt.strip() == "CWD=" + os.path.realpath(os.path.join(SB.path, "Theory_work/WaveT/TE")) and
                    txt_r.strip() == "CWD=" + os.path.realpath(SB.path)))
finally:
    import shutil
    shutil.rmtree(LOG, ignore_errors=True)
    SB.__exit__(None, None, None)
for name, ok in results:
    print("PASS" if ok else "FAIL", name)
sys.exit(0 if results and all(ok for _, ok in results) else 1)
