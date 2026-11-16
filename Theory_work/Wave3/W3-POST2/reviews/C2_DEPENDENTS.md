# W3-POST2 — C2 diff round: dependents of every changed object

Companion to `reviews/C2_DIFF.md` (change numbers #k refer to its §3 table). Paths are relative to
`Theory_work/Wave3/W3-POST2/`; line numbers are at HEAD (= `reviews/MANIFEST_C2.txt`). POST2 has no `DEPS.tsv` (it
predates PROTOCOL v4), so this list was built by hand from the citations in the files (`grep` for E0, E1, `[C1B-k]`,
intercept, D(b), and the registry premises in `Theory_work/INFRA/registry/claims.tsv`). A seat reads the changed lines
and the dependent lines below; it does not re-read other unchanged text.

## M-class objects (check line by line)

| changed object | where | used by (inside POST2) | registry claims affected |
|---|---|---|---|
| **Lemma E0** (#9) | `lemmas/E_visibility.md:15-20` | (1) Lemma E1(b), `lemmas/E_visibility.md:46` (B = j₀; needs \|J′\| ≤ m♯_n for (G3′)), whose proof is `:26-55`; (2) D3 cutoff, `lemmas/D_hellinger.md:52-55` (B = s₀ + j₀); (3) pointer `REPORT.md:108-109`. Inherited inputs: the cutoff definition R_m, m♯_n (`Theory_work/Wave3/W3-POST/STATEMENT.md:36-38`), Ω, K (`:21`), the ratio product [T03R] `PROOF.md:22` | E (via E1(b)); D.D(b) (via D3); C case (iii) and E3.1 indirectly (below) |
| **E1(b) now cites E0** (#10) | `lemmas/E_visibility.md:46` | (1) E2 assembly, `lemmas/E_visibility.md:56-70` (underfits with \|J′\| ≤ j₀) → Claim E `STATEMENT.md:126-133`; (2) Claim C case (iii), `lemmas/C_expectation.md:52` (κ̄_n = n^{−2} from Lemma E1) and `:54` (E1(a)) → Claim C `STATEMENT.md:83-94`; (3) D3, `lemmas/D_hellinger.md:57-59` (E1(b) at c₂ = c₁ + 1 for far underfits); (4) E3.1, `lemmas/E_visibility.md:76-78` (its last clause "Theorem 1-VIS contains …" uses Claim E) | E, C, D.D(b), E3.1 |
| **D3 cutoff chain — the repaired D(b) step** (#11) | `lemmas/D_hellinger.md:52-55` | the rest of D3: mass outside 𝒮_n `:55-59`; conditional bounds on 𝒮_n `:60-71` (needs \|S\| ≤ m♯_n for near underfits so that (G2*) covers them); constants and conclusion `:72-81` → Claim D(b) `STATEMENT.md:112-116`; registry block `REPORT.md:240-244`; summaries `REPORT.md:99-100`, `ASSUMPTION_MAP.md:13, 16, 38, 46`. Inherited inputs: Ω and K (`Theory_work/Wave3/W3-POST/STATEMENT.md:21`), j₀ (`STATEMENT.md:21`), (G2*) (`STATEMENT.md:18-19`) | **D.D(b)**, D |
| **D4 Remark 0, intercept** (#8) | `lemmas/D_hellinger.md:84-88` | the Claim D statement itself: `STATEMENT.md:117-119` (this range is a **premise** of registry rows D.D(a) and D.D(b) in `claims.tsv`); `REPORT.md:95-96`. It relies on Lemma D0 (`lemmas/D_hellinger.md:14-17`), D2's conclusion (`:46-47`) for D(a), and D3's conclusion (`:76-79`, the choice M_n = √log n and the constant C′_H) for D(b). Inherited input: the truth convention (`Theory_work/Wave3/W3-POST/STATEMENT.md:31`) | D.D(a), D.D(b), D |
| **Claim B relation strengthened** (#13) | `STATEMENT.md:79-80`; `REPORT.md:119, 228` | relation and registry text only; uses the existing proof `lemmas/B_tail_approx.md:45-48` (exact reference) and B Remark 1; compared with [W3P] Lemma 1a (`Theory_work/Wave3/W3-POST/STATEMENT.md:48`) | B (relation field only) |
| **c₀ < c₁ grid** (#14) | `STATEMENT.md:136`; `REPORT.md:122` | the "coexist for c₀ < c ≤ c₁" relation of Claim E | E (relation field only) |

## W- and R-class objects (check only that the new wording matches the proof; no proof depends on them)

| changed object | where | depends on it |
|---|---|---|
| N2 qualification (#3, #4) | `REPORT.md:149-150, 193`; `ASSUMPTION_MAP.md:14, 27`; `lemmas/A_occam.md:33-34` | nothing (remarks; A0/A1 proofs do not use N2) |
| N4 wording (#2) | `REPORT.md:156-158`; `ASSUMPTION_MAP.md:28` | nothing (Claim E's c > c₁ proof does not use N4) |
| D(a) scale "argued, no lower bound" (#17) | `REPORT.md:161-162`; `ASSUMPTION_MAP.md:59-60`; `lemmas/D_hellinger.md:96-98` | nothing (no lower-bound theorem is stated) |
| rank-loss wording (#16) | `REPORT.md:55-56` | nothing |
| scope flag, numbering map, labels, registry blocks, check records, citations, version pointers, N5 header, SL exponent, council record (#1, #5–#7, #12, #15, #18–#20) | see `C2_DIFF.md` §3 | nothing mathematical; the registry blocks `REPORT.md:202-254` restate statuses and premises |

## Outside POST2 (for HQ; not to be reviewed in this round)

- W3-DIST consumes POST2 Claim D (D(b) and its intercept remark).
- W3-MISR claims MIS(i), MIS(i′), MIS(ii), Cor-G(b), Cor-H are registered "conditional on" W3-POST2:C, E, A1, A0 and D
  (`claims.tsv` rows 413–418). The C2 decisions on C, E, A1, A0 and D feed those conditions.
