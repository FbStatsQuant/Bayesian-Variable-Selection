#!/usr/bin/env python3
"""Pre-Lean BLIND API batch: request builder (pattern of Theory_work/Wave3/W3-D3/api_request_build.py and
Theory_work/Wave3/API_AUDIT/audit_batch.py). NO API CALL; HQ submits.

  python3 Theory_work/Wave3/API_AUDIT/prelean_blind/prelean_blind_build.py            # from the worktree root

Writes, next to this script:
  requests/<PB-Tk>-s<1|2>.jsonl   one Message Batches request per file ({"custom_id", "params"}); 6 targets x N=2 samples
  requests.json                   all 12 requests as one JSON list (audit_batch.py `submit` format; git-ignored, regenerable)
  BUILD_MANIFEST.txt              sha256 + last-touch commit of every source file used, line spans, dropped line numbers
  TOKENS.tsv                      per-request character count and token estimate (chars/3.5 + brief; pessimistic chars/2.5)

Blind: every request is self-contained (statement, full proof files, consumed statements). No review, council file,
disposition, CHECKPOINT, LOG, CODEX_*, FABLE_CARD, PRE_LEAN_PASS file, earlier audit result or ERRATA file is read by
this script. Status/review words are redacted inside lines; a line that still carries one is dropped (numbers listed in
BUILD_MANIFEST.txt). The model is claude-fable-5-2, effort high, as audit_batch.py (HQ to confirm).
"""
import csv
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
T = "Theory_work/Wave3/"
MODEL = "claude-fable-5-2"
MAX_TOKENS = 64000
N_SAMPLES = 2
NO_NOTES = "--no-notes" in sys.argv  # rebuild from a main that already holds the corrections: no pending-corrections note

# ---------------------------------------------------------------- redaction
HARD = ["PROVED", "VERIFIED", "CHECKED", "council", "Council", "MANIFEST", "sol=", "opus=", "astra=", "Status", "STATUS",
        "LOCKED", "unchecked", "line-checked", "line check", "[REG-", "reviews/", "review", "Review", "disposition",
        "CHECKPOINT", "LOG.md", "CODEX", "FABLE", "PRE_LEAN", "PRE-LEAN", "REPORT", "ERRATA", "TRIAGE", "API_AUDIT",
        "DEPS", "Opus", "Astra", "Sol ", "Fable", "PLAN.md", "REFUTED", "by this seat", "blind read", "pre-check",
        "precheck", "PENDING_LEAD", "HQ ", "gpt-", "AUDITED", "DRAFT", "freeze", "re-frozen",
        "FALSIFIED", "CORRECT-WITH"]
QUOTE = re.compile(r'\*{0,2}"[^"\n]*(PROVED|VERIFIED|PASS|council|CHECKED|unchecked)[^"\n]*"\*{0,2}')
PAREN = re.compile(r'\s*\((?:[^()\n]*?)(?:not line-checked|unchecked|not checked|council|PROVED|VERIFIED|status)[^()\n]*\)')
TAG = re.compile(r'\s?\[(?:[A-Z][A-Za-z0-9]{0,6})(?:[-–][A-Za-z0-9′]+)+(?:\([a-z]+\))?(?:\s*[,;]\s*[A-Z][A-Za-z0-9]{0,6}(?:[-–][A-Za-z0-9′]+)+)*\]')
TAG_EXTRA = re.compile(r'\s?\[(?:BT3|BT4|BT\d|B2|R3|R4|D71|S\d|P\d C-\d|R\d+(?:, ?[A-Z]\d+)*|T14-REP|GUARD-W|SL-card|H5-\d+)\]')
AFTER = re.compile(r'\s*\((?:lead, [0-9-]+, )?after the (?:same|cross)-family[^)]*\)')
LEAD = re.compile(r'\s*\(lead, 20[0-9-]+[^)]*\)')
VERIF = re.compile(r'\s*\(verified against arXiv.*?not accessed: `[^`]*`\)')
HQR = re.compile(r'\s*\(HQ rulings[^)]*\)')
STREAM = re.compile(r'\s*\(this stream, DRAFT\)')
TAG3 = re.compile(r'\s?\[(?:P\d [A-Z]-\d\d(?:, ?[A-Z]\d-\d\d)?|S\d-\d\d(?:, ?BT\d)+|L01|R4, S2-F2)\]')
SUBS = [QUOTE, PAREN, TAG3, AFTER, LEAD, STREAM, VERIF, HQR, re.compile(r'\(main [0-9a-f]{8}\)'), TAG, TAG_EXTRA]


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def last_commit(path):
    r = subprocess.run(["git", "log", "-1", "--format=%h", "--", path], cwd=ROOT, capture_output=True, text=True)
    return r.stdout.strip()


def read_lines(rel):
    return (ROOT / rel).read_text(encoding="utf-8").splitlines()


PASSRX = re.compile(r"\bPASS\b")

