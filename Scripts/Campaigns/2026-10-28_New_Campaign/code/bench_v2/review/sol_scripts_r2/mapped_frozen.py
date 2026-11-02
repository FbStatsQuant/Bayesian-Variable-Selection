"""Review-only execution of original frozen.py with its destination literal mapped locally."""
import sys
from pathlib import Path
original=Path(sys.argv.pop(1)); destination=str(Path(sys.argv.pop(1)))
source=original.read_text(encoding='utf-8')
remote='/home/fb31/projects/BVS/New_Campaign/code/bench_v2/F3_AdaptiveLasso'
assert source.count('if str(dest) != "'+remote+'":')==1
source=source.replace('if str(dest) != "'+remote+'":','if str(dest) != '+repr(destination)+':')
if sys.argv[1]=='stage':
    assert sys.argv[-1]==remote
    sys.argv[-1]=destination
else:
    sys.argv=[destination if v==remote else v for v in sys.argv]
exec(compile(source,str(original),'exec'),{'__name__':'__main__','__file__':str(original)})
