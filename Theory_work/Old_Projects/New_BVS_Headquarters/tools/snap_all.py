import subprocess,os,hashlib
D="/home/fb31/Bayesian-Variable-Selection/Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots"
lines=subprocess.run(["git","for-each-ref","--format=%(refname:short) %(objectname:short)","refs/remotes/origin/theory/"],stdout=subprocess.PIPE,universal_newlines=True).stdout.split("\n")
branches={}
for l in lines:
    if l.strip():
        r,c=l.split(); branches[r.split("origin/theory/")[1]]=(r,c)
TEXT=("md","tex","lean")
man=[]; other=[]; written=0
def ls(r,prefix):
    out=subprocess.run(["git","ls-tree","-r","-l",r,"--",prefix],stdout=subprocess.PIPE,universal_newlines=True).stdout
    for line in out.splitlines():
        meta,path=line.split("\t",1); mode,typ,sha,size=meta.split()
        if size!="-": yield path,sha,int(size)
def ext_of(path):
    fn=path.rsplit("/",1)[-1]
    return fn.rsplit(".",1)[-1].lower() if "." in fn else ""
def dump(b,c,path,sha,rel):
    global written
    data=subprocess.run(["git","cat-file","blob",sha],stdout=subprocess.PIPE).stdout
    out=os.path.join(D,rel)
    os.makedirs(os.path.dirname(out),exist_ok=True); open(out,"wb").write(data); written+=len(data)
    man.append("%s  %d  theory/%s@%s  %s  ->  branch_snapshots/%s" % (hashlib.sha256(data).hexdigest(),len(data),b,c,path,rel))
for b,(r,c) in sorted(branches.items()):
    pre="theory_campaign/"+b+"/"
    for path,sha,size in ls(r,pre):
        if ext_of(path) in TEXT: dump(b,c,path,sha,b+"/"+path[len(pre):])
        else: other.append("theory/%s@%s\t%s\t%d\tgit-blob:%s" % (b,c,path,size,sha))
r,c=branches["campaign"]
for path,sha,size in ls(r,"theory_campaign/"):
    top=path.split("/")[1]
    if top in branches and top!="campaign": continue
    if ext_of(path) in TEXT: dump("campaign",c,path,sha,"campaign/"+path[len("theory_campaign/"):])
    else: other.append("theory/campaign@%s\t%s\t%d\tgit-blob:%s" % (c,path,size,sha))
open(os.path.join(D,"SNAPSHOT_MANIFEST.txt"),"w").write("# sha256  bytes  source-ref  source-path  ->  archive-path\n"+"\n".join(man)+"\n")
open(os.path.join(D,"NONTEXT_INDEX.tsv"),"w").write("ref\tpath\tbytes\tgit_blob\n"+"\n".join(other)+"\n")
print("text files",len(man),"bytes",written,"nontext indexed",len(other))
