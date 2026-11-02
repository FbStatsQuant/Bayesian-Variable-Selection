#!/usr/bin/env python3
"""test_lists.py -- acceptance tests of lists/units.tsv (DESIGN.md section 1).  py -3 test_lists.py [WORKDIR]

Columns: piece task unit dataset scale repeat.  enum20: 600 rows, 1 task; enum30: 600 rows, 24 tasks x 25 (task = 4*(s-1) + block); smc: 2,400 rows, 96 tasks x 25
(cell (p,S,c) x 4 blocks of 25 replicates); smcrep: 12,000 rows, 480 tasks x 25 (cell x m x 4 blocks); no bench rows.  Unit ids: enum `p0020_S1_r001`,
smc `p0020_S1_r001_c100`, smcrep `p0020_S1_r001_c100_rep3`.  Replicate order ascending inside a task.
"""
import collections
import os
import re
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.dirname(HERE)
UNITS = os.path.join(B, 'lists', 'units.tsv')
MAKE = os.path.join(B, 'tools', 'make_lists.py')
HEADER = ['piece', 'task', 'unit', 'dataset', 'scale', 'repeat']
PS, SS, CS, MS, RS = ('0020', '0030'), tuple(range(1, 7)), ('c100', 'c050'), (1, 2, 3, 4, 5), tuple(range(1, 101))
COUNTS = {'enum20': 600, 'enum30': 600, 'smc': 2400, 'smcrep': 12000}
NTASKS = {'enum20': 1, 'enum30': 24, 'smc': 96, 'smcrep': 480}
DS_RE = re.compile(r'^p(0020|0030)_S([1-6])_r(\d{3})$')


def load():
    with open(UNITS, 'rb') as fh:
        raw = fh.read()
    text = raw.decode('utf-8')
    rows = [ln.split('\t') for ln in text.split('\n') if ln != '']
    return raw, text, rows


def ds_parts(ds):
    m = DS_RE.match(ds)
    return (m.group(1), int(m.group(2)), int(m.group(3))) if m else None


