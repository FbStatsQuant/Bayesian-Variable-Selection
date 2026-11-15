# Brief ACC (Sol, correctness check of a registry transcription) — W3-RM2, HQ 2026-11-12

You are a careful verifier (Codex gpt-6.1-sol, reasoning effort high). Read-only except for writing ONE output file.
Task: check that a registry carrier transcribes the frozen W3-RM2 registry block faithfully, field by field.

Frozen source (inside council manifest MANIFEST_R1 00bbeab8…; do not edit):
- `C:/Users/felip/BVS-wt/W3-RM2/Theory_work/Wave3/W3-RM2/REPORT.md` lines 153–236 ("Registry block", 18 claims)
- the files it refers to: `.../W3-RM2/STATEMENT.md` (sections §1, §3.1, §3.2, §4 claims (C1)–(C5) incl. the bridge table,
  §5), `.../W3-RM2/lemmas/L6_examples.md` (E2–E5), `.../lemmas/L4_sandR_b.md`, `.../lemmas/L5_formR.md`,
  `C:/Users/felip/Bayesian-Variable-Selection/Theory_work/Wave2/W2-LOC2/lemmas/L2_NAR.md`.
Carrier to check: `C:/t3j/d/Theory_work/INFRA/registry/fragments/W3-RM2_accept.md` (its header states the rules), and
its status source `C:/t3j/d/Theory_work/Wave3/W3-RM2/CHECKPOINT_4.md`.

Allowed differences (HQ decisions — do NOT flag these as mismatches, but do check they are applied as stated):
1. Grammar only: one claim per block; `STATEMENT.md:(C1)`, `§1` etc. resolved to `path:a-b` line spans; spaces in
   depends_on use labels hyphenated; content the grammar cannot carry (assumption/property ids not in the registry,
   sharpness, binding, assumption-level implies, bracket notes) moved verbatim into `notes`.
2. Status / status_source: CHECKPOINT_4.md lines; 16 claims PROVED-CHECKED with the R1 council cell; Ex-PolyR and
   Ex-PolyF unchecked ("PROVED; line-checked LC2-C; Astra seat ACCEPT; not examined by the Opus seat — next council
   round"). `council` field added; `correct:PENDING` → `correct:PASS(<both council reviews>)` on RM2-F/RM2-R.
3. `implies` over W3-RM:RM-F / RM-R not recorded (kept as text in notes).
4. Template edges W3-RM:SAND-R (on SAND-R-b), W3-RM:D-loc and W2-LOC2:NA-R (on D-to-W) are note edges only (no
   depends_on), with the reasons and line references given in the notes.
5. Conditions: SOP:TH09 on RM2-F and claims that use it (Cont-F, Ex-PolyF, Ex-Proxy, Ex-Equi); W2-APP:POST@hyp on
   RM2-R, POST-R and claims that use them (Cont-R, Ex-PolyR); W2-LOC2:Lemma-BC/Lemma-IR @hyp on Ex-PolyR/Ex-PolyF.
   §5 (STATEMENT.md:290-312) added as a premise span where the hypothesis is named (RM2-F, RM2-R, POST-R).

Check, for each of the 18 claims: (a) the statement span is exactly the text the block's reference denotes (not more,
not less — report the right span if not); (b) premise spans correspond to the block's premises (plus the allowed §5
span); (c) kind, depends_on (ids, uses) match the block apart from allowed changes; (d) notes reproduce the block's
assumptions / consumes / sharpness / binding / implies text verbatim; (e) conclusion / rate / scope verbatim; (f)
status text and conditions as in rules 2 and 5, and the status_source line holds exactly that status; (g) the line
references inside the notes of rule 4 (L4_sandR_b.md:12, L5_formR.md:108-117, L2_NAR.md:79-85, 102-105) say what the
notes claim. Also say whether any claim in the block is missing or added.

Output: write `C:/Users/felip/BVS-wt/W3-RM2/Theory_work/Wave3/W3-RM2/reviews/ACC_carrier_match_sol.md` with a table
`| claim | verdict | finding |` (verdict MATCH or MISMATCH; for a mismatch give the exact fix), then an overall line
`ACC-VERDICT: ALL-MATCH` or `ACC-VERDICT: MISMATCHES=<n>`. Change no other file. Your final message: the overall line
plus each mismatch in one line.
