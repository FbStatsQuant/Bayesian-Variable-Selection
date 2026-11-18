# IMPACT — manifests that hash W2-UNI `lemmas/L5_delivery.md`, and F-UNI's dependents (if the v2 narrow is applied)

Run on 2026-11-16 at 05:48 CST.

**Search.** Three passes, each for every `*MANIFEST*`, `INPUTS*` and `DEPS.tsv` that names `W2-UNI/lemmas/L5_delivery.md` or
contains its current sha256 `9b50e358…c056`:
- `git grep` on origin/main 967313dd;
- `grep -r` over `/home/fb31/BVS-wt/*/` (20 worktrees, 84 hits);
- `grep -r` over `/home/fb31/Bayesian-Variable-Selection/Theory_work/Wave3/W3-DIST/` (0 hits).

**What the search found.**
- No DEPS.tsv names the file.
- W2-UNI has no manifest of its own. Its council cell is "Astra 9.0 / Opus 8.9, round 1", with no digest.
- W3-DIST's S2, SW1 and R1 inputs do not pin the file.
- The other worktrees hold copies of the origin/main manifests below. Those copies are byte-identical to origin/main, or
  (for `paper/generated/MANIFEST.txt`) are that checkout's own generated copy. Each is listed once.

The patch changes the file's sha256 from 9b50e358…c056 to b6b2465c…2295 (LINES_CHECK), so every manifest that pins 9b50e358 goes stale.

**Precedent for the fix.** This follows the CORRECTION-ONLY / citefix precedent (D39/D41, 7c45d4b; MISR_NARROW): re-freeze the
manifest with only the drifted hash changed, and add HQ seat carriers that cite the diff check. The diff check here is
`Theory_work/Dept/research/FUNI_NARROW/DIFF_sol.md`. This is a statement change, so per v4 an OpenAI reviewer runs it, and
the carriers must cite it **and** the WEAKER tag.

## Manifests

| # | manifest (path) | pins | state | needed if the patch is applied |
|---|---|---|---|---|
| 1 | origin/main `Theory_work/INFRA/paper/generated/MANIFEST.txt`, line 20 `W2-UNI:F-UNI … L5_delivery.md:15-21 b0a0f3c2cf20d781 SUSPECT` (+ `blocks/W2-UNI_F-UNI.tex`) | F-UNI claim hash | ACCEPTED (generated) | Re-run `assemble.py` after the recorder step. Expect exactly that one line (prefix → `05c4cdf65a209b21`, state → ACTIVE) and one regenerated block. No carrier is needed. |
| 2 | origin/main `Theory_work/Wave3/API_AUDIT/pass1/MANIFEST.tsv` (f27–f31), `pass2/MANIFEST.tsv` (f35), `sharp1/MANIFEST.tsv` (f14) | 9b50e358 | historical API-audit send records | None. They stay as records of what was sent. Their result files (`f30.md`, `f14.md`, `R-AUD1_sol.md`) cite old line numbers inside 15–21 and resolve against the pinned version (LINES_CHECK §C). |
| 3 | W3-RM2-R `reviews/MANIFEST_R3.txt` (b06a8588…), line 21 `#EXTRA` + line 421 `9b50e358… EXT:Theory_work/Wave2/W2-UNI/lemmas/L5_delivery.md` | current | council **R3 PASS**, DLV-0 accepted, **not yet recorded** (no W3-RM2-R rows on origin/main) | If the patch is applied before the W3-RM2-R record: re-freeze `MANIFEST_R3r` (R3 with only line 421 changed, so verify shows exactly 1 difference) and add HQ seat carriers `R3r_record_{sol,opus}.md` citing `DIFF_sol.md` (WEAKER, F-UNI only). Content is unaffected, because DLV-0's statement already is (𝔇, IDEAL-W⁺) (`STATEMENT.md:80-90, 144-150`) and it consumes F-UNI only as the Step-2 template. Two bookkeeping edits on record: (i) the consumed pin `W2-UNI:F-UNI@1.1.0` (`STATEMENT.md:232`, table `:219`) either stays as the template pin or is re-pointed to `@2.0.0`; (ii) DLV-0 should name the registered **A:IDEAL-W+** (`A_IDEALW_PLUS.md`). Simplest order: record W3-RM2-R first, then apply this patch as a post-record CORRECTION-ONLY batch with the same carriers. |
| 4 | W3-RM2-R `reviews/MANIFEST_R1.txt` (4c2183ce…), `MANIFEST_R2.txt` (e71637e0…), `INPUTS_R1.txt` line 21 (path only) | 9b50e358 / path | earlier rounds, superseded by R3 | None (historical). |
| 5 | W3-READER `reviews/INPUTS_R1.txt` line 17 (path only, no hash); no READER manifest is frozen yet | path | RUNNING (CP3 council briefs drafted) | **Freeze:** if the patch lands before the READER CP3 freeze, the freeze hashes the new file and needs nothing. If it lands after, re-freeze and add a carrier. **Content:** this does need a change. Row 3.1 (Thm 6) and its delivery clause ("always produces output; P(Ŝ = S₀) → 1") consume `W2-UNI:F-UNI@1.1.0` with operational premises (S4) = C-DLV's IDEAL-W (`READER_VERSIONS.md:44-50, 682-689`, bridge B6.6). After v2, (S4) must add **A:IDEAL-W+**, or the delivery clause must be scoped to 𝔇 (bounded, no asymptotics). The pin must become `@2.0.0`. READER already keeps the delivery clause out of the abstract until the F-UNI gate resolves (`:688-689`; CLAIMS_CARD gate item (4)). |

