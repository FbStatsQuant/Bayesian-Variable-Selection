import json,re,glob,os,sys,random
here=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
L=json.load(open(os.path.join(here,'messages_all.json'),encoding='utf-8'))
ref={i['position']:i for i in L}
parts=sorted(glob.glob(os.path.join(here,'archive','transcript','part_*.md')))
got={}; allpos=set()
for f in parts:
    s=open(f,encoding='utf-8').read()
    m=re.search(r'part_\d+_(\d+)-(\d+)\.md',f); a,b=int(m[1]),int(m[2])
    blocks=re.findall(r'<!-- BEGIN pos (\d+) -->\n(.*?)\n<!-- END pos \1 -->',s,re.S)
    act=set(int(x) for x in re.findall(r'^> activity \[pos (\d+)\]',s,re.M))
    hdr=set(int(x) for x in re.findall(r'^### \[pos (\d+)\]',s,re.M))
    poss=set(int(p) for p,_ in blocks)|act
    missing=[p for p in range(a,b+1) if p not in poss]
    for p,t in blocks: got[int(p)]=t
    allpos|=poss
    print(os.path.basename(f),'msgs',len(blocks),'hdrs',len(hdr),'activity',len(act),'covered',len(poss),'of',b-a+1,'missing',missing[:10], 'size',os.path.getsize(f))
bad=[p for p in ref if got.get(p)!=ref[p]['text']]
extra=[p for p in got if p not in ref]
print('ref msgs',len(ref),'transcript msgs',len(got),'mismatch',bad[:20],'extra',extra[:20])
print('total positions covered',len(allpos),'expected 1677', 'gaps',[p for p in range(1677) if p not in allpos][:20])
