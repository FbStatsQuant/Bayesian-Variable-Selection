# SW1 disposition (lead) — exhaustive sweep (Codex gpt-6-astra high, blind) and diff check RC5 (Codex gpt-6.1-sol high)

Manifest of the round: 90c988397325835d176455ad7673506964a507e0ac1c004f477d1472e34ba5bd (quoted by SW1, BT2, RC5;
`verify` OK after the round and before any edit). The ten texts changed afterwards are kept as the sweep read them
in `as_reviewed_by_SW1/`. BT2 has its own file, `BT2_disposition.md`.

## RC5 — `RC5_diffcheck_sol.md`
All 13 items of round LC2 RESOLVED; the symbol ϖ_n in place of the reviewer's λ_n accepted;
"ATTESTATION: editorial/record only — L4–L6 and STATEMENT v1.4 stand as reviewed in round LC2".

## SW1 — `SW1_sweep_astra.md`
Verdict: **SWEEP WITH FINDINGS — 0 FATAL, 2 MAJOR, 4 MINOR, 1 NIT.** Claim table: **(C1) RM2-F, (C2) RM2-R, (C3),
(C4) and every bridge VERIFIED**; (C5) examples and (C6) sharpness record VERIFIED-WITH-AMENDMENTS. Both MAJOR
findings are about records, not about a theorem. All seven accepted and applied (markers [SW1-#]).

| # | class | finding | action |
|---|---|---|---|
| 1 | MAJOR | STATEMENT §3 (and the imported hypothesis list of Theorem 1) reads "M, φ₀ ∈ (0, 1]"; the examples E3–E5 use an energy constant M > 1, so "every hypothesis verified" is false on the literal reading | the reviewer's remedy, in full: the constants now read "M > 0, φ₀ ∈ (0, 1]" (STATEMENT §3, `lemmas/L1_sandF_b.md` §0), and STATEMENT §3 carries the remark "Energy constant" with the response-rescaling argument (the method depends on the response only through y = Y/s_y; (aY, aθ*, aσ) with a²B ≤ 1 has the same scores, tables, start law, posterior and path; the signal-to-noise ratios and leak ratios are invariant; (V) holds with a²M_n). `L6_examples.md` points to it. No theorem's hypothesis domain shrinks; the examples stand as stated |
| 2 | MAJOR | B2 was presented as a certified, isolated violation of the width condition; (W) is not certified to fail on the realised designs, and the claim "leakage untouched" is false: Cov(O, H \| P_t) = −r√(s(1 − r²)/m) ≠ 0 | B2 is now called a nominal width-stress design everywhere (REPORT flag 6 and §5, SHARPNESS §4, SPEC, RESULTS); SPEC states the conditional covariance and that the leak is small but not zero. Counts and the LS0-only scope unchanged |
| 3 | MINOR | the LS0 re-implementation is called "as coded" but departs from production in three boundary branches (tolerance 1e-9; current centre returned at the cap; first-maximum ties) | the three departures are stated in SPEC and RESULTS; `final_size` of a capped probe is labelled the current centre at the cap; comments in `rm2_common.R` corrected (no code line changed, so no number changes) |
| 4 | MINOR | ASSUMPTION_MAP still described the unproved v1.3 package | header, the TL row and the binding bullet updated to the proofs as written |
| 5 | MINOR | L6's source ledger carried the removed dependency W3-RM:B9 and a stale line pin | corrected |
| 6 | MINOR | SHARPNESS §1 dropped a logarithm: the sample floors need q√(log n/n) → 0 | corrected, with the two conditions and their sources separated |
| 7 | NIT | L6 E5 called a shifted quantity an "unshifted width" | "width gap" |

## Other edits made with these (record only)
* `citecheck.py` added (modelled on the parent's): 92 citations extracted, **0 MISS** (`reviews/CITECHECK.txt`). Its
  first run found five citations whose path had no ticket abbreviation on its line (STATEMENT §5 ×1, REPORT §2 ×2,
  L5 ×2); the abbreviation was added in each. No cited range was wrong.
* REPORT §1, §4, §6: the sweep and better-theorem results and the recommended revision v1.5; SHARPNESS open-item
  rows O3′, O4′ (pointers to BT2 P6, P7); ASSUMPTION_MAP one stale word ("planned").
No hypothesis, claim, lemma statement, proof step, constant or code pin changes. The one hunk with mathematical
content is the "Energy constant" remark ([SW1-1]), which the sweep itself asked for; it is checked, with every
other hunk, by an independent Sol diff check (RC6) in the council round (PROTOCOL rule 15).
