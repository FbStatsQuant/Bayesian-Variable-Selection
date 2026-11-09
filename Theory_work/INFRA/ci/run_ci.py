"""run_ci.py — continuous audit of the theory program (local, read-only on tracked files).

Steps (each can be selected with --steps, default all):
  check      tools/check.py (registry vs files, SoP registry, FINAL chapter); ERRORs fail the run
  paper      tools/assemble.py --check (generated paper blocks current)
  falsify    re-run the cheap saved falsification scripts listed in ci/falsification.tsv (cheap = calibrated
             runtime < 120 s); compares regenerated output files with the committed ones; restores the tree
  cite       re-run every ticket's citecheck.py (same snapshot/restore) and compare MISS counts with the
             committed CITECHECK.txt
  reaudit    pick one random ACTIVE PROVED-CHECKED claim and write the brief for a fresh adversarial
             (Astra-high) re-audit
  optimize   EVENT-TRIGGERED only (--event wave-boundary|technique|strategy-review [--note ...]): pick one
             BINDING claim of an unsettled headline hypothesis (binding.tsv; more early sub-par signals first)
             and write an improvement-ticket brief priced in re-proof + re-review
Default steps: check,paper,falsify,cite,reaudit. falsification.tsv entries with kind=boundary simulate just
outside an assumption: if the conclusion still holds, that is reported as an "improvable" SIGNAL, not a failure.
Options: --seed N (default: today's date, so a day's picks are reproducible), --calibrate (time every
falsification entry with a 120 s cap and rewrite runtime_s/cheap in falsification.tsv), --out DIR.
Output: ci/out/<YYYY-MM-DD>/SUMMARY.md (+ check.json, briefs, logs). Exit 1 if check ERROR, a falsification
script fails, or a citecheck MISS count increases.
Nothing here schedules itself; see ci/README.md.
"""
from __future__ import annotations

import argparse
import datetime as dt
import os
import random
import re
import subprocess
import sys
import time

CI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(CI), "tools"))
import bvsreg as R  # noqa: E402

MANIFEST = os.path.join(CI, "falsification.tsv")
MAN_COLS = ["kind", "claims", "assumption", "script", "args", "timeout_s", "runtime_s", "cheap", "outputs",
            "expect", "notes"]  # kind: falsify | boundary
CAP = 120
PY = sys.executable
RECAL_ALL = "--recalibrate-all" in sys.argv
import shlex  # noqa: E402
# interpreter for the tickets' numerics (needs numpy/scipy/mpmath): config.tsv `numerics_python`, env BVS_NUMERICS_PY
PYNUM = shlex.split(os.environ.get("BVS_NUMERICS_PY") or R.config().get("numerics_python") or "") or [PY]


def git(*a, cwd=None):
    return subprocess.run(["git", "-C", cwd or R.ROOT, *a], capture_output=True, text=True,
                          encoding="utf-8", errors="replace").stdout


class Sandbox:
    """A disposable DETACHED git worktree of HEAD in a temp directory. Every script runs there, never in the
    real checkout, so nothing tracked or untracked in the user's tree can be modified or deleted. After each run
    the sandbox is reset (checkout + clean); on exit it is removed (`git worktree remove --force` + prune), also
    on errors and interrupts. CI therefore audits the COMMITTED state (HEAD), not uncommitted work."""

    def __enter__(self):
        import tempfile
        # remove sandboxes left by a run that was killed before its cleanup could run
        for ln in git("worktree", "list", "--porcelain").splitlines():
            if ln.startswith("worktree ") and "bvs-ci-" in ln:
                subprocess.run(["git", "-C", R.ROOT, "worktree", "remove", "--force", ln[9:].strip()],
                               capture_output=True)
        git("worktree", "prune")
        self.path = tempfile.mkdtemp(prefix="bvs-ci-")
        os.rmdir(self.path)  # git worktree add wants to create it
        r = subprocess.run(["git", "-C", R.ROOT, "worktree", "add", "--detach", self.path, "HEAD"],
                           capture_output=True, text=True)
        if r.returncode != 0:
            raise RuntimeError(f"cannot create CI sandbox: {r.stderr.strip()[:300]}")
        return self

    def reset(self):
        git("checkout", "--", ".", cwd=self.path)
        git("clean", "-fdqx", cwd=self.path)

    def changed(self, prefix):
        """Tracked files modified and files created under prefix since HEAD (repo-relative)."""
        out = git("status", "--porcelain", "--untracked-files=all", "--", prefix, cwd=self.path)
        return [ln[3:].strip().strip('"') for ln in out.splitlines() if ln.strip()]

    def __exit__(self, *exc):
        import shutil
        subprocess.run(["git", "-C", R.ROOT, "worktree", "remove", "--force", self.path], capture_output=True)
        subprocess.run(["git", "-C", R.ROOT, "worktree", "prune"], capture_output=True)
        shutil.rmtree(self.path, ignore_errors=True)
        return False