# hand patches (file-path suffix, old, new): applied to every line of the file before the generic redaction; new=None cuts
# the line. They remove only review/status wording and leave the mathematics of the line intact.
PATCHES = [
    ("W3-PSHARP/STATEMENT.md", "(W3-POST REPORT §4 item 8,", "(a target recorded in an earlier ticket)"),
    ("W3-PSHARP/STATEMENT.md", "`Theory_work/Wave3/W3-POST/REPORT.md:190`) cannot", "cannot"),
    ("W3-DIST/STATEMENT.md", "two links unchecked", "two links open"),
    ("W3-DIST/STATEMENT.md", "; ids as in DEPS.tsv", ""),
    ("W3-DIST/STATEMENT.md", "Status after Proposition NEC", "After Proposition NEC"),
    ("W3-DIST/STATEMENT.md", " in the API attempt `work/api_attempts/dist1b/F-a-r2.md`, unchecked", ""),
    ("W3-DIST/STATEMENT.md", '(selection consistency of the exact posterior; status "T03♯: PROVED; SF VERIFIED (W2-VT03R); XF', "(selection consistency of the exact posterior)."),
    ("W3-DIST/STATEMENT.md", 'VERIFIED (A-REV2)"). Corollary C', "Corollary C"),
    ("W3-DIST/STATEMENT.md", "since HQ steer A5; ", ""),
    ("W3-DIST/work/D_output/P6_DISTC.md", "; C1 Opus #7", ""),
    ("W3-DIST/work/D_output/P6_DISTC.md", " Statuses:", ""),
    ("W3-DIST/work/D_output/P6_DISTC.md", "two links are unchecked", "two links are open"),
    ("W3-DIST/work/D_output/P6_DISTC.md", "(`W3-SAMP/STATEMENT.md:66-68`).", None),
    ("W3-DIST/work/D_output/COR_C.md", "is not claimed: it was not line-checked.)", "is not claimed.)"),
    ("W3-READER/READER_VERSIONS.md", " (post-freeze rider POST2-R1)", ""),
    ("W3-READER/READER_VERSIONS.md", " This description of the output was code-checked by independent reviewers.", ""),
    ("W3-READER/READER_VERSIONS.md", ", and its description of the output was code-checked by", "."),
    ("W3-READER/READER_VERSIONS.md", "independent reviewers. Theorem 9B", "Theorem 9B"),
    ("W3-READER/READER_VERSIONS.md", " (verified against arXiv v1: Lemma 6.1, statement p. 16, proof p. 28; journal version (Ann. Statist. 42(2)) not accessed: `reviews/NH14_check.md`)", ""),
    ("W3-READER/READER_VERSIONS.md", "source `FUNI_NARROW/A_IDEALW_PLUS.md@fc30c749`; its statement is contained word for word in this ticket's earlier carrier copy", "source `FUNI_NARROW/A_IDEALW_PLUS.md@fc30c749`)"),
    ("W3-READER/READER_VERSIONS.md", "`reviews/carriers/A_IDEALW_PLUS.md`) [FRZ-RQ]. The two limits", "The two limits"),
    ("W3-DIST/work/E_bridges/B0.md", ', status "PROVED-CHECKED; council R2, MANIFEST', ":"),
    ("W3-DIST/work/E_bridges/B0.md", '217d6708…" (registry `Theory_work/INFRA/registry/claims.tsv:412`):', None),
    ("W3-DIST/work/E_bridges/B0.md", " (cited, PROVED-CHECKED)", " (cited)"),
    ("W3-DIST/work/E_bridges/ASSEMBLY.md", ', status "T03♯: PROVED; SF VERIFIED (W2-VT03R); XF', ""),
    ("W3-DIST/work/E_bridges/ASSEMBLY.md", 'VERIFIED (A-REV2)"), `W3-POST', "), `W3-POST"),
    ("W3-DIST/work/E_bridges/ASSEMBLY.md", "recorded for the reviewer.", "recorded as a remark."),
    ("W3-DIST/work/E_bridges/ASSEMBLY.md", "; status quoted in §0)", ")"),
    ("W3-D3/lemmas/B3w.md", ': each "PROVED-CHECKED; council R2, MANIFEST 9719c817… (= R2 c5cd9cdd re-frozen', ":"),
    ("W3-D3/lemmas/B3w.md", 'CITATION-ONLY as R2r), astra=9.3 PASS, opus=9.2 PASS". Statements used verbatim:', "Statements used verbatim:"),
    ("W3-D3/lemmas/ASSEMBLY.md", " (statuses verbatim; registry at main 029bb748)", ""),
    ("W3-D3/lemmas/ASSEMBLY.md", ' — "PROVED-CHECKED; council C3, MANIFEST 420c1cb0…, astra=8.8 PASS, opus=8.7', ""),
    ("W3-D3/lemmas/ASSEMBLY.md", 'PASS". Used:', "Used:"),
    ("W3-RM2-R/STATEMENT.md", "(AUDITED, code reading)", "(code-reading audits, taken as hypotheses)"),
    ("W3-RM2-R/STATEMENT.md", ", in the restated form of", ', in the form "Under the premises of Theorem D, P(𝒰_n) = 0 for every n ≥ 3"'),
    ("W3-RM2-R/STATEMENT.md", "`Theory_work/Wave3/API_AUDIT/pass1/R-AUD1_sol.md:32-35` (\"Under the premises of Theorem D, P(𝒰_n) = 0 for every", None),
    ("W3-RM2-R/STATEMENT.md", 'n ≥ 3"). The standalone', ". The standalone"),
    ("W3-RM2-R/STATEMENT.md", " (HQ disposition,", "."),
    ("W3-RM2-R/STATEMENT.md", "`API_AUDIT/pass1/TRIAGE.md:23-28`). Consistency", "Consistency"),
    ("W3-RM2-R/lemmas/Q4_core_plus.md", "absence of interruption; \"CAL is not used\" (DLV `lemmas/L4_delivery.md:75`). Status", "absence of interruption; \"CAL is not used\" (DLV `lemmas/L4_delivery.md:75`)."),
    ("W3-RM2-R/lemmas/Q4_core_plus.md", ' ("PROVED (by this seat, unchecked)" inside GEN "PROVED-CHECKED")', ""),
    ("W3-RM2-R/lemmas/Q4_core_plus.md", ' (W3-RM:E4@1.0.0, "PROVED-CHECKED")', " (W3-RM:E4@1.0.0)"),
    ("W3-RM2-R/lemmas/Q5_dlv0.md", '@1.0.0 "PROVED-CHECKED": under EX-A', "@1.0.0: under EX-A"),
    ("W3-RM2-R/lemmas/Q5_dlv0.md", 'C-DLV:L2-S3 "AUDITED (code reading)".', "C-DLV:L2-S3 (a code-reading audit, taken as hypothesis)."),
    ("W3-RM2-R/lemmas/Q5_dlv0.md", " in the restated form of `Theory_work/Wave3/API_AUDIT/pass1/R-AUD1_sol.md:32-35`", " in the form"),
    ("W3-RM2-R/lemmas/Q5_dlv0.md", " (`Theory_work/Wave3/API_AUDIT/pass1/TRIAGE.md:23-28`)", ""),
    ("W3-RM2-R/lemmas/Q5_dlv0.md", "(HQ audit A1 corrected statement, council round 3 passed; A4 preflight addition,", "(A1 corrected statement; A4 preflight addition),"),
    ("W3-RM2-R/lemmas/Q5_dlv0.md", 'OK-WITH-FIXES), as consumed by W2-UNI:F-UNI@1.1.0 ("PROVED-CHECKED"),', "as consumed by W2-UNI:F-UNI@1.1.0,"),
    ("W3-RM2-R/lemmas/Q5_dlv0.md", '("AUDITED (code reading)")', "(code-reading audits)"),
    ("W3-RM2-R/STATEMENT.md", "v3.2 freezes", "v3.2 is fixed"),
    ("W3-RM2-R/lemmas/Q5_dlv0.md", "v3.2 freezes", "v3.2 is fixed"),
    ("Wave1C/C-DLV/STATEMENT.md", " — AUDITED (code reading; R01, R02, R05, R06, council)", " — a code-reading audit (taken as hypothesis)"),
    ("W3-DIST/lemmas/X.md", "∎ (DRAFT.)", "∎"),
    ("W3-DIST/work/E_bridges/ASSEMBLY.md", "**Status of Theorem B.**", "**Theorem B, premises.**"),
    ("W3-RM2-R/lemmas/Q5_dlv0.md", "by this seat;", ";"),
    ("W3-POST/STATEMENT.md", "`Theory_work/State_of_Project/sections/04_theory.tex:771`).**", ").**"),
    ("W3-D3/STATEMENT.md", "that option is OFF (HQ),", "that option is OFF,"),
    ("W3-DIST/work/D_output/COR_C.md", "(STRONGER, for HQ)", "(STRONGER)"),
    ("W3-DIST/work/D_output/COR_C.md", "(for HQ; same mathematics)", "(same mathematics)"),
    ("W3-DIST/work/D_output/P6_DISTC.md", "(STRONGER, for HQ)", "(STRONGER)"),
    ("W3-POST/STATEMENT.md", '; card `Theory_work/State_of_Project/sections/04_theory.tex:780-788`; status "T03♯:', ")."),
    ("W3-DIST/STATEMENT.md", '([P2] A0, "PROVED (by this seat, unchecked)")', "([P2] A0)"),
    ("W3-DIST/work/E_bridges/B2.md", "so it does not depend on that status.", "so it does not depend on that comparison."),
    ("W3-READER/lemmas/R1_set_sizes.md", "; inside `SOP:TH09@1.0.2`, status", ")"),
    ("W3-READER/lemmas/R1_set_sizes.md", '"PROVED-CHECKED (T03♯ only: …)" (main 6cd699dd) [REG-6cd6]), with', "with"),
    ("W3-DIST/work/D_output/P6_DISTC.md", 'Σ_Ω e^F = Z"; status "CODE-CHECKED"). Locked', 'Σ_Ω e^F = Z"). Locked'),
    ("W3-D3/lemmas/B3w.md", "that option is OFF (HQ),", "that option is OFF,"),
    ("W3-DIST/STATEMENT.md", " The form is the lead's choice (HQ's", ""),
    ("W3-DIST/STATEMENT.md", "settled note of 2026-11-15); the text between the rules is the proposed main-text wording, with no internal ids.", "The text between the rules is the proposed main-text wording."),
    ("W3-SAMP/STATEMENT.md", "; C1 Opus #7", ""),
    ("W3-SAMP/STATEMENT.md", " (C1 Opus #5)", ""),
]
CUT = re.compile(r"$^")