**Summary.**
- One accepted generated manifest needs a re-run: #1, no carrier.
- One council-passed but unrecorded manifest needs a re-freeze plus carriers: W3-RM2-R R3 (#3), unless the patch is applied after the W3-RM2-R record.
- One running ticket must take A:IDEAL-W⁺ into its premises: W3-READER (#5).
- No accepted, recorded ticket manifest pins this file, so no accepted ticket needs a re-freeze.

## F-UNI's registry dependents (the SUSPECT cascade) — who is cleared

The narrowed F-UNI gives two clauses. Clause (a) is delivery under IDEAL-W on the bounded domain 𝔇, with no asymptotic
conclusion. Clause (b) is every n and P(Ŝ⁺ = S₀) → 1, but only under **A:IDEAL-W+**. A user is covered if it either needs
delivery only on 𝔇, or already assumes A:IDEAL-W+.

| claim (state now) | what it uses from F-UNI / UNI-0 | covered by narrowed F-UNI? | verdict |
|---|---|---|---|
| W2-UNI:F-UNI@1.1.0 (SUSPECT) | — | becomes v2.0.0 | **clear on apply** (rehash, A:IDEAL-W+ added to assumptions; DIFF_sol as check record) |
| W2-UNI:UNI-0@1.1.2 (SUSPECT) | `STATEMENT.md:108-109`: "under the delivery premises/allocation, P(no output) = 0 and **P(Ŝ⁺ = S₀) → 1**". The delivery premises are FACA L7's, i.e. IDEAL-W (`:30-31`, inside its premise span `:22-34`). This needs every n and n → ∞ under IDEAL-W. | **No.** (a) is bounded; (b) needs A:IDEAL-W+, which UNI-0 does not assume. The other conclusions (Sand, NA, TL, D_n → 0, posterior rate, P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0, P(𝒪 ∩ {Ŝ⁺ = S₀}) = 1 − P(U_n) − o(1)) do not use F-UNI. | **stay SUSPECT.** Repair: an in-span same-line narrowing of `:108-109` ("under the delivery premises/allocation and A:IDEAL-W⁺"), WEAKER, major bump. Do not edit `:30-31`, because that premise span is shared by other rows. |
| W2-UNI:UNI-1@2.0.0 (SUSPECT) | `STATEMENT.md:123`: "with the delivery premises P(Ŝ⁺ = S₀) → 1" (same premises, `:30-31`). p may grow (limsup log p/log n < α₀), so the exact branch is not guaranteed. | **No**, for the same reason. The other conclusions are unaffected. | **stay SUSPECT.** Same repair at `:123`. Natural member of the 17-claim batch. |
| W3-RM:SAND-R@1.0.0 (SUSPECT) | `W2-UNI:UNI-0@proof:UNI L2_k0 §3–§6` (sandwich lemma only). `L3_SANDR.md:9`: "Only the sandwich interface is claimed, not NA, TL, POST or delivery." | Not needed: no delivery use. | **clear.** This does not depend on the narrowing; the cascade came from UNI-0's row edge, not from a use. |
| W3-RM:SAND-Rp@1.0.0 (SUSPECT) | `W3-RM:SAND-R@stmt` only | not needed | **clear** |
| W3-RM:RM-R@1.1.2 (SUSPECT) | Through SAND-R/SAND-Rp only. Its conclusions are those of (C0), which states "**No delivery claim** (P(U_n) → 0 is not asserted)" (`W3-RM/STATEMENT.md:172`). | not needed | **clear** |
| W3-RM:Examples@1.0.2 (SUSPECT) | `W2-UNI:UNI-0@stmt (E-R1)`: UNI-0's class and its L2_k0 verifications feed RM-R's hypotheses (`lemmas/L7_examples.md:10-27`). RM-R/RM-F carry no delivery. | not needed | **clear.** Recorder note: the table cell `L7_examples.md:96` ("UNI-0 'PROVED-CHECKED'") quotes UNI-0's status. That is a status quote, not a use of UNI-0's delivery clause. |

**Unregistered users** (not in the cascade, listed for HQ):
- W3-RM2-R:DLV-0 is covered: its own statement is already (𝔇, A:IDEAL-W⁺). See #3.
- W3-READER Thm 6 (3.1–3.2), delivery clause: **not covered** until (S4) adds A:IDEAL-W⁺. See #5.

**Registry mechanics.** UNI-0 and UNI-1 stay SUSPECT, so the cascade rule may re-flag the four W3-RM rows through the
UNI-0 edge. Clearing them needs the edge-scope justification above: `@proof:L2_k0 §3–§6` and `@stmt (E-R1)` both consume
delivery-free parts.

**Observation for HQ (outside this task; not changed here).** TR1 §1 says the base-cap obstruction "would also affect a
literal shipped implementation of the old ℓ-cap method". The same every-n sentence, "for every admissible n ≥ 3, P(no output) = 0"
under IDEAL-W, appears in rows that are currently **ACTIVE**:
- W2-FAC-A:Prop-F-FAC (`W2-FAC-A/lemmas/L7_delivery.md:22-24`);
- C-DLV:Prop-F;
- the FINAL s6 Propositions F / F-GROW (`s6_delivery.tex:46, :54`).

F-UNI v2 consumes FACA L7 Step 2 only as restricted by TR1. These rows presumably belong to the 17-claim batch.
