# -*- coding: utf-8 -*-
"""Build REGISTRY.md and LOCKABLE.md from registry_data.py.  Text processing + git only (no computation).

Usage (from anywhere inside the worktree):  python3 -I build_registry.py   (after `git fetch origin`)
"""
import collections
import datetime
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import registry_data as D  # noqa: E402

ROWS = D.ROWS
REPO = subprocess.check_output(["git", "-C", HERE, "rev-parse", "--show-toplevel"], text=True).strip()


def git(*a):
    return subprocess.check_output(["git", "-C", REPO] + list(a), text=True).strip()


def esc(t):
    return str(t).replace("|", "\\|").replace("\n", " ")


def split(v):
    code, _, txt = v.partition("|")
    return code, txt


# ----------------------------------------------------------------------------------------------------------------
# verification level
# ----------------------------------------------------------------------------------------------------------------
LEVELS = [
    "XF-VERIFIED (cross-family VERIFIED, clean or qualified)",
    "XF-ADVERSE (cross-family GAP/ERROR)",
    "SF-VERIFIED only (same-family VERIFIED, no cross-family review)",
    "SF-ADVERSE only (same-family GAP/ERROR, no cross-family review)",
    "REFEREE-AUTHORED (no independent check)",
    "UNVERIFIED (author only)",
]


def is_referee_authored(row):
    return row["st"] == "REFEREE" or row["id"].endswith("(A2)") or row["id"].endswith("(A4)") or row["id"].endswith("(A3)")


def level(row):
    if is_referee_authored(row):
        return LEVELS[4]
    sf, _ = split(row["sf"])
    cf, _ = split(row["cf"])
    if cf in ("V", "V*"):
        return LEVELS[0]
    if cf in ("G", "E"):
        return LEVELS[1]
    if sf in ("V", "V*"):
        return LEVELS[2]
    if sf in ("G", "E"):
        return LEVELS[3]
    return LEVELS[5]


STATUSES = ["PROVED", "PROVED-UNDER", "PROOF SKETCH", "COUNTEREXAMPLE", "CONJECTURE", "OPEN", "REFEREE"]
results = [r for r in ROWS if r["kind"] == "result"]
claims = [r for r in ROWS if r["kind"] == "claim"]
ids = [r["id"] for r in ROWS]
assert len(ids) == len(set(ids)), [i for i, c in collections.Counter(ids).items() if c > 1]
for r in results:
    assert r["st"] in STATUSES, (r["id"], r["st"])

# ----------------------------------------------------------------------------------------------------------------
# sections of the main table
# ----------------------------------------------------------------------------------------------------------------
SECTIONS = [
    ("E1", "Theorem 1 — T03♯ and its T02 lemmas (W1-T03R; verifier W2-VT03R; cross-family A-REV2)"),
    ("Prop1-TD", "Theorem 3 part A — refined T37 / greedy repair (W1-T37R; verifier W3-VT37R; cross-family A-REV2)"),
    ("EXP′", "Theorem 2 — EXP′, chain laws, linked-hub family (W1-EXP; verifier W3-VEXP; cross-family A-REV2)"),
    ("IND-T", "Supplement — premises of Theorem B and Lemma U (W2-PREM; cross-family A-REV1/A-REV2)"),
    ("ThmB-T24", "Theorem 4 route (e′) / supplement — Gibbs-path repair, restated T24 (W1-T24G; verifier W2-VT24G; cross-family A-REV1)"),
    ("LemmaA-T38E", "Theorem 5 — delivery and eligibility (W1-T38E; verifier W3-VT38E; cross-family A-REV1)"),
    ("LemmaRO", "Theorem 4, Proposition 1, Proposition 2 — bookkeeping (W2-BOOK)"),
    ("T26-Lemma1", "Theorem 6 — evidence and PIP consistency (W2-T26)"),
    ("PXN-P1", "Theorems 2(v)/5(b1-LH-iid) — p ≫ n family (W3-PXN; same-family referee W5-VMASK; no cross-family review)"),
    ("PGD-L1.1", "Theorem 3 asymptotic clause — PGD / LD♭ (W3-PGD PROOF.md, REPORT.md a stub; same-family referee W5-VPGD; no cross-family review)"),
    ("T38-(0)", "Theorem 5 assembled (W4-T38FULL)"),
    ("SHARE-D4", "Theorem 5 route (b2) — envelope delivery (W4-SHARE; same-family referee W5-B2ENV; A-REV3 not landed)"),
    ("AREV1-LemmaS-sharp", "Referee-supplied repairs (A-REV1)"),
    ("Lemma-STREAM", "Late-landing: implementation lemmas (W5-LOCKBOOK audit)"),
    ("ADRAFT-ThmA", "Original-draft track (A-DRAFT, F-DRAFT; checked by A-REV4 where noted)"),
    ("OCERT-LemmaM", "New results: a-posteriori certificates (O-CERT; unverified)"),
    ("OSWAP-L0", "New results: finite-n theory of posterior misses (O-SWAP; unverified)"),
    ("PXN-LemmaTr", "Theorem 5(b1-LH-iid) lemmas verified by W5-VMASK (W3-PXN Lemmas Tr, Λ, U; added at the fifth fetch)"),
    ("VMASK-R1-NB", "New results: W5-VMASK (NB proof on LH-iid c = 1; numerically checked remarks)"),
    ("VPGD-R0", "New results: W5-VPGD REPAIRS.md (R0–R4, tie proposition, lattice form W_Lat, LH-PGD)"),
    ("OBG-LemmaR", "New results: bridge-Gibbs discovery, T38(b) without LS0 (O-BGIBBS; unreviewed)"),
    ("FAV-LemmaX", "New results: 2^B-free favourable rate on iid block-diagonal designs (W5-FAVIID REPORT.md / PROOF.md; author only)"),
    ("OWS-WS1", "New results: weight stability and regime dichotomy (O-WSTAB PROOF.md; no REPORT)"),
    ("CEX-W2frac(A4)", "Referee-supplied items (A-REV4, A-REV3)"),
    ("FMP-M1", "New results: masked-regime meaning of Ẑ and the PIPs (F-MASKPIP; unreviewed)"),
    ("OMIX-B1", "New results: mixture start and common plug-in σ² (O-MIX; unreviewed)"),
    ("B2E-LemmaOF", "New results: no-method-change masked theorems on LH (W5-B2ENV PROOF.md; author only)"),
    ("W6F1-PropU′", "Repair drafts (W6-FIXREV1 CONSOLIDATED.md, W6-FIXREV2 STATEMENTS.md; not reviewed)"),
]
sec_at = dict(SECTIONS)

