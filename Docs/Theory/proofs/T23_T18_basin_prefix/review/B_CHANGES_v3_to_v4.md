# Changes from PROOF_v3 to PROOF_v4 (after Stage B round 3)

Both reviewers ruled PROOF_v3 verified with no fatal or gap finding. Astra #2 had no findings. The Opus reviewer had two exposition findings; the lead accepted both. Wording only: no change to any argument, hypothesis, conclusion or constant. Script: helpers/make_v4.py.

| Round-3 finding (Opus) | Lead's judgment | Change in PROOF_v4 |
|---|---|---|
| F1: σ-fields defined by variates "drawn before" a moment fail if variates are generated in batches ahead of use; for rejection-type choices, refer to the fresh sequence | Accepted | 𝒟_c, 𝓕ⁱ_s and 𝒟₀,…,𝒟_m are now defined by the variates *used by the random choices made before* the relevant moment (consumption order). (F) now speaks of "the fresh variates from which c is made (a sequence, if c uses a random number of them)". A sentence adds that variates are attributed to the choice that uses them, so (F) is unaffected by batching, processing order or sub-streams. |
| F2: X^{(t)}_{i,·} indexed both by measured round h (§1, Lemmas 2, 5) and by terminal round s+1 (Lemma 1) | Accepted | Lemma 1 now writes terminal-round paths as Z^{(t)}_{i,s+1}, with the link X^{(k)}_{i,h} = Z^{(k)}_{i,L+h}. Lemma 5 cites Lemma 1 "with s = H (the path of measured round h is Z^{(·)}_{i,H+1})". |
