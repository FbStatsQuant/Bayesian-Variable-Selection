import re,os,sys,glob,collections
ROOT=sys.argv[1]; files=sys.argv[2:]
snap=os.path.join(ROOT,'archive','branch_snapshots')
import json
msgs={i['position']:i['text'] for i in json.load(open(os.path.join(ROOT,'messages_all.json'),encoding='utf-8'))}
idx=collections.defaultdict(list)
for dp,_,fs in os.walk(snap):
    for f in fs: idx[f].append(os.path.join(dp,f))
cache={}
def content(p):
    if p not in cache: cache[p]=open(p,encoding='utf-8',errors='replace').read()
    return cache[p]
def strip_q(t):  # remove blockquote prefixes
    return '\n'.join(re.sub(r'^> ?','',l) for l in t.split('\n'))
allmsgs='\n'.join(msgs.values())
for f in files:
    s=open(f,encoding='utf-8').read()
    blocks=re.findall(r'<!-- BEGIN VERBATIM (.*?) -->\n(.*?)\n<!-- END VERBATIM',s,re.S)
    ok=0;bad=[]
    for src,body in blocks:
        cands=[]
        m=re.search(r'([\w.\-@]+\.(?:md|tex|lean|txt))',src)
        if m: cands=idx.get(m.group(1),[])
        texts=[body,strip_q(body)]
        found=False
        for c in cands:
            C=content(c)
            if any(t.strip() and t.strip() in C for t in texts): found=True;break
        if not found:
            # try line-wise containment (all nonempty lines appear)
            for c in cands:
                C=content(c); lines=[l for l in strip_q(body).split('\n') if l.strip()]
                if lines and all(l.strip() in C for l in lines): found='lines';break
        if not found and ('pos' in src):
            if strip_q(body).strip() in allmsgs or body.strip() in allmsgs: found=True
        if found: ok+=1
        else: bad.append((src,len(cands),body[:80].replace('\n',' ')))
    print(os.path.basename(f),'blocks',len(blocks),'ok',ok,'unverified',len(bad))
    for b in bad[:15]: print('   ',b)
