# W3-T03ACC — PLAN (2026-11-15 23:50 CST; deadline CP3 Thu 2026-11-19 18:00 CT, aim Wed 11-18 18:00)

Tier B, NORMAL mode (v4 H1; POLICIES §14 level 0). No new mathematics: the proof **as written**
(`sources/W1-T03R/PROOF.md` @7e14d6f, with [P1] = `sources/P1/PROOF_v3.tex`, [P3] = `sources/P3/PROOF_v2.tex`) is
line-checked; any GAP is repaired in `lemmas/` (copy of the step, changed lines marked `[R-#]`) and re-checked by a new
Sol agent. A gap that needs a new argument is an early checkpoint (Tier A) reported to the manager at once.

## 1. Chain and OpenAI budget (Tier B, about 4; here 5)
| step | who | inputs | output | est. hours (wall) |
|---|---|---|---|---|
| SL1 statement lock | Sol (gpt-6.1-sol, high), fresh, blind | MANIFEST_SL1: STATEMENT, PLAN, BRIEF, TARGET, sources/ | `reviews/SL1_statement_lock_sol.md` | 2–4 (queued behind Codex congestion until ~midday 11-16) |
| CP1 | lead | — | `CHECKPOINT_1.md`; manager answers | — |
| LC-A, LC-B, LC-C line checks | Sol ×3, new agent per batch, blind to LOG and other reviews | the batch's lines + what they cite | `reviews/LC_<X>_line_check_sol.md` | 3–5 each; in parallel when Codex allows |
| repairs (if any) | lead → new Sol re-check of the repair + STALE DEPS rows | `lemmas/` | `reviews/RC_*` | 0–8 |
| API Fable audit (HQ, v4 H3) | proof material only | `api/` (moved to `reviews/api/` before any freeze) | disposition table in `reviews/API_dispositions.md`: each FATAL/MAJOR confirmed by a line check or rejected with evidence | 1–2 |
| DEPS.tsv, REPORT.md (+ registry block, status source = this ticket), citecheck 0 MISS | lead | — | — | 2–3 |
| council R1 | **Astra** (gpt-6-astra, high; HQ's choice, `BRIEF.md:28`) + **Opus 5.5 high** (Claude Third), fresh, blind | MANIFEST_R1 | `reviews/R1_*` | 4–6 |
| diff round (if any accepted C/S/F) | same seat models, fresh threads | diff + DEPS dependents | `reviews/R2_*` | 3–4 |
| CP3 | lead | bind, staged ingest | `CHECKPOINT_3.md` | 1 |

## 2. Line-check batches (each 2–4 objects as v4 §2A asks; all [P1]/[P3] steps consumed are inside a batch because
T01–T03 are SAME-FAMILY-ONLY, STATEMENT §5)
- **LC-A — size tail.** PROOF.md §1 (`:13-47`, Lemma E1(a),(b),(d), definition of m♯_n; E2(i) `:49-59`) and §2
  (`:74-101`, Lemma den′, Theorem T02(i♯)); with [P1] `lem:spec`, `lem:prior`, `lem:chi`, `lem:slab`, `lem:IGint`
  (`PROOF_v3.tex:60-152`), `thm:T01iii` (`:232-252`), `thm:Ta` (`:253-268`), `lem:num`, `lem:den`, `thm:T02i`
  (`:313-384`). E1(c) and E2(ii),(iii) are used only by Prop. E3 (out of scope) — the checker confirms that.
- **LC-B — anchored eigenvalues and supersets.** PROOF.md §4 (`:127-145`, Lemma I, Lemma B (B1)–(B3)) and (C1)–(C5)
  (`:170-185`); with [P3] §§1–4 (`PROOF_v2.tex:1-279`: setting, `eq:mn`, `lem:red`, `eq:score`, `lem:smoother`,
  `cor:diff`, `lem:det`, `lem:prior`, `lem:signal` statement, `lem:chi`, `sec:good`, `lem:Gprob`, `lem:ongood`,
  `lem:onesup`, `prop:sup`).
- **LC-C — underfitting models and assembly.** (C6)–(C10) and Assembly (`PROOF.md:187-209`); with [P3] §§5–6
  (`PROOF_v2.tex:280-396`: `lem:SvsSp`, `lem:signalgain`, `lem:assemble`, `sec:main` Step 0, Step 1, (i)–(v)), and the
  `lem:signal` proof; plus the "unchanged / changed steps" lists (`PROOF.md:205-207`) checked for completeness.

Each checker gets STATEMENT.md (locked), its batch, and the sources; verdict per step VERIFIED / GAP / ERROR with
file:line; is asked to break each step; checks the hidden-hypothesis question (every use of an eigenvalue bound is
covered by R, SE_λ(j₀), SE_w(m♯_n; g₀) or interlacing) and the uniformity of every O_P in m and in the model family.

## 3. DEPS rows planned (v4 §4.1; kept by hand with sha256sum)
`STMT` (STATEMENT §2–§3) · `E1` · `E2i` · `DEN′` · `T02i♯` · `LemI` · `LemB` · `C1`…`C10` · `ASM` · `P1:<label>` rows
(one per consumed label group, as copies under `sources/P1/`) · `P3:<label>` rows · `REPORT`. A row is OK when its
checked sha equals its current sha and a line-check file names it VERIFIED.

## 4. Claims and registry
Claim ids `W3-T03ACC:T03S.1` … `T03S.5` (STATEMENT §3), implying SOP:TH09 / TH128 (same statement). HQ records; the
lead never touches main or the registry. Headline consequence: rows 1.1, 1.2, 3.1 lose "conditional on SOP:TH09" on
acceptance (HQ's call, v4 H5 card); no headline statement changes (READER_DELTA.md).

## 5. Schedule and risk
11-16 ~00:00 SL1 queued → CP1 → manager. 11-16 midday–evening: SL1 returns; LC-A/B/C launched together. 11-17: repairs
(if any), API dispositions, DEPS, REPORT, citecheck; freeze R1 by 11-17 evening; seats run overnight. 11-18: diff round if
needed; CP3 by 11-18 18:00 (one day slack to the 11-19 18:00 deadline). **Risk:** Codex availability (lock and the three
line checks all need it). If the line checks have not started by 11-17 08:00, CP3 by Thu 18:00 is at risk and I will say
so the same morning. A GAP needing new mathematics (none expected: SF and XF found none) also moves the date.
