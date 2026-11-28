PURE check of `T7/T7-1_correction.patch` (fresh Opus subagent, claudeAgent_personal, high; scratch in `.rc_tmp/t71/`). Verbatim report (harness indent removed):

PURE-VERDICT: PURE
1. `git apply --check` passes. I applied the patch to a scratch copy (`.rc_tmp/t71/new.md`). It still has 1458 lines. A character-level word-diff shows one change on line 470: `, provided the $\sigma^2_{\mathcal C}$ below is positive (for instance $\sigma^2>0$),` is inserted between "(A0) holds" and " with". Nothing else changes.
2. The inserted text, LaTeX macros included, is exactly the card's row T7-1 column (c) (`FABLE_CARD.md:11`).
3. The sentence is now true. Line 465 of Theorem 4's (A0) requires $\sigma^2_{\mathcal C}>0$. Line 472 defines $\sigma^2_{\mathcal C}=\sigma^2+\beta_M^\top(\Sigma_{MM}-\Sigma_{MC}\Sigma_{CC}^{-1}\Sigma_{CM})\beta_M$. The bracket is a Schur complement of a covariance matrix, so it is positive semidefinite and $\sigma^2>0$ is enough.
4. The card's counterexample holds: take an omitted column equal to a candidate and $\varepsilon=0$. The Schur complement is 0, so $\sigma^2_{\mathcal C}=0$ and (A0) fails. The old wording was therefore false at $\sigma^2=0$.
5. The new proviso matches the master. `W3-MISR-R/STATEMENT.md:57-60` allows $\sigma^2\ge0$ and requires $\sigma^2_{\mathcal C}=\sigma^2+\tau^2>0$, which is the same condition. The proviso also carries over to the two later sentences that begin "the same holds" (the Moore–Penrose case and noisy-linear omitted predictors).
6. Theorem 4's statement (lines 447-466), the other lines of the example (467-469, 471-475) and the Remark are untouched.
7. Registry, reported only, not edited: line 470 lies inside the premises span `READER_VERSIONS.md:444-564` of `W3-READER:R1` in `Theory_work/INFRA/registry/claims.tsv`. It is in no other W3-READER premises span. So R1's premises hash and cascade need the recorder, as the patch header already says.
