# W3-T03ACC — REPORT (council acceptance of T03♯ = SOP:TH09 on its existing proof)

Tier B re-check, NORMAL mode. This file restates nothing (v4 §3): the statement is `STATEMENT.md` v1.1 (LOCKED), the
proof is `sources/W1-T03R/PROOF.md` @7e14d6f as written (no new mathematics), with the locked inputs
`sources/P1/PROOF_v3.tex` and `sources/P3/PROOF_v2.tex`. Pins: `sources/PINS.md`.

## 1. Claims
| claim | statement | premises |
|---|---|---|
| `W3-T03ACC:T03S.1` (posterior concentration) | `STATEMENT.md:64` | `STATEMENT.md:43-60` (R1, G, R, SE_λ(j₀), SE_w(m♯_n; g₀), BM) |
| `W3-T03ACC:T03S.2` (PIPs, MPM) | `STATEMENT.md:65` | same |
| `W3-T03ACC:T03S.3` (global HPM) | `STATEMENT.md:66-69` | same |
| `W3-T03ACC:T03S.4` (large-signal inclusion without beta-min) | `STATEMENT.md:70-73` | `STATEMENT.md:43-56` (no BM) |
| `W3-T03ACC:T03S.5` (scale invariance) | `STATEMENT.md:74-77` | definitions `STATEMENT.md:22-41, 57-60` |
Definitions: `STATEMENT.md:22-41`; readings: `STATEMENT.md:92-117`; consumed results and their statuses: `STATEMENT.md:118-131`.

## 2. Checks (review files; verdicts verbatim)
| step | object | reviewer | verdict | file |
|---|---|---|---|---|
| statement lock SL1 | STATEMENT v1.0 → v1.1 | Sol (gpt-6.1-sol, high), fresh, blind | "LOCK WITH CHANGES" (CRITICAL 1 F, MAJOR 1 E, MINOR 1 E; all applied in v1.1) | `reviews/SL1_statement_lock_sol.md`, `reviews/SL1_disposition.md` |
| line check LC-A | E1(a),(b),(d), m♯_n, E2(i), den′, T02(i♯); [P1] setting, `lem:slab`, `lem:IGint`, `lem:spec`(a)–(e), `lem:prior`(a)–(d), `lem:chi`, `prop:closed`, `thm:T01i`, `thm:T01ii`, `thm:T01iii`, `thm:Ta`, `lem:num`, `lem:den`, `thm:T02i` | Sol, new agent, blind | "Overall: VERIFIED" (0 GAP, 0 ERROR) | `reviews/LC_A_line_check_sol.md` |
| line check LC-B | SE_λ/SE_w, Lemma I, Lemma B, (C1)–(C5); [P3] §§1–5 | Sol, new agent, blind | "Overall: VERIFIED" (0 GAP, 0 ERROR) | `reviews/LC_B_line_check_sol.md` |
| line check LC-C | (C6)–(C10), Assembly (T03S.1–.5), completeness of the change lists; [P3] §§6–7 | Sol, new agent, blind | "Overall: VERIFIED" (0 GAP, 0 ERROR) | `reviews/LC_C_line_check_sol.md` |
Every row of `DEPS.tsv` under a claim must be OK before the council freeze. [P1] `lem:prior`(e) lies inside the row
`P1.prelim` but is not used by T03♯ (it serves [P1] §T02(ii)); LC-A did not check it.

Points settled by the checks (no change to any clause): the recorded growth exponent A is used as is, with no step
needing A ≥ 1 (LC-A N4, LC-C N6; `STATEMENT.md:98-102`); p = 1 needs no extra hypothesis (SL1; LC-A N1; LC-C N7;
`STATEMENT.md:103-108`). Editorial items: `ERRATA.md`.

## 3. What this ticket does not do
No new proof, no change of hypothesis or conclusion, no statement about the sampler's reported HPM (`STATEMENT.md:85-91`).
The record's scope paragraph (`sources/statement/W6-FIXREV2_STATEMENTS.md:63-81`) accompanies the theorem and is not
under review. HEURISTIC/OPEN: none asserted here.

