#!/usr/bin/env python3
"""test_lists.py -- acceptance tests of lists/units.tsv of PROD_L_BENCH (DESIGN.md section 2).  py -3 test_lists.py [WORKDIR]

Header piece task unit dataset scale repeat (as PROD-L). Piece `bench` ONLY, 2,400 units `<dataset>_<scale>` (dataset p0020|p0030 x S1..S6 x r001..r100, scale c100|c050),
repeat 0, 96 tasks x 25 (cell (p, S, c) x 4 blocks of 25 replicates, replicate ascending). No other piece (no enum, smc, smcrep, benchretry rows).
"""
import collections
import os
import re
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
B = os.environ.get('PRODL_B_SRC') or os.path.dirname(HERE)
UNITS = os.path.join(B, 'lists', 'units.tsv')
MAKE = os.path.join(B, 'tools', 'make_lists.py')
HEADER = ['piece', 'task', 'unit', 'dataset', 'scale', 'repeat']
PS, SS, CS, RS = ('0020', '0030'), tuple(range(1, 7)), ('c100', 'c050'), tuple(range(1, 101))
DS_RE = re.compile(r'^p(0020|0030)_S([1-6])_r(\d{3})$')


def ds_parts(ds):
    m = DS_RE.match(ds)
    return (m.group(1), int(m.group(2)), int(m.group(3))) if m else None


class TestLists(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(UNITS, 'rb') as fh:
            cls.raw = fh.read()
        cls.text = cls.raw.decode('utf-8')
        rows = [ln.split('\t') for ln in cls.text.split('\n') if ln != '']
        cls.header, cls.data = rows[0], rows[1:]

    def test_L01_file_shape(self):
        self.assertNotIn(b'\r', self.raw, 'LF only')
        self.assertTrue(self.raw.endswith(b'\n'))
        self.assertNotIn('\n\n', self.text)

    def test_L02_header_and_columns(self):
        self.assertEqual(self.header, HEADER)
        self.assertEqual([r for r in self.data if len(r) != 6][:3], [])

    def test_L03_only_piece_bench_2400_rows(self):
        self.assertEqual({r[0] for r in self.data}, {'bench'})
        self.assertEqual(len(self.data), 2400)

    def test_L04_units_unique_and_format(self):
        units = [r[2] for r in self.data]
        self.assertEqual(len(units), len(set(units)))
        for r in self.data:
            self.assertIsNotNone(ds_parts(r[3]), r)
            self.assertIn(r[4], CS, r)
            self.assertEqual(r[2], '%s_%s' % (r[3], r[4]), r)
            self.assertEqual(r[5], '0', r)

    def test_L05_cells_and_replicates(self):
        cells = collections.defaultdict(list)
        for r in self.data:
            p, s, rep = ds_parts(r[3])
            cells[(p, s, r[4])].append(rep)
        self.assertEqual(sorted(cells), sorted((p, s, c) for p in PS for s in SS for c in CS))
        for k, v in cells.items():
            self.assertEqual(sorted(v), list(RS), 'replicates 1..100 exactly once in cell %s' % (k,))

    def test_L06_96_tasks_of_25_one_cell_one_block_each(self):
        tasks = collections.defaultdict(list)
        for r in self.data:
            tasks[int(r[1])].append(r)
        self.assertEqual(sorted(tasks), list(range(96)))
        blocks = collections.defaultdict(set)
        for t, rows in tasks.items():
            self.assertEqual(len(rows), 25, 'task %d size' % t)
            cell = {(ds_parts(r[3])[0], ds_parts(r[3])[1], r[4]) for r in rows}
            self.assertEqual(len(cell), 1, 'task %d mixes cells' % t)
            reps = [ds_parts(r[3])[2] for r in rows]
            b = (reps[0] - 1) // 25
            self.assertEqual(reps, list(range(25 * b + 1, 25 * b + 26)), 'task %d: ascending aligned block of 25 replicates' % t)
            blocks[next(iter(cell))].add(b)
        self.assertEqual(len(blocks), 24)
        for cell, bl in blocks.items():
            self.assertEqual(bl, {0, 1, 2, 3}, 'cell %s: 4 blocks in 4 different tasks' % (cell,))

    def test_L07_same_numbering_rule_as_the_prodl_smc_piece(self):
        """PROD-L's smc piece numbers tasks cell-by-cell in the order of its generator; the bench piece must reproduce that order (cells p, S, c)"""
        pl = os.path.join(os.path.dirname(B), 'PROD_L', 'lists', 'units.tsv')
        if not os.path.isfile(pl):
            self.skipTest('PROD_L lists not available')
        with open(pl, encoding='utf-8') as fh:
            smc = [ln.rstrip('\n').split('\t') for ln in fh if ln.startswith('smc\t')]
        mine = {r[2]: r[1] for r in self.data}
        self.assertEqual({r[2]: r[1] for r in smc}, mine, 'task numbering identical to PROD-L smc')

    def test_L08_generator_exists_and_checks(self):
        self.assertTrue(os.path.isfile(MAKE), 'tools/make_lists.py missing')


def load_workdir():
    sys.argv = [sys.argv[0]] + [a for a in sys.argv[1:] if a.startswith('-')]


if __name__ == '__main__':
    load_workdir()
    if not os.path.isfile(UNITS):
        print('FAIL lists/units.tsv not found at ' + UNITS)
        print('test_lists: 0 passed, 1 failed')
        sys.exit(1)
    suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    res = unittest.TextTestRunner(verbosity=2).run(suite)
    failed = len(res.failures) + len(res.errors) + len(res.skipped)
    print('test_lists: %d passed, %d failed' % (res.testsRun - failed, failed))
    sys.exit(0 if failed == 0 else 1)
