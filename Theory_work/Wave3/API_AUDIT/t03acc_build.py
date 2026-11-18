"""Build the blind Fable audit of T03-sharp (SOP:TH09) for W3-T03ACC (HQ, 2026-11-15). Two independent samples."""
import json, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import audit_batch as ab
ROOT = Path(__file__).resolve().parents[3]
def show(rev, p): return subprocess.run(["git", "-C", str(ROOT), "show", f"{rev}:{p}"], capture_output=True, text=True, encoding="utf-8").stdout
def num(t): return "\n".join(f"{i:5d}  {l}" for i, l in enumerate(t.splitlines(), 1))
files = [(f"theory_campaign/W1-T03R/{n} @7e14d6f", show("7e14d6f", f"theory_campaign/W1-T03R/{n}")) for n in ("PROOF.md", "REPORT.md", "NOTES.md")]
for p in ["Docs/Theory/proofs/T01_T02_contrast_dimension/PROOF_v3.tex", "Docs/Theory/proofs/T03_A2_selection_consistency/PROOF_v2.tex",
          "Docs/Theory/proofs/T03_A2_selection_consistency/STATEMENT.md", "Docs/Theory/theorems/T03_A2_selection_consistency.md"]:
    files.append((p, (ROOT / p).read_text(encoding="utf-8")))
rows = (ROOT / "Theory_work/State_of_Project/registry/theory_main.tsv").read_text(encoding="utf-8").splitlines()
files.append(("Theory_work/State_of_Project/registry/theory_main.tsv (header + line 68)", rows[0] + "\n" + rows[67]))
ctx = "<files>\n" + "\n\n".join(f'<file path="{p}">\n{num(t)}\n</file>' for p, t in files) + "\n</files>"
task = ("Audit this registered claim: SOP:TH09 = Theorem T03-sharp (posterior concentration 1 - pi(S0) = O_P(sqrt(log n/n)) "
        "under R1, G, R, SE_lambda, SE_w, BM; exact HPM and MPM consistent; large-signal inclusion without beta-min), statement "
        "in theory_main.tsv line 68 and its proof in theory_campaign/W1-T03R/PROOF.md (building on [P1] T01_T02 PROOF_v3 and "
        "[P3] T03_A2 PROOF_v2). Check every step line by line; for each consumed result say whether its stated hypotheses are met. "
        "Report each issue with severity FATAL/MAJOR/MINOR and file:line.")
reqs = []
for k in (1, 2):
    reqs.append({"custom_id": f"t03acc-{k}", "file": "SOP:TH09", "claims": ["SOP:TH09"], "params": {
        "model": ab.MODEL, "max_tokens": 64000, "output_config": {"effort": "high"}, "system": ab.SYSTEM,
        "messages": [{"role": "user", "content": [{"type": "text", "text": ctx, "cache_control": {"type": "ephemeral"}},
                                                  {"type": "text", "text": task}]}]}})
out = Path(__file__).parent / "t03acc"
(out / "requests.json").write_text(json.dumps(reqs, ensure_ascii=False), encoding="utf-8")
print(len(reqs), "requests;", sum(len(t) for _, t in files), "chars of context")
