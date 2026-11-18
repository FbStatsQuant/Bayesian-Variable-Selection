#!/usr/bin/env python3
# NOT RUN until HQ's GO. Builds Sol5/NA_DROP_v14/ticket from the NA_DROP v1.3 ticket and applies the Fable allocation card's texts
# (FABLE_ALLOC_CARD.md section 6) exactly: R-a, R-b, R-c in lemmas/L3_listR.md; the E1 cell of ERRATA.md (added to the ticket: 6 files);
# the two new depends_on entries of W3-D5P:LIST-R in REPORT.md; a changelog row v1.4 in STATEMENT.md. Whitespace-flexible matching; every Old string must match once.
import re,shutil,os
P='Theory_work/Wave3/PRE_LEAN_PASS/'
SRC=P+'Sol5/NA_DROP/ticket/Theory_work/Wave3/W3-D5P/'
DST=P+'Sol5/NA_DROP_v14/ticket/Theory_work/Wave3/W3-D5P/'
shutil.rmtree(P+'Sol5/NA_DROP_v14/ticket',ignore_errors=True); shutil.copytree(P+'Sol5/NA_DROP/ticket',P+'Sol5/NA_DROP_v14/ticket')
shutil.copy('Theory_work/Wave3/W3-D5P/ERRATA.md',DST+'ERRATA.md')
def rd(p): return open(DST+p,encoding='utf-8').read()
def wr(p,s): open(DST+p,'w',encoding='utf-8').write(s)
def flexsub(s,old,new):
    pat=re.escape(old).replace(r'\ ',r'\s+'); m=list(re.finditer(pat,s)); assert len(m)==1,(old[:70],len(m)); return s[:m[0].start()]+new+s[m[0].end():]
L=rd('lemmas/L3_listR.md')
L=flexsub(L,"after which `finish` (`v3_fit.R:79-87`) does not branch on the clock, so DLV-0's guard and MACH accounting are unaffected [R2-E-2] —","after which `finish` (`v3_fit.R:79-87`) does not branch on the clock, so every guard decision of the tagged fit is that of the pinned fit [R2-E-2], while the work and storage of the new computation are bounded in (0.6) —")
L=flexsub(L,"the remaining operations (`vapply` of `paste`, `exp`, `log`, indexing within 1..m) raise no error. Hence the post-commit fit returns if and only if the pinned fit returns, and 𝒪, `status`, `hpm`, `top_store`,","the remaining operations (`vapply` of `paste`, `exp`, `log`, indexing within 1..m) raise no error other than a failed allocation, which (0.6) excludes under (D). Hence, under (D) read for the method with the list fields, the post-commit fit returns whenever the pinned fit returns; without (D) the two can differ only through an allocation inside the helper. In both cases 𝒪 on returning runs, `status`, `hpm`, `top_store`,")
par=open(P+'Sol5/NA_DROP_v14/R-c_paragraph_0.6.txt',encoding='utf-8').read().strip()
# insert (0.6) directly after the (0.5) paragraph: before the next paragraph that follows "apply to the method with the list fields."
anchor="So L2, RM0-plus (b⁺) and DLV-0\napply to the method with the list fields"
m=re.search(r"apply to the method with the list fields[^\n]*\n",L); assert m,'anchor for (0.6) not found'
L=L[:m.end()]+par+"\n"+L[m.end():]
wr('lemmas/L3_listR.md',L)
E=rd('ERRATA.md')
e_old="so every guard decision is that of the pinned fit, and the added O(\\|𝒯\\|K) operations and O(\\|𝒯\\| + p) words, dominated by the store already held, are absorbed by the polynomial envelopes of (D)"
e_new=open(P+'Sol5/NA_DROP_v14/E1_new_cell.txt',encoding='utf-8').read().strip()
E=flexsub(E,e_old,e_new); wr('ERRATA.md',E)
R=rd('REPORT.md')
R=flexsub(R,"W3-D5P:LIST-K@stmt ; W3-D5P:LIST-CODE@stmt ; W3-RM2-R:RM2-R-plus@stmt ; W3-RM2-R:RM0-plus@stmt ; W3-RM2-R:DLV-0@stmt ; W2-APP:POST@stmt","W3-D5P:LIST-K@stmt ; W3-D5P:LIST-CODE@stmt ; W3-RM2-R:RM2-R-plus@stmt ; W3-RM2-R:RM0-plus@stmt ; W3-RM2-R:DLV-0@stmt ; W2-APP:POST@stmt ; C-DLV:L1-R@proof:brackets,R.4 ; C-DLV:Cor-R@stmt")
wr('REPORT.md',R)
S=rd('STATEMENT.md')
S=flexsub(S,"# W3-D5P — STATEMENT v1.3 (locked v1.0 + changelog rows v1.1–v1.3)","# W3-D5P — STATEMENT v1.4 (locked v1.0 + changelog rows v1.1–v1.4)")
i=S.index("| v1.3 |"); j=S.index("\n",i)
row="\n| v1.4 | none in a claim: proof only (Sol-5b b′-1 = T6-1, Fable allocation card): L3 (0.5) \"unaffected\" and \"returns iff\" sentences replaced; new (0.6) bounds the work and storage of the list helper (T_B, T_W against the brackets of C-DLV Lemma R), scoped to (D); ERRATA E1's assertion replaced by the proof; depends_on of LIST-R gains C-DLV:L1-R and C-DLV:Cor-R | EQUAL (proof completion; no statement changes; \"the tagged fit returns whenever the core fit does\" withdrawn for allocations that do not satisfy (D)) | NA-b1' (Sol-5b b′-1) | `Sol5/FABLE_ALLOC_CARD.md` | review of v1.4 pending |"
S=S[:j]+row+S[j:]
wr('STATEMENT.md',S)
print('applied')
