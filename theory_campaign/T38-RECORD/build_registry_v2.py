# -*- coding: utf-8 -*-
"""Build REGISTRY_v2.md and LOCKABLE_v2.md (T38-RECORD) from registry_v2_data.py, which overlays the verbatim
S-REGISTRY rows (registry_data.py). Derived from S-REGISTRY build_registry.py. Text processing + git only.

Usage: python3 -I build_registry_v2.py   (after `git fetch origin`)
"""
import collections
import datetime
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import registry_v2_data as D  # noqa: E402

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
    return row["st"] == "REFEREE" or re.search(r"\(A[2-9]\)$", row["id"]) is not None


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
    ("OPW2-ThmA", "New results: PW2-free variance bound for the island evidence ratio (O-PW2; unreviewed)"),
    ("B2E-LemmaOF", "New results: no-method-change masked theorems on LH (W5-B2ENV PROOF.md; author only)"),
    ("W6F1-PropU′", "Repair drafts (W6-FIXREV1 CONSOLIDATED.md, W6-FIXREV2 STATEMENTS.md; not reviewed)"),
    ("OBG-BG2", "v2 — O-BGIBBS final head 55679ee: BG2, BG1′, LH-rate, BG3, LH-lock (T38(b) without LS0; author only; A-REV7 pending)"),
    ("FSH-F1", "v2 — F-SHARE REPORT (head 13bc665): closed-class delivery F1/F2 (author only; A-REV7 pending)"),
    ("SEP-A", "v2 — W7-SEP (head 858004e): separation theorem, Prop. GU (author only; A-REV7 pending)"),
    ("PART-ThmA", "v2 — W7-PART (head b2aa940): partition = groups (author only; A-REV6 pending)"),
    ("T05-R", "v2 — W7-SEC (head 7e33e8a): T05, T33, T32(i) addendum (author's own check only)"),
    ("STG-L0", "v2 — O-STAGES (head 8d3c142): stage count T_n (author only)"),
    ("DIL-E", "v2 — O-DILUTE (head abedf99): dilution masking (author only; A-REV6 pending)"),
    ("SIG-S0", "v2 — F-SIGMA (head e2a3481): common-σ̂² start (author only; the method change is rejected)"),
    ("T38-v3", "v2 — T38-RECORD: statement of record for Theorem 5"),
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
    (["Cost-T38", "T32(i)"], "v2. T32(i): W5-LOCKBOOK PROVED, W7-SEC re-count 'no error' (same family) vs W6-FIXREV1 T38 dependency k1 and W7-SEP input I11 'CONJECTURE'. The latter are stale (they predate or ignore W5-LOCKBOOK), not dissenting. Recorded PROVED (author W5-LOCKBOOK), same family only; T38 v3 cites PROVED-UNDER T32(i)."),
    (["SEP-E"], "v2. W7-SEP SEP(E)'s v3 row is conditional on T32(i) as a CONJECTURE (I11); W5-LOCKBOOK proves T32(i). Same staleness as the Cost-T38 conflict. W7-SEP also cites only O-BGIBBS BG1 (PROOF SKETCH), not BG3 (PROVED) + LH-lock (PROOF SKETCH)."),
    (["T38-b1′", "T38-b2", "OBG-T38b-BG3", "FSH-T38b2", "B2E-D2LH"], "v2. 'Without LS0 there is no masked-regime theorem' (W4-T38FULL, W6-FIXREV1: OPEN) vs no-LS0 candidates on LH (W5-B2ENV D2-LH and B2-LH, W5-VMASK R1, O-BGIBBS BG3 + LH-lock, F-SHARE F1/F2, W7-SEP GU). Recorded: candidates, pending A-REV7; none XF reviewed (T38 v3 I.D)."),
    (["OCERT-§4"], "v2. O-VCERT: §4 empty, every O-CERT numeric claim unsupported (at 17e7f15) vs O-CERT 0edc58f/332bf3e: illustration on 4 study fits added afterwards. The later illustration has not been reviewed."),
    (["STG-Wp"], "v2. O-STAGES Cor. W′ rests on (LL), F-DRAFT Theorem W's layer law, vs O-WSTAB's COUNTEREXAMPLE to F-DRAFT W(c) and W(b) on the divergent side (2Ar > 1). O-WSTAB's own W′ (ORTH, T_ideal ∈ {1, 2}) is PROVED independently and is consistent. (LL) may need restating for 2Ar > 1."),
    (["OMIX-C1"], "v2. O-MIX: common plug-in σ² (C) 'is the right tool for the n = 200 dilution masking' (BO toy) vs O-DILUTE §5 ('Do not adopt it') and F-SIGMA Thm S6 ('No single σ̂² serves truths and nulls at once'). Decision taken: rejected (E-SPINE §2.2). Theorem C1 itself (under BO) is not disputed."),
    (["T38-b1-LH", "T38-b1-LH-iidfail"], "v2 (cross-family vs cross-family). The (b1-LH) clause 'Q_fπ₀(S₀) → 0 when c ≥ 2 and p → ∞': A-REV5 ERROR (slow-p counterexample, p ≍ log log n) vs A-REV8 GAP (the ceiling does not vanish, but this is not a counterexample to the actual production Q_f, which may run on the exact branch). Both give the same repair (n^{1−c/2}p^{−c}log²n → 0). Recorded at the weaker verdict, ERROR, on the clause only; the LS0 consistency conclusion is VERIFIED by A-REV8."),
    (["SEP-GU"], "v2 (cross-family scope). A-REV7: Prop. GU VERIFIED as a greedy best-neighbour theorem; A-REV9: GAP in its own review because the imported Lemma M was not re-audited there (A-REV8 VERIFIED Lemma M). Not a mathematical disagreement; recorded V* with both texts."),
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
SKIP = {"theory/campaign", "theory/smoke-test", "theory/T38-RECORD"}
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
    "theory/F-SHARE": "v2: REPORT.md read (F1, F3, Lemmas 1.2, 3.1–3.4, PK, DOM, F2, §4, F1′, F2-iid).",
    "theory/A-REV4": "REVIEW.md (verdict table, §§1–7), BOOK_CHECK.md, DRAFTS_CHECK.md and NUMERICS.md read (GPT-6 Astra; Owls numerics reported; covers W2-T26, W2-BOOK, F-DRAFT, A-DRAFT §2).",
    "theory/A-REV3": "REVIEW.md (verdict table, W3-PXN and W4-SHARE sections, reproduction summary) read; STATUS.md not read.",
    "theory/F-MASKPIP": "REPORT.md read (statements M1–M3, R, N; §4.1 helper simulation not extracted).",
    "theory/O-MIX": "REPORT.md read (statements B1–B3, C0–C3, recommendation table).",
    "theory/W7-PART": "v2: REPORT.md via W8-SYNTH digest G3 (Theorems A–C, L1–L3, CE1–CE3) and §1 headline.",
    "theory/W7-SEP": "v2: REPORT.md read (Theorem SEP (A)–(E), BASIN, GU, Cor. GU-LH).",
    "theory/O-PW2": "REPORT.md read (headline statements A–C and the numerical counterexample).",
    "theory/W7-SEC": "v2: REPORT.md via W8-SYNTH digest G3 (T05, T33, T32(i) re-check and fp addendum).",
    "theory/O-BGIBBS": "v2: final REPORT.md read (BG2, BG1′, LH-rate, BG3, LH-lock added).",
    "theory/O-LS0": "v2: REPORT.md read (wrap-up by O-LS0-WRAP); data facts in §D2.",
    "theory/O-DILUTE": "v2: REPORT.md + THEORY.md via W8-SYNTH digest G5 (Thm E, R, Lemma N, Prop S, D′, DM).",
    "theory/O-STAGES": "v2: REPORT.md via W8-SYNTH digest G3.",
    "theory/F-SIGMA": "v2: REPORT.md via W8-SYNTH digest G5 (S0–S6, C-E1–C-E4).",
    "theory/O-VCERT": "v2: REPORT.md via W8-SYNTH digest G5 (verdict table, R1, R2); entered in the O-CERT rows' same-family column.",
    "theory/S-ELS": "v2: REPORT.md (ledger extraction); data facts in §D2.",
    "theory/L-LEAN": "v2: REPORT.md (final, head cfa78ed; Astra round 2 GREEN); §G.",
    "theory/F-REFEREE": "v2: REFEREE_REPORT.md / RESPONSE_PLAN.md via W8-SYNTH §5; §H.",
    "theory/W8-SYNTH": "v2: SYNTHESIS.md read in full (no new results; conflicts §4 folded into §A2).",
    "theory/E-SPINE": "v2: docs amendment branch (Docs/Theory/AMENDMENTS_20261102.md); decisions in §I.",
    "theory/A-REV5": "v2: REVIEW.md read (landed during the rebuild; verdict table, overall verdicts, residual errors, LOCKABLE list); REV1_CHECK/REV2_CHECK not read separately.",
    "theory/A-REV6": "v2: REVIEW.md read (landed during the rebuild); BOOK.md T32 rows read; SHARE/WEIGHTS/PARTITION by reference only.",
    "theory/A-REV7": "v2: REVIEW.md read in full (landed during the rebuild).",
    "theory/API-AUDIT": "after the T38-RECORD cut-off (in progress: NOTES only); not read.",
    "theory/API-FAVIID": "after the T38-RECORD cut-off (REPORT + amended W5-FAVIID report, hand-off for an XF referee); not read; rebuild to include.",
    "theory/API-POS": "after the T38-RECORD cut-off (in progress: NOTES only); not read.",
    "theory/API-RESID": "after the T38-RECORD cut-off (partial Step 0 output, data); not read.",
    "theory/A-REV8": "v2: REVIEW.md read in full (landed during the rebuild; XV-MASKED-LS0).",
    "theory/A-REV9": "v2: REVIEW.md read (landed during the rebuild; final verdict register); DILUTE_STAGES_CHECK / MASKED_PW2_CHECK not read separately.",
    "theory/W5-FAVIID": "v2: REPORT.md complete at head 31695b1 (headline, §4.5, card); rows unchanged.",
    "theory/W3-PGD": "v2: REPORT.md final (head fdeaec3); rows unchanged.",
    "theory/O-CERT": "v2: head 332bf3e adds §4 illustration (4 study fits) and Remark C6′ after O-VCERT's review.",
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
w("# SMC-BVS theory campaign — CLAIMS REGISTRY v2\n\n")
w("Rebuilt by T38-RECORD (branch `theory/T38-RECORD`) on %s from `origin/theory/*` at the head SHAs in §E. It extends S-REGISTRY's "
  "REGISTRY.md (head 3d88da6): the original rows are loaded verbatim (`registry_data.py`) and `registry_v2_data.py` adds annotations "
  "and new rows for every branch that landed later (O-BGIBBS final, F-SHARE REPORT, W7-SEP, W7-PART, W7-SEC, O-STAGES, O-DILUTE, F-SIGMA, "
  "O-VCERT, S-ELS, O-LS0, L-LEAN, F-REFEREE, W8-SYNTH, E-SPINE). Text processing only; nothing was recomputed and **no status was upgraded**: "
  "later same-family verdicts go in the same-family column only. Companion file: `LOCKABLE_v2.md`. Statement of record for Thm 5: `T38_STATEMENT.md` (v3). "
  "Reproduce with `python3 -I theory_campaign/T38-RECORD/build_registry_v2.py`.\n\n" % today)
