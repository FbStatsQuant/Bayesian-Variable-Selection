# Archive: "New BVS Headquarters" (SMC-BVS theory campaign, 2026-11-02 → 2026-11-04)

## What this is

This folder is a permanent, text-only archive of the T3 thread **"New BVS Headquarters"**. It was made so the thread and the duplicate T3 projects it lives in can be deleted without losing anything. The next thread, **"Theory Meta HQ"**, is meant to continue the theoretical work from this archive alone. **New agents: read `START_HERE.md` first.**

| | |
|---|---|
| Source thread | "New BVS Headquarters", threadId `5e38497d-7dfd-48f9-88e9-b21895922f58` |
| Machine / environment | Owls (`owls.stat.rice.edu`, user `fb31`), T3 environmentId `b18966a3-98dd-4510-a488-d5dfb1650daa`, project `58858238-933d-4ae9-bac2-213d20df8897` |
| Size of thread | 1,677 timeline items (positions 0–1676); 440 user and assistant messages; 181 runs (run 182 queued and never started) |
| Date range | 2026-11-02T14:40Z → 2026-11-04T15:16Z |
| Working dir / branch | `/home/fb31/BVS_GH/Bayesian-Variable-Selection` (now gone), branch `theory/campaign`. The repo now lives at `/home/fb31/Bayesian-Variable-Selection` on Owls |
| GitHub | `FbStatsQuant/Bayesian-Variable-Selection`; PR #1 https://github.com/FbStatsQuant/Bayesian-Variable-Selection/pull/1 (`theory/E-SPINE`, unmerged at thread end); 84 `origin/theory/*` branches |
| Model / account | HQ ran on Claude Opus 5.5, Claude Personal account. Delegates ran on Opus/Fable/Sonnet/Haiku (CP, CW, cloud, API) and Astra/Sol (Codex) |
| Archived on | 2026-11-04, by an archiving session (Claude Opus 5.5) with Haiku transcript agents and Sonnet drafting agents |

The thread began as a question about spending credits and deploying through T3 [pos 0]. It grew into the SMC-BVS theory campaign: about 100 agent instances, 8 cloud waves, Astra cross-family reviews, API-credit runs and a literature phase. A methodology meeting fixed method v3.1, and a theorem meeting fixed the paper-1 list (8 main and 12 supplement cards). See `01_overview_and_timeline.md`.

## How to navigate

- **Orientation:** `START_HERE.md` (one-page state plus reading order) → `05_open_questions_and_next_steps.md`.
- **Theory:**
  - `02_theory.md` is the final state, with verbatim statements and IDs TH01–TH22 and so on.
  - `02b_theory_campaign_history.md` is the full campaign history (IDs ≥ 101).
  - `ID_REGISTRY.md` is the lookup table and alias index.
  - `notation_and_conventions.md` covers symbols, settings and changed conventions.
- **Results:** `03_results_and_conclusions.md`.
- **Reasoning:** `03b_reasoning_and_traces.md` covers decisions, dead ends, reversals, reviewer findings and a trace index.
- **Artifacts:** `04_code_and_files_index.md` lists branches, paths, scripts, threads and billing facts.
- **Primary sources:**
  - `transcript/`: verbatim messages plus traces. Start at `transcript/INDEX.md`.
  - `inputs/Local_to_Global_draft.txt`: Felipe's first proposal draft as text. Its goals (§5.1–5.4, §13.1) are mandatory for paper 1 [pos 1144], [pos 1150]. The Song–Liang (2015) PDF is not copied; it is on `theory/campaign` at `theory_campaign/inputs/SongLiang2015.pdf`.
  - `branch_snapshots/`: verbatim .md/.tex/.lean from every `theory/*` branch and the pre-campaign `Docs/` at main@c4ef0dc. `SNAPSHOT_MANIFEST.txt` maps each file to its ref, path and sha256. `NONTEXT_INDEX.tsv` indexes the non-text files that were not copied (csv/json/pdf/py/npz…) by path, size and git blob.

### Conventions used in every document

- **Positions:** `[pos N]` is a position in the source thread. Find it in `transcript/part_*.md` with `grep -n "BEGIN pos N "`.
- **IDs:** stable archive IDs, always written with the native name (e.g. `TH05 (M5 Theorem HPM)`, `TH262 (Theorem A)`). There are two ID spaces: two-digit IDs for the final state, three-digit (≥ 101) for the campaign history (see `ID_REGISTRY.md`). Shorthand inside the docs:
  - "02a" = `02_theory.md`;
  - "02b" = `02b_theory_campaign_history.md`;
  - "REG-A"/"REG-B" = parts A and B of `ID_REGISTRY.md`;
  - "TLF" = `branch_snapshots/MEET-THM/THEOREM_LIST_FINAL.md`;
  - "METH31" = `MEET-v31/METHOD_v3.1_FINAL.md`.
