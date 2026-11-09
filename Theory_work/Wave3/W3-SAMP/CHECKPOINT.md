# W3-SAMP · CHECKPOINT (2026-11-09 17:35 CST)

**[Superseded by REPORT.md, 17:20.] Proved (by this seat, unchecked at the time; LC1 running):** all six results of the locked STATEMENT v2 —
Lemma CC (code facts), PC (completed = potential records), MR (identities incl. pre-step RB states given 𝓒),
ST (staying at S₀: any π-invariant kernel leaves S₀ w.p. ≤ o₁; all Gibbs coordinates together ≤ o₁; one round ≤ 19o₁),
Theorem D (draw discovery; exact equality for draws; reported-HPM consequence), Theorem LT♯ (corrected LT for the coded
RB PIPs / pip_primary / MPM / HPM; sup-norm, no factor p, no size control, no rate; premise NC_r), Theorem C (concentrated
bridge: T·δ̄ → 0 ⇒ Ẑ/Z → 1, PIPs/MPM/HPM consistent, any N_e, any frozen schedule; improves T² to T).

**Key findings for HQ.**
1. Main (4676af6) computes **no plain PIP**; W1-N1's `pip_plain` identification is for the frozen v2.2.1 core only.
2. ADJ_opus's "mid-round N1 extension unproved" is already T12 (i.c)/(ii); the conditioning on 𝓒 is a short extension of
   W1-N1 L3 (`lemmas/MR_identities.md`).
3. ADJ_opus Flaw 1 is repaired by Lemma ST (bounded B ≤ 16 is used). Flaw 2 (near-circular premise): NC_r stays a
   computational premise, honestly labelled — it cannot be dropped (trap example), is not necessary (near example), is
   discharged by Theorem C, and is one-sidedly falsifiable from the ledger; no output certifies it.

**Sharpness gate:** ASSUMPTION_MAP.md + boundary numerics done; "better theorem" review BT1 (Astra) running. Flagged
`improvable`: the T factor in C (numerics: E|W−1| decreases in T at fixed δ̄) and NC_r (terminal repair). Candidate
min(T, D⁺) version of C is cheap. HQ decides whether to strengthen.

**Left:** LC1 dispositions → mid-point (Astra) → sweep (Sol) → citecheck → council (Astra high + Opus high, claudeAgent).
Start-mass rate (P-START, PROGRAM item 2) is an **input**, not proved here — coordinate with the item-2 ticket.
