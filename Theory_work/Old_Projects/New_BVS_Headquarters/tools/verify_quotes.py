import os,sys,re,json
ROOT=sys.argv[1]; files=sys.argv[2:]
corpus=[]
for dp,_,fs in os.walk(os.path.join(ROOT,'archive','branch_snapshots')):
    for f in fs:
        if f.endswith(('.md','.tex','.lean','.txt','.diff')): corpus.append(open(os.path.join(dp,f),encoding='utf-8',errors='replace').read())
corpus.append('\n'.join(i['text'] for i in json.load(open(os.path.join(ROOT,'messages_all.json'),encoding='utf-8'))))
corpus.append('\n'.join((i.get('text') or '') for i in json.load(open(os.path.join(ROOT,'activity_all.json'),encoding='utf-8'))))
C='\n'.join(corpus)
Cn=re.sub(r'\s+',' ',C)
for f in files:
    lines=open(f,encoding='utf-8').read().split('\n')
    runs=[];cur=[]
    for l in lines:
        if l.lstrip().startswith('>'): cur.append(re.sub(r'^\s*> ?','',l))
        else:
            if cur: runs.append(cur); cur=[]
    if cur: runs.append(cur)
    exact=ws=linewise=0; bad=[]
    for r in runs:
        t='\n'.join(r).strip()
        if not t or t.startswith(('Summary','Source')): exact+=1; continue
        if t in C: exact+=1; continue
        if re.sub(r'\s+',' ',t) in Cn: ws+=1; continue
        ls=[x.strip() for x in r if x.strip() and not x.strip().startswith(('[…]','[...]','…'))]
        if ls and all(re.sub(r'\s+',' ',x) in Cn for x in ls): linewise+=1; continue
        bad.append(t[:120].replace('\n',' | '))
    print(f"{os.path.basename(f)} quotes {len(runs)} exact {exact} ws-only {ws} linewise {linewise} UNMATCHED {len(bad)}")
    for b in bad[:6]: print('    ',b)
