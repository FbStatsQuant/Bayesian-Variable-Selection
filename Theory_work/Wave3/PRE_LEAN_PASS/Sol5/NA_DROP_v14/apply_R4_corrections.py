#!/usr/bin/env python3
# Applies Opus R4 findings F-1, C-1, S-1, S-2 (x2), C-2, S-3, C-4 (x2) exactly as the seat worded them (HQ rule: wording/qualifier findings applied as written).
# NOT applied (optional or for the manager): C-3, E-1, S-4. Whitespace-flexible; each Old must match exactly once.
import re
D='Theory_work/Wave3/PRE_LEAN_PASS/Sol5/NA_DROP_v14/ticket/Theory_work/Wave3/W3-D5P/'
def sub(f,old,new):
    s=open(D+f,encoding='utf-8').read()
    pat=re.escape(old).replace(r'\ ',r'\s+'); m=list(re.finditer(pat,s)); assert len(m)==1,(f,old[:60],len(m))
    open(D+f,'w',encoding='utf-8').write(s[:m[0].start()]+new+s[m[0].end():])
L='lemmas/L3_listR.md'
sub('ERRATA.md','; optionally: on the exact branch the last guard decision is the preflight (`v3_fit.R:115-117`) and `:121-122` creates the list','')  # F-1
sub(L,'runs the pinned code on the same state,','runs the pinned code on the same state (on the exact branch `finish(fit)` is a lazy argument of `v3_exact_list_last`, forced at `v3_run.R:277`, so `finish` runs after `v3_list_fields`; it consults no guard and allocates O(1) words, and the bounds below do not depend on this order),')  # C-1
sub('STATEMENT.md','they fall under the existing IDEAL-W⁺ premise; no new premise.','they are counted as R-level objects in the manner of Lemma R (`L1_resources.md:95-96`), and their bytes, like those of R\'s global string cache that the m keys enter, fall under MACH\'s peak bytes ≤ β·(words held) + β₀; no new premise.')  # S-1
sub(L,'constants C_W + 1, C_M + 8,','constants C_W + 1, C_M + 8 (Lemma R\'s bounds are W̄ = C_W·𝔅_W and M̄ = 2C_M·𝔅_M, `L1_resources.md:73, 78`, so M̄ + 16·𝔅_M = 2(C_M + 8)·𝔅_M),')  # S-2.1
sub(L,'the right sides are terms of the brackets','the right sides are sums of terms of the brackets (the first with factor 16)')  # S-2.2
sub(L,'holds with the same polynomial allocation formulas.','holds with the same polynomial allocation formulas. The same two additive terms carry over to the re-derivation of these envelopes for the shipped code (`W3-RM2-R/STATEMENT.md:76-79`), whose word bound M_G ≥ M̄ is only increased by T_M.')  # C-2
sub(L,'Under (D), by (0.4) and (0.5), P(𝒪ᶜ) = 0','Under (D), read for the method with the list fields ((0.6); its envelopes dominate the pinned core\'s, so (0.4) applies), by (0.4), (0.5) and (0.6), P(𝒪ᶜ) = 0')  # S-3
sub(L,'and max(orig) ≤ p_raw (`v3_fit.R:118`)','and max(orig) ≤ p_raw (`orig` = `pre$kept` = `which(!constant)` over the p_raw columns, `v3_preprocess.R:112`; `v3_fit.R:118`)')  # C-4.1
sub(L,'(`v3_run.R:245-269`)','(`v3_run.R:245-269`; on the exact branch also the constant-size wrapper `v3_exact_list_last`, `:274-279`, inside the constant 40000)')  # C-4.2
print('R4 corrections applied')