COLS = ("| ID | Paper target | Source (branch · file · label) | Author status | Same-family verification | "
        "Cross-family verification | Repairs applied / pending | Open premises | Plain-English meaning |\n"
        "|---|---|---|---|---|---|---|---|---|\n")


def vtxt(v):
    code, txt = split(v)
    tag = {"V": "VERIFIED", "V*": "VERIFIED*", "G": "GAP", "E": "ERROR", "N": "none"}.get(code, code)
    if code == "N":
        return "none" if txt == "none" else "none — " + txt
    return "**%s** — %s" % (tag, txt)


def rep_text(row):
    base = row["rep"]
    if row["rs"] in ("pending", "applied"):
        return "[%s] %s" % (row["rs"].upper(), base)
    return base


def row_md(r):
    idc = "`%s`" % r["id"]
    if r["flags"]:
        idc += " ⚑ " + r["flags"].upper() if r["flags"] == "CONFLICT" else " (" + r["flags"] + ")"
    cells = [idc, r["tgt"], r["src"], r["st"], vtxt(r["sf"]) if not is_referee_authored(r) else "n/a (referee-authored)",
             vtxt(r["cf"]) if not is_referee_authored(r) else "referee-authored: " + split(r["cf"])[1],
             rep_text(r), r["prem"], r["mean"]]
    return "| " + " | ".join(esc(c) for c in cells) + " |\n"


