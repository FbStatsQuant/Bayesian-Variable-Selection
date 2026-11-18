Scope: the supplied fix diff, disposition, affected passages and cited source lines only; no full-document or PDF re-read.

| Finding | Verdict | Reason |
|---|---|---|
| D2-01 | RESOLVED | Both remarks now use the root mean square of the one-observation Hellinger distances, matching [W3-POST2/STATEMENT.md:105](/home/fb31/BVS-wt/WRITING/Theory_work/Wave3/W3-POST2/STATEMENT.md:105) and [W3-MISR-R/STATEMENT.md:34](/home/fb31/BVS-wt/WRITING/Theory_work/Wave3/W3-MISR-R/STATEMENT.md:34); the contraction conclusions are unchanged. |
| D2-02 | RESOLVED | The local-search paragraph now includes the additional scan after the last allowed move, certification when it finds no improvement, and an uncertified improving-neighbour return otherwise, matching [v3_engine.h:407](/home/fb31/BVS-wt/WRITING/Scripts/SMC_BVS/core/cpp/v3_engine.h:407) through line 414. |
| D2-03 | RESOLVED | The remark's own status note now explicitly marks the composition for (ii)–(iii) as awaiting its final independent check, carrying the NEW status of B4.4 in [READER_VERSIONS.md:543](/home/fb31/BVS-wt/WRITING/.rc_tmp/d2_sources/READER_VERSIONS.md:543). |
| D2-04 | RESOLVED | The overview now explicitly states the random-design posterior-miss bound in probability and HPM/MPM recovery, matching [READER_VERSIONS.md:279](/home/fb31/BVS-wt/WRITING/.rc_tmp/d2_sources/READER_VERSIONS.md:279), without extending the fixed-design expectation bound. |
| D2-05 | RESOLVED | The revised in-words paragraph specifies indicator-multiplied errors of order $\rho_n$ in probability, relative/log evidence errors and intersection probabilities; the overview explicitly excludes conditioning, and Table 1 summarises that qualified statement, matching [READER_VERSIONS.md:1241](/home/fb31/BVS-wt/WRITING/.rc_tmp/d2_sources/READER_VERSIONS.md:1241) through line 1248. |
| D2-06 | RESOLVED | The penalty approximation is now attributed to the determinant contribution alone, with the fit contribution able to outweigh it, consistent with the two separate terms in [CODE_FACTS.md:37](/home/fb31/BVS-wt/WRITING/.rc_tmp/d2_sources/CODE_FACTS.md:37). |
| D2-07 | RESOLVED | The added assertion that no candidate model contains the true regression function is removed; the replacement restores the reader example's wording about the full model and candidate-only fit at [READER_VERSIONS.md:469](/home/fb31/BVS-wt/WRITING/.rc_tmp/d2_sources/READER_VERSIONS.md:469), without changing the Gaussian reduction formulas. |
| D2-08 | RESOLVED | The ledger now identifies the existing `W3-POST:Lemma-1a'@1.0.0` row and preserves its unchecked status, matching [claims.tsv:343](/home/fb31/BVS-wt/WRITING/Theory_work/INFRA/registry/claims.tsv:343); the same correction is present in [status_ledger.tex:5](/home/fb31/BVS-wt/WRITING/Docs/Writing/results/status_ledger.tex:5). |

| Sync hunks | Verdict | Reason |
|---|---|---|
| Notation and asymptotic definitions | CLAIM-NEUTRAL | Changing the generic matrix letter from $B$ to $\Lambda$ preserves the submatrix definition; moving the asymptotic definitions preserves their quantifiers and meaning. The added $\gtrsim$ definition is the reverse of $\lesssim$, and the replacement pointer retains access to the definitions. |
| Posterior and evidence display | CLAIM-NEUTRAL | The retained definition of $F$ gives $e^{F(S)}=w(\lvert S\rvert)m(S)/\bar w_K$; therefore the new posterior and sum defining $Z$ are algebraically identical to the old ones, including the evidence's absolute normalisation. This also matches [CODE_FACTS.md:40](/home/fb31/BVS-wt/WRITING/.rc_tmp/d2_sources/CODE_FACTS.md:40)–41. |
| Temperature subscripts | CLAIM-NEUTRAL | Replacing $\phi_t$ by $\phi_{[t]}$ changes only the indexing typography; the ordered grid, endpoints and intermediate distributions are unchanged. |

New problems introduced by the reviewed hunks: none found.

RECHECK: ALL-RESOLVED
