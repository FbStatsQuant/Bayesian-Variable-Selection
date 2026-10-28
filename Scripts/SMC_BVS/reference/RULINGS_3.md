# Lead's rulings, round 3 (2026-10-22), on verification round 2 (VERIFY_PART_I_r2.md)

**Verdict of round 2.**
- 13 of the 14 round-1 findings are resolved. G4 (random-draw order) matches the prototype exactly, including the Gibbs step.
- Open: N1 (gap) and N2–N6 (minor). Apply ALL of the following:

| Item | Change |
|---|---|
| N1 (the snap must match the prototype exactly) | **Line ~375:** replace the first two sentences with: "Snap only a forced step. When the step is forced, set the endpoint to min(1, φ+1/T_e); if this value is ≥ 1−10⁻¹², set it to exactly 1 (RC-2, ASSUMPTIONS §17; `cpp/v3_calib.h`, `pilot_next_phi`). Never snap a non-forced bisected endpoint lo. The direct endpoint 1 needs no snap. A snapped forced step still counts in `forced_pilot_steps`." |
| | **Line ~390:** "For each endpoint v about to be appended (the target b or the bisected lo), if v ≥ 1−10⁻¹², set v = 1. Then require v > u and ρ_V(u,v) ≥ 0.90 at the snapped v, append v, and fail if the grid then has more than T_e intervals." |
| | **Settings row "Endpoint snap" (~527):** "A forced pilot floor step or a grid point about to be appended, with value ≥ 1−10⁻¹², becomes exactly 1. Non-forced pilot endpoints are never snapped. Grid checks apply after the snap." |
| | Also correct the RULINGS_2/G3 description in CHANGES.md: the deployed rule is the prototype's RC-2 exactly. |
| N2 | Delete "check strict progress after snapping". |
| N3 | Guide-table lookup: "…then step back while k > 1 and W_{k−1} ≥ u_eff", so the result is the first k with W_k ≥ u_eff (bit-identical to `lower_bound`). |
| N4 | State the prototype's timing procedure (`v3_fit.R`, `v3_time_scores`): time 200 scores at size k* on a timing context built from the first min(p, max(64, k*)) standardised columns. Label it "operational measurement, not a statistical setting". |
| N5 | Match the prototype's coefficients exactly: convolution term 8⌈p/B⌉(K+1)(B+1); exact-branch store term 8(40p+1)(min(K,⌈p/2⌉)+8). Keep M_extra only if the prototype has it; otherwise remove it. |
| N6 | Time-guard checkpoints: after every bridge stage of each island (pilot, diagnostic islands and final run), after each grid construction, and after each local search. |

Update CHANGES.md and the Revision log. Change nothing else.