POST = [(re.compile(r'; status ,\s*$'), ''), (re.compile(r'\); status \. '), '). '), (re.compile(r'with status \. '), ' '), (re.compile(r'; status \. '), '. '),
        (re.compile(r'; inherited statuses: START\s+\(N1:75\), KERNEL\s*$'), '')]


def patch(rel, line):
    for suf, old, new in PATCHES:
        if rel.endswith(suf) and old in line:
            if new is None:
                return None
            line = line.replace(old, new)
    return line


def clean(line, rel=""):
    """-> text, or None when the line still carries a status/review word after redaction"""
    out = patch(rel, line) if rel else line
    if out is None:
        return None
    for rx in SUBS:
        out = rx.sub("", out)
    for rx, rep in POST:
        out = rx.sub(rep, out)
    if any(m in out for m in HARD) or PASSRX.search(out):
        return None
    return out


def skip_header(lines, start):
    """Index (1-based) of the first line after a leading 'Status' paragraph (through the next blank line)."""
    for i in range(start, min(start + 14, len(lines)) + 1):
        if re.match(r'^\*{0,2}Status', lines[i - 1]):
            j = i
            while j <= len(lines) and lines[j - 1].strip():
                j += 1
            return j + 1
    return start


def excerpt(rel, a=None, b=None, hdr=False):
    lines = read_lines(rel)
    a = a or 1
    b = b or len(lines)
    if hdr:
        a = skip_header(lines, a)
    kept, dropped = [], []
    for i in range(a, b + 1):
        c = clean(lines[i - 1], rel)
        if c is None:
            dropped.append(i)
            continue
        kept.append(f"{i:4d}| {c}")
    return "\n".join(kept), dropped, a, b