w("**Cross-family reviews that landed during this rebuild** (all five are entered in the cross-family column; a re-review never raises an earlier adverse code on the original text, and the repair rows carry the re-review): "
  "A-REV5 (189770c; re-review of W6-FIXREV1/2 repairs, W4-T38FULL, W3-PXN, W3-PGD), A-REV6 (02d6a4a; post-A-REV4 repairs: W3-PXN, W4-SHARE, W2-T26, W2-BOOK/W5-LOCKBOOK, W7-PART, F-SHARE, O-BGIBBS, F-DRAFT, A-DRAFT), "
  "A-REV7 (70eadf3; no-LS0 masked theorem on LH: BG3, LH-lock, F1/F2, D2-LH, B2-LH, GU), A-REV8 (6417192; the LS0 route: LS-score, Lemma M, Thm b1, LH-LAT, W_Lat, W3-PXN P6/P7), "
  "A-REV9 (bbadda3; O-CERT, F-MASKPIP, O-PW2, O-DILUTE, W7-SEP, W7-PART, O-STAGES, O-WSTAB, O-SWAP, W7-SEC). Astra-authored new arguments are rows with author status REFEREE or an (A5)–(A9) suffix.\n\n")
w("**How to read the columns.** *Author status* is the status word the author wrote (PROVED / PROVED-UNDER = \"PROVED given/under named inputs\" / PROOF SKETCH / "
  "COUNTEREXAMPLE / CONJECTURE / OPEN / REFEREE = a repair or counterexample supplied by a cross-family referee without a PROVED label). "
  "*Same-family* = a campaign verifier run (Opus checking Opus). *Cross-family* = A-REV1–A-REV9 (Astra reviewers; A-REV5–A-REV9 landed during this rebuild); A-REV4 covers W2-BOOK (Lemma RO, Prop. 1–2) and F-DRAFT, and checks A-DRAFT §2 as Astra-on-Astra (recorded in the same-family column of those rows). "
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
w("Levels: XF = reviewed by A-REV1–A-REV9 (VERIFIED, clean or with a stated qualification); XF-ADVERSE = a cross-family GAP/ERROR stands on that row; SF = a campaign verifier run only; REFEREE-AUTHORED = written by a cross-family referee; UNVERIFIED = author only (includes same-family *authors* checking their own work).\n\n")
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

# ---- D2 data facts, F renames, G Lean, H referee, I decisions (v2)
w("## D2. Data facts (v2; not results, not counted)\n\n| Code | Fact | Source | Kind |\n|---|---|---|---|\n")
for c, s_, src, k in D.DATA:
    w("| `%s` | %s | %s | %s |\n" % (c, esc(s_), esc(src), esc(k)))
w("\n")

# ---- E. coverage
w("## E. Coverage: branches read and head SHAs\n\n")
w("Files matched: REPORT, REVIEW, REPAIRS, CARDS, STATEMENTS, ARCHITECTURE, plus REFEREE / CONSOLIDATED / NEW_TARGETS / T38_STATEMENT where a branch has no REPORT yet.\n\n")
w("| Branch | Head | Files read | Note |\n|---|---|---|---|\n")
for b, h, f in cov:
    w("| %s | `%s` | %s | %s |\n" % (b, h, ", ".join(esc(x) for x in f) or "—", esc(NOTES.get(b, ""))))
have = {b.split("/", 1)[1] for b, _, _ in cov}
expected = ["F-PXN"]
missing = [x for x in expected if x not in have]
w("\nNamed in the LEDGER but with no branch on origin at the last fetch: " + ", ".join("`theory/%s`" % x for x in missing)
  + " (F-PXN was cancelled). `theory/campaign` and smoke branches skipped. Re-run the builder after they land.\n")
w("\n## F. Proposed label renames (W8-SYNTH §4.15; proposals only, old labels stay valid citations)\n\n| Colliding label | Where | Proposed paper label |\n|---|---|---|\n")
for a, b, c in D.RENAMES:
    w("| %s | %s | %s |\n" % (esc(a), esc(b), esc(c)))
w("\n## G. Lean formalisation (L-LEAN)\n\n| Target | Registry rows | Lean names | Scope |\n|---|---|---|---|\n")
for a, b, c, d_ in D.LEAN:
    w("| %s | %s | %s | %s |\n" % (esc(a), esc(b), esc(c), esc(d_)))
w("\n" + D.LEAN_FIDELITY + "\n")
w("\n## H. F-REFEREE objections and their state\n\nRecommendation: major revision. Tags updated from W8-SYNTH §5 with O-LS0, E-SPINE and the in-flight reviews.\n\n| # | Objection | State |\n|---|---|---|\n")
for a, b, c in D.REFEREE:
    w("| %s | %s | %s |\n" % (a, esc(b), esc(c)))
w("\n## I. Decisions recorded (they change wording, never status)\n\n"
  "- **LS0 is part of the method**: approval in effect after O-LS0 (0/2,394 HPM changes; `theory/campaign · HQ/SR_AUDIT.md`; `E-SPINE · AMENDMENTS_20261102.md §2.1`).\n"
  "- **Spine**: 'moving off the start is needed', not 'tempering is needed' (`E-SPINE`, after W7-SEP Prop. GU).\n"
  "- **Common-σ² start rejected** (O-DILUTE §5, F-SIGMA Thm S6).\n"
  "- **n = 200 disclosure numbers corrected** (beta-min ≥ 43×, thresholds ≈ 2·10⁶, 0 search misses, 6 stops, no single 'favourable from n ≈' figure).\n"
  "- **Open:** output convention (strict 𝒪 vs 𝒪_H). Headline of Thm 5: W8-SYNTH's condition for a no-LS0 headline (A-REV7 verifies a route on an explicit family) is **met** by B2-LH on A-REV7's analytic subfamily; the choice is HQ's and Felipe's (T38_STATEMENT v3 Part IV, D2).\n")
open(os.path.join(HERE, "REGISTRY_v2.md"), "w", encoding="utf-8").write("".join(out))

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
w("# LOCKABLE v2 — candidates for locking (Felipe's adoption decision)\n\n")
w("Rebuilt by T38-RECORD on %s from `REGISTRY_v2.md` (same rule as S-REGISTRY LOCKABLE.md). **Rule** (strict): author status **PROVED** (not PROVED-UNDER) **and** same-family verdict VERIFIED "
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

w("## 2. REPAIRED, not yet re-reviewed (author PROVED + same-family VERIFIED; cross-family GAP/ERROR; repair written by W6-FIXREV1/2 or O-VCERT, not re-reviewed by a second family)\n\n")
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
w("Largest holes after A-REV5–A-REV9: the p ≫ n route (`PXN-P6`, `PXN-P7`, `PXN-Cor`, `VMASK-R1-NB`: XF GAP retained by A-REV6 and A-REV8); F-SHARE F2 (`FSH-F2`: XF GAP) and its c = 1 DOM exemption (ERROR); the stated cost rate (`Cost-T38`: XF GAP, log³ calibration factor); T32(i) itself (SF only; A-REV6 'supported', A-REV9 deferred); Prop 1 / Prop 2 / GUARD wording repairs (A-REV4, A-REV6 BOOK R1–R5: Astra candidates pending Claude); W7-SEC (A-REV9 deferred); O-STAGES and O-WSTAB beyond the rows A-REV9 named; and every Astra-authored repair (rows with author status REFEREE), which needs a Claude verification before it can count.\n\n")
w("## 4. Theorem 5 at a glance (from `T38_STATEMENT.md` v3, after A-REV5–A-REV9)\n\n"
  "| Part | Author status | SF | XF | Lockable under the rule? |\n|---|---|---|---|---|\n"
  "| (0) composition (`T38-(0)`) | PROVED | W3-VT38E | A-REV1 §7.4; A-REV5; A-REV8 | **yes — strict** |\n"
  "| (0_H) HPM convention | PROVED | none | A-REV5 (output interface VERIFIED) | no SF check |\n"
  "| (a) favourable (`T38-(a)`) | PROVED-UNDER (F) | inputs | inputs (EXP′) | no (conditional; ORTH joint PROOF SKETCH) |\n"
  "| (b1) Theorem b1 (`Thm-b1`) | PROVED-UNDER (M1)–(M3) | W5-VMASK | A-REV8, A-REV5 VERIFIED | conditional implication verified by both (§3d) |\n"
  "| LS-score, Lemma M, LH-LAT | PROVED | W5-VMASK | A-REV8 VERIFIED (LS-score move count ERROR at C₀ = S₀) | **yes — strict**, with the A-REV8 qualifications |\n"
  "| (b1-LH) (`T38-b1-LH`) | PROVED | W5-VMASK | A-REV8 VERIFIED; iid-failure clause ERROR/GAP (`T38-b1-LH-iidfail`) | **yes — strict**, without the iid-failure clause |\n"
  "| (b1-LH-iid) (`PXN-Cor`) | PROVED | W5-VMASK | GAP (A-REV3, A-REV6, A-REV8) | no |\n"
  "| (b1′) D2 route (`W6F1-D2inf`) | PROVED (implication) | — | A-REV5 VERIFIED | §3b (no independent SF check of the repair) |\n"
  "| (b1′-LH) D2-LH (`B2E-D2LH`) | PROVED-UNDER | none | A-REV7 VERIFIED qualitative; rate GAP | no SF check |\n"
  "| (b2) Gibbs-path interface (`W6F1-T38`) | PROVED (implication) | — | A-REV5 VERIFIED; D3 surrogate GAP | — |\n"
  "| (b2-LH) B2-LH (`B2E-B2LH`) | PROVED-UNDER STAB-LH | none | A-REV7 VERIFIED conditional | no SF check; STAB certificate and subfamily are Astra-authored (`STAB-cert(A7)`, `B2LH-subfamily(A7)`) |\n"
  "| BG3 / LH-lock (`OBG-BG3`, `OBG-LH-lock`) | PROVED / PROOF SKETCH | none | A-REV7 VERIFIED / VERIFIED conditional fixed-p; general locking ERROR | no SF check; status of LH-lock stays PROOF SKETCH |\n"
  "| F1 / F2 (`FSH-F1`, `FSH-F2`) | PROVED / PROOF SKETCH | none | A-REV7 VERIFIED / GAP | no |\n"
  "| GU (`SEP-GU`) | PROVED | none | A-REV7 VERIFIED (greedy); A-REV9 deferred | no SF check |\n"
  "| (c) cost (`Cost-T38`) | PROVED-UNDER T32(i) | W7-SEC (count) | A-REV5 GAP (qualification), A-REV6 GAP (rate) | no |\n\n")
w("## 5. The referees' own LOCKABLE recommendations (copied; recommendations, not adoptions)\n\n"
  "- **A-REV5:** (1) finite Theorem B with F′ and the CON §2 conventions, U′ bookkeeping, multi-target P; (2) Lemma S′, finite D2 with r*/NB′, D2-∞ with explicit rates; (3) E3′ with q < 1, centre emission, completed scans; (4) the T03♯ core and exact-tail lemmas; (5) Lemma T, POS-repaired A5, Lemma 0(b′), Prop. F, Lemma NT; (6) fixed-design EXP′ (0.51), deterministic-chain Theorems 3/4 with H3; (7) the U budget argument and C3 components; (8) T38's isolated conditional composition and b1′/b2 interfaces (not the whole T38 statement).\n"
  "- **A-REV6:** W4-SHARE D4/D5, SH(i)/(ii), G identity, M(a), product-form B2-W4; W3-PXN P1–P5, P8 in their restricted scope; W2-T26 Theorem A, conditional B, Lemmas 1–3; W2-BOOK fixed-data island-product identity and output Markov implication; F-DRAFT W1; A-DRAFT §2 A/A1/D/D1; W5-B2ENV M-LH; W7-PART Theorem B; F-SHARE F1 and O-BGIBBS BG3 as templates; O-WSTAB/O-DILUTE exact identities.\n"
  "- **A-REV7:** use B2-LH with an explicit verified stability condition (preferably the analytic certificate) as the no-LS0 masked theorem; D2-LH as a second qualitative c = 1 route; BG3 as a fixed-p component lemma; F1 as an abstract closure lemma. Do not cite F2 or GU alone as growing-p no-LS0 guarantees.\n"
  "- **A-REV8:** retain Thm 5(b1) as a conditional candidate for v3 + LS0 with the exact-Gram LH instance; correct the zero-distance move count, the c = 2 separation rate and GUARD's statistical-output scope.\n"
  "- **A-REV9:** O-CERT Lemma M, the deterministic Z_𝒯 inequality, C1(c), conditional C2, C3 ratios, exact C4 bounds, the strict-score C5 inclusion (initial list; see its final register).\n")
open(os.path.join(HERE, "LOCKABLE_v2.md"), "w", encoding="utf-8").write("".join(lk))

print("results", len(results), "claims", len(claims), "errors", len(err_rows), "gaps", len(gap_rows))
print("strict", len(strict), "after", len(after), "sf_only", len(sf_only), "xf_only", len(xf_only), "cex", len(cex), "cond", len(cond))
print({s: sum(matrix[s].values()) for s in STATUSES})
