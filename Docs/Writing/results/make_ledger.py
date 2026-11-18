"""Generate status_ledger.tex (D2 Appendix C) from STATUS_LEDGER.md. Registry strings are kept verbatim (escaped)."""
import re, sys
md = open('STATUS_LEDGER.md', encoding='utf-8').read().splitlines()
rows = [l for l in md if l.startswith('| ') and not l.startswith('| Result (reader') and not l.startswith('|---')]
UNI = {'♯': r'$\sharp$', '′': "$'$", '…': r'\ldots{}', '–': '--', '—': '---', '⇒': r'$\Rightarrow$', '≤': r'$\le$',
       '→': r'$\to$', '⁶': r'$^6$', '⁴': r'$^4$', '⁵': r'$^5$', '≥': r'$\ge$', '“': '``', '”': "''"}
def esc(t):
    out = []
    for i, seg in enumerate(re.split(r'(\$[^$]*\$)', t)):
        if i % 2 == 1:
            out.append(seg); continue
        seg = seg.replace('\\', r'\textbackslash{}')
        for a, b in [('&', r'\&'), ('%', r'\%'), ('#', r'\#'), ('_', r'\_'), ('{', r'\{'), ('}', r'\}'),
                     ('~', r'\textasciitilde{}'), ('^', r'\textasciicircum{}')]:
            seg = seg.replace(a, b)
        seg = seg.replace(r'\textbackslash\{\}', r'\textbackslash{}')
        seg = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', seg)
        seg = re.sub(r'`([^`]*)`', r'\\texttt{\1}', seg)
        for a, b in UNI.items():
            seg = seg.replace(a, b)
        out.append(seg)
    return ''.join(out)
lines = [r'\begingroup\footnotesize', r'\begin{longtable}{@{}p{0.15\linewidth}p{0.05\linewidth}p{0.5\linewidth}p{0.22\linewidth}@{}}',
         r'\toprule Result & Card row & Registry status, verbatim (\texttt{claims.tsv}, main f8a6c2da) & Label used \\ \midrule \endhead']
for r in rows:
    cells = [c.strip() for c in r.strip().strip('|').split(' | ')]
    if len(cells) != 4:
        sys.exit(f'bad row: {r[:80]}')
    lines.append(' & '.join(esc(c) for c in cells) + r' \\ \addlinespace')
lines += [r'\bottomrule', r'\end{longtable}', r'\endgroup']
flags = [l for l in md if l.startswith('- **H')]
lines.append(r'\paragraph{Open flags for HQ.}')
lines.append(r'\begin{itemize}[leftmargin=1.5em]\footnotesize')
lines += [r'\item ' + esc(l[2:]) for l in flags]
lines.append(r'\end{itemize}')
open('status_ledger.tex', 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
print(len(rows), 'rows,', len(flags), 'flags')