_claims = {r["id"]: r for r in csv.DictReader(open(ROOT / "Theory_work/INFRA/registry/claims.tsv", encoding="utf-8"),
                                              delimiter="\t")}


def claim_span(cid):
    r = _claims[cid]
    a, b = (int(x) for x in r["lines"].split("-"))
    return r["file"], a, b


def F(rel, a=None, b=None, label="", hdr=False):
    return ("F", T + rel if not rel.startswith("Theory_work") else rel, a, b, label, hdr)


def C(cid, label=""):
    f, a, b = claim_span(cid)
    return ("F", f, a, b, label or f"CONSUMED STATEMENT: {cid}", False)


# ---------------------------------------------------------------- targets
EB = "W3-DIST/work/E_bridges/"
DIST = "W3-DIST/STATEMENT.md"
RV = "W3-READER/READER_VERSIONS.md"

TARGETS = {}

TARGETS["PB-T1"] = dict(
    title="Theorem 3(a): the rate lower bound on every design (W3-PSHARP:B)",
    claims=["W3-PSHARP:B"],
    sources=[
        F("W3-POST/STATEMENT.md", 16, 39, "DEFINITION: the coded target pi (the method as coded)"),
        F("W3-PSHARP/STATEMENT.md", 16, 115, "STATEMENT: notation, Lemma S, Proposition A (statement only), Corollary B (= Theorem 3(a) master)"),
        F(RV, 329, 333, "PRESENTED STATEMENT: Theorem 3(a)"),
        F("W3-PSHARP/lemmas/S_one_step.md", hdr=True, label="PROOF FILE: Lemma S and Lemma V"),
        F("W3-PSHARP/lemmas/B_sparsity.md", hdr=True, label="PROOF FILE: Corollary B"),
    ],
    pending=[])

TARGETS["PB-T3"] = dict(
    title="Hellinger reduction (W3-DIST:H), Lemma D0 (W3-POST2:D0), domination transfer and the output corollary (W3-DIST:P6, DIST-C deterministic clauses, Cor-C core)",
    claims=["W3-DIST:H", "W3-POST2:D0", "W3-DIST:P6", "W3-DIST:DIST-C", "W3-DIST:Cor-C"],
    sources=[
        F(DIST, 17, 70, "SETTING AND OBJECTS (W3-DIST section 0)"),
        F(DIST, 136, 238, "PRESENTED STATEMENTS: setup, Theorem A (= Thm 9), Theorem B (= 9B), Corollary C (= Cor 9C)"),
        F(DIST, 271, 318, "STATEMENT: code facts and Theorem DIST-C (section 2)"),
        F(DIST, 320, 326, "STATEMENT: Lemma H (Hellinger reduction)"),
        F(DIST, 381, 382, "STATEMENT: Lemma P6 (deterministic transfer)"),
        C("W3-SAMP:CC", "CONSUMED STATEMENT: W3-SAMP Lemma CC (code facts)"),
        F("W3-SAMP/lemmas/CC_code_check.md", hdr=True, label="CONSUMED PROOF FILE (short, needed for the output description): Lemma CC"),
        F("W3-DIST/API_CARDS.md", 6, 30, "COMMON DEFINITIONS used by the proof files below"),
        F("W3-DIST/work/B_transfer/H.md", hdr=True, label="PROOF FILE: Lemma H"),
        F("W3-POST2/lemmas/D_hellinger.md", 7, 19, label="PROOF FILE (the D0 part): Lemma D0"),
        F("W3-DIST/work/D_output/P6_DISTC.md", hdr=True, label="PROOF FILE: Lemma P6 and Theorem DIST-C"),
        F("W3-DIST/work/D_output/COR_C.md", hdr=True, label="PROOF FILE: Corollary C from Theorem A and DIST-C"),
    ],
    pending=[])

