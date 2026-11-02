import pathlib,json,hashlib,subprocess
r=pathlib.Path('theory_campaign/A-REV8'); rows=json.loads((r/'sources/manifest.json').read_text());bad=[]
for v in rows:
 name=(v['ref'].split('/')[-1]+'__'+v['path'].split(v['ref'].split('/')[-1]+'/')[-1].replace('/','__')) if 'ref' in v else pathlib.Path(v['path']).name
 p=r/'sources'/name
 if hashlib.sha256(p.read_bytes()).hexdigest()!=v['sha256']:bad.append(str(p))
print('source hash mismatches:',bad)
assert not bad
