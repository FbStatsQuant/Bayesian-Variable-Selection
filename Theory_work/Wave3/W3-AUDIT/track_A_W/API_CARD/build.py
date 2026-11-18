"""Build the AUDITW card: a blind Claude Fable 5.2 referee of track A_W items W1 (ISL) and W2 (FRZ).

Same pattern as Theory_work/Wave3/API_AUDIT/audit1 (SYSTEM.md, REQ_*.md, requests.json in audit_batch.py shape,
REQUESTS.tsv, MANIFEST.tsv, USAGE.txt). No API call; no key is read. Every excerpt is taken verbatim, with line
numbers, from git blobs at fixed commits (git show), so a rebuild is byte-identical while the pins hold.

  python3 -I Theory_work/Wave3/W3-AUDIT/track_A_W/API_CARD/build.py build <items_commit>
"""
import hashlib, json, re, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
CODE_PIN = "4676af6"
CODE = "Scripts/SMC_BVS/core/"
FORBIDDEN = re.compile(r"\b(PROVED|CHECKED|council|PASS|VERIFIED|AUDITCALC|Opus|Fable|Astra|Sol|seats?|Codex|LOCK(ED)?)\b|gpt-", re.I)

# (label, path, commit-key, line ranges); commit-key "items" = the W1/W2 commit, "pin" = the code pin, "main" = sources
def sources(items):
    W = "Theory_work/Wave3/W3-AUDIT/track_A_W/"
    return [
        ("W1 statement", W + "W1_ISL/STATEMENT.md", items, [(1, None)]),
        ("W1 proof", W + "W1_ISL/PROOF.md", items, [(1, None)]),
        ("W2 statement", W + "W2_FRZ/STATEMENT.md", items, [(1, None)]),
        ("W2 proof", W + "W2_FRZ/PROOF.md", items, [(1, None)]),
        ("Lemma B (older core; the steps under test)", "Theory_work/Wave1/W1-N1/lemmas/L1_bridge.md", items, [(4, None)]),
        ("Lemma F (older core; the step under test)", "Theory_work/Wave1/W1-N1/lemmas/L3_freezing.md", items, [(4, None)]),
        ("Premises of the older ticket", "Theory_work/Wave1/W1-N1/STATEMENT.md", items, [(64, 95)]),
        ("T12 freezing lemma", "Docs/Theory/proofs/T12_T8_frozen_run_identities/PROOF_v6.tex", items, [(155, 166)]),
        ("Consumer: Theorem D, section 1", "Theory_work/Wave3/W3-SAMP/lemmas/D_theorem.md", items, [(6, 31)]),
        ("Consumer: Lemma MR", "Theory_work/Wave3/W3-SAMP/lemmas/MR_identities.md", items, [(25, 80)]),
        ("Code: engine (variate source, steps, round, resampling, island)", CODE + "cpp/v3_engine.h", CODE_PIN, [(16, 25), (86, 372)]),
        ("Code: exact pi_0 sampler", CODE + "cpp/v3_start.h", CODE_PIN, [(150, 177)]),
        ("Code: score cache", CODE + "cpp/v3_score.h", CODE_PIN, [(262, 295)]),
        ("Code: final run (islands, streams)", CODE + "cpp/v3_core.cpp", CODE_PIN, [(388, 452)]),
        ("Code: calibration streams", CODE + "cpp/v3_core.cpp", CODE_PIN, [(588, 600)]),
        ("Code: uniform generator", CODE + "cpp/v3_util.h", CODE_PIN, [(40, 62)]),
        ("Code: frozen object, final-run settings, final run", CODE + "v3_run.R", CODE_PIN, [(66, 100), (220, 229)]),
        ("Code: calibration return", CODE + "v3_calib.R", CODE_PIN, [(140, 190)]),
        ("Code: budgets", CODE + "v3_preprocess.R", CODE_PIN, [(18, 32)]),
    ]

ITEMS = [
    ("W:ISL-0", "W1 (ISL-0): the island record is a function of (c, data, uniforms read); no other influence"),
    ("W:ISL-st", "W1 (ISL-st): stopping times, the read bounds, fresh uniforms, the draw count D_r(c)"),
    ("W:ISL-d", "W1 (ISL-d): joint measurability and Polish values, incl. the coordinates the consumers use"),
    ("W:FRZ-a", "W2 (FRZ-a): the freezing lemma (monotone class)"),
    ("W:FRZ-b", "W2 (FRZ-b): SI, A0 and E0 = {C in A0}, O_r = Phi(C, U_r) at the code"),
    ("W:FRZ-c", "W2 (FRZ-c): conditioning at general c; the consumers' integrands; the actual-pair reading"),
    ("W:FRZ-d", "W2 (FRZ-d): the evidence bounds"),
    ("W:USE-D", "the use Theorem D section 1 makes of Lemma B's control flow, (B-0), (B-d) and of the freezing step is supported by W1, W2"),
    ("W:USE-MR", "the use Lemma MR Steps 2-4 make of Lemma B (B-d) and of Lemma F's freezing step is supported by W1, W2"),
]

