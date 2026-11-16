# W3-SCR — council round R3 (diff round, PROTOCOL_v4 §5.5) — seat `opus`

Reviewer: Claude Opus 5.5 (fresh thread, read-only). Date: 2026-11-16 03:01 CST.
Worktree `/home/fb31/BVS-wt/W3-SCR-R2` (branch `theory/W3-SCR-R2`). Manifest under review: `19847f54…6fbce5dc` (MANIFEST_R3.txt).
Inputs used: my R2 review, `R3_REPORT_diff.patch`, `R3_CHANGED.tsv`, and the STATEMENT / CODE_CHECK / lemma line ranges named by the pointers (read only to check the pointers).
I did not read other reviews, dispositions, scores or the claims registry.

## 0. Manifest verification

```
$ python Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-SCR Theory_work/Wave3/W3-SCR/reviews/MANIFEST_R3.txt
verify: OK MANIFEST 19847f54f60d58a7d7f8214004b09a41242492c1c7237dc60de42f2a6fbce5dc
```
(exit 0)

Further checks:
- **MANIFEST_R2 vs MANIFEST_R3.** `diff` shows the header line and exactly one entry changed: REPORT.md, `21e577a9…` → `c076bad9…`.
- **Patch matches git.** The supplied patch is identical to `git diff 925aa8d5 e18e479e -- REPORT.md`, apart from the `index` line. `925aa8d5` is the commit whose REPORT.md hashes to the R2 entry; `e18e479e` is the one whose REPORT.md hashes to the R3 entry.
- **Lines outside the diff.** REPORT.md lines 1–10 and 56–167 are byte-identical to the R2 version. The file length is unchanged (167 lines, 42 lines out and 42 in). So §1 and §3, including the status-source lines 59–65, are unchanged and unmoved.

## 1. My R2 findings

| R2 finding | Status | New REPORT lines | Reason |
|---|---|---|---|
| Finding 1 (F) — A1 summary omitted "κ, b, M, σ fixed" | **RESOLVED** | 40 (also 49, 54) | The summary is gone. REPORT:40 points to STATEMENT:158–163, which is exactly Corollary A1 and includes "with κ, b, M, σ fixed (not depending on n)" (159–160). |
| Finding 2 (F) — A1° summary false as stated ("not the total signal"); old REPORT:50 | **RESOLVED** | 41; 49 replaces old line 50 | The false sentence is deleted. REPORT:41 points to STATEMENT:165–169, which carries all five hypotheses, including ‖μ‖ = o(nσ) and s₀𝐋_n ≤ κn/576. The old line 50 is now a pointer to STATEMENT:228–236. |
| Finding 3 (F) — SCR-G(ii), SCR-C and SCR-R dropped hypotheses | **RESOLVED** | 33, 42, 45 | SCR-G → STATEMENT:132–145, which includes "C and N, both of size ≤ q_n" (139). SCR-C → 171–176, which includes the screening hypothesis, ‖θ*‖₂ = O(σ√n) and q_n log p = o(n) (172–173). SCR-R → 194–199, which includes "Under the hypothesis of (A∞) or (A°∞)" (196). |

My R2 E findings (E1–E4) are outside this diff round and are not re-raised.

