"""Open every explicitly registered path:line and check exact supporting text.
Also detect unregistered repository path:line citations in lead-authored markdown.
Verbatim reviewer files are evidence, not editable lead citations.
"""
from pathlib import Path
import json,re,sys
sys.stdout.reconfigure(encoding='utf-8')
root=Path(__file__).resolve().parents[4]
ticket=root/'Theory_work/Wave2/W2-FAC-XA'
anchors=[
 ('Theory_work/Wave2/W2-FAC-B/REPORT.md','PROVED-CHECKED'),
 ('Theory_work/Wave2/W2-FAC-A/REPORT.md','flagged target STATEMENT.md v1.2)'),
 ('Theory_work/Wave2/W2-FAC-B/STATEMENT.md','XF VERIFIED (A-REV2)'),
 ('Theory_work/Wave2/W2-FAC-B/STATEMENT.md','addition checked in A4'),
 ('Theory_work/Wave2/PROTOCOL.md','all target results are asymptotic'),
 ('Theory_work/Wave1/PROTOCOL.md','Mid-point REDIRECT/STOP'),
]
manifest=[];fails=[]
for path,token in anchors:
 lines=(root/path).read_text(encoding='utf-8').splitlines()
 hits=[(i+1,line) for i,line in enumerate(lines) if token in line]
 if not hits:
  fails.append('MISSING TOKEN '+path+' '+token);continue
 line,text=hits[0];manifest.append(dict(path=path,line=line,quote=text))
(ticket/'reviews/CITATIONS.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
out=[]
for item in manifest:
 actual=(root/item['path']).read_text(encoding='utf-8').splitlines()[item['line']-1]
 ok=actual==item['quote'];out.append(('PASS ' if ok else 'FAIL ')+item['path']+':'+str(item['line'])+' '+actual)
 if not ok:fails.append(str(item))
pattern=re.compile(r'(Theory_work/[A-Za-z0-9_./-]+\.(?:md|tex|py|R)):(\d+)')
for f in list(ticket.glob('*.md'))+list((ticket/'lemmas').glob('*.md')):
 for path,line in pattern.findall(f.read_text(encoding='utf-8')):
  lines=(root/path).read_text(encoding='utf-8').splitlines() if (root/path).exists() else []
  valid=1<=int(line)<=len(lines)
  out.append(('LOCATION PASS ' if valid else 'FAIL ')+path+':'+line)
  if not valid:fails.append(path+':'+line)
out.append('Failures: '+str(len(fails)));out.extend(fails)
(ticket/'reviews/CITECHECK.txt').write_text('\n'.join(out)+'\n',encoding='utf-8')
print('\n'.join(out));raise SystemExit(bool(fails))