## 4. Registry block
Status source for every claim: this ticket (`REPORT.md:17-23`). The `council:` field and the `correct:` gate are filled
from the CP3 checkpoint file (editorial; this file is inside the frozen manifest).

```
REGISTRY
claim: W3-T03ACC:T03S.1 | kind: theorem | statement: STATEMENT.md:64 | premises: STATEMENT.md:43-60
name: T03♯(i) posterior concentration (= SOP:TH09, TH128 clause 1)
status: PROVED (W1-T03R, proof as written); LC-A, LC-B, LC-C VERIFIED (W3-T03ACC); council R1 PENDING | status_source: REPORT.md:17-23
conclusion: posterior: 1 − π(S₀) = O_P(r_n) | rate: √(log n/n) | scope: fixed design, s₀ ≥ 1 fixed, p ≤ n^A (A fixed), asymptotic
implies: SOP:TH09 (same statement, clause 1) ; TH128 (same)
gates: correct:PENDING(reviews/BRIEF_R1_astra.md, reviews/BRIEF_R1_opus.md)

REGISTRY
claim: W3-T03ACC:T03S.2 | kind: theorem | statement: STATEMENT.md:65 | premises: STATEMENT.md:43-60
name: T03♯(ii) PIP bound and MPM consistency
status: PROVED (W1-T03R, proof as written); LC-A, LC-B, LC-C VERIFIED (W3-T03ACC); council R1 PENDING | status_source: REPORT.md:17-23
conclusion: posterior: max_j |PIP_j − 1{j ∈ S₀}| ≤ 1 − π(S₀) for every data set; P₀(MPM = S₀) → 1 | scope: as T03S.1
depends_on: W3-T03ACC:T03S.1@stmt
implies: SOP:TH09 (clause 2)
gates: correct:PENDING(reviews/BRIEF_R1_astra.md, reviews/BRIEF_R1_opus.md)

REGISTRY
claim: W3-T03ACC:T03S.3 | kind: theorem | statement: STATEMENT.md:66-69 | premises: STATEMENT.md:43-60
name: T03♯(iii) global-HPM consistency
status: PROVED (W1-T03R, proof as written); LC-A, LC-B, LC-C VERIFIED (W3-T03ACC); council R1 PENDING | status_source: REPORT.md:17-23
conclusion: posterior: P₀(S† ≠ S₀) ≤ 2E₀[1 − π(S₀)] → 0; S₀ strict maximiser of F on {π(S₀) > ½} | scope: as T03S.1; no expectation rate
depends_on: W3-T03ACC:T03S.1@stmt
implies: SOP:TH09 (clause 3)
gates: correct:PENDING(reviews/BRIEF_R1_astra.md, reviews/BRIEF_R1_opus.md)

REGISTRY
claim: W3-T03ACC:T03S.4 | kind: theorem | statement: STATEMENT.md:70-73 | premises: STATEMENT.md:43-56
name: T03♯(iv) large-signal inclusion without beta-min
status: PROVED (W1-T03R, proof as written); LC-A, LC-B, LC-C VERIFIED (W3-T03ACC); council R1 PENDING | status_source: REPORT.md:17-23
conclusion: posterior: Π(S ⊉ J_n(c) | y) = O_P(r_n) and 1 − min_{J_n(c)} PIP_j = O_P(r_n), c > c₀; same for J_n^∞ | scope: as T03S.1, no beta-min
implies: SOP:TH09 (clause 4)
gates: correct:PENDING(reviews/BRIEF_R1_astra.md, reviews/BRIEF_R1_opus.md)

REGISTRY
claim: W3-T03ACC:T03S.5 | kind: remark | statement: STATEMENT.md:74-77 | premises: none (deterministic)
name: T03♯(v) scale invariance of the beta-min conditions and J_n
status: PROVED (W1-T03R, proof as written); LC-C VERIFIED (W3-T03ACC); council R1 PENDING | status_source: REPORT.md:17-23
conclusion: identity: the BM inequalities and J_n(c), J_n^∞ are invariant under (θ*, σ*²) → (θ*/d, σ*²/d²) | scope: any n
implies: SOP:TH09 (clause 5)
gates: correct:PENDING(reviews/BRIEF_R1_astra.md, reviews/BRIEF_R1_opus.md)
```
