# W3-VT38E working notes (referee of W1-T38E)

Source under review: branch `origin/theory/W1-T38E`, commit 436a712, folder `theory_campaign/W1-T38E/`
(BRIEF.md, REPORT.md, PROOF.md, scripts/*.py). The W1 `*.out` files cited in its REPORT are NOT in the branch
(`.gitignore` line 20 ignores `*.out`), so W1's numerical evidence is only reproducible by rerunning its scripts.
All outputs of this run are saved as `scripts/*.txt` for that reason.

## Engine/spec facts checked (Scripts/SMC_BVS/core/cpp, METHODOLOGY_v3.md)
- Round: Fisher-Yates uniform permutation of the m = p+B+2 labels, fresh per particle and round (`draw_order`, `one_round`). Matches D2 step 5.
- Gibbs: heat bath o_j = a/(1+a); addition at |S| = K excluded (o_j = 0, flipped config not evaluated); flipped configuration evaluated (`eval(tmpQ, ME_GIBBS_FLIP)`), current state recorded as held (SR). Matches Lemma A and D2.
- Ledger: every fresh evaluation is offered to the HPM running best (`Ledger::event` -> `offer_stores`). Cache hits were offered when first scored. So "evaluated" = "scored".
- Island: N iid pi0 draws, each evaluated (ME_INIT) -> scored; stage = reweight exp(dphi*d), multinomial resample, one round at phi_new; then L burn-in + Hm = 4 measured rounds at phi = 1, no reweighting/resampling. Matches D3 and T38(b)-R step (5).
- Pilot rule `pilot_next_phi`: phi'=1 if ESS(1-phi) >= 0.9H; else 60 bisections on (phi,1], lo passes by construction; if lo-phi < 1/T_e then phi' = min(1, phi+1/T_e), forced. ESS = (sum w)^2/sum w^2 on the current (unweighted) population. Matches D2 step 2.
- Pilot: `cpp_cal_pilot` with H = budgets$tiers$H[tier+1], T_e likewise.
- Local search: up to ell moves, then one more scan; strict F improvement; lexicographic ties; scans flips (j = 1..p) then swaps. Matches E3 / TD'.
