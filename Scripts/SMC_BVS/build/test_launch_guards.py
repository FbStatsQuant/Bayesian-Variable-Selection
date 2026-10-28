"""Non-numerical guard tests; root executes on Owls under nice19."""
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile

snapshot = Path(sys.argv[1]).resolve()
root = Path('/home/fb31/smcbvs_v3_deploy_20261022/A_build').resolve()
assert root in snapshot.parents
records = []
for name in ('launch.sh', 'job.sh'):
    script = snapshot / 'build' / name
    source = script.read_text()
    expression = re.search(r"awk -v l=.*? '(BEGIN \{[^']+\})'", source).group(1)
    for load, mem, expected in ((40,31457280,0),(40.01,31457280,1),(40,31457279,1),(0,70000000,0)):
        result = subprocess.run(['awk','-v',f'l={load}','-v',f'm={mem}',expression], capture_output=True,text=True)
        assert result.returncode == expected, (name,load,mem,result.stderr)
        records.append({'script':name,'check':'admission boundary','load':load,'available_kb':mem,'exit':result.returncode})
with tempfile.TemporaryDirectory(prefix='guard_', dir=root) as temp:
    private = Path(temp)
    escape = private / 'escape'
    escape.symlink_to('/proc', target_is_directory=True)
    for name in ('launch.sh','job.sh'):
        script = snapshot / 'build' / name
        run = private.name + '_' + name.replace('.','_')
        out = root / 'runs' / run if name == 'launch.sh' else private / 'output'
        second = run if name == 'launch.sh' else str(out)
        smoke = [str(snapshot/'reference/gen_dev_data.R'),str(private/'inputs'),str(private/'results'),'500','c100','2','24']
        cases = [
            ('relative input', smoke[:1]+['relative_input']+smoke[2:], 'Smoke paths must be absolute'),
            ('relative output', smoke[:2]+['relative_output']+smoke[3:], 'Smoke paths must be absolute'),
            ('symlink input escape', smoke[:1]+[str(escape/'input')]+smoke[2:], 'Smoke path outside A ownership'),
            ('symlink output escape', smoke[:2]+[str(escape/'output')]+smoke[3:], 'Smoke path outside A ownership'),
            ('allocation mismatch', smoke[:5]+['8','24'], '2 GiB'),
        ]
        for label,args,message in cases:
            result=subprocess.run(['bash',str(script),str(snapshot),second,'smoke',*args],cwd=private,capture_output=True,text=True)
            assert result.returncode == 2 and message in result.stderr, (name,label,result.returncode,result.stderr)
            assert not out.exists(), (name,label,'created output before refusal')
            records.append({'script':name,'check':label,'exit':result.returncode,'stderr':result.stderr.strip()})
    # Direct job output containment and launcher preexisting run symlink.
    result=subprocess.run(['bash',str(snapshot/'build/job.sh'),str(snapshot),str(escape/'output'),'build'],capture_output=True,text=True)
    assert result.returncode == 2 and 'Path outside A ownership' in result.stderr
    records.append({'script':'job.sh','check':'output symlink escape','exit':result.returncode})
    run_link=root/'runs'/private.name
    assert not run_link.exists()
    run_link.symlink_to('/proc',target_is_directory=True)
    try:
        result=subprocess.run(['bash',str(snapshot/'build/launch.sh'),str(snapshot),private.name,'build'],capture_output=True,text=True)
        assert result.returncode == 2 and 'Output outside A ownership' in result.stderr
        records.append({'script':'launch.sh','check':'run symlink escape','exit':result.returncode})
    finally:
        run_link.unlink()
print(json.dumps({'passed':len(records),'checks':records},indent=2))
