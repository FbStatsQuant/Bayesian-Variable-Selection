#!/usr/bin/env python3
import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
import subprocess
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "runner"))
import launch
import retry
import accounting


class SchedulerTests(unittest.TestCase):
    def test_launch_guarded_and_sequential(self):
        with tempfile.TemporaryDirectory(dir=HERE) as tmp:
            root = Path(tmp); runner = root / "runner"; runner.mkdir()
            (runner / "freeze.json").write_text(json.dumps({"source_sha256":"a"*64}))
            resources = root / "resources.json"
            resources.write_text((HERE.parent / "runner" / "resources.json").read_text())
            run = "20261030T0000Z_bench_f3v2_prod"
            logs = root / "logs"
            calls = []
            live = [False]
            def path_map(x):
                return logs if x == "/scratch/fb31/New_Campaign/logs" else Path(x)
            def fake(cmd, **kwargs):
                calls.append(cmd)
                if cmd[0] == "bash":
                    (logs / run).mkdir(parents=True, exist_ok=True)
                    return SimpleNamespace(stdout="GATE_OK\n", stderr="", returncode=0)
                if cmd[0] == "squeue":
                    if "-r" in cmd and live[0]:
                        return SimpleNamespace(stdout="101_1\n", stderr="", returncode=0)
                    return SimpleNamespace(stdout="", stderr="", returncode=0)
                if cmd[0] == "sacct":
                    job = cmd[cmd.index("-j")+1]
                    cell = launch.CELLS[int(job)-101][0]
                    rows = [r for r in launch.units("prod") if f"p{r[1]:04d}_{r[4]}" == cell]
                    return SimpleNamespace(stdout="".join(f"{job}_{r[0]}|COMPLETED\n" for r in rows), stderr="", returncode=0)
                return SimpleNamespace(stdout=str(100 + sum(c[0] == "sbatch" for c in calls)), stderr="", returncode=0)
            argv = ["launch.py", "prod", run, "--resources", str(resources)]
            with patch.object(launch, "__file__", str(runner / "launch.py")), patch.object(launch, "Path", side_effect=path_map), patch.object(launch.subprocess, "run", side_effect=fake), patch.object(sys, "argv", argv), contextlib.redirect_stdout(io.StringIO()):
                launch.main()
                live[0] = True
                with self.assertRaises(ValueError): launch.main()
                live[0] = False
                for _ in range(3): launch.main()
                launch.main()
            sbatches = [c for c in calls if c[0] == "sbatch"]
            self.assertEqual(len(sbatches), 4)
            self.assertEqual(sum(c[0] == "bash" for c in calls), 6)
            self.assertTrue(all("--array=" in " ".join(c) and "%30" in " ".join(c) for c in sbatches))
            self.assertEqual(len((logs / run / "jobs.tsv").read_text().splitlines()), 5)

    def test_sacct_timeout_only_retry_once(self):
        with tempfile.TemporaryDirectory(dir=HERE) as tmp:
            root = Path(tmp); runner = root / "runner"; runner.mkdir()
            (runner / "freeze.json").write_text(json.dumps({"source_sha256":"a"*64}))
            run = "20261030T0000Z_bench_f3v2_dev"
            logs = root / "logs" / run; logs.mkdir(parents=True)
            (logs / "jobs.tsv").write_text("cell\tjob_id\tminutes\tmem_gib\tcommand\ndev\t42\t75\t4\tprimary\n")
            states = ["TIMEOUT", "FAILED", "OUT_OF_MEMORY"] + ["COMPLETED"]*23
            raw = "".join(f"42_{i}|{state}\n" for i, state in enumerate(states, 1))
            calls = []
            syncs = []
            def path_map(x):
                return root if x == "/scratch/fb31/New_Campaign" else Path(x)
            def fake(cmd, **kwargs):
                calls.append(cmd)
                if cmd[0] == "sacct": return SimpleNamespace(stdout=raw, stderr="", returncode=0)
                if cmd[0] == "bash": return SimpleNamespace(stdout="GATE_OK\n", stderr="", returncode=0)
                if cmd[0] == "squeue": return SimpleNamespace(stdout="", stderr="", returncode=0)
                if cmd[0] == "sbatch":
                    self.assertGreaterEqual(len(syncs), 1, "sbatch preceded durable claim")
                    return SimpleNamespace(stdout="43\n", stderr="", returncode=0)
                raise AssertionError(cmd)
            argv = ["retry.py", "dev", run]
            with patch.object(retry, "__file__", str(runner / "retry.py")), patch.object(retry, "Path", side_effect=path_map), patch.object(retry.subprocess, "run", side_effect=fake), patch.object(retry.os, "fsync", side_effect=lambda fd: syncs.append(fd)), patch.object(sys, "argv", argv), contextlib.redirect_stdout(io.StringIO()):
                retry.main()
                with self.assertRaises(ValueError):
                    retry.main()
            submissions = [c for c in calls if c[0] == "sbatch"]
            self.assertEqual(len(submissions), 1)
            self.assertIn("--array=1%13", submissions[0])
            self.assertIn("--time=150", submissions[0])
            self.assertIn("job_id=43", (logs / "retry_dev.intent").read_text())
            self.assertGreaterEqual(len(syncs), 2, "accepted job id was not synced")

    def test_accepted_then_sbatch_client_dies_blocks_relaunch(self):
        with tempfile.TemporaryDirectory(dir=HERE) as tmp:
            root = Path(tmp); runner = root / "runner"; runner.mkdir()
            (runner / "freeze.json").write_text(json.dumps({"source_sha256":"a"*64}))
            resources = root / "resources.json"
            resources.write_text((HERE.parent / "runner" / "resources.json").read_text())
            run = "20261030T0000Z_bench_f3v2_dev"; logs = root / "logs"; accepted = []
            def path_map(x): return logs if x == "/scratch/fb31/New_Campaign/logs" else Path(x)
            def fake(cmd, **kwargs):
                if cmd[0] == "bash":
                    (logs / run).mkdir(parents=True, exist_ok=True)
                    return SimpleNamespace(stdout="GATE_OK\n", stderr="", returncode=0)
                if cmd[0] == "squeue": return SimpleNamespace(stdout="", stderr="", returncode=0)
                if cmd[0] == "sbatch":
                    accepted.append("43")
                    raise subprocess.CalledProcessError(143, cmd)
                raise AssertionError(cmd)
            argv = ["launch.py", "dev", run, "--resources", str(resources)]
            with patch.object(launch, "__file__", str(runner / "launch.py")), patch.object(launch, "Path", side_effect=path_map), patch.object(launch.subprocess, "run", side_effect=fake), patch.object(sys, "argv", argv), contextlib.redirect_stdout(io.StringIO()):
                with self.assertRaises(subprocess.CalledProcessError): launch.main()
                with self.assertRaises(ValueError): launch.main()
            self.assertEqual(accepted, ["43"])
            self.assertTrue((logs / run / "primary_dev.intent").exists())
            self.assertIn("client_status=143", (logs / run / "primary_dev.sbatch_error.txt").read_text())

    def test_retry_durable_claim_survives_client_error(self):
        with tempfile.TemporaryDirectory(dir=HERE) as tmp:
            root = Path(tmp); runner = root / "runner"; runner.mkdir()
            (runner / "freeze.json").write_text(json.dumps({"source_sha256":"a"*64}))
            run = "20261030T0000Z_bench_f3v2_dev"; logs = root / "logs" / run; logs.mkdir(parents=True)
            (logs / "jobs.tsv").write_text("cell\tjob_id\tminutes\tmem_gib\tcommand\ndev\t42\t75\t4\tprimary\n")
            raw = "".join(f"42_{i}|{'TIMEOUT' if i == 1 else 'COMPLETED'}\n" for i in range(1,27))
            syncs = []; submissions = []
            def path_map(x): return root if x == "/scratch/fb31/New_Campaign" else Path(x)
            def fake(cmd, **kwargs):
                if cmd[0] == "sacct": return SimpleNamespace(stdout=raw,stderr="",returncode=0)
                if cmd[0] == "squeue": return SimpleNamespace(stdout="",stderr="",returncode=0)
                if cmd[0] == "bash": return SimpleNamespace(stdout="GATE_OK",stderr="",returncode=0)
                if cmd[0] == "sbatch":
                    self.assertGreaterEqual(len(syncs),1)
                    submissions.append(cmd)
                    raise subprocess.CalledProcessError(143,cmd)
                raise AssertionError(cmd)
            with patch.object(retry, "__file__",str(runner / "retry.py")), patch.object(retry,"Path",side_effect=path_map), patch.object(retry.subprocess,"run",side_effect=fake), patch.object(retry.os,"fsync",side_effect=lambda fd:syncs.append(fd)), patch.object(sys,"argv",["retry.py","dev",run]), contextlib.redirect_stdout(io.StringIO()):
                with self.assertRaises(subprocess.CalledProcessError): retry.main()
                with self.assertRaises(ValueError): retry.main()
            self.assertEqual(len(submissions),1)
            self.assertTrue((logs / "retry_dev.intent").is_file())

    def test_accounting_rejects_missing_and_sums_cells(self):
        with tempfile.TemporaryDirectory(dir=HERE) as tmp:
            root = Path(tmp) / "20261030T0000Z_bench_f3v2_dev"; root.mkdir()
            (root / "jobs.tsv").write_text("cell\tjob_id\tminutes\tmem_gib\tcommand\ndev\t42\t75\t4\tprimary\n")
            raw = "".join(f"42_{i}|COMPLETED|60|1|60|0:0\n" for i in range(1,27))
            argv = ["accounting.py", str(root)]
            out = io.StringIO()
            def fake(cmd, **kwargs):
                return SimpleNamespace(stdout="" if cmd[0] == "squeue" else raw)
            with patch.object(sys, "argv", argv), patch.object(accounting.subprocess, "run", side_effect=fake), contextlib.redirect_stdout(out):
                accounting.main()
            self.assertEqual(out.getvalue().count("CELL_TOTAL"), 4)
            self.assertIn("\t0.43333333333333335\t", out.getvalue())
            def incomplete(cmd, **kwargs):
                return SimpleNamespace(stdout="" if cmd[0] == "squeue" else raw.split("42_26|")[0])
            with patch.object(sys, "argv", argv), patch.object(accounting.subprocess, "run", side_effect=incomplete), contextlib.redirect_stdout(io.StringIO()):
                with self.assertRaises(ValueError): accounting.main()


if __name__ == "__main__":
    unittest.main(verbosity=2)
