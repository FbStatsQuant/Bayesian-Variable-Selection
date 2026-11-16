# BRIEF — council diff round R2, seat `opus` (Claude Opus 5.5 on Claude Third, effort high) — after round R1 (PROTOCOL_v4 §5.5)

You are one of the two council seats for theory ticket W3-DIST of the SMC-BVS project, in the **diff round** that
follows round R1. This file is your whole brief. Repo clone: `/home/fb31/Bayesian-Variable-Selection`. Paths below are
relative to the ticket folder `Theory_work/Wave3/W3-DIST/` unless they start with `Theory_work/`, `Scripts/`, `Docs/` or
`Papers/` (then relative to the repo root). **Change no git state. Write exactly one file:** `reviews/R2_council_opus.md` (UTF-8).
Edit nothing else. Start no agents. No cluster jobs. Effort high, not above. Any computation small, `nice`, at most 2
cores. **Do not write any file outside the repo clone and set no TMPDIR.** Prefer inline computation with no files. If
you need scratch files, put them only in `/home/fb31/Bayesian-Variable-Selection/.rc_tmp/W3-DIST-R2-opus/` (inside the
clone, at its root; **never inside the ticket folder**, whose content is frozen, and never in `/tmp`), and delete that
folder at the end. Do not add it to git. Never run a command that asks for an approval: nobody can answer it.

## What happened in round R1
Round R1 reviewed the content frozen as `MANIFEST c7d74e49a9e5a05fb4c9457f6ccf3bb7c83cb85ca00bf49e47d3d8f4a7c8834d`. The seat
`opus` (the same model as you, in another thread) wrote **`reviews/R1_council_opus.md`: this is your own R1 review; read it in
full first.** The other seat's review is `reviews/R1_council_astra.md`; read its findings section too, because the diff answers
both seats. Result of R1: no correctness finding from either seat; each seat failed its gates on one finding of its
own — **R1-astra-01** (kind F: the statuses of Lemmas S, X, X′ lacked "conditional on SOP:TH09") and **R1-opus-01**
(kind S: the gloss on the rate in Theorem DIST-1, consequence (c), let A vary). The lead's disposition is
`reviews/R1_disposition.md`. Editorial findings were moved to `ERRATA.md` and are **not** applied in this round.

## Frozen content of this round
The round is frozen in `reviews/MANIFEST_R2.txt`. Its first line is `MANIFEST c5cd9cdd30ecfe06a39b06ee0aa8b86f70d4b08425a98e9f4d09023de5282ddc`. You may run (from the repo root,
read-only) `python3 -B Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-DIST
Theory_work/Wave3/W3-DIST/reviews/MANIFEST_R2.txt`.

**The diff since R1's manifest is `reviews/DIFFS_R1_to_R2.patch`** (every changed file of the ticket folder, and the one
changed external input). In words:
1. `STATEMENT.md` v1.4.9 → v1.4.10: Theorem DIST-1, consequence (c): the gloss on the rate (one sentence); two changelog
   rows. `lemmas/DIST12.md` v0.2 → v0.3: one sentence of the paragraph "Dependence on the sparsity" after D.4.
   `TARGET.md` §2, row P3: the same gloss. (R1-opus-01.)
2. `REPORT.md` (generated from `REPORT_extra.md` by `mkreport.py`; both are in the diff): the statuses of Lemmas S, V, X, X′
   and Proposition NEC now read "PROVED (by this seat), line-checked, conditional on SOP:TH09", and their registry
   dependency is `SOP:TH09@hyp`; §5 says so; the review trail (§2) has rows for R1 and for the diff check D5; the rate
   field of the DIST-1 block names the fixed parameters. (R1-astra-01, and R1-opus-01 for the rate field.)
3. `DEPS.tsv`: the rows of the edited proof file. `ERRATA.md`: new file (editorial findings E1–E8). `PINS.md`: the version
   label only.
4. **One external input changed:** `Theory_work/Wave3/W3-MISR/STATEMENT.md` received a correction in its line 1
   (changelog) and in its Corollary H (the sentence on the Kullback–Leibler reading, now restricted to a deterministic
   intercept). **W3-DIST does not use that sentence**: it consumes only Lemma R′ (a), (a′) of that file (bridge B0;
   `work/E_bridges/B0.md` quotes its lines 70–72 and 75–77), and the truth in W3-DIST has a deterministic intercept
   (`STATEMENT.md` §0). Check that the lines quoted by `work/E_bridges/B0.md` are unchanged in the frozen file.

## What you decide in this round
You do **not** re-read unchanged text, and you do **not** add editorial findings. Answer exactly these questions:
1. **Is each finding of your own R1 review resolved** by the diff? (State it per finding id. The editorial findings of
   R1 are parked in `ERRATA.md`: check only that each is recorded there.)