TARGETS["PB-T4"] = dict(
    title="Theorems 1 and 1' (W3-POST2:C, W3-POST2:E) and the presented Theorem 2 (W3-D3:Thm2SG with B3w and ExSG)",
    claims=["W3-POST2:C", "W3-POST2:E", "W3-D3:Thm2SG", "W3-D3:B3w", "W3-D3:ExSG"],
    sources=[
        F("W3-POST/STATEMENT.md", 16, 100, "CONSUMED STATEMENT: the coded posterior, outputs, m#_n; Lemma 1a, 1a'; Theorem 1 (O_P form: R1, (E), (F_lambda), (F_w), (BM), items 1-7)"),
        F(RV, 99, 156, "PRESENTED STATEMENT: Theorem 1 (reader statement)"),
        F("W3-POST2/STATEMENT.md", 11, 98, "STATEMENT: interfaces, Claims A, B, C (expectation rate, = Thm 1)"),
        F("W3-POST2/STATEMENT.md", 126, 139, "STATEMENT: Claim E (Theorem 1-VIS, = Thm 1')"),
        F("W3-POST2/lemmas/A_occam.md", hdr=True, label="PROOF FILE: Claim A (inputs (G3'), (C4'), (C5'), (C8') of C and E)"),
        F("W3-POST2/lemmas/C_expectation.md", hdr=True, label="PROOF FILE: Proposition ER (Theorem 1, expectation form)"),
        F("W3-POST2/lemmas/E_visibility.md", hdr=True, label="PROOF FILE: Theorem 1-VIS (Theorem 1')"),
        F("W3-D3/STATEMENT.md", 14, "S5", "STATEMENT: W3-D3 symbols, setting, Theorem 2SG, Lemma B3w, Proposition ExSG, remarks"),
        F("W3-D3/lemmas/B3w.md", hdr=True, label="PROOF FILE: Lemma B3w"),
        F("W3-D3/lemmas/ASSEMBLY.md", hdr=True, label="PROOF FILE: Theorem 2SG and Proposition ExSG"),
        F(EB + "B0.md", 7, 40, "CONSUMED: scale reduction B0 (statement)"),
        F(EB + "B1.md", 7, 30, "CONSUMED: B1 (statement)"),
        F(EB + "B2core.md", 7, 30, "CONSUMED: B2-core (statement)"),
        F(EB + "B2.md", 22, 55, "CONSUMED: B2 (statement and proof of part (a))"),
        F(EB + "B3.md", 7, None, "TEMPLATE: W3-DIST B3 (adapted by Lemma B3w; its amendment A-2)"),
        F("W3-READER/lemmas/R1_set_sizes.md", 6, 31, "CONSUMED: set-size arithmetic (B1.2, B1.3)"),
        F(RV, 26, 30, "STANDING ASSUMPTIONS (S1), (S2)"),
        F(RV, 257, 290, "PRESENTED STATEMENT: Theorem 2 (reader statement)"),
        F("W3-READER/NOTATION.md", 9, 40, "NOTATION sections 1-2"),
    ],
    pending=[])

TARGETS["PB-T5"] = dict(
    title="Theorems 9, 9B and Corollary 9C (W3-DIST:Thm-A, Thm-B, Cor-C)",
    claims=["W3-DIST:Thm-A", "W3-DIST:Thm-B", "W3-DIST:Cor-C"],
    sources=[
        F(DIST, 17, 415, "STATEMENT: W3-DIST sections 0-3 (setting, theorems DIST-1..3, presented statements, DIST-C, key lemmas, bridges)"),
        F(RV, 1051, 1172, "PRESENTED STATEMENT: Theorem 9, 9B, Corollary 9C (reader statement)"),
        F("W3-POST/STATEMENT.md", 16, 100, "CONSUMED STATEMENT: the coded posterior; Theorem 1 (O_P form) with item 6"),
        C("W3-MISR:R'", "CONSUMED STATEMENT: W3-MISR Lemma R' (equivariance of the parameter posterior)"),
        C("W2-APP:POST", "CONSUMED STATEMENT: W2-APP Lemma POST (diagonal transfer)"),
        C("W3-SAMP:CC", "CONSUMED STATEMENT: W3-SAMP Lemma CC (code facts)"),
        F("W3-SAMP/lemmas/CC_code_check.md", hdr=True, label="CONSUMED PROOF FILE (short, needed for the output description): Lemma CC"),
        F("W3-DIST/API_CARDS.md", 6, 30, "COMMON DEFINITIONS used by the proof files below"),
        F("W3-DIST/lemmas/DIST12.md", hdr=True, label="PROOF FILE: DIST-1, DIST-2"),
        F("W3-DIST/lemmas/X.md", 19, 222, label="PROOF FILE: Lemma X (in-sample exponential core), self-contained"),
        F("W3-DIST/work/C_size/X12.md", hdr=True, label="PROOF FILE: Lemma X' (without (ND)) and the instances for DIST-1/DIST-2"),
        F("W3-DIST/work/C_size/S.md", hdr=True, label="PROOF FILE: Lemma S (size tail)"),
        F("W3-DIST/work/C_size/V.md", hdr=True, label="PROOF FILE: Lemma V"),
        F("W3-DIST/work/B_transfer/T.md", hdr=True, label="PROOF FILE: Lemma T (sample-to-population transfer)"),
        F("W3-DIST/work/B_transfer/H.md", hdr=True, label="PROOF FILE: Lemma H (Hellinger reduction)"),
        F("W3-DIST/work/B_transfer/DIST3.md", hdr=True, label="PROOF FILE: DIST-3"),
        F(EB + "B0.md", hdr=True, label="PROOF FILE: bridge B0"),
        F(EB + "B1.md", hdr=True, label="PROOF FILE: bridge B1"),
        F(EB + "B2core.md", hdr=True, label="PROOF FILE: bridge B2-core"),
        F(EB + "B2.md", hdr=True, label="PROOF FILE: bridge B2"),
        F(EB + "B3.md", hdr=True, label="PROOF FILE: bridge B3"),
        F(EB + "ASSEMBLY.md", hdr=True, label="PROOF FILE: assembly of Theorems A and B from DIST-1..3 and the bridges"),
        F("W3-DIST/work/D_output/P6_DISTC.md", hdr=True, label="PROOF FILE: Lemma P6 and Theorem DIST-C"),
        F("W3-DIST/work/D_output/COR_C.md", hdr=True, label="PROOF FILE: Corollary C"),
    ],
    pending=[])

