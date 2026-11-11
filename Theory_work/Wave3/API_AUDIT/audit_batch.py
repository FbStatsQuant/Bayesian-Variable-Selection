"""Blind API audit of PROVED-CHECKED registry claims (HQ, 2026-11-11; owner go).

One Message Batches request per claim file: the claims in that file are audited with the ticket's statement/proof
files as context (reviews/, numerics/, LOG, PLAN, CHECKPOINT excluded so the read is blind). Model: Claude Fable 5.2,
effort high (never above). The API key is read from C:/Users/felip/.anthropic/bvs_audit_key and is never printed.

  python Theory_work/Wave3/API_AUDIT/audit_batch.py build  <outdir>     # write requests.json + MANIFEST (no API call)
  python Theory_work/Wave3/API_AUDIT/audit_batch.py build2 <outdir>     # pass 2: author-only PROVED claims (priority tickets)
  python Theory_work/Wave3/API_AUDIT/audit_batch.py count  <outdir>     # token count (free endpoint), cost estimate
  python Theory_work/Wave3/API_AUDIT/audit_batch.py submit <outdir>     # create the batch, write batch_id.txt
  python Theory_work/Wave3/API_AUDIT/audit_batch.py wait   <outdir>     # poll until ended, then write results/
"""
import csv, hashlib, json, os, sys, time, collections
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
REG = ROOT / "Theory_work/INFRA/registry/claims.tsv"
KEY = Path("C:/Users/felip/.anthropic/bvs_audit_key")
MODEL = "claude-fable-5-2"
MAX_TOKENS = 64000
EXCLUDE_TOP = {"LOG.md", "PLAN.md"}

SYSTEM = """You are an independent referee auditing mathematical results in a research project on the asymptotic theory of a
sequential Monte Carlo method for Bayesian variable selection (linear regression, p ≤ n^A, often p ≫ n). Every result is
asymptotic; finite-n behaviour is not a defect.

You receive the working files of one ticket (statements, lemmas, proofs, reports) and a list of registered claims, each
located by file and line span. Earlier reviews are deliberately withheld. Ignore any status, score or review verdict the
files themselves assert ("PROVED-CHECKED", "council 8.8", etc.): judge only the mathematics on the page.

For each listed claim decide whether the statement is proved, as stated, by the material provided:
- check every step of the proof that the files give or cite, including constants, the order of quantifiers, uniformity
  (in p, n, models, events), probability-event bookkeeping, and that each cited lemma is applied within its hypotheses;
- results consumed from outside this ticket (listed in the appendix, or cited by id) may be taken as true as stated, but
  check that their stated hypotheses actually hold where they are used;
- a counterexample, a false inequality, a missing case or a hypothesis that is used but not stated are what matter. Do
  not report style, notation or presentation issues.

Severity: ERROR = the claim as stated is false, or a step is false and no easy repair exists; GAP = a step is unjustified
or missing but the claim is plausibly true with a repair you can describe; MINOR = a local slip that does not affect the
claim; OK = no problem found after checking.

Output, in this order:
1. For each claim, a short section: the claim id, what you checked, and each finding with severity, exact location
   (file:line), the problem, and (for GAP/ERROR) a concrete counterexample or the missing argument.
2. Then exactly one line per claim, nothing after the last one:
AUDIT <claim id> VERDICT=<OK|MINOR|GAP|ERROR|UNCHECKABLE> FINDINGS=<count of GAP+ERROR>
Use UNCHECKABLE only when the proof is not in the material provided (say where you looked)."""


def load_claims():
    rows = list(csv.DictReader(open(REG, encoding="utf-8"), delimiter="\t"))
    return rows, {r["id"]: r for r in rows}


