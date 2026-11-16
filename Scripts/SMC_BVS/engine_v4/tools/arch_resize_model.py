#!/usr/bin/env python3
"""arch_resize_model.py -- per-stage cost model of one V-1M fit (WP3_ARCH_REVIEW.md, section 8).

Billed core-h of 16 final islands (N = 2,500, T = 120 bridge stages + 8 burn-in + 4 measured rounds, p = 1e6) plus
calibration = 3 island-equivalents, as a function of the start law's mean support size E0 = E_pi0|S|, for three code
states. Every constant below is labelled with its source; the output is an ESTIMATE built from MEASURED anchors.
No dependencies beyond the standard library. Usage: python3 arch_resize_model.py
"""

# ---------------------------------------------------------------------------------------------------------------
# Schedule shape: the share w_t of the population that is still pi_0-like at stage t.
# G0 (MEASURED, real partition and start law, calibrated grids, 16 / 8 islands): w_t = acceptance rate of the
# independence step, normalised by its value at stage 1 (records/G0/stage_2747799 p = 5,000; stage_2747372 p = 10,000).
W_G0_5K = [1.000, 1.000, 0.791, 0.785, 0.591, 0.583, 0.425, 0.300, 0.291, 0.241, 0.206, 0.190, 0.189, 0.180, 0.175, 0.156,
           0.143, 0.122, 0.081, 0.065, 0.003, 0.001] + [0.0] * 14
W_G0_10K = [1.000, 0.952, 0.885, 0.851, 0.815, 0.800, 0.790, 0.763, 0.725, 0.695, 0.641, 0.579, 0.456, 0.208, 0.009, 0.002,
            0.001] + [0.0] * 11
# Stand-in bridge at 1e5 (MEASURED, Owls, pilot rule with floor 1/30): w_t = (mean |S|_t - 5.8) / (24.13 - 5.8).
S_1E5 = [24.13, 23.45, 22.91, 22.48, 21.57, 20.88, 20.09, 18.99, 17.81, 16.71, 15.38, 13.94, 12.70, 11.79, 10.94, 9.78, 8.32,
         6.91, 6.25, 5.85, 5.64, 5.56, 5.59, 5.80, 5.76]
W_1E5 = [max(0.0, (s - 5.8) / (24.13 - 5.8)) for s in S_1E5]
PROFILES = {"G0 5k grid": W_G0_5K, "G0 10k grid": W_G0_10K, "1e5 stand-in bridge": W_1E5}

T_BRIDGE, ROUNDS_TERMINAL = 120, 12          # plan: precise fit, T ~ 120, L = 8, Hm = 4 (FEASIBILITY section 0)
STEPS_PER_ROUND = 2500 * (1_000_000 + 16)    # N (p + B + 2)
ISLANDS, CALIB_EQUIV = 16, 3                 # manager: calibration ~ 3 island-equivalents (H = 512, D-1 / D-26)
S_LATE = 6.0                                 # mean |S| in late rounds (MEASURED, every 1e6 run: 6.0-6.1)
NS_PER_WALL_S = 96 / STEPS_PER_ROUND * 1e9   # one second of wall of a 96-CPU island, in ns CPU per step (38.4)

# ---------------------------------------------------------------------------------------------------------------
# Per-step costs, ns CPU (SPR, 96 threads on one socket).
def m0_of(e0, m_late):
    # sweeps per particle-round of a pi_0-like population: 1 + 0.37 E0 (MEASURED on the stand-in: M 10.1 at E0 = 24,
    # 21-22 at E0 = 56), never below the late value
    return max(m_late, 1.0 + 0.37 * e0)

def pair_today(k):
    # today's code, ns CPU per (support, label) pair without check and compaction.
    # k = 6: 164 = 180 (MEASURED, job 2749483 `check`, round 5) minus the round's compaction (1.67 s = 16 per pair);
    # k = 55: 790 (MEASURED, job 2749483 early stage 3, reference: (phase A 9.16 s + phase B 0.92 s) x 96 / 1.251e9
    # pairs = 774, + build 15). Linear in k between the two (ESTIMATE).
    return 164.0 + (790.0 - 164.0) * (k - 6.0) / 49.0

