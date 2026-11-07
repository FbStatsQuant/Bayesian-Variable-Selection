import os, hashlib, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = os.path.join(ROOT, 'archive_final')
PURPOSE = {
 'README.md': 'What this archive is, source IDs, navigation, conventions, integrity checks, file index',
 'START_HERE.md': 'One-page current state of the theory, reading order, which file for what, fallback source IDs',
 'MANIFEST.md': 'Every file with size, purpose and sha256 (this file; its own checksum is not listed)',
 '01_overview_and_timeline.md': 'Arc of the thread by phase and date, ~95-row timeline, Felipe\'s standing rules, final state',
 '02_theory.md': 'Theory, Part A: final state: v3.1 setup (verbatim), paper-1 cards M1–M8 (TH01–TH08), supplements TH09–TH20, FW/drops/limitations/obligations, rulings, coverage',
 '02b_theory_campaign_history.md': 'Theory, Part B: campaign history: every result, conjecture, refutation, counterexample (TH/LM/CJ/RF/CE ≥101), 14 themes, dead ends, conflicts',
 'ID_REGISTRY.md': 'Every stable ID (parts A and B) with native names, kind, exact status, defining file, positions, and an alias index',
 'notation_and_conventions.md': 'Symbols, priors, parameterisations, the v3.1 settings table and (n,p) rules, convention changes, name collisions',
 '03_results_and_conclusions.md': 'Final theoretical and empirical results with numbers and files; conclusions, novelty, venue, confidence',
 '03b_reasoning_and_traces.md': 'Decision log (DEC), dead ends, reversals and corrections, reviewer findings, trace index',
 '04_code_and_files_index.md': 'Every branch, commit, PR, thread, worktree, machine path, script, result file and billing fact',
 '05_open_questions_and_next_steps.md': 'Pending approvals, FW items, obligations, open conflicts, engineering TODOs, next steps, infrastructure rules',
 'inputs/Local_to_Global_draft.txt': "Text of Felipe's first Local-to-Global proposal draft (sets mandatory theory goals §5.1–5.4, §13.1); copied from Owls ~/.config/bvs-hq/inputs/ (PDF on theory/campaign: theory_campaign/inputs/Local_to_Global_proposal.pdf)",
 'transcript/INDEX.md': 'Transcript index: parts, dates, runs, key positions, integrity notes',
 'branch_snapshots/SNAPSHOT_MANIFEST.txt': 'Map of every snapshot file to source ref@commit, path and sha256',
 'branch_snapshots/NONTEXT_INDEX.tsv': 'Index of non-text files on the theory branches and main@c4ef0dc Docs (not copied): path, bytes, git blob',
}
snapmap = {}
for line in open(os.path.join(F, 'branch_snapshots', 'SNAPSHOT_MANIFEST.txt'), encoding='utf-8'):
    m = re.match(r'^[0-9a-f]{64}\s+\d+\s+(\S+)\s+(\S+)\s+->\s+(\S+)', line)
    if m: snapmap[m.group(3)] = f'verbatim snapshot of {m.group(2)} at {m.group(1)}'
rows = []; total = 0
for dp, dns, fs in os.walk(F):
    dns.sort()
    for f in sorted(fs):
        p = os.path.join(dp, f); rel = os.path.relpath(p, F).replace('\\', '/')
        if rel == 'MANIFEST.md': continue
        data = open(p, 'rb').read(); total += len(data)
        if rel in PURPOSE: pur = PURPOSE[rel]
        elif rel.startswith('transcript/part_'):
            m = re.search(r'part_(\d+)_(\d+)-(\d+)', rel); pur = f'Verbatim transcript part {m.group(1)}: messages at positions {m.group(2)}–{m.group(3)}, plus one-line activity notes'
        elif rel.startswith('transcript/traces/'):
            m = re.search(r'traces_(\d+)_(\d+)-(\d+)', rel); pur = f'Verbatim reasoning, subagent, file-change and orchestration-tool-input traces, positions {m.group(2)}–{m.group(3)}'
        elif rel.startswith('tools/'): pur = 'Archive tooling (renderers, snapshotter, verifiers) used to build and check this archive'
        elif rel.startswith('branch_snapshots/'):
            pur = snapmap.get(rel, 'snapshot file (see SNAPSHOT_MANIFEST.txt)')
        else: pur = ''
        rows.append((rel, len(data), hashlib.sha256(data).hexdigest(), pur))
def fmt(n): return f'{n:,}'
top = [r for r in rows if not r[0].startswith('branch_snapshots/') or r[0] in PURPOSE]
snaps = [r for r in rows if r[0].startswith('branch_snapshots/') and r[0] not in PURPOSE]
out = ['# MANIFEST: every file in this archive\n',
       'Files: %d (including this manifest). Total bytes excluding MANIFEST.md: %s. Checksums: sha256. To verify, rebuild "sha256  path" pairs from the table rows and run `sha256sum -c` from the archive root (the archiving session did exactly this on Owls).\n' % (len(rows) + 1, fmt(total)),
       '## Documents, transcript and tools\n', '| path | bytes | sha256 | purpose |', '|---|---|---|---|']
out += [f'| {r[0]} | {fmt(r[1])} | {r[2]} | {r[3]} |' for r in top]
out += ['', f'## Branch snapshots ({len(snaps)} files)\n', '| path | bytes | sha256 | purpose |', '|---|---|---|---|']
out += [f'| {r[0]} | {fmt(r[1])} | {r[2]} | {r[3]} |' for r in snaps]
open(os.path.join(F, 'MANIFEST.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
# README file index
idx = ['| file | bytes | purpose |', '|---|---|---|']
for r in top: idx.append(f'| `{r[0]}` | ' + ('(this file)' if r[0]=='README.md' else fmt(r[1])) + f' | {r[3]} |')
sb = sum(r[1] for r in snaps)
idx.append(f'| `branch_snapshots/` ({len(snaps)} files in {len({r[0].split("/")[1] for r in snaps})} folders) | {fmt(sb)} | Verbatim theory texts of every `theory/*` branch, `campaign`, `E-SPINE` (PR #1) and `main@c4ef0dc/Docs` |')
idx.append(f'| `MANIFEST.md` | (see file) | {PURPOSE["MANIFEST.md"]} |')
rd = open(os.path.join(F, 'README.md'), encoding='utf-8').read()
rd = re.sub(r'<!-- FILE_INDEX_START -->.*<!-- FILE_INDEX_END -->', '<!-- FILE_INDEX_START -->\n' + '\n'.join(idx) + f'\n\nTotal size: about {total/1e6:.1f} MB (text only); exact sizes and checksums in MANIFEST.md.\n<!-- FILE_INDEX_END -->', rd, flags=re.S)
open(os.path.join(F, 'README.md'), 'w', encoding='utf-8', newline='\n').write(rd)
print('rows', len(rows), 'total', total)