**F1–F4 overall.** These read as resolved. For F4 (the other seat's finding, not part of my count): the SCR-M "δ_S" summary is gone, and REPORT:32 points to STATEMENT:103–130, which states the gap bound exactly (115–116).

## 2. Does the diff break anything?

I checked every pointer against the file it names. Each start and end line falls on a claim boundary.

| REPORT line | Pointer | Lands on | OK |
|---|---|---|---|
| 19 | STATEMENT:12–47 | §0 Setting: Model G, score, 𝒩, certificate, 𝒞, scanned centres, EX-A (ends at "q always denotes…", 47) | yes |
| 20 | STATEMENT:49–75 | §1 Quantities through margins and floors (ends at the B3 remark, 75) | yes |
| 21 | CODE_CHECK:20–72 | CC1 (20) through the end of CC6 (72), including the reported-flag block 27–37 | yes |
| 24 | L1_score:7–82 | L1.1 (7) to the end of the file (82); lines 1–6 are the notation header | yes |
| 25 | L2_noise:11–57 | deterministic witness (11) through E3b and its proof (57); lines 1–10 are cited tools and conventions | yes |
| 28 | STATEMENT:79–85 | SCR-A heading to "on 𝓔_A, S₀ is contained…" | yes |
| 29 | STATEMENT:87–90 | (A∞) | yes |
| 30 | STATEMENT:92–95 | SCR-A° | yes |
| 31 | STATEMENT:96–101 | (A°∞) with its parenthetical | yes |
| 32 | STATEMENT:103–130 | SCR-M, M1–M6 and the illustration | yes |
| 33 | STATEMENT:132–145 | SCR-G (i)–(iii) and the closing remark | yes |
| 34 | STATEMENT:147–148 | Lemma B heading and the definition of c_θ | yes |
| 35–39 | 149; 150–151; 152–153; 154; 155 | B1; B2; B2°; B2d; B3, each one line or block exactly | yes |
| 40 | STATEMENT:158–163 | Corollary A1 | yes |
| 41 | STATEMENT:165–169 | Corollary A1° | yes |
| 42 | STATEMENT:171–176 | SCR-C (stops before "Excess set…", 177) | yes |
| 43 | STATEMENT:177–192 | L5.1 (EC′) paragraph | yes |
| 44 | L5_exact:71–75 | Corollary L5.2 statement (the proof starts at 77) | yes |
| 45 | STATEMENT:194–199 | SCR-R, both heading lines included | yes |
| 46 | STATEMENT:201–212 | SCR-N and consequences (1) and (2) | yes |
| 47 | STATEMENT:214–227; 238–246 | §3 claimed / not claimed / design-agnostic; §4 Interface | yes |
| 49 | STATEMENT:228–236 | "Changes vs the card" (1)–(7) | yes |
| 52–53 | 177–192, 171–176, 190, 220–221 | L5.1; SCR-C; "No bound on \|E\| is claimed"; "a bound on \|Ŝ∖S₀\| in general designs" (not claimed) | yes |
| 54 | 161–163; 147–156; 158 | A1 growth condition and q_n range; Lemma B in full; A1's floor hypothesis | yes |

- **Coverage.** All 21 claim ids have a pointer: CC, L1, L2, SCR-A, A-inf, SCR-Ao, Ao-inf, SCR-M, SCR-G, B1, B2, B2o, B2d, B3, A1, A1o, SCR-C, L5.1, L5.2, SCR-R, SCR-N. None is missing or mislabelled.
- **No restatement.** Lines 19–21 list object names only. Lines 13–16 are a meta note, and their two factual claims are true: only §2 changed, and §3 keeps its text and line numbers.
- **The non-claim on lines 52–53** ("no bound on |Ŝ∖S₀| is claimed") does not restate a claim. It points to the statement's own non-claim (STATEMENT:190, 220–221), and SCR-C, the only case with a bound, is cited in the same sentence. I raise no finding here.
- **Nothing outside §2 changed** (see §0).
- **No other file depends on §2.** No STATEMENT, lemma, CODE_CHECK or ASSUMPTION_MAP line cites REPORT §2. I took this from R3_CHANGED.tsv and did not search for it myself. Either way, no claim text or proof changed.

**New findings: none** (no C, S or F). As the brief requires, I add no E findings this round.

## 3. Per-claim table (21 rows)

The claim text and proofs are unchanged since R2 (manifest verify, and the one-entry manifest diff). The diff touches only REPORT §2, so I carry each R2 decision forward. The REPORT-summary caveats on SCR-G, A1 and A1° in R2 are now gone.

| id | decision |
|---|---|
| CC | ACCEPT |
| L1 | ACCEPT |
| L2 | ACCEPT |
| SCR-A | ACCEPT |
| A-inf | ACCEPT |
| SCR-Ao | ACCEPT |
| Ao-inf | ACCEPT |
| SCR-M | ACCEPT |
| SCR-G | ACCEPT |
| B1 | ACCEPT |
| B2 | ACCEPT |
| B2o | ACCEPT |
| B2d | ACCEPT |
| B3 | ACCEPT |
| A1 | ACCEPT |
| A1o | ACCEPT |
| SCR-C | ACCEPT |
| L5.1 | ACCEPT |
| L5.2 | ACCEPT |
| SCR-R | ACCEPT |
| SCR-N | ACCEPT |

## 4. Gates (on manifest 19847f54…)

- **G1 (every step correct): PASS.** The proofs are unchanged and were all accepted in R2. The diff contains no mathematics.
- **G2 (hypotheses used = hypotheses stated): PASS.** The R2 failure came only from REPORT §2. §2 now restates nothing, and each pointer lands on the full statement.
- **G3 (no hidden assumptions): PASS.** No change.
- **G4 (cited results have adequate status): PASS.** No change.
- **G5 (constants and rates tracked): PASS.** No change. The constants are no longer restated in REPORT, so they cannot drift.
- **G6 (fidelity to the code): PASS.** CODE_CHECK is unchanged, and the CC pointer covers CC1–CC6.

## 5. Score

**9.4.** I hold no C, S or F finding. All three of my R2 F findings are resolved by exact pointers, and F4 reads as resolved too. Every one of the 21 claims is accepted.

`COUNCIL-VERDICT round=R3 manifest=19847f54f60d58a7d7f8214004b09a41242492c1c7237dc60de42f2a6fbce5dc seat=opus score=9.4 gates=PASS`
