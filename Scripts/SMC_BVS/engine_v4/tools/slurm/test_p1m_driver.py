#!/usr/bin/env python3
"""Tests of the dry-run Slurm driver, the manifest filler and the cost tool. Stdlib unittest; everything under $TMPDIR.

No real job is ever submitted: the submission test puts a FAKE `sbatch` (a shell script that only records its
arguments and prints an id) first on PATH, and the local chain test runs the stage scripts with a stub binary.
"""
import copy
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import p1m_cells  # noqa: E402
import p1m_cost  # noqa: E402
import p1m_driver  # noqa: E402
import p1m_manifest  # noqa: E402
import p1m_stage_cost  # noqa: E402

EXAMPLE = os.path.join(HERE, "examples", "plan_A2_pilot_1e4.json")


def load_example():
    with open(EXAMPLE) as fh:
        return json.load(fh)


class Base(unittest.TestCase):
    def setUp(self):
        root = os.environ.get("TMPDIR") or tempfile.gettempdir()
        self.tmp = tempfile.mkdtemp(prefix="p1m_driver_", dir=root)
        os.environ["P1M_TEST_ROOT"] = self.tmp   # inside $TMPDIR (path_allowed)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def gen(self, plan, dept=None, name="out"):
        pp = os.path.join(self.tmp, name + "_plan.json")
        with open(pp, "w") as fh:
            json.dump(plan, fh)
        out = os.path.join(self.tmp, name)
        args = ["--plan", pp, "--out", out, "--now", "2026-11-15T23:00:00Z"]
        if dept:
            args += ["--dept", dept]
        return p1m_driver.main(args), out


class TestResolve(Base):
    def test_worst_case_and_tasks(self):
        P = p1m_driver.resolve(load_example())
        # 1e4 defaults: setup 8×20m, calibrate 16×45m, islands 16×(16×15m), merge 8×15m, eval 4×20m per fit
        per_fit = 8 * (20 / 60) + 16 * 0.75 + 16 * 16 * 0.25 + 8 * 0.25 + 4 * (20 / 60)
        self.assertAlmostEqual(P["worst_case_core_h"], round(2 * per_fit, 1))
        self.assertEqual(P["n_tasks"], 2 * (4 + 16))

    def test_limits(self):
        pl = load_example()
        pl["fits"] = [dict(pl["fits"][0], run_id="f%d" % i) for i in range(8)]   # 8 × 20 = 160 tasks > 150
        with self.assertRaisesRegex(p1m_driver.PlanError, "150-task cap"):
            p1m_driver.resolve(pl)
        pl = load_example(); pl["resources"] = {"islands": {"time": "03:00:00"}}
        with self.assertRaisesRegex(p1m_driver.PlanError, "max_task_hours"):
            p1m_driver.resolve(pl)
        pl = load_example(); pl["max_task_hours"] = 30; pl["resources"] = {"islands": {"time": "1-01:00:00"}}
        with self.assertRaisesRegex(p1m_driver.PlanError, "QOS wall"):
            p1m_driver.resolve(pl)
        pl = load_example(); pl["fits"][0]["seed"] = 0
        with self.assertRaisesRegex(p1m_driver.PlanError, "seed"):
            p1m_driver.resolve(pl)
        pl = load_example(); pl["core_h_cap"] = 10
        with self.assertRaisesRegex(p1m_driver.PlanError, "core_h_cap"):
            p1m_driver.resolve(pl)
        pl = load_example(); pl["fits"][1]["run_id"] = pl["fits"][0]["run_id"]
        with self.assertRaisesRegex(p1m_driver.PlanError, "duplicate"):
            p1m_driver.resolve(pl)
        pl = load_example(); pl["fits"][0]["run_id"] = "../evil"
        with self.assertRaises(p1m_driver.PlanError):
            p1m_driver.resolve(pl)

    def test_mixed_rungs_rejected_at_generation(self):
        pl = load_example(); pl["fits"][1]["p"] = 100000
        rc, _ = self.gen(pl)
        self.assertEqual(rc, 65)

    def test_dept_guard(self):
        os.environ.pop("P1M_TEST_ROOT")
        for bad in ("/tmp/elsewhere", p1m_driver.DEPT_DEFAULT + "_x", p1m_driver.DEPT_DEFAULT + "/../elsewhere"):
            rc, _ = self.gen(load_example(), dept=bad)
            self.assertEqual(rc, 64, bad)
        # --out outside the department folder (and no test root) is refused too
        pp = os.path.join(self.tmp, "plan.json"); json.dump(load_example(), open(pp, "w"))
        self.assertEqual(p1m_driver.main(["--plan", pp, "--out", "/tmp/p1m_out_elsewhere"]), 64)
        # a test root outside $TMPDIR does not open the gate
        os.environ["P1M_TEST_ROOT"] = "/tmp"
        self.assertFalse(p1m_driver.path_allowed("/tmp/x"))


