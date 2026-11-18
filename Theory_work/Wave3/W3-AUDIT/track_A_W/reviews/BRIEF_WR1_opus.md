# BRIEF — council round W-R1, seat `opus` (Claude Opus 5.5 (high)) — blind first read — W3-AUDIT track A_W: W1 (ISL), W2 (FRZ)

You are one of the two council seats for two Tier B key-lemma items of W3-AUDIT track A_W (SMC-BVS project). Work only
inside `/home/fb31/BVS-wt/W3-AUDIT`. **Change no git state. Write exactly one file:**
`Theory_work/Wave3/W3-AUDIT/track_A_W/reviews/WR1_council_opus.md`. Edit nothing else; start no subagents.

## Frozen content
`Theory_work/Wave3/W3-AUDIT/track_A_W/reviews/MANIFEST_WR1.txt`, first line `MANIFEST 0b8b93aa57f48dee848d20f70b19f9f4f11933b647557a523c2cf62be14c3aea`; verify with
`python3 -B Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-AUDIT/track_A_W Theory_work/Wave3/W3-AUDIT/track_A_W/reviews/MANIFEST_WR1.txt`.

## Files you may read
`Theory_work/Wave3/W3-AUDIT/track_A_W/W1_ISL/` and `.../W2_FRZ/` (`STATEMENT.md`, `PROOF.md`, `CITECHECK.txt`), and
`.../track_A_W/citecheck.py`; the external inputs listed in `reviews/INPUTS_WR1.txt` (pinned code `Scripts/SMC_BVS/core/` at
4676af6; the older steps `Theory_work/Wave1/W1-N1/lemmas/L1_bridge.md`, `L3_freezing.md`, W1-N1 `STATEMENT.md` §2; T12's
freezing lemma; the consumers `Theory_work/Wave3/W3-SAMP/STATEMENT.md`, `lemmas/D_theorem.md`, `lemmas/MR_identities.md`;
the sibling statements T1, T4–T7, FR, C1, already council-checked, not under review). **Do not read** `INDEX.md`, `LOG.md`,
any `CHECK.md`, `CHECKPOINT_*.md`, `API_CARD/`, any other file in any `reviews/` folder, or anything else in
`Theory_work/Wave3/W3-AUDIT/`: blind first read.

## What the council decides
- **W1 (ISL)** — at the code of record, for final island r and every calibration value c in the success set, on the
  potential run: (ISL-0) the island record (incl. every π₀ draw) is a function of (c, data, uniforms read); (ISL-st) every
  operation starts at a bounded stopping time and reads fresh i.i.d. uniforms, with the stated bounds and the draw count
  D_r(c) = N_e(1 + T + L + 4); (ISL-d) the record is jointly measurable with Polish values, and every coordinate the
  consumers use is a measurable function of (c, record). This discharges `W1-N1:B` (B-0), the control-flow clause of (B-b)
  and (B-d) as `W3-SAMP:D` and `W3-SAMP:MR` use them.
- **W2 (FRZ)** — (FRZ-a) the freezing lemma; (FRZ-b) its hypotheses hold at the code (SI, A₀ with E₀ = {𝓒° ∈ A₀},
  O_r = Φ(𝓒°, U_r)); (FRZ-c) conditioning on the calibration record at general c, covering `W1-N1:F`, `W3-SAMP:MR`'s
  extension (Steps 2–4) and `W3-SAMP:D`'s freezing step, with the potential pair (𝒜°, 𝓒°) and T5's transfer rules for the
  actual pair; (FRZ-d) the evidence bounds.
You are briefed to break them. Gates (a gate PASSes only if you hold no C, S or F finding for it): G1 correctness of every
step and code citation; G2 hypotheses used = stated; G3 no hidden assumptions; G4 imports and statuses verbatim; G5 scope
(potential vs actual pair, executed settings, streams, islands); G6 fidelity to the code as pinned and to the re-checked
older steps and the consumers' uses. You **must** give `gates=FAIL` when you hold a C, S or F finding of your own. Tag
findings C / S / F / E (E never blocks).

## Output (your one file)
Verdict summary; gate table G1–G6; claim table `| id | decision |` for W1, W2 (ACCEPT / REJECT); numbered findings with
file:line and repair; overall score x.y / 10 (C, S, F only); checks performed; not checked. End with exactly ONE line of its
own:
```
COUNCIL-VERDICT round=R1 manifest=0b8b93aa57f48dee848d20f70b19f9f4f11933b647557a523c2cf62be14c3aea seat=opus score=<x.y> gates=PASS|FAIL
```
Write no other line containing `COUNCIL-VERDICT`. If you did not review exactly this manifest's content, write `gates=FAIL`.
