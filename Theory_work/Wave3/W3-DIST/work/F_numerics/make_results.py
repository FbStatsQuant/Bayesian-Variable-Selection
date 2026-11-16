import sys; sys.dont_write_bytecode = True
parts = [open("RESULTS_head.md").read()]
parts.append("# Tables\n\n## Items 1 and 6b\n" + open("out/analysis_item1_6b.md").read() + "\n\n### Item 1 extras (log-slopes, t̂_c, relation to π(S₀))\n```\n" + open("out/item1_extra.txt").read() + "```\n")
parts.append("\n" + open("out/analysis_item2.md").read() + "\n\n" + open("out/analysis_item3.md").read() + "\n\n" + open("out/analysis_item4.md").read() + "\n\n" + open("out/analysis_item5.md").read())
parts.append("\n\n## Item 6a — Lemma V re-check (output of `item6a_lemmaV.py`)\n```\n" + open("out/item6a_out.txt").read() + "```\nThe unchanged helper script `../prior_probe/probe_checks.py` re-run: identical to `../prior_probe/probe_checks_out.txt` (C3: max Δ − rhs = −1.532·10⁻³, min eig D′ = −2.6·10⁻¹⁵, log-bound margin −0.094; C4 size laws unchanged).\n")
parts.append("\n## Item 7 — citecheck (output of `citecheck.py`)\n" + open("out/citecheck_out.txt").read())
open("RESULTS.md", "w").write("".join(parts))
