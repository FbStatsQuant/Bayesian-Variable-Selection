#!/usr/bin/env python3
# NA_DROP v1.5 (HQ ruling, option C, on Sol-6 b″-1): the delivery conclusion keeps "on output" for the method with the list fields;
# the allocation card's claim is withdrawn (its inventory stays as a note, "not a claim"); b″-2, b″-3, b″-4 as wording.
# Whitespace-flexible; every Old must match exactly once (or the stated count).
import re
D='Theory_work/Wave3/PRE_LEAN_PASS/Sol5/NA_DROP_v15/ticket/Theory_work/Wave3/W3-D5P/'
def sub(f,old,new,count=1):
    s=open(D+f,encoding='utf-8').read()
    pat=re.escape(old).replace(r'\ ',r'\s+').replace(r'\n',r'\s+')
    m=list(re.finditer(pat,s)); assert len(m)==count,(f,old[:70],len(m))
    for x in reversed(m): s=s[:x.start()]+new+s[x.end():]
    open(D+f,'w',encoding='utf-8').write(s)
L='lemmas/L3_listR.md'
T61='allocation/delivery of the list fields is not claimed for the tagged method beyond output runs'
# ---- STATEMENT.md
sub('STATEMENT.md','# W3-D5P — STATEMENT v1.4 (locked v1.0 + changelog rows v1.1–v1.4)','# W3-D5P — STATEMENT v1.5 (locked v1.0 + changelog rows v1.1–v1.5)')
sub('STATEMENT.md','under the delivery premises, unconditionally |','under the delivery premises, on output runs of the method with the list fields ('+T61+') |')
old_iii=open(D+'STATEMENT.md',encoding='utf-8').read().split('\n')[124:128]
assert old_iii[0].startswith('(iii) *With delivery.*') and old_iii[3].rstrip().endswith('O_P(r_n).'),old_iii
new_iii=['(iii) *With delivery.* Assume in addition the delivery premises (D). Then every admissible run of the pinned core returns output (DLV-0). For the method with the list fields the conclusions are claimed on output runs only (𝒪 := {the run returns output}) [T6-1]:',
'    for every seed, N_e, R′ and calibration outcome, P(𝒪 ∩ B₄) → 0, and P(𝒪 ∩ (B₁(t) ∪ B₂(t) ∪ B₃(t))) → 0 for every t ∈ (0, ½);',
'    if moreover p ≥ 2 for all large n, then for every t_n as in (ii), P(𝒪 ∩ (B₁(t_n) ∪ B₂(t_n) ∪ B₃(t_n))) → 0, i.e. the two PIP errors and the evidence error are O_P(r_n) on output.',
'    '+T61.capitalize()+'; the form without "on output" is not asserted for it.']
Ls=open(D+'STATEMENT.md',encoding='utf-8').read().split('\n'); Ls[124:128]=new_iii; open(D+'STATEMENT.md','w',encoding='utf-8').write('\n'.join(Ls))
sub('STATEMENT.md','| v1.4 | none in a claim: proof only','| v1.4 | **Withdrawn in v1.5** (HQ ruling (C); see the v1.5 row). none in a claim: proof only')
row15='| v1.5 | (C3)(iii) and the registry conclusion: the delivery conclusion "without \'on output\'" is kept only on output runs for the method with the list fields (T6-1, HQ ruling, option (C), on Sol-6 b″-1): '+T61+'; L3 (0.5) (b″-2 causal-order sentence; b″-3 field equality limited to the fields used), (0.6) (the allocation card\'s claim withdrawn; its inventory a note, not a claim), Step 3 and the remarks; ERRATA E1; CARD, REPORT status quotes (b″-4); depends_on of LIST-R back to the v1.1 list | **WEAKER** ((iii) no longer asserts that every admissible run of the tagged method returns output; clause (o), the qualifier removals on output runs and (C3)(i)–(ii) unchanged; no new premise) | NA-b″1 to NA-b″4 | `Sol6/CODEX_gpt-6.2-sol.md` (R5 FAIL on 906961f6, superseded by the (C) scoping, which HQ ruled) | review of v1.5 pending |'
S=open(D+'STATEMENT.md',encoding='utf-8').read().split('\n')
i=[k for k,l in enumerate(S) if l.startswith('| v1.4 |')]; assert len(i)==1
S.insert(i[0]+1,row15); open(D+'STATEMENT.md','w',encoding='utf-8').write('\n'.join(S))
# ---- L3
sub(L,'(0.4) (D) ⇒ every admissible run returns output for every valid non-degenerate input (DLV-0,','(0.4) (D) ⇒ every admissible run of the pinned core returns output for every valid non-degenerate input (DLV-0,')
sub(L,'RM2R `STATEMENT.md:138-143`, last sentence).','RM2R `STATEMENT.md:138-143`, last sentence). DLV-0 is a statement about the pinned core; it is not transferred to the method with the list fields (0.5)–(0.6).')
sub(L,"so every guard decision of the tagged fit is that of the pinned fit [R2-E-2], while the work and storage of the new computation are bounded in (0.6) — on every input and every\nrealisation of the run's uniforms the post-commit fit and the pinned fit execute the same computation up to the new\nfields,",
 "so the new computation, which comes after the last guard consultation, cannot affect any guard decision: for matching guard inputs every guard decision of the tagged fit is that of the pinned fit [R2-E-2] (measured elapsed time and operation durations are not fixed by the input and the uniforms, so no decision-by-decision comparison of separate executions is claimed) — on every input and every\nrealisation of the run's uniforms the post-commit fit and the pinned fit execute the same computation (not the same measured times) up to the new\nfields,")
