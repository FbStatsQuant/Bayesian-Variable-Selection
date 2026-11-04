# summarise.py -- condense results/{A,B,C}_*.txt into results/summary.txt (max over phi and over Gibbs coordinates).
import re, glob, os
here = os.path.dirname(os.path.abspath(__file__)); res = os.path.join(here, "..", "results")
rows = []
for f in sorted(glob.glob(os.path.join(res, "[ABC]_*.txt"))):
    tag = os.path.basename(f)[:-4]; cur = {}
    phi = None
    for line in open(f):
        m = re.match(r"== phi = ([\d.]+) ==", line)
        if m: phi = m.group(1); continue
        m = re.match(r"\s+(.+?)\s+rowsum_err=(\S+)\s+\|\|piK-pi\|\|_1=(\S+)\s+DB abs=(\S+)\s+DB rel\(all\)=(\S+)\s+DB rel\(flows>1e-13\)=(\S+)", line)
        if m and phi is not None:
            name = re.sub(r"Gibbs j=\d+", "Gibbs (all j)", m.group(1).strip())
            vals = [float(x) for x in m.groups()[1:]]
            key = (name, phi)
            cur[key] = [max(a, b) for a, b in zip(cur.get(key, vals), vals)]
    for (name, phi), v in cur.items(): rows.append((tag, phi, name, v))
with open(os.path.join(res, "summary.txt"), "w") as o:
    o.write("%-26s %-5s %-30s %10s %12s %10s %12s %14s\n" % ("design", "phi", "kernel", "rowsum", "||piK-pi||1", "DB abs", "DB rel(all)", "DB rel(>1e-13)"))
    for tag, phi, name, v in rows:
        o.write("%-26s %-5s %-30s %10.2e %12.2e %10.2e %12.2e %14.2e\n" % (tag, phi, name, *v))
print(open(os.path.join(res, "summary.txt")).read())
