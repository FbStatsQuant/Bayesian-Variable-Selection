import pathlib
p=pathlib.Path('theory_campaign/A-REV4/nm_check.py')
s=p.read_text(encoding='utf-8-sig').replace('rows=[]','rows=[]; raw=[]')
s=s.replace('residuals.append(b2-n/2*math.log(1/(1-.25/2))+.5*math.log(n));','raw.append(dict(n=n,rep=rep,logBF_proxy=b2,posterior=post,start=ini)); residuals.append(b2-n/2*math.log(1/(1-.25/2))+.5*math.log(n));')
s += '\nwith open("nm_raw.json", "w") as f: json.dump(raw,f)\n'
pathlib.Path('theory_campaign/A-REV4/nm_raw_check.py').write_text(s)
