"""Open every full path:line citation in lead-authored statement/proof/report files.
Reviewers' verbatim replies are excluded; they are evidence, not lead citations.
Validate exact line plus required supporting phrase, fail closed on new citations.
"""
from pathlib import Path
import re
HERE=Path(__file__).resolve().parent
TICKET=HERE.parent
ROOT=TICKET.parents[2]
expected={
('Theory_work/State_of_Project/sections/04_theory.tex',70):'D0: data/target',
('Theory_work/State_of_Project/sections/04_theory.tex',71):'Score.',
('Theory_work/State_of_Project/sections/04_theory.tex',72):'Prior.',
('Theory_work/State_of_Project/sections/04_theory.tex',73):'Start/bridge.',
('Theory_work/State_of_Project/sections/04_theory.tex',74):'G: sampling model.',
('Scripts/SMC_BVS/core/cpp/v3_core.cpp',372):'static void ingest_tables',
('Scripts/SMC_BVS/core/cpp/v3_core.cpp',408):'ingest_tables(led, *h)',
('Scripts/SMC_BVS/core/cpp/v3_core.cpp',473):'long long cap_ll',
('Scripts/SMC_BVS/core/cpp/v3_engine.h',97):'q.F = D.logprior[k] + lm',
('Scripts/SMC_BVS/core/cpp/v3_engine.h',408):'best.F > C.F',
('Scripts/SMC_BVS/core/cpp/v3_engine.h',409):'A.moves >= ell',
('Scripts/SMC_BVS/core/cpp/v3_score.h',40):'D.K = std::min(p, n / 2)',
}
files=list(TICKET.glob('*.md'))+list((TICKET/'lemmas').glob('*.md'))
rx=re.compile(r'((?:Theory_work|Scripts)/[A-Za-z0-9_./-]+):(\d+)')
rows=[];miss=0
for f in sorted(files):
    for path,line in rx.findall(f.read_text(encoding='utf8')):
        line=int(line);phrase=expected.get((path,line));target=ROOT/path
        content=target.read_text(encoding='utf8').splitlines() if target.is_file() else []
        text=content[line-1] if 0<line<=len(content) else ''
        ok=phrase is not None and phrase in text
        miss+=not ok
        rows.append(f'{"PASS" if ok else "FAIL"} {f.relative_to(TICKET)} -> {path}:{line} expected={phrase!r}\n  {text}')
rows.append(f'CHECKED {len(rows)} citations; MISSES {miss}')
(HERE/'CITECHECK.txt').write_text('\n'.join(rows)+'\n',encoding='utf8')
print(rows[-1]);assert not miss