TARGETS["PB-T8"] = dict(
    title="Theorem 7: the reported model equals the truth, fixed design (W3-RM2-R:RM2-F-plus with RM0-plus and DLV-0)",
    claims=["W3-RM2-R:RM2-F-plus", "W3-RM2-R:RM0-plus", "W3-RM2-R:DLV-0"],
    sources=[
        F(RV, 26, 60, "STANDING ASSUMPTIONS (S1)-(S4)"),
        F(RV, 815, 858, "PRESENTED STATEMENT: Theorem 7 (reader statement)"),
        F("W3-RM2-R/STATEMENT.md", 33, 205, "STATEMENT: W3-RM2-R base, definitions and hypotheses, claims on the core, delivery and the reported model, example"),
        F("W3-RM2-R/lemmas/Q1_sandF_c.md", hdr=True, label="PROOF FILE: Lemma SAND-F-c"),
        F("W3-RM2-R/lemmas/Q2_TL_c.md", hdr=True, label="PROOF FILE: Lemma TL-F-c"),
        F("W3-RM2-R/lemmas/Q4_core_plus.md", hdr=True, label="PROOF FILE: Theorem RM0-plus (core)"),
        F("W3-RM2-R/lemmas/Q5_dlv0.md", hdr=True, label="PROOF FILE: Lemma DLV-0"),
        F("W3-RM2-R/lemmas/Q6_assembly.md", hdr=True, label="PROOF FILE: assembly of Theorem RM2-F-plus"),
        C("W3-RM2:NA-W"), C("W3-RM:E4"), C("W3-RM:RM-0"),
        C("C-DLV:Thm-D"), C("C-DLV:L2-S2"), C("C-DLV:L1-R"), C("C-DLV:Cor-R"), C("C-DLV:L3-3.3"), C("C-DLV:L3-3.4"),
        C("C-DLV:Prop-F"), C("C-DLV:P1-Inventory"), C("C-DLV:L2-S3"), C("W2-UNI:F-UNI"),
        C("C-GROW:L1.1"), C("C-GROW:L1.2"),
    ],
    pending=[])

TARGETS["PB-T9"] = dict(
    title="Theorem 10: the printed outputs are consistent (W3-READER:R4, from W3-SAMP:C and W3-START2-R:IF-START)",
    claims=["W3-READER:R4"],
    sources=[
        F(RV, 26, 30, "STANDING ASSUMPTIONS (S1), (S2)"),
        F(RV, 61, 70, "STANDING CONVENTIONS (S5) (sampler)"),
        F(RV, 1286, 1323, "PRESENTED STATEMENT: Theorem 10 (reader statement)"),
        F("W3-READER/lemmas/R4_printed_outputs.md", None, None, "PROOF FILE: assembly R4 (the claim, its proof and its scope remarks)", hdr=False),
        F("W3-SAMP/STATEMENT.md", 20, 60, "CONSUMED: W3-SAMP objects and conventions"),
        F("W3-SAMP/STATEMENT.md", 149, 163, "CONSUMED STATEMENT: W3-SAMP Theorem C (concentrated bridge)"),
        F("W3-START2-R/STATEMENT.md", 34, 87, "CONSUMED: W3-START2-R definitions and assumptions ((FL-R16), (V-R), (L-R++) ...)"),
        F("W3-START2-R/STATEMENT.md", 215, 246, "CONSUMED STATEMENT: W3-START2-R Gaussian rows (T3++), START-R, IF-START"),
        F("W3-POST/STATEMENT.md", 16, 100, "CONSUMED STATEMENT: the coded posterior; Theorem 1 (O_P form) with item 6"),
        C("W2-APP:POST", "CONSUMED STATEMENT: W2-APP Lemma POST"),
        F("Theory_work/Wave2/W2-APP/lemmas/L1_POST.md", 9, 19, "CONSUMED (standardised-signal convention): W2-APP L1_POST"),
        F("W3-READER/lemmas/R1_set_sizes.md", 6, None, "CONSUMED: set-size arithmetic R1 (B2.1, B6.1)"),
        F("W3-READER/NOTATION.md", 9, 60, "NOTATION"),
    ],
    pending=[])
# PB-T9 inputs of R4 (statement text of the inputs is taken from their own files above; the 'Inputs' section of
# the R4 file is cut below because it quotes registry statuses)

# "Known pending corrections (do not re-report)": the items of origin/theory/PRE-LEAN:Theory_work/Wave3/PRE_LEAN_PASS/CORRECTIONS.md
# (cdb5f027) that touch the text of a packet, plus the deferred T4 R4; location, then old -> new. Lines are those of origin/main.
T11 = ("W3-PSHARP/STATEMENT.md:100 (consequence (B1)) [T1-1]: \"if s₀ ≥ λ√n then π(S₀) ≤ 1/(1 + λ/3)\" → \"if s₀ ≥ λ√n, λ ≥ 0, then π(S₀) ≤ 1/(1 + λ/3)\"; "
       "W3-PSHARP/lemmas/B_sparsity.md:33 (B1): \"If s₀ ≥ λ√n: a_n ≥ λ/3\" → \"If s₀ ≥ λ√n (λ ≥ 0): a_n ≥ λ/3\"")
