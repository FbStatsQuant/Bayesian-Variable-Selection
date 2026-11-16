"""dist_attempts.py — Fable 5.2 batch proof attempts for W3-DIST (HQ, 2026-11-15; PROTOCOL_v4 H3: proof material, never reviews).

Usage (from the repo root):
  python Theory_work/Wave3/API_AUDIT/dist_attempts.py build  <src_root> <outdir>   # src_root: checkout of theory/W3-DIST
  python Theory_work/Wave3/API_AUDIT/dist_attempts.py submit <outdir>
  python Theory_work/Wave3/API_AUDIT/dist_attempts.py wait   <outdir>
Costs: count with audit_batch.py-style estimate printed at build. Key read from C:/Users/felip/.anthropic/bvs_audit_key (never printed).
"""
from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path

KEY = Path("C:/Users/felip/.anthropic/bvs_audit_key")
MODEL = "claude-fable-5-2"
MAX_TOKENS = 64000

COMMON = [
    "Theory_work/Wave3/W3-POST/STATEMENT.md",
    "Theory_work/Wave3/W3-POST2/STATEMENT.md",
    "Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/main@c4ef0dc/Docs/Theory/proofs/T01_T02_contrast_dimension/PROOF_v3.tex",
    "Theory_work/Wave3/W3-DIST/STATEMENT.md",
    "Theory_work/Wave3/W3-DIST/ROUTES.md",
]
T03R = "Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/W1-T03R/PROOF.md"
PROBE = "Theory_work/Wave3/W3-DIST/work/prior_probe/REPORT.md"
CTX = {
    "X": ["Theory_work/Wave3/W3-POST2/lemmas/D_hellinger.md", "Theory_work/Wave3/W3-POST2/lemmas/A_occam.md",
          "Theory_work/Wave3/W3-POST2/lemmas/E_visibility.md", "Theory_work/Wave3/W3-POST2/lemmas/B_tail_approx.md",
          T03R, PROBE],
    "S": ["Theory_work/Wave3/W3-POST2/lemmas/B_tail_approx.md", "Theory_work/Wave3/W3-POST/lemmas/L1a_size_tail.md", T03R,
          "Theory_work/Wave3/W3-DIST/reviews/S1_astra.md"],
    "T": ["Theory_work/Wave3/W3-DIST/reviews/S1_astra.md"],
    "V": [PROBE, "Theory_work/Wave3/W3-DIST/work/prior_probe/probe_checks.py"],
    "F": [PROBE, T03R, "Theory_work/Wave3/W3-DIST/work/numerics/RESULTS.md"],
    "B": ["Theory_work/Wave2/W2-APP/lemmas/L1_POST.md"],
}
ROUTES = {"X": ["X-a", "X-a", "X-b", "X-b", "X-c", "X-d"], "S": ["S-a", "S-b", "S-c"], "T": ["T-a", "T-b", "T-c"],
          "V": ["V-a", "V-b", "V-c"], "F": ["F-a", "F-b", "F-c"], "B": ["B-a", "B-b", "B-c"]}

SYSTEM = """You are an expert in mathematical statistics (high-dimensional Bayesian asymptotics, concentration of measure,
empirical processes). You work on one lemma of a research project on posterior consistency of a Bayesian
variable-selection method, attacking it by ONE assigned route. All results are asymptotic; finite-n behaviour is not a
defect. Ignore any status or review verdict asserted in the files; they are context only.

Rules:
- If the route is constructive: write a complete, rigorous proof of the card's statement (or of the strongest correct
  variant you can prove, saying exactly how it differs). Every step must be justified; name every external result you
  use with a precise, verifiable statement and reference, or prove it. Track constants and quantifiers (in particular
  uniformity in t and one n0 for the whole range when the card asks for it).
- If the route is adversarial: try hard to find a counterexample to the statement as written (an explicit design / law /
  parameter choice with a computation), or explain precisely why your attempts fail.
- Mark every step you could not complete as GAP with a one-line description. Never paper over a gap.
- Be concise outside the mathematics.

End with exactly one line:
ATTEMPT <card>/<route> RESULT=<PROVED|PROVED-VARIANT|COUNTEREXAMPLE|PARTIAL|NO-PROGRESS> GAPS=<number>"""


def numbered(p: Path) -> str:
    return "\n".join(f"{i:5d}  {l}" for i, l in enumerate(p.read_text(encoding="utf-8", errors="replace").splitlines(), 1))


