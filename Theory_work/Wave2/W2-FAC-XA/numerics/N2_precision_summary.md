# N2 floating-point ordering audit

The main run follows FAC-B general scans and the production exact-float-tie lexicographic rule. This independent direct F_many Cholesky audit re-scores the candidates tied by that scan. It does not substitute a different rule or revise the recorded path.

Improving tied scans: 1. Direct/scanned choice disagreements: 0. All tied candidates are safe null deletions: True.

- n=100000000, p=200, seed=3, unequal, exact, step=7: tied deletions [[180], [151]]; direct score spread 0; production removes [180], direct scoring removes [180].

Main-grid spot checks have maximum direct/scanned score discrepancy 3.52859497e-05. Tiny ordering gaps can therefore be numerically unresolved. Observed safe deletion and endpoint outcomes are diagnostics of the recorded implementation, not a claim of real-arithmetic path agreement. No alternate full path or high-precision proof is claimed.

Artifacts: N2_precision.py, N2_tie_audit.json, N2_precision_summary.md. Run after N2_simulations.py with python -B. Only N2-prefixed outputs are written.
