import json, sys
for f in sys.argv[1:]:
    print(f)
    for l in open(f):
        if not l.startswith('{'): print(l.strip()[:200]); continue
        d = json.loads(l)
        print({k: d[k] for k in ['S','c','rep','M','phi0sq','maxR','maxR_null','kappa_EXP','lemma13_cert','log10_pi0S0','pi0_R0','pi0_R2','draws_true_q10_50_90','draws_extra_mean','mode_size'] if k in d}, 'nmiss', len(d['mode_missing']))