# ----------------------------------------------------------------------------------------------------------------
# conflicts
# ----------------------------------------------------------------------------------------------------------------
CONFLICTS = [
    (["Lemma0(b)", "R2-dichotomy"], "W1-T37R Lemma 0(b) PROVED → W3-VT37R: inclusion VERIFIED but the 'posterior miss' inference ERROR (CEX-2), repair R2 stated PROVED → A-REV2: Lemma 0(b) as written ERROR **and** R2 itself ERROR (omits inferior local maxima / capped searches ending below the truth). Both recorded; W6-FIXREV2 (REPORT.md) replaces them by Lemma 0(b′) and the three-way Prop. F — same-family, unreviewed. W6-FIXREV2 §3.1 also disputes A-REV2's table wording that 'the initial centre is the truth' is trivial success (a search from S₀ moves away unless (L) holds at S₀)."),
    (["TDP-iff-DS"], "W3-VT37R VERIFIED the TD′_P ⇔ (L)∧all D_S equivalence (exhaustive check, ties have measure zero) vs A-REV2 ERROR (exact ties; strict D_S is only sufficient). W6-FIXREV2 agrees (Lemma T) and adds Lemma NT: ties are P₀-null under joint non-degeneracy, so the equivalence holds almost surely there but not deterministically."),
    (["PropU"], "W2-VT24G VERIFIED Prop. U as bookkeeping vs A-REV1 ERROR (independence moves can remove a truth; extra-for-extra swap can leave the phase-1 family). Theorem B unaffected."),
    (["LemmaS-attain"], "W1-T38E / W3-VT38E: bound 'tight', attained by two-level weights (VERIFIED) vs A-REV1 ERROR on the full domain (needs f > 1−e). The inequality itself is VERIFIED by all."),
    (["E3(ii)"], "W3-VT38E VERIFIED Theorem E3 including (ii) vs A-REV1 ERROR (omits locked T22(i-a)'s q < 1; p = 2 example). (i) and (iii) are VERIFIED by both."),
    (["EXP-const"], "W3-VEXP VERIFIED W1-EXP Thm 1 ('no mathematical ERROR') vs A-REV1/A-REV2 ERROR on the displayed limit 0.52/c_* (actual 0.51/c_*). Finite bound unaffected; same constant in W2-PREM Lemma U."),
    (["Thm4-iff"], "W1-EXP Thm 4 'iff' gloss; W3-VEXP R4 repair claims 'p^{−c} alone forces vanishing mass whatever η' vs A-REV2: 'iff' ERROR and VEXP's added claim not justified."),
    (["T38b-R(whole)"], "W1-T38E: 'PROVED given inputs'; W3-VT38E VERIFIED the whole composition; A-REV1: entire supplied statement GAP (composition and route (b1) VERIFIED; routes (b1′), (b2) and the execution qualifications are GAP)."),
    (["ORTH-joint", "T26-PropC"], "W2-T26 Prop. C = PROOF SKETCH (ORTH satisfies Theorem B's hypotheses) vs W4-T38FULL §2 'with no open statistical input on ORTH' / 'new composition, checked line by line here' (no verifier). F-REFINE writes 'PROVED/SKETCH'. Recorded as PROOF SKETCH (weaker)."),
    (["Thm2-BO (label)"], "W1-EXP labels Thm 2 PROOF SKETCH; W3-VEXP says it is a verbatim corollary of locked T22(iii) with no step open but 'does not change W1's status word'; F-REFINE lists '(F2) Thm 2 … VERIFIED'. Author status kept PROOF SKETCH (label mismatch, not a mathematical dispute)."),
    (["T38-(0)", "T38b-R(whole)"], "Scope of A-REV1: it reviewed W1-T38E's T38(b)-R, not W4-T38FULL (W6-FIXREV1 §3.1: several A-REV1 §7 repairs were already in W4). A-REV1's GAP applies in full to W1-T38E's statement and only to residual items for W4; W6-FIXREV1's T38 files supersede both."),
    (["Lemma0(a,c)"], "A-REV2's table calls the case 'initial centre already is the truth' trivial success; W6-FIXREV2 §3.1 disputes the wording (CEX-2 design: a search started at S₀ moves to S₀+x₃). A-REV2's §4.2 text is consistent with W6's correct statement."),
    (["Version: W1-T37R"], "W3-VT37R reviewed W1-T37R at d492f22 (REPORT.md an unfinished draft; exp1 json files 0 bytes). A-REV2 pinned 3bcc429 (complete REPORT, results present) and says the earlier referee's description does not apply. `git diff d492f22 3bcc429` touches only REPORT.md, exp1/exp1b results and a README: PROOF.md is identical, so the mathematical verdicts apply to the head; the W1 REPORT-level numbers (Exp 1/1b) were never adversarially re-run."),
    (["Legend: ARCHITECTURE"], "F-REFINE ARCHITECTURE.md marks nodes [P] = 'campaign PROVED, same-family VERIFIED' (e.g. Thm 4 T21 composition, Thm 2(ii)); the source reports show same-family verification for T21 only via W2-VT24G (route e′) and W3-VT38E (composition). Both F-REFINE files were written before A-REV1/A-REV2 landed (CARDS: 'had pushed nothing'): read their VERIFIED as same-family only, against the cross-family column here."),
    (["ThmW", "VPGD-PropT"], "W3-PGD Theorem W and F-REFINE ARCHITECTURE/CARDS ('the general sufficient condition for (M2)') vs W5-VPGD REPAIRS.md R6.1 Prop. T: in its REGION form R_{a,d}(𝒟), a ≥ 2, PGD fails with an exact tie on the masked linked-hub family with c ≥ 2 (20/20 population cases, D_S fails in 200/200 fits), so Theorem W does not cover the masked families; it holds in the lattice form W_Lat (VPGD-WLat), which W5-VPGD proves. W3 never claimed LH; the gap is in F-REFINE's description. Same-family only."),
    (["PXN-P6"], "W5-VMASK verified W3-PXN P6 (including Lemma Tr with a union over n^{A+1}2^{17} sets and the general-set use of W1-EXP L1.4 with count (p+1)^{s₀+2}) vs A-REV3: P6 GAP (Lemma Λ(a) calls Tr(c) over all sets of size ≤ s₀+2, count p^{s₀+2} and dimension possibly > 16, beyond Tr(c)'s stated range; Lemma U(U1) arithmetic false). Both agree on U1; A-REV3 did not read W5-VMASK. The weaker verdict is recorded in the cross-family column; neither side has a counterexample to the intended lattice conclusion."),
    (["SHARE-M(b)", "SHARE-B2W4"], "W4-SHARE Prop. M(b) PROOF SKETCH; W5-B2ENV referee: argument correct, upgraded on LH to PROVED (B2E-MLH, author only); Theorem B2-W4 VERIFIED given its inputs; vs A-REV3: M(b) ERROR (quadratic equality used as an expansion: exact gain/n → ½log 2 vs ¼; vanishing crossing temperature false under BM-C) and the §7 exit-loss simplification ERROR (two-state counterexample). D4, D5 and the conditional B2-W4 inequality are VERIFIED by both families. A-REV3 did not read W5-B2ENV; nobody states whether B2E-MLH (which uses EXP′, not the quadratic expansion) is affected."),
    (["LH-LAT", "LH-LAT-sharp"], "W4-T38FULL Prop. LH-LAT 'm₀ is sharp' (its own same-family subagent: 20 brute-force cases) vs W5-VMASK: validity VERIFIED in 202/202 settings, but m₀ is sharp only on homogeneous pairs (108/108) and not on 32/94 heterogeneous settings (down to ×0.002); repair R5 gives the exact formula."),
]
flagged = {r["id"] for r in ROWS if r["flags"] == "CONFLICT"}
listed = {i for ids_, _ in CONFLICTS for i in ids_}
assert flagged <= listed, flagged - listed

