# W2-FAC-PKA request to W2-SIM

HQ authorized NOTS request, 2026-11-09. Do not coordinate or share another parallel proof ticket's findings with PKA. Results requested under Theory_work/Wave2/W2-SIM/results/ with configuration, code revision, raw per-seed data and interpretation. Nonblocking for PKA.

## Priority 1: swap growth and complete-scan discovery, feasible exact Gram

Reuse PKA numerics/n1_exact_grid.py (TableAdapter and run_path) and n2_checks.py controls; FAC-B numerics/cs_core.py, fac_core.py, bvs_core.py. Imports must not rewrite source bytecode. Exact-Gram p MUST be <=n-1; do not bypass assertions. Grid n=800,1600,3200,6400 then 12800/25600 as practical, p=floor(c*n), c=.6,.85,.98; rho=.5 primary, .2/.8 sensitivity. Truth positions (2,26,53,75), coefficients .5*(1.4,1,1.8,1.2), sigma=1. Start from actual capped block DP, not [p], random size-K or oracle start. Preserve and save partition; baseline source partition tie tolerance differs from production and must be labeled. 100 seeds primary if resources permit, 20 pilot; prioritize n-growth over repeats. Dense partition and start DP may need optimized replacements; validate same blocks, scores and selected mode on small cases before scaling. Do not replace DP by greedy allocation without proof/control.

Per seed: |start|, truth inclusion/missing IDs, retained-null mean xi and quantiles; every move (out,in,tag,score), initial consecutive swaps, total null swaps, truth-in/out swaps, additions/deletions; first scan index whose feasible neighborhood contains S0, terminal model, all cap outcomes a=ell+|start| and a'=ell+2|start|. Distinguish scoring from arrival and stopping. Record maximum centre magnitude, first-deletion index, end-of-swap index, and whether swaps reappear after deletions. Compute uncapped path once; infer caps from its scan-prefix only.

Theory-changing outcomes: persistent swaps beyond ell+s0+1 with complete-scan misses motivates proving an asymptotic LS0-route counterexample; bounded swaps or shrinking miss frequency redirects toward original-cap consistency. Arrival after cap does NOT alone imply failure. Additions/repeated exchanges or failure of doubled cap would invalidate a simple two-phase/one-swap-per-null remedy. Every empirical trend remains evidence, not a limit proof.

## Priority 2: singleton-partition diagnostic, explicitly nonproduction

Same exact Gram, s0=1, theta_0=1, c=.6,.85,.98. Use singleton blocks, so capped start can be computed by sorting exact marginal table scores and maximizing prefix score plus log prior over k<=K (ties follow source rule). This is a uniform-partition theory diagnostic, NOT production behavior. Scale n up to 1e5 or 1e6 if O(p) CS scans allow; pilot 20 seeds. Test conjecture initial swaps/log n diverges, and record early centre drift and residual Q. Reuse run_path, replacing only start construction. Also s0=2, theta=(1,-.1), singleton blocks: measure weaker truth exclusion then truth-in swap. Do not combine these results with production partition outcomes.

## Priority 3: actual production core, population-CS p>=n

Generate raw independent rows X_ij=sqrt(rho) f_i+sqrt(1-rho)e_ij, Gaussian noise independent; apply production preprocessing and actual linkage. n=200,400,800,... feasible; p/n=2.5,5 and p=ceil(n^1.25) separately. Primary aligned truth as above, rho=.5. Run merged full method with baseline cap and paired-seed enlarged LS0 cap if switch supports it, final search cap unchanged. Record S0 first-scoring phase (start/tables, SMC, final search, LS0), output/guard status, HPM, local_limit, LS0 move decomposition, computational budgets/calibration/fallback. This tests whether SMC/final search rescues LS0 misses; never extrapolate an exact-Gram theorem into this design. Preserve production commit, R/C++ versions, seed and resource allocation. No production modifications by PKA; any diagnostic instrumentation stays in SIM's authorized area and is disclosed.

Priority may be reduced for resource feasibility; return exact exclusions. PKA proceeds independently and does not wait for these experiments.
