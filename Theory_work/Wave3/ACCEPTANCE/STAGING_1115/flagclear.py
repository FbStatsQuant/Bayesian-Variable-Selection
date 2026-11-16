"""Clear every headline=yes flag (HQ 4(a), consultant AGREE) and write registry/HEADLINE_CANDIDATES.md. python flagclear.py <root>"""
import os, re, subprocess, sys
root = sys.argv[1]; os.chdir(root)
T = "Theory_work/INFRA/tools"; sys.path.insert(0, T); sys.dont_write_bytecode = True
import bvsreg as R  # noqa: E402

CARD = "/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/CLAIMS_CARD.md"
card = {}
for ln in open(CARD, encoding="utf-8"):
    m = re.match(r"^\|\s*([0-9]\.[0-9])(?:\s*\(([^)]*)\))?\s*\|", ln)
    if not m:
        continue
    label = m.group(1) + (f" ({m.group(2)})" if m.group(2) else "")
    cells = ln.split("|")
    notheadline = "not headline" in cells[2]
    for tok in re.findall(r"`([A-Z0-9-]+:[^`@]+)@", ln):
        tk, _, loc = tok.partition(":")
        for l_ in loc.split("/"):
            cid = f"{tk}:{l_}"
            card.setdefault(cid, []).append(label + (" [card: not headline]" if notheadline else ""))
rows = [r for r in R.load_claims() if r.get("headline") == "yes"]
print(len(rows), "flagged rows")


def pending(g):
    out = []
    for k in ("lit", "necessity", "better"):
        if re.search(rf"(?<![\w-]){k}:PASS\(", g):
            continue
        m = re.search(rf"(?<![\w-]){k}:([A-Z-]+)(\(([^)]*)\))?", g)
        out.append(f"{k}:{m.group(1)}" + (f" ({m.group(3)[:60]})" if m and m.group(3) else "") if m else f"{k}: not recorded")
    if re.search(r"better-proposal:", g) and "better:PASS" not in g:
        out.append("better-proposals recorded (dispositions in gates)")
    return "; ".join(out) or "none (all three PASS)"


lines = ["# Headline candidates (registry; HQ 2026-11-15, PROTOCOL_v4 H5 card on tool-set flags, consultant AGREE)", "",
         "**Citation rule.** A row may be cited as a pillar in the reader card, a chapter or the paper only when it is "
         "`headline=yes` in `claims.tsv` with its strength gates run (`lit:`, `necessity:`, `better:` — LIFECYCLE §4.2). "
         "Until the owner's headline list is set, any supersession or statement change on a row below needs an H5 card "
         "through HQ.", "",
         "All 44 `headline=yes` flags were cleared on 2026-11-15 (they were tool-set at seeding / ingest, or set on "
         "today's H5 cards for RM2-F/R and MISR). Each row below is a checked-intermediate or unchecked claim whose "
         "headline admission is pending; the flag returns when its strength gates run and the owner's list includes it. "
         "Card = W3-READER `CLAIMS_CARD.md` v0.2 row(s) citing the id (pillar.item (Thm k)); `—` = not on the card.", "",
         "| id@version | ticket | card row | strength gates pending (from `gates`) | status (verbatim, first 70 chars) |",
         "|---|---|---|---|---|"]
for r in rows:
    lines.append(f"| {r['id']}@{r['version']} | {r['ticket']} | {', '.join(card.get(r['id'], [])) or '—'} | "
                 f"{pending(r.get('gates', '')).replace('|', '/')} | {r['status'][:70].replace('|', '/')} |")
oncard = sorted(set(card) - {r['id'] for r in rows})
lines += ["", f"Card ids that carry no flag today (not cleared, listed for completeness): {', '.join(oncard)}.", ""]
open("Theory_work/INFRA/registry/HEADLINE_CANDIDATES.md", "w", encoding="utf-8").write("\n".join(lines))
for r in rows:
    p = subprocess.run([sys.executable, f"{T}/registry.py", "set", r["id"], "headline=",
                        f"--reason", "HQ 4(a) 2026-11-15 (H5 card, consultant AGREE): tool-set headline flag cleared; "
                        "headline admission pending; see registry/HEADLINE_CANDIDATES.md"], capture_output=True, text=True)
    if p.returncode:
        sys.exit(f"STOP {r['id']}: {p.stderr[-300:]}")
print("cleared", len(rows), "; on card:", sum(1 for r in rows if r['id'] in card))
print("ids:", "; ".join(r["id"] for r in rows))
