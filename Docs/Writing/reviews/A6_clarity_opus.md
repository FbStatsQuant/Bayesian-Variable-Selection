# A6 owner-review edition: fresh-reader clarity review (Opus)

Reviewer: a statistician new to the project, reading for the owner's two questions
(Q1: do the assumptions make sense? Q2: do the theorems look natural and intelligible?).
Source: `.rc_tmp/a6/owner_review_clarity.pdf` (49 pp.), main text pp. 1–26 read closely;
supplement read only where the main text points (Remarks A.2, A.17/(NL), A.20; Appendix B).
Scope: clarity only. Suspected mathematical problems are listed separately at the end and were not checked.
Page numbers are PDF page numbers. Findings are ranked within each list, most important first.

---

## 0. The three fixes that matter most

1. **Two clashes in numbering and labels** (see 1.1, 1.2). Results 1–6 are Theorems 5, 6, 7, 8, Proposition 10 and Theorem 11,
   and Assumptions 3 and 4 have items (a)–(e) that collide with the entry parts (a)–(e). A reader loses their place in exactly
   the sections that answer Q1 and Q2.
2. **Assumption 4 (p. 15–16) is not explained in words.** Part (b) "In words" leaves out the locality condition (ii),
   describes (c) wrongly ("within Q", but l ranges over all of [p]), and does not explain the size condition or the constants
   b, b_H. Result 3 depends on this entry, and it is the one assumption the owner most needs to judge (see 4, Assumption 4).
3. **The main text never says which designs are "without leakage"** (pp. 2, 8, 9). The supplement (§A.5, (NL)) says that
   only the independent designs qualify. So no correlated design has a consistency guarantee for the reported PIPs or evidence.
   The owner should read this on p. 2, not on p. 33.

---

## 1. Sentences I had to read twice

**1.1 (pp. 17–22, whole of Section 6; Table 5). Three numbering systems.** "Result 1 … Theorem 5", "Result 4 … (Thm 8)",
"Result 5 … (Prop. 10)", "Theorem 8 requires n ≳ 1,450" (p. 21), "Remark 9", and the registry uses yet another numbering
(App. E: "Theorem 2 = Theorem 5"). On every cross-reference I had to look up which Result a Theorem is.
*Hard because:* Lemma, Example, Assumption, Theorem and Remark share one counter, so the theorem numbers are offset from the result numbers.
*Fix:* number the main statements Theorem 1–6 to match Results 1–6 (or call them "Theorem R1 … R6"). Give Lemma 1, Example 2 and
Remark 9 their own counters, or rename them. Also say once: "Result k is Theorem k."

**1.2 (p. 14, Assumption 3; pp. 15–16, Assumption 4). Item labels collide with entry parts.** For example, p. 16: "(b) In words.
(a) Only a small set Q … (b) The leakage set is not collinear … (c) Within Q …", and p. 14: "(b) In words. Items (a)–(c) are …
Item (d) asks only …" sits directly above "(d) Reasonable?".
*Hard because:* "(d)" means two different things within a few lines.
*Fix:* label the assumption's items (i)–(v) (Assumption 3) and 4.1–4.3 (Assumption 4), or label the entry parts with words only
("Statement / In words / Rules out / Reasonable? / vs Song–Liang"), without letters.

**1.3 (p. 15) Assumption 4(a)(ii), locality.** "every l ∉ Q has a deterministic H_l ⊇ {l} ∪ S0 with |H_l| ≤ n^{b_H}, such that for all
l ∉ Q, all U ∌ l with |U| ≤ 15 and U0 := U ∩ H_l: |Cov(W_l, W_v | W_{U0})| ≤ r_n and |Cov(W_j, W_v | W_{U0})| ≤ r_n for all v ∈ U \ H_l
and j ∈ S0 \ U0."
*Hard because:* the "In words" part does not translate it ("only its nearby predictors matter").
*Fix (add to In words):* "(ii) Each predictor l outside Q has a neighbourhood H_l (at most n^{b_H} predictors, containing l and the true
predictors). Once the part of U inside that neighbourhood is held fixed, the predictors of U outside it are nearly uncorrelated
with l and with the true predictors. So conditioning on far-away predictors changes nothing that matters."