# ----------------------------------------------------------------------------------------------------------------
# summary computations
# ----------------------------------------------------------------------------------------------------------------
matrix = collections.OrderedDict((s, collections.Counter()) for s in STATUSES)
for r in results:
    matrix[r["st"]][level(r)] += 1

err_rows = [r for r in ROWS if split(r["sf"])[0] == "E" or (split(r["cf"])[0] == "E" and not is_referee_authored(r))]
gap_rows = [r for r in ROWS if r not in err_rows and (split(r["sf"])[0] == "G" or (split(r["cf"])[0] == "G" and not is_referee_authored(r)))]


def who_flagged(r):
    out = []
    for lab, v in (("same-family", r["sf"]), ("cross-family", r["cf"])):
        c, t = split(v)
        if c == "E":
            out.append("%s: %s" % (lab, t))
    return "; ".join(out)


def repair_exists(r):
    if r["rs"] == "applied":
        return "YES — applied (%s)" % r["rep"]
    if r["rs"] == "pending":
        return "PENDING — %s" % r["rep"]
    return "NO — %s" % r["rep"]


# ----------------------------------------------------------------------------------------------------------------
# git snapshot of source branches
# ----------------------------------------------------------------------------------------------------------------
branches = [b.strip().replace("origin/", "", 1) for b in git("branch", "-r").splitlines() if "origin/theory/" in b]
branches = sorted(b for b in branches if b.startswith("theory/"))
rx = re.compile(r"^theory_campaign/[^/]+/(REPORT|REVIEW|REPAIRS|CARDS|STATEMENTS|ARCHITECTURE|REFEREE|CONSOLIDATED|NEW_TARGETS|T38_STATEMENT|BOOK_CHECK|DRAFTS_CHECK)[^/]*$", re.I)
SKIP = {"theory/campaign", "theory/smoke-test", "theory/S-REGISTRY"}
cov = []
for b in branches:
    if b in SKIP or "smoke" in b:
        continue
    files = [f for f in git("ls-tree", "-r", "--name-only", "origin/" + b).splitlines()
             if rx.search(f) and "/sources/" not in f]
    files = [f.split("/", 1)[1] for f in files]
    cov.append((b, git("rev-parse", "--short", "origin/" + b), files))
