# Strategy review — blind proposal brief (binding)

Set by Theory HQ, 2026-11-09, approved by Felipe Bedoya. You are one of two independent blind proposers (one Claude
Fable 5.2, one OpenAI gpt-6-astra). You do not coordinate with the other proposer.

## Why this exists
The SMC-BVS paper needs a consistency theory. A program of theorems has been developed over several waves by other
models. Before spending a large compute budget finishing it, Felipe wants a **fresh, unanchored proposal**: what is the
best package of theorems this paper could aim at? Different theorems, better assumptions, better proof strategies are
all welcome.

## Felipe's goals (binding)
1. **Song & Liang (2015, JRSSB 77(5):947–972) is the template for the story** (posterior consistency, sure screening,
   MAP/HPM selection consistency, misspecification). PDF:
   `C:\Users\felip\.t3\userdata\attachments\647bfd65-83bc-403a-b3b0-0a8352044e7f-588fe83a-5cbe-4a20-8055-1cfbd7c9c936-pdf.pdf`.
2. **Design-agnostic**: theorems under mild, general, reasonable assumptions on X (as in Song–Liang), then consistency.
   No organisation by design families; specific designs are only examples/experiments.
3. **Dimension**: p ≤ n^A for any fixed A (p ≫ n included). Super-polynomial p is out of scope.
4. **Asymptotic** results only (finite-n is not a goal; do not list it as a limitation).
5. **About the method as coded**, not an idealised sampler: SMC-BVS v3.1 (Bayesian variable selection with a
   g/ridge-type marginal likelihood, beta-binomial size prior with size cap K, a block-tempered SMC sampler with an
   exact block start distribution π₀, calibration, islands, a start-mode local search "LS0" and a final local search;
   output = reported HPM, PIPs, evidence). Song–Liang prove nothing about their sampler; we want guarantees for what
   the method outputs, but we are open to any route (e.g. posterior concentration + sampler accuracy, search-based
   discovery, or hybrids).

## What you may read (and only this — do NOT open anything else under Theory_work/ or Docs/Theory/, to avoid anchoring)
- The method: `Theory_work/State_of_Project/sections/02_method.tex` and the notation in
  `Theory_work/State_of_Project/sections/A_notation.tex` (method symbols only); the production code
  `Scripts/SMC_BVS/core/` (R + C++: v3_fit.R, v3_run.R, v3_calib.R, cpp/v3_engine.h, v3_start.h, v3_score.h, ...).
- The Song–Liang PDF; any standard literature you know (cite precisely; do not invent results).

## Deliverable
One file: `Theory_work/Wave2/SR/BLIND_<fable|astra>.md` (about 6–10 pages of Markdown). Contents:
1. **The proposed theorem package** (numbered): for each theorem — precise statement; assumptions, each with why it is
   mild/standard (compare Song–Liang's Conditions 1–5 and the literature); what it buys the paper.
2. **Which part of the method carries the reported-model guarantee** and why (posterior concentration + sampler
   accuracy? search-based discovery from the start mode? both?) — with the main obstacle of each route.
3. **Proof strategy** per theorem: key lemmas, tools from the literature, the hardest step, a risk/difficulty estimate
   (low / medium / high) and what would make it fail.
4. **What not to claim**, and the cleanest honest scope.
5. A one-paragraph **recommendation**: the package you would bet a multi-week proving budget on.
Rules: effort high; no subagents (this must be one coherent view); no git commands; write only your file; state clearly
where you are speculating.
