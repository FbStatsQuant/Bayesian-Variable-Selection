# W3-DIST proof leg — common rules for worker streams (read first)

Ticket W3-DIST (lead: Claude Fable 5.2). Repo clone `/home/fb31/Bayesian-Variable-Selection`; ticket folder
`Theory_work/Wave3/W3-DIST/`. You are a worker on Claude Third, effort high at most.
- **Write only under your own folder `Theory_work/Wave3/W3-DIST/work/<your stream>/`.** Run no git command. Start no
  agents. No cluster jobs. Do not edit STATEMENT.md, TARGET.md, ROUTES.md, DEPS.* or anything in `reviews/`.
- Read `Theory_work/Wave3/W3-DIST/STATEMENT.md` (v1.3.1: §0 setting, §1 master theorems, §1R reader versions, §3 lemmas
  and bridges), `ROUTES.md` (your section) and `API_CARDS.md` ("Common definitions" and your card). Notation there is
  binding. Do **not** read `reviews/`, `LOG.md` or `CHECKPOINT_*.md`.
- The statements are **targets fixed by HQ**. Prove them as stated. If a statement is false or needs a change, do not
  change it silently: prove the nearest true statement and put a section **"STATEMENT-CHANGE REQUEST"** at the top of
  your file, saying exactly what must change and why (with the counterexample if there is one).
- Proof standard: every inequality explicit, every constant named and its dependence stated, every probability bound
  with its event; one n₀ where the statement asks for one; no "similarly", no "it is easy to see". Where you use an
  inherited result, cite `file:line` and quote the statement used; inherited results below PROVED-CHECKED may be used
  only as explicitly stated hypotheses, or re-derived. Small numerical sanity checks (Python, local, < 5 min) are
  welcome; put scripts and outputs next to the proof.
- Status label on everything you write: **DRAFT (by this seat, unchecked)**. Each lemma goes afterwards to an
  independent pre-check and a cross-family line check; write so that a line-by-line reader can verify it.
- One markdown file per lemma, as named in your brief. End your reply with a 12-line summary: what is proved, what is
  not, statement-change requests, risks.