NOTES = {
    "theory/A-DRAFT": "full REPORT.md read (Astra; original-draft track).",
    "theory/F-DRAFT": "no REPORT.md; CROSSWALK.md and NEW_TARGETS.md (summary table of statuses) read as its statements file.",
    "theory/F-SHARE": "BRIEF.md only (no results).",
    "theory/A-REV4": "REVIEW.md (verdict table, §§1–7), BOOK_CHECK.md, DRAFTS_CHECK.md and NUMERICS.md read (GPT-6 Astra; Owls numerics reported; covers W2-T26, W2-BOOK, F-DRAFT, A-DRAFT §2).",
    "theory/A-REV3": "REVIEW.md (verdict table, W3-PXN and W4-SHARE sections, reproduction summary) read; STATUS.md not read.",
    "theory/F-MASKPIP": "REPORT.md read (statements M1–M3, R, N; §4.1 helper simulation not extracted).",
    "theory/O-MIX": "REPORT.md read (statements B1–B3, C0–C3, recommendation table).",
    "theory/W7-PART": "specs and port/check scripts only; no report yet.",
    "theory/W7-SEP": "NOTES.md (working notes and plan) only; no results yet.",
    "theory/O-PW2": "scripts only (exact small-p PW2 script); no report yet.",
    "theory/O-BGIBBS": "REPORT.md read (new at the fifth fetch; §4.1 simulation results still to be filled).",
    "theory/O-LS0": "scripts only; no REPORT.md yet (LS0 post hoc run on Owls).",
    "theory/O-WSTAB": "no REPORT.md; PROOF.md read as its statements file (theorem headers and status words only).",
    "theory/S-PAPER": "LaTeX skeleton + README (not a results branch).",
    "theory/W3-PGD": "REPORT.md is a 340-byte stub; claims read from PROOF.md (statement headers only); referee = W5-VPGD.",
    "theory/W5-B2ENV": "REFEREE.md (same-family verdicts on W4-SHARE) and PROOF.md (headers, status words, Prop. M-LH, Thm B2-LH) read.",
    "theory/W5-FAVIID": "REPORT.md (statement table; body sections still placeholders) and PROOF.md headers/status words read, incl. Prop. B1.",
    "theory/W5-LOCKBOOK": "REPORT.md + STATEMENTS.tex read (same-family referee of W2-BOOK/W2-T26; proves T32(i)). AUDIT.md/PROOF.md not read.",
    "theory/W5-VMASK": "REPORT.md read (26-row verdict table on W3-PXN and W4-T38FULL, statements, confidence card); REPAIRS.md R1–R7 via the report.",
    "theory/W5-VPGD": "REFEREE.md, REPAIRS.md (R0–R6) and REPORT.md (verdict table, statements) read. STAR.md referenced, not read.",
    "theory/W6-FIXREV1": "REPORT.md read (change-log table); CONSOLIDATED.md and T38 files: section headings only, statements not individually extracted.",
    "theory/W6-FIXREV2": "REPORT.md read (change-log table §2.1 + §3); STATEMENTS.md headings only.",
}
nofile = [b for b, h, f in cov if not f]
read_ok = [b for b, h, f in cov if f]

# ----------------------------------------------------------------------------------------------------------------
# write REGISTRY.md
# ----------------------------------------------------------------------------------------------------------------
today = datetime.date.today().isoformat()
out = []
w = out.append
w("# SMC-BVS theory campaign — CLAIMS REGISTRY\n\n")
w("Built by S-REGISTRY (branch `theory/S-REGISTRY`) on %s from `origin/theory/*` as fetched at the head SHAs listed in §E. "
  "Text processing only; nothing was recomputed and **no status was upgraded**. Companion file: `LOCKABLE.md`. "
  "Reproduce with `python3 -I theory_campaign/S-REGISTRY/build_registry.py` (rows live in `registry_data.py`).\n\n" % today)
w("**How to read the columns.** *Author status* is the status word the author wrote (PROVED / PROVED-UNDER = \"PROVED given/under named inputs\" / PROOF SKETCH / "
  "COUNTEREXAMPLE / CONJECTURE / OPEN / REFEREE = a repair or counterexample supplied by a cross-family referee without a PROVED label). "
  "*Same-family* = a campaign verifier run (Opus checking Opus). *Cross-family* = A-REV1 / A-REV2 / A-REV4 (Astra reviewers) only; A-REV4 covers W2-BOOK (Lemma RO, Prop. 1–2) and F-DRAFT, and checks A-DRAFT §2 as Astra-on-Astra (recorded in the same-family column of those rows). "
  "Verdict tags: **VERIFIED**, **VERIFIED*** (verified after a repair or with a stated qualification), **GAP**, **ERROR**, none. "
  "*Repairs*: `[APPLIED]` = a campaign run has already written the fix; `[PENDING]` = no repair written yet. **W6-FIXREV1 and W6-FIXREV2 REPORT.md have landed** and apply every A-REV finding (they agree with all of them; FIXREV2 adds two wording qualifications), so most former pending items are now `[APPLIED]`; but those repairs are same-family (Opus) and **no second model family has reviewed them** Paper targets follow F-REFINE `CARDS.md` / `ARCHITECTURE.md`; \"supplement\" and \"none\" as in `ARCHITECTURE.md` §5.\n\n")
