import json, sys
R = json.load(open(sys.argv[1]))
print('| design | n | L+4 | median η₂(a=1) | mean η₂(a=1) | median ε_del(1) | median c₂(1) | median η₂(2) | median c₂(2) | median 1−π(S₀) | (L+4)·median η₂(1) |')
print('|---|---|---|---|---|---|---|---|---|---|---|')
for r in R:
    m, a = r['median'], r['mean']
    print('| S%d c=0.5 | %d | %d | %.3f | %.3f | %.3f | %.3f | %.3f | %.3f | %.3f | %.2f |' % (
        r['scen'], r['n'], r['L'] + 4, m['eta2_1'], a['eta2_1'], m['epsdel_1'], m['c2_1'], m['eta2_2'], m['c2_2'], m['delta1'], (r['L'] + 4) * m['eta2_1']))