T31 = ("W3-DIST/work/D_output/P6_DISTC.md:70-72 (Positivity) [T3-1]: \"and m(S) is the integral of a strictly positive likelihood against a proper prior: m(S) ∈ (0, ∞).\" → "
       "\"and m(S) > 0, as the integral of a strictly positive likelihood against a proper prior. Also m(S) < ∞, by the closed form m(S) ∝ D_S^{−1/2}(2b₀ + Q_S)^{−ν} ([P1] `prop:closed`), since D_S ∈ (0, ∞), Q_S ≥ 0 and b₀ > 0.\"")
T4R1 = ("W3-POST/STATEMENT.md:86 (Theorem 1, item 4) [T4-R1]: \"sup_{h:Ω→[0,1]} |π(h) − h(S₀)| = O_P(r_n)\" → "
        "\"sup_{h:2^{[p]}→[0,1]} |Σ_{S∈Ω}π(S)h(S) − h(S₀)| = δ_n for every data set, hence O_P(r_n)\"")
T4R4 = ("W3-D3/STATEMENT.md:64-65 and W3-D3/lemmas/B3w.md:25 (Lemma B3w, m♯_n) [T4-R4, deferred]: \"(computed with p_ret and s₀)\" → "
        "\"(computed with (n, p, s₀), as in (c); on 𝒜_n, p_ret = p)\"")
T4N1 = ("W3-READER/READER_VERSIONS.md:109 and :121-122 (Theorem 1, (A6) second form) [T4-N1]: \"or θ*_min√(n/log n) → ∞\" → "
        "\"or θ*_min ≥ σ_*√(M_n log n/n)/φ₀ for a fixed sequence M_n → ∞\"; \"n₀ depends also on the divergence of θ*_min√(n/log n)\" → \"n₀ depends also on the sequence (M_n)\"")
T5R3 = ("W3-DIST/work/E_bridges/B3.md:98-99 (amendment A-2) [T5-R3]: \"The event 𝒜′_n is intersected with {p_ret = p} (which holds on the event of B1).\" → "
        "\"𝒜′_n is redefined as the set of outcomes on which the completed pair below satisfies the conditions of Step 6, with m♯_n computed from (n, p, s) and a replacement truth with exactly s nonzero coordinates; it is measurable in the completed pair and contains 𝒜_n (as in W3-D3/lemmas/B3w.md (c)).\"")
T5R1 = ("W3-DIST/STATEMENT.md:96-97 (DIST-2 commentary) [T5-R1]: \"Best rate ε_n² ≍ (1 + s₀^r) log n · ℓ_n/n: one logarithm slower than DIST-1 at polynomial p.\" → "
        "\"Best rate, for fixed s₀^r: ε_n² ≍ log n · ℓ_n/n, one logarithm slower than DIST-1 at polynomial p. As proved, its constant is at most of order (1 + s₀^r)³ for fixed (A, σ*², M, M′) (an upper bound, not known to be tight).\"")
T5R2 = ("W3-DIST/STATEMENT.md:78 (DIST-1) [T5-R2]: \"Equivalently, for every sequence ε_n\" → \"In particular (dropping the size clause), for every sequence ε_n\"")
T5R4 = ("W3-DIST/STATEMENT.md:151-152 (Theorem A premises) [T5-R4]: \"and are counted in them (in particular r = p outside them).\" → "
        "\"and are counted in them: there the posterior probabilities in the displays are read as 1. The common exceptional set of the proofs also contains every data set with r < p.\"")
T5R4R = ("W3-READER/READER_VERSIONS.md:1065-1067 (Theorem 9 setting) [T5-R4-reader]: \"(and p = p_raw outside them)\" → "
         "\"there the posterior probabilities in the displays are read as 1. The common exceptional set of the proofs also contains every data set with p < p_raw.\"")
T81 = ("W3-RM2-R/STATEMENT.md:80-81 (IDEAL-W⁺) [T8-1]: \", which are treated as true:\" → \"; the two bounds are treated as satisfied (the rejection predicates `le > 1e6`, `cap_ll > INT_MAX` never fire):\"")
T82 = ("W3-START2-R/STATEMENT.md:237 (START-R, remark after (iii); in the consumed span) [T8-2]: \"o₀ ≥ ½(n + 1)^{−1/2} on every data set\" → \"o₀ ≥ ½(n + 1)^{−1/2} on every data set with s₀ < K\"")
TARGETS["PB-T1"]["pending"] = [x.strip() for x in T11.split("; W3-PSHARP/lemmas") ]
TARGETS["PB-T1"]["pending"] = [TARGETS["PB-T1"]["pending"][0], "W3-PSHARP/lemmas" + TARGETS["PB-T1"]["pending"][1]]
TARGETS["PB-T3"]["pending"] = [T31]
TARGETS["PB-T4"]["pending"] = [T4R4, T4R1, T4N1, T5R3]
TARGETS["PB-T5"]["pending"] = [T31, T5R3, T5R1, T5R2, T5R4, T5R4R, T4R1]
T4N1B = ("W3-READER/READER_VERSIONS.md:824 (Theorem 7, (A1)) [T4-N1]: \"or θ*_min√(n/log n) → ∞\" → \"or θ*_min ≥ σ_*√(M_n log n/n)/φ₀ for a fixed sequence M_n → ∞\"")
TARGETS["PB-T8"]["pending"] = [T81, T4N1B]
TARGETS["PB-T9"]["pending"] = [T82, T4R1]


