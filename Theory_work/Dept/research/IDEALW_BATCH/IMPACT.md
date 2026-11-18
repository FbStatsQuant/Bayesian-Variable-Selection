# IMPACT — manifests that hash a file touched by the IDEAL-W⁺ batch (if the patches are applied)

2026-11-16 05:59 CST, against origin/main 967313dd. Search: every `*MANIFEST*`, `INPUTS*` and `DEPS*` file outside
`Scripts/Campaigns` on origin/main (72 files), plus the same names under every `/home/fb31/BVS-wt/*/Theory_work/` and
`/home/fb31/Bayesian-Variable-Selection/Theory_work/`. Each was matched against the 20 touched paths and their current
LF-normalised sha256 (`manifest.py`'s rule; whole-file hashes in LINES_CHECK.md §0). Copies byte-identical to the origin/main
file are listed once.

**Every touched file changes its whole-file sha256**, so every manifest that pins a *current* hash of one of them becomes stale
on apply. No Wave 2 or Wave 1C folder has its own acceptance manifest (`find` finds none under `W2-*`, `C-DLV`, `FINAL`,
`HQ_AUDIT`). D69 therefore does not route the errata to `reviews/ERRATA.md`: no accepted manifest walks C-DLV or FINAL. They are
applied in place as `ERRATUM__*.patch`. Only external (`EXT:`) pins matter.

## Manifests

| # | manifest | pins (touched file → state of the pin) | status of the manifest | needed on apply |
|---|---|---|---|---|
| 1 | origin/main `Theory_work/Wave3/W3-RM2/reviews/MANIFEST_R1.txt` (registry council digest 00bbeab8…) + `MANIFEST_{BT1,LC1,LC2,MP1,PC1,RC1,RC2,RC4,SC1,SL1,SW1}.txt`, `INPUTS.txt` | `EXT:W2-LOC2/STATEMENT.md` = b1c93061…, `EXT:W2-UNI/STATEMENT.md` = a5754a8a… | **ACCEPTED** (R1 = council cell of the W3-RM2 rows) | **none.** Neither pin equals the current origin/main file (LOC2 aa074a55…, UNI 925a9eb3…; both files have one version on origin/main since Wave 2 closed). The pins are already not current, so the batch makes nothing newly stale. This mismatch predates the batch; I flag it for the recorder without touching it. |
| 2 | W3-RM2-R `reviews/MANIFEST_R3.txt` (council R3; also R1, R2 and `INPUTS_R1.txt`), `~/BVS-wt/W3-RM2-R` (theory/W3-RM2-R, not on origin/main) | `EXT:C-DLV/lemmas/L2_degenerate.md` 6d46b556… **current**; `EXT:C-DLV/STATEMENT.md` 464d659a… **current**; `EXT:W2-FAC-A/lemmas/L7_delivery.md` 7b1a9364… **current** | **CP3 accepted by HQ 11-16; acceptance not yet recorded** (recorder tasks U/V after card 14 + HQ GO; QUEUE:58) | If the batch lands **before** the RM2-R record: re-freeze CORRECTION-ONLY as `MANIFEST_R3r.txt` (= R3 with exactly these 3 EXT lines changed; `manifest.py verify` shows 3 differences). Add HQ seat carriers `R3r_record_{sol,opus}.md` citing `Theory_work/Dept/research/IDEALW_BATCH/DIFF_sol.md`; the content is errata + the FAC-A L7 narrow, and DLV-0 already assumes IDEAL-W⁺ / 𝔇 (TR1 §2), so its content is unaffected. If the batch lands **after** the record: the same re-freeze + carriers, plus a council-cell re-point on the RM2-R rows. Precedent: W3-MISR-R `MANIFEST_R3r` + `R3r_record_*.md` (CORRECTION-ONLY, task S, 11-16). **Recommend: bundle with the RM2-R recording (one re-freeze).** |
| 3 | W3-READER `reviews/INPUTS_R1.txt` (line 18: `C-DLV/STATEMENT.md`, path only) | path only, no hash | RUNNING, no READER manifest frozen | none if the batch lands before the READER freeze (the freeze hashes the new file). After it: re-freeze + carrier as in #2. Only an appended amendment note changes; C-DLV's claims are unchanged. |
| 4 | origin/main `Theory_work/INFRA/paper/generated/MANIFEST.txt` (+ older copies in 16 worktrees) | claim-hash prefixes of blocks: W2-FAC-A:Thm-FAC-L 88e789bd…, W2-FAC-A:Prop-F-FAC 121f77a0…, W2-FAC-B:Thm-FAC-CS bc18ab1a…, W2-FAC-X:Thm-FAC-CS-iid b078d360… **change**; W2-FAC-PK:Thm-NEG, W2-LOC2:PLR (unchanged, LINES_CHECK A) | ACCEPTED (generated) | Re-run `assemble.py` after the recorder rehash. Expect exactly 4 block diffs (those four claims), plus any block for rows the recorder adds. |
| 5 | origin/main `Theory_work/Wave3/API_AUDIT/{pass1,pass2,pass3,sharp1}/MANIFEST.tsv` | C-DLV `STATEMENT.md` (pass1/sharp1, current hash); C-DLV `INVENTORY.md` / `L2_degenerate.md`, FAC-B `L5_assembly.md` (old hashes); FAC-B/X/XA/S5 STATEMENT and X10 (several at the current hash) | historical API-audit send records (what was sent, not an acceptance) | none (they record what was sent then; precedent MISR_NARROW IMPACT #4) |
| 6 | DEPS.tsv anywhere (incl. W3-RM2-R `DEPS.tsv`) | no touched path | — | none |

## Carriers (CORRECTION-ONLY precedent)

Only #2 needs a carrier: a re-frozen W3-RM2-R manifest with HQ seat carriers. The precedent is W3-MISR-R
`reviews/MANIFEST_R3r.txt` with `R3r_record_{sol,opus}.md`: "CORRECTION-ONLY; NOT a new review". Each carrier copies its seat's
own per-claim table verbatim and adds one verdict line for the new digest, citing the Sol diff check `IDEALW_BATCH/DIFF_sol.md`
and the WEAKER tags. The 19 batch rows have no manifest-based council cell to re-point. Their council cells cite Wave 2
`reviews/` seat files without a MANIFEST digest. Their re-registration is a NARROW bump: major version, WEAKER, cite `DIFF_sol.md`.

## Same every-n sentence outside the batch (manager's request; not patched)

| claim / text | method paragraph (quoted) | about shipped code? | verdict |
|---|---|---|---|
| **C-DLV:Prop-F** (`C-DLV/lemmas/L4_delivery.md:79-84`; method `:7`, STATEMENT `§0 :11-12`) | "𝔐 = v3.1 + LS0 (STATEMENT.md §0); premises EX-A, EX-S, SR, OP-LS0 (cap ℓ_n = ℓ), e4, GUARD-W, IDEAL-W, MACH, CONFIG, TDP-IMPL"; §0: "**Method** 𝔐 = v3.1 + LS0 as specified (SoP/02_method.tex: … LS0 :490-501 …), R′ = 4k declared (k fixed), LS0 cap ℓ_n = ℓ." | **No.** LS0 is the specified component (INVENTORY section G: "Spec-only components (v3.1 + LS0)"). The specified method has neither `v3.ls0_ell` nor an `int` cap, and IDEAL-W makes its integers unbounded. | **Sweep reading confirmed: not exposed.** The ERRATUM note appended to C-DLV `STATEMENT.md` says so explicitly. |
| **FINAL s6 Proposition F**, corrected form (`FINAL/sections/s6_delivery.tex:29-46`) | ":29 Consider the specified v3.1 method with deterministic LS0 … set LS0's move cap to a_n=ℓ_n+\|S̃₀\| … Assume … IDEAL-W …"; but ":37 *Addition for the C-ENG head code* … for the implementation at `493579a`, whose preflight also charges LS0's worst case … the allocation must in addition satisfy … P̄_LS0 … P_e + A" | **Partly.** The method is the specified one, but the allocation clause is written for the implementation at `493579a`, and that commit carries both validators (`git show 493579a:` → `v3_run.R:96`, `v3_core.cpp:474`). Remark (3) (`:62`) says it is "*not* a reliability statement about the shipped binary". | **Candidate** (not patched; not in claims.tsv). It needs HQ's reading. If the allocation addition makes it a claim about 493579a, then "for every admissible n ≥ 3" needs 𝔇 / A:IDEAL-W⁺ like F-FAC. Otherwise a one-line remark that the head-code addition does not import the head's validators. |
| **FINAL s6 Proposition F-GROW** (`s6_delivery.tex:54-58`) | ":54 Under exactly the method, fallback, premises and allocation of Proposition F (cap a_n=ℓ_n+\|S̃₀\|) … Then, for every admissible n≥3, P(no output)=0, and along each such sequence P(Ŝ=S₀)→1" | Same as Proposition F (inherits its allocation addition for `493579a`). | **Candidate** (with F). |
| A2/A3 (in the batch) | A2 `:9`: "Use the method and premises of A1:62–75 …" = FINAL F's *specified* method, without the 493579a addition | A2/A3's method paragraph is spec-level, like C-DLV's. HQ listed them in the 17, so they are narrowed here (WEAKER, harmless). | Narrowed. The A2/A3 notes record the tension and that A2's allocation lacks A4's preflight terms. **Open item for HQ:** keep the narrowing, or reclassify A2/A3 as spec-level like C-DLV:Prop-F. |

## Summary for HQ

- **Accepted manifests needing re-freeze: none on origin/main.** W3-RM2 R1's LOC2/UNI pins are already not current, which
  predates this batch.
- **Running ticket: W3-RM2-R R3** pins 3 touched files at the current hash. A CORRECTION-ONLY `MANIFEST_R3r` plus 2 HQ carriers is
  needed whenever the batch lands. Best done together with the RM2-R recording.
- **Generated paper manifest:** re-run `assemble.py`; expect 4 block diffs.
- **Candidates outside the batch:** FINAL s6 Proposition F (corrected) and F-GROW, through the `493579a` allocation clause;
  C-DLV:Prop-F is confirmed not exposed. Further registry candidates are in CASCADE.md §2.
