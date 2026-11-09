"""Exact rational checks of the fixed witness and deterministic end states."""
from fractions import Fraction as F
from pathlib import Path
import json


def rational_shadow():
    values = list(map(F, ['-1.78', '-.78', '-.53', '-.09', '-.05',
                          '.28', '.43', '.57', '.67', '1.52']))
    kept = list(range(10))
    c, eps, B = F('1.5'), F('.5'), F(0)
    h = sum(values) / (10 + c)
    E = F(0)
    replacements = []
    G = max(v-u for u, v in zip(values, values[1:]))
    checks = 0
    for j in [2, 3, 8, 7, 5, 6, 1]:
        q = len(kept) + c
        x = (B + sum(values[i] for i in kept)) / q
        assert abs(values[j]-x) <= min(abs(values[i]-x) for i in kept)+eps
        a = max(values[i] for i in kept if values[i] <= h)
        b = min(values[i] for i in kept if values[i] > h)
        other = [i for i in kept if i != j]
        distance = min(abs(values[i]-h) for i in other)
        v = values[j]
        if abs(v-h) > distance:
            v = h + (distance if v > h else -distance)
        Ep = max(E, abs(v-values[j]))
        hp = h-(v-h)/(q-1)
        ap = max(values[i] for i in other if values[i] <= hp)
        bp = min(values[i] for i in other if values[i] > hp)
        assert abs(ap+bp-2*hp) <= max(abs(a+b-2*h), G+2*Ep+2*min(h-a,b-h)/(q-1))
        if values[j] == b:
            assert bp-b <= E+G
        if values[j] == a:
            assert a-ap <= E+G
        replacements.append(v)
        assert all(ap <= z <= bp for z in replacements)
        xp = (B+sum(values[i] for i in other))/(q-1)
        assert abs(hp-xp) <= (10-len(other))*eps/(len(other)+c)
        assert Ep <= eps*(1+2*(10-len(other)-1)/(len(other)+1+c))
        h, E, kept = hp, Ep, other
        checks += 1
    return checks


def end_states():
    H, w, eps, c = F(10), F(1, 10000), F(1, 1000000), F('1.5')
    checks = 0
    for m in range(1, 21):
        for plus in range(m+1):
            I = 2*plus-m
            for B in [F('-.01'), F('.01')]:
                values = [(H-F(i+1, m+1)*w)*(1 if i < plus else -1)
                          for i in range(m)]
                q = m+c
                x = (B+sum(values))/q
                assert H-abs(x) > w
                e = abs(B)+m*w
                assert abs(q*x-I*H) <= e
                if I:
                    distances = [abs(v-x) for v in values]
                    d = min(distances)
                    assert 2*(H-e)/q-w > eps
                    assert all((v > 0) == (I > 0)
                               for v, dist in zip(values, distances) if dist <= d+eps)
                    if abs(I) >= 2:
                        assert F(abs(I)-1, 1)/(q-1) <= F(abs(I), 1)/q
                checks += 1
    return checks


result = {'arithmetic': 'exact Fraction', 'rational_shadow_steps': rational_shadow(),
          'deterministic_end_states': end_states(), 'failures': 0,
          'scope': 'fixed finite algebraic checks, not an asymptotic probability test'}
Path(__file__).with_name('N8_verify_results.json').write_text(json.dumps(result, indent=2))
print(json.dumps(result, indent=2))