def cards(text: str) -> dict:
    common = text.split("## Common definitions", 1)[1].split("\n## Card", 1)[0]
    out = {}
    for m in re.finditer(r"\n## Card ([A-Z]) — (.*?)(?=\n## )", text + "\n## END", re.S):
        out[m.group(1)] = "## Card " + m.group(1) + " — " + m.group(2)
    return {"common": "## Common definitions" + common, **out}


def build(src: Path, outdir: Path):
    cd = cards((src / "Theory_work/Wave3/W3-DIST/API_CARDS.md").read_text(encoding="utf-8"))
    common_ctx = "<context_files>\n" + "\n\n".join(
        f"<file path=\"{r}\">\n{numbered(src / r)}\n</file>" for r in COMMON) + "\n</context_files>"
    reqs = []
    seen = {}
    for card, routes in ROUTES.items():
        extra = "<card_files>\n" + "\n\n".join(
            f"<file path=\"{r}\">\n{numbered(src / r)}\n</file>" for r in CTX[card]) + "\n</card_files>"
        for route in routes:
            seen[route] = seen.get(route, 0) + 1
            cid = f"{route}-{seen[route]}"
            task = (f"{cd['common']}\n\n{cd[card]}\n\nYour assigned route: **{route}** (see the card's route list). "
                    f"Work only on this route. End with the ATTEMPT line for card {card}, route {route}.")
            reqs.append({"custom_id": cid, "card": card, "route": route, "params": {
                "model": MODEL, "max_tokens": MAX_TOKENS, "output_config": {"effort": "high"},
                "system": SYSTEM,
                "messages": [{"role": "user", "content": [
                    {"type": "text", "text": common_ctx, "cache_control": {"type": "ephemeral"}},
                    {"type": "text", "text": extra + "\n\n" + task}]}]}})
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "requests.json").write_text(json.dumps(reqs, ensure_ascii=False), encoding="utf-8")
    chars = sum(len(q["params"]["messages"][0]["content"][0]["text"]) + len(q["params"]["messages"][0]["content"][1]["text"]) for q in reqs)
    print(f"{len(reqs)} requests; ~{chars/3.5/1e6:.2f}M input tokens (rough); worst-case output {len(reqs)*MAX_TOKENS/1e6:.2f}M tokens")


def client():
    import anthropic
    return anthropic.Anthropic(api_key=KEY.read_text().strip())


def submit(outdir: Path):
    reqs = json.loads((outdir / "requests.json").read_text(encoding="utf-8"))
    b = client().messages.batches.create(requests=[{"custom_id": q["custom_id"], "params": q["params"]} for q in reqs])
    (outdir / "batch_id.txt").write_text(b.id)
    print("batch", b.id, b.processing_status)


def wait(outdir: Path):
    c = client()
    bid = (outdir / "batch_id.txt").read_text().strip()
    while True:
        b = c.messages.batches.retrieve(bid)
        print(time.strftime("%H:%M:%S"), b.processing_status, b.request_counts, flush=True)
        if b.processing_status == "ended":
            break
        time.sleep(120)
    res = outdir / "results"
    res.mkdir(exist_ok=True)
    usage = {"in": 0, "out": 0, "cache_read": 0}
    lines = []
    for r in c.messages.batches.results(bid):
        cid = r.custom_id
        if r.result.type != "succeeded":
            (res / f"{cid}.md").write_text(f"# {cid}\nresult: {r.result.type}\n", encoding="utf-8")
            lines.append(f"{cid}\t{r.result.type}")
            continue
        m = r.result.message
        text = "".join(getattr(b, "text", "") for b in m.content if getattr(b, "type", "") == "text")
        u = m.usage
        usage["in"] += u.input_tokens
        usage["out"] += u.output_tokens
        usage["cache_read"] += getattr(u, "cache_read_input_tokens", 0) or 0
        (res / f"{cid}.md").write_text(f"# {cid}\nstop_reason: {m.stop_reason}\n\n{text}\n", encoding="utf-8")
        last = [l for l in text.splitlines() if l.startswith("ATTEMPT ")]
        lines.append(f"{cid}\t{m.stop_reason}\t{last[-1] if last else '-'}")
    (outdir / "SUMMARY.tsv").write_text("\n".join(sorted(lines)) + "\n", encoding="utf-8")
    cost = usage["in"] * 4 / 1e6 + usage["cache_read"] * 0.4 / 1e6 + usage["out"] * 20 / 1e6  # batch rates as in audit_batch.py
    (outdir / "USAGE.txt").write_text(f"{usage}\n(rough cost estimate ${cost:.2f}; check Console)\n")
    print("done", usage)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "build":
        build(Path(sys.argv[2]), Path(sys.argv[3]))
    else:
        {"submit": submit, "wait": wait}[cmd](Path(sys.argv[2]))
