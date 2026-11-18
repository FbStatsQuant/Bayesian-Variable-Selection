# overlap1e4: analysis of the 10⁴ T-vs-V overlap rung

Pre-registration: `OVERLAP_1e4_PREREG.md` (script sha256 inside). Script: `compare_overlap.py` (python3, **stdlib only**, read-only on the run dirs; tested on Python 3.9).

## Inputs
- Run dirs `records/<batch>/<run_id>/` (Owls `SMC_Engineering_Department/records/`, after offload + `sha256sum -c`), both arms, run ids `4-<design>-n200-r<rep>-<T|V>-s<1|2>`.
  Needed per dir: `eval.bin.json` (or `eval.json`), `truth.json`, `run_manifest.json`, **`fit.bin`** (the p-wide PIPs are only there), and the cost file (`cost_<run_id>.json` from `p1m_cost.py`, in the run dir, in `cost/`, or in a `--cost-dir`).
- The V-vs-T cross Hellinger file (`--cross-file`), once the extra `law.bin` evaluation exists (PREREG §3.6, §8 item 1).

## After each wave (W0, W1, W2): partial read, no verdict
```
python3 -I compare_overlap.py --wave-check --records /path/records/<batch> [more roots ...] --out /path/overlap1e4/out_W0 [--cost-dir DIR]
```
Writes `wave_check.csv` (one row per dataset × seed with both arms: HPM / MPM equality, F, log Ẑ difference in island s.e., worst PIP ratio, d_H(T, f\*), the triangle screen, cost, tier / escalation flags) and `per_fit.csv` (every fit, `reasons` = why it is not delivered). Use it first on W0 to check that the T-arm fields parse; island-only s.e., one seed: it is not the pre-registered test.

Single-arm field check (no pairing): `compare_overlap.py --smoke --records DIR [--fitbin-dir DIR] --out OUT`.

## After W3 (40/40): the pre-registered comparison
```
python3 -I compare_overlap.py --records /path/records/<W0> /path/records/<W1> /path/records/<W2> /path/records/<W3> \
    --out /path/overlap1e4/verdict_final --cost-dir /path/cost_dirs ... \
    --cross-file /path/cross_vt.json --expect-commit <F>
```
Outputs: `per_dataset.csv`, `per_fit.csv`, `verdict.md`, `verdict.json` (outcome CLEAN / MARGINAL / NOT CLEAN / INCOMPLETE / INVALID, every criterion with status and detail, the PREREG constants, the script sha256). Do not edit them; the independent review reads them. The same command on W0–W2 only cannot return CLEAN (criterion D fails, usually INCOMPLETE); treat it as a dry run, not a verdict.

Check the script sha256 before the final run: `sha256sum compare_overlap.py` must equal the value in `OVERLAP_1e4_PREREG.md`.

## Self-test (any time, no cluster data)
```
python3 -B tests/test_compare_overlap.py [--keep DIR]
```
13 synthetic cases (clean, one HPM mismatch → CLEAN 9/10, two → NOT CLEAN, Hellinger fail on 1 / 2 datasets, T higher F, PIP fail, evidence fail, cost over, missing fit, missing fit.bin, broken X/y pairing → INVALID, no cross file → INCOMPLETE) + a `--wave-check` case. The fixtures are generated from `tests/template_eval.bin.json` (the real T5 eval record) and a real-format `fit.bin` container, p = 200.

## Exit meaning of the criteria
`D` delivered 40/40 · `PAIR` X/y sha pairing · `S1` HPM sets (≥ 9/10) · `S2` T never higher F · `S3` MPM equal · `S4` NULL PIP ≤ 0.5 · `P` PIP tolerance · `E1` log Ẑ · `E2` log Z_T lower-bound consistency · `H` predictive Hellinger · `C` cost ≤ 1.5× model. Formulas: PREREG §3. Outcome rules: PREREG §4.
