# T7 addendum: rulings on walk `walks/T7.md` (walkC 4cdb915e; WALK COMPLETE, 1 MINOR, 2 Lean NOTEs)

No ruling in `T7.md` changes. The walk finds no mathematical issue in the chain R′ → MIS(i) → (i′) → (ii) → CorG-min → CorGb-plus.

| Row | Ruling | (a) Kind | (b) Recorded STATEMENT? | (c) Fix |
|---|---|---|---|---|
| **MINOR:** "no condition on how Σ, β, σ² vary with n" | AGREE | Wording overclaim: (A2) and (A3) are conditions on the sequence (Σ_n, β_n, σ²_n), so the sentence contradicts them as written | No. The masters say only "may depend on n" (`W3-MISR-R/STATEMENT.md:99`) | Replacements below; five places |
| **NOTE:** POST2 displays (I1)–(I5) as standalone lemmas | AGREE | Lean note | No | None. Lean states each with its threshold dependence, so that the c-independence in MIS(i′)(a) can be stated. Same item as T4 Lean item 3. |
| **NOTE:** deterministic-p instance of MIS-R (ii) | AGREE | Lean simplification | No | None. Formalise (ii)(a) only for deterministic p, deterministic (β^𝒞, σ²_𝒞) and 𝓕_n = σ(X^r_𝒞); the freezing step is then the plain independence lemma. This fits T7 Lean item 3. |

## Replacement wording for the MINOR

- `READER_VERSIONS.md:449` (title): "no condition on how $\Sigma$, $\beta$, $\sigma^2$ vary with $n$" → "$\Sigma$, $\beta$, $\sigma^2$ may vary with $n$, subject only to (A2)–(A3)".
- `READER_VERSIONS.md:462`: "No condition is placed on how $m$, $\Sigma$, $\beta^{\mathcal C}$ or $\sigma^2_{\mathcal C}$ vary with $n$." → "$m$, $\Sigma$, $\beta^{\mathcal C}$ and $\sigma^2_{\mathcal C}$ may depend on $n$; no condition beyond (A1)–(A3) is placed on how they vary."
- `READER_VERSIONS.md:1424` (Theorem 2X, the same sentence; not in the walk's row): the same replacement with $\beta$, $\sigma^2$.
- `CLAIMS_CARD.md:57` (comparator cell) and `Docs/Writing/results/sections/sec3_selection.tex:432-433` (the paper draft, same clause): "and no condition on how $\Sigma$, $\beta$, $\sigma^2$ vary with $n$" → "and with $\Sigma$, $\beta$, $\sigma^2$ free to vary with $n$, subject only to the theorem's floor and signal conditions".

The two `READER_DELTA.md` source files (`W3-MISR-R:36`, `W3-D2:16`) carry the old sentence as history; I would leave them. `W3-MISR/STATEMENT.md:167-169` uses similar words only for σ² and τ² separately and then says the hypotheses must hold relative to σ²_𝒞; that is accurate and stays.

## Fit with T7-1 and T7-2

No overlap and no conflict: T7-1 edits the Example (`:469`), T7-2 edits the fixed-design remark (`:481`). T7-2's phrase cites "(A1)", consistent with the new line 462's "(A1)–(A3)". All three, with the line-449 title, go in the same reader touch.
