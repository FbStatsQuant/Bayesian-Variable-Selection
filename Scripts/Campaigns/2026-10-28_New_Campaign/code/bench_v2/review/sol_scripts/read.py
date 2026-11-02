import sys
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
C=Path('C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign')
for arg in sys.argv[1:]:
    parts=arg.split('@'); p=C/parts[0]
    print('\nFILE',parts[0])
    lines=p.read_text(encoding='utf-8-sig').splitlines()
    lo,hi=map(int,parts[1].split(':')) if len(parts)>1 else (1,len(lines))
    for i,s in enumerate(lines,1):
        if lo<=i<=hi: print(f'{i}: {s}')
