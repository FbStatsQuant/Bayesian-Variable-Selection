#!/usr/bin/env python3
"""W3-D2 API blind-audit request builder (for HQ; pattern of Theory_work/Wave3/API_AUDIT/audit_batch.py). NO API CALL.

  python3 Theory_work/Wave3/W3-D2/api_request_build.py <outdir>

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

# (path, first line, last line, label) — 1-based inclusive; None = whole file
SOURCES = [
    (T + "W3-D2/STATEMENT.md", 14, 75, "TICKET STATEMENT (§§0–4: setting, Theorem 2X, Corollary 2X, deterministic facts, remarks)"),
    (T + "W3-D2/PROOF.md", None, None, "TICKET PROOF"),
    (T + "W3-MISR-R/STATEMENT.md", 25, 108, "CONSUMED: master statement (notation, Corollary G-min, Corollary G(b)+ = 'CorGb-plus')"),
    (T + "W3-MISR-R/lemmas/G2_corr.md", 9, None, "CONSUMED: proof of the master (for constants and the non-empty-T usage)"),
    (T + "W3-MISR/STATEMENT.md", 17, 123, "CONSUMED: definitions of the candidate posterior, classes, constants; MIS-R (i)"),
    (T + "W3-POST/STATEMENT.md", 16, 39, "CONSUMED: the coded posterior, outputs, size cutoff m#_n"),
    (T + "W3-READER/lemmas/R1_set_sizes.md", 6, 46, "CONSUMED: set-size arithmetic (B1.3, B4.1)"),
    (T + "W3-READER/READER_VERSIONS.md", 26, 30, "RECORDED THEOREM 2: standing assumptions (S1), (S2)"),
    (T + "W3-READER/READER_VERSIONS.md", 262, 281, "RECORDED THEOREM 2: reader statement"),
    (T + "W3-READER/NOTATION.md", 9, 28, "RECORDED MODEL: notation §1"),
]

SYSTEM = """You are an independent referee. You receive one short theorem with its proof, and excerpts of the results it
consumes. Consumed results may be taken as true as stated; check that their stated hypotheses actually hold where they are
used. Your task: break the proof. Check every step: the instance of the consumed master (including degenerate cases such
as an empty set of omitted columns), the identity of the objects compared, quantifiers and the dependence of constants,
thresholds in n, probability bookkeeping, the deterministic inequalities, and the corollary's reduction from the recorded
hypotheses. Also check that the theorem as stated does not use a hypothesis it does not state, and that the recorded
statement is quoted faithfully. Report findings only: no praise, no summary of what is correct, no style or presentation
remarks. For each finding: severity (ERROR = a claim as stated is false or a step is false with no easy repair; GAP = a
step is unjustified but plausibly repairable — describe the repair; MINOR = a local slip that does not affect a claim),
exact location (file:line), the problem, and for ERROR/GAP a counterexample or the missing argument.
End with exactly two lines, nothing after them:
AUDIT W3-D2:Thm2X FINDINGS=<count of GAP+ERROR>
AUDIT W3-D2:Cor2X FINDINGS=<count of GAP+ERROR>"""


def excerpt(rel, a, b):
    lines = (ROOT / rel).read_text(encoding="utf-8").splitlines()
    a = a or 1
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
    user = ("Claims to audit: W3-D2:Thm2X (STATEMENT §1, the reader statement and clause (E)) and W3-D2:Cor2X "
            "(STATEMENT §2), with the deterministic facts of STATEMENT §3. Break the proof; findings only.\n\n"
            + "\n\n".join(parts))
    req = {"custom_id": "W3-D2-blind-audit",
           "params": {"model": MODEL, "max_tokens": MAX_TOKENS, "system": SYSTEM,
                      "messages": [{"role": "user", "content": user}]}}
    (out / "requests.json").write_text(json.dumps([req], ensure_ascii=False, indent=1), encoding="utf-8")
    (out / "MANIFEST.txt").write_text("\n".join(man) + "\n", encoding="utf-8")
    print(f"wrote {out/'requests.json'} ({len(user)} chars of user content) and MANIFEST.txt")


if __name__ == "__main__":
    main()
