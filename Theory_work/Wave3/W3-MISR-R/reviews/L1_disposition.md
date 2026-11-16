# L1 disposition (statement lock; reviewer Sol gpt-6.1-sol high, fresh, blind; verdict LOCK-WITH-AMENDMENTS)

Reply verbatim: `L1_statement_lock_sol.md`. Lead: Claude Opus 5.5. All findings accepted; STATEMENT v1.0 → v1.1 (locked).

| finding | severity | disposition | where |
|---|---|---|---|
| L1-1 row-wise KL reading too broad with a design-dependent intercept | MAJOR | ACCEPT; the reviewer's sentence adopted verbatim (deterministic α and (E1) parameters) | STATEMENT §4, KL reading (ii) |
| L1-2 "neither … can be non-Gaussian" overstated (marginal scale mixtures) | MINOR | ACCEPT; reviewer's wording adopted ("Gaussian conditionally on the candidate design") | STATEMENT §2(d) |
| L1-3 conditional-mean remark needs a convention without moments | MINOR | ACCEPT; mean of the regular conditional law, no integrability assumed | STATEMENT §2 remark |
| L1-4 g_n formulation (N-dim contrast vs n-dim response; zero contrast) | MINOR | ACCEPT; Ψ(x, u) := Π(· \| x, Uu) as BASE (R3), fixed Borel kernel at zero contrast | PLAN §1, H2 (RD) |
| Q1 note: MIS-R (ii) slices cover bounded sizes; class/event hypotheses still required | — | ACCEPT; parenthesis in §2(a) | STATEMENT §2(a) |
| Q5 note: cite [W3P] :18-22 for column standardisation; name Cramér in §7 | — | ACCEPT | STATEMENT §7 |
| Q5 scope note: registry status strings not verified by the reviewer | — | NOTED; the strings in §7 were copied from `Theory_work/INFRA/registry/claims.tsv` on origin/main (e5d802a) on 2026-11-15 by the lead | — |

Lead addition after the lock (not seen by L1): [LA-1] CorH-U clause (G), changelog v1.2, NEW-CLAIM (clause); a
statement-change check (new Sol agent) is owed before the council freeze and is planned inside the line-check batch.