class TestGenerate(Base):
    def test_files_and_rules(self):
        rc, out = self.gen(load_example())
        self.assertEqual(rc, 0)
        dept = p1m_driver.DEPT_DEFAULT
        for st in p1m_driver.STAGES:
            path = os.path.join(out, "stage_%s.sbatch" % st)
            txt = open(path).read()
            self.assertEqual(subprocess.call(["bash", "-n", path]), 0, path)
            self.assertIn("#SBATCH --constraint=sapphirerapids", txt)
            self.assertIn("#SBATCH --qos=nots_commons", txt)
            self.assertIn("#SBATCH --kill-on-invalid-dep=yes", txt)
            self.assertIn("#SBATCH --output=%s/scratch/slurm_out/" % dept, txt)
            self.assertIn("export TMPDIR=$DEPT/scratch/tmp/${SLURM_JOB_ID}", txt)
            code = [l for l in txt.splitlines() if not l.lstrip().startswith("#")]
            self.assertFalse(any(re.search(r"(^|[;&|(]|\$\()\s*(sbatch|scancel|scontrol)\s", l) for l in code))   # never submit
            self.assertNotIn("/tmp/", txt.replace("scratch/tmp/", ""))
        self.assertEqual(subprocess.call(["bash", "-n", os.path.join(out, "submit.sh")]), 0)
        self.assertEqual(subprocess.call(["sha256sum", "--quiet", "-c", "SHA256SUMS"], cwd=out), 0)
        m = json.load(open(os.path.join(out, "manifests", "A2_ARs_n200_r1", "merge.json")))
        self.assertEqual(m["schema"], "smcbvs4.manifest/1")
        self.assertEqual(len([k for k in m["inputs"] if os.path.basename(k).startswith("island_")]), 16)
        rm = json.load(open(os.path.join(out, "run_manifests", "A2_ARs_n200_r2.json")))
        self.assertEqual(rm["params"]["data_seed"], 20261202)
        row = open(os.path.join(out, "ledger_row.md")).read()
        self.assertIn("A2_pilot", row)
        self.assertIn("%.1f" % p1m_driver.resolve(load_example())["worst_case_core_h"], row)

    def test_deterministic(self):
        _, a = self.gen(load_example(), name="a")
        _, b = self.gen(load_example(), name="b")
        self.assertEqual(open(os.path.join(a, "SHA256SUMS")).read(), open(os.path.join(b, "SHA256SUMS")).read())


class TestFakeSubmission(Base):
    """submit.sh against a FAKE sbatch (records arguments only): checks the dependency graph and the job count."""

    def test_graph(self):
        fake_dept = os.path.join(self.tmp, "dept")
        rc, out = self.gen(load_example())
        self.assertEqual(rc, 0)
        scr = os.path.join(fake_dept, "scripts", "A2_pilot")
        shutil.copytree(out, scr)
        os.makedirs(os.path.join(scr, "bin"))
        with open(os.path.join(scr, "bin", "smcbvs4"), "w") as fh:
            fh.write("#!/bin/sh\nexit 0\n")
        os.chmod(os.path.join(scr, "bin", "smcbvs4"), 0o755)
        for d in ("scratch/slurm_out", "scratch/tmp"):
            os.makedirs(os.path.join(fake_dept, d))
        fbin = os.path.join(self.tmp, "fakebin")
        os.makedirs(fbin)
        calls = os.path.join(self.tmp, "sbatch_calls.txt")
        with open(os.path.join(fbin, "sbatch"), "w") as fh:
            fh.write("#!/bin/bash\nn=$(( $(wc -l < %s 2>/dev/null || echo 0) + 1000 ))\necho \"$n $*\" >> %s\necho $n\n" % (calls, calls))
        os.chmod(os.path.join(fbin, "sbatch"), 0o755)
        # PR12 MINOR-9: the stub is passed by absolute path (SBATCH) and the PATH holds no other sbatch
        safe_path = os.pathsep.join([fbin, "/usr/bin", "/bin"])
        fake = os.path.join(fbin, "sbatch")
        self.assertEqual(shutil.which("sbatch", path=safe_path), fake)
        env = dict(os.environ, PATH=safe_path, SBATCH=fake, P1M_DEPT=fake_dept, P1M_TEST_ROOT=self.tmp)
        # without CONFIRM it refuses
        self.assertEqual(subprocess.call(["bash", os.path.join(scr, "submit.sh")], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL), 64)
        self.assertFalse(os.path.exists(calls))
        env["CONFIRM"] = "yes"
        self.assertEqual(subprocess.call(["bash", os.path.join(scr, "submit.sh")], env=env, stdout=subprocess.DEVNULL), 0)
        lines = [l.split() for l in open(calls).read().splitlines()]
        self.assertEqual(len(lines), 2 + 3 * 2)
        ids = {i: l for i, l in enumerate(lines)}
        self.assertIn("--array=1-2", ids[0]); self.assertIn("stage_setup.sbatch", ids[0])
        self.assertIn("--dependency=aftercorr:1000", ids[1]); self.assertIn("stage_calibrate.sbatch", ids[1])
        # fit 1: islands afterok on calibrate task 1; merge on islands; eval on merge
        self.assertIn("--array=1-16%16", ids[2]); self.assertIn("--dependency=afterok:1001_1", ids[2]); self.assertEqual(ids[2][-1], "1")
        self.assertIn("--dependency=afterok:1002", ids[3]); self.assertIn("stage_merge.sbatch", ids[3])
        self.assertIn("--dependency=afterok:1003", ids[4]); self.assertIn("stage_eval.sbatch", ids[4])
        self.assertIn("--dependency=afterok:1001_2", ids[5]); self.assertEqual(ids[5][-1], "2")
        subs = [json.loads(l) for l in open(os.path.join(fake_dept, "scratch", "runs", "A2_pilot", "submissions.jsonl"))]
        self.assertEqual([s["stage"] for s in subs], ["setup", "calibrate", "islands", "merge", "eval", "islands", "merge", "eval"])
        # a tampered script is refused
        with open(os.path.join(scr, "stage_merge.sbatch"), "a") as fh:
            fh.write("# tamper\n")
        self.assertEqual(subprocess.call(["bash", os.path.join(scr, "submit.sh")], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL), 66)


