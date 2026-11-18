MODEL: gpt-6.2-astra (codex, reasoningEffort high)
VERDICT: FLAWS-FOUND

1. T3-1 | FLAW | [P6_DISTC.md:71](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-215eb534-a080473e9c42fff9/Theory_work/Wave3/W3-DIST/work/D_output/P6_DISTC.md:71) | The positivity proof infers \(m(S)<\infty\) from a strictly positive likelihood and a proper prior. Those facts prove \(m(S)>0\) but do not give an upper bound. Minimal fix: bound the Gaussian likelihood by \(C_n v^{-d/2}\), where \(d\) is the likelihood dimension. The conditional slab has mass one, and the positive-rate inverse-gamma prior has finite \(\mathbb E[v^{-d/2}]\). This supplies finiteness for every \(S\). Severity: local.
2. T3-2 | LEAN-COMPILE | [P6_DISTC.md:158](/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/t3-215eb534-a080473e9c42fff9/Theory_work/Wave3/W3-DIST/work/D_output/P6_DISTC.md:158) | Ordinary real-valued Jensen requires integrability in \(\xi\), which can fail at a fixed \((x,y)\). For the empty model, put mass \(2^{-k}\) at \(v=4^{-k}\), \(k\ge1\). At \(y=\bar y^r\), every atom contributes \(1/\sqrt{2\pi}\) to the mixture density, so its value is infinite. Minimal fix: define the nonnegative mixture by `lintegral`. Its total integral is one by line 158, hence it is finite \(\mu\)-almost everywhere. On that full-measure set \(g_\xi(x,y)\) is \(Q\)-integrable, and so is its square root by \(\sqrt u\le 1+u\). Apply Jensen there and integrate. The predictive bound is unchanged. Severity: local.

CHECKED:

- P6(a) uses the finite tower identity for measurable \(B\) and a conditional kernel defined at every model. At a \(\pi\)-null model its value is immaterial because domination forces \(Q(S)=0\).
- Summing the domination hypothesis gives \(1\le L\). This rules out \(L=0\), \(L<1\), and, on finite \(\Omega\), any \(Q\) lacking absolute continuity with respect to \(\pi\).
- P6(b) divides only by \(a>0\). Models at equality are excluded by the strict threshold, and the restricted-sum argument covers an empty bad set.
- P6(c) has joint measurability by continuity on each Borel piece of the finite disjoint union. Tonelli gives unit mixture mass, and the almost-everywhere Jensen inequality has the stated direction.
- Splitting the average squared Hellinger distance over \(A\) and \(A^c\) gives \(Q(A)+\varepsilon^2Q(A^c)\le Q(A)+\varepsilon^2\).
- The normal affinity follows from the completed square and Gaussian integral in H.md, lines 48–53. Its exponent has denominator \(4(v+\sigma_*^2)\).
- For every \(r=v/\sigma_*^2>0\), \(A,B\in[0,1]\), the product remainder is \(-(1-A)(1-B)\le0\), and \(1-A\le(\sqrt r-1)^2/(1+r)\le(r-1)^2\). This covers \(r=1\) and arbitrarily small or large positive \(r\).
- The exponential bound and \(v+\sigma_*^2\ge\sigma_*^2>0\) give \(1-B\le\min\{1,\Delta^2/(4\sigma_*^2)\}\). The clipped affine-error term is Borel and bounded even when \(\mathbb E_x\Delta^2=\infty\).
- Dropped columns vanish after sample centring and can still contribute at a new \(x\). In sample, the zero sum of \(\hat\mu-\mu\) kills the cross term with \(\bar\varepsilon\).
- D0 averages the centred mean errors, yielding \(\|\hat\mu-\mu\|^2/(4n\sigma_*^2)\). The plug-in intercept adds \(\bar\varepsilon^2/(4\sigma_*^2)\) to the in-sample upper bound.
- In (C-0), a completed run has a nonempty store and positive atom masses. Exact scores give the normalized restriction and justify both reciprocal domination constants.
- In C-i°, \(\pi(\mathcal T)\ge a>0\) excludes an empty or zero-mass store. Division gives \(\varrho_n/a\), including at \(a=1\).
- In (C-ii)(α), an offered model of mass strictly above \(1/2\) is the unique maximizer, so the ledger retains and reports it. For Cor-C’s raw true model, the scoring premise already requires all its columns to have survived.
- In (C-iii), the HPM has mass at least that of the hit model, strictly above \(\sqrt{\varrho_n}\), while the entire bad-model set has mass at most \(\sqrt{\varrho_n}\) on the success event. This also covers score ties and \(\varrho_n=1/4\).
- Cor-C uses one data-only success event from Theorem A(i). On each data set in it, division by any qualifying store mass gives \(n^{-cM}/n^{-cM/2}=n^{-cM/2}\) simultaneously for every completed run. No union over seeds or stream independence is needed.

COUNT: 2
