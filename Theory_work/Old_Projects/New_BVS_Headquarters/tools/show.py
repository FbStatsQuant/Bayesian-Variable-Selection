import json,sys,os
here=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
L=json.load(open(os.path.join(here,'messages_all.json'),encoding='utf-8'))
a,b=int(sys.argv[1]),int(sys.argv[2])
out=[]
for i in L:
    if a<=i['position']<=b:
        r='U' if i['type']=='user_message' else 'A'
        if i.get('creationSource')=='mcp': r+='(mcp)'
        out.append(f"\n## [{i['position']}|{r}|run{i['runId'].split(':')[-1]}|{i['updatedAt'][5:16]}]\n{i['text']}")
sys.stdout.reconfigure(encoding='utf-8')
print(''.join(out))
