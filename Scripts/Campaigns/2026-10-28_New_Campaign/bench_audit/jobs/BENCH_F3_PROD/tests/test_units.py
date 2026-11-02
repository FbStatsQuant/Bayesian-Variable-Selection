#!/usr/bin/env python3
"""Check the complete mapping without executing fits."""
import importlib.util
from pathlib import Path
import unittest

path = Path(__file__).resolve().parents[1] / "runner" / "units.py"
spec = importlib.util.spec_from_file_location("units", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class MappingTests(unittest.TestCase):
    def test_production_cartesian_product(self):
        rows = module.units("prod")
        self.assertEqual(len(rows), 2400)
        self.assertEqual([r[0] for r in rows], list(range(1, 2401)))
        self.assertEqual({r[1:5] for r in rows}, {(p, s, r, c)
            for p in (500, 1000) for s in range(1, 7) for r in range(1, 101)
            for c in ("c100", "c050")})
        self.assertEqual(len({r[5] + "_" + r[4] for r in rows}), 2400)

    def test_dev_and_timing(self):
        rows = module.units("dev")
        self.assertEqual(len(rows), 26)
        self.assertEqual([r[0] for r in rows], list(range(1, 27)))
        self.assertEqual(len({r[5] + "_" + r[4] for r in rows}), 26)
        self.assertEqual(sum(r[6] == "dev" for r in rows), 24)
        self.assertEqual({(r[2], r[4]) for r in rows if r[6] == "prod"},
                         {(4, "c050"), (6, "c050")})


if __name__ == "__main__":
    unittest.main(verbosity=2)
