# Check only whitelisted external citations; never execute citecheck.py itself,
# because its final external check reads TRIAGE.md, outside this seat's allowlist.
import ast, pathlib, sys
sys.dont_write_bytecode=True
base=pathlib.Path(__file__).resolve().parents[2]
repo=base.parents[2]
tree=ast.parse((base/'citecheck.py').read_text(encoding='utf-8'))
checks=next(x.value for x in tree.body if isinstance(x,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='CHECKS' for t in x.targets))
checks=eval(compile(ast.Expression(checks),'<checks>','eval'),{'W':'Theory_work/Wave3/'})
count=0
for f,a,b,tokens,where in checks:
    if 'API_AUDIT' in f: continue
    seg='\n'.join((repo/f).read_text(encoding='utf-8').splitlines()[a-1:b])
    for tok in tokens:
        assert tok in seg,(f,a,b,tok)
        count+=1
print(count,'whitelisted external citation-token checks PASS; TRIAGE check excluded by brief.')