- **Statuses** are copied from the sources and never upgraded. **UNCERTAIN:** marks conflicts between sources.
- **Verbatim vs summary:** verbatim text sits in blockquotes or `BEGIN VERBATIM` blocks with the source file named; everything else is labelled "Summary:" or is editorial. Quotes that are not byte-identical to their source carry a fidelity note or a visible "⚠ FIDELITY FLAG". In those cases the snapshot file is authoritative. In the narrative docs (01, 03, 03b, 05), quotation marks sometimes enclose a short status string or a lightly trimmed phrase; the `[pos N]` or file citation next to it is authoritative.
- **Math:** Markdown with LaTeX or the sources' Unicode math, as filed.

### What is deliberately NOT included (indexed instead)

- Datasets, simulation outputs, fit bundles and binaries: they are on NOTS and the laptop, indexed in `04_code_and_files_index.md` and `branch_snapshots/NONTEXT_INDEX.tsv`.
- Full tool outputs: kept only where they carry theory or results, otherwise summarised in one line.
- Secrets: the GitHub token and API key exist on Owls under `~/.config/bvs-hq/`. Their values never appear in this archive.

## Integrity checks performed

1. **Transcript:**
   - All 440 messages were fetched twice, independently: once by the archiving HQ and once by the 8 per-part transcript agents.
   - The two fetches match character for character, and all 1,677 positions are covered.
   - No message hit the 50,000-character read limit.
   - The last page of part 8 was re-fetched by the archiving HQ after the agent could not save it.
2. **Snapshots:** every file was copied by `git cat-file` from the `origin/theory/*` tips, with its sha256 recorded in `branch_snapshots/SNAPSHOT_MANIFEST.txt`. The copy on Owls was checked against `MANIFEST.md` after upload.
3. **Quotes:**
   - Part A: 97/99 `BEGIN VERBATIM` blocks byte-identical (the other 2: an explanatory line and one elided "[…]" quote).
   - Part B: 925 + 54 of 1,091 blockquotes identical (byte or line), 55 notation transliterations (coverage ≥ 0.98), 57 flagged.
   - Inline quotations in the narrative docs were checked against the transcript and snapshots. Misquotes found were corrected, including an invented error message for the final failed runs, which is now replaced by the real "workspace folder no longer exists" error.
4. **Secret scan:** no token or key pattern anywhere in the archive.
5. **Size and checksums:** `MANIFEST.md` lists every file with its size and sha256.

## File index

