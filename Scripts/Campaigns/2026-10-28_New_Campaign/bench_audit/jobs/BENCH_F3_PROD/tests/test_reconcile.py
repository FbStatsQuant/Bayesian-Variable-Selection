#!/usr/bin/env python3
import csv
import hashlib
from pathlib import Path
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "runner"))
import reconcile

SOURCE = "a" * 64


def fixture(root):
    for _, p, _, _, scale, dataset, _ in reconcile.units("dev"):
        folder = root / f"p{p:04d}" / f"{dataset}_{scale}"
        folder.mkdir(parents=True)
        (folder / "F3.done").write_text("done\n")
        (folder / "F3.rds").write_bytes(b"fixture, not an RDS")
        with (folder / "F3.csv").open("w", newline="") as f:
            fields = ["run_id", "dataset_id", "case_id", "scale_key", "method_id", "source_sha256", "rule_id", "status"]
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            w.writerow(dict(run_id="test", dataset_id=dataset, case_id=dataset + "_" + scale,
                            scale_key=scale, method_id="F3", source_sha256=SOURCE, rule_id="cv_min", status="ok"))
        hashes = [hashlib.sha256((folder / n).read_bytes()).hexdigest() + "  " + n
                  for n in ("F3.rds", "F3.csv")]
        (folder / "F3.sha256").write_text("\n".join(hashes) + "\n")


class ReconcileTests(unittest.TestCase):
    def test_complete_and_negative_controls(self):
        with tempfile.TemporaryDirectory(dir=HERE) as tmp:
            root = Path(tmp)
            fixture(root)
            rows, extras, tally = reconcile.reconcile(root, "dev", "test", SOURCE)
            self.assertEqual(sum(r[2] == "valid" for r in rows), 26)
            self.assertEqual(tally["ok"], 26)
            self.assertEqual(extras, [])
            folder = root / rows[0][1]
            (folder / "F3.done").unlink()
            self.assertEqual(reconcile.reconcile(root, "dev", "test", SOURCE)[0][0][2], "missing")
            (folder / "F3.done").write_text("done\n")
            (folder / "F3.rds").write_text("corrupt")
            self.assertEqual(reconcile.reconcile(root, "dev", "test", SOURCE)[0][0][2], "corrupt")
            hashes = (folder / "F3.sha256").read_text().splitlines()
            (folder / "F3.sha256").write_text(hashes[1] + "\n" + hashes[1] + "\n")
            self.assertEqual(reconcile.reconcile(root, "dev", "test", SOURCE)[0][0][2], "corrupt")
            duplicate = root / "p0500" / "unexpected_copy"
            duplicate.mkdir()
            (duplicate / "F3.done").write_text("duplicate")
            self.assertEqual(reconcile.reconcile(root, "dev", "test", SOURCE)[1], ["p0500/unexpected_copy"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
