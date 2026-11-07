# State of the Project (SMC-BVS)

The unified, versioned record of where the SMC-BVS project stands: method v3.1, all empirical results, the approved
paper-1 theorem targets (exact statements, per-clause status), the work done and the open problems. It is the
starting point of the agentic theory loop. **Read `State_of_Project_v1.0.pdf` (agent brief on page 1).**

| Path | What |
|---|---|
| `State_of_Project_v<version>.pdf` | the compiled document |
| `main.tex`, `preamble.tex`, `sections/*.tex` | LaTeX sources (LuaLaTeX) |
| `registry/*.tsv` | machine-readable registry of every stable ID (status verbatim, checks, regime, dependencies, open items, sources) |
| `tables/` | generated tables (`scripts/make_tables.py`, `scripts/registry_to_tex.py`) — do not edit by hand |
| `figures/` | figures |
| `scripts/build.sh` | full build + checks (Windows Git Bash, MiKTeX LuaLaTeX; Cambria / Segoe UI Symbol fonts) |
| `scripts/check.py` | fidelity checks: sources resolve and are unchanged since commit 21ebc28, IDs resolve, registry statuses = archive registry, coverage, no dropped glyphs |
| `scripts/check_section.sh` | compile and check one section in isolation |
| `AUTHORING.md` | binding authoring rules for agents (verbatim statements and statuses, citations, ID ownership) |
| `review/RUBRIC.md` | council review rubric; `review/QUESTION_BANK*.md` evaluation questions; `review/rounds/` review records |
| `checks/` | generated check outputs (coverage report, previews) |

Sources: the theory-campaign archive `Theory_work/Old_Projects/New_BVS_Headquarters/` (NBH) and the repository
results, frozen at commit 21ebc28. Build: `bash Theory_work/State_of_Project/scripts/build.sh`.