<!-- FILE_INDEX_START -->
| file | bytes | purpose |
|---|---|---|
| `01_overview_and_timeline.md` | 50,822 | Arc of the thread by phase and date, ~95-row timeline, Felipe's standing rules, final state |
| `02_theory.md` | 305,447 | Theory, Part A: final state: v3.1 setup (verbatim), paper-1 cards M1–M8 (TH01–TH08), supplements TH09–TH20, FW/drops/limitations/obligations, rulings, coverage |
| `02b_theory_campaign_history.md` | 2,687,506 | Theory, Part B: campaign history: every result, conjecture, refutation, counterexample (TH/LM/CJ/RF/CE ≥101), 14 themes, dead ends, conflicts |
| `03_results_and_conclusions.md` | 62,491 | Final theoretical and empirical results with numbers and files; conclusions, novelty, venue, confidence |
| `03b_reasoning_and_traces.md` | 60,642 | Decision log (DEC), dead ends, reversals and corrections, reviewer findings, trace index |
| `04_code_and_files_index.md` | 81,542 | Every branch, commit, PR, thread, worktree, machine path, script, result file and billing fact |
| `05_open_questions_and_next_steps.md` | 38,271 | Pending approvals, FW items, obligations, open conflicts, engineering TODOs, next steps, infrastructure rules |
| `ID_REGISTRY.md` | 695,920 | Every stable ID (parts A and B) with native names, kind, exact status, defining file, positions, and an alias index |
| `README.md` | (this file) | What this archive is, source IDs, navigation, conventions, integrity checks, file index |
| `START_HERE.md` | 7,917 | One-page current state of the theory, reading order, which file for what, fallback source IDs |
| `notation_and_conventions.md` | 94,871 | Symbols, priors, parameterisations, the v3.1 settings table and (n,p) rules, convention changes, name collisions |
| `branch_snapshots/NONTEXT_INDEX.tsv` | 217,702 | Index of non-text files on the theory branches and main@c4ef0dc Docs (not copied): path, bytes, git blob |
| `branch_snapshots/SNAPSHOT_MANIFEST.txt` | 236,356 | Map of every snapshot file to source ref@commit, path and sha256 |
| `inputs/Local_to_Global_draft.txt` | 25,629 | Text of Felipe's first Local-to-Global proposal draft (sets mandatory theory goals §5.1–5.4, §13.1); copied from Owls ~/.config/bvs-hq/inputs/ (PDF on theory/campaign: theory_campaign/inputs/Local_to_Global_proposal.pdf) |
| `tools/BRIEF_COMMON.md` | 4,954 | Archive tooling (renderers, snapshotter, verifiers) used to build and check this archive |
| `tools/fidelity.py` | 4,640 | Archive tooling (renderers, snapshotter, verifiers) used to build and check this archive |
| `tools/flag_fidelity.py` | 4,002 | Archive tooling (renderers, snapshotter, verifiers) used to build and check this archive |
| `tools/make_index.py` | 7,998 | Archive tooling (renderers, snapshotter, verifiers) used to build and check this archive |
| `tools/make_manifest.py` | 5,827 | Archive tooling (renderers, snapshotter, verifiers) used to build and check this archive |
| `tools/render_part.py` | 4,389 | Archive tooling (renderers, snapshotter, verifiers) used to build and check this archive |
| `tools/render_traces.py` | 3,118 | Archive tooling (renderers, snapshotter, verifiers) used to build and check this archive |
| `tools/show.py` | 528 | Archive tooling (renderers, snapshotter, verifiers) used to build and check this archive |
| `tools/snap_all.py` | 2,204 | Archive tooling (renderers, snapshotter, verifiers) used to build and check this archive |
| `tools/verify.py` | 1,286 | Archive tooling (renderers, snapshotter, verifiers) used to build and check this archive |
| `tools/verify_inline.py` | 1,484 | Archive tooling (renderers, snapshotter, verifiers) used to build and check this archive |
| `tools/verify_quotes.py` | 1,511 | Archive tooling (renderers, snapshotter, verifiers) used to build and check this archive |
| `tools/verify_verbatim.py` | 1,763 | Archive tooling (renderers, snapshotter, verifiers) used to build and check this archive |
| `transcript/INDEX.md` | 8,215 | Transcript index: parts, dates, runs, key positions, integrity notes |
| `transcript/part_01_0-208.md` | 69,132 | Verbatim transcript part 01: messages at positions 0–208, plus one-line activity notes |
| `transcript/part_02_209-550.md` | 116,943 | Verbatim transcript part 02: messages at positions 209–550, plus one-line activity notes |
| `transcript/part_03_551-807.md` | 78,170 | Verbatim transcript part 03: messages at positions 551–807, plus one-line activity notes |
| `transcript/part_04_808-957.md` | 68,988 | Verbatim transcript part 04: messages at positions 808–957, plus one-line activity notes |
| `transcript/part_05_958-1107.md` | 73,232 | Verbatim transcript part 05: messages at positions 958–1107, plus one-line activity notes |
| `transcript/part_06_1108-1238.md` | 62,232 | Verbatim transcript part 06: messages at positions 1108–1238, plus one-line activity notes |
| `transcript/part_07_1239-1361.md` | 60,663 | Verbatim transcript part 07: messages at positions 1239–1361, plus one-line activity notes |
| `transcript/part_08_1362-1676.md` | 98,020 | Verbatim transcript part 08: messages at positions 1362–1676, plus one-line activity notes |
| `transcript/traces/traces_01_0-208.md` | 92,548 | Verbatim reasoning, subagent, file-change and orchestration-tool-input traces, positions 0–208 |
| `transcript/traces/traces_02_209-550.md` | 251,564 | Verbatim reasoning, subagent, file-change and orchestration-tool-input traces, positions 209–550 |
| `transcript/traces/traces_03_551-807.md` | 253,888 | Verbatim reasoning, subagent, file-change and orchestration-tool-input traces, positions 551–807 |
| `transcript/traces/traces_04_808-957.md` | 72,199 | Verbatim reasoning, subagent, file-change and orchestration-tool-input traces, positions 808–957 |
| `transcript/traces/traces_05_958-1107.md` | 82,884 | Verbatim reasoning, subagent, file-change and orchestration-tool-input traces, positions 958–1107 |
| `transcript/traces/traces_06_1108-1238.md` | 84,008 | Verbatim reasoning, subagent, file-change and orchestration-tool-input traces, positions 1108–1238 |
| `transcript/traces/traces_07_1239-1361.md` | 54,627 | Verbatim reasoning, subagent, file-change and orchestration-tool-input traces, positions 1239–1361 |
| `transcript/traces/traces_08_1362-1676.md` | 262,391 | Verbatim reasoning, subagent, file-change and orchestration-tool-input traces, positions 1362–1676 |
| `branch_snapshots/` (1133 files in 84 folders) | 20,449,223 | Verbatim theory texts of every `theory/*` branch, `campaign`, `E-SPINE` (PR #1) and `main@c4ef0dc/Docs` |
| `MANIFEST.md` | (see file) | Every file with size, purpose and sha256 (this file; its own checksum is not listed) |

Total size: about 26.9 MB (text only); exact sizes and checksums in MANIFEST.md.
<!-- FILE_INDEX_END -->
