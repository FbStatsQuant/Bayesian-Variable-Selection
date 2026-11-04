# W4-SHARE working notes (branch theory/W4-SHARE)

Started 2026-11-02. Inputs read: PROTOCOL, task file, THEORY_PRIORITIES, W1-T38E (REPORT, PROOF §§1-7),
W3-VT38E REPORT, W1-T24G REPORT, METHODOLOGY_v3 §§3-6, 00_COMMON, T13/T15 STATEMENT.md.

## Plan
1. Exact reduction of the W-count to a branching chain in a varying environment (BPVE); envelope theorem.
2. Oscillation corollary: the cumulative selection loss of a set W over the whole bridge is at most e^{-kappa},
   kappa = d-oscillation between outsiders and W, because sum_t Delta_t = 1 (grid-independent).
3. Sharpness: two-state / C1 analysis (supercritical outsider lineage), threshold log N.
4. BVS instantiation: which W, which outsiders; truth-first ordering; small-p exact numerics.
5. Minimal method change.

## Log (what was done)
- PROOF.md: D4 (space-time potential envelope), D5 (oscillation), G (grid independence), SH (sharpness), X (gate),
  M (no posterior barrier near truth; core proved), PD (start mass x fitness = posterior), assembly B2-W4.
- s0: elementary checks; s1: toys (SH exact, D5 multi-stage, C1 + branching prediction, C1 w/o o, C1 with method grid).
- bvs_core.py: faithful small-p engine (exact scores, blocks, tables, pi0, neighbour graph, full round, resampling).
- s2/s2b: start-masked designs in T03 regime: S0 always scored during the bridge; delivery and LT hold.
- s3/s3b: posterior-barrier design: delivery holds, LT fails, S0 scored only through a rare gate; Prop X tight.
- Self-review of D4/D5/SH/X/M(a)/PD done line by line after writing (see REPORT §6 for what still needs an
  independent reader).