class TestLists(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw, cls.text, cls.rows = load()
        cls.header = cls.rows[0]
        cls.data = cls.rows[1:]
        cls.by = collections.defaultdict(list)
        for r in cls.data:
            if len(r) == 6:
                cls.by[r[0]].append(r)

    # ---- file shape ---------------------------------------------------------------------------------------------------------
    def test_L01_file_exists_lf_only_trailing_newline(self):
        self.assertTrue(os.path.isfile(UNITS))
        self.assertNotIn(b'\r', self.raw, 'LF line endings only')
        self.assertTrue(self.raw.endswith(b'\n'))
        self.assertNotIn('\n\n', self.text, 'no blank lines')

    def test_L02_header(self):
        self.assertEqual(self.header, HEADER)

    def test_L03_every_row_has_six_columns(self):
        self.assertEqual([r for r in self.data if len(r) != 6][:3], [])

    def test_L04_pieces_and_counts(self):
        self.assertEqual(sorted(self.by), sorted(COUNTS), 'pieces present (no bench rows)')
        for p, n in COUNTS.items():
            self.assertEqual(len(self.by[p]), n, p)
        self.assertEqual(len(self.data), sum(COUNTS.values()))

    def test_L05_no_bench_rows(self):
        self.assertEqual([r for r in self.data if 'bench' in r[0]], [])

    def test_L06_units_unique_within_piece_and_overall(self):
        for p, rows in self.by.items():
            units = [r[2] for r in rows]
            self.assertEqual(len(units), len(set(units)), 'duplicate unit ids in ' + p)
        allu = [r[2] for r in self.data]
        self.assertEqual(len(allu), len(set(allu)), 'unit ids are unique across pieces too')

    def test_L07_task_counts_and_sizes(self):
        for p, n in NTASKS.items():
            t = collections.Counter(int(r[1]) for r in self.by[p])
            self.assertEqual(sorted(t), list(range(n)), '%s task ids 0..%d' % (p, n - 1))
            if p != 'enum20':
                self.assertEqual(set(t.values()), {25}, '%s: 25 units per task' % p)
        self.assertEqual(len(self.by['enum20']), 600)

    # ---- unit id formats ----------------------------------------------------------------------------------------------------
    def test_L10_enum_unit_format(self):
        for p, pp in (('enum20', '0020'), ('enum30', '0030')):
            for r in self.by[p]:
                self.assertEqual(r[2], r[3], 'enum unit id = dataset id')
                parts = ds_parts(r[3])
                self.assertIsNotNone(parts, r)
                self.assertEqual(parts[0], pp, r)
                self.assertEqual((r[4], r[5]), ('-', '0'), r)

    def test_L11_smc_unit_format(self):
        for r in self.by['smc']:
            self.assertIsNotNone(ds_parts(r[3]), r)
            self.assertIn(r[4], CS, r)
            self.assertEqual(r[2], '%s_%s' % (r[3], r[4]), r)
            self.assertEqual(r[5], '0', r)

    def test_L12_smcrep_unit_format(self):
        for r in self.by['smcrep']:
            self.assertIsNotNone(ds_parts(r[3]), r)
            self.assertIn(r[4], CS, r)
            self.assertIn(r[5], [str(m) for m in MS], r)
            self.assertEqual(r[2], '%s_%s_rep%s' % (r[3], r[4], r[5]), r)

    # ---- exact enumeration --------------------------------------------------------------------------------------------------
    def test_L20_enum_datasets_exact(self):
        for p, pp in (('enum20', '0020'), ('enum30', '0030')):
            want = {'p%s_S%d_r%03d' % (pp, s, r) for s in SS for r in RS}
            self.assertEqual({r[3] for r in self.by[p]}, want, p)

    def test_L21_smc_cells_exact_and_replicates_once_per_cell(self):
        cells = collections.defaultdict(list)
        for r in self.by['smc']:
            p, s, rep = ds_parts(r[3])
            cells[(p, s, r[4])].append(rep)
        self.assertEqual(sorted(cells), sorted((p, s, c) for p in PS for s in SS for c in CS))
        for k, v in cells.items():
            self.assertEqual(sorted(v), list(RS), 'replicates 1..100 exactly once in cell %s' % (k,))

    def test_L22_smcrep_cells_exact_and_replicates_once_per_cell_and_m(self):
        cells = collections.defaultdict(list)
        for r in self.by['smcrep']:
            p, s, rep = ds_parts(r[3])
            cells[(p, s, r[4], int(r[5]))].append(rep)
        self.assertEqual(sorted(cells), sorted((p, s, c, m) for p in PS for s in SS for c in CS for m in MS))
        for k, v in cells.items():
            self.assertEqual(sorted(v), list(RS), 'replicates 1..100 exactly once in cell %s' % (k,))

    def test_L23_every_smc_unit_has_exactly_five_repeats(self):
        reps = collections.defaultdict(list)
        for r in self.by['smcrep']:
            reps[(r[3], r[4])].append(int(r[5]))
        smc_units = {(r[3], r[4]) for r in self.by['smc']}
        self.assertEqual(set(reps), smc_units, 'smcrep covers exactly the smc (dataset, scale) units')
        bad = [k for k, v in reps.items() if sorted(v) != [1, 2, 3, 4, 5]]
        self.assertEqual(bad[:5], [], 'each smc unit has repeats m = 1..5 exactly once')
        self.assertEqual(len(smc_units) * 5, len(self.by['smcrep']))

    # ---- task structure -----------------------------------------------------------------------------------------------------
    def test_L30_enum30_task_formula(self):
        for r in self.by['enum30']:
            p, s, rep = ds_parts(r[3])
            self.assertEqual(int(r[1]), 4 * (s - 1) + (rep - 1) // 25, r)

    def test_L31_each_task_holds_one_cell_and_one_block_of_25_replicates(self):
        for piece in ('enum30', 'smc', 'smcrep'):
            tasks = collections.defaultdict(list)
            for r in self.by[piece]:
                tasks[int(r[1])].append(r)
            blocks_of_cell = collections.defaultdict(set)
            for t, rows in tasks.items():
                cells = set()
                for r in rows:
                    p, s, rep = ds_parts(r[3])
                    cells.add((p, s, r[4] if piece != 'enum30' else '-', r[5] if piece == 'smcrep' else '0'))
                self.assertEqual(len(cells), 1, '%s task %d mixes cells %s' % (piece, t, sorted(cells)[:3]))
                reps = [ds_parts(r[3])[2] for r in rows]
                block = (reps[0] - 1) // 25
                self.assertEqual(reps, list(range(25 * block + 1, 25 * block + 26)), '%s task %d: ascending block of 25 replicates' % (piece, t))
                blocks_of_cell[next(iter(cells))].add(block)
            for cell, blocks in blocks_of_cell.items():
                self.assertEqual(blocks, {0, 1, 2, 3}, '%s cell %s: its 4 blocks sit in 4 different tasks' % (piece, cell))
            ncell = {'enum30': 6, 'smc': 24, 'smcrep': 120}[piece]
            self.assertEqual(len(blocks_of_cell), ncell)

    def test_L32_enum20_is_a_single_task_zero(self):
        self.assertEqual({r[1] for r in self.by['enum20']}, {'0'})

    def test_L33_replicates_ascending_inside_every_task(self):
        last = {}
        for r in self.data:
            key = (r[0], r[1], ds_parts(r[3])[1])      # enum20 holds the 6 scenarios in one task: ascending within each scenario
            rep = ds_parts(r[3])[2]
            if key in last:
                self.assertGreater(rep, last[key], 'task %s of %s not ascending at %s' % (r[1], r[0], r[2]))
            last[key] = rep

    def test_L34_scenario_p_scale_ids_are_in_range(self):
        for r in self.data:
            p, s, rep = ds_parts(r[3])
            self.assertIn(p, PS)
            self.assertIn(s, SS)
            self.assertIn(rep, RS)

    def test_L40_generator_exists(self):
        self.assertTrue(os.path.isfile(MAKE), 'tools/make_lists.py (the committed generator) is missing')


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
