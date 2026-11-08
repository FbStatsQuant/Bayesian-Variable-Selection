from pathlib import Path
import sys, runpy, contextlib
root=Path.cwd()
num=root/'Theory_work/Wave1/W1-N3/numerics'
scratch=root/'Theory_work/Wave1/W1-N3/reviews/R07_scratch_sol'
sys.path.insert(0,str(num))
import n3lib
n3lib.HARNESS=str(scratch/'sm_harness.exe')
for script,args in [('check_union_order.py',[]),('fp_example.py',[]),('cex_default_cap.py',[]),('cex_family.py',[]),('lemma_probes.py',[]),('eng10_n2.py',[]),('run_checks.py',['20261108']),('run_checks.py',['7'])]:
    sys.argv=[str(num/script)]+args
    output=scratch/(script.removesuffix('.py')+('_'+args[0] if args else '')+'.txt')
    with output.open('w',encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
        runpy.run_path(str(num/script),run_name='__main__')
    result=output.read_text(encoding='utf-8')
    print(script,args,'FAIL occurrences:',result.count('FAIL'), 'output:',output.name,flush=True)
# Verify every line-numbered C++ quotation against frozen text.
import re, math
source=(root/'Scripts/Campaigns/2026-10-28_New_Campaign/code/core/v2_2_1/core/cpp/v3_start.h').read_text(encoding='utf-8').splitlines()
quotes=0
for lemma in (num.parent/'lemmas').glob('*.md'):
    for n,line in enumerate(lemma.read_text(encoding='utf-8').splitlines(),1):
        match=re.match(r'^(\d{3})  (.*)$',line)
        if match:
            quotes+=1
            if source[int(match[1])-1].strip()!=match[2].strip(): print('QUOTE MISMATCH',lemma.name,n)
print('Verified quoted source lines:',quotes)
print('Binomial constants:',math.comb(22,11),math.comb(23,11))
