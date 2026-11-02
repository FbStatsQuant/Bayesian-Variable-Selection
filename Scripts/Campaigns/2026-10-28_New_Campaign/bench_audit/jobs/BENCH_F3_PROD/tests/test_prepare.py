#!/usr/bin/env python3
import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
PROD = HERE.parent
sys.path.insert(0, str(PROD / "runner"))
import frozen
spec = importlib.util.spec_from_file_location("prepare", PROD / "prepare.py")
prepare = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prepare)


class PackageTests(unittest.TestCase):
    def test_prepare_and_upload_verifier(self):
        with tempfile.TemporaryDirectory(dir=HERE) as tmp:
            root = Path(tmp); code = root / "code"; tree = code / "F3_AdaptiveLasso"
            tree.mkdir(parents=True)
            names = ("config.R", "common.R", "methods/glmnet_helpers.R", "methods/fit_F3_alasso.R", "run_case.R")
            for name in names:
                f = tree / name; f.parent.mkdir(exist_ok=True); f.write_text(name)
            manifest = code / "MANIFEST_SHA256.txt"
            manifest.write_text("".join(f"{frozen.sha(tree / n)}  F3_AdaptiveLasso/{n}\n" for n in names))
            source = hashlib.sha256("\n".join(f"{n}  {frozen.sha(tree/n)}" for n in names).encode()).hexdigest()
            jobs = root / "jobs"; prod = jobs / "BENCH_F3_PROD"; runner = prod / "runner"
            runner.mkdir(parents=True)
            (runner / "freeze.json").write_text(json.dumps({"source_sha256":source, "manifest_sha256":frozen.sha(manifest)}))
            (prod / "JOB.md").write_text("production job")
            dev = jobs / "BENCH_F3_DEV" / "runner"; dev.mkdir(parents=True)
            (dev / "sizing.py").write_text("test")
            run = "20261030T0000Z_bench_f3v2_prod"
            with patch.object(prepare, "HERE", prod), patch.object(sys, "argv", ["prepare.py", "prod", run, str(code)]), contextlib.redirect_stdout(io.StringIO()):
                prepare.main()
                with self.assertRaises(ValueError): prepare.main()
            staged = jobs / "staging" / run
            digest = frozen.sha(staged / "UPLOAD_SHA256.txt")
            cmd = [sys.executable, "-B", str(PROD / "runner" / "upload_check.py"), str(staged), digest]
            self.assertEqual(subprocess.run(cmd, capture_output=True).returncode, 0)
            self.assertEqual((staged / "MANIFEST_SHA256.txt").read_bytes(), (staged / "runner" / "MANIFEST_SHA256.txt").read_bytes())
            self.assertEqual(subprocess.run(cmd, capture_output=True).returncode, 0)
            (staged / "JOB.md").write_text("changed")
            self.assertNotEqual(subprocess.run(cmd, capture_output=True).returncode, 0)

    def test_real_freeze_prepare_repeat_verify(self):
        code = Path("C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2")
        with tempfile.TemporaryDirectory(dir=HERE) as tmp:
            jobs = Path(tmp) / "jobs"; prod = jobs / "BENCH_F3_PROD"; prod.mkdir(parents=True)
            shutil.copytree(PROD / "runner", prod / "runner", ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            (prod / "JOB.md").write_text("test")
            dev = jobs / "BENCH_F3_DEV" / "runner"; dev.mkdir(parents=True)
            shutil.copy2(PROD.parent / "BENCH_F3_DEV" / "runner" / "sizing.py", dev / "sizing.py")
            run = "20261030T235959Z_bench_f3v2_prod"
            with patch.object(prepare, "HERE", prod), patch.object(sys, "argv", ["prepare.py", "prod", run, str(code)]), contextlib.redirect_stdout(io.StringIO()):
                prepare.main()
            upload = jobs / "staging" / run
            digest = frozen.sha(upload / "UPLOAD_SHA256.txt")
            command = [sys.executable, "-B", str(PROD / "runner" / "upload_check.py"), str(upload), digest]
            installed = jobs / "simulated_install" / "F3_AdaptiveLasso"
            installed.parent.mkdir()
            shutil.copytree(upload / "F3_AdaptiveLasso", installed)
            for _ in range(2):
                self.assertEqual(subprocess.run(command, capture_output=True).returncode, 0)
                self.assertEqual((upload / "MANIFEST_SHA256.txt").read_bytes(), (upload / "runner" / "MANIFEST_SHA256.txt").read_bytes())
                frozen.check(installed, upload / "runner" / "MANIFEST_SHA256.txt", upload / "runner" / "freeze.json")
            dry_run = [sys.executable, str(upload / "runner" / "launch.py"), "prod", run,
                       "--resources", str(upload / "runner" / "resources.json"), "--dry-run"]
            self.assertEqual(subprocess.run(dry_run, capture_output=True).returncode, 0)
            self.assertEqual(subprocess.run(command, capture_output=True).returncode, 0)
            downloaded = jobs / "downloaded_upload"
            shutil.copytree(upload, downloaded)
            verify_download = [sys.executable, "-B", str(PROD / "runner" / "upload_check.py"), str(downloaded), digest]
            self.assertEqual(subprocess.run(verify_download, capture_output=True).returncode, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
