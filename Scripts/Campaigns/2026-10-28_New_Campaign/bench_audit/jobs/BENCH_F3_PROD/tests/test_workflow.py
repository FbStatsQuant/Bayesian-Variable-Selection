#!/usr/bin/env python3
import csv
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import subprocess
import unittest

HERE = Path(__file__).resolve().parent
RUNNER = HERE.parent / "runner"
sys.path.insert(0, str(RUNNER))
import fill_resources
import launch
import retry
import throttle
import terminal


class WorkflowTests(unittest.TestCase):
    def test_dry_run_vectors(self):
        cfg = json.loads((RUNNER / "resources.json").read_text())
        cmd = launch.commands("prod", "20261030T0000Z_bench_f3v2_prod", RUNNER, "a"*64, cfg)
        self.assertEqual(len(cmd), 4)
        self.assertEqual([next(x for x in c if x.startswith("--array=")) for c in cmd],
                         ["--array=1-1199:2%30", "--array=2-1200:2%30",
                          "--array=1201-2399:2%30", "--array=1202-2400:2%30"])
        self.assertEqual([next(x for x in c if x.startswith("--time=")) for c in cmd],
                         ["--time=30", "--time=30", "--time=30", "--time=30"])   # HQ D64 resources
        dev = launch.commands("dev", "20261030T0000Z_bench_f3v2_dev", RUNNER, "a"*64, cfg)
        self.assertIn("--array=1-26%13", dev[0])
        for c in cmd + dev:
            self.assertIn("--constraint=sapphirerapids", c)
            self.assertIn("--cpus-per-task=1", c)

    def test_retry_only_timeout_and_double(self):
        text = "JobID|State\n42_1|TIMEOUT\n42_2|FAILED\n42_3|OUT_OF_MEMORY\n42_4|COMPLETED\n"
        states = retry.select(text, "42", {1, 2, 3, 4})
        selected = [(i, Path(".")) for i, state in states.items() if state == "TIMEOUT"]
        cmd = retry.retry_command({"minutes":"45", "mem_gib":"4", "cell":"p0500_c050"}, selected, "prod", "run",
                                  RUNNER, "a"*64, Path("/scratch/logs"))
        self.assertIn("--array=1%30", cmd)
        self.assertIn("--time=90", cmd)
        with self.assertRaises(ValueError):
            retry.select(text, "42", {1,2,3,4,5})
        with self.assertRaises(ValueError):
            retry.select(text + "42_1|TIMEOUT\n", "42", {1,2,3,4})
        with tempfile.TemporaryDirectory(dir=HERE) as tmp:
            marker = Path(tmp) / "retry.intent"
            retry.claim(marker, cmd)
            with self.assertRaises(FileExistsError):
                retry.claim(marker, cmd)

    def test_fill(self):
        rows = [{"p":str(p), "scale":s, "time_minutes":str(t), "mem_gib":"3"}
                for p, s, t in [(500,"c100",11),(500,"c050",12),(1000,"c100",13),(1000,"c050",14)]]
        cfg = fill_resources.fill(rows)
        self.assertEqual(cfg["p1000_c050"], {"minutes":14,"mem_gib":3})
        self.assertEqual(len(cfg),4)
        with self.assertRaises(ValueError):
            fill_resources.fill(rows + rows[:1])
        with self.assertRaises(ValueError):
            fill_resources.fill(rows[:-1])
        with tempfile.TemporaryDirectory(dir=HERE) as tmp:
            sample = Path(tmp) / "sizing.tsv"; output = Path(tmp) / "resources.json"
            with sample.open("w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=rows[0].keys(), delimiter="\t")
                writer.writeheader(); writer.writerows(rows)
            cmd = [sys.executable, "-B", str(RUNNER / "fill_resources.py"), str(sample), str(output)]
            self.assertEqual(subprocess.run(cmd, capture_output=True).returncode, 0)
            self.assertEqual(json.loads(output.read_text())["p1000_c050"]["minutes"], 14)
            self.assertNotEqual(subprocess.run(cmd, capture_output=True).returncode, 0)

    def test_all_array_throttles_fail_closed(self):
        data = "42_1|other|RUNNING\n42_[2-20%20]|other|PENDING\n55_[1-4%4]|next|PENDING\n66|plain|RUNNING\n"
        self.assertEqual(throttle.count(data), 24)
        self.assertEqual(throttle.count("42_[1-20]|other|PENDING\n"), 100000)
        with self.assertRaises(ValueError):
            throttle.count("bad_array|other|PENDING\n")
        from unittest.mock import patch
        from types import SimpleNamespace
        with patch.object(throttle.subprocess, "run", return_value=SimpleNamespace(stdout="55_[1-80%80]|other|PENDING\n")):
            with self.assertRaises(ValueError): throttle.check(30)

    def test_terminal_absent_vs_live_and_query_failure(self):
        from unittest.mock import patch
        from types import SimpleNamespace
        with patch.object(terminal.subprocess, "run", return_value=SimpleNamespace(stdout="88_3\n")):
            terminal.assert_absent("42")
        with patch.object(terminal.subprocess, "run", return_value=SimpleNamespace(stdout="42_3\n")):
            with self.assertRaises(ValueError): terminal.assert_absent("42")
        with patch.object(terminal.subprocess, "run", side_effect=subprocess.CalledProcessError(1, "squeue")):
            with self.assertRaises(subprocess.CalledProcessError): terminal.assert_absent("42")


if __name__ == "__main__":
    unittest.main(verbosity=2)
