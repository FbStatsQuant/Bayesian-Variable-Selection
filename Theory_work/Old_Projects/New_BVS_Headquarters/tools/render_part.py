"""Render a verbatim transcript part from saved t3_thread_read JSON pages.
Usage: python -I render_part.py OUT.md PARTNUM START END page1.json [page2.json ...]
Pages may be messages-view or activity-view saves; items are merged by position."""
import json, sys, re, os
out, partnum, a, b = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
items = {}
for f in sys.argv[5:]:
    d = json.load(open(f, encoding='utf-8'))
    for i in d['items']:
        p = i['position']
        if a <= p <= b:
            # prefer the copy with the longest text (untruncated)
            if p not in items or len(i.get('text') or '') > len(items[p].get('text') or ''):
                items[p] = i
WRITE_PAT = re.compile(r"(cat\s*>|>>?\s*[\w/~$.\"']|\btee\b|git (commit|push|add|checkout -b|branch|merge|rebase|reset|tag)|\bcp\b|\bmv\b|\brm\b|sed -i|mkdir|scp\b|rsync\b|Write\(|apply_patch)")
def run(i): return i['runId'].split(':')[-1] if i.get('runId') else '?'
lines = []
nmsg = 0; trunc = []
pos_sorted = sorted(items)
lines.append(f"# Transcript part {partnum:02d}: positions {a}-{b}\n")
lines.append("Source: T3 thread \"New BVS Headquarters\" `5e38497d-7dfd-48f9-88e9-b21895922f58`, environment `b18966a3-98dd-4510-a488-d5dfb1650daa` (Owls).\n")
lines.append("Message text between `<!-- BEGIN pos N -->` and `<!-- END pos N -->` is copied verbatim from `t3_thread_read`. Timestamps are the item's `updatedAt` (UTC). Tool activity is summarised in `> activity` lines; file writes and changes are recorded with their paths.\n")
body = []
for p in pos_sorted:
    i = items[p]; t = i['type']; txt = i.get('text') or ''
    if i.get('textTruncated') and t in ('user_message', 'assistant_message'): trunc.append(p)
    if t in ('user_message', 'assistant_message'):
        nmsg += 1
        role = 'USER' if t == 'user_message' else 'ASSISTANT'
        extra = ''
        if t == 'user_message' and i.get('creationSource') == 'mcp':
            extra = f" · sent via MCP" + (f" by thread `{i['senderThreadId']}`" if i.get('senderThreadId') else '') + " (not typed by the user)"
        if i.get('messageId','') and str(i.get('messageId')).startswith('scheduled-task-message'):
            extra += " · scheduled-task wake-up message"
        body.append(f"\n---\n\n### [pos {p}] {role} · run {run(i)} · {i.get('updatedAt')}{extra}\n<!-- itemId: {i['itemId']} -->\n<!-- BEGIN pos {p} -->\n{txt}\n<!-- END pos {p} -->\n")
    elif t == 'file_change':
        path = txt.split('\n', 1)[0].strip()
        body.append(f"> activity [pos {p}] FILE CHANGE: `{path}`\n")
    elif t == 'checkpoint':
        try:
            arr = json.loads(txt)
            desc = '; '.join(f"{x.get('kind')} `{x.get('path')}` (+{x.get('additions')}/-{x.get('deletions')})" for x in arr)
        except Exception:
            desc = txt[:300].replace('\n', ' ')
        body.append(f"> activity [pos {p}] CHECKPOINT (files changed in workspace): {desc}\n")
    elif t == 'command_execution':
        first = txt.split('\n', 1)[0]
        head = txt[:1500]
        mm = WRITE_PAT.search(head)
        if mm:
            s0 = max(0, mm.start() - 60); snip = head[s0:mm.end() + 120].replace('\n', ' / ')
            body.append(f"> activity [pos {p}] COMMAND (may write files / change git state): `{first[:200].replace('`','ʼ')}` ... matched: `{snip.replace('`','ʼ')}`\n")
        else:
            body.append(f"> activity [pos {p}] command: `{first[:160].replace('`','ʼ')}`\n")
    elif t == 'dynamic_tool':
        m = re.search(r'"toolName":\s*"([^"]+)"', txt)
        body.append(f"> activity [pos {p}] tool call: {m.group(1) if m else 'unknown'}\n")
    elif t == 'reasoning':
        body.append(f"> activity [pos {p}] (assistant reasoning, {len(txt)} chars, not transcribed)\n")
    else:
        body.append(f"> activity [pos {p}] {t}: {(i.get('title') or txt[:160]).replace(chr(10),' ')}\n")
first = pos_sorted[0] if pos_sorted else None; last = pos_sorted[-1] if pos_sorted else None
lines.append(f"Items in range: {len(pos_sorted)} (first pos {first}, last pos {last}); user/assistant messages: {nmsg}.\n")
if trunc: lines.append(f"WARNING: items still truncated in source pages: {trunc}\n")
open(out, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines) + ''.join(body))
print('wrote', out, 'items', len(pos_sorted), 'messages', nmsg, 'first', first, 'last', last, 'truncated', trunc)