**1.4 (p. 16) "In (a), 32s0 = 2 · 16s0: with probability tending to one the start mode has at most 2(|Q| + 16s0) predictors, so the size
condition leaves room to add a missing true predictor to it."**
*Hard because:* Result 3 says that the start mode contains S0, so why would a true predictor be missing? Also, the alternative "Q = [p]"
in the same condition is not explained.
*Fix:* "The size condition K ≥ 2|Q| + 32s0 + 1 makes sure that the size cap K never blocks a move of the local search: the start mode has
at most 2(|Q| + 16s0) predictors (with probability tending to one), so the search can always add one more. When Q = [p] the
condition is not needed because …" (fill in).

**1.5 (p. 14) (EF_Σ)(e).** "For a fixed design, whose sets here have a fixed size, their sets are no larger only for their Theorem 1 and
Theorem S, since their Theorem 2, and so their Theorem 3, assume r_n → ∞ (p. 953); for random rows our sets grow like log n, so the
comparison applies whenever r̄_n ≲ log n."
*Hard because:* four theorems, two set sizes and two design types are packed into one clause chain.
*Fix:* state it as a short case list. "Fixed design: ours is stronger than their Theorems 1 and S, and not comparable with their
Theorems 2–3, which take r_n → ∞. Random rows: ours is stronger when r̄_n ≲ log n, and not comparable otherwise." Move the page
citations to a footnote.

**1.6 (p. 7) Section 4.3, first sentence.** "A run either produces output, with status “exact” (enumeration) or “completed” (sampler; a
completed run), or stops without estimates (a run stopped by its time guard is one; anything else it returns is flagged incomplete,
and the results do not cover it)."
*Hard because:* the nested parentheses, and "anything else it returns" has no clear referent. "Time guard" is not defined anywhere.
*Fix:* "A run ends in one of three ways: *exact* (Ω was enumerated), *completed* (the sampler ran to the end), or *stopped* (for
example by the time guard, which stops a run that exceeds its time allocation). A stopped run reports no estimates; any partial output
is flagged incomplete, and no result covers it."

**1.7 (p. 2) "What is not claimed."** "Statements about a run’s estimates concern the event that its calibration succeeds, or that the
run completes; no lower bound on the probability of that event is claimed, except that under Convention (C2+) every run produces
output."
*Hard because:* "that event" could refer to either event, and (C2+) is undefined until p. 17.
*Fix:* "Results about a run's estimates hold on the event that the run's calibration succeeds (or that the run completes). We do not
bound the probability of that event. The one exception: on an idealised computer (Convention C2+, Section 5.6) every run produces
output."

**1.8 (p. 17) Theorem 5, conventions for removed columns.** "Assume (GL), (DIM) with p = p_raw (the bound on the number of raw
predictors) … on the event that the method removes a column, set PIP_j := 0 for a removed column j and π(S0 | y) := 0 if S0 ∉ Ω, and, if
no column is retained, take the posterior to be a point mass at ∅."
*Hard because:* bookkeeping for a rare event sits inside the main theorem, and "(DIM) with p = p_raw" reads as an equation.
*Fix:* move the conventions to a sentence before the theorem ("When the method drops a constant column we set …"), and write
"(DIM) applied to p_raw".

**1.9 (p. 13) (SG)(d).** "(SG) holds for Gaussian rows and for correlated mixtures x = m_n + Bξ (BB^⊤ a correlation matrix) of independent
features confined to K standard deviations of their mean, with one common K".
*Hard because:* K is the size cap and ξ is the temperature everywhere else.
*Fix:* "…of independent features ξ_k, each within c standard deviations of its mean, for one fixed c (so bounded data such as genotypes
qualify)". Use letters that are not taken (c, η).

**1.10 (p. 15) (V)(d)(ii).** "generic coefficients: for designs with finitely many local correlation patterns, every coefficient vector
outside one fixed null set of hyperplanes."
*Hard because:* "null set of hyperplanes" and "local correlation patterns" are both undefined. Remark A.20 also says "countably many",
not "finitely many".
*Fix:* "(ii) generic coefficients: if the design is built from a fixed list of local correlation patterns (block types, AR, banded),
visibility holds for every coefficient vector except those on finitely many hyperplanes (a set of Lebesgue measure zero)".