SYSTEM = """You are an independent referee. You receive the statement of one or more results from a research project on the asymptotic theory of a sequential Monte Carlo method for Bayesian variable selection (linear regression, p ≤ n^A, often p ≫ n), the full proof files, and the statements of the results they consume. Every result is asymptotic; finite-n behaviour is not a defect. Consumed results may be taken as true as stated; check that their stated hypotheses actually hold where they are used.

Your task: break the proofs. Find a genuine error, or say that you find none. Check every step: constants, the order of quantifiers, uniformity (in n, p, models, designs, events), probability-event bookkeeping and the thresholds in n that a bound needs and what those thresholds may depend on, measurability, that every cited lemma is applied within its stated hypotheses, that the proof does not use a hypothesis the statement does not state, that the statement does not claim more than the proof proves, and that consumed or recorded statements are quoted faithfully. Judge only the mathematics on the page; ignore any status or verdict the files might assert.

A list "Known pending corrections (do not re-report)" may be given; these items are already accepted, so do not report them (a different problem at the same place is still welcome).

Report findings only: no praise, no summary of what is correct, no style, notation or presentation remarks. For each finding give: severity (ERROR = a claim as stated is false or a step is false with no easy repair; GAP = a step is unjustified but plausibly repairable — describe the repair; MINOR = a local slip that does not affect a claim), the exact location (file:line, using the line numbers printed at the start of each line), the problem, and for ERROR/GAP a counterexample or the missing argument. If after checking you find no genuine error, say so in one sentence; do not pad with minor remarks and do not invent defects.

End with exactly one line per claim listed in the request, nothing after them, in this form:
AUDIT <claim id> FINDINGS=<count of GAP+ERROR>"""


def build_target(tid, spec):
    parts, man, drops = [], [], []
    for (_, rel, a, b, label, hdr) in spec["sources"]:
        if b == "S5":
            lines = read_lines(rel)
            b = next(i for i, l in enumerate(lines, 1) if l.startswith("## 5.")) - 1
        if tid == "PB-T9" and rel.endswith("R4_printed_outputs.md"):
            lines = read_lines(rel)
            a = next(i for i, l in enumerate(lines, 1) if l.startswith("## Claim (R4)"))
        txt, dropped, a2, b2 = excerpt(rel, a, b, hdr)
        parts.append(f"===== {label}\n===== file: {rel} (lines {a2}-{b2})\n{txt}")
        man.append((rel, a2, b2, dropped))
        if dropped:
            drops.append((rel, dropped))
    pend = [re.sub(r" \[T\d-[A-Za-z0-9-]+(?:, deferred)?\]", "", x) for x in spec["pending"]]
    if NO_NOTES:
        pend = []
    note = "" if NO_NOTES else ("Known pending corrections (do not re-report):\n" + "\n".join(f"- {p}" for p in pend)) if pend else \
        "Known pending corrections (do not re-report): none for this target."
    claims = "\n".join(f"- {c}" for c in spec["claims"])
    user = (f"Target: {spec['title']}.\n\nClaims to audit (the closing lines of your reply must name exactly these ids):\n{claims}\n\n"
            f"{note}\n\nThe sections below hold the statements, the full proof files and the consumed results. Line numbers "
            f"printed as `NNNN|` are the line numbers of the file named in the section header. Break the proofs; findings only.\n\n"
            + "\n\n".join(parts))
    return user, man


def main():
    reqdir = HERE / "requests"
    reqdir.mkdir(exist_ok=True)
    base = subprocess.run(["git", "rev-parse", "--short=8", "origin/main"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    allreq, tok, mantxt = [], [], [f"# source base: origin/main {base}; per file: sha256  path  lines  last-touch-commit  dropped(status/review words)"]
    seen = {}
    for tid, spec in TARGETS.items():
        user, man = build_target(tid, spec)
        for rel, a, b, dropped in man:
            if rel not in seen:
                seen[rel] = (sha(rel), last_commit(rel))
            mantxt.append(f"{tid}  {seen[rel][0]}  {rel}  lines {a}-{b}  {seen[rel][1]}  dropped: {dropped}")
        chars = len(user) + len(SYSTEM)
        tok.append((tid, chars))
        for k in range(1, N_SAMPLES + 1):
            req = {"custom_id": f"{tid}-s{k}",
                   "params": {"model": MODEL, "max_tokens": MAX_TOKENS, "output_config": {"effort": "high"},
                              "system": SYSTEM, "messages": [{"role": "user", "content": user}]}}
            allreq.append(req)
            (reqdir / f"{tid}-s{k}.jsonl").write_text(json.dumps(req, ensure_ascii=False) + "\n", encoding="utf-8")
    (HERE / "requests.json").write_text(json.dumps(allreq, ensure_ascii=False), encoding="utf-8")
    (HERE / "BUILD_MANIFEST.txt").write_text("\n".join(mantxt) + "\n", encoding="utf-8")
    with open(HERE / "TOKENS.tsv", "w", encoding="utf-8") as f:
        f.write("target\tchars\test_tokens_chars_over_3.5\test_tokens_pessimistic_chars_over_2.5\n")
        for tid, c in tok:
            f.write(f"{tid}\t{c}\t{round(c / 3.5)}\t{round(c / 2.5)}\n")
        f.write(f"TOTAL_per_sample\t{sum(c for _, c in tok)}\t{round(sum(c for _, c in tok) / 3.5)}\t{round(sum(c for _, c in tok) / 2.5)}\n")
        f.write(f"TOTAL_12_requests\t{2 * sum(c for _, c in tok)}\t{round(2 * sum(c for _, c in tok) / 3.5)}\t{round(2 * sum(c for _, c in tok) / 2.5)}\n")
    print(open(HERE / "TOKENS.tsv").read())


if __name__ == "__main__":
    main()
