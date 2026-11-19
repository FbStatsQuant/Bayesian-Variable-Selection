import glob, json, os, importlib.util, math, sys
OPS = "/home/fb31/BVS-wt/P1M/Docs/Experiments/P1M/results/precision1e4/ops_tools/stop_rules_prec.py"
sp = importlib.util.spec_from_file_location("srp", OPS); srp = importlib.util.module_from_spec(sp); sp.loader.exec_module(srp)
R = os.path.expanduser("~/SMC_Engineering_Department/records/precision1e4")
rows = []
for w in ["A0","P1","P2","P3","P4","B1"]+["S%d"%i for i in range(1,11)]:
    for f in sorted(glob.glob(R+"/%s/_batch_*/cost/cost_4-*.json"%w)):
        j = json.load(open(f)); rid = j["run_id"]
        if "batch" in os.path.basename(f) : continue
        st = j["stages"]
        try: k = srp.klass(rid)
        except Exception as e: k = "ERR %s"%e
        rows.append(dict(wave=w, rid=rid, klass=k, core_h=j["billed_core_h"], stages={s:v["billed_core_h"] for s,v in st.items()}, wall={s:v["wall_s_max"] for s,v in st.items()}, rss={s:v["max_rss_bytes"] for s,v in st.items()}, tasks={s:v["tasks"] for s,v in st.items()}))
print(len(rows), "fits; total core-h %.2f" % sum(r["core_h"] for r in rows))
json.dump(rows, open("costs.json","w"), indent=1)
cl = {}
for r in rows: cl.setdefault(r["klass"], []).append(r)
for k, rs in sorted(cl.items()):
    print(k, len(rs), round(sum(x["core_h"] for x in rs)/len(rs),3), round(max(x["core_h"] for x in rs),3), srp.TABLE.get(k))
