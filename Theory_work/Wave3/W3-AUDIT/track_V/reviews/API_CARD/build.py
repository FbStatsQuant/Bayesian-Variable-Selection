"""Build the AUDITV card: a blind Claude Fable 5.2 referee of track V item V1 (Lemma VIS, visibility uniform in n).

Same pattern as Theory_work/Wave3/API_AUDIT/audit1 (SYSTEM.md, REQ_*.md, requests.json in audit_batch.py shape,
REQUESTS.tsv, MANIFEST.tsv, USAGE.txt). No API call; no key is read. Every excerpt is taken verbatim, with line
numbers, from git blobs at fixed commits (git show), so a rebuild is byte-identical while the pins hold.

  python3 -I Theory_work/Wave3/W3-AUDIT/track_V/reviews/API_CARD/build.py build <items_commit>
"""
import hashlib, json, re, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[5]
MAIN = "029bb748"
FORBIDDEN = re.compile(r"\b(PROVED|CHECKED|council|PASS|VERIFIED|AUDITCALC|Opus|Fable|Astra|Sol|seats?|Codex|LOCK(ED)?)\b|gpt-", re.I)

# (label, path, commit, line ranges): "items" = the V1 commit, MAIN = the theorems' commit
def sources(items):
    V = "Theory_work/Wave3/W3-AUDIT/track_V/"
    return [
        ("V1 statement", V + "V1_VIS/STATEMENT.md", items, [(1, None)]),
        ("V1 proof", V + "V1_VIS/PROOF.md", items, [(1, None)]),
        ("Theorem 5 (reader version)", "Theory_work/Wave3/W3-READER/READER_VERSIONS.md", MAIN, [(568, 600)]),
        ("Theorem 6 (reader version)", "Theory_work/Wave3/W3-READER/READER_VERSIONS.md", MAIN, [(660, 700)]),
        ("Theorem 10 (reader version)", "Theory_work/Wave3/W3-READER/READER_VERSIONS.md", MAIN, [(1282, 1295)]),
        ("Notation: partial covariance", "Theory_work/Wave3/W3-READER/NOTATION.md", MAIN, [(155, 175)]),
        ("Design dossier B8 (visibility)", "Theory_work/Wave3/W3-AUDIT/TRACK_B.md", items, [(209, 233)]),
        ("Track C table (internal proxy computations)", "Theory_work/Wave3/W3-AUDIT/track_C/RESULTS.md", items, [(22, 51)]),
        ("Track C design definitions", "Theory_work/Wave3/W3-AUDIT/work/C_PLAN.md", items, [(8, 22)]),
    ]

ITEMS = [
    ("V:VIS-0", "(VIS-0): the reduction to <gamma(U, j), theta> and the lower bound Var(W_j | W_U) >= c16"),
    ("V:VIS-a", "(VIS-a): the sign route (Stieltjes after sign flips, aligned truths) and its constant theta_lo*c16"),
    ("V:VIS-b", "(VIS-b): the generic route: B closed, |vis| >= c16*dist(theta, B), the uniform constant a = c*delta"),
    ("V:VIS-c", "(VIS-c): B null and nowhere dense when the set of local directions has countable closure"),
    ("V:VIS-d", "(VIS-d): finitely many local patterns and stationary designs give countable closure"),
    ("V:VIS-e", "(VIS-e): the instances (IND, AR of either sign, equicorrelation, one factor, blocks) with their floors"),
    ("V:UNIF", "the lemma gives a margin uniform in n (B does not depend on n), not merely nonzero for almost every theta at each n"),
    ("V:SCOPE", "the design statements (which designs are inside by which route; D14/D15 on B; D18 not covered) agree with the lemma and the dossier"),
]

SYSTEM = """You are a blind, independent referee. A research project on a sequential Monte Carlo method for Bayesian variable
selection (Gaussian linear regression, p >> n allowed) uses a population "visibility" hypothesis: for every true predictor
j and every set U of at most 15 other columns, |Cov(W_j, W^T theta* | W_U)| >= a with a fixed a > 0, uniformly in n. A
short lemma (V1) gives sufficient conditions with an explicit uniform constant. You receive, verbatim with file and line
numbers: the lemma and its proof, the theorems' hypotheses it serves, the notation, the design dossier and the internal
design computations. Status labels and review records are withheld.

Judge only the texts given. All results are about population correlation matrices along a sequence n -> infinity; the
requirement is a margin that does not depend on n (a statement "nonzero for almost every theta at each n" is not enough).

Your job is to break each item listed in the task. For each, either REFUTE it or say NO FINDING:
- REFUTED needs a concrete reason with exact references (file:line): a counterexample (small explicit matrices are best),
  a false inequality, a missing case, a hypothesis used but not stated, or a design statement that contradicts the lemma
  or the dossier.
- UNCLEAR only when the texts given cannot settle the item; then name the passage or fact you would need.
Do not report style, wording, presentation or possible improvements.

Output, in this order:
1. Findings only: for each REFUTED or UNCLEAR item, a short section headed by its id with the problem, the references and
   the counterexample or the missing passage. Write nothing for a NO FINDING item.
2. Then exactly one line per item listed in the task, in the listed order, and nothing after the last one:
AUDITV <item> VERDICT=<NO-FINDING|REFUTED|UNCLEAR>"""