def numbered(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    return "\n".join(f"{i+1:4d}| {l}" for i, l in enumerate(lines))


def excerpt(rel, span):
    p = ROOT / rel
    if not p.exists() or not span:
        return None
    lines = p.read_text(encoding="utf-8").splitlines()
    try:
        a, b = (int(x) for x in span.split("-"))
    except ValueError:
        return None
    return "\n".join(lines[max(a - 1, 0):b])


def ticket_files(ticket_dir: Path, claim_files):
    files = []
    for p in sorted(ticket_dir.glob("*.md")):
        if p.name in EXCLUDE_TOP or p.name.startswith("CHECKPOINT"):
            continue
        files.append(p)
    lem = ticket_dir / "lemmas"
    if lem.is_dir():
        files += sorted(lem.glob("*.md"))
    for cf in claim_files:  # claim files always included even if excluded above
        p = ROOT / cf
        if p not in files:
            files.append(p)
    return files


PASS2_TICKETS = ["W3-RM", "W3-POST2", "W3-POST", "W2-LOC2", "W1-GEN", "W1-PXN", "W1-N1", "W1-N3", "C-PACK", "W2-UNI",
                 "C-ENG", "W2-APP"]


def select(rows, mode):
    if mode == "pass2":  # author-only PROVED claims of the tickets feeding running work and the headline (HQ priority)
        return [r for r in rows if r["status"].startswith("PROVED") and "PROVED-CHECKED" not in r["status"]
                and r["ticket"] in PASS2_TICKETS and r["file"].endswith(".md")]
    return [r for r in rows if "PROVED-CHECKED" in r["status"]]


def build(outdir: Path, mode="pass1"):
    rows, byid = load_claims()
    pc = select(rows, mode)
    byfile = collections.defaultdict(list)
    for r in pc:
        byfile[r["file"]].append(r)
    requests, manifest = [], []
    for n, (cf, claims) in enumerate(sorted(byfile.items())):
        tdir = (ROOT / cf).parent
        if tdir.name == "lemmas":
            tdir = tdir.parent
        files = ticket_files(tdir, [cf])
        ctx = []
        for p in files:
            rel = p.relative_to(ROOT).as_posix()
            ctx.append(f"<file path=\"{rel}\">\n{numbered(p)}\n</file>")
            manifest.append((n, rel, hashlib.sha256(p.read_bytes()).hexdigest()))
        ext_ids = []
        for r in claims:
            for fld in ("depends_on", "consumes"):
                for x in r[fld].replace(";", " ").split():
                    x = x.strip(", ")
                    if x and x not in ext_ids and not x.startswith(r["ticket"] + ":"):
                        ext_ids.append(x)
        appendix = []
        for x in ext_ids:
            d = byid.get(x)
            if d:
                ex = excerpt(d["file"], d["lines"]) or "(statement text unavailable)"
                appendix.append(f"[{x}] {d['name']} — {d['file']}:{d['lines']}\n{ex}")
            else:
                appendix.append(f"[{x}] (external premise or alias; take as stated where it is invoked)")
        claim_list = "\n".join(
            f"- {r['id']} ({r['kind']}: {r['name']}) — statement at {r['file']}:{r['lines']}; premises: {r['premises'] or '—'}"
            for r in claims)
        user = [  # ticket files first and cached: requests of the same ticket share this prefix
            {"type": "text", "text": "<ticket_files>\n" + "\n\n".join(ctx) + "\n</ticket_files>",
             "cache_control": {"type": "ephemeral"}},
            {"type": "text", "text": "<consumed_results>\n" + ("\n\n".join(appendix) or "(none)")
             + "\n</consumed_results>\n\n" + f"Audit these {len(claims)} registered claim(s):\n{claim_list}"}]
        cid = f"f{n:02d}"
        requests.append({"custom_id": cid, "file": cf, "claims": [r["id"] for r in claims], "params": {
            "model": MODEL, "max_tokens": MAX_TOKENS,
            "output_config": {"effort": "high"},
            "system": SYSTEM,
            "messages": [{"role": "user", "content": user}],
        }})
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "requests.json").write_text(json.dumps(requests, ensure_ascii=False), encoding="utf-8")
    with open(outdir / "MANIFEST.tsv", "w", encoding="utf-8") as f:
        f.write("request\tfile\tsha256\n")
        for n, rel, h in manifest:
            f.write(f"f{n:02d}\t{rel}\t{h}\n")
    with open(outdir / "REQUESTS.tsv", "w", encoding="utf-8") as f:
        f.write("custom_id\tclaim_file\tclaims\n")
        for q in requests:
            f.write(f"{q['custom_id']}\t{q['file']}\t{';'.join(q['claims'])}\n")
    print(f"{len(requests)} requests, {sum(len(q['claims']) for q in requests)} claims -> {outdir}")