CHECK_PER_STEP = 5.72 * NS_PER_WALL_S        # MEASURED: `ref` 23.90 s vs `check` 18.18 s per round (job 2749483)

def step_levers(k, m, offers):
    # levers 1-3 (check off the step path, bounded scoring, Gram rows), ns CPU per step without compaction.
    # Anchors (MEASURED, job 2749483): late round `gram` 11.77 s = 452 per step at k = 6, M = 3.89; early stage 3 `gram`
    # at k = 55, M = 20: phase A 1.40 s x 96 / 6.4e7 steps = 2,100 (products 37.2 thread-s = 580, flips 1,520), build
    # ~ 300 (1,274 support builds of ~ 15 ms), phase B 0.84 s = 1,260 at ~ 0.6 offers per step.
    flips = 142.0 + (1500.0 - 142.0) * (k - 6.0) / 49.0          # ~ 1.4 flips per step at every stage; cost grows with k
    products = 92.0 * (m - 1.0) / 2.89                           # one new Gram row per state change
    build = 300.0 * (m / 20.0) * (k / 55.0) ** 3                 # k deletion scores per sweep
    phase_b = 60.0 + offers * 2000.0                             # consumption + the store-offer path (ESTIMATE split)
    fixed = 85.0                                                 # orders 65, walk 20
    return flips + products + build + phase_b + fixed

def compaction(k, offers, per_merge_fix=0.0):
    # ns CPU per step of top-store compaction: (offers per stage / staged entries per compaction) x seconds each.
    # 1.15e7 staged entries per compaction and 1.6 s each at stored |S| 6-8.5 are MEASURED (jobs 2748756 / 2749328: 355e6
    # offers, 31 compactions, 48.8 s). The growth with the stored model size is an ESTIMATE: half of the 1.6 s is taken as
    # proportional to the entry size (26 + 4k bytes).
    merges = offers * STEPS_PER_ROUND / 1.15e7
    seconds = 0.8 + 0.0146 * (26.0 + 4.0 * k) - per_merge_fix
    return merges * seconds * NS_PER_WALL_S

O_LATE = 0.005   # offers buffered per step in late rounds (MEASURED: 12e6 per round, jobs 2748756 / 2749328 / 2749483)

def step_cost(state, k, m, offers, calibration, fix=0.0):
    if state == "today":
        c = m * pair_today(k) + CHECK_PER_STEP + compaction(k, offers)
        # serial leader compaction in calibration islands: MEASURED 157 s for 355e6 offers and 39 s for 180e6 (job 2749483,
        # leaders island, rounds 1-2): 0.22-0.44 us of wall per top-store offer
        if calibration: c += offers * STEPS_PER_ROUND * 0.33e-6 * NS_PER_WALL_S
        return c
    # levers 1-3; in calibration islands the leader stores with parallel compaction (O3): two stores of half the
    # capacity ~ one more top-store compaction (ESTIMATE)
    return step_levers(k, m, offers) + compaction(k, offers, fix) * (2.0 if calibration else 1.0)

def island(state, e0, m_late, w, o_fresh, calibration=False, fix=0.0):
    """(sum over the island's 132 rounds of ns CPU per step, mean M over the rounds)."""
    m0 = m0_of(e0, m_late); total = 0.0; msum = 0.0
    reps = T_BRIDGE / len(w)   # the grid refinement keeps the distribution of stages over phi
    floor = state == "floor" and not calibration          # offers below calibration's cut-off are dropped (final islands)
    for wt in w:               # bridge stages
        k = S_LATE + (e0 - S_LATE) * wt; m = m_late + (m0 - m_late) * wt
        total += reps * step_cost(state, k, m, O_LATE if floor else o_fresh, calibration, fix); msum += reps * m
    total += ROUNDS_TERMINAL * step_cost(state, S_LATE, m_late, O_LATE, calibration, fix); msum += ROUNDS_TERMINAL * m_late
    return total, msum / (T_BRIDGE + ROUNDS_TERMINAL)

