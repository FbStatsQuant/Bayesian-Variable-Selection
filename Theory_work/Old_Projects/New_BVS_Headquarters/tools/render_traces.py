import json,sys,os
A=json.load(open(sys.argv[1],encoding='utf-8')); outdir=sys.argv[2]
ranges=[(1,0,208),(2,209,550),(3,551,807),(4,808,957),(5,958,1107),(6,1108,1238),(7,1239,1361),(8,1362,1676)]
KEEP_INPUT={'mcp__t3-code__delegate_task','mcp__t3-code__t3_thread_launch','mcp__t3-code__t3_thread_send','RemoteTrigger','mcp__t3-code__schedule_task','mcp__t3-code__task_cancel','mcp__t3-code__t3_thread_update','mcp__t3-code__link_pull_request','mcp__t3-code__t3_project_create','PushNotification'}
os.makedirs(outdir,exist_ok=True)
def run(i): return i['runId'].split(':')[-1] if i.get('runId') else '?'
for n,a,b in ranges:
    out=[f"# Tool and reasoning traces, part {n:02d}: positions {a}-{b}\n",
         "Companion to `../part_%02d_%d-%d.md`. It keeps, verbatim: the HQ assistant's reasoning items, subagent items, file_change diffs, and the inputs of orchestration tool calls (delegate_task, t3_thread_launch, t3_thread_send, RemoteTrigger and similar), which are the briefs and steering messages sent to other agents. Tool outputs are cut to 600 characters, and shell commands to their first 800 characters (command plus the start of its output). Read-only lookups (thread reads, searches, ToolSearch) appear as one line. Text between BEGIN/END markers is verbatim.\n" % (n,a,b)]
    for i in A:
        p=i['position']
        if not (a<=p<=b): continue
        t=i['type']; txt=i.get('text') or ''; ts=i.get('updatedAt'); tr=' (SOURCE ITEM TRUNCATED at 50000 chars)' if i.get('textTruncated') else ''
        hdr=f"\n### [pos {p}] {t} · run {run(i)} · {ts}{tr}\n"
        if t in ('reasoning','subagent','file_change','error','compaction','run_interrupt_request','run_interrupt_result','link_request','secret_request'):
            out.append(hdr+f"<!-- BEGIN pos {p} -->\n{txt}\n<!-- END pos {p} -->\n")
        elif t=='dynamic_tool':
            try: d=json.loads(txt)
            except Exception: d=None
            if d is None:
                out.append(hdr+f"(unparsable tool record, first 600 chars)\n<!-- BEGIN pos {p} -->\n{txt[:600]}\n<!-- END pos {p} -->\n")
            elif d.get('toolName') in KEEP_INPUT:
                o=json.dumps(d.get('output'),ensure_ascii=False)
                out.append(hdr+f"tool: `{d.get('toolName')}`\n\ninput (verbatim JSON):\n<!-- BEGIN pos {p} -->\n{json.dumps(d.get('input'),ensure_ascii=False,indent=1)}\n<!-- END pos {p} -->\n\noutput (first 600 chars): `{o[:600].replace('`','ʼ')}`\n")
            else:
                out.append(f"- [pos {p}] tool `{d.get('toolName')}` input: `{json.dumps(d.get('input'),ensure_ascii=False)[:300].replace('`','ʼ')}`\n")
        elif t=='command_execution':
            out.append(hdr+f"<!-- BEGIN pos {p} (first 800 chars) -->\n{txt[:800]}\n<!-- END pos {p} -->\n")
        elif t=='checkpoint':
            out.append(f"- [pos {p}] checkpoint: {txt[:1500]}\n")
        elif t=='notification':
            out.append(f"- [pos {p}] notification: {txt}\n")
    fn=os.path.join(outdir,f"traces_{n:02d}_{a}-{b}.md")
    open(fn,'w',encoding='utf-8',newline='\n').write(''.join(out))
    print(fn,os.path.getsize(fn))