w("**Standing caveat.** F-REFINE's CARDS/ARCHITECTURE were written before A-REV1/A-REV2 existed, so their \"VERIFIED\" is same-family only. "
  "None of this is adopted; locking is Felipe's decision.\n\n")

# ---- A. summary
w("## A. Summary\n\n")
w("### A1. Counts by author status × verification level\n\n")
w("%d named results in the main table (§B) plus %d flagged sub-claims (§C, not counted here). Verification level is the highest reached "
  "with a clean verdict; an adverse cross-family verdict overrides a same-family VERIFIED.\n\n" % (len(results), len(claims)))
short = ["XF-VERIFIED", "XF-ADVERSE", "SF-VERIFIED only", "SF-ADVERSE only", "REFEREE-AUTHORED", "UNVERIFIED"]
w("| Author status | " + " | ".join(short) + " | **Total** |\n|---|" + "---|" * (len(short) + 1) + "\n")
tot = collections.Counter()
for s in STATUSES:
    c = matrix[s]
    n = sum(c.values())
    if n == 0:
        continue
    for lv in LEVELS:
        tot[lv] += c[lv]
    w("| %s | %s | **%d** |\n" % (s, " | ".join(str(c[lv]) for lv in LEVELS), n))
w("| **Total** | %s | **%d** |\n\n" % (" | ".join("**%d**" % tot[lv] for lv in LEVELS), len(results)))
w("Levels: XF = reviewed by A-REV1/A-REV2/A-REV3/A-REV4 (VERIFIED, clean or with a stated qualification); XF-ADVERSE = a cross-family GAP/ERROR stands on that row; SF = a campaign verifier run only; REFEREE-AUTHORED = written by a cross-family referee; UNVERIFIED = author only (includes same-family *authors* checking their own work).\n\n")
by_status = collections.Counter(r["st"] for r in results)
w("By status only: " + ", ".join("%s %d" % (s, by_status[s]) for s in STATUSES if by_status[s]) + ".\n\n")

w("### A2. CONFLICTS (sources disagree; both sides recorded in the rows)\n\n")
w("| # | Rows | What conflicts |\n|---|---|---|\n")
for k, (idl, txt) in enumerate(CONFLICTS, 1):
    w("| C%d | %s | %s |\n" % (k, ", ".join("`%s`" % i for i in idl), esc(txt)))
w("\n")

w("### A3. Items with an ERROR verdict, and whether a repair exists\n\n")
w("%d items (main-table rows and flagged sub-claims). *Repair state*: YES = a campaign run has written the fix (for A-REV findings: W6-FIXREV1/2, same-family, not re-reviewed); PENDING = proposed only; NO = none.\n\n" % len(err_rows))
w("| Item | Part of | Who flagged ERROR | Repair? |\n|---|---|---|---|\n")
for r in err_rows:
    w("| `%s` | %s | %s | %s |\n" % (r["id"], esc(r["tgt"]), esc(who_flagged(r)), esc(repair_exists(r))))
w("\nGAP verdicts (no ERROR) are marked in §B/§C; they are: " + ", ".join("`%s`" % r["id"] for r in gap_rows) + ".\n\n")
n_app = sum(1 for r in err_rows if r["rs"] == "applied")
n_pen = sum(1 for r in err_rows if r["rs"] == "pending")
n_no = len(err_rows) - n_app - n_pen
w("ERROR items: %d with a repair already applied, %d with a repair only proposed by the referee (not yet written by any run), %d with no repair.\n\n" % (n_app, n_pen, n_no))

w("### A4. Lockable candidates\n\nSee `LOCKABLE.md` (author PROVED + same-family VERIFIED + cross-family VERIFIED or repaired). "
  "Strict-list size: see that file; it is a list of candidates, not a recommendation to adopt.\n\n")

# ---- B. main table
w("## B. Registry of named results\n\n")
w("Rows are grouped by source family. Within a group, lemmas precede theorems only where the source did.\n\n")
open_table = False
for r in results:
    if r["id"] in sec_at:
        w("\n### B.%s\n\n" % esc(sec_at[r["id"]]))
        w(COLS)
    w(row_md(r))
w("\n")