def git_show(commit, path):
    return subprocess.run(["git", "-C", str(ROOT), "show", f"{commit}:{path}"], check=True,
                          capture_output=True).stdout.decode("utf-8")


def scrub(line):
    # status words inside the lemma files (headers, changelog) are replaced, never silently kept
    return FORBIDDEN.sub("[status omitted]", line)


def build(items_commit):
    parts, manifest = [], ["source\tpath\tcommit\tsha256"]
    parts.append("# AUDITV — V1 (visibility with a margin uniform in n)\n")
    parts.append("Material for a blind review. Every excerpt is verbatim with its file and line numbers (the theorems and notation at "
                 "commit " + MAIN + ", the other texts at commit " + items_commit + "). Status labels have been replaced by "
                 "[status omitted].\n")
    for k, (label, path, commit, ranges) in enumerate(sources(items_commit), 1):
        text = git_show(commit, path)
        manifest.append(f"S{k}\t{path}\t{commit}\t{hashlib.sha256(text.encode('utf-8')).hexdigest()}")
        lines = text.splitlines()
        for a, b in ranges:
            if b is None:  # whole file, but without a trailing changelog (it names review records)
                cut = [i for i, l in enumerate(lines) if l.startswith("## Changelog")]
                b = cut[0] if cut else len(lines)
            b = min(b, len(lines))
            parts.append(f"## {k}. {label}\n`{path}` @ {commit}, lines {a}–{b}:\n```")
            parts.extend(f"{i:5d}| {scrub(lines[i - 1])}" for i in range(a, b + 1))
            parts.append("```\n")
    context = "\n".join(parts)
    bad = [m.group(0) for m in FORBIDDEN.finditer(context.replace("[status omitted]", ""))]
    if bad:
        sys.exit(f"status words survived: {sorted(set(bad))}")
    task = ("## Task (sent as a separate block)\n\nBreak the lemmas; findings only.\n\nItems to judge (" + str(len(ITEMS))
            + "), in this order; return one machine line for each:\n"
            + "\n".join(f"{i} — {d}" for i, d in ITEMS) + "\n")
    (HERE / "SYSTEM.md").write_text(SYSTEM + "\n", encoding="utf-8")
    (HERE / "REQ_V.md").write_text(context + "\n" + task, encoding="utf-8")
    (HERE / "MANIFEST.tsv").write_text("\n".join(manifest) + "\n", encoding="utf-8")
    reqs, rows = [], ["custom_id\titems\tn_items\titem_ids"]
    for s in (1, 2):
        cid = f"auditV-s{s}"
        reqs.append({"custom_id": cid, "file": "Theory_work/Wave3/W3-AUDIT/track_V/reviews/API_CARD/REQ_V.md",
                     "claims": [i for i, _ in ITEMS],
                     "params": {"model": "claude-fable-5-2", "max_tokens": 128000, "output_config": {"effort": "high"},
                                "system": SYSTEM,
                                "messages": [{"role": "user", "content": [
                                    {"type": "text", "text": context, "cache_control": {"type": "ephemeral"}},
                                    {"type": "text", "text": task}]}]}})
        rows.append(f"{cid}\tV1\t{len(ITEMS)}\t" + ";".join(i for i, _ in ITEMS))
    (HERE / "requests.json").write_text(json.dumps(reqs, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    (HERE / "REQUESTS.tsv").write_text("\n".join(rows) + "\n", encoding="utf-8")
    ch = len(context) + len(task) + len(SYSTEM)
    tin = ch / 3.5
    (HERE / "USAGE.txt").write_text(
        "AUDITV token and cost estimate (OFFLINE ESTIMATE: tokens ≈ characters / 3.5; not a count).\n"
        f"chars/request {ch}; est. input tokens/request {tin:.0f}; 2 requests (samples).\n"
        "Batch rates for Claude Fable 5.2: input $4.00 / MTok, output $20.00 / MTok.\n"
        f"Input ≈ ${2 * tin * 4e-6:.2f}; output expected ≈ 20k tokens/request ≈ $0.80; worst case (max_tokens 128000) "
        f"${2 * 128000 * 20e-6:.2f}.\n", encoding="utf-8")
    print(f"built: {len(ITEMS)} items, {ch} chars/request (~{tin:.0f} tokens)")


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] != "build":
        sys.exit(__doc__)
    build(sys.argv[2])