**1.11 (p. 16) Assumption 4(d).** "The bound b < 1/2 comes from the proof: at model size about √n the penalty of one more predictor stops
dominating the best of p noise gains".
*Fix:* "Adding a predictor to a model of size k costs about log(2p/k) in prior odds plus ½ log n in Occam factor. Once k passes √n this
total falls to about log p, which is what the best of p null predictors gains by chance. So the proof cannot keep models larger than
about √n from growing, and it needs |Q| ≤ n^b with b < ½."

**1.12 (p. 7) Stage 6.** "It stops at the first scan with no strict improvement and certifies its end point; after its last allowed move it
scans once more, and if a neighbour still improves it stops there, uncertified."
*Fix:* "If a scan finds no strictly better neighbour, the search stops and its end point is *certified* (a local optimum). If it uses up
its move cap first, it scans once more: the end point is certified if that scan finds no improvement, and uncertified otherwise."

**1.13 (p. 17) (C2+).** "…and the code’s two fixed integer limits on the move caps lifted (neither can be reached on any input R can
represent)."
*Hard because:* why lift a limit that cannot be reached? And "R" can be read as the reals or as R′.
*Fix:* "…and the two hard-coded integer limits on the move caps removed. This changes nothing in practice, since neither limit can be
reached on any input the R language can represent; it only simplifies the proof."

**1.14 (p. 17) (C1).** "a sample size n is admissible if some data set of that size is valid." *Fix:* say what makes a data set valid at
size n, or drop the clause and write "for every n ≥ 3" where (14) uses it.

**1.15 (p. 8) Reading the evidence.** "so by Markov’s inequality log(0.05 Ẑ) exceeds log Z, jointly with completion, with probability at
most 0.05." *Fix:* "…so, by Markov's inequality, the probability that the run completes and still reports a lower bound log(0.05 Ẑ)
above log Z is at most 0.05."

**1.16 (p. 6) Stage 1 threshold.** "With N0 := max(2500, n, p) and N0^c := ⌈512N0/2500⌉, if |Ω| ≤ (5N0^c + 4N0) p the method scores every
model". *Hard because:* the threshold has no stated meaning. *Fix:* add "…that is, when enumeration costs no more scores than the sampler
would" (if that is what it is), and move the formula to Appendix C.

**1.17 (p. 7) Calibration.** "the grid refines the pilot’s temperatures so that each step keeps an effective-sample-size fraction,
computed on a set of candidate models, of at least 0.90." *Fix:* "…the grid is chosen so that each step keeps at least 90% effective
sample size (computed on a set of candidate models; Appendix A.6)." Better still, move this to A.6: Table 2 says no theorem uses it.

**1.18 (p. 13) (FS_θ)(b).** "(FS_θ) fixes the effects on the standardised scale the method works on; it replaces (GL) and (SP) in
Result 3." *Hard because:* it reads as a signal bound, but it is a different data model. See 3.3. *Fix:* "(FS_θ) is a different form of the
data model: it says that the true coefficients are fixed numbers on the sample-standardised scale (θ* = Dβ*), not on the raw scale. Result 3
uses it in place of (GL) and (SP) because … (one line)."

**1.19 (p. 10) "Our designs" paragraph.** It packs eleven design labels, three studies and their parameters into one paragraph. Every
later (d) part sends the reader back to it. *Fix:* replace it with a small table (label | study | correlation | n, p, s0 |
λ_min(Σ_n) | sign pattern). The λ_min column can absorb the list in (EF_Σ)(d), and two more columns (inside (V)? inside Assumption 4?)
would answer Q1 at a glance.

**1.20 (p. 18) Result 1, "Why it is natural".** "…while the best of the p null predictors gains about log p in log fit; together these models
weigh of order √(log p/n)". See 3.1. *Fix:* "…each null predictor's fit factor e^{T_j²/2}, with T_j² ≈ χ²_1, has no finite mean, so the
sum over p null predictors is about p √(log p) rather than p. Multiplied by the prior factor (s0+1)/(2p) and the Occam factor n^{-1/2},
this gives a total of order √(log p / n) (Remark A.2)."

