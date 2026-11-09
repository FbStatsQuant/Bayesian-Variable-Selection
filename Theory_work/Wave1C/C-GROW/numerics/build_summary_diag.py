"""assembles SUMMARY_DIAG.md from findings_diag.md (hand-written), notes_diag.md (hand-written) and the generated D*_summary.md files"""
import subprocess, sys, datetime
for s in ("build_diag.py", "build_growth.py", "build_pooled.py"):
    subprocess.run([sys.executable, s], capture_output=True)
try:
    subprocess.run([sys.executable, "d4_post.py"], capture_output=True)
except Exception as e:
    print(e)
rd = lambda f: open(f).read()
out = "# C-GROW diagnostics (SUMMARY_DIAG) -- test sub-agent, assembled %s\n\n" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
out += rd("findings_diag.md") + "\n---\n\n" + rd("notes_diag.md") + "\n---\n\n"
out += rd("D1_summary.md") + "\n" + rd("D3_growth_summary.md").split("## D1 supplement")[1].join(["### D1 supplement", ""]) if False else ""
out += rd("D1_summary.md") + "\n"
g = rd("D3_growth_summary.md"); i = g.index("## D1 supplement")
out += "### " + g[i + 3:] + "\n\n---\n\n"
out += rd("D2_summary.md") + "\n---\n\n" + rd("D3_summary.md") + "\n" + g[:i].replace("## D3 growth", "### D3d growth") + "\n" + rd("D3_blocks_summary.md").replace("## D3 add-on", "### D3e add-on") + "\n---\n\n"
out += rd("D4_summary.md") + "\n---\n\n" + rd("POOLED.md")
open("SUMMARY_DIAG.md", "w").write(out)
print(len(out))
