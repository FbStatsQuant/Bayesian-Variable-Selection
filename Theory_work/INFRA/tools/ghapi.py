"""ghapi.py — minimal GitHub REST client for the theory workflow (used when the `gh` CLI is not installed).

The token comes from git's own credential helper (`git credential fill` for github.com), is kept in memory only and
is never printed or written. Standard library only.

  python Theory_work/INFRA/tools/ghapi.py labels                 create/update the workflow labels (idempotent)
  python Theory_work/INFRA/tools/ghapi.py issue --title T --body-file F [--label L ...]
  python Theory_work/INFRA/tools/ghapi.py pr --head BRANCH --base main --title T --body-file F
  python Theory_work/INFRA/tools/ghapi.py list-issues [--label L]
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import urllib.error
import urllib.request

REPO = "FbStatsQuant/Bayesian-Variable-Selection"
API = f"https://api.github.com/repos/{REPO}"
LABELS = {  # name: (color, description)
    "theory": ("5319e7", "Theory program (Theory_work/)"),
    "lemma-gap": ("d93f0b", "A proof step does not go through; statement may stand (PATCH)"),
    "retraction": ("b60205", "Statement false, too broad, or evidence weaker than recorded (RETRACT/NARROW/DOWNGRADE)"),
    "suspect": ("fbca04", "Claim SUSPECT after an upstream change; repair issue from propagate.py"),
    "sim-request": ("0e8a16", "Numerics needed: falsification, boundary-violation, study"),
    "strategy": ("1d76db", "Supersession, coexistence, new route, deprecation"),
    "editorial": ("c5def5", "Wording, stale rows, citations; no mathematical change"),
    "major-claim": ("000000", "Changes what the paper claims: Felipe approves"),
    "council-pass": ("0e8a16", "Council passed (both reviewers >= 8.0, all gates); counts as PR approval"),
    "improvement": ("bfdadc", "Improvement ticket: weaken an assumption / strengthen a conclusion / extend scope"),
}
_TOKEN = None


def token() -> str:
    global _TOKEN
    if _TOKEN is None:
        out = subprocess.run(["git", "credential", "fill"], input="protocol=https\nhost=github.com\n\n",
                             capture_output=True, text=True, timeout=30).stdout
        _TOKEN = next((l.split("=", 1)[1] for l in out.splitlines() if l.startswith("password=")), "")
        if not _TOKEN:
            sys.exit("no GitHub credential available from git credential helper")
    return _TOKEN


def call(method: str, url: str, data: dict | None = None):
    req = urllib.request.Request(url if url.startswith("http") else API + url, method=method,
                                 data=json.dumps(data).encode() if data is not None else None,
                                 headers={"Authorization": f"Bearer {token()}", "Accept": "application/vnd.github+json",
                                          "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "theory-infra"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            body = r.read()
            return r.status, (json.loads(body) if body else None)
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read() or b"null")


def ensure_labels():
    for name, (color, desc) in LABELS.items():
        st, _ = call("POST", "/labels", {"name": name, "color": color, "description": desc})
        if st == 422:  # exists: update colour/description
            st, _ = call("PATCH", f"/labels/{name}", {"color": color, "description": desc})
        print(f"label {name}: {st}")


def create_issue(title, body, labels=()):
    st, j = call("POST", "/issues", {"title": title, "body": body, "labels": list(labels)})
    return j.get("html_url") if st == 201 else f"ERROR {st}: {j}"


def create_pr(head, base, title, body):
    st, j = call("POST", "/pulls", {"head": head, "base": base, "title": title, "body": body})
    return j.get("html_url") if st == 201 else f"ERROR {st}: {j}"


def issue(title, body_file, labels):
    """Create an issue with gh if installed, else via the REST API. Returns the URL or an error string."""
    if shutil.which("gh"):
        cmd = ["gh", "issue", "create", "--repo", REPO, "--title", title, "--body-file", body_file]
        for l in labels:
            cmd += ["--label", l]
        r = subprocess.run(cmd, capture_output=True, text=True)
        return (r.stdout or r.stderr).strip()
    with open(body_file, encoding="utf-8") as fh:
        return create_issue(title, fh.read(), labels)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["labels", "issue", "pr", "list-issues"])
    ap.add_argument("--title")
    ap.add_argument("--body-file")
    ap.add_argument("--label", action="append", default=[])
    ap.add_argument("--head")
    ap.add_argument("--base", default="main")
    a = ap.parse_args()
    if a.cmd == "labels":
        ensure_labels()
    elif a.cmd == "issue":
        print(issue(a.title, a.body_file, a.label))
    elif a.cmd == "pr":
        with open(a.body_file, encoding="utf-8") as fh:
            print(create_pr(a.head, a.base, a.title, fh.read()))
    else:
        q = "?state=all&per_page=50" + (f"&labels={a.label[0]}" if a.label else "")
        st, j = call("GET", "/issues" + q)
        for i in j or []:
            print(f"#{i['number']} [{i['state']}] {i['title']}")


if __name__ == "__main__":
    main()
