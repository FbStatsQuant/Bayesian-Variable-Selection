# SMC-BVS: State of the Project — review questions

Answer each question using only the document "SMC-BVS: State of the Project". Be short and exact: give the key numbers, hypotheses, regimes, and status words, with their qualifiers. If the document does not state the answer, say so rather than guessing, and say where you looked.

**Q01.** What are the target-posterior settings of SMC-BVS v3.1: the g in the g-prior, the model-size prior, and the cap on model size?

**Q02.** How does the method build its "local-to-global" start π₀: how are the blocks formed and sized, what is computed exactly inside a block, and how is π₀ sampled? What block size did the 2,400-fit study use?

**Q03.** How is the reported HPM defined, and how are ties broken?

**Q04.** What is the default number of final islands R′? What does optional stacking change, and what must be true about it?

**Q05.** What is LS0, and what did it do to the study's outputs? Was it in the production code that produced the 2,400 fits?

**Q06.** In the low-p regime (n = 200, p ∈ {20, 30}, exact posterior by enumeration), how accurate is Ẑ, how often does the SMC HPM equal the exact HPM, and where does SMC-BVS rank on pooled exact recovery?

**Q07.** Decompose the 2,400 high-p fits (n = 200, p ∈ {500, 1000}) by outcome. How many were exact recoveries, posterior misses, search misses, and stopped fits? What are the stopped fits?

**Q08.** At high p, how does SMC-BVS (HPM) rank against the benchmarks at c = 0.5 versus c = 1?

**Q09.** What does the N200 account predict for the number of wrong reported models at n = 200, how does it compare with the observed count, and what status does the prediction rest on?

**Q10.** What did the confirmatory start test (ABL-CONF) find about the prior start and about the block start's cost? Which claim is licensed and which is not?

**Q11.** The study reports "0 search misses". Is that an identified fact at high p (p = 500, 1000), or is it qualified? How does it differ at low p?

**Q12.** M5(0) states a bound on P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) involving a term D_n. State the bound and say exactly what D_n means.

**Q13.** State the T03♯ conclusion (rate) and its main hypotheses.

**Q14.** At what sample size do the proof thresholds of the asymptotic selection theorem (T03♯) begin to apply, how does that compare with the study, and what is disclosed about the beta-min condition?

**Q15.** Which hypothesis excludes the study's own generator (groups of 5) from the LH-iid result (Theorem 5(b1) with LS0, p ≫ n included)? Why does it fail?

**Q16.** Define the "LH" design family used by the masked-regime theorems: group size, correlations, cross-group links, coefficients, noise, and how p grows with n.

**Q17.** Define the "W" reporting exhibit family (used for M1(i) and M2) and contrast it with LH.

**Q18.** In M6(b), how many iid draws from the block start π₀ are needed to discover the true model on LH, and what happens on either side of that scale? What does this result NOT cover?

**Q19.** What probability statement does M1(d) (and the certificate card) make about the evidence lower bound 0.05·Ẑ, and what reading is explicitly NOT licensed?

**Q20.** What blocks M1's accuracy statement for general bounded summaries h (as opposed to marginal PIPs)? Give its status and the fallback if it fails.

**Q21.** What is the status and cross-check level of API-PXNGAP, and what does it claim?

**Q22.** What does the Lean library certify, and is any main theorem card Lean-certified?

**Q23.** Which v3.1 outputs can NOT be claimed for the 2,400-fit study without further work?

**Q24.** Why was the literal T37 (truth dominance ⇒ greedy repair) abandoned, and what replaced it?

**Q25.** What happened to the claim that tempering (the bridge) is needed for the method to succeed?

**Q26.** Why was the backfit/residualised start rejected for paper 1, and which earlier argument was withdrawn?

**Q27.** Which two statements about Ẑ were corrected during the method meeting, and what is the corrected wording?

**Q28.** What is the status of the claimed separation from Song–Liang split-and-merge, what evidence exists, and what did HQ recommend?

**Q29.** What is the approval state of the paper-1 theorem list (at the end of the archive, and now)? What are the planned next steps and wave order, and what safeguard applies to binding goals?

**Q30.** What are the honest scope limits of M2 (the §5.3 weight-stability package): at what cross-block correlation scale are its constants useful, and what is and is not claimed about the stage count?