SYSTEM = """You are a blind, independent referee. A research project on a sequential Monte Carlo (SMC) method for Bayesian
variable selection proves theorems about the method's coded implementation. Two short lemmas (W1, W2) re-check, against
the code of record, steps of an older code-bridge lemma (Lemma B) and of a freezing lemma (Lemma F) that two consumer
results (Theorem D, Lemma MR) rely on. You receive, verbatim with file and line numbers: the two lemmas with their proofs,
the older steps, the consumers' passages, and the code excerpts. Status labels and review records are withheld.

Judge only the texts given. The premises are idealisations and are not under test: EX-A (exact real arithmetic and exact
scores), H-U (each stream is an i.i.d. U[0,1) sequence; streams are independent), the "potential run" (no time-guard stop).
Everything else is under test.

Your job is to break each item listed in the task. For each, either REFUTE it or say NO FINDING:
- REFUTED needs a concrete reason with exact references (file:line): a code path the proof misses (a uniform read, a
  value that feeds a transition, a stream read elsewhere, a branch whose read count is not decided by the past), a false
  bound, a measurability gap, a hypothesis used but not stated, a step of the freezing argument that fails, or a consumer
  use that the lemma as stated does not support.
- UNCLEAR only when the texts given cannot settle the item; then name the passage or fact you would need.
Do not report style, wording, presentation or possible improvements.

Output, in this order:
1. Findings only: for each REFUTED or UNCLEAR item, a short section headed by its id with the problem, the references and
   the counterexample or the missing passage. Write nothing for a NO FINDING item.
2. Then exactly one line per item listed in the task, in the listed order, and nothing after the last one:
AUDITW <item> VERDICT=<NO-FINDING|REFUTED|UNCLEAR>"""


def git_show(commit, path):
    return subprocess.run(["git", "-C", str(ROOT), "show", f"{commit}:{path}"], check=True,
                          capture_output=True).stdout.decode("utf-8")


def scrub(line):
    # status words inside the lemma files (headers, changelog) are replaced, never silently kept
    return FORBIDDEN.sub("[status omitted]", line)


def build(items_commit):
    parts, manifest = [], ["source\tpath\tcommit\tsha256"]
    parts.append("# AUDITW — W1 (island control flow, MEAS) and W2 (freezing at general c), code of record " + CODE_PIN + "\n")
    parts.append("Material for a blind review. Every excerpt is verbatim with its file and line numbers (the code at commit "
                 + CODE_PIN + ", the texts at commit " + items_commit + "). Status labels have been replaced by "
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
    (HERE / "REQ_W.md").write_text(context + "\n" + task, encoding="utf-8")
    (HERE / "MANIFEST.tsv").write_text("\n".join(manifest) + "\n", encoding="utf-8")
    reqs, rows = [], ["custom_id\titems\tn_items\titem_ids"]
    for s in (1, 2):
        cid = f"auditW-s{s}"
        reqs.append({"custom_id": cid, "file": "Theory_work/Wave3/W3-AUDIT/track_A_W/API_CARD/REQ_W.md",
                     "claims": [i for i, _ in ITEMS],
                     "params": {"model": "claude-fable-5-2", "max_tokens": 128000, "output_config": {"effort": "high"},
                                "system": SYSTEM,
                                "messages": [{"role": "user", "content": [
                                    {"type": "text", "text": context, "cache_control": {"type": "ephemeral"}},
                                    {"type": "text", "text": task}]}]}})
        rows.append(f"{cid}\tW1, W2\t{len(ITEMS)}\t" + ";".join(i for i, _ in ITEMS))
    (HERE / "requests.json").write_text(json.dumps(reqs, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    (HERE / "REQUESTS.tsv").write_text("\n".join(rows) + "\n", encoding="utf-8")
    ch = len(context) + len(task) + len(SYSTEM)
    tin = ch / 3.5
    (HERE / "USAGE.txt").write_text(
        "AUDITW token and cost estimate (OFFLINE ESTIMATE: tokens ≈ characters / 3.5; not a count).\n"
        f"chars/request {ch}; est. input tokens/request {tin:.0f}; 2 requests (samples).\n"
        "Batch rates for Claude Fable 5.2: input $4.00 / MTok, output $20.00 / MTok.\n"
        f"Input ≈ ${2 * tin * 4e-6:.2f}; output expected ≈ 20k tokens/request ≈ $0.80; worst case (max_tokens 128000) "
        f"${2 * 128000 * 20e-6:.2f}.\n", encoding="utf-8")
    print(f"built: {len(ITEMS)} items, {ch} chars/request (~{tin:.0f} tokens)")


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] != "build":
        sys.exit(__doc__)
    build(sys.argv[2])
