# STYLE_A5_R1: advisor note on the restructure under the assumption rule (2026-11-17)

Read: the changed parts of §1, §4, §5, §6 and the two supplement remarks, against `ASSUMPTION_COMPLIANCE.md` and
`PRECEDENTS_2026-11-17.md`. The log is clean, both summary tables are in place, and no old result number is left.

## (a) Do the decisions read as intended?
1. **Result 3:** the fixed wordings are there. Two leftovers break "no unqualified AR": "for AR designs" (§5.3.3,
   visibility) and "block, banded and AR structures" (§5.3.3, floor and local regressions).
2. **Result 4:** heading, weaker conclusion, the flag, "no run is claimed to certify" and the miss counts are all
   there. It is not called the result for strong-factor data. Its headline sentence is overstated in four places (b1).
3. **Result 5 and the row 3.6 remark:** as decided.
4. **The list guarantee (Remark A.9):** as decided; "nothing in this paper proves it" is the right sentence.
5. **The omitted-variables example** is labelled; **both disclosures** are present (§3.7 and the row-law line).
6. **Precedents lines** are present for six assumptions and §5.3.4. Four keep only the favourable half (b3).

## (b) Over- and under-statement (flags, not fixed)
1. **Result 4 as a conditional guarantee.** The theorem bounds an intersection: the probability that a run certifies
   a small model *and* that model misses a true predictor tends to zero. Four places say something stronger:
   - §1 item 4 and Table 2: "a certified … model misses no true predictor, with probability tending to one";
   - the abstract: "a certified small reported model misses no true predictor";
   - §6: "concludes only that no true predictor is missed";
   - Result 4, In words, second sentence: "a certified small model misses no true predictor".
   Remark 13(i) says the theorem is "not a guarantee conditional on certification". One wording for all: "a run
   rarely certifies a small model that misses a true predictor".
2. **"Why it matters" of Result 4, "so it covers designs where those conditions fail".** Next to its own numerics (61
   of 122 certified models missed a true predictor at $n=50$; the size budget needs $n\gtrsim1{,}450$) this edges
   toward what HQ ruled out. Suggest "it applies where those conditions fail, when its own conditions hold".
3. **Precedent comparisons that drop the unfavourable half of the source:**
   - *Signal, lower bound:* keeps "when $p\ge n^a$ our order is the same"; drops "when $\log p=o(\log n)$ ours is the
     larger requirement".
   - *Eigenvalue floor:* keeps the fixed-design match; drops that the random-design floor is asked on larger,
     $O(\log n)$ sets.
   - *Near-exact collinearity:* drops "Narisetty and He's floor may be lower than ours when $p$ is large". And "ours
     excludes exact duplicates" reads as an advantage; in the source it means ours asks more there.
   - *Certified screening:* "As for the eigenvalue floor … above", but its sets have $k_n+s_0$ predictors, which can
     be far larger than a multiple of the sparsity.
4. **The rule paragraph, "Every assumption of a result in the main text is of one of three kinds".** The compliance
   audit puts visibility and the leakage set in none of them; HQ's answer was to narrow Result 3. The text never
   says so, and §5.3.3 has no Precedents line. One sentence is missing: the two conditions of Result 3 have no
   precedent and are argued only for block and moderate AR correlation, which is why Result 3 is stated for those.
5. **§1 item 3, "they fail for pervasive common factors with effects of mixed signs".** That is the visibility
   failure. The leakage set fails for every pervasive factor with $p\gg\sqrt n$, whatever the signs (§5.4 has it
   right).
6. **Gaussian rows, Precedents line.** By the audit, only Bayesian selection papers count as class 1. The line opens
   with three Lasso papers and gives Song and Liang's worked case last, as "also". Put the qualifying evidence
   first. The source also says the Raskutti–Wainwright–Yu inequality carries no covariance condition of its own.
7. **"Moderate AR" is never defined** (13 uses). Say once what it covers: AR(1) correlation 0.5 and 0.6 in our designs.
8. **Smaller:**
   - "riboflavin-like data" (§1, §5.4) is unexplained at first use;
   - "which only independent predictors satisfy" (Result 5's closing line, the row 3.6 "why") should be "which, of our
     designs, only the independent ones satisfy";
   - "it needs no leakage at all" (row 3.6 "why") still reads as "does not need leakage".

## (c) Flow and duplication after the renumbering
1. **Table 3 has no rows for Result 4**, a main-text result, but keeps a group for a supplement remark. §5.3.4 also
   has no "Our designs" line, though the rule paragraph announces one for §5.3.3–5.3.5. Result 4 is a fixed-design
   theorem; say whether our designs meet its floor.
2. **"The theorem for block and moderate AR correlation"** appears four times inside Result 3 alone (heading, In
   words, Remark 11(ii), Scope) and again in §1, Table 2, §5.4 and §6. Keep the heading, the Scope line and §5.4.
3. **"Needs neither condition"** appears in the heading, In words, the "why", §5.3.4, §5.4 and §6.
4. **§6 has grown back into a scope summary:** it restates Result 3's and Result 4's reach and the two supplement
   remarks. In the last round it pointed to §5.4 in one sentence.
5. **Result order** is now 1–6 in sequence, which reads better than before; Result 6 (the rate of Result 1) comes last.
   If it stays there, its first sentence should say that it is about Result 1.

## (d) Trims at the 25-page limit (about 0.7 page)
1. **§6:** back to one pointer for the design scope (5 lines).
2. **Result 3:** drop the first sentence of "In words" and Remark 11(ii) (3 lines).
3. **Result 4:** the second sentence of "In words" and the "why" say the same thing; keep one (2 lines). Remark 13(ii)
   on the second form can go to the supplement (2 lines).
4. **§5.3.3:** the "Evidence" lines still restate (V) and the leakage-set definition, which §4.4 gives (6 lines).
5. **§5.3.5** judges an assumption of a supplement remark: move it to the supplement with that remark (about 10
   lines), and drop its group from Table 3.
6. **§5.4:** its last sentence repeats Result 5's closing paragraph (2 lines).
