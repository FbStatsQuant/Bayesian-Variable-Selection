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
import p1m_cost  # noqa: E402
import p1m_driver  # noqa: E402
import p1m_manifest  # noqa: E402

EXAMPLE = os.path.join(HERE, "examples", "plan_A2_pilot_1e4.json")


def load_example():
    with open(EXAMPLE) as fh:
        return json.load(fh)


class Base(unittest.TestCase):
    def setUp(self):
        root = os.environ.get("TMPDIR") or tempfile.gettempdir()
        self.tmp = tempfile.mkdtemp(prefix="p1m_driver_", dir=root)
        os.environ["P1M_DRIVER_TEST"] = "1"

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
        os.environ.pop("P1M_DRIVER_TEST")
        rc, _ = self.gen(load_example(), dept="/tmp/elsewhere")
        self.assertEqual(rc, 64)


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
            self.assertIn("#SBATCH --output=%s/scratch/slurm_out/" % dept, txt)
            self.assertIn("export TMPDIR=$DEPT/scratch/tmp/${SLURM_JOB_ID}", txt)
            code = [l for l in txt.splitlines() if not l.lstrip().startswith("#")]
            self.assertFalse(any(re.search(r"(^|[;&|(]|\$\()\s*(sbatch|scancel|scontrol)\s", l) for l in code))   # never submit
            self.assertNotIn("/tmp/", txt.replace("scratch/tmp/", ""))
        self.assertEqual(subprocess.call(["bash", "-n", os.path.join(out, "submit.sh")]), 0)
        self.assertEqual(subprocess.call(["sha256sum", "--quiet", "-c", "SHA256SUMS"], cwd=out), 0)
        m = json.load(open(os.path.join(out, "manifests", "A2_ARs_n200_r1", "merge.json")))
        self.assertEqual(m["schema"], "smcbvs4.manifest/1")
        self.assertEqual(len([k for k in m["inputs"] if k.startswith("island_")]), 16)
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
        env = dict(os.environ, PATH=fbin + os.pathsep + os.environ["PATH"], P1M_DEPT=fake_dept)
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
# stub smcbvs4: writes <out>.bin and <out>.json {status, outputs} for any command; checks the manifest inputs exist
cmd=$1; shift; out=""; man=""
while [[ $# -gt 0 ]]; do case $1 in --out) out=$2; shift 2;; --manifest) man=$2; shift 2;; *) shift;; esac; done
if [[ -n $man ]]; then python3 -c "import json,sys; m=json.load(open('$man')); assert all(not str(v).startswith('@') for v in m['inputs'].values()), m['inputs']" || exit 13; fi
echo "$cmd" > "$out.bin"
[[ $cmd == gen ]] && echo '{}' > "$(dirname $out)/truth.json"
printf '{"status":"completed","outputs":{"%s.bin":"h_%s_%s"}}\n' "$(basename $out)" "$cmd" "$(basename $out)" > "$out.json"
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
        mm = json.load(open(os.path.join(rd, "manifests", "merge.json")))
        self.assertEqual(mm["inputs"]["island_2.bin"], "h_island_island_2")
        self.assertEqual(mm["inputs"]["calib.bin"], "h_calibrate_calib")
        self.assertEqual(mm["machine"]["slurm_job_id"], "77")
        self.assertEqual(mm["params"]["threads"], 2)
        im = json.load(open(os.path.join(rd, "manifests", "island_3.json")))
        self.assertEqual(im["params"]["island"], 3)
        self.assertTrue(os.path.exists(os.path.join(rd, "run_manifest.json")))
        self.assertTrue(os.path.exists(os.path.join(rd, "eval.json")) and os.path.exists(os.path.join(rd, "law.json")))
        ends = open(os.path.join(dept, "scratch", "runs", "A2_pilot", "ends.jsonl")).read().splitlines()
        self.assertEqual(len(ends), 1 + 1 + 3 + 1 + 1)
        self.assertEqual(os.listdir(os.path.join(dept, "scratch", "tmp")), [])   # TMPDIR removed on exit


class TestManifest(Base):
    def test_refuses_incomplete_input(self):
        rd = os.path.join(self.tmp, "run"); os.makedirs(rd)
        t = os.path.join(self.tmp, "t.json")
        json.dump({"inputs": {"data.bin": "@from:data.json"}, "params": {}}, open(t, "w"))
        json.dump({"status": "invalid_input", "outputs": {}}, open(os.path.join(rd, "data.json"), "w"))
        with self.assertRaises(SystemExit):
            p1m_manifest.main(["fill", "--template", t, "--run-dir", rd, "--out", os.path.join(self.tmp, "m.json")])
        json.dump({"status": "completed", "outputs": {"/x/y/data.bin": "abc"}}, open(os.path.join(rd, "data.json"), "w"))
        p1m_manifest.main(["fill", "--template", t, "--run-dir", rd, "--out", os.path.join(self.tmp, "m.json")])
        self.assertEqual(json.load(open(os.path.join(self.tmp, "m.json")))["inputs"]["data.bin"], "abc")


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
