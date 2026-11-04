# The final method for paper 1: SMC-BVS v3.1 (plain-language summary for Felipe)

HQ, 2026-11-04. Approved by HQ after the method meeting (MEET-v31), two independent reviews (Sol 6.1: a proof check and an audit), and the N9 kernel check. Full detail: `METHOD_v3.1_FINAL.md` (as amended by `AMENDMENT_HQ_01.md`), branch `theory/MEET-v31`.

## 1. What the method is

**v3.1 is the v3 study method, unchanged as a statistical method,** plus a parallel execution layer and some extra outputs. Unchanged:
- your target posterior: g = n, τ = 1, IG(0.01, 0.01), Beta-Binomial(1, p), cap K = min(p, ⌊n/2⌋);
- the local-to-global start: correlation-clustered blocks, each enumerated exactly, multiplied into the start π₀;
- the SMC tempering bridge from π₀ to the exact posterior, with its moves;
- calibration, budgets and the HPM decision;
- the unbiased evidence estimate Ẑ.

**What v3.1 adds:**
1. **Parallel layer, over islands and scans, never over variables.**
   - The final islands, the calibration's diagnostic islands, the local-search scans and the block tables run concurrently.
   - The output is identical, bit for bit, to the serial run. This was checked on 3 of 3 study designs, at about 1.9× speed with 2 cores.
2. **Optional stacking.** More islands can be added at the same per-island size, declared before the run.
3. **LS0.** One extra local search from the start's mode. It changed none of the 2,394 study best models, and it is what makes one selection-consistency theorem true of the shipped method.
4. **New reporting.**
   - The **Ẑ-weighted PIP is now the primary PIP**, because it is the one with a consistency theorem as islands grow. The equal-weight PIP is secondary.
   - An estimator for joint summaries: pair inclusion and model size.
   - A **certificate card**: one-sided guarantees the run reports about itself. For example, if Ẑ is below the total score of the stored models, the evidence is certainly underestimated.
   - Explicit NA fields when a run stops without output.

**The 2,400-fit study is not re-run.** It stands as v3.1 with 4 islands. The new PIP and the certificate card are computed from saved outputs. The one exception is joint summaries: they need a small new run, because those particles weren't saved.

## 2. Local-to-global: kept, and what the data say

- **Arms tested:**
  - A: block start;
  - B: single-variable blocks;
  - C: start from the prior.
- **Pre-registered result: "keep, no cost claim".** The rule's design was flawed: the prior start's poor evidence made every design inconclusive.
- **Descriptive findings**, 12 designs × 1 seed:
  - Arm C's evidence is **certifiably too low on 10 of 12 designs**: Ẑ falls below a model score the run itself found, which is a lower bound on Z. Arms A and B never are.
  - Arm B matched A's evidence but cost more, sometimes over 4 h against 10–28 min.
- **Confirmatory test (done, 2026-11-04; `theory/ABL-CONF` REPORT.md).** 118 fits, 3 designs × 10 seeds, rule fixed and dry-run in advance.
  - **Licensed:** at equal declared budgets the prior start underestimates the evidence on all three designs, by 6–13 nats in median. The block start does not.
  - **Cost, per design:**
    - on the correlated design S5, the block start reached the same accuracy as single-variable blocks at about 30% less cost (10/10 paired wins);
    - on the masked design S4, single-variable blocks never finished within 75 min (0/10), while the block start finished 9/10;
    - on the favourable design S1, the two cost the same.
  - Because the cost claim had to hold on every design, the overall cost claim is formally "inconclusive". The per-design results may be reported as pre-registered results.

## 3. Generality in (n, p): your rule

Every setting is in one of four classes:
- a fixed modelling convention with a reason;
- an explicit function of n, p or X;
- a declared compute budget, which changes cost and never the target;
- a machine-precision tolerance.

Nothing is tuned to the study. No separate p ≪ n / p ≫ n rule is needed:
- the block size uses √p when p < n and √n when p > n;
- the cap K only binds when p > n/2;
- small problems are enumerated exactly (every p when n ≤ 5, and every n eventually at fixed p).

The weak spot: some budgets are fixed numbers (2,500 particles floor, 4 islands, ESS 0.90). They never affect correctness, but an asymptotic theorem may need them to grow. You approved letting the theorem meeting turn them into explicit growth rates in n and p if a theorem requires it.

## 4. Limitations stated in the paper (each proved, or true by definition)

1. Each Gibbs round has p + B + 2 sequential steps. This is inherent to the kernel; parallelism is over particles and islands.
2. Each worker needs scoring access to all predictors. A private p × p Gram per worker is *not* inherent.
3. Any product start built from block-local scores can be masked by cross-block correlation. The bridge exists to correct this.
4. No diagnostic computed from the run's own weights has a universal guarantee of detecting a never-visited mode. The certificate card still detects some failures.
5. The properties of Ẑ behind the 95% lower bound imply no two-sided relative-error bound.
6. Selection accuracy at n = 200 is limited by the data, not the sampler: in at least 565 of 2,394 fits a scored competitor strictly beats the true model.
7. The cap K excludes truths larger than K, and a fixed compute allocation cannot support unlimited (n, p). Both are true by definition.

Unproved properties are **not** called limitations: rebuild convergence, delivery probability, mixing rates, weak-dependence stability and others are theorem obligations.

## 5. What the independent reviews changed

They checked 73 claims. Most held. The fixes were all wording or bookkeeping; **no method decision changed:**
- An argument against the backfit start was withdrawn. The start is still rejected: it would need a full re-run, it has no exact sampler with a known normaliser, and it has no theorem.
- A "PIP Monte Carlo SD ≤ 0.01" claim was downgraded to a budget, not a guarantee.
- A false local-search bound and a false "no upper bound on Z" limitation were corrected.
- A bug in the item-1 rule script was fixed. The outcome is the same.
- **New safeguard:** if a theorem behind one of your mandatory proposal goals (§5.1–5.4, §13.1) fails, it comes back to you. It is never silently dropped.

## 6. Kernel validity (N9): checked

Every move, the random-order round and the start sampler were proved valid and verified exactly on the production code. Removing a Hastings factor makes the check fail, as it should. This was the last gate: **no open method questions remain.**
