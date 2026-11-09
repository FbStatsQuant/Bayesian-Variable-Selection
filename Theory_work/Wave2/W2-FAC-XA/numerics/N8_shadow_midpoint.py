"""Local falsification only; no gain coupling, production scores, or theorem test."""
import json
import math
import random
from pathlib import Path

OUT = Path(__file__).with_name('N8_shadow_midpoint_results.json')
stats = {'steps': 0, 'midpoint_checks': 0, 'jump_checks': 0,
         'failures': [], 'max_midpoint_residual': 0.0,
         'max_center_bound_residual': 0.0, 'max_width_bound_residual': 0.0,
         'actual_center_outside_shadow_gap': 0}


def gap(values, kept, h):
    left = [values[i] for i in kept if values[i] <= h]
    right = [values[i] for i in kept if values[i] > h]
    return max(left, default=-math.inf), min(right, default=math.inf)


def step(values, kept, h, replacements, E, B, c, eps, j, label):
    m, M = len(kept), len(values)
    q = m + c
    x = (B + sum(values[i] for i in kept)) / q
    nearest = min(abs(values[i] - x) for i in kept)
    assert abs(values[j] - x) <= nearest + eps + 1e-10
    a, b = gap(values, kept, h)
    other = [i for i in kept if i != j]
    distance = abs(values[j] - h)
    d_other = min((abs(values[i] - h) for i in other), default=math.inf)
    v = values[j]
    if distance > d_other:
        v = h + math.copysign(d_other, values[j] - h)
    delta = v - values[j]
    hp = h - (v - h) / (q - 1)
    Ep = max(E, abs(delta))
    past = replacements + [v]
    stats['steps'] += 1
    if not other:
        return other, hp, past, Ep
    ap, bp = gap(values, other, hp)
    xp = (B + sum(values[i] for i in other)) / (q - 1)
    tol = 2e-9 * (1 + max(abs(z) for z in values) + abs(B))

    def check(ok, name, details=None):
        if not ok and len(stats['failures']) < 20:
            stats['failures'].append({'case': label, 'check': name,
                                      'kept': kept, 'j': j, 'detail': details})

    bound = (M - len(other)) * eps / (len(other) + c)
    residual = abs(hp - xp) - bound
    stats['max_center_bound_residual'] = max(stats['max_center_bound_residual'], residual)
    check(residual <= tol, 'center bound', residual)
    width = eps * (1 + 2 * (M - len(other) - 1) / (len(other) + 1 + c))
    residual = Ep - width
    stats['max_width_bound_residual'] = max(stats['max_width_bound_residual'], residual)
    check(residual <= tol, 'width bound', residual)
    check(all(ap - tol <= z <= bp + tol for z in past), 'shadow containment')
    deleted = set(range(M)) - set(other)
    check(all(ap - Ep - tol <= values[i] <= bp + Ep + tol for i in deleted),
          'original containment')
    if xp < ap - tol or xp > bp + tol:
        stats['actual_center_outside_shadow_gap'] += 1
    if all(math.isfinite(z) for z in (a, b, ap, bp)):
        G = max((v2 - v1 for v1, v2 in zip(sorted(values), sorted(values)[1:])), default=0)
        dh = min(h - a, b - h)
        upper = max(abs(a + b - 2 * h), G + 2 * Ep + 2 * dh / (q - 1))
        residual = abs(ap + bp - 2 * hp) - upper
        stats['midpoint_checks'] += 1
        stats['max_midpoint_residual'] = max(stats['max_midpoint_residual'], residual)
        check(residual <= tol, 'MID', residual)
        if values[j] == b:
            stats['jump_checks'] += 1
            check(bp - b <= E + G + tol, 'right gap jump')
        if values[j] == a:
            stats['jump_checks'] += 1
            check(a - ap <= E + G + tol, 'left gap jump')
    return other, hp, past, Ep


def exhaustive(values, B, c, eps, label):
    # No subset memoization: different histories give different shadow centers.
    calls = 0

    def visit(kept, h, replacements, E):
        nonlocal calls
        calls += 1
        if not kept:
            return
        x = (B + sum(values[i] for i in kept)) / (len(kept) + c)
        d = min(abs(values[i] - x) for i in kept)
        for j in kept:
            if abs(values[j] - x) <= d + eps + 1e-12:
                visit(*step(values, kept, h, replacements, E, B, c, eps, j, label))

    visit(list(range(len(values))), (B + sum(values)) / (len(values) + c), [], 0)
    return calls


def sampled(values, B, c, eps, policy, rng, label):
    kept = list(range(len(values)))
    h = (B + sum(values)) / (len(kept) + c)
    replacements, E = [], 0
    while kept:
        x = (B + sum(values[i] for i in kept)) / (len(kept) + c)
        d = min(abs(values[i] - x) for i in kept)
        eligible = [i for i in kept if abs(values[i] - x) <= d + eps + 1e-12]
        if policy == 'nearest':
            j = min(eligible, key=lambda i: abs(values[i] - x))
        elif policy == 'farthest':
            j = max(eligible, key=lambda i: abs(values[i] - x))
        elif policy == 'farther_shadow_side':
            a, b = gap(values, kept, h)
            D = a + b - 2 * h
            j = max(eligible, key=lambda i: (math.copysign(1, values[i] - h) * D,
                                             abs(values[i] - h)))
        else:
            j = rng.choice(eligible)
        kept, h, replacements, E = step(values, kept, h, replacements, E,
                                        B, c, eps, j, label)


def main():
    deterministic = []
    configurations = [([-3, -2, -1, 1, 2, 3], 0),
                      ([-1.2, -.8, -.1, .02, .4, 1.5, 2], .3),
                      ([.1, .1001, 2], -2.2001),
                      ([-.5, 1.5], -1),
                      ([-1.78, -.78, -.53, -.09, -.05, .28, .43, .57], 0)]
    for index, (values, B) in enumerate(configurations):
        for c in (1.5, 3.0):
            for eps in (0.0, .01, .5, 1.0):
                label = f'deterministic-{index}-c{c}-eps{eps}'
                calls = exhaustive(values, B, c, eps, label)
                deterministic.append({'case': label, 'history_nodes': calls})
    policies = ['nearest', 'farthest', 'farther_shadow_side', 'random']
    paths = 0
    for seed in range(20):
        rng = random.Random(seed)
        for M in (64, 256):
            values = [rng.gauss(0, 1) for _ in range(M)]
            B = rng.gauss(0, 1)
            for eps in (1e-6, .01, .25):
                for policy in policies:
                    sampled(values, B, 2.5, eps, policy, rng,
                            f'seed{seed}-M{M}-eps{eps}-{policy}')
                    paths += 1
    result = {'scope': 'falsification only; no empirical theorem probability claim',
              'seeds': list(range(20)), 'gaussian_paths': paths,
              'deterministic_configurations': deterministic, 'checks': stats}
    OUT.write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps({'output': str(OUT), 'paths': paths, 'checks': stats}, indent=2))
    if stats['failures']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
