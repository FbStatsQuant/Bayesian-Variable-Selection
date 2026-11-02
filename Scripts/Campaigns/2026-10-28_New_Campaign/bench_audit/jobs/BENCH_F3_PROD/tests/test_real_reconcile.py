#!/usr/bin/env python3
import contextlib
import io
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "runner"))
import reconcile
from validate_args import args_for

CAMP = Path("C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign")
STUDY = Path("C:/Users/felip/Documents/NOTS_BVS/NOTS_projects_ml75/BVS/bench20261019")
CODE = CAMP / "code/bench_v2/F3_AdaptiveLasso"
ROOT = CAMP / "code/bench_v2/tests/runner_output/results/v2_local_e2e"
SOURCE = "3e01c77b27ad96ad8ec4761b6b25ea5511d357e8aa08a1db7b2972e71734f42c"
R = "C:/Program Files/R/R-4.4.1/bin/Rscript.exe"
UNIT = (1,500,1,1,"c100","dev_p0500_S1_r001","dev")


class RealReconciliation(unittest.TestCase):
    def test_real_fixture_through_reconciliation(self):
        run = subprocess.run
        def actual_r(cmd, **kwargs):
            self.assertEqual(cmd[0], "Rscript")
            return run([R] + cmd[1:], **kwargs)
        def fixture_args(root, run_id, source, unit):
            return args_for(root, run_id, source, unit, study=STUDY, code=CODE)
        argv = ["reconcile.py", "--root", str(ROOT), "--kind", "dev", "--run-id", "v2_local_e2e", "--source-sha256", SOURCE]
        with patch.object(reconcile,"units",return_value=[UNIT]), patch.object(reconcile,"args_for",side_effect=fixture_args), patch.object(reconcile.subprocess,"run",side_effect=actual_r), patch.object(sys,"argv",argv), contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(reconcile.main(),0)


if __name__=="__main__":
    unittest.main(verbosity=2)
