#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
import subprocess

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "runner"))
import frozen


class FreezeTests(unittest.TestCase):
    def test_membership_hash_and_source(self):
        with tempfile.TemporaryDirectory(dir=HERE) as tmp:
            root = Path(tmp); tree = root / "F3_AdaptiveLasso"; tree.mkdir()
            names = ("config.R", "common.R", "methods/glmnet_helpers.R",
                     "methods/fit_F3_alasso.R", "run_case.R")
            for name in names:
                f = tree / name
                f.parent.mkdir(exist_ok=True)
                f.write_text(name)
            manifest = root / "MANIFEST_SHA256.txt"
            manifest.write_text("".join(f"{frozen.sha(tree / n)}  F3_AdaptiveLasso/{n}\n" for n in names))
            source = hashlib.sha256("\n".join(f"{n}  {frozen.sha(tree/n)}" for n in names).encode()).hexdigest()
            freeze = root / "freeze.json"
            freeze.write_text(json.dumps(dict(manifest_sha256=frozen.sha(manifest), source_sha256=source)))
            frozen.check(tree, manifest, freeze)
            (tree / "extra").write_text("extra")
            with self.assertRaises(ValueError): frozen.check(tree, manifest, freeze)
            (tree / "extra").unlink()
            (tree / "config.R").write_text("changed")
            with self.assertRaises(ValueError): frozen.check(tree, manifest, freeze)
            (tree / "config.R").write_text("config.R")
            freeze.write_text(json.dumps(dict(manifest_sha256=frozen.sha(manifest), source_sha256="b"*64)))
            with self.assertRaises(ValueError): frozen.check(tree, manifest, freeze)

    def test_transfer_manifest_detects_changes(self):
        with tempfile.TemporaryDirectory(dir=HERE) as tmp:
            folder = Path(tmp)
            (folder / "result").write_text("result")
            cmd = [sys.executable, "-B", str(HERE.parent / "runner" / "manifests.py"), str(folder)]
            self.assertEqual(subprocess.run(cmd, capture_output=True).returncode, 0)
            self.assertEqual(subprocess.run(cmd + ["--verify"], capture_output=True).returncode, 0)
            (folder / "result").write_text("changed")
            self.assertNotEqual(subprocess.run(cmd + ["--verify"], capture_output=True).returncode, 0)

    def test_manifests_preflight_and_empty(self):
        with tempfile.TemporaryDirectory(dir=HERE) as tmp:
            root = Path(tmp); a = root / "a"; b = root / "b"; c = root / "c"
            for folder in (a, b, c): folder.mkdir()
            (a / "one").write_text("one")
            (c / "incomplete.tmp").write_text("unfinished")
            cmd = [sys.executable, "-B", str(HERE.parent / "runner" / "manifests.py"), str(a), str(b), str(c)]
            self.assertNotEqual(subprocess.run(cmd, capture_output=True).returncode, 0)
            self.assertFalse((a / "MANIFEST.sha256").exists())
            (c / "incomplete.tmp").unlink()
            self.assertEqual(subprocess.run(cmd, capture_output=True).returncode, 0)
            self.assertEqual((b / "MANIFEST.sha256").read_bytes(), b"")
            self.assertEqual(subprocess.run(cmd + ["--verify"], capture_output=True).returncode, 0)
            (b / "unexpected").write_text("new")
            self.assertNotEqual(subprocess.run(cmd + ["--verify"], capture_output=True).returncode, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