**1.21 (p. 20, Section 6.4 title).** "certified screening, the guarantee that needs neither condition". *Fix:* "…the guarantee that needs
no visibility or leakage condition".

**1.22 (p. 15) (V)(c).** "the signal of each, given nothing, is 1 − ρ". *Fix:* "each has covariance 1 − ρ with the signal (nothing held
fixed), which vanishes as ρ → 1".

**1.23 (p. 6) Stage 3.** "(draw the total size, then the size of each block backwards, then a subset of each block)". *Fix:* "…then the
size of each block, from the last block to the first, …".

**1.24 (p. 9) Section 4.5.** "The verdict was clean, under the scoring script as amended before scoring (the registered script printed a
weaker verdict because of a defect that an independent review identified)". *Fix:* cut it (see cut 1), or write "The engine matched
the method on all pre-declared criteria."

**1.25 (p. 22) Section 7, opening.** "The order is the owner’s: … both after the p = 10^6 mission. The Lean certificates are gated
separately on the owner’s word." *Fix:* "The owner has set the order: the trap theorem first, then the analysis at p = 10^7, both after
the p = 10^6 runs. Lean work starts only when the owner approves it."

---

## 2. Symbols and terms met before their definition, or never defined

| # | Term / symbol | First met | Defined? |
|---|---|---|---|
| 2.1 | "designs without leakage" / no-leakage condition (NL) | p. 2, also pp. 8, 9 (Table 2) | Informal "leaks" on p. 5. The formal condition (NL) appears only in the supplement, §A.5 (p. 33), which also says that only the independent designs satisfy it. **Never defined in the main text.** |
| 2.2 | Convention (C2+) | p. 2, p. 9 (Table 2) | p. 17, §5.6. Add "(Section 5.6)" at first use. |
| 2.3 | "the project's registry", "theory freeze", "registry row 1.2" | p. 1, p. 18 | Never defined for an outside reader. Section 8 uses it as known. Add one sentence on p. 1: "the registry is the project's list of statements and their review status". |
| 2.4 | "AR designs", AR(1) | p. 2 ("block and AR designs") | p. 10 ("AR(1) at 0.6"). "AR(1)" is never spelled out. Write "autoregressive (AR(1))" at first use. |
| 2.5 | Leakage set | p. 5 ("small leakage set (Section 6.3)") | p. 15, **§5.4, not 6.3**. Fix the cross-reference. Appendix B also lists §6.3 for Q, L(Q), H_l. |
| 2.6 | "time guard" | p. 7 (§4.3), p. 9 (Table 2) | Never defined. Stage 1 describes only the check before the run. |
| 2.7 | k_n | p. 11 (Table 4: "floor on k_n + s0 sets") | p. 16, §5.5. |
| 2.8 | "temperature" | p. 6 ("A step is one move … from one temperature to the next") | p. 7, eq. (9). |
| 2.9 | π_1, B (Figure 1) | p. 6 figure | π_ξ in (9), p. 7; B in Stage 2. |
| 2.10 | P_n (Song–Liang's number of predictors) | p. 4 ("λ_n = r_n/P_n"), pp. 12, 16 | Never defined. Add "P_n, their p". |
| 2.11 | r_n (two meanings) | p. 4: Song–Liang's prior parameter | Reused on p. 15, Assumption 4(a)(ii), for a different vanishing sequence. Rename one of them. |
| 2.12 | K and ξ reused | p. 13, (SG)(d) | K is the size cap (p. 3) and ξ the temperature (p. 7). Rename. |
| 2.13 | ϱ ("equicorrelation ϱ ∈ {0.5, 0.7}") | p. 21, Remark 9 | Not defined. ρ is used everywhere else. |
| 2.14 | R′, I_max, m ("no grid refinement (m = 1)"), "rebuilds", "20p stores", "candidate stores", "calibration floor", "fourteen seeded streams" | p. 9, Table 3 (p. 10) | I_max and "rebuild" are explained only in App. A.6 / C. R′, m, "calibration floor" and "stores" are never defined in the main text. Cut or define (see cut 1). |
| 2.15 | "worst-island bound" | p. 23 (§7.3), p. 24 (§7.4, Table 6) | Not in the main text. It is in Remark A.17(iii), p. 33. |
| 2.16 | "missed-signal result / family" | p. 24 (§7.4 item 3, "Possible strengthenings"), Table 6 | Never named in the main text. It seems to be Theorem A.7 (one-line list, p. 27). |
| 2.17 | "list-mass premise", "raw-scale bridge", "global-overlap premise", "the equicorrelated example below b = 3/8", "a count of the form 17 − s0" | p. 24, §7.4 | Only in the supplement, or not at all (I found no "equicorrelated example" in the main text). |
| 2.18 | "weighted tempered Gibbs sampler" | p. 22, §7.1 | Neither defined nor cited (presumably Zanella and Roberts). |
| 2.19 | "riboflavin gene-expression data" | p. 15, (V)(d) | Never introduced. Add "a public data set (n = 71, p = 4,088)" and a citation. |
| 2.20 | "beta-min condition" | p. 19 (Scope of Result 1) | Standard, but say that it is the lower half of (FS_β). |
| 2.21 | PIP-hat_{r,j} index r | p. 7 | r as the island index becomes clear only at (10). |
| 2.22 | "energy bounds" | p. 22, Theorem 11(b) | Self-explanatory from the formula. Fine. |
| 2.23 | "admissible run" | p. 17 (C1), used p. 20 | Defined before use. Fine, but (C1)'s definition is odd (see 1.14). |

---

## 3. Steps or claims I could not follow

**3.1 (p. 18) Result 1, where √(log p) comes from.** The paragraph says the best null predictor gains about log p in log fit. That alone
gives a factor e^{log p} = p, which cancels the prior factor 1/(2p) and leaves (s0+1)/(2√n), with no √(log p). The missing step (the
sum of p heavy-tailed fit factors) is only in Remark A.2. Without it the heuristic does not give the stated rate. Also, "log p ≍ log n
under (DIM)" does not follow from (DIM), which allows bounded p. The rate is √(log n / n) because of the log(p√n) in (16). See the
fix in 1.20.

**3.2 (pp. 2, 8, 9) How much the reported PIPs and evidence are covered.** The text says three times that their consistency holds "only on
designs without leakage" but never says which designs those are. Remark A.17 / §A.5 says: only the independent designs, and not AR,
the main design of the 10^6 plan. *Fix:* add on p. 2: "…only on designs without leakage, which among our designs means only the
independent ones (S1, IND)".

**3.3 (p. 13) What (FS_θ) asks, and whether it is reasonable.** (FS_θ) writes y^r = α1 + Xθ* + ε with X the *sample-standardised* design
and θ* deterministic. Under a random design, θ* = Dβ* depends on the sample standard deviations, so (FS_θ) and (GL) with fixed β* are
different models. Neither (b) nor (d) says how they relate, or whether one implies the other approximately (D → I under (GR) with
unit variances). The (d) part argues only about the size of the effects. *Fix:* one sentence on how (FS_θ) relates to (GL) + (FS_β),
and why Result 3 needs this form.

**3.4 (p. 5, p. 25) Example 2 against Result 3.** The example says "Result 3 proves this picture in general", but §8.2 item 2 says that the
leakage set Q for this example is not known. A single n = 100 example cannot instantiate asymptotic assumptions anyway. *Fix:* write
"Result 3 shows that, asymptotically and under Assumption 4, this is what happens in general", and either name a plausible Q
(for example {1, 3, 5, 6}) or say that the example only illustrates.

**3.5 (p. 20) Result 3, "by Result 1 nothing the run scores beats S0".** Result 1 assumes (GL), (SG) and (FS_β). Result 3 assumes (GR) and
(FS_θ) instead. A reader cannot tell whether Result 1 applies under Result 3's hypotheses. *Fix:* "by the analogue of Result 1 under
Result 3's assumptions (proved within Theorem 7)", or whatever is true.

**3.6 (pp. 12–13) Why the set size 5(A+1)(s0+1) log n.** (SG) and (EF_Σ) both constrain sets of this size, and Assumption 3 uses a window
q_n ∝ M log n. No entry says where the number comes from. *Fix:* one line: "the proof must control every model up to this size,
because the posterior puts negligible mass on larger models".

**3.7 (p. 15) The constants b, b_H and the constraint 15 b_H + b < ½.** They appear before part (a) with no explanation. *Fix:* one sentence
on the origin of the constraint (the 15 comes from the block size 16, but why the product?), or move it into the statement with a footnote.

**3.8 (p. 19) Result 2 in words: "for every large enough level M".** The assumption itself depends on M (the window q_n grows with M), so a
larger M asks more of the design. The words read as if M were free. *Fix:* "for every large enough level M for which Assumption 3 holds
with the window q_n of that M".

**3.9 (p. 6) Stage 1 threshold.** See 1.16. I could not tell what the exact-case threshold represents.

**3.10 (p. 20) Status box of Result 3.** "the two code-reading audits that its delivery route takes as hypotheses are independently
checked". Does Result 3 then have hypotheses beyond (C1)/(C2+)? The box reads as if it does. *Fix:* "Its link to the code rests on
two audits of the code, both independently checked; they add no assumption on the data."

**3.11 (p. 16) 5.5(c).** "Rules out … signals that vary with n". The conditions only bound the signals, so they may vary inside the bounds.
See also Possible errors.

---

## 4. Q1: one-line verdicts on the assumptions of Section 5

Each line says whether a statistician can tell what the entry asks, why it is needed and whether it is reasonable.

| Assumption | Verdict |
|---|---|
| (GL) Gaussian linear model | **Clear.** Asks, why and reasonableness all plain. |
| (DIM) p ≤ n^A | **Clear.** Minor: A ≈ 3.0 here vs "A ≥ 3.05" in §7.2. Table 4 "Used by 1–3" omits Result 6(b), which assumes p ≤ n^A. |
| (SP) fixed s0 | **Clear, and the best entry.** (d) gives a real reason (Result 6(a) makes s0 = O(√log n) nearly necessary). |
| (SG)/(GR) law of the rows | **Mostly clear.** (b) does not say why only sparse directions, or why that size (3.6). The (d) mixture example is unreadable as written (symbol clash, 1.9). |
| (FS_β)/(FS_θ) fixed signals | **(b) fails for (FS_θ).** It is a different data model on the sample-standardised scale, not just a signal bound (3.3, 1.18). Table 4 also contradicts "replaces (GL) and (SP) in Result 3" by listing (GL) and (SP) as used by Result 3. |
| (EF_Σ) eigenvalue floor | **Clear.** (b)–(d) are good, and the λ_min list is useful. (e) is unreadable (1.5). The set size is unexplained (3.6). |
| Assumption 3 (distribution setting) | **Clear in substance.** (b) is a good relaxation summary. Two problems: the label collision (1.2), and (b) does not say that the assumption tightens as M grows (3.8). |
| (V) visibility | **Mostly clear.** (a) and (c) are good. The second sentence of (b) gives a reason, not a meaning, and does not explain why "every U with \|U\| ≤ 15" rather than "its own block" (blocks are data-dependent; say so). (d)(ii) needs rewording (1.10), and riboflavin is undefined. |
| Assumption 4 (leakage set, local regressions) | **(b) fails; (d) partly fails.** (b) skips locality (ii) (1.3), misdescribes (c), and garbles the size condition (1.4). b, b_H and 15b_H + b < ½ are unexplained (3.7). (d) asserts that (b), (c) "follow from a floor and the locality of Σ_n" without defining locality, and its b < ½ reason is too terse (1.11). This is the entry the owner most needs to judge. |
| §5.5 floor/signal bounds (Result 4) | **Mostly clear; needs a name.** It is the only assumption without a tag (give it one, e.g. (CS)). (c) "signals that vary with n" is inaccurate (3.11). "Section 6 compares the two" should say §6.4. |
| Conventions (C1), (C2+), (C3) | **Clear in intent.** The admissible-n clause (1.14) and the lifted integer limits (1.13) need one plain sentence each. |

Entries whose (b) "In words" fails: **(FS_θ)** and **Assumption 4**; partly **(V)** (its (b) explains the motivation, not the meaning).
Entries whose (d) "Reasonable?" fails or is thin: **Assumption 4** (the locality claim is unexplained); **(FS_θ)** (argues only
the size of the effects, not the scale on which they are fixed); **(SG)** (the mixture example is unreadable).

---

## 5. Q2: one-line verdicts on Results 1–6

| Result | Words match formal? | "Why natural" convinces? | Unexplained in the statement |
|---|---|---|---|
| 1 (Thm 5) posterior concentration | Yes, but the words omit sub-Gaussian rows and p ≤ n^A. | **Partly.** The √(log p) step is missing (3.1), and "log p ≍ log n under (DIM)" is not implied. | The removed-column conventions crowd the statement (1.8). |
| 2 (Thm 6) distribution | Yes. The "Setting" paragraph is good. | **Yes.** | That the assumption depends on M (3.8). Why "at least two predictors" must remain. |
| 3 (Thm 7) reported model = truth | Yes, but the words omit Gaussian rows, fixed signals and the floor. The p. 2 summary ("for block and AR designs every run reports exactly the true model") drops "with probability tending to one" and "coefficients that do not cancel". | **Yes**, via Example 2. Weakened by "by Result 1" under different assumptions (3.5), and by Example 2's Q being unknown (3.4). | "Let Σ_n be positive definite" in addition to (EF_Σ): say why. The status box suggests extra hypotheses (3.10). |
| 4 (Thm 8) certified screening | Yes. Remark 9(i) is a model of how to say what is not claimed. | **Yes.** | The constant 200 in c_SB (fine to leave, but say it is from a union bound). The title (1.21). |
| 5 (Prop 10) evidence unbiased | Yes. | **Yes.** It is clear what is new (the frozen calibration). | Nothing in substance. The status box jargon ("line checks", "frozen-run identities", "code of record") should go or be glossed. |
| 6 (Thm 11) rate optimal | Yes for (a). For (b), the words say "two families of designs" and the statement defines them. Good. | **Mostly.** But "No fixed prior can put all its mass … faster than … n^{-1/2}" overclaims; it holds for *this* prior (g = n). | The scaling of the energy bound ‖θ*‖² ≤ nM_θ (θ* is on the unit-variance scale, so this allows coefficients of order √n; is that intended?). |

---

## 6. Internal jargon and ids in the main text

Excluded, as allowed: the code tags in §4.5, and §8 (status section). I list the status-box registry ids last, as borderline.

1. **HQ** (pp. 23, 25: §7.1, §7.2, §7.3, the §8.2 heading). Write "the project lead" or "open questions".
2. **Theory Department / Engineering / Writing Department / "on hold" / "mission" / "gated on the owner's word" / "now spread to
   February–March 2027" / "earlier campaign" / "theory-side hardening pass" / "Theory Department's queue" / "queued after the
   freeze"** (title, pp. 22–24). Project-management language. Keep one sentence of schedule at most.
3. **Study names: "the 2,400-fit study", "the 10^6 plan", "the strong-factor study", "a screening study", "the 1M runs"** (pp. 1, 10, 16,
   21). They are never described as studies (who ran them, where they are reported). One line each, or a citation to the companion report.
4. **Design labels S1–S6, IND, AR, BLK, FAC** (pp. 10–16, 20). They are defined on p. 10, but only in a dense paragraph (see 1.19). Use a table.
5. **"registry", "theory freeze", "rows", "status strings"** in Sections 1, 6 (Table 5) and §5–6 text (outside §8). See 2.3.
6. **Engineering terms in §4.5 outside the code tags: R′, I_max, m, "the binary's default", "run plan", "registered script", "scoring
   script as amended", "calibration floor", "stores", "counter-based"** (pp. 9–10).
7. **Theory-internal names: "missed-signal result/family", "list result", "worst-island bound", "list-mass premise", "raw-scale bridge",
   "global-overlap premise", "approximate-Gram condition", "aggregated leak term", "trap benchmark", "showcase fit"** (pp. 22–25).
8. **Status-box ids (borderline):** "registry row 1.2 / 2.1 / 3.1 / 3.5 / 3.7 / 1.3", "delivery route", "code-reading audits", "line
   checks", "frozen-run identities", "code of record", "recorded 11-17" (Table 5). The boxes are marked "removed for submission", but
   for the owner, "the version proved in the registry is a stronger form of this statement" (p. 20) raises a question the text does
   not answer.
9. `resource_limit` (p. 6) is a code status string. That is fine as code, but say "the run stops with a resource-limit status".

---

## 7. Cuts (≈ 5 pages, none needed for Q1/Q2)

1. **§4.5 and Table 3 (≈ 1.5 pp., pp. 8–10).** Replace them with three sentences: what the engine is, that no theorem covers it,
   and where its runs are reported. Move "The frozen configuration", "How it was checked" and Table 3 to an appendix or to the
   engineering report. The Table 2 row "parallel 10^6 engine" can stay.
2. **§7.4 "named open problems" and "Possible strengthenings" (≈ 0.8 p., p. 24) → Appendix E.** They are written in theory-internal
   names (§6 item 7) and none is used by Results 1–6. Also shorten §7.1–7.3 to about 4 lines each (what it would show; status), dropping
   "What exists", "The rule for claims" and the Lean level list (≈ 0.8 p.).
3. **§8.1 Table 6 and §8.2 items 3, 4, 7, 8, 9 (≈ 1 p., pp. 25–26) → Appendix E.** These are registry housekeeping and engineering
   confirmations. Keep §8.1's first paragraph (one line: "no result was retracted or narrowed since the freeze"), "What did not
   change", and §8.2 items 1, 2, 5, 6.
4. **Part (e), "vs Song and Liang", in §5 (≈ 1 p.).** Table 4 already gives each verdict. Cut each (e) to one sentence and move the
   page-by-page argument ((SG)(e), (EF_Σ)(e), (DIM)(e), 3(e), 4(e)) to an appendix. This also removes the hardest sentence in the
   document (1.5).
5. **Engineering detail in §4.2 (≈ 0.5 p., pp. 6–7).** Table 2 says no theorem depends on the Stage 1 thresholds (N0^c, |Ω| ≤ …), the
   clustering rule, the calibration internals (ESS 0.90, tiers, fallback) or the move mix. Keep one sentence each and point to
   Appendix C / A.6. Also merge the three format descriptions (§1 items 3–4, the §5 intro, the §6 intro) into one (≈ 0.2 p.).

---

## Possible errors (not checked)

1. **p. 23, §7.2:** "A ≥ 3.05 here". log(10^7)/log(200) = 3.042, so the bound should be A ≥ 3.04. The text is also inconsistent with p. 12 ("A ≈ 3.0").
2. **p. 11, Table 4, "Used by":** (GL) and (SP) are listed as used by Result 3, but (FS_θ) "replaces (GL) and (SP) in Result 3" (p. 13), and
   Theorem 7 and Table 5 do not list them. (DIM) "1–3" omits Result 6(b), which assumes p ≤ n^A. (SP) may also be used by 6(b) ("s0 fixed").
3. **p. 18, Result 1 heuristic:** as written it gives (s0+1)/(2√n), with no √(log p) (see 3.1). "log p ≍ log n under (DIM)" fails for bounded p,
   which (DIM) allows.
4. **p. 22, Result 6 "Why it is natural":** "No fixed prior can put all its mass on one model faster than … n^{-1/2}". A g-prior with larger
   g has a smaller Occam factor, so the claim seems true only for this prior.
5. **p. 16, §5.5(c):** "Rules out … signals that vary with n". The stated bounds allow θ* to vary with n inside [θ̲, ·] and the ℓ1 bound.
6. **p. 22, Theorem 11(b):** the energy bound ‖θ*‖² ≤ nM_θ on unit-variance-scale coefficients looks like a scaling slip (compare ‖μ‖² ≤ nM_μ).
7. **p. 15 vs p. 36:** "finitely many local correlation patterns" (main text) vs "countably many" (Remark A.20).
8. **p. 28, Remark A.2:** cites "Remark 11(b)"; presumably Theorem 11(b).
9. **p. 5:** the leakage-set cross-reference "Section 6.3" should be §5.4. Appendix B (p. 37) also puts Q, L(Q), H_l in §6.3.
10. **p. 16, Assumption 4(c), "In words":** "Within Q, the regression of a predictor on the others" does not match the statement, where l ranges
    over all of [p] and T over L(Q).
