#!/usr/bin/env python3
"""Independent fidelity check of every stmt box against its cited source span (stdlib only).

Normalises both sides to a stream of 'content characters' (letters, digits, Greek/math symbols), dropping
LaTeX markup, markdown markup, whitespace and punctuation, then reports a similarity ratio per box.
Boxes below the threshold are listed for manual comparison. Usage: python scripts/verify_stmt.py [threshold]
"""
import difflib, glob, os, re, sys, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
DOC = os.path.dirname(HERE)
REPO = os.path.abspath(os.path.join(DOC, "..", ".."))
NBH = "Theory_work/Old_Projects/New_BVS_Headquarters/"
STMT = re.compile(r"\\begin\{stmt\}\{([^{}]*)\}(.*?)\\end\{stmt\}", re.S)

MATHMAP = {r"\le": "≤", r"\leq": "≤", r"\ge": "≥", r"\geq": "≥", r"\ne": "≠", r"\neq": "≠", r"\to": "→",
           r"\infty": "∞", r"\in": "∈", r"\notin": "∉", r"\subseteq": "⊆", r"\cap": "∩", r"\cup": "∪",
           r"\pi": "π", r"\sigma": "σ", r"\delta": "δ", r"\varepsilon": "ε", r"\epsilon": "ε", r"\lambda": "λ",
           r"\theta": "θ", r"\phi": "φ", r"\varphi": "φ", r"\rho": "ρ", r"\psi": "ψ", r"\mu": "μ", r"\eta": "η",
           r"\alpha": "α", r"\beta": "β", r"\gamma": "γ", r"\tau": "τ", r"\nu": "ν", r"\kappa": "κ", r"\chi": "χ",
           r"\Phi": "Φ", r"\Lambda": "Λ", r"\Omega": "Ω", r"\sharp": "♯", r"\cdot": "·", r"\times": "×",
           r"\lfloor": "⌊", r"\rfloor": "⌋", r"\lceil": "⌈", r"\rceil": "⌉", r"\sum": "∑", r"\prod": "∏",
           r"\Rightarrow": "⇒", r"\Leftrightarrow": "⇔", r"\approx": "≈", r"\lesssim": "≲", r"\mid": "|",
           r"\Vert": "‖", r"\|": "‖", r"\ell": "ℓ", r"\partial": "∂", r"\nabla": "∇", r"\pm": "±"}
SUBSUP = str.maketrans("₀₁₂₃₄₅₆₇₈₉⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻ₙᵢⱼₖ", "01234567890123456789+-nijk")


def norm(s, tex):
    if tex:
        s = re.sub(r"(?<!\\)%.*", "", s)
        s = re.sub(r"\\(src|pos)\{[^{}]*\}", "", s)
        for k in sorted(MATHMAP, key=len, reverse=True):
            s = re.sub(re.escape(k) + r"(?![A-Za-z])", MATHMAP[k], s)
        s = re.sub(r"\\(textbf|textit|emph|texttt|mathrm|mathbf|mathcal|mathbb|mathsf|operatorname|text|hat|bar|tilde|widehat|overline|textsf|mathit)\b", "", s)
        s = re.sub(r"\\[A-Za-z]+\*?", "", s)
    s = unicodedata.normalize("NFKC", s).translate(SUBSUP)
    s = s.replace("−", "-")
    keep = [c for c in s if c.isalnum() or c in "≤≥≠→∞∈∉⊆∩∪πσδελθφρψμηαβγτνκχΦΛΩ♯×⌊⌋⌈⌉∑∏⇒⇔≈≲‖ℓ∂∇±<>=+-"]
    return "".join(keep).lower()


def span_text(spec):
    out = []
    for piece in spec.split(";"):
        piece = piece.strip()
        m = re.match(r"^(\S+?)(?::([0-9][0-9,\-–\s]*))?(?:\s.*)?$", piece)
        if not m:
            continue
        path = m.group(1)
        if path.startswith("NBH/"):
            path = NBH + path[4:]
        full = os.path.join(REPO, path)
        if not os.path.exists(full):
            return None
        lines = open(full, encoding="utf-8", errors="replace").read().splitlines()
        if not m.group(2):
            out.append("\n".join(lines))
            continue
        for part in re.split(r"[,\s]+", m.group(2).strip()):
            if not part:
                continue
            a = re.split(r"[-–]", part)
            lo = int(a[0]); hi = int(a[1]) if len(a) > 1 and a[1] else lo
            out.append("\n".join(lines[lo - 1:hi]))
    return "\n".join(out)


def main():
    thr = float(sys.argv[1]) if len(sys.argv) > 1 else 0.90
    rows = []
    for f in sorted(glob.glob(os.path.join(DOC, "sections", "*.tex"))):
        t = open(f, encoding="utf-8").read()
        for m in STMT.finditer(t):
            spec, body = m.group(1), m.group(2)
            line = t[:m.start()].count("\n") + 1
            src = span_text(spec)
            if src is None:
                rows.append((0.0, 0.0, os.path.basename(f), line, spec, "SOURCE MISSING")); continue
            body = re.sub(r"^\s*\\textbf\{[^\n]*?\}[^\n]*?\\\\\s*$", "", body, flags=re.M)  # editorial label line
            a, b = norm(body, True), norm(src, False)
            if not a:
                continue
            sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
            # coverage of the box by the source (box text should be contained in the span)
            matched = sum(bl.size for bl in sm.get_matching_blocks())
            cov = matched / max(1, len(a))
            rows.append((cov, sm.ratio(), os.path.basename(f), line, spec, ""))
    rows.sort()
    bad = [r for r in rows if r[0] < thr]
    print(f"{len(rows)} stmt boxes; box-content covered by source (median) = {sorted(r[0] for r in rows)[len(rows)//2]:.3f}; below {thr}: {len(bad)}")
    for r in bad:
        print(f"  cov={r[0]:.3f} ratio={r[1]:.3f}  {r[2]}:{r[3]}  [{r[4]}] {r[5]}")


if __name__ == "__main__":
    main()