2. **Does the diff break anything?** Read every hunk. For each changed object, look at its dependents: Theorem DIST-1
   and its consequences, Theorem DIST-2 (same proof file), reader Theorem A and Corollary C and Theorem DIST-C (which
   use DIST-1, DIST-2), the parity row P3 of `TARGET.md` §2 and the registry blocks of `REPORT.md`. Is the other seat's
   finding repaired correctly, in your judgement?
3. **Two points to confirm by name (required from both seats):**
   (a) **The text of target clause TC3 is unchanged** (`TARGET.md` §5: "Best radius ε_n² = C²M₀ log n/n with
   M₀ = O((1 + s₀^r)(A + 1))") and is still proved as written (`lemmas/X.md` §0, `lemmas/DIST12.md` D.1, D.4).
   (b) **The new gloss — "for fixed (A, σ*², M, M′), ε_n² is of order (1 + s₀^r) log n/n" — is exactly what is proved**: no
   more (nothing is claimed about the dependence of the rate on A beyond the factor in M₀) and no less. The changelog
   row 1.4.10 tags this change EQUAL on TC3 and WEAKER on a descriptive sentence that is not a target clause (A now
   fixed; log p_raw becomes log n): say whether you agree.
4. The six gates, each PASS or FAIL **on this manifest**: G1 correctness of every step; G2 hypotheses used = hypotheses
   stated; G3 no hidden assumptions; G4 imports have adequate status and say what is claimed (conditions on inputs
   below PROVED-CHECKED carried in the statuses); G5 constants and rates tracked; G6 fidelity to the method as coded and
   honesty of scope. For a gate you passed in R1 and that the diff does not touch, you may carry your R1 verdict and say
   so. Tag any new finding C (correctness), S (strength) or F (faithfulness); only these count.
   **You must give `gates=FAIL` if you hold a C, S or F finding of your own, whatever severity you would give it.**
5. The per-claim table for all 20 ids (W3-DIST:DIST-1, DIST-2, DIST-3, DIST-C, Thm-A, Thm-B, Cor-C, H, T, S, V, X, X',
   NEC, P6, B0, B1, B2core, B2, B3): ACCEPT | REJECT | NOT-EXAMINED. For a claim the diff does not touch, carry your R1
   decision; for a claim it touches (DIST-1; S, V, X, X', NEC for their statuses; any dependent you judge affected),
   decide again.

Project convention (owner's rule, not a defect): every result here is asymptotic (n → ∞) unless marked deterministic.

## Output format (in your one file)
```
Verdict summary: one paragraph.
My R1 findings: per id, RESOLVED | NOT RESOLVED (why).
Does the diff break anything: per hunk group (1–4 above), with what you checked.
Named confirmations 3(a), 3(b): CONFIRMED | NOT CONFIRMED, with the reason; agreement with the changelog tag.
Gate table: G1 … G6, PASS or FAIL (say "carried from R1" where that applies).
Per-claim table: | id | decision | for the 20 ids.
New findings (C / S / F only), numbered R2-opus-01, …, with location and repair; or "none".
Overall score: x.y / 10 (C, S and F only; 8.0 or more means acceptable as checked mathematics as it stands).
Checks performed. Not checked.
```

---
## Verdict line (mandatory, machine-checked)

You are reviewing the content frozen as `MANIFEST c5cd9cdd30ecfe06a39b06ee0aa8b86f70d4b08425a98e9f4d09023de5282ddc` (round R2, seat `opus`). End your review with
exactly ONE line of its own, in exactly this form (no other text on the line; backticks around it are allowed):

```
COUNCIL-VERDICT round=R2 manifest=c5cd9cdd30ecfe06a39b06ee0aa8b86f70d4b08425a98e9f4d09023de5282ddc seat=opus score=<x.y> gates=PASS|FAIL
```

- `score` is your overall score (one decimal, 0.0–10.0); `gates=PASS` only if EVERY gate passes on exactly this
  manifest; otherwise `gates=FAIL`.
- Write no other line containing `COUNCIL-VERDICT` (not for an older or newer manifest, not as an example, not in
  prose; do not copy the verdict line of your R1 review). If you did not review exactly the content of this manifest,
  write `gates=FAIL`.
- Quoting the digest elsewhere in the review does not count as a verdict; this line is what CP3 acceptance and
  `manifest.py bind` read, and they refuse a review with zero, several, malformed or contradictory verdict lines.
---

Final message: your answers to questions 1–3, the gate verdicts, the score, any C / S / F finding (short), and the
path of your file.