def fit_core_h(state, e0, m_late, w, o_fresh, fix=0.0):
    """(fit, final islands, calibration, mean M) in billed core-h."""
    isl, mbar = island(state, e0, m_late, w, o_fresh, False, fix)
    cal, _ = island(state, e0, m_late, w, o_fresh, True, fix)
    to_h = STEPS_PER_ROUND * 1e-9 / 3600.0
    return (ISLANDS * isl + CALIB_EQUIV * cal) * to_h, ISLANDS * isl * to_h, CALIB_EQUIV * cal * to_h, mbar

O_CENTRAL, O_BRACKET = 0.03, (0.01, 0.03, 0.10)
# Offers buffered per step in a bridge stage: the least known input (ESTIMATE). MEASURED analogues: 0.14 / 0.07 / 0.03 / 0.01
# in rounds 1-4 of the phi = 1 transient at N = 2,500 (jobs 2748756, 2749328); 0.18 per step = 1.1 store capacities per
# stage on the 1e5 bridge at N = 256, i.e. 39% of a fully fresh stage's c (1 + ln(n / c)); the same share at N = 2,500,
# 1e6 is 0.03 per step (2 capacities per stage).
STATES = (("today", "today (be24e9d)", 0.0), ("levers", "levers 1-3", 0.0), ("levers", "levers 1-3 + sort fix (m3)", 0.9),
          ("floor", "+ offer floor (with m3)", 0.9))

if __name__ == "__main__":
    plan = 600.0 * (T_BRIDGE + ROUNDS_TERMINAL) * STEPS_PER_ROUND * 1e-9 / 3600.0
    print(f"plan: 600 ns CPU per step x 132 rounds = {plan:.0f} core-h per island; H-10: 1,188 core-h per fit")
    print(f"late anchors: today {3.89 * pair_today(6) + CHECK_PER_STEP + compaction(6, O_LATE):.0f} ns CPU per step (MEASURED 918), "
          f"levers 1-3 {step_levers(6, 3.89, O_LATE) + compaction(6, O_LATE):.0f} (MEASURED 452)")
    for m_late in (3.9, 5.5):
        print(f"\n== late M = {m_late} ({'stand-in at 1e6' if m_late < 5 else 'G0, real data at 5k-10k'})")
        print("E0   state                        fit core-h: central [low, high]   x H-10 | 16 islands  calibration | mean M | pi_0-like stage, ns CPU per step: kernel + compaction")
        for e0 in (10, 25, 56):
            for state, label, fix in STATES:
                vals = [(fit_core_h(state, e0, m_late, w, o, fix), o) for o in O_BRACKET for w in PROFILES.values()]
                central = [v[0] for v in vals if v[1] == O_CENTRAL]; n = len(central)
                c = [sum(v[i] for v in central) / n for i in range(4)]
                lo = min(v[0][0] for v in vals); hi = max(v[0][0] for v in vals)
                m0 = m0_of(e0, m_late); o_e = O_LATE if state == "floor" else O_CENTRAL
                kern = (m0 * pair_today(e0) + CHECK_PER_STEP) if state == "today" else step_levers(e0, m0, o_e)
                print(f"{e0:<4d} {label:<28s} {c[0]:7.0f} [{lo:6.0f}, {hi:6.0f}]   {c[0] / 1188.0:4.1f}   | {c[1]:7.0f}   {c[2]:7.0f}    | {c[3]:4.1f}   | {kern:7.0f} + {compaction(e0, o_e, fix):5.0f}")
    print("\nmean pi_0-like share over the stages:", {n: round(sum(w) / len(w), 2) for n, w in PROFILES.items()})
    print("sensitivity (E0 = 25, late M = 3.9, levers 1-3 + m3), fit core-h by stage profile at the central offer rate:",
          {n: round(fit_core_h("levers", 25, 3.9, w, O_CENTRAL, 0.9)[0]) for n, w in PROFILES.items()})
