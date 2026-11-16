"""DRY-RUN stager (disposable clone only). Records a set of rows as checked under v4 §7 + W3-11 (HQ 4(b)):
own CHECKPOINT status source, council cell, correct:PASS gate, and 'conditional on X' + X@hyp for every lower-assurance
direct input that A3 reports, iterated until A3 is quiet. Optionally clears headline flags. Prints the acceptance result.
python stage_acc.py <clone> <config.json>
config: {ticket, folder, rows:[local ids], council, gates, checkpoint, clear_headline:[local ids], carriers:{path:text}}"""
import json, os, re, subprocess, sys
root, cfg = sys.argv[1], json.load(open(sys.argv[2]))
os.chdir(root)
T = "Theory_work/INFRA/tools"
sys.path.insert(0, T)
sys.dont_write_bytecode = True
import bvsreg as R  # noqa: E402

tk, fold, rows = cfg["ticket"], cfg["folder"], cfg["rows"]
ids = [f"{tk}:{c}" for c in rows]
for p, txt in cfg.get("carriers", {}).items():
    open(p, "w", encoding="utf-8").write(txt)


def sh(*a):
    p = subprocess.run([sys.executable, *a], capture_output=True, text=True)
    if p.returncode and "check.py" not in a[0]:
        sys.exit(f"STOP {a[:3]}: {p.stdout[-400:]} {p.stderr[-400:]}")
    return p


for c in cfg.get("clear_headline", []):
    sh(f"{T}/registry.py", "set", f"{tk}:{c}", "headline=", "--reason", "dry run variant (ii): tool-set flag cleared")
cond = {i: [] for i in ids}       # conditions per claim (canonical ids)
hyp = {i: set() for i in ids}     # inputs to turn into @hyp edges
ck = os.path.join(fold, cfg["checkpoint"])
orig_deps = {i: R.index(R.load_claims())[i]["depends_on"] for i in ids}
orig_gates = {i: R.index(R.load_claims())[i]["gates"] for i in ids}
def gates_for(i):
    kept = [g.strip() for g in re.split(r";\s*(?=[A-Za-z-]+:)", orig_gates[i]) if g.strip() and not g.strip().startswith("correct:")]
    return " ; ".join([cfg["gates"]] + kept)
for it in range(8):
    # (re)write the checkpoint, statuses, edges, council, gates
    lines, at = [f"# {cfg['checkpoint']} — {tk} statuses (HQ record, PROTOCOL_v4 §7; DRY RUN)", ""], {}
    for i in ids:
        rn = cfg.get("rename", {})
        st = "PROVED-CHECKED" + (f", conditional on {', '.join(rn.get(x, x) for x in cond[i])}" if cond[i] else "")
        lines += [i, st]
        at[i] = (len(lines), st)
        lines.append("")
    open(ck, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    al, allids = R.load_aliases(), {r["id"] for r in R.load_claims()}
    for i in ids:
        deps = []
        for d in R.split_list(orig_deps[i]):
            x = R.resolve(d, allids, al, tk)
            if x in hyp[i]:
                if f"{x}@hyp" not in deps:
                    deps.append(f"{x}@hyp")
            else:
                deps.append(d)
        for x in hyp[i]:
            if f"{x}@hyp" not in deps:
                deps.append(f"{x}@hyp")
        sh(f"{T}/registry.py", "correct-status", i, "--status", at[i][1], "--source", f"{ck}:{at[i][0]}",
           "--reason", "dry run")
        sh(f"{T}/registry.py", "set", i, f"council={cfg['council']}", f"gates={gates_for(i)}",
           f"depends_on={'; '.join(deps)}", "--reason", "dry run")
    out = sh(f"{T}/check.py", "--acceptance", *ids).stdout
    errs = [l for l in out.splitlines() if l.startswith("ERROR")]
    new = False
    for e in errs:
        m = re.match(r"ERROR\s+A3-assurance\s+(\S+)\s+status .*? but uses ([^@\s]+)@", e)
        if m and m.group(1) in cond:
            x = R.resolve(m.group(2), allids, al)
            if x and x not in cond[m.group(1)]:
                cond[m.group(1)].append(x); hyp[m.group(1)].add(x); new = True
        m = re.match(r"ERROR\s+A3-condition\s+(\S+)\s+consumes the conditional result \S+, which rests on (\S+) \(via", e)
        if m and m.group(1) in cond:
            w = {v: k for k, v in cfg.get("rename", {}).items()}.get(m.group(2), m.group(2))
            if w not in cond[m.group(1)]:
                cond[m.group(1)].append(w); new = True
    if not new:
        break
print(f"iterations: {it + 1}")
for i in ids:
    print(f"  {i}: PROVED-CHECKED" + (f", conditional on {', '.join(cond[i])}" if cond[i] else ""))
print(f"acceptance {len(ids)} rows: {len(errs)} ERROR")
for e in sorted(set(x[:230] for x in errs))[:25]:
    print("  ", e)
print([l for l in out.splitlines() if l.startswith("acceptance (")][-1:])