def client():
    import anthropic
    return anthropic.Anthropic(api_key=KEY.read_text().strip())


def count(outdir: Path):
    reqs = json.loads((outdir / "requests.json").read_text(encoding="utf-8"))
    c = client()
    tot = 0
    for q in reqs:
        p = q["params"]
        t = c.messages.count_tokens(model=p["model"], system=p["system"], messages=p["messages"]).input_tokens
        tot += t
        print(q["custom_id"], t, q["file"])
    # batch = half price: Fable 5.2 $4/MTok in, $20/MTok out
    print(f"input tokens {tot}; input cost ${tot*4/1e6:.2f}; worst-case output ${len(reqs)*MAX_TOKENS*20/1e6:.2f}")


def submit(outdir: Path):
    reqs = json.loads((outdir / "requests.json").read_text(encoding="utf-8"))
    if (outdir / "batch_id.txt").exists():
        sys.exit("batch already submitted: " + (outdir / "batch_id.txt").read_text())
    c = client()
    b = c.messages.batches.create(requests=[{"custom_id": q["custom_id"], "params": q["params"]} for q in reqs])
    (outdir / "batch_id.txt").write_text(b.id)
    print("batch", b.id, b.processing_status)


def wait(outdir: Path):
    c = client()
    bid = (outdir / "batch_id.txt").read_text().strip()
    while True:
        b = c.messages.batches.retrieve(bid)
        if b.processing_status == "ended":
            break
        print(time.strftime("%H:%M:%S"), b.processing_status, b.request_counts, flush=True)
        time.sleep(120)
    reqs = {q["custom_id"]: q for q in json.loads((outdir / "requests.json").read_text(encoding="utf-8"))}
    res = outdir / "results"
    res.mkdir(exist_ok=True)
    usage = collections.Counter()
    verdicts = []
    for r in c.messages.batches.results(bid):
        q = reqs[r.custom_id]
        if r.result.type != "succeeded":
            (res / f"{r.custom_id}.md").write_text(f"# {q['file']}\nRESULT {r.result.type}\n", encoding="utf-8")
            verdicts.append((r.custom_id, "-", f"RESULT={r.result.type}"))
            continue
        m = r.result.message
        text = "\n".join(b.text for b in m.content if b.type == "text")
        usage["in"] += m.usage.input_tokens
        usage["out"] += m.usage.output_tokens
        usage["cache_read"] += getattr(m.usage, "cache_read_input_tokens", 0) or 0
        hdr = f"# Audit {r.custom_id}: {q['file']}\nclaims: {', '.join(q['claims'])}\nstop_reason: {m.stop_reason}\n\n"
        (res / f"{r.custom_id}.md").write_text(hdr + text, encoding="utf-8")
        for line in text.splitlines():
            if line.startswith("AUDIT "):
                verdicts.append((r.custom_id, line.split()[1], line))
        if m.stop_reason != "end_turn":
            verdicts.append((r.custom_id, "-", f"STOP={m.stop_reason}"))
    with open(outdir / "VERDICTS.tsv", "w", encoding="utf-8") as f:
        f.write("request\tclaim\tline\n")
        for v in sorted(verdicts):
            f.write("\t".join(v) + "\n")
    cost = usage["in"] * 4 / 1e6 + usage["out"] * 20 / 1e6
    (outdir / "USAGE.txt").write_text(f"{dict(usage)}\napprox cost ${cost:.2f} (batch rates, cache reads billed lower)\n")
    print("done", dict(usage), f"${cost:.2f}")


if __name__ == "__main__":
    cmd, out = sys.argv[1], Path(sys.argv[2])
    if cmd == "build2":
        build(out, "pass2")
    else:
        {"build": build, "count": count, "submit": submit, "wait": wait}[cmd](out)
