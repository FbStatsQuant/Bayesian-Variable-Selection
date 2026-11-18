#!/usr/bin/env python3
"""W3-D3 API blind-audit request builder (for HQ; pattern of Theory_work/Wave3/API_AUDIT/audit_batch.py). NO API CALL.

  python3 Theory_work/Wave3/W3-D3/api_request_build.py <outdir>

Writes <outdir>/requests.json (one Message Batches request) and <outdir>/MANIFEST.txt (sha256 of every source file used).
Blind: no review files, LOG, PLAN, CHECKPOINT or REPORT; status quotations are redacted inside lines, and lines that still
carry a status word are dropped (their numbers are listed in MANIFEST so HQ can see what was cut).
HQ sets the model and effort per its API card rules (default below mirrors audit_batch.py: claude-fable-5-2, effort high).
"""
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
T = "Theory_work/Wave3/"
MODEL = "claude-fable-5-2"
MAX_TOKENS = 64000
STATUS_MARKERS = ["PROVED", "VERIFIED", "council", "MANIFEST", "sol=", "opus=", "astra=", "Status:", "PASS", "LOCK",
                  "unchecked", "[REG-"]
# redactions applied first (a status quotation or tag inside a line of mathematics); a line that still carries a marker
# afterwards is dropped whole
REDACT = [re.compile(r'\*{0,2}"[^"]*(PROVED|VERIFIED|PASS|council)[^"]*"\*{0,2}'),
          re.compile(r'\(main [0-9a-f]{8}\)'), re.compile(r'\[REG-[0-9a-f]{4}\]'), re.compile(r',? ?status\b')]

# (path, first line, last line, label) — 1-based inclusive; None = whole file; "S5" = up to the line before "## 5." of STATEMENT
EB = T + "W3-DIST/work/E_bridges/"
SOURCES = [
    (T + "W3-D3/STATEMENT.md", 14, "S5", "TICKET STATEMENT (symbols, §§0–4: setting, Theorem 2SG, Lemma B3w, Proposition ExSG, remarks)"),
    (T + "W3-D3/lemmas/B3w.md", 6, None, "TICKET PROOF: Lemma B3w"),
    (T + "W3-D3/lemmas/ASSEMBLY.md", 6, None, "TICKET PROOF: Theorem 2SG and Proposition ExSG"),
    (T + "W3-POST/STATEMENT.md", 16, 100, "CONSUMED: the coded posterior, outputs, m#_n; Theorem 1 (R1, (E), (F_lambda), (F_w), (BM), items 1-6)"),
    (EB + "B0.md", 7, 40, "CONSUMED: scale reduction B0 (statement)"),
    (EB + "B1.md", 7, 30, "CONSUMED: B1 (statement)"),
    (EB + "B2core.md", 7, 30, "CONSUMED: B2-core (statement)"),
    (EB + "B2.md", 22, 55, "CONSUMED: B2 (statement and proof of part (a))"),
    (EB + "B3.md", 7, None, "TEMPLATE: W3-DIST B3 (adapted by Lemma B3w; its amendment A-2)"),
    (T + "W3-READER/lemmas/R1_set_sizes.md", 6, 31, "CONSUMED: set-size arithmetic (B1.2, B1.3)"),
    (T + "W3-READER/READER_VERSIONS.md", 26, 30, "RECORDED THEOREM 2: standing assumptions (S1), (S2)"),
    (T + "W3-READER/READER_VERSIONS.md", 257, 290, "RECORDED THEOREM 2: reader statement"),
    (T + "W3-READER/NOTATION.md", 9, 40, "RECORDED MODEL: notation §§1-2"),
]

SYSTEM = """You are an independent referee. You receive one short theorem with a bridge lemma, a proposition, their proofs,
and excerpts of the results they consume. Consumed results may be taken as true as stated; check that their stated
hypotheses actually hold where they are used. Your task: break the proofs. Check every step: that the window of sparse
directions covers every set the proof needs; the constants after the scale reduction; that the probability bounds apply
(size conditions, thresholds in n and what they may depend on); the completion off the event where no column is removed
and the measurability of the interface events; that every hypothesis of the consumed random-design interface (item 6) and
of its regime holds; the transfer from the completed objects to the actual outputs; and the moment-generating-function
inequalities of the proposition (including the in-place proof of Hoeffding's lemma). Also check that the theorem as
stated does not use a hypothesis it does not state, and that the recorded statement is quoted faithfully. Report findings
only: no praise, no summary of what is correct, no style or presentation remarks. For each finding: severity (ERROR = a
claim as stated is false or a step is false with no easy repair; GAP = a step is unjustified but plausibly repairable —
describe the repair; MINOR = a local slip that does not affect a claim), exact location (file:line), the problem, and for
ERROR/GAP a counterexample or the missing argument.
End with exactly three lines, nothing after them:
AUDIT W3-D3:Thm2SG FINDINGS=<count of GAP+ERROR>
AUDIT W3-D3:B3w FINDINGS=<count of GAP+ERROR>
AUDIT W3-D3:ExSG FINDINGS=<count of GAP+ERROR>"""


def excerpt(rel, a, b):
    lines = (ROOT / rel).read_text(encoding="utf-8").splitlines()
    a = a or 1
    if b == "S5":
        b = next(i for i, l in enumerate(lines, 1) if l.startswith("## 5.")) - 1
    b = b or len(lines)
    kept, dropped = [], []
    for i in range(a, b + 1):
        l = lines[i - 1]
        if any(m in l for m in STATUS_MARKERS):
            for rx in REDACT:
                l = rx.sub("", l)
        if any(m in l for m in STATUS_MARKERS):
            dropped.append(i)
            continue
        kept.append(f"{i:4d}| {l}")
    return "\n".join(kept), dropped, hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    parts, man = [], []
    for rel, a, b, label in SOURCES:
        txt, dropped, sha = excerpt(rel, a, b)
        parts.append(f"===== {label}\n===== file: {rel} (lines {a or 1}-{b or 'end'})\n{txt}")
        man.append(f"{sha}  {rel}  lines {a or 1}-{b or 'end'}  dropped(status words): {dropped}")
    user = ("Claims to audit: W3-D3:Thm2SG (STATEMENT §1), W3-D3:B3w (STATEMENT §2) and W3-D3:ExSG (STATEMENT §3), "
            "in the setting of STATEMENT §0. Break the proofs; findings only.\n\n"
            + "\n\n".join(parts))
    req = {"custom_id": "W3-D3-blind-audit",
           "params": {"model": MODEL, "max_tokens": MAX_TOKENS, "system": SYSTEM,
                      "messages": [{"role": "user", "content": user}]}}
    (out / "requests.json").write_text(json.dumps([req], ensure_ascii=False, indent=1), encoding="utf-8")
    (out / "MANIFEST.txt").write_text("\n".join(man) + "\n", encoding="utf-8")
    print(f"wrote {out/'requests.json'} ({len(user)} chars of user content) and MANIFEST.txt")


if __name__ == "__main__":
    main()