STUB = r"""#!/bin/bash
# stub smcbvs4: writes an empty valid container at --out and the record <out>.json; with --manifest, checks that every
# input is a path whose content hash matches (as WP1's main does)
cmd=$1; shift; out=""; man=""; truth=""
while [[ $# -gt 0 ]]; do case $1 in --out) out=$2; shift 2;; --manifest) man=$2; shift 2;; --truth) truth=$2; shift 2;; *) shift 2;; esac; done
if [[ $cmd == prep && -n ${STUB_PREP_RC:-} ]]; then printf '{"status":"completed","prep_status":"no_predictors","hpm":[]}' > "$out.json"; exit $STUB_PREP_RC; fi
python3 - "$out" "$man" "$cmd" <<'PY' || exit 13
import hashlib, json, struct, sys
out, man, cmd = sys.argv[1:4]
def chash(p):
    b = open(p, "rb").read(); ns = struct.unpack_from("<I", b, 20)[0]
    return hashlib.sha256(b[128:128 + 128 * ns]).hexdigest()
if man:
    m = json.load(open(man))
    for path, h in m["inputs"].items():
        assert chash(path) == h, (path, h)
tag = cmd.encode()[:32].ljust(32, b"\0")   # in `reserved` (v0.1.1-style file: content field zero)
hdr = b"SMCBVS4\0" + struct.pack("<IIIIQ", 1, 6, 3, 0, 128) + hashlib.sha256(b"").digest() + b"\0" * 32 + tag
open(out, "wb").write(hdr)
json.dump({"status": "completed", "command": cmd}, open(out + ".json", "w"))
PY
[[ -n $truth ]] && echo '{}' > "$truth"
exit 0
"""


