#!/usr/bin/env python3
# Opus R6 findings C-1, C-2, S-1, S-2, S-3, S-4 (two), E-1, E-2 applied exactly as the seat worded them (HQ rule). Not applied: F (note), E-1 of the earlier R4 (n/a).
import re
D='Theory_work/Wave3/PRE_LEAN_PASS/Sol5/NA_DROP_v15/ticket/Theory_work/Wave3/W3-D5P/'
def sub(f,old,new):
    s=open(D+f,encoding='utf-8').read()
    pat=re.escape(old).replace(r'\ ',r'\s+').replace(r'\n',r'\s+')
    m=list(re.finditer(pat,s)); assert len(m)==1,(f,old[:70],len(m))
    open(D+f,'w',encoding='utf-8').write(s[:m[0].start()]+new+s[m[0].end():])
L='lemmas/L3_listR.md'
sub(L,"— on every input and every\nrealisation of the run's uniforms the post-commit fit and the pinned fit execute the same computation (not the same measured times) up to the new\nfields,","— on every input, every\nrealisation of the run's uniforms and matching guard inputs, the post-commit fit and the pinned fit execute the same computation up to the new\nfields (the measured times themselves are not claimed equal),")
sub('ERRATA.md','"so every guard decision of the tagged fit is that of the pinned fit [applied in L3 (0.5)], and','"so the new computation, which comes after the last guard consultation, cannot affect any guard decision; for matching guard inputs every guard decision of the tagged fit is that of the pinned fit [applied in L3 (0.5)], and')
sub('REPORT.md','rate: O_P(sqrt(log n / n)) for the two PIP errors and |log_Z_list - log Z| (p >= 2)','rate: O_P(sqrt(log n / n)) on output runs (each error set to 0 off the output event) for the two PIP errors and |log_Z_list - log Z| (p >= 2)')
sub('STATEMENT.md','i.e. the two PIP errors and the evidence error are O_P(r_n) on output.','i.e. the two PIP errors and the evidence error, each set to 0 off 𝒪, are O_P(r_n) ("on output"; no statement conditional on 𝒪).')
sub(L,"so `peak_memory_kb` and `timings$total`, which `finish` samples, are measured after the helper; the proof does not use them, and the conformance citation `reviews/IMPL_LIST_codeprint.md:42` is read for the fields and state the proof uses)","so `peak_memory_kb`, `timings$total` and `runtime_guard$elapsed_seconds` (`v3_fit.R:80-82`; `cpp/v3_core.cpp:787`), which `finish` samples, are measured after the helper; the proof does not use them, and the conformance citation `reviews/IMPL_LIST_codeprint.md:42` (\"fields added after `finish()`\", `v3_fit.R:131`: textual order; in evaluation order `finish` runs after `v3_list_fields` on the exact branch) is read only for the fields and state the proof uses)")
sub('STATEMENT.md','under the delivery premises, on output runs of the method with the list fields (allocation/delivery of the list fields is not claimed for the tagged method beyond output runs)','with the delivery premises, the method with the list fields gains nothing beyond output runs (allocation/delivery of the list fields is not claimed for the tagged method beyond output runs)')
sub('REPORT.md','; under (D), on output runs only: allocation/delivery','; under (D) as without it, these conclusions are on output runs only for the method with the list fields: allocation/delivery')
sub('STATEMENT.md','the delivery conclusion "without \'on output\'" is kept only on output runs for the method with the list fields','the delivery conclusion is scoped to output runs for the method with the list fields (the form without \'on output\' is withdrawn)')
sub(L,'(K original indices of at most D ≤ 10 decimal digits each)','(each of at most K original indices of at most D ≤ 10 decimal digits)')
print('R6 corrections applied')