sub(L,"raise no error other than a failed allocation, which (0.6) excludes under (D). Hence, under (D) read for the method with the list fields, the post-commit fit returns whenever the pinned fit returns; without (D) the two can differ only through an allocation inside the helper. In both cases 𝒪 on returning runs, `status`, `hpm`, `top_store`,\n`fit$exact` (with its store) and every other existing field are those of core 4676af6. So L2, RM0-plus (b⁺) and DLV-0\napply to the method with the list fields, and the new fields are SPEC's functions of the pinned outputs.",
 "raise no error other than a failed allocation, which is not excluded here: "+T61+" [T6-1, HQ ruling, option (C)], see (0.6). Hence on a post-commit run that returns output, 𝒪, `status`, `hpm`, `top_store`,\n`fit$exact` (with its store) and the other existing fields the proof uses are those of core 4676af6 (on the exact branch `finish(fit)` is a lazy argument of `v3_exact_list_last` (`v3_fit.R:131`), forced at `v3_run.R:277` after `v3_list_fields`, so `peak_memory_kb` and `timings$total`, which `finish` samples, are measured after the helper; the proof does not use them, and the conformance citation `reviews/IMPL_LIST_codeprint.md:42` is read for the fields and state the proof uses). So L2 and RM0-plus (b⁺) apply to the method with the list fields on output runs; DLV-0 is not transferred (0.4); and the new fields are SPEC's functions of the pinned outputs.")
L3t=open(D+L,encoding='utf-8').read().split('\n')
a=[k for k,l in enumerate(L3t) if l.startswith('(0.6) *Work and storage of the list fields*')]; assert len(a)==1
b=[k for k,l in enumerate(L3t) if l.startswith('The reader assumptions (A1)–(A6) of Theorem 6')]; assert len(b)==1
new06=['(0.6) *Allocation and delivery of the list fields: not claimed beyond output runs* [b′-1, T6-1; HQ ruling, option (C), on Sol-6 b″-1]. '+T61.capitalize()+'. A note, **not a claim**: after the last guard the helper (`v3_run.R:245-269`; on the exact branch also `v3_exact_list_last`, `:274-279`) allocates a lookup of length max(orig) ≤ p_raw, m ≤ 40p + 1 duplicate-check key strings (K original indices of at most D ≤ 10 decimal digits each), and numeric vectors of length m and p; `PRE_LEAN_PASS/Sol5/FABLE_ALLOC_CARD.md` counts the live bytes and operations of these objects, but it does not bound the creation and interning of the key strings by `paste`, the live words of R\'s global string cache, or the operation cost of producing and hashing the decimal strings under IDEAL-W⁺ (Sol-6 b″-1). Therefore no bound against the brackets of C-DLV Lemma R, no constants C_W + 1, C_M + 8, and no extension of Lemma R, Corollary R or (D) to the method with the list fields is asserted; the allocation card\'s claim is withdrawn.']
L3t[a[0]:b[0]]=new06; open(D+L,'w',encoding='utf-8').write('\n'.join(L3t))
sub(L,"Under (D), read for the method with the list fields ((0.6); its envelopes dominate the pinned core's, so (0.4) applies), by (0.4), (0.5) and (0.6), P(𝒪ᶜ) = 0 for every admissible run of the method with the list fields. Hence for any event B of the run, P(B) ≤ P(𝒪 ∩ B) + P(𝒪ᶜ) =\nP(𝒪 ∩ B), and Step 2 gives P(B₄) → 0 and P(B₁(t) ∪ B₂(t) ∪ B₃(t)) → 0 for every t ∈ (0, ½), and, when p ≥ 2 for all\nlarge n, P(B₁(t_n) ∪ B₂(t_n) ∪ B₃(t_n)) ≤ P(𝓜_nᶜ) + P(𝒦_nᶜ) + P(ε_n > t_n) → 0 for every deterministic t_n ∈ (0, ½) with\nt_n/r_n → ∞.",
 "(D) gives P(𝒪ᶜ) = 0 for the pinned core (0.4); for the method with the list fields no such statement is made ((0.5)–(0.6), T6-1), so (iii) is Step 2 on output runs. For every seed, N_e, R′ and calibration outcome, Step 2 gives P(𝒪 ∩ B₄) → 0 and P(𝒪 ∩ (B₁(t) ∪ B₂(t) ∪ B₃(t))) → 0 for every t ∈ (0, ½), and, when p ≥ 2 for all\nlarge n, P(𝒪 ∩ (B₁(t_n) ∪ B₂(t_n) ∪ B₃(t_n))) ≤ P(𝓜_nᶜ) + P(𝒦_nᶜ) + P(ε_n > t_n) → 0 for every deterministic t_n ∈ (0, ½) with\nt_n/r_n → ∞.")
