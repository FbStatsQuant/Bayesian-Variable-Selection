# W3-POST2 — council diff round C2, seat A (gpt-6-astra, high, Codex) — brief

You are **seat A** of the council for ticket **W3-POST2** (SMC-BVS theory project), in a **diff round** under
`Theory_work/Wave3/PROTOCOL_v4.md` §5.5 (read §5 and the HQ amendments H1–H5 at the top). You reviewed this ticket in
council round C1 on 2026-11-09 (your review: `reviews/C1_council_astra.md`). Since then the lead applied the C1 dispositions and
HQ repaired one step of Claim D(b). You now check only what changed. Work alone: no subagents, no git operations.

**Checkout.** `/home/fb31/BVS-wt/POST2-diff` (branch `theory/W3-POST2-diff` = `origin/main` 3333e0c). Below, paths
are relative to `Theory_work/Wave3/W3-POST2/` in that checkout unless they start with `Theory_work/`.

**Write only** `reviews/C2_council_astra.md` (your review) and, if you run checks, files under `reviews/C2_scratch_astra/`.
Edit nothing else. Run any Python with `python -I`.

## The frozen content
You are reviewing the content frozen as `MANIFEST 96fd83cf3564e3f4a0ff5b98295c79a55868d9192e6987e9d40e936e5ad9541a`
(`reviews/MANIFEST_C2.txt`; 12 ticket files and 4 external sources listed as `#EXTRA`). Before you start, run
`python Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-POST2 Theory_work/Wave3/W3-POST2/reviews/MANIFEST_C2.txt`
from the checkout root; it must print `verify: OK`. If it does not, stop and give `gates=FAIL`.

## Read, in this order
1. Your own C1 review: `reviews/C1_council_astra.md`.
2. The lead's disposition of C1: `reviews/C1_disposition.md`.
3. `reviews/C2_DIFF.md` — what changed since C1, and where it is now. **Read its §1 first:** the exact file state C1
   read is not in git. The diff therefore has two layers: L1 (the C1 dispositions, given as a located inventory, not a
   byte diff) and L2 (the D(b) repair, exact, in the patch). Treat both layers as the diff.
4. `reviews/C2_diff.patch` — `git diff 92f6798 HEAD -- Theory_work/Wave3/W3-POST2` (layer L2). The patch also adds two
   review files by another reviewer (`PC1_postcouncil_diff_sol.md`, `PC2_repair_check_sol.md`). They are record only.
   Do not use their conclusions as premises; check every step yourself.
5. `reviews/C2_DEPENDENTS.md` — for every changed object, the lines inside POST2 that depend on it.
6. The frozen files, **only** at the changed lines (C2_DIFF §3) and at the dependent lines (C2_DEPENDENTS), plus the
   inherited sources those lines cite (the `#EXTRA` files of the manifest; [T03R] =
   `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/W1-T03R/PROOF.md`, [P3] and [P1] = the two `PROOF_v*.tex`
   in the same snapshot tree, [W3P] = `Theory_work/Wave3/W3-POST/STATEMENT.md`).

Do **not** re-read unchanged text except where C2_DEPENDENTS points. You are not asked for a new full review.

## Answer exactly these four questions

**(a) Your C1 findings.** For each finding in your C1 review (all of them, by your own numbering): is it resolved?
Answer `yes` or `no`, with the file:line at HEAD that shows it. One table: `| my C1 finding | resolved | file:line | note |`.

**(b) Does the diff break anything?** In particular: **is the repaired D(b) correct, and are D(b)'s statement and its
uses consistent?** Check it line by line:
- the D3 cutoff chain `lemmas/D_hellinger.md:52-55`, including small fixed p and K < s₀ + j₀ − 1;
- Lemma E0 `lemmas/E_visibility.md:15-20` (statement, proof, and both uses: B = j₀ at `:46`, B = s₀ + j₀ at D3);
- the rest of D3 that depends on the cutoff (`lemmas/D_hellinger.md:55-81`), through the constants C_H, C′_H;
- the statement of D(b) at `STATEMENT.md:112-116` against what D3 proves (hypotheses, constants and their
  dependence, mode of convergence), and every other place that states or uses D(b) (C2_DEPENDENTS lists them);