def kill_tree(pid):
    if os.name == "nt":
        subprocess.run(["taskkill", "/T", "/F", "/PID", str(pid)], capture_output=True)
    else:
        import signal
        try:
            os.killpg(os.getpgid(pid), signal.SIGKILL)
        except OSError:
            pass


def run_in(sb, script_rel, args, timeout, logdir):
    """Run one script inside the sandbox; stdout/stderr go to a file (no pipe a stray child could hold open);
    on timeout the whole process tree is killed. Returns (rc, secs, text, changed_files)."""
    sdir = os.path.dirname(os.path.join(sb.path, script_rel))
    logf = os.path.join(logdir, "_run.log")
    t0 = time.time()
    kw = {"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP} if os.name == "nt" else {"start_new_session": True}
    with open(logf, "w", encoding="utf-8", errors="replace") as fh:
        try:
            p = subprocess.Popen([*PYNUM, os.path.basename(script_rel), *args], cwd=sdir, stdout=fh,
                                 stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                                 env={**os.environ, "PYTHONHASHSEED": "0", "MPLBACKEND": "Agg"}, **kw)
        except OSError as e:
            return f"LAUNCH-ERROR {e}", 0.0, "", []
        try:
            rc = p.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            kill_tree(p.pid)
            try:
                p.wait(timeout=30)
            except subprocess.TimeoutExpired:
                pass
            rc = "TIMEOUT"
    secs = time.time() - t0
    with open(logf, encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    ticket_dir = "/".join(script_rel.replace("\\", "/").split("/")[:3])
    changed = sb.changed(ticket_dir)
    sb.reset()
    return rc, secs, text, changed


# ------------------------------------------------------------------ steps
def step_check(out):
    p = subprocess.run([PY, os.path.join(R.TOOLS, "check.py"), "--json", os.path.join(out, "check.json")],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    with open(os.path.join(out, "check.txt"), "w", encoding="utf-8") as fh:
        fh.write(p.stdout + p.stderr)
    last = (p.stdout.strip().splitlines() or ["?"])[-2:]
    return p.returncode == 0, "check.py: " + " | ".join(last) + " (full list: check.txt)"


def step_paper(out):
    p = subprocess.run([PY, os.path.join(R.TOOLS, "assemble.py"), "--check"], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return p.returncode == 0, p.stdout.strip() or p.stderr.strip()


def load_manifest():
    return R.read_tsv(MANIFEST)[1] if os.path.exists(MANIFEST) else []


BOUNDARY = re.compile(r"^BOUNDARY-RESULT:\s*(HOLDS|FAILS)\b", re.M)


def step_falsify(out, calibrate=False):
    man = load_manifest()
    # calibration resumes: rows already timed (runtime_s set) are skipped unless --recalibrate-all
    todo = [m for m in man if (calibrate and (RECAL_ALL or not m.get("runtime_s"))) or
            (not calibrate and m.get("cheap") == "yes")]
    if not todo:
        return True, "0 script(s) run (manifest empty or nothing cheap)"
    lines, ok = [], True
    with Sandbox() as sb:
        for m in todo:
            timeout = CAP if calibrate else int(float(m.get("timeout_s") or CAP))
            rc, secs, txt, changed = run_in(sb, m["script"], m.get("args", "").split(), timeout, out)
            exp = m.get("expect", "")
            good = rc == 0 and ((not exp) or re.search(exp, txt) is not None)
            if calibrate:
                m["runtime_s"] = f"{secs:.1f}" if rc != "TIMEOUT" else f">{CAP}"
                m["cheap"] = "yes" if rc == 0 and secs < CAP else "no"
                m["timeout_s"] = str(min(CAP, max(30, int(secs * 3) + 10))) if m["cheap"] == "yes" else str(CAP)
                last = txt.strip().splitlines()[-1][:120] if txt.strip() else ""
                m["notes"] = "" if rc == 0 else f"calibration rc={rc}: {last}"
            tag = "PASS" if good else ("TIMEOUT" if rc == "TIMEOUT" else "FAIL")
            if m.get("kind") == "boundary":
                # only a COMPLETED experiment that prints `BOUNDARY-RESULT: HOLDS|FAILS` is a scientific outcome;
                # crashes / import errors / timeouts are execution failures
                b = BOUNDARY.search(txt) if rc == 0 else None
                if b and b.group(1) == "HOLDS":
                    tag = f"SIGNAL improvable (conclusion held outside {m.get('assumption', '?')})"
                elif b:
                    tag = "boundary: conclusion failed outside the assumption (consistent with necessity)"
                else:
                    tag, good = f"FAIL (boundary experiment did not complete: rc={rc})", False
            ok &= good or calibrate
            outs = set(R.split_list(m.get("outputs", "")))
            diff = [c for c in changed if c in outs]
            note = (f"; regenerated output differs from committed: {', '.join(diff)}" if diff else "") + \
                   (f"; also wrote {len(changed) - len(diff)} other file(s)" if len(changed) > len(diff) else "")
            lines.append(f"- {tag} `{m['script']}` ({secs:.1f}s; claims {m['claims']}){note}")
            if calibrate:  # persist after every script, so an interrupted calibration loses nothing
                R.write_tsv(MANIFEST, MAN_COLS, man)
            with open(os.path.join(out, "falsify.log"), "a", encoding="utf-8") as fh:
                fh.write(f"===== {m['script']} {m.get('args', '')} rc={rc} {secs:.1f}s changed={changed}\n"
                         f"{txt[-4000:]}\n")
    if calibrate:
        R.write_tsv(MANIFEST, MAN_COLS, man)
    return ok, f"{len(lines)} script(s) run in a disposable worktree of HEAD\n" + "\n".join(lines)


def miss_count(text):
    return sum(1 for ln in text.splitlines() if re.match(r"\s*(MISS|BAD|FAIL)", ln))


def step_cite(out):
    import glob
    lines, ok = [], True
    with Sandbox() as sb:
        for cc in sorted(glob.glob(os.path.join(sb.path, "Theory_work", "Wave*", "*", "**", "citecheck.py"),
                                   recursive=True)):
            rel = os.path.relpath(cc, sb.path).replace("\\", "/")
            d = os.path.dirname(cc)
            cands = [os.path.join(d, "CITECHECK.txt"), os.path.join(d, "reviews", "CITECHECK.txt"),
                     os.path.join(os.path.dirname(d), "CITECHECK.txt")]
            committed = next((c for c in cands if os.path.exists(c)), None)
            before = open(committed, encoding="utf-8", errors="replace").read() if committed else ""
            rc, secs, txt, changed = None, 0.0, "", []
            # run, read the regenerated report BEFORE the sandbox reset, then reset
            sdir_rel = os.path.relpath(cc, sb.path)
            rc, secs, txt, changed = run_in_keep(sb, sdir_rel, CAP, out, committed)
            after = txt
            b, a = miss_count(before), miss_count(after)
            good = rc in (0, 1) and a <= b
            ok &= good
            lines.append(f"- {'PASS' if good else 'FAIL'} `{rel}`: MISS {b} committed -> {a} now (rc={rc})")
    return ok, "\n".join(lines)


def run_in_keep(sb, script_rel, timeout, logdir, report_path):
    """Like run_in, but returns the regenerated report (or stdout if the script writes none) before resetting."""
    sdir = os.path.dirname(os.path.join(sb.path, script_rel))
    logf = os.path.join(logdir, "_cite.log")
    kw = {"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP} if os.name == "nt" else {"start_new_session": True}
    t0 = time.time()
    with open(logf, "w", encoding="utf-8", errors="replace") as fh:
        p = subprocess.Popen([*PYNUM, os.path.basename(script_rel)], cwd=sdir, stdout=fh, stderr=subprocess.STDOUT,
                             stdin=subprocess.DEVNULL, **kw)
        try:
            rc = p.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            kill_tree(p.pid)
            rc = "TIMEOUT"
    secs = time.time() - t0
    if report_path and os.path.exists(report_path):
        text = open(report_path, encoding="utf-8", errors="replace").read()
    else:
        text = open(logf, encoding="utf-8", errors="replace").read()
    sb.reset()
    return rc, secs, text, []


def proof_files(r):
    t = next((t for t in R.load_tickets() if t["ticket"] == r["ticket"]), None)
    if not t:
        return []
    d = os.path.join(R.ROOT, t["folder"], "lemmas")
    return sorted(os.path.relpath(os.path.join(d, f), R.ROOT).replace("\\", "/") for f in os.listdir(d)) \
        if os.path.isdir(d) else []


def step_reaudit(out, rng):
    rows = R.load_claims()
    by = R.index(rows)
    deps = R.Graph(rows).deps
    pool = [r for r in rows if r["state"] == "ACTIVE" and r["kind"] != "external" and
            R.status_strength(r["status"]) == 3 and r["kind"] in ("theorem", "proposition", "lemma", "corollary")]
    if not pool:
        return True, "no eligible PROVED-CHECKED claim"
    r = rng.choice(sorted(pool, key=lambda x: x["id"]))
    dl = "\n".join(f"- {d}: {by[d]['name']} — status `{by[d]['status'][:160]}` [{by[d]['state']}]"
                   for d in deps.get(r["id"], [])) or "- (none recorded)"
    brief = f"""# Adversarial re-audit brief — {r['id']} ({R.today()})

Reviewer: Codex gpt-6-astra, reasoningEffort high (fresh thread, no prior context). Read-only on the repository
(git worktree of main at the current commit). Write your reply to
`Theory_work/INFRA/audits/{R.today()}_{r['id'].replace(':', '_')}_astra.md` and nothing else.

## Your job
Break this result. You are not asked whether the ticket's reviewers were careful; you are asked whether the
statement below is TRUE as stated and whether its proof is COMPLETE. Do not use the ticket's reviews or council
verdicts as evidence (you may read them only after forming your own verdict, to report disagreements).

## The claim
- {r['name']} — `{r['file']}:{r['lines']}` (registry v{r['version']}, sha256 {r['sha256'][:16]}…)
- verbatim status: `{r['status']}`; council: {r.get('council') or '—'}
- scope: {r.get('scope') or 'see statement'}; assumptions: {r.get('assumptions') or 'see statement'}
- proof files: {', '.join(proof_files(r)) or 'see ticket folder'}
- saved falsification scripts: {r.get('falsification') or 'none recorded'}

## Inputs it relies on (statuses verbatim; check that each is used within its stated scope)
{dl}

## Attacks to run (at least these)
1. Hypotheses used vs hypotheses stated, step by step; any hidden uniformity, measurability, or growth condition.
2. Every cited input: is the cited version's statement strong enough for the use made of it (scope, constants,
   law: fixed design vs joint)?
3. Boundary cases of every parameter (p near its upper range, s₀ = 0/1, ties, rank deficiency, a = 1/2 type
   degeneracies) — try to build a counterexample; run a small exact computation if it helps (p ≤ 10).
4. Quantifier order and o(1) terms that may depend on the sequence.

## Reply format
First line exactly one of: HOLDS / HOLDS-WITH-AMENDMENTS / GAP / FALSE. Then findings as FATAL / MAJOR / MINOR /
EDITORIAL with file:line, each with a concrete repair or counterexample. Last section: the exact registry action
you recommend (none / PATCH / downgrade / narrow / retract — see Theory_work/INFRA/LIFECYCLE.md).
"""
    f = os.path.join(out, f"reaudit_{r['id'].replace(':', '_')}.md")
    with open(f, "w", encoding="utf-8") as fh:
        fh.write(brief)
    return True, f"picked {r['id']} from {len(pool)} eligible; brief: {os.path.relpath(f, R.ROOT)}"


def step_optimize(out, rng, event="", note=""):
    """Event-triggered (wave boundary, newly landed technique, new strategy-review proposal) — never scheduled.
    Targets only BINDING claims: the claim whose proof forces a not-yet-settled headline hypothesis."""
    rows = R.load_claims()
    by = R.index(rows)
    g = R.Graph(rows)
    asm, sharp, binding = R.load_assumptions(), R.load_sharpness(), R.load_binding()
    pool = [b for b in binding if by.get(b["headline"], {}).get("headline") == "yes"
            and by[b["headline"]]["state"] == "ACTIVE" and not R.settled(b["headline"], b["assumption"], sharp)]
    if not pool:
        return True, "no binding claim for an unsettled headline hypothesis (seed binding.tsv / sharpness.tsv)"
    rng.shuffle(pool)
    pool.sort(key=lambda b: -len(R.split_list(b.get("signals", ""))))  # most early sub-par signals first
    b = pool[0]
    h = by[b["headline"]]
    bc = R.resolve(b.get("binding_claim", ""), set(by), R.load_aliases()) or h["id"]
    bcr = by.get(bc, {})
    paths = {d: p for d, p in g.dependents(h["id"]).items() if by[d]["state"] in R.VALID}
    direct = sorted(d for d, p in paths.items() if len(p) == 2)
    heads = sorted(d for d in paths if by[d].get("headline") == "yes")
    tickets = sorted({by[d]["ticket"] for d in paths})
    v, fails = R.necessity(h["id"], b["assumption"], sharp)
    ar = asm.get(b["assumption"], {})
    others = "\n".join(f"- {x}: {R.necessity(h['id'], x, sharp)[0]}" for x in R.hypotheses(h))
    slug = R.safe(b["assumption"].split(":", 1)[-1])
    brief = f"""# Improvement-ticket brief — weaken {b['assumption']} in {h['id']} ({R.today()})

Trigger: {event or 'manual'}{(' — ' + note) if note else ''}. Generated by the optimizer step of
Theory_work/INFRA/ci/run_ci.py. **HQ decides whether to launch**; Felipe approves if the headline statement changes.
Suggested ticket `W?-IMP-{slug}` on branch `theory/W?-IMP-{slug}`.
**Kill budget (required; HQ sets it before launch, e.g. 3 proof attempts or one wave).** On expiry record the
attempt with `propagate.py fail-route {h['id']} --assumption {b['assumption']} --route ...` (a failed removal route
is weak necessity evidence) and stop.

## Target
- headline: {h['name']} — `{h['file']}:{h['lines']}`; status `{h['status'][:160]}`
- conclusion: {h.get('conclusion') or '—'}; rate: {h.get('rate') or '—'}; scope: {h.get('scope') or '—'}
- assumption {b['assumption']} — {ar.get('name', '?')}: {ar.get('statement', '')[:200]}
  (bridge: {ar.get('bridge') or '—'}; necessity so far: {v}; failed removal routes: {fails})
- **binding claim** (where it is forced): {bc} — {bcr.get('name', '')} `{bcr.get('file', '')}:{bcr.get('lines', '')}`
- mechanism: {b.get('mechanism') or '—'}
- early sub-par signals: {b.get('signals') or 'none recorded'} {('— ' + b['notes']) if b.get('notes') else ''}

## Other hypotheses of the headline (necessity)
{others}

## Directions (lock one in STATEMENT.md; the new theorem enters the registry as CANDIDATE)
1. Weaken {b['assumption']} at the binding step (replace the crude bound). If the assumption is also used with
   necessity polarity, SPLIT it rather than weakening it globally (`registry.py assumption-impact {b['assumption']}`).
2. Or prove necessity: a counterexample just outside the assumption (closes the flag as NECESSARY).
3. First, boundary-violation numerics: simulate just outside {b['assumption']}; if the conclusion still holds,
   that supports direction 1 (add the script to ci/falsification.tsv with kind=boundary).

## Price (assurance parity: the candidate must pass the gates {h['id']} passed: {h.get('gates') or '—'})
- the candidate: statement lock + lemma checks + mid-point + sweep + council + strength gate
- if it implies {h['id']} (free supersession): {len(direct)} cheap re-point check(s), nothing else
- if not (headline-changing): {len(direct)} × (1 proof session + 1 lemma check) for the direct dependents
  ({', '.join(direct) or '—'}), {len(tickets)} sweep(s), {len(heads)} council(s) + strength gate(s) for the
  dependent headlines ({', '.join(heads) or '—'}); paper regeneration is free (assemble.py)
- exact numbers once the candidate exists: `propagate.py supersede {h['id']} --by <Y> --reason ... --dry-run`
"""
    f = os.path.join(out, f"improve_{R.safe(h['id'])}_{slug}.md")
    with open(f, "w", encoding="utf-8") as fh:
        fh.write(brief)
    return True, (f"picked {h['id']} / {b['assumption']} (binding {bc}) from {len(pool)} candidate pairs; "
                  f"brief: {os.path.relpath(f, R.ROOT)}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--steps", default="check,paper,falsify,cite,reaudit")
    ap.add_argument("--event", default="", help="optimizer trigger: wave-boundary | technique | strategy-review")
    ap.add_argument("--note", default="", help="what happened (quoted in the optimizer brief)")
    ap.add_argument("--seed", type=int)
    ap.add_argument("--calibrate", action="store_true")
    ap.add_argument("--recalibrate-all", action="store_true", help="with --calibrate: re-time rows already timed")
    ap.add_argument("--out")
    a = ap.parse_args()
    day = dt.date.today().isoformat()
    out = a.out or os.path.join(CI, "out", day)
    os.makedirs(out, exist_ok=True)
    rng = random.Random(a.seed if a.seed is not None else int(day.replace("-", "")))
    if a.calibrate:
        ok, msg = step_falsify(out, calibrate=True)
        print(msg)
        return
    results = []
    steps = {"check": step_check, "paper": step_paper, "falsify": step_falsify, "cite": step_cite,
             "reaudit": lambda o: step_reaudit(o, rng), "optimize": lambda o: step_optimize(o, rng, a.event, a.note)}
    if a.event and "optimize" not in a.steps.split(","):
        a.steps += ",optimize"
    for s in a.steps.split(","):
        t0 = time.time()
        try:
            ok, msg = steps[s](out)
        except Exception as e:  # a broken step must not hide the others
            ok, msg = False, f"step crashed: {e!r}"
        results.append((s, ok, msg, time.time() - t0))
    head = git("rev-parse", "--short", "HEAD").strip()
    lines = [f"# Theory CI — {day} (HEAD {head})", ""]
    for s, ok, msg, secs in results:
        lines += [f"## {s}: {'PASS' if ok else 'FAIL'} ({secs:.0f}s)", "", msg, ""]
    summ = os.path.join(out, "SUMMARY.md")
    with open(summ, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    print("\n".join(lines))
    sys.exit(0 if all(ok for _, ok, _, _ in results) else 1)


if __name__ == "__main__":
    main()
