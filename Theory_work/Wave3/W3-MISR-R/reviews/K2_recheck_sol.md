**K1-2 — RESOLVED.** In [H1_plus.md:50](/home/fb31/BVS-wt/W3-MISR-R/Theory_work/Wave3/W3-MISR-R/lemmas/H1_plus.md:50), both cutoffs are now n ≥ 9. Since log n/n decreases for n > e and log 9/9 ≈ 0.244136 < 1/4, the variance ratio lies in the domain of (KL). Off the stated bad set, (KL) gives k̄_n ≤ (1 + C_H/2) log n/n, proving the claimed inclusion. The auxiliary sequence √log n still diverges, so the posterior convergence follows unchanged.

**K1-3 — RESOLVED.** In [H2_uniform.md:25](/home/fb31/BVS-wt/W3-MISR-R/Theory_work/Wave3/W3-MISR-R/lemmas/H2_uniform.md:25), the refinement by supp β = T is Borel: it imposes β_j ≠ 0 for j ∈ T and β_j = 0 otherwise. At fixed p there are finitely many supports and models. On each refined stratum, the selection event is the discrete event S ≠ T, and the remaining comparisons involve continuous functions for each fixed S. Integrating their Borel indicators against the jointly Borel posterior density on each model-specific coefficient space, then summing over models, gives Borel g_n on nonzero contrast. Its zero extension is Borel as well. Thus the joint measurability required by freezing is justified.

**Other effects.** No new findings. H1.2 retains its constants, set thresholds and asymptotic conclusions; H2.2's use of H1.2 is unaffected. H2.0 retains its posterior kernel, equality-in-law statement and null-set convention; its uses in H2.2 and H2.4, and subsequent consequences within the two files, remain valid.

**Change completeness.** Applied the supplied repair diff in memory to its committed base blobs, `0240624a` for H1_plus and `6f58f133` for H2_uniform. The results match the current files byte for byte, with target blobs `88222f9d` and `4d4b901b`, respectively. The supplied diff is the only change relative to those K1 versions.

The verdicts below cover this repair re-check and preserve the lemmas' declared dependency conditions. Both corresponding DEPS.tsv rows are STALE as stated; no registry file was modified.

| lemma | verdict |
| --- | --- |
| H1_plus | VERIFIED |
| H2_uniform | VERIFIED |

K2-VERDICT: 2 RESOLVED; 0 NOT RESOLVED; 0 new findings (0 FATAL, 0 MAJOR, 0 MINOR, 0 NIT); 2 VERIFIED; 0 NOT-VERIFIED.
