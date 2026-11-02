# A-REV2 source pins

Review baseline: `00c7b34` (the supplied campaign worktree). No source or locked status is edited.
These are the remote heads fetched on 2026-11-02; findings refer to these versions, not the older
heads sometimes named in the first referee's report.

| Branch | Commit |
|---|---|
| theory/W1-T03R | 7e14d6f090bef91861455f45c69017e2a5774198 |
| theory/W2-VT03R | b9f6d9b8f6507dd1053d6b916d7a68e1f7b4aa5e |
| theory/W1-T37R | 3bcc42958f9d7373178ebab931f62ad38538c8f3 |
| theory/W3-VT37R | 4988b966f2aafa9c61077e6002146297f0df0dd7 |
| theory/W1-EXP | 722bd18e51fcc3b485c07590097e137dac71a5aa |
| theory/W3-VEXP | 7970fa0b00dd07c70d2670d17fcb44ba3748b52a |
| theory/W2-PREM | 988c5f55c0fb0fbd6050b6a4d0c75f14159716e3 |

Read each branch's `theory_campaign/<branch suffix>/PROOF.md`, `REPORT.md`, and (where present)
`REPAIRS.md` with `git show <commit>:<path>`. Scratch snapshots in `sources/` are ignored.
The independent checks do not import those snapshots or their numerical implementations.

Run the small numerical audit from the repository root, one job at a time:

```sh
/home/fb31/.config/bvs-hq/owls/owls_run -j 2 -- python3 theory_campaign/A-REV2/scripts/check_review.py
```

The script writes `results/checks.json`. Its assertions test finite identities and concrete
counterexamples; they do not establish asymptotic theorems. The report supplies the proof audit.