class TestLocalChain(Base):
    """Runs every stage script in order on this machine with a stub binary and a fake department under $TMPDIR."""

    def test_chain(self):
        dept = os.path.join(self.tmp, "SMC_Engineering_Department")
        pl = load_example(); pl["fits"] = pl["fits"][:1]; pl["fits"][0]["Rp"] = 3
        rc, out = self.gen(pl, dept=dept)
        self.assertEqual(rc, 0)
        scr = os.path.join(dept, "scripts", "A2_pilot")
        shutil.copytree(out, scr)
        os.makedirs(os.path.join(scr, "bin"))
        with open(os.path.join(scr, "bin", "smcbvs4"), "w") as fh:
            fh.write(STUB)
        os.chmod(os.path.join(scr, "bin", "smcbvs4"), 0o755)
        with open(os.path.join(scr, "env.sh"), "w") as fh:   # no module system on Owls
            fh.write("true\n")
        for d in ("scratch/slurm_out", "scratch/tmp", "scratch/runs/A2_pilot"):
            os.makedirs(os.path.join(dept, d))
        base = dict(os.environ, SLURM_JOB_ID="77", SLURM_CPUS_PER_TASK="2")

        def run(stage, task=None, arg=None):
            env = dict(base)
            if task is not None:
                env["SLURM_ARRAY_TASK_ID"] = str(task)
            cmd = ["bash", os.path.join(scr, "stage_%s.sbatch" % stage)] + ([str(arg)] if arg else [])
            r = subprocess.run(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            self.assertEqual(r.returncode, 0, "%s: %s" % (stage, r.stderr))

        run("setup", task=1)
        run("calibrate", task=1)
        for r in (1, 2, 3):
            run("islands", task=r, arg=1)
        run("merge", arg=1)
        run("eval", arg=1)
        rd = os.path.join(dept, "scratch", "runs", "A2_pilot", "A2_ARs_n200_r1")
        em = json.load(open(os.path.join(rd, "manifests", "eval.json")))
        self.assertEqual(len(em["inputs"]), 2)
        self.assertEqual(em["params"]["truth_sha256"], p1m_manifest.sha256_file(os.path.join(rd, "truth.json")))
        self.assertTrue(os.path.exists(os.path.join(rd, "manifests", "post.json")))
        mm = json.load(open(os.path.join(rd, "manifests", "merge.json")))
        self.assertEqual(len(mm["inputs"]), 3 + 3)
        self.assertEqual(mm["inputs"][os.path.join(rd, "island_2.bin")], p1m_manifest.content_hash(os.path.join(rd, "island_2.bin")))
        gm = json.load(open(os.path.join(rd, "manifests", "gen.json")))
        self.assertEqual(gm["params"]["seed"], 20261201)   # gen takes the data seed
        self.assertEqual(mm["machine"]["slurm_job_id"], "77")
        self.assertEqual(mm["params"]["threads"], 2)
        im = json.load(open(os.path.join(rd, "manifests", "island_3.json")))
        self.assertEqual(im["params"]["id"], 3)
        self.assertTrue(os.path.exists(os.path.join(rd, "run_manifest.json")))
        self.assertTrue(os.path.exists(os.path.join(rd, "eval.bin.json")) and os.path.exists(os.path.join(rd, "law.bin.json")))
        ends = open(os.path.join(dept, "scratch", "runs", "A2_pilot", "ends.jsonl")).read().splitlines()
        self.assertEqual(len(ends), 1 + 1 + 3 + 1 + 1)
        self.assertEqual(os.listdir(os.path.join(dept, "scratch", "tmp")), [])   # TMPDIR removed on exit


class TestPilotBatch(Base):
    """WP7 O5: plan key "pilot" -> stage_pilot.sbatch + submit_pilot.sh (setup -> pilot only), its own worst case, the
    pilot binary in build.sh, island_isa in cmake, and calibrate's --cost-dir; the example plans resolve."""

    def plan(self):
        pl = load_example(); pl["fits"] = pl["fits"][:1]
        pl["pilot"] = {"cpus": 96, "mem": "64G", "time": "01:00:00"}
        pl["island_isa"] = "sapphirerapids"
        return pl

    def test_generate_and_submit(self):
        fake_dept = os.path.join(self.tmp, "dept")
        rc, out = self.gen(self.plan())
        self.assertEqual(rc, 0)
        P = json.load(open(os.path.join(out, "plan.resolved.json")))
        self.assertAlmostEqual(P["worst_case_pilot_core_h"], round(8 * (20 / 60) + 96 * 1.0, 1))   # setup 8 x 20 min + pilot
        build = open(os.path.join(out, "build.sh")).read()
        self.assertIn("-DV4_ISLAND_ISA=sapphirerapids", build)
        self.assertIn("make -C \"$B\" -j3 smcbvs4 v4_pilot_island", build)
        self.assertIn('--cost-dir "$RUN/cost"', open(os.path.join(out, "stage_calibrate.sbatch")).read())
        pil = open(os.path.join(out, "stage_pilot.sbatch")).read()
        self.assertIn("#SBATCH --cpus-per-task=96", pil); self.assertIn("#SBATCH --time=01:00:00", pil)
        self.assertIn('v4_pilot_island" --data "$RUN/data.bin" --setup "$RUN/setup.bin"', pil)
        sums = open(os.path.join(out, "SHA256SUMS")).read()
        self.assertIn("stage_pilot.sbatch", sums); self.assertIn("submit_pilot.sh", sums)
        scr = os.path.join(fake_dept, "scripts", "A2_pilot")
        shutil.copytree(out, scr)
        os.makedirs(os.path.join(scr, "bin"))
        for b in ("smcbvs4", "v4_pilot_island"):
            with open(os.path.join(scr, "bin", b), "w") as fh:
                fh.write("#!/bin/sh\nexit 0\n")
            os.chmod(os.path.join(scr, "bin", b), 0o755)
        for d in ("scratch/slurm_out", "scratch/tmp"):
            os.makedirs(os.path.join(fake_dept, d))
        fbin = os.path.join(self.tmp, "fakebin"); os.makedirs(fbin)
        calls = os.path.join(self.tmp, "sbatch_calls.txt")
        with open(os.path.join(fbin, "sbatch"), "w") as fh:
            fh.write("#!/bin/bash\nn=$(( $(wc -l < %s 2>/dev/null || echo 0) + 2000 ))\necho \"$n $*\" >> %s\necho $n\n" % (calls, calls))
        os.chmod(os.path.join(fbin, "sbatch"), 0o755)
        env = dict(os.environ, PATH=os.pathsep.join([fbin, "/usr/bin", "/bin"]), SBATCH=os.path.join(fbin, "sbatch"), P1M_DEPT=fake_dept,
                   P1M_TEST_ROOT=self.tmp)
        sp = os.path.join(scr, "submit_pilot.sh")
        self.assertEqual(subprocess.call(["bash", sp], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL), 64)   # no CONFIRM
        env["CONFIRM"] = "yes"
        self.assertEqual(subprocess.call(["bash", sp], env=env, stdout=subprocess.DEVNULL), 0)
        lines = [l.split() for l in open(calls).read().splitlines()]
        self.assertEqual(len(lines), 2)   # setup and pilot, nothing else
        self.assertIn("stage_setup.sbatch", lines[0])
        self.assertIn("stage_pilot.sbatch", lines[1]); self.assertIn("--dependency=aftercorr:2000", lines[1])
        os.remove(os.path.join(scr, "bin", "v4_pilot_island"))   # build.sh not run: refused
        self.assertEqual(subprocess.call(["bash", sp], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL), 66)

    def test_pilot_stage_runs(self):
        dept = os.path.join(self.tmp, "SMC_Engineering_Department")
        rc, out = self.gen(self.plan(), dept=dept)
        scr = os.path.join(dept, "scripts", "A2_pilot")
        shutil.copytree(out, scr); os.makedirs(os.path.join(scr, "bin"))
        args_log = os.path.join(self.tmp, "pilot_args.txt")
        with open(os.path.join(scr, "bin", "v4_pilot_island"), "w") as fh:
            fh.write("#!/bin/bash\necho \"$*\" > %s\nwhile [[ $# -gt 0 ]]; do [[ $1 == --out ]] && echo '{}' > \"$2\"; shift 2; done\n" % args_log)
        os.chmod(os.path.join(scr, "bin", "v4_pilot_island"), 0o755)
        with open(os.path.join(scr, "env.sh"), "w") as fh:
            fh.write("true\n")
        for d in ("scratch/slurm_out", "scratch/tmp", "scratch/runs/A2_pilot"):
            os.makedirs(os.path.join(dept, d))
        env = dict(os.environ, SLURM_JOB_ID="79", SLURM_CPUS_PER_TASK="2", SLURM_ARRAY_TASK_ID="1")
        r = subprocess.run(["bash", os.path.join(scr, "stage_pilot.sbatch")], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        a = open(args_log).read()
        self.assertIn("--seed 1 ", a)   # the fit's engine seed (example plan: seed 1)
        self.assertIn("--threads 2", a); self.assertIn("--with-ledger 1", a); self.assertIn("cost_pilot", a)

    def test_example_plans_resolve(self):
        t5 = p1m_driver.resolve(json.load(open(os.path.join(HERE, "examples", "plan_T5_1e5.json"))))
        self.assertLessEqual(t5["worst_case_core_h"], t5["core_h_cap"])
        self.assertEqual(t5["isa_check"], {"island": 1, "against": "x86-64-v3"})
        self.assertEqual(t5["island_isa"], "sapphirerapids")
        pp = p1m_driver.resolve(json.load(open(os.path.join(HERE, "examples", "plan_P7_pilot_1e6.json"))))
        self.assertEqual(pp["fits"][0]["run_id"], "6-AR-n200-r01-V-s1")
        self.assertLessEqual(pp["worst_case_pilot_core_h"], 150)

    def test_isa_check(self):   # D-32: SPR constraint everywhere, comparison build, island re-run after the island array, compare
        pl = self.plan(); pl["isa_check"] = {"island": 1}
        P = p1m_driver.resolve(pl)
        base = p1m_driver.resolve(self.plan())
        r = P["fits"][0]["resources"]["islands"]
        self.assertAlmostEqual(P["worst_case_core_h"], round(base["worst_case_core_h"] + int(r["cpus"]) * p1m_driver.hours(r["time"]), 1))
        self.assertEqual(P["n_tasks"], base["n_tasks"] + 1)
        fake_dept = os.path.join(self.tmp, "dept")
        rc, out = self.gen(pl)
        self.assertEqual(rc, 0)
        for fn in os.listdir(out):
            if fn.endswith(".sbatch"):
                self.assertIn("#SBATCH --constraint=sapphirerapids", open(os.path.join(out, fn)).read(), fn)
        build = open(os.path.join(out, "build.sh")).read()
        self.assertIn("-DV4_ISLAND_ISA=sapphirerapids", build)
        self.assertIn('cp "$BP/smcbvs4" "$SCR/bin/smcbvs4_isa_check"', build)
        self.assertIn("-DV4_ISLAND_ISA=x86-64-v3", build.split("BP=$SCR/build_isa_check")[1])   # default comparison: an FMA build
        q = self.plan(); q["isa_check"] = {"island": 1, "against": "portable"}
        rc2, out2 = self.gen(q, name="out_portable")
        self.assertNotIn("V4_ISLAND_ISA", open(os.path.join(out2, "build.sh")).read().split("BP=$SCR/build_isa_check")[1])
        isa = open(os.path.join(out, "stage_isa_check.sbatch")).read()
        self.assertIn('"$SCR/bin/smcbvs4_isa_check" island', isa); self.assertIn("p1m_stage_cost.py\" isa", isa)
        self.assertTrue(os.path.exists(os.path.join(out, "p1m_stage_cost.py")))
        scr = os.path.join(fake_dept, "scripts", "A2_pilot")
        shutil.copytree(out, scr); os.makedirs(os.path.join(scr, "bin"))
        for b in ("smcbvs4", "smcbvs4_isa_check"):
            with open(os.path.join(scr, "bin", b), "w") as fh:
                fh.write("#!/bin/sh\nexit 0\n")
            os.chmod(os.path.join(scr, "bin", b), 0o755)
        for d in ("scratch/slurm_out", "scratch/tmp"):
            os.makedirs(os.path.join(fake_dept, d))
        fbin = os.path.join(self.tmp, "fakebin"); os.makedirs(fbin)
        calls = os.path.join(self.tmp, "sbatch_calls.txt")
        with open(os.path.join(fbin, "sbatch"), "w") as fh:
            fh.write("#!/bin/bash\nn=$(( $(wc -l < %s 2>/dev/null || echo 0) + 3000 ))\necho \"$n $*\" >> %s\necho $n\n" % (calls, calls))
        os.chmod(os.path.join(fbin, "sbatch"), 0o755)
        env = dict(os.environ, PATH=os.pathsep.join([fbin, "/usr/bin", "/bin"]), SBATCH=os.path.join(fbin, "sbatch"), P1M_DEPT=fake_dept,
                   P1M_TEST_ROOT=self.tmp, CONFIRM="yes")
        self.assertEqual(subprocess.call(["bash", os.path.join(scr, "submit.sh")], env=env, stdout=subprocess.DEVNULL), 0)
        lines = [l.split() for l in open(calls).read().splitlines()]
        st = [next(a for a in l if a.endswith(".sbatch")) for l in lines]
        self.assertEqual(st, ["stage_setup.sbatch", "stage_calibrate.sbatch", "stage_islands.sbatch", "stage_isa_check.sbatch",
                              "stage_merge.sbatch", "stage_eval.sbatch"])
        self.assertIn("--dependency=afterok:3002", lines[3])   # after the island array
        self.assertIn("--dependency=afterok:3002", lines[4])   # merge does not wait for the check
        os.remove(os.path.join(scr, "bin", "smcbvs4_isa_check"))
        self.assertEqual(subprocess.call(["bash", os.path.join(scr, "submit.sh")], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL), 66)
        with self.assertRaises(p1m_driver.PlanError):   # isa_check without island_isa
            q = self.plan(); q["island_isa"] = ""; q["isa_check"] = {"island": 1}; p1m_driver.resolve(q)
        with self.assertRaises(p1m_driver.PlanError):   # island beyond Rp
            q = self.plan(); q["isa_check"] = {"island": 99}; p1m_driver.resolve(q)

    def test_compare_isa(self):
        def info(h, secs, isa):
            return {"meta": {"output_hash": h, "status": "completed", "binary": {"island_isa": isa}},
                    "sections": [{"name": "meta", "dtype": 9, "dims": [1], "sha256": isa}] + [{"name": n, "dtype": 1, "dims": [3], "sha256": x} for n, x in secs]}
        a = info("0x1", [("top_v", "aa"), ("pip_r", "bb")], "sapphirerapids")
        ok, d = p1m_stage_cost.compare_isa(a, info("0x1", [("top_v", "aa"), ("pip_r", "bb")], "portable"))
        self.assertTrue(ok); self.assertEqual(d["island_isa"], ["sapphirerapids", "portable"])
        ok, d = p1m_stage_cost.compare_isa(a, info("0x1", [("top_v", "aa"), ("pip_r", "bX")], "portable"))
        self.assertFalse(ok); self.assertEqual(d["differing_sections"], ["pip_r"])
        self.assertFalse(p1m_stage_cost.compare_isa(a, info("0x2", [("top_v", "aa"), ("pip_r", "bb")], "portable"))[0])

    def test_bad_pilot(self):
        for bad in ({"cpus": 96, "mem": "64G"}, {"cpus": 500, "mem": "64G", "time": "01:00:00"}, {"cpus": 96, "mem": "64G", "time": "03:00:00"}):
            pl = self.plan(); pl["pilot"] = bad
            with self.assertRaises(p1m_driver.PlanError):
                p1m_driver.resolve(pl)
        pl = self.plan(); pl["island_isa"] = "x; rm -rf /"
        with self.assertRaises(p1m_driver.PlanError):
            p1m_driver.resolve(pl)


class TestStageCost(Base):
    """WP7 O5: p1m_stage_cost.py reads D-30 cost records (JSON-lines with resumed segments; meta.cost columns) and sums
    them per stage kind; the T5 report collects a run directory."""

    def rows(self, seg, steps):
        out = []
        for st in steps:
            kind = 0 if st == 0 else (1 if st <= 3 else (2 if st == 4 else 3))
            out.append({"step": st, "kind": kind, "segment": seg, "phi": [0, .1, .5, 1, 1, 1][st], "wall": 1.0 + st, "particle_rounds": 0 if st == 0 else 10,
                        "sweeps": 0 if st == 0 else 40, "passes": 4, "act_cols": 40, "flips": 0 if st == 0 else 2000, "offers": 100 * st, "merges": 1,
                        "t_compact": .5, "t_check": 0.0, "t_ckpt": .1, "t_phaseA": .5, "t_phaseB": .1, "mean_S": 3.0 + st, "hwm_kb": 1048576 * st,
                        "M": 4.0, "flips_per_step": 2.0, "act_cols_per_pass": 10.0, "store_mean_k": 4.0})
        return out

    def test_segments_summary_and_t5(self):
        hdr = {"schema": "smcbvs4.cost/1", "m": 100, "threads": 2, "N": 10, "p": 98}
        p = os.path.join(self.tmp, "c.jsonl")
        with open(p, "w") as fh:   # segment 0 ran steps 0-3 (checkpoint after 2), segment 1 resumed at 3
            fh.write(json.dumps({"cost_header": dict(hdr, segment=0)}) + "\n")
            for r in self.rows(0, [0, 1, 2, 3]):
                fh.write(json.dumps(r) + "\n")
            fh.write(json.dumps({"cost_header": dict(hdr, segment=1)}) + "\n")
            for r in self.rows(1, [3, 4, 5]):
                fh.write(json.dumps(r) + "\n")
        with open(p, "a") as fh:   # the exit row (kind 4), with a field the kernel does not measure ("NaN")
            fh.write(json.dumps(dict(self.rows(1, [5])[0], step=6, kind=4, phi="NaN", particle_rounds=0, sweeps="NaN", wall=0.5)) + "\n")
        (h, rows), = p1m_stage_cost.load(p)
        self.assertEqual([r["step"] for r in rows], [0, 1, 2, 3, 4, 5, 6])
        self.assertTrue(rows[6]["sweeps"] != rows[6]["sweeps"])   # "NaN" -> float nan
        self.assertEqual(rows[3]["segment"], 1)   # the resumed segment's row wins
        s = p1m_stage_cost.summary(h, rows)
        self.assertEqual(s["bridge"]["steps"], 3)
        self.assertAlmostEqual(s["bridge"]["M"], 4.0)
        self.assertAlmostEqual(s["bridge"]["flips_per_step"], 2.0)   # 6000 flips / (30 rounds x m 100)
        self.assertAlmostEqual(s["bridge"]["ns_cpu_per_step"], 1e9 * (2 + 3 + 4) * 2 / (30 * 100))
        self.assertEqual(s["total"]["segments"], 2)
        self.assertEqual(s["exit"]["steps"], 1); self.assertAlmostEqual(s["total"]["wall_s"], sum(1.0 + st for st in range(6)) + 0.5)
        # meta.cost columns (island_r.bin via `smcbvs4 info --meta 1`)
        cols = {}
        for r in rows:
            for k, v in r.items():
                cols.setdefault(k, []).append(v)
        j = os.path.join(self.tmp, "isl.json")
        json.dump({"meta": {"cost": dict(hdr, rows=len(rows), columns=cols)}}, open(j, "w"))
        (h2, rows2), = p1m_stage_cost.load(j)
        self.assertEqual(json.dumps(rows2, sort_keys=True), json.dumps(rows, sort_keys=True))   # NaN != NaN: compare text
        # T5 report of a run directory: calibration records + stage records (no island files here)
        rd = os.path.join(self.tmp, "run"); os.makedirs(os.path.join(rd, "cost"))
        shutil.copy(p, os.path.join(rd, "cost", "cost_pilot_t0_k0_r0.jsonl"))
        json.dump({"status": "completed", "timings": {"tail_local_seconds": 3.0, "ls0_seconds": 4.0}}, open(os.path.join(rd, "fit.bin.json"), "w"))
        out = os.path.join(self.tmp, "t5.json")
        with open(os.devnull, "w") as dn:
            old = sys.stdout; sys.stdout = dn
            try:
                p1m_stage_cost.main(["t5", rd, "--json", out])
            finally:
                sys.stdout = old
        rep = json.load(open(out))
        self.assertEqual(rep["stages"]["fit"]["timings"]["ls0_seconds"], 4.0)
        self.assertIn("cost_pilot_t0_k0_r0.jsonl", rep["calibration"])


class TestPrepOutcome(TestLocalChain):
    """prep exit 20 (no_predictors): setup ends the pipeline cleanly, later stages exit 0, eval records the outcome."""

    def test_chain(self):
        os.environ["STUB_PREP_RC"] = "20"
        try:
            dept = os.path.join(self.tmp, "SMC_Engineering_Department")
            pl = load_example(); pl["fits"] = pl["fits"][:1]; pl["fits"][0]["Rp"] = 2
            rc, out = self.gen(pl, dept=dept)
            scr = os.path.join(dept, "scripts", "A2_pilot")
            shutil.copytree(out, scr); os.makedirs(os.path.join(scr, "bin"))
            with open(os.path.join(scr, "bin", "smcbvs4"), "w") as fh:
                fh.write(STUB)
            os.chmod(os.path.join(scr, "bin", "smcbvs4"), 0o755)
            with open(os.path.join(scr, "env.sh"), "w") as fh:
                fh.write("true\n")
            for d in ("scratch/slurm_out", "scratch/tmp", "scratch/runs/A2_pilot"):
                os.makedirs(os.path.join(dept, d))
            env = dict(os.environ, SLURM_JOB_ID="78", SLURM_CPUS_PER_TASK="2")
            for st, task, arg in (("setup", 1, None), ("calibrate", 1, None), ("islands", 1, 1), ("islands", 2, 1), ("merge", None, 1), ("eval", None, 1)):
                e = dict(env)
                if task is not None:
                    e["SLURM_ARRAY_TASK_ID"] = str(task)
                r = subprocess.run(["bash", os.path.join(scr, "stage_%s.sbatch" % st)] + ([str(arg)] if arg else []), env=e,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
                self.assertEqual(r.returncode, 0, "%s: %s" % (st, r.stderr))
            rd = os.path.join(dept, "scratch", "runs", "A2_pilot", "A2_ARs_n200_r1")
            self.assertEqual(open(os.path.join(rd, "OUTCOME")).read().strip(), "no_predictors")
            self.assertFalse(os.path.exists(os.path.join(rd, "setup.bin")))
            ev = json.load(open(os.path.join(rd, "eval.bin.json")))
            self.assertEqual(ev["fit_status"], "prep_no_predictors")
            self.assertEqual(ev["hpm"], [])
        finally:
            os.environ.pop("STUB_PREP_RC")


class TestManifest(Base):
    def test_refuses_incomplete_or_bad_input(self):
        import hashlib, struct
        rd = os.path.join(self.tmp, "run"); os.makedirs(rd)
        binp = os.path.join(rd, "data.bin")
        sec = b"x" * 128   # one fake section entry
        hdr = b"SMCBVS4\0" + struct.pack("<IIIIQ", 1, 2, 0, 1, 256) + hashlib.sha256(sec).digest() + b"\0" * 64
        open(binp, "wb").write(hdr + sec)
        t = os.path.join(self.tmp, "t.json")
        json.dump({"inputs": {binp: "@hash"}, "params": {}}, open(t, "w"))
        out = os.path.join(self.tmp, "m.json")
        with self.assertRaises(SystemExit):   # no producer record
            p1m_manifest.main(["fill", "--template", t, "--out", out])
        json.dump({"status": "invalid_input"}, open(binp + ".json", "w"))
        with self.assertRaises(SystemExit):   # producer failed
            p1m_manifest.main(["fill", "--template", t, "--out", out])
        json.dump({"status": "completed"}, open(binp + ".json", "w"))
        p1m_manifest.main(["fill", "--template", t, "--out", out])
        self.assertEqual(json.load(open(out))["inputs"][binp], hashlib.sha256(sec).hexdigest())
        open(binp, "r+b").write(b"SMCBVS4\0" + struct.pack("<IIIIQ", 1, 2, 0, 1, 256) + b"\1" * 32)   # corrupt table hash
        with self.assertRaises(SystemExit):
            p1m_manifest.main(["fill", "--template", t, "--out", out])


class TestContentHashV012(Base):
    def test_v012_header(self):
        import hashlib, struct
        sec = b"y" * 128
        th = hashlib.sha256(sec).digest()
        head = b"SMCBVS4\0" + struct.pack("<IIIIQ", 1, 2, 0, 1, 256)
        ch = hashlib.sha256(head + b"\0" * 64 + b"\0" * 32 + sec).digest()
        pth = os.path.join(self.tmp, "x.bin")
        open(pth, "wb").write(head + th + ch + b"\0" * 32 + sec)
        self.assertEqual(p1m_manifest.content_hash(pth), ch.hex())
        open(pth, "wb").write(head + th + b"\2" * 32 + b"\0" * 32 + sec)
        with self.assertRaises(SystemExit):
            p1m_manifest.content_hash(pth)


class TestCells(Base):
    """MANIFEST_CELLS generator: unique run ids, seeds in range, deterministic, every plan valid for the driver."""

    def test_expand_and_plans(self):
        rows = p1m_cells.expand()
        self.assertEqual(len({r["run_id"] for r in rows}), len(rows))
        self.assertTrue(all(1 <= r["seed"] <= 2 ** 31 - 1 for r in rows))
        self.assertEqual(rows, p1m_cells.expand())
        # OD-14: five 1M fits at n = 200 + the N = 10⁴ check; option D one fit at n = 1,000
        c6 = [r for r in rows if r["block"] == "rung 1e6"]
        self.assertEqual(len(c6), 5); self.assertEqual(sum(r["N"] == 5000 for r in c6), 1)   # H-9: AR-weak at 1M dropped; self-check N = 5,000
        self.assertEqual([r["n"] for r in rows if r["block"] == "option D"], [1000])
        # ADJ-OPP present at 10⁴ and 10⁵ (Sol F7)
        self.assertTrue(any(r["design"] == "ADJ-OPP" and r["p"] == 10 ** 5 for r in rows))
        out = os.path.join(self.tmp, "plans")
        written = p1m_cells.plans(rows, out)
        planned_ids = set()
        for f in written:
            P = p1m_driver.resolve(json.load(open(f)))
            self.assertLessEqual(P["n_tasks"], 150)
            planned_ids |= {x["run_id"] for x in json.load(open(f))["fits"]}
        # PR #19 MINOR-6: the fit count (TSV data rows) and the planned count (all but the 20 block-costed T8 rows)
        self.assertEqual(len(rows), 259)   # H-9 258 + the H-10 gated AR-weak 1M cell
        self.assertEqual(len(planned_ids), len(rows) - 20)
        self.assertEqual(len(written), 48)   # H-10: + the gated AR-weak 1M plan

    def test_precision_seeds_independent(self):
        """PR #19 MAJOR-1 (Sol F6): every precision arm has its own final and calibration seed, shared with no other fit."""
        rows = p1m_cells.expand()
        prec = [r for r in rows if r["block"] == "precision"]
        self.assertEqual(len(prec), 24)
        finals = [r["seed"] for r in prec]
        calibs = [json.loads(r["params"])["calib_seed"] for r in prec]
        self.assertEqual(len(set(finals)), 24); self.assertEqual(len(set(calibs)), 24)
        others = {(r["data_seed"], r["seed"]) for r in rows if r["block"] != "precision"}
        all_seeds = {r["seed"] for r in rows if r["block"] != "precision"} | {r["data_seed"] for r in rows}
        for r, c in zip(prec, calibs):
            self.assertNotIn((r["data_seed"], r["seed"]), others)
            self.assertNotIn(r["seed"], all_seeds); self.assertNotIn(c, all_seeds | set(finals))
        # the assert in expand() catches a shared precision key
        bad = [dict(r) for r in rows]
        p = [r for r in bad if r["block"] == "precision"]
        p[1]["seed"] = p[0]["seed"]
        with self.assertRaises(AssertionError):
            p1m_cells.check_seeds(bad)

    def test_a3_paired(self):
        """PR #19 MAJOR-2: every A3 fit has a default-partition V fit on the same data; an unpaired one is refused."""
        rows = p1m_cells.expand()
        a3 = [r for r in rows if "A3" in r["run_id"]]
        self.assertEqual(len(a3), 15)
        default = {r["data_seed"] for r in rows if r["mode"] == "V" and r["N"] == 2500 and r["Rp"] == 16
                   and r["seed"] == r["data_seed"] and "partition" not in json.loads(r["params"])}
        self.assertTrue(all(r["data_seed"] in default for r in a3))
        extra = dict(a3[-1]); extra["data_seed"] += 5; extra["seed"] += 5; extra["run_id"] = "4-BLK-n200-r10-A3-exactlink-s1"
        with self.assertRaises(AssertionError):
            p1m_cells.check_a3_pairing(rows + [extra])

    def test_seed_rule_limits(self):
        """PR #19 MINOR-5: the field widths are asserted (rep <= 99), so the seed rule stays one-to-one."""
        cells = p1m_cells.CELLS
        try:
            p1m_cells.CELLS = [("science 1e4", 4, "AR", 200, 100, p1m_cells.V1, "")]
            with self.assertRaises(AssertionError):
                p1m_cells.expand()
        finally:
            p1m_cells.CELLS = cells

    def test_only_rung(self):
        """PR #19 MINOR-7: --only takes a rung (4|5|6 or 1eK) or p."""
        self.assertEqual(p1m_cells.rung_to_p("5"), 10 ** 5)
        self.assertEqual(p1m_cells.rung_to_p("1e6"), 10 ** 6)
        self.assertEqual(p1m_cells.rung_to_p("10000"), 10 ** 4)
        rows = p1m_cells.expand()
        w = p1m_cells.plans(rows, os.path.join(self.tmp, "p5"), only="5")
        self.assertTrue(w and all(f["p"] == 10 ** 5 for x in w for f in json.load(open(x))["fits"]))


class TestCost(Base):
    def test_parse(self):
        sacct = "\n".join([
            "1000_1|p1m_A2_pilot_setup|COMPLETED|600|8|4800||n1|00:20:00",
            "1000_1.batch|batch|COMPLETED|600|8|4800|2048M|n1|",
            "1000_2|p1m_A2_pilot_setup|COMPLETED|660|8|5280||n2|00:20:00",
            "1000_2.batch|batch|COMPLETED|660|8|5280|1G|n2|",
            "1002_1|p1m_A2_pilot_islands|COMPLETED|1200|16|19200||n3|00:30:00",
            "1002_1.batch|batch|COMPLETED|1200|16|19200|3.5G|n3|",
            "1002_2|p1m_A2_pilot_islands|TIMEOUT|1800|16|28800||n4|00:30:00",
        ])
        sp = os.path.join(self.tmp, "sacct.txt"); open(sp, "w").write(sacct + "\n")
        subs = [{"stage": "setup", "fit": "all", "job": "1000"}, {"stage": "islands", "fit": "A", "job": "1002"},
                {"stage": "islands", "fit": "B", "job": "1005"}]
        su = os.path.join(self.tmp, "subs.jsonl"); open(su, "w").write("".join(json.dumps(s) + "\n" for s in subs))
        od = os.path.join(self.tmp, "cost")
        self.assertEqual(p1m_cost.main(["--sacct", sp, "--submissions", su, "--out-dir", od]), 0)
        a = json.load(open(os.path.join(od, "cost_A.json")))
        self.assertAlmostEqual(a["stages"]["setup"]["billed_core_h"], 4800 / 3600, places=4)
        self.assertAlmostEqual(a["stages"]["islands"]["billed_core_h"], (19200 + 28800) / 3600, places=4)
        self.assertEqual(a["stages"]["islands"]["max_rss_bytes"], int(3.5 * (1 << 30)))
        self.assertEqual(a["stages"]["islands"]["states"], ["COMPLETED", "TIMEOUT"])
        b = json.load(open(os.path.join(od, "cost_B.json")))
        self.assertAlmostEqual(b["stages"]["setup"]["billed_core_h"], 5280 / 3600, places=4)
        tot = json.load(open(os.path.join(od, "cost_batch.json")))
        self.assertAlmostEqual(tot["billed_core_h"], (4800 + 5280 + 19200 + 28800) / 3600, places=3)


if __name__ == "__main__":
    unittest.main(verbosity=2)
