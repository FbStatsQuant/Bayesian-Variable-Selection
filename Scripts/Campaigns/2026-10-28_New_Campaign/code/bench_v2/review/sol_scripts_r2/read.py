import sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
for arg in sys.argv[1:]:
    bits=arg.rsplit('::',1)
    p=Path(bits[0]); start,end=(1,100000)
    if len(bits)==2: start,end=map(int,bits[1].split('-'))
    print('\nFILE',p)
    for i,line in enumerate(p.read_text(encoding='utf-8-sig').splitlines(),1):
        if start<=i<=end: print(f'{i}: {line}')