- the intercept remark `lemmas/D_hellinger.md:84-88` and `STATEMENT.md:117-119`: does "D(a), D(b) hold verbatim for
  h̄_int" follow from what is written, with the same constants?
- the other M-class changes of C2_DIFF §3 (#13 Claim B relation, #14 c₀ < c₁ grid) and the E1(b) → E2, Claim C
  case (iii) and E3.1 dependents.
For each item say: correct / not correct, with file:line and the reason.

**(c) Per-claim table.** `| id | decision |` with ACCEPT / REJECT / NOT-EXAMINED, for every W3-POST2 registry claim:
`W3-POST2:A0`, `W3-POST2:A1`, `W3-POST2:A2`, `W3-POST2:B`, `W3-POST2:C`, `W3-POST2:D`, `W3-POST2:D.D(a)`,
`W3-POST2:D.D(b)`, `W3-POST2:E`, `W3-POST2:E3.1` (rows in `Theory_work/INFRA/registry/claims.tsv`, ticket W3-POST2).
ACCEPT means: your C1 acceptance stands and nothing in the diff or its dependents breaks the claim on this manifest.
REJECT needs a C, S or F finding of yours that names the line. Use NOT-EXAMINED only if you could not decide.

**(d) The verdict line** (below).

## Findings
Tag each finding (v4 §5.3): **C** (correctness: a step is false or does not follow), **S** (statement: the stated
claim differs from what is proved — hypotheses, constants, scope), **F** (fidelity to the coded target / a
hypothesis used but not stated), or **E** (editorial: wording, notation, record, citation form, presentation of
numerics). Only C, S or F block, and only if it names the clause or line and says what fails. **Do not add new E
findings in this round** (you may note that an old E item of yours is unresolved in table (a)). "A stronger theorem is
provable" is not a finding. **If you hold a C, S or F finding of your own, you must give `gates=FAIL`**, whatever
severity you would give it (v4 §5.1).

Also give the six gates (G1 correctness of every changed step, G2 hypotheses used = stated, G3 no hidden assumptions,
G4 cited statuses, G5 constants and rates tracked, G6 coded target), each PASS/FAIL with one line, judged on the diff
and its dependents on this manifest. The score (one decimal, 0.0–10.0) reflects C, S and F only.

---
## Verdict line (mandatory, machine-checked)

You are reviewing the content frozen as `MANIFEST 96fd83cf3564e3f4a0ff5b98295c79a55868d9192e6987e9d40e936e5ad9541a`
(round R2, seat `A`). End your review with exactly ONE line of its own, in exactly this form (no other text on
the line; backticks around it are allowed):

```
COUNCIL-VERDICT round=R2 manifest=96fd83cf3564e3f4a0ff5b98295c79a55868d9192e6987e9d40e936e5ad9541a seat=A score=<x.y> gates=PASS|FAIL
```

- `score` is your overall score (one decimal, 0.0–10.0); `gates=PASS` only if EVERY gate passes on exactly this
  manifest; otherwise `gates=FAIL`.
- Write no other line containing `COUNCIL-VERDICT` (not for an older or newer manifest, not as an example, not in
  prose). If you did not review exactly the content of this manifest, write `gates=FAIL`.
- Quoting the digest elsewhere in the review does not count as a verdict; this line is what CP3 acceptance and
  `manifest.py bind` read, and they refuse a review with zero, several, malformed or contradictory verdict lines.
---

(Round label: this diff round is recorded as round R2 for `manifest.py`, whose verdict format needs `R<k>`; C1 = R1.)

## Output
Save the full review to `reviews/C2_council_astra.md`, in this order: (a) table; (b) item by item; findings (tagged); gates;
(c) table; the verdict line as the last line. Then reply with: the verdict line, the per-claim decisions that are not
ACCEPT, and each C/S/F finding in one line (or "no C/S/F findings").
