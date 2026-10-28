"""Stage A source registration under lead ruling R-2; never edit the project ledger."""
import hashlib
from pathlib import Path

base=Path(__file__).resolve().parents[1]
project=base.parents[2]
ledger=base/'LEDGER_CANDIDATES.md'
marker='## SMC-BVS v3 deployment'
if ledger.exists():
    raise SystemExit('candidate file exists; preserve it and stage a deliberate new revision')
purpose={
'v3.R':'production loader and reproducible compiler cache',
'v3_preprocess.R':'Part I preprocessing, exact-branch decision, fixed budgets and seed validation',
'v3_setup.R':'Part I context, composite blocks/tables/start and neighbours',
'v3_run.R':'Part I final evidence/primary PIPs, selected-HPM local certificate, stage records and stream documentation',
'v3_calib.R':'Part I pilot, restricted grid, rebuilds/escalation, diagnostics and guard checkpoints',
'v3_exact.R':'Part I exact enumeration wrapper and heuristic certificate reporting',
'v3_fit.R':'Part I fit orchestration, memory-only SMC preflight, exact timing and operational limits',
'v3_core.cpp':'Part I Rcpp exports, exact enumeration, uncapped cut_group and calibration state',
'v3_score.h':'Part I normalized scorer, Cholesky/refactor/QR and numerical-route counts',
'v3_blocks.h':'Part I complete linkage, composite blocks and neighbour graph (prototype bytes)',
'v3_start.h':'Part I exact composite-start law, convolution and sampler (prototype bytes)',
'v3_calib.h':'Part I restricted grid and RC-2 forced-step snap (prototype bytes)',
'v3_engine.h':'Part I bridge kernels, inverse-CDF guide resampling, RB PIPs and local search',
'v3_ledger.h':'Part I HPM tie rule, score ledger and stores',
'v3_util.h':'Part I seed splitting, SplitMix64/xoshiro256 and keys (prototype bytes)',
'v3_runtime.h':'Part I strict elapsed+operation runtime guard and checkpoint archive',
'v3_holder.h':'shared Rcpp scorer-context ownership',
'Makevars.v3':'prototype compiler arithmetic flags, no FMA contraction',
'adapter.R':'Part IV.1.4 one-case/scale rows, primary PIP original-index mapping, hashes and method seed',
'run_case.R':'single-unit CLI and explicit allocation/adapter-policy inputs',
'generate_smoke.R':'Part II.7 dev-only seed and input generation wrapper',
'gen_dev_data.R':'pinned benchmark development generator; inputs component only',
'run_smoke.R':'single dev fit at full production settings and explicit allocation',
}
files=sorted(p for p in (base/'code').rglob('*') if p.is_file() and (p.suffix in {'.R','.cpp','.h'} or p.name=='Makevars.v3'))
files += [base/'smoke/generate_smoke.R',base/'smoke/reference/gen_dev_data.R',base/'smoke/run_smoke.R']
lines=['',marker,'',
'Thread A, 2026-10-22. Math: `01_Methodology_and_Theory/MASTER_Methodology_and_Plan/MASTER_Methodology_and_Plan.md`, Part I; study adapter Part IV.1.4; dev seeds Part II.7. Order: pinned dev/input source -> input-hash adapter -> production loader/preprocessing/setup/calibration/final -> full record and hpm/pip05 rows. No truth or holdout is read by fitting.',
'',
'All rows below are **unverified pending Thread B**. A own tests and internal review do not substitute for B\'s independent Part I checks. Build on Owls R 4.6.0/GCC 11.5.0 passed; R-1 revision adapter evidence is in the current handoff. Regression and full dev smoke evidence is tracked in `A_build/HANDOFF_v1.md` and `A_build/STATUS.md` under the deployment folder. The lead alone merges these candidates. Earlier pre-ruling registrations already in the project ledger must be deduplicated by path and SHA-256.',
'', '| path | implements | author | status | date | sha256 |','|---|---|---|---|---|---|']
inventory=[]
for path in files:
    digest=hashlib.sha256(path.read_bytes()).hexdigest()
    relative=path.relative_to(project).as_posix()
    author='AI (GPT-6.1 Sol; prototype retained where stated)'
    if path.name=='gen_dev_data.R': author='benchmark generator, unchanged pinned copy'
    lines.append(f'| {relative} | {purpose[path.name]} | {author} | unverified (B pending) | 2026-10-22 | {digest} |')
    inventory.append(f'{digest}  {relative}')
payload=('\n'.join(lines)+'\n').encode('utf-8')
with ledger.open('xb') as f: f.write(payload)
(base/'evidence/ledger_registration.sha256').write_bytes(('\n'.join(inventory)+'\n').encode())
print(f'Staged {len(files)} source rows in A_build/LEDGER_CANDIDATES.md; root files untouched.')