sub(L,"X_n := 0 on 𝒪ᶜ, a null event under (D)) [NA-C8], so that {X_n > t} ⊆ B₁(t) ∪ B₂(t) ∪ B₃(t).","X_n := 0 on 𝒪ᶜ) [NA-C8], so that {X_n > t} ⊆ 𝒪 ∩ (B₁(t) ∪ B₂(t) ∪ B₃(t)).")
sub(L,"contradicting P(B₁(t_n) ∪ B₂(t_n) ∪ B₃(t_n)) → 0. Hence each error is O_P(r_n). ∎(iii)","contradicting P(𝒪 ∩ (B₁(t_n) ∪ B₂(t_n) ∪ B₃(t_n))) → 0. Hence each error is O_P(r_n) on output. ∎(iii)")
sub(L,'to carry L2, RM0-plus and DLV-0 from the pinned core to the method with\n  the list fields ("changes no other field and no other state");','to carry L2 and RM0-plus from the pinned core to the method with\n  the list fields on output runs ("changes no other field and no other state"; DLV-0 is not transferred, T6-1);')
# ---- ERRATA
E=open(D+'ERRATA.md',encoding='utf-8').read().split('\n')
r=[k for k,l in enumerate(E) if l.startswith('| E1 |')]; assert len(r)==1
cells=E[r[0]].split(' | ')
# the proposed-fix cell is the last one; it is delimited by the first "|" occurrences outside \|; locate by the opening quote
j=E[r[0]].index('| "so every guard decision')
newcell='| "so every guard decision of the tagged fit is that of the pinned fit [applied in L3 (0.5)], and '+T61+' [T6-1; HQ ruling, option (C), on Sol-6 b″-1], see L3 (0.6). The earlier wordings are withdrawn: \'dominated by the store already held\'; the allocation card\'s bound of the helper by T_W and T_B against the brackets of C-DLV Lemma R, and \'Lemma R and Corollary R hold for the method with the list fields\'. The card\'s inventory (`PRE_LEAN_PASS/Sol5/FABLE_ALLOC_CARD.md`) may stay as a note, marked \'not a claim\': it does not bound the creation and interning of the `paste` key strings or the global string cache (Sol-6 b″-1). On the exact branch the last guard decision is the preflight (`v3_fit.R:115-117`) and `:121` creates the list." |'
E[r[0]]=E[r[0]][:j]+newcell; open(D+'ERRATA.md','w',encoding='utf-8').write('\n'.join(E))
# ---- REPORT
sub('REPORT.md','changelog v1.1–v1.4','changelog v1.1–v1.5')
sub('REPORT.md','Sol-5 (b) points b-1 to b-4 applied in v1.3 (review of v1.3 pending)','Sol-5 (b) points b-1 to b-4 applied in v1.3 (Sol-5b R3 8.7 FAIL: b-1 to b-4 FIXED, b′-1 open; the v1.4 allocation proof was not accepted, Sol-6 R5 8.4 FAIL, b″-1); v1.5 scopes the delivery conclusion to output runs (HQ ruling, option C; review of v1.5 pending)',count=2)
sub('REPORT.md','; under (D) without "on output" [R1-sol-1, R1-sol-3, R1-opus-2]','; under (D), on output runs only: '+T61+' [T6-1]')
sub('REPORT.md',' ; C-DLV:L1-R@proof:brackets,R.4 ; C-DLV:Cor-R@stmt','')
# ---- CARD / READER_DELTA
sub('CARD.md','on output; without "on output" under the delivery conventions (S4).','on output; '+T61+' [T6-1].')
sub('CARD.md','Sol-5 (b) R1 FAIL, points b-1 to b-4 applied in v1.3; review of v1.3 pending)','Sol-5 (b) R1 FAIL, points b-1 to b-4 applied in v1.3; Sol-5b R3 8.7 FAIL, b-1 to b-4 fixed, b′-1 open; v1.4 not accepted, Sol-6 R5 8.4 FAIL; v1.5 scopes the delivery conclusion to output runs, HQ ruling option C, review pending; this is separate from IMPL-LIST, discharged at the tag)')
sub('READER_DELTA.md','on output, and without "on output"\n> under the delivery conventions (S4).','on output; '+T61+'.')
print('v1.5 applied')
