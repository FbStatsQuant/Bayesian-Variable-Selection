#!/usr/bin/env python3
"""vec_check.py -- checks the recorded sbatch argument vectors of a PROD-L submission against DESIGN.md sections 5 and 7.

Input: the file written by the sbatch stub of tests/lib.sh (one argument per line, calls separated by '---CALL n'). The stub returns job id ID_BASE+n for
call n, so the step of each id is known from the job name of that call. Effective options of a call = its argv options, completed by the '#SBATCH' lines
of the script it submits (the pilot keeps the job name / cpus / mem / time in the script header, the driver adds the array and the dependency).
Prints one 'PASS name' or 'FAIL name: detail' line per check family. Exit status 0 always (the shell side counts the lines).

Kinds: main (the 10-step main wave or a --pieces subset), r (resubmission wave), p5 (P5 wave), p5scan (the single scan job).
Written from the spec only; never reads the builder's scripts except the sbatch script a vector names (for its #SBATCH header).
"""
import argparse
import os
import re
import sys

LONG_WITH_VALUE = {
    'job-name', 'array', 'cpus-per-task', 'mem', 'time', 'partition', 'account', 'constraint', 'dependency', 'chdir', 'output', 'error',
    'nodes', 'ntasks', 'export', 'kill-on-invalid-dep', 'mem-per-cpu', 'signal', 'mail-type', 'mail-user', 'qos', 'begin', 'comment', 'gres'}
SHORT = {'J': 'job-name', 'a': 'array', 'c': 'cpus-per-task', 't': 'time', 'p': 'partition', 'A': 'account', 'C': 'constraint',
         'd': 'dependency', 'D': 'chdir', 'o': 'output', 'e': 'error', 'N': 'nodes', 'n': 'ntasks'}


def parse_opts(tokens):
    """tokens -> (options dict, positionals)."""
    opts, pos, i = {}, [], 0
    while i < len(tokens):
        t = tokens[i]
        if t.startswith('--'):
            body = t[2:]
            if '=' in body:
                k, v = body.split('=', 1)
                opts[k] = v
            elif body in LONG_WITH_VALUE and i + 1 < len(tokens):
                opts[body] = tokens[i + 1]
                i += 1
            else:
                opts[body] = ''
        elif t.startswith('-') and len(t) >= 2 and t[1] in SHORT:
            k = SHORT[t[1]]
            if len(t) > 2:
                opts[k] = t[2:].lstrip('=')
            elif i + 1 < len(tokens):
                opts[k] = tokens[i + 1]
                i += 1
        else:
            pos.append(t)
        i += 1
    return opts, pos


def read_calls(path):
    calls, cur = [], None
    with open(path, encoding='utf-8', newline='') as fh:
        for line in fh.read().split('\n'):
            line = line.rstrip('\r')
            if line.startswith('---CALL '):
                cur = []
                calls.append(cur)
            elif cur is not None and line != '':
                cur.append(line)
    return calls


def script_directives(script):
    toks = []
    if not script:
        return toks
    cand = [script]
    if re.match(r'^/[a-zA-Z]/', script):
        cand.append(script[0] + ':' + script[2:])
    for c in cand:
        if os.path.isfile(c):
            with open(c, encoding='utf-8', errors='replace') as fh:
                for ln in fh:
                    m = re.match(r'#SBATCH\s+(.*)$', ln.strip())
                    if m:
                        toks += m.group(1).split()
            break
    return toks


def seconds(t):
    t = t.strip()
    days = 0
    dayform = '-' in t
    if dayform:
        d, t = t.split('-', 1)
        days = int(d)
    p = [int(x) for x in t.split(':')]
    if dayform:
        p = p + [0] * (3 - len(p))
        return days * 86400 + p[0] * 3600 + p[1] * 60 + p[2]
    if len(p) == 1:
        return p[0] * 60
    if len(p) == 2:
        return p[0] * 60 + p[1]
    return p[0] * 3600 + p[1] * 60 + p[2]