# ---- C. flagged sub-claims
w("## C. Flagged sub-claims (ERROR / GAP verdicts inside larger results; not counted in A1)\n\n")
w(COLS)
for r in claims:
    w(row_md(r))
w("\n")

# ---- D. implementation + retired
w("## D. Implementation facts the theorems lean on (not results; not counted)\n\n")
w("| Code | Statement | Source | Status |\n|---|---|---|---|\n")
for c, s, src, st in D.IMPL:
    w("| `%s` | %s | %s | %s |\n" % (c, esc(s), esc(src), esc(st)))
w("\n### Retired / refuted statements (replacement in the last column)\n\n")
w("| Retired statement | Why | Replacement |\n|---|---|---|\n")
for a, b, c in D.RETIRED:
    w("| %s | %s | %s |\n" % (esc(a), esc(b), esc(c)))
w("\n")

# ---- E. coverage
w("## E. Coverage: branches read and head SHAs\n\n")
w("Files matched: REPORT, REVIEW, REPAIRS, CARDS, STATEMENTS, ARCHITECTURE, plus REFEREE / CONSOLIDATED / NEW_TARGETS / T38_STATEMENT where a branch has no REPORT yet.\n\n")
w("| Branch | Head | Files read | Note |\n|---|---|---|---|\n")
for b, h, f in cov:
    w("| %s | `%s` | %s | %s |\n" % (b, h, ", ".join(esc(x) for x in f) or "—", esc(NOTES.get(b, ""))))
have = {b.split("/", 1)[1] for b, _, _ in cov}
expected = ["F-PXN", "O-DILUTE"]
missing = [x for x in expected if x not in have]
w("\nNamed in the LEDGER but with no branch on origin at the last fetch: " + ", ".join("`theory/%s`" % x for x in missing)
  + " (F-PXN was cancelled). `theory/campaign` and smoke branches skipped. Re-run the builder after they land.\n")
open(os.path.join(HERE, "REGISTRY.md"), "w", encoding="utf-8").write("".join(out))

# ----------------------------------------------------------------------------------------------------------------
# LOCKABLE.md
# ----------------------------------------------------------------------------------------------------------------
def okc(v):
    return split(v)[0] in ("V", "V*")


strict = [r for r in results if r["st"] == "PROVED" and okc(r["sf"]) and okc(r["cf"]) and not is_referee_authored(r)]
after = [r for r in results if r["st"] == "PROVED" and okc(r["sf"]) and split(r["cf"])[0] in ("G", "E") and r["rs"] == "applied"]
sf_only = [r for r in results if r["st"] == "PROVED" and okc(r["sf"]) and split(r["cf"])[0] == "N"]
xf_only = [r for r in results if r["st"] == "PROVED" and split(r["sf"])[0] == "N" and okc(r["cf"]) and not is_referee_authored(r)]
cex = [r for r in results if r["st"] == "COUNTEREXAMPLE" and okc(r["sf"]) and okc(r["cf"])]
cond = [r for r in results if r["st"] == "PROVED-UNDER" and okc(r["sf"]) and okc(r["cf"])]

lk = []
w = lk.append
w("# LOCKABLE — candidates for locking (Felipe's adoption decision)\n\n")
w("Built by S-REGISTRY on %s from `REGISTRY.md`. **Rule** (strict): author status **PROVED** (not PROVED-UNDER) **and** same-family verdict VERIFIED "
  "(or VERIFIED after repair) **and** cross-family verdict VERIFIED (or VERIFIED with qualification). Items whose cross-family verdict is GAP/ERROR qualify only through a written repair (§2: W6-FIXREV1/2, same-family, not re-reviewed). This file lists candidates; it does not adopt, lock or upgrade anything, "
  "and VERIFIED here is a referee verdict on the stated hypotheses (the table's *Qualification* column must travel with the statement).\n\n" % today)
w("**Counts:** %d strict candidates · %d repaired by W6 but not re-reviewed · %d same-family-only · %d cross-family-only · %d counterexamples confirmed by both · %d conditional implications verified by both.\n\n"
  % (len(strict), len(after), len(sf_only), len(xf_only), len(cex), len(cond)))
w("## 1. Strict candidates\n\n| ID | Paper target | Source | Same-family | Cross-family (qualification) | Premises that must stay attached |\n|---|---|---|---|---|---|\n")
for r in strict:
    w("| `%s` | %s | %s | %s | %s | %s |\n" % (r["id"], esc(r["tgt"]), esc(r["src"]), esc(split(r["sf"])[1]),
                                                esc(split(r["cf"])[1]), esc(r["prem"])))
