s = open("n3_twomodel.py").read()
s = s.replace('''        rmax = 0.0
        for t in T:
            w = lg0 + t * d; lz = logsumexp(w)
            if i1 == i2: r = 1 - math.exp(w[i1] - lz)
            else: r = 1 - math.exp(w[i1] - lz) - math.exp(w[i2] - lz)
            rmax = max(rmax, r)
''', '''        def rmax_on(hi):
            m = 0.0
            for t in np.linspace(0, hi, 4001):
                w = lg0 + t * d; lz = logsumexp(w)
                r = 1 - math.exp(w[i1] - lz) - (0.0 if i1 == i2 else math.exp(w[i2] - lz))
                m = max(m, r)
            return m
        rmax = rmax_on(2.0); r125 = rmax_on(1.25); r150 = rmax_on(1.5)
        def Bfun(eps):
            th = 0.9 / (1 - eps) ** 2; s0 = 2 * math.atanh(math.sqrt(1 - th)); lam = math.log(th / (1 - th))
            return 1 + math.ceil((2 * lam + 2 * s0) / (s0 / 2)) + math.ceil(math.log(max(1, (-x0 - lam) / (2 * s0))) / math.log(4 / 3))
''')
s = s.replace("x0=x0, D=D, r_max=rmax,\n                   B=np.nan, Nb_le_B=None)",
 "x0=x0, D=D, r_max=rmax, r_max_125=r125, r_max_150=r150,\n                   B=np.nan, Nb_le_B=None, B125=np.nan, Nb_le_B125=None)")
a = s.index("        if rmax <= 0.02:"); b = s.index("        rows.append(row)")
s = s[:a] + '''        if rmax <= 0.02:
            row["B"] = Bfun(rmax); row["Nb_le_B"] = Nb <= row["B"]
        if r125 <= 0.02:
            row["B125"] = Bfun(r125) + math.ceil(math.log(2.25 / 0.25) / math.log(4 / 3)) + 1; row["Nb_le_B125"] = Nb <= row["B125"]
''' + s[b:]
s = s.replace('''       f"fraction r_max <= 0.01: {np.mean(R<=0.01):.3f} ({int((R<=0.01).sum())}/{N}); <= 0.02: {np.mean(R<=0.02):.3f} ({int((R<=0.02).sum())}/{N}).", ""]''',
'''       f"fraction r_max <= 0.01: {np.mean(R<=0.01):.3f} ({int((R<=0.01).sum())}/{N}); <= 0.02: {np.mean(R<=0.02):.3f} ({int((R<=0.02).sum())}/{N}).", ""]
for key, nm in (("r_max", "[0,2]"), ("r_max_150", "[0,1.5]"), ("r_max_125", "[0,1.25]")):
    A = np.array([r[key] for r in rows])
    out.append(f"range {nm}: quantiles (0,50,90,100%) " + ", ".join(f"{q:.4g}" for q in np.quantile(A, [0, .5, .9, 1])) + f"; frac <=0.01: {np.mean(A<=0.01):.3f} ({int((A<=0.01).sum())}/{N}); frac <=0.02: {np.mean(A<=0.02):.3f} ({int((A<=0.02).sum())}/{N})")
ok125 = [r for r in rows if r["Nb_le_B125"] is not None]
if ok125:
    out.append(f"B125 (eps = r_max_125, plus ceil(log(9)/log(4/3))+1 = {math.ceil(math.log(9)/math.log(4/3))+1}) evaluated on {len(ok125)}: max N_b {max(r['N_b_replay'] for r in ok125)}, min/max B125 {min(r['B125'] for r in ok125)}/{max(r['B125'] for r in ok125)}, max N_b/B125 {max(r['N_b_replay']/r['B125'] for r in ok125):.4f}; N_b > B125: {sum(not r['Nb_le_B125'] for r in ok125)}")
    for r in ok125:
        if not r["Nb_le_B125"]: out.append(f"  VIOLATION125 {r['file']} tier {r['tier']} {r['label']}: N_b={r['N_b_replay']} B125={r['B125']}")
out.append("")''')
open("n3_twomodel.py", "w").write(s)
