# W3-DIST — blind read S1 (statement lock + break + better theorem) — gpt-6-astra, codex, reasoningEffort high

You are an independent reviewer. Repo clone: `/home/fb31/Bayesian-Variable-Selection`. **Read-only on everything except
your one output file `Theory_work/Wave3/W3-DIST/reviews/S1_astra.md`.** Run no git command that changes state. Start no
agents. Do not read any other file under `Theory_work/Wave3/W3-DIST/reviews/`, nor `LOG.md`, `CHECKPOINT_*.md` or
`BRIEF.md` of that ticket.

## What is under review
Candidate theorem statements (nothing is proved yet) for a Song–Liang (2015, JRSS-B 77(5)) Theorems 1–2 analog:
Hellinger consistency, for the joint (x, y) law under a random design, of (i) the exact posterior of a specific coded
Bayesian variable-selection model and (ii) distributions built from what the coded sampler returns.
Frozen manifest: `Theory_work/Wave3/W3-DIST/reviews/MANIFEST_S1.txt` — quote its digest (first line) in your report.

Files you may read (and only these, plus the manifest):
- `Theory_work/Wave3/W3-DIST/STATEMENT.md`, `ROUTES.md`, `ASSUMPTION_MAP.md`, `DEPS.md`, `PLAN.md`
- `Theory_work/Wave3/W3-DIST/work/prior_probe/REPORT.md`, `Theory_work/Wave3/W3-DIST/work/numerics/RESULTS.md`
  (helper outputs; unchecked — treat as evidence to test, not as facts)
- every file listed in `Theory_work/Wave3/W3-DIST/reviews/INPUTS.txt` (the Song–Liang PDF: read journal pp. 950–956,
  i.e. PDF pages 4–10; the in-sample input results; the pinned code).

## Your job: break the candidate statements
For each of Theorems DIST-1, DIST-2, DIST-3, DIST-C and Lemmas H, T, X, X′, S, P6 in STATEMENT.md:
1. **Counterexample as stated?** Try to construct one (a design law, a truth, a data configuration). Pay special
   attention to: (a) Lemma T — is a distribution-free bound of this exact form true (check the level-set class, the
   relative-deviation inequality invoked, the integration over levels, constants, and whether dropped constant columns
   and the data-dependent intercept/standardisation are really covered); (b) Lemma H; (c) DIST-1's claim that the inner
   threshold can be e^{−ct} with only (E), (C), (ND) — look for a design satisfying (ND) on which a set of
   Hellinger-far models keeps posterior mass ≥ n^{−c}; (d) the cutoff m_n(t) and Lemma S with the data-dependent
   inverse-gamma rate b₀s_y² and models of size up to n/2; (e) DIST-2 without any design condition; (f) DIST-3's (TR₀).
2. **Missing assumption?** Name any hypothesis the route in ROUTES.md silently uses (e.g. s₀ ≥ 1, s₀ ≤ K, p ≥ 2, a true
   column constant in-sample, t-range, measurability/independence of ε and X, dependence of constants on n).
3. **Does (ii) overclaim what the code returns?** Check the code pins in STATEMENT §2 against the code files, and
   whether "store BMA", "HPM plug-in", "MPM plug-in" are honest descriptions; whether (C-i)–(C-iv) claim anything the
   cited results (W3-SAMP D, LT♯, C, TR; M4(c)) do not deliver.
4. **Comparison with Song–Liang.** Is each "matches / beats / short" reading implied by STATEMENT fair? In particular
   the reading that their conditions (9), (10) fail for the coded prior and (11), (14) hold; the rate comparison with
   their Corollary 1 at P_n = n^A; and whether their Theorems 1–2 really need no eigenvalue/identifiability condition.
5. **Better theorem.** Propose, if you can, a strictly better statement that looks provable by the routes in
   ROUTES.md or another route you describe (weaker assumptions, better rate, exponential form in more cases, a
   cleaner coded-output statement). Say what you would drop or add.

## Output (`reviews/S1_astra.md`)
- First line: `S1 blind read — manifest <digest>`.
- Findings, each: id, severity (CRITICAL / MAJOR / MINOR / NIT), the statement concerned, the argument or
  counterexample in full, and the minimal repair.
- A verdict per statement: SOUND-AS-STATED (as far as you can see) / REPAIRABLE (say how) / FALSE-AS-STATED.
- Section "Better theorem": your proposals, each with a one-paragraph provability argument.
- Final line: overall verdict for a proof leg: GO / GO-WITH-REPAIRS / NO-GO, and one sentence why.
Do not soften findings. If you could not check something, say exactly what and why.
