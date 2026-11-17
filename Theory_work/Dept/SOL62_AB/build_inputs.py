#!/usr/bin/env python3
"""Builds Theory_work/Dept/SOL62_AB/case<k>/{BRIEF.md,INPUTS.md,RUN.md} from git history (read-only).

Evaluation only (D124). Nothing is sent anywhere. Every excerpt is `git show <commit>:<path>` (optionally a line range,
1-indexed inclusive), preserved byte for byte; the only additions are the delimiter lines
`<<<FILE ... >>>` / `<<<END FILE>>>` and, in RUN.md, the fixed REPLAY NOTICE.
Run from the repo root:  python3 -I Theory_work/Dept/SOL62_AB/build_inputs.py
"""
import hashlib
import os
import subprocess

OUT = "Theory_work/Dept/SOL62_AB"
W = "Theory_work/Wave3"

REPLAY_NOTICE = """REPLAY NOTICE (added for this replay; it is not part of the original brief). The repository checkout named in the
brief is NOT available to you, and you cannot write files. The files the brief asks you to read are supplied inline after
the brief, each between `<<<FILE path @commit [lines a-b] >>>` and `<<<END FILE>>>` markers, byte-for-byte as the original
reviewer saw them (some are line-range excerpts; some listed files are not supplied). Treat the supplied text as the
frozen inputs. Where the brief names a file or check that is not supplied, say "not supplied" for that item and do not guess
its content. Ignore any instruction to write a file; return the complete reply as your final message, in the format the
brief specifies. You may run code if you need to check arithmetic."""

CASES = {
    1: dict(
        brief=("01873c40", f"{W}/W3-MISR-R/reviews/L1_brief.md"),
        strip_header=True,
        files=[
            ("01873c40", f"{W}/W3-MISR-R/BRIEF.md", None),
            ("01873c40", f"{W}/W3-MISR-R/STATEMENT.md", None),
            ("01873c40", f"{W}/W3-MISR-R/PLAN.md", None),
            ("01873c40", f"{W}/W3-MISR/STATEMENT.md", (17, 45)),
            ("01873c40", f"{W}/W3-MISR/STATEMENT.md", (162, 198)),
            ("01873c40", f"{W}/W3-MISR/lemmas/G_corollaries.md", (24, 35)),
            ("01873c40", f"{W}/W3-MISR/lemmas/G_corollaries.md", (67, 94)),
        ],
    ),
    2: dict(
        brief=("934a2b43", f"{W}/W3-D2/reviews/BRIEF_R1_sol.md"),
        strip_header=True,
        files=[
            ("934a2b43", f"{W}/W3-D2/STATEMENT.md", None),
            ("934a2b43", f"{W}/W3-D2/PROOF.md", None),
            ("934a2b43", f"{W}/W3-D2/TARGET.md", None),
            ("934a2b43", f"{W}/W3-D2/numerics/N1_floor_and_e2e.py", None),
            ("934a2b43", f"{W}/W3-D2/numerics/N1_out.txt", None),
            ("a14ce83b", f"{W}/W3-MISR-R/STATEMENT.md", (88, 108)),
            ("e2680987", f"{W}/W3-POST/STATEMENT.md", (16, 40)),
        ],
    ),
    3: dict(
        brief=("4df0ea57", f"{W}/W3-MISR-R/reviews/K2_brief.md"),
        strip_header=True,
        files=[
            ("4df0ea57", f"{W}/W3-MISR-R/reviews/K2_repair_diff.txt", None),
            ("4df0ea57", f"{W}/W3-MISR-R/reviews/K1_linecheck_sol.md", (13, 24)),
            ("4df0ea57", f"{W}/W3-MISR-R/lemmas/H1_plus.md", None),
            ("4df0ea57", f"{W}/W3-MISR-R/lemmas/H2_uniform.md", None),
            ("4df0ea57", f"{W}/W3-MISR-R/DEPS.tsv", (1, 1)),
            ("4df0ea57", f"{W}/W3-MISR-R/DEPS.tsv", (10, 11)),
            ("4df0ea57^", f"{W}/W3-MISR-R/lemmas/H1_plus.md", None),
            ("4df0ea57^", f"{W}/W3-MISR-R/lemmas/H2_uniform.md", None),
        ],
    ),
}


def git_show(commit, path):
    return subprocess.run(["git", "show", f"{commit}:{path}"], check=True, capture_output=True).stdout.decode("utf-8")


def excerpt(text, rng):
    if rng is None:
        return text
    lines = text.splitlines(keepends=True)
    a, b = rng
    return "".join(lines[a - 1:b])


def sha(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:12]


def main():
    for k, spec in CASES.items():
        d = os.path.join(OUT, f"case{k}")
        os.makedirs(d, exist_ok=True)
        bc, bp = spec["brief"]
        brief = git_show(bc, bp)
        with open(os.path.join(d, "BRIEF.md"), "w", encoding="utf-8", newline="") as f:
            f.write(brief)
        # prompt body of the original = text after the first line consisting of '---' (above it: saved-before-launch header)
        lines = brief.splitlines(keepends=True)
        idx = next(i for i, l in enumerate(lines) if l.strip() == "---")
        body = "".join(lines[idx + 1:]).lstrip("\n")
        blocks, manifest = [], []
        for commit, path, rng in spec["files"]:
            txt = excerpt(git_show(commit, path), rng)
            lab = f"{path} @{commit}" + (f" lines {rng[0]}-{rng[1]}" if rng else " (whole file)")
            manifest.append(f"| `{path}` | `{commit}` | {f'{rng[0]}-{rng[1]}' if rng else 'whole'} | {len(txt)} | {sha(txt)} |")
            blocks.append(f"<<<FILE {lab} >>>\n{txt}{'' if txt.endswith(chr(10)) else chr(10)}<<<END FILE>>>\n")
        inputs_body = "\n".join(blocks)
        head = (f"# Case {k} — INPUTS (excerpts, byte-for-byte from git; nothing added inside the markers)\n\n"
                "| path | commit | lines | chars | sha256[:12] of excerpt |\n|---|---|---|---|---|\n"
                + "\n".join(manifest) + "\n\nBuilt by `build_inputs.py`; the text between the markers below is the excerpt.\n\n")
        with open(os.path.join(d, "INPUTS.md"), "w", encoding="utf-8", newline="") as f:
            f.write(head + inputs_body)
        prompt = REPLAY_NOTICE + "\n\n===== ORIGINAL BRIEF (verbatim; text after the saved-before-launch header) =====\n\n" + body + \
            "\n===== SUPPLIED INPUTS =====\n\n" + inputs_body
        with open(os.path.join(d, "PROMPT_6.2.txt"), "w", encoding="utf-8", newline="") as f:
            f.write(prompt)
        print(f"case{k}: brief {len(brief)} chars, inputs {len(inputs_body)} chars, prompt {len(prompt)} chars, ~{len(prompt)/3.5:.0f} tokens")


if __name__ == "__main__":
    main()
