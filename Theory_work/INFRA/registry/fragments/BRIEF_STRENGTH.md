# Drafting brief: strength layer for the HEADLINE theorems (helper)

You draft; the INFRA lead verifies. Work only in the worktree `C:\Users\felip\BVS-infra` (read-only except your four
output files in `Theory_work/INFRA/registry/fragments/strength/`). No git commands. Be efficient: use the
registry fragments `Theory_work/INFRA/registry/fragments/b*.jsonl` (claims with file + line spans) to jump to each
statement; read STATEMENT/REPORT spans and the lemma where an assumption is used, not whole proofs.

## Headline claims (ids as in the fragments; SOP:* are State-of-Project anchors)
SOP:TH09 (T03♯, row in Theory_work/State_of_Project/registry/theory_supp.tsv; statement in
Theory_work/Wave1C/FINAL/sections/s3_posterior.tex thm:ST), W2-APP:POST, SOP:TH05.0 (M5(0), theory_main.tsv),
W1-N1:Thm-N1, W1-PXN:Thm-PXN, W1-GEN:Thm-GEN, C-GROW:Thm-GROW, C-MIS:Thm-MIS(i), C-MIS:Thm-MIS(ii),
C-DLV:Prop-F, W2-FAC-A:Prop-F-FAC, W2-LOC2:F-LOC2, W2-UNI:F-UNI, W2-APP:Thm-LOC, W2-LOC2:PLR, W2-LOC2:Thm-Poly,
W2-FAC-A:Thm-FAC-L, W2-FAC-B:Thm-FAC-CS, W2-FAC-X:Thm-FAC-CS-iid, W2-FAC-PK:Thm-NEG, W2-FAC-PK:Thm-PATH.

## Key rule: interface properties
A SHARED assumption A (used by ≥ 2 headline claims, e.g. beta-min, p ≤ n^A growth, Gaussian noise, exact Gram /
iid Gaussian rows, block visibility, the LS0 cap/implementation premises (OP), SIZE) gets ONE bridge lemma A ⇒ P,
where P is the property the proofs actually use (e.g. "uniform add/delete score margin", "sandwich event",
"NA/TL lattice events"). Record A (kind assumption) and P (kind property). If the bridge lemma exists in the
fragments, name it; otherwise write `bridge` = "MISSING" (that is a finding, not your job to prove).
Restate family-named hypotheses ("compound symmetry", "AR(1)") as the property used, keeping the family as a
separate instance assumption.

## Output files (UTF-8)
1. `assumptions.tsv` (tab-separated, header):
   `id	kind	shared	name	statement	source	implies	bridge	version	notes`
   id `A:<SHORT>` for assumptions, `P:<SHORT>` for properties (e.g. A:BETAMIN, A:P-POLY, A:EXACT-GRAM,
   A:IID-GAUSS-ROWS, P:SCORE-MARGIN). kind assumption|property; shared yes|no; statement ≤ 200 chars;
   source = path:line where it is stated; implies = ids it implies (e.g. A:EXACT-GRAM implies A:GRAM-OP-BOUND),
   "; "-separated; bridge = claim id of A ⇒ P (for an A) / of the lemma proving P (for a P); version 1.0.0.
2. `strength.jsonl`, one object per headline claim:
   `{"id", "headline":"yes", "assumptions":[A ids; suffix "~nec" when the claim USES the assumption in a
   necessity/counterexample sense (Thm-NEG, SHARP-type), "~iff" for iff statements], "consumes":[P ids the proof
   uses], "conclusion":"<level>: <text>", "rate":"", "scope":"p range; design class; law", "implies":[claim ids
   whose statements this one implies — only when clear from the statements, e.g. FAC-CS-iid ⇒ FAC-CS instance?
   say so in notes if unsure], "gates":"correct:PASS(<council evidence>); lit:<PENDING|PARTIAL(file)>;
   necessity:<PENDING|PARTIAL>; better:PENDING", "method_commit":"<commit hash if the claim names one>",
   "notes":""}`
   Conclusion levels (weakest→strongest): identity < target < posterior < reported-model < delivery; "negative"
   for NEG/obstruction results. posterior = π(S₀|y)→1 type; reported-model = reported Ŝ = S₀ jointly with the
   output event; delivery = P(Ŝ⁺ = S₀) → 1 with fallback/allocation.
3. `sharpness.tsv` (header `claim	assumption	verdict	evidence	notes`), for each (headline, assumption):
   verdict NECESSARY | NECESSARY-FOR-ROUTE | FAILED-REMOVAL | ARTEFACT | WEAKENABLE | NONE; evidence = claim id
   (e.g. W2-FAC-A:Prop-SHARP, W2-APP:VN, W2-APP:Ex-STAR, W2-FAC-PK:Thm-NEG, W1-GEN:Cex-GEN(C6)) or path:line.
   One row per piece of evidence (several rows per pair allowed). NONE if no necessity evidence is recorded.
4. `binding.tsv` (header `headline	assumption	binding_claim	mechanism	signals	notes`): for each headline
   assumption, the claim (usually a lemma) whose proof FORCES it and how (mechanism ≤ 150 chars: union bound over
   the lattice, balancing exponent, worst-case Gram bound, ...). signals = any of: boundary-numerics,
   artefact-threshold, single-use-union-bound, family-named, literature-dominance, prover-divergence,
   unharvested-conclusion (";"-separated) that the files suggest, with the reason in notes.

## Finish
Final message (≤ 20 lines): counts, the shared assumptions you found, MISSING bridges, and every place you were
unsure. Do not paste the files.
