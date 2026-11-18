# W3-D3 — K1 disposition (lead, 2026-11-17)

Reply: `reviews/K1_linecheck_opus.md` (Opus 5.5 high, claudeAgent_personal, fresh, blind): B3w.md, ASSEMBLY.md and STATEMENT
v1.1 VERIFIED-WITH-AMENDMENTS; statement-change table: 5 rows CONFIRMED, row 2 CONTESTED (K1-8); window arithmetic re-run
(859 cases, 0 violations) and ExSG (b) bounds checked numerically by the reviewer. All findings accepted; STATEMENT v1.2.
Repair diff: `reviews/K1_repair.diff`.

| finding | disposition | where |
|---|---|---|
| K1-1 [C, minor] completed truth θ⁰ arbitrary ⇒ item 6 speaks of supp θ°, ASSEMBLY of S₀ | ACCEPTED as specified: θ⁰ with supp θ⁰ = S₀; supp θ° = S₀ on every outcome; ASSEMBLY Step 3 sentence added | STATEMENT §2 (c); B3w Step 6; ASSEMBLY Step 3 |
| K1-2 [F] quotations of B1 (a), B2-core altered K⁴ → L⁴ | ACCEPTED: K⁴ restored inside the quotations; "read with K := L" added | B3w "Inherited results" |
| K1-3 [S] "and so" in §2 (c) | ACCEPTED: replaced by "Moreover (with (b) …) … in regime R1" | STATEMENT §2 (c) |
| K1-4 [E] integer remark | ACCEPTED | B3w Step 0 (1) |
| K1-5 [E] target version; "Fix n ≥ 3" | ACCEPTED | B3w header; ASSEMBLY Step 1 |
| K1-6 [E] measurability wording | ACCEPTED (moot after K1-1; wording updated, support fixed at S₀) | B3w Step 6 "Events" |
| K1-7 [E] changelog rows missing | ACCEPTED: one row added as proposed | STATEMENT §9 |
| K1-8 [S] B3w (c) is an added conclusion | ACCEPTED: row 2 retagged STRONGER on B3w, EQUAL for Theorem 2SG | STATEMENT §9 |
| K1-9 [E] converse example also violates (A3) | ACCEPTED: note added | STATEMENT §5 |
| K1-10 [E] (A3) parenthetical dropped | ACCEPTED: restored verbatim | STATEMENT §1 |
| K1-11 [E] commentary inside a span | ACCEPTED: moved to remark §4 (f) | STATEMENT §2, §4 |
| K1-12 [E] "qualify" | ACCEPTED: glossed "satisfy (A4)"; Theorem 2SG also needs (A3) | STATEMENT §5 |

Also in v1.2 (lead; citecheck): off-main W3-AUDIT paths written as plain text with the branch; three bare `:a-b`
references given their alias on the line; B3's registry status quoted in full. citecheck 70 checks, 0 failures; staged
ingest 0 problems, acceptance PASS.

DEPS: rows whose span did not change since K1 read it (S:setting, S:ExSG, P:ExSG) are marked checked by K1; the repaired rows
(S:Thm2SG, S:B3w, S:class, S:inputs, P:B3w, P:Thm2SG, R:registry) go to the K2 re-check (new Opus agent).