def mem_mb(v):
    m = re.match(r'^(\d+)([KMGT]?)B?$', v.strip().upper())
    if not m:
        return None
    n, u = int(m.group(1)), m.group(2) or 'M'
    return {'K': n // 1024, 'M': n, 'G': n * 1024, 'T': n * 1024 * 1024}[u]


def parse_deps(v, id2name):
    out = {}
    for part in re.split(r'[,?]', v or ''):
        part = part.strip()
        if not part:
            continue
        typ, _, rest = part.partition(':')
        ids = [x for x in rest.split(':') if x]
        out.setdefault(typ, set()).update(id2name.get(int(x), 'id' + x) if x.isdigit() else x for x in ids)
    return out


STEP = {  # step: (cpus, mem_mb, time_s)  -- PROD_L_BENCH DESIGN sections 3-4. s9_collect: cpus/mem/time are not specified beyond 1 CPU (checked as None below)
    's0_verify': (1, 2048, 1800), 's1_bench': (1, 1024, 3600), 's2_benchretry': (1, 1024, 3600), 's9_collect': (1, None, None)}
PIECE_STEP = {'bench': 's1_bench', 'benchretry': 's2_benchretry'}
THROTTLE = {'s1_bench': {'alone': 32, 'withH': 16}, 's2_benchretry': {'alone': 32, 'withH': 16}}
MAIN_ARRAY = {'s1_bench': '0-95'}


def expected_main(pieces, profile):
    """main wave: s0_verify -> s1_bench (afterok verify) -> s9_collect (afterany); NO lock / unlock steps"""
    exp = {'s0_verify': (None, {}),
           's1_bench': ('%s%%%d' % (MAIN_ARRAY['s1_bench'], THROTTLE['s1_bench'][profile]), {'afterok': {'s0_verify'}}),
           's9_collect': (None, {'afterany': {'s0_verify', 's1_bench'}})}
    return exp


def expected_later(arrays, profile):
    """arrays: ordered list of (step, array-spec-base, throttle-max or None); later waves: arrays (no verify step) + s9_collect afterany the arrays"""
    exp = {}
    names = []
    for step, base, _ in arrays:
        exp[step] = (base, {})
        names.append(step)
    exp['s9_collect'] = (None, {'afterany': set(names)})
    return exp


def array_matches(actual, base, maxthr, single_ok):
    """actual like '0-23%4' / None; base '0-23%4' (exact when it carries %N) or '0-5' (throttle <= maxthr allowed)."""
    if actual is None:
        return single_ok
    rng, _, thr = actual.partition('%')
    brng, _, bthr = base.partition('%')
    if single_ok and rng in ('0', '0-0') and brng in ('0', '0-0'):
        return True
    if rng != brng:
        return False
    if bthr:
        return thr == bthr
    if maxthr is None:
        return True
    return (thr == '') or (thr.isdigit() and int(thr) <= maxthr)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--argv', required=True)
    ap.add_argument('--kind', default='main')
    ap.add_argument('--profile', default='alone')
    ap.add_argument('--pieces', default='bench')
    ap.add_argument('--tasks', default='')          # r kind: piece=k,...  (number of tasks of each resubmission list)
    ap.add_argument('--p5-n', type=int, default=0)
    ap.add_argument('--id-base', type=int, default=7000)
    ap.add_argument('--logrun', default='')
    a = ap.parse_args()

    results = []

    def rec(name, ok, detail=''):
        results.append((name, ok, detail))

    calls = read_calls(a.argv)
    infos = []
    for i, argv in enumerate(calls, 1):
        opts, pos = parse_opts(argv)
        script = pos[-1] if pos else ''
        sopts, _ = parse_opts(script_directives(script))
        eff = dict(sopts)
        eff.update(opts)
        infos.append({'n': i, 'id': a.id_base + i, 'eff': eff, 'script': script, 'argv': argv})
    id2name = {x['id']: x['eff'].get('job-name', '?') for x in infos}

    pieces = [p for p in a.pieces.split(',') if p]
    if a.kind == 'main':
        exp = expected_main(pieces, a.profile)
    elif a.kind == 'r':
        tasks = dict(kv.split('=') for kv in a.tasks.split(',') if kv)
        arrays = []
        for p in pieces:
            k = int(tasks.get(p, 1))
            s = PIECE_STEP[p]
            arrays.append((s, '0-%d' % (k - 1), THROTTLE.get(s, {}).get(a.profile)))
        exp = expected_later(arrays, a.profile)
    else:
        print('FAIL kind: unknown kind ' + a.kind)
        return
    want_names = ['lowpB_' + s for s in exp]
    got_names = [x['eff'].get('job-name', '?') for x in infos]

    rec('submission count = %d' % len(exp), len(infos) == len(exp), 'got %d' % len(infos))
    rec('job names lowpB_<step>, each once', sorted(got_names) == sorted(want_names), 'got %s want %s' % (sorted(got_names), sorted(want_names)))
    by = {}
    for x in infos:
        nm = x['eff'].get('job-name', '?')
        if nm.startswith('lowpB_'):
            by[nm[len('lowpB_'):]] = x
    id_of = {s: by[s]['id'] for s in by}
    step_of_id = {v: k for k, v in id_of.items()}
    # dependencies are expressed in step names
    id2step = {x['id']: x['eff'].get('job-name', '?').replace('lowpB_', '', 1) for x in infos}

    def per(name, fn):
        bad = []
        for s, spec in exp.items():
            x = by.get(s)
            if x is None:
                bad.append(s + ': missing')
                continue
            msg = fn(s, spec, x)
            if msg:
                bad.append('%s: %s' % (s, msg))
        rec(name, not bad, '; '.join(bad))

    def acp(s, spec, x):
        e = x['eff']
        m = [k for k, v in (('account', 'commons'), ('partition', 'commons'), ('constraint', 'sapphirerapids')) if e.get(k) != v]
        return ('wrong %s' % ','.join(m) + ' (%s)' % {k: e.get(k) for k in m}) if m else ''
    per('account=commons partition=commons constraint=sapphirerapids', acp)

    def cpus(s, spec, x):
        c = int(x['eff'].get('cpus-per-task', '1') or 1)
        return '' if c == STEP[s][0] else 'cpus %d want %d' % (c, STEP[s][0])
    per('cpus per task', cpus)

    def mem(s, spec, x):
        v = x['eff'].get('mem')
        m = mem_mb(v) if v else None
        return '' if (STEP[s][1] is None and m) or m == STEP[s][1] else 'mem %r want %s MB' % (v, STEP[s][1])
    per('memory', mem)

    def tim(s, spec, x):
        v = x['eff'].get('time')
        try:
            t = seconds(v) if v else None
        except ValueError:
            t = None
        return '' if (STEP[s][2] is None and t) or t == STEP[s][2] else 'time %r (=%s s) want %s s' % (v, t, STEP[s][2])
    per('time limit', tim)

    def arr(s, spec, x):
        want = spec[0]
        got = x['eff'].get('array')
        if want is None:
            return '' if not got else 'unexpected array %s' % got
        if a.kind == 'r':
            maxthr = THROTTLE.get(s, {}).get(a.profile)
            return '' if array_matches(got, want, maxthr, True) else 'array %r want %s (throttle <= %s)' % (got, want, maxthr)
        return '' if got == want else 'array %r want %s' % (got, want)
    per('arrays and throttles', arr)

    def dep(s, spec, x):
        got = parse_deps(x['eff'].get('dependency', ''), id2step)
        want = {k: v for k, v in spec[1].items() if v}
        return '' if got == want else 'dependency %r -> %s want %s' % (x['eff'].get('dependency'), got, want)
    per('dependencies (DESIGN section 5 table)', dep)

    def kill(s, spec, x):
        if not any(spec[1].values()):
            return ''
        return '' if x['eff'].get('kill-on-invalid-dep') == 'yes' else '--kill-on-invalid-dep=yes missing'
    per('--kill-on-invalid-dep=yes on dependents', kill)

    if a.logrun:
        def norm(p):
            """one spelling for MSYS (/tmp/..., /c/...) and Windows (C:/.../Temp/...) forms of the same path"""
            p = p.replace('\\', '/').rstrip('/')
            low = p.lower()
            tmp = 'c:/users/felip/appdata/local/temp/'
            if low.startswith(tmp):
                return '/tmp/' + p[len(tmp):]
            m = re.match(r'^([a-zA-Z]):/(.*)$', p)
            return ('/%s/%s' % (m.group(1).lower(), m.group(2))) if m else p
        lr = norm(a.logrun)

        def outp(s, spec, x):
            bad = []
            for k in ('output', 'error'):
                v = x['eff'].get(k)
                if v and not norm(v).startswith(lr):
                    bad.append('%s=%s' % (k, v))
            return ', '.join(bad)
        per('slurm outputs under LOG_RUN', outp)

    def outpat(s, spec, x):
        e = x['eff']
        if e.get('array'):
            pat, bad_pat = '%A_%a', None
        else:
            pat, bad_pat = '%j', '%a'
        bad = []
        for k in ('output', 'error'):
            v = e.get(k)
            if not v:
                bad.append('%s missing' % k)
            elif pat not in v or (bad_pat and bad_pat in v):
                bad.append('%s=%s lacks %s' % (k, v, pat))
        return ', '.join(bad)
    per('--output/--error use %j (plain jobs) and %A_%a (array jobs)', outpat)
    per('--no-requeue on every vector (F3)', lambda s, spec, x: '' if 'no-requeue' in x['eff'] else '--no-requeue missing')

    for name, ok, detail in results:
        print(('PASS ' if ok else 'FAIL ') + name + ('' if ok or not detail else ': ' + detail))


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:   # a crash must show up as a visible FAIL, not as silence
        print('FAIL vec_check crashed: %r' % (exc,))