w("\n### Strict candidates grouped by paper target\n\n")
bt = collections.OrderedDict()
for r in strict:
    bt.setdefault(r["tgt"], []).append(r["id"])
for t, l in bt.items():
    w("- **%s**: %s\n" % (t, ", ".join("`%s`" % i for i in l)))
w("\nCaveats that apply to the whole list: every proof is asymptotic or conditional on its stated hypotheses; none speaks to the n = 200 numbers "
  "(F-REFINE ARCHITECTURE §6–§7); implementation facts (GUARD, SR, emit_centre) are not audited theorems.\n\n")

w("## 2. REPAIRED, not yet re-reviewed (author PROVED + same-family VERIFIED; cross-family GAP/ERROR; W6 repair written, same-family only)\n\n")
w("These satisfy the rule through its \"or repaired\" clause, but the repair has **not** been seen by a second model family; treat as conditional candidates. A-REV re-review of the W6 text would promote them.\n\n")
if after:
    w("| ID | Cross-family finding | Repair |\n|---|---|---|\n")
    for r in after:
        w("| `%s` | %s | %s |\n" % (r["id"], esc(split(r["cf"])[1]), esc(r["rep"])))
else:
    w("none.\n")
w("\n")

w("## 3. NOT lockable under the rule — shown so nothing is mistaken for a candidate\n\n")
w("### 3a. Author PROVED + same-family VERIFIED, no cross-family review yet\n\n")
w("| ID | Paper target | Same-family | Note |\n|---|---|---|---|\n")
for r in sf_only:
    w("| `%s` | %s | %s | cross-family review pending |\n" % (r["id"], esc(r["tgt"]), esc(split(r["sf"])[1])))
w("\n### 3b. Cross-family VERIFIED but no independent same-family check (author = verifier, or no verifier run)\n\n")
w("| ID | Paper target | Cross-family | Why not strict |\n|---|---|---|---|\n")
for r in xf_only:
    w("| `%s` | %s | %s | %s |\n" % (r["id"], esc(r["tgt"]), esc(split(r["cf"])[1]), esc(split(r["sf"])[1])))
w("\n### 3c. Counterexamples confirmed by a same-family verifier and by A-REV1/A-REV2 (candidates for locking as negative results)\n\n")
w("| ID | Statement | Same-family | Cross-family |\n|---|---|---|---|\n")
for r in cex:
    w("| `%s` | %s | %s | %s |\n" % (r["id"], esc(r["mean"]), esc(split(r["sf"])[1]), esc(split(r["cf"])[1])))
w("\n### 3d. Conditional theorems (PROVED-UNDER) whose implication is verified by both families\n\n")
w("| ID | Paper target | Premises | Cross-family |\n|---|---|---|---|\n")
for r in cond:
    w("| `%s` | %s | %s | %s |\n" % (r["id"], esc(r["tgt"]), esc(r["prem"]), esc(split(r["cf"])[1])))
w("\n### 3e. Headline items with NO verification at all (author only)\n\n")
unv = [r for r in results if level(r) == LEVELS[5] and r["st"] in ("PROVED", "PROVED-UNDER")]
w(", ".join("`%s`" % r["id"] for r in unv) + "\n\n")
w("Largest holes (no cross-family review at the last fetch): Prop 1 and Prop 2 beyond the A-REV4 items (`Prop1-T07`, `Prop2*`: A-REV4 reviewed Lemma RO, the island identity and the Markov bound, and found GAP/ERROR items that are NOT yet repaired); `Thm4-C1`, `T21-e′`; the W3-PGD / W5-VPGD family (`ThmW`, `PGD-*`, `VPGD-*`: same-family only); the W3-PXN family and W4-T38FULL lemmas (`PXN-*`, `LS-score`, `LemmaM`, `LH-LAT`: second same-family verdict from W5-VMASK; A-REV3 had not landed); W4-SHARE (`SHARE-*`: same-family W5-B2ENV; A-REV3 not landed); and everything marked author-only in 3e: W5-VMASK R1, the W5-VPGD repairs, O-BGIBBS (Lemma R, BG1), W5-FAVIID, W5-B2ENV PROOF.md, O-WSTAB, O-CERT, O-SWAP.\n")
open(os.path.join(HERE, "LOCKABLE.md"), "w", encoding="utf-8").write("".join(lk))

print("results", len(results), "claims", len(claims), "errors", len(err_rows), "gaps", len(gap_rows))
print("strict", len(strict), "after", len(after), "sf_only", len(sf_only), "xf_only", len(xf_only), "cex", len(cex), "cond", len(cond))
print({s: sum(matrix[s].values()) for s in STATUSES})
