"""R07 independent exact-rational adversarial check of L7 sections 2 (deterministic).
Exhaustive AN histories on small random rational configurations, incl. ties and
points equal to the shadow centre. Checks, at every step:
 C1 replacement v = h + sign*d_h when both sides exist (clipped position);
 C2 right (left) selection with D>0 (D<0) => |D| <= |delta|;
 C3 endpoint jump g <= E_t + G (old certificate);
 C4 exact identity D' = D + g + 2 d_h/(q-1) (right) / D - g - 2d_h/(q-1) (left);
 C5 MID; C6 certificate (past v in closed new gap, deleted originals within E of gap);
 C7 L3 centre and width bounds; C8 nestedness of gaps.
Also records whether h ever coincides with a retained coordinate (tie convention)."""
from fractions import Fraction as F
import random, json, sys
from pathlib import Path

INF = None
stats = dict(steps=0, both_side_steps=0, clip_checks=0, sel_checks=0, jump_checks=0,
             ident_checks=0, mid_checks=0, cert_checks=0, h_on_point=0, failures=[])

def fail(name, info):
    if len(stats['failures']) < 30:
        stats['failures'].append({'check': name, **{k: str(v) for k, v in info.items()}})

def gap(vals, kept, h):
    L = [vals[i] for i in kept if vals[i] <= h]
    R = [vals[i] for i in kept if vals[i] > h]
    return (max(L) if L else None), (min(R) if R else None)

def run(vals, B, c, eps, cap):
    M = len(vals)
    srt = sorted(vals)
    G = max(b - a for a, b in zip(srt, srt[1:]))
    nodes = [0]
    def visit(kept, h, past, E):
        nodes[0] += 1
        if nodes[0] > cap or len(kept) <= 1:
            return
        m = len(kept); q = m + c
        x = (B + sum(vals[i] for i in kept)) / q
        dmin = min(abs(vals[i] - x) for i in kept)
        a, b = gap(vals, kept, h)
        if any(vals[i] == h for i in kept):
            stats['h_on_point'] += 1
        for j in kept:
            if abs(vals[j] - x) > dmin + eps:
                continue
            other = [i for i in kept if i != j]
            dist = abs(vals[j] - h)
            dother = min(abs(vals[i] - h) for i in other)
            v = vals[j]
            if dist > dother:
                v = h + dother if vals[j] > h else h - dother
            delta = v - vals[j]
            hp = h - (v - h) / (q - 1)
            Ep = max(E, abs(delta))
            pastp = past + [v]
            ap, bp = gap(vals, other, hp)
            xp = (B + sum(vals[i] for i in other)) / (q - 1)
            stats['steps'] += 1
            info = dict(vals=vals, B=B, c=c, eps=eps, kept=kept, j=j, h=h)
            # C6 certificate
            stats['cert_checks'] += 1
            for z in pastp:
                if (ap is not None and z < ap) or (bp is not None and z > bp):
                    fail('C6 past v outside gap', info)
            for i in set(range(M)) - set(other):
                if (ap is not None and vals[i] < ap - Ep) or (bp is not None and vals[i] > bp + Ep):
                    fail('C6 deleted outside band', info)
            for i in other:
                if ap is not None and bp is not None and ap < vals[i] < bp:
                    fail('C6 retained in open gap', info)
            # C7
            t1 = M - len(other)
            if abs(hp - xp) > t1 * eps / (len(other) + c):
                fail('C7 centre', info)
            if Ep > eps * (1 + F(2 * (t1 - 1)) / (len(other) + 1 + c)):
                fail('C7 width', info)
            if None not in (a, b, ap, bp):
                stats['both_side_steps'] += 1
                L, R = h - a, b - h
                dh = min(L, R); D = R - L
                right = vals[j] > h
                stats['clip_checks'] += 1
                if v != (h + dh if right else h - dh):
                    fail('C1 clip position', info)
                stats['sel_checks'] += 1
                if right and D > 0 and D > abs(delta):
                    fail('C2 right selection', info)
                if (not right) and D < 0 and -D > abs(delta):
                    fail('C2 left selection', info)
                # C8 nested
                if not (ap <= a and bp >= b):
                    fail('C8 nested', info)
                g = (bp - b) if right else (a - ap)
                if (right and vals[j] == b) or ((not right) and vals[j] == a):
                    stats['jump_checks'] += 1
                    if g > E + G or g < 0:
                        fail('C3 jump', info)
                elif g != 0:
                    fail('C3 nonendpoint g!=0', info)
                Dp = bp + ap - 2 * hp
                stats['ident_checks'] += 1
                expect = D + g + 2 * dh / (q - 1) if right else D - g - 2 * dh / (q - 1)
                if Dp != expect:
                    fail('C4 identity', dict(info, Dp=Dp, expect=expect))
                stats['mid_checks'] += 1
                if abs(Dp) > max(abs(D), G + 2 * Ep + 2 * dh / (q - 1)):
                    fail('C5 MID', info)
            visit(other, hp, pastp, Ep)
    visit(list(range(M)), (B + sum(vals)) / (M + c), [], F(0))
    return nodes[0]

def main():
    rng = random.Random(7)
    configs = 0; nodes = 0
    for trial in range(400):
        M = rng.choice([4, 5, 6, 7])
        den = rng.choice([4, 8, 10])
        vals = [F(rng.randint(-3 * den, 3 * den), den) for _ in range(M)]
        if trial % 5 == 0 and M >= 3:      # force ties
            vals[1] = vals[0]
        B = F(rng.randint(-2 * den, 2 * den), den)
        c = rng.choice([F(5, 4), F(3, 2), F(3)])
        eps = rng.choice([F(0), F(1, 20), F(1, 4), F(1), F(3)])
        nodes += run(vals, B, c, eps, cap=200000)
        configs += 1
    stats['configs'] = configs; stats['history_nodes'] = nodes
    out = Path(__file__).with_name('r07_exact_out.json')
    out.write_text(json.dumps(stats, indent=1))
    print(json.dumps({k: v for k, v in stats.items() if k != 'failures'}, indent=1))
    print('failures', len(stats['failures']))
    for f in stats['failures'][:10]:
        print(f)

main()
