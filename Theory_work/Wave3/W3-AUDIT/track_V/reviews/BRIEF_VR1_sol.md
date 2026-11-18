# BRIEF — council round V-R1, seat `sol` (Codex gpt-6.1-sol (high)) — blind first read — W3-AUDIT track V: V1 (Lemma VIS)

You are one of the two council seats for one Tier B key lemma of W3-AUDIT track V (SMC-BVS project). Work only inside
`/home/fb31/BVS-wt/W3-AUDIT`. **Change no git state. Write exactly one file:**
`Theory_work/Wave3/W3-AUDIT/track_V/reviews/VR1_council_sol.md`. Edit nothing else; start no subagents.

## Frozen content
`Theory_work/Wave3/W3-AUDIT/track_V/reviews/MANIFEST_VR1.txt`, first line `MANIFEST c271cfac4cb87cdd05448fd54f9f83ee217390294cdf6844338ab30b210b7e98`; verify with
`python3 -B Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-AUDIT/track_V Theory_work/Wave3/W3-AUDIT/track_V/reviews/MANIFEST_VR1.txt`.

## Files you may read
`Theory_work/Wave3/W3-AUDIT/track_V/V1_VIS/` (`STATEMENT.md`, `PROOF.md`, `CITECHECK.txt`) and `.../track_V/citecheck.py`;
the inputs `Theory_work/Wave3/W3-AUDIT/TRACK_B.md` (dossier B8, lines 209-233) and `Theory_work/Wave3/W3-AUDIT/track_C/RESULTS.md`;
the theorems the lemma serves, read with git: `git -C /home/fb31/BVS-wt/W3-AUDIT show origin/main:Theory_work/Wave3/W3-READER/READER_VERSIONS.md`
(Theorem 5: lines 565-600; Theorem 6: 660-700; Theorem 10: 1282-1295) and
`git -C /home/fb31/BVS-wt/W3-AUDIT show origin/main:Theory_work/Wave3/W3-READER/NOTATION.md` (lines 155-175).
**Do not read** `INDEX.md`, `LOG.md`, `CHECK.md`, `CHECKPOINT_*.md`, any other file in `reviews/`, or anything else in
`Theory_work/Wave3/W3-AUDIT/`: blind first read.

## What the council decides
**V1 (Lemma VIS)** — population visibility |Cov(W_j, Wᵀθ* | W_U)| ≥ a for all j ∈ S₀, all U ∌ j with |U| ≤ 15, with a
**uniform in n**: (VIS-0) reduction to ⟨γ(U, j), ϑ⟩ with Var(W_j | W_U) ≥ c₁₆; (VIS-a) sign route (DΣ⁻¹D with nonpositive
off-diagonals, truths aligned within components) with a = θ_lo·c₁₆; (VIS-b) generic route |vis| ≥ c₁₆·dist(ϑ, B) with B
the fixed closed union of hyperplanes over the closure of all local visibility directions (all n), a = c̲·δ; (VIS-c) B
null and nowhere dense for countably many local patterns; (VIS-d) block/factor/equicorrelation designs with finitely many
types and stationary designs with r(d) → 0; (VIS-e) instances (IND, AR(ρ) of either sign, equicorrelation ρ ≥ 0, one
factor, blocks). The binding requirement (owner): a margin uniform in n, not merely "nonzero for almost every θ" at each n.
You are briefed to break it (small explicit matrices are welcome). Gates (a gate PASSes only if you hold no C, S or F
finding for it): G1 correctness of every step; G2 hypotheses used = stated; G3 no hidden assumptions; G4 the theorems'
visibility hypotheses and notation quoted faithfully; G5 scope (uniformity in n, n ≥ n₀, positive definiteness, which
designs); G6 fidelity of the examples and of the design statements to B8 and track C. You **must** give `gates=FAIL`
when you hold a C, S or F finding of your own. Tag findings C / S / F / E (E never blocks).

## Output (your one file)
Verdict summary; gate table G1–G6; claim table `| V1 | ACCEPT/REJECT |`; numbered findings with file:line and repair;
overall score x.y / 10 (C, S, F only); checks performed; not checked. End with exactly ONE line of its own:
```
COUNCIL-VERDICT round=R1 manifest=c271cfac4cb87cdd05448fd54f9f83ee217390294cdf6844338ab30b210b7e98 seat=sol score=<x.y> gates=PASS|FAIL
```
Write no other line containing `COUNCIL-VERDICT`. If you did not review exactly this manifest's content, write `gates=FAIL`.
