#!/usr/bin/env python3
import importlib.util
from pathlib import Path
import unittest

JOB = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("sizing", JOB / "runner" / "sizing.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def sample():
    rows = []
    i = 0
    for p in (500, 1000):
        for scenario in range(1, 7):
            for scale in ("c100", "c050"):
                i += 1
                rows.append(dict(index=str(i), p=str(p), scale=scale, wall_seconds="60", max_rss_kib="1048576"))
    for _ in range(2):
        i += 1
        rows.append(dict(index=str(i), p="1000", scale="c050", wall_seconds="120", max_rss_kib="2097152"))
    return rows


class SizingTests(unittest.TestCase):
    def test_known_values(self):
        result = mod.sizing(sample())
        self.assertEqual(len(result), 4)
        self.assertEqual(result[-1][2:3], (8,))
        self.assertEqual(result[-1][4:8], (120.0, 2097152, 10, 3))
        self.assertAlmostEqual(sum(x[-1] for x in result), 42.5)

    def test_duplicate_or_missing_refused(self):
        rows = sample()
        rows[-1]["index"] = "25"
        with self.assertRaises(ValueError):
            mod.sizing(rows)
        with self.assertRaises(ValueError):
            mod.sizing(sample()[:-1])


if __name__ == "__main__":
    unittest.main(verbosity=2)
