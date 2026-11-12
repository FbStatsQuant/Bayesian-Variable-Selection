# Recording brief — W3-PSHARP and W3-MISR (HQ, 2026-11-12)

You act **for HQ** (Claude Opus 5.5, effort high, provider claude-personal). Unlike other workers you ARE authorized to
change git state on `main` in `C:/Users/felip/Bayesian-Variable-Selection`, but only as below; never force-push, never
rewrite history, never touch other branches. Read `Theory_work/INFRA/LIFECYCLE.md` §3–§4.1 (incl. "Seat tables by
addendum; carrier files", "Line endings"), `Theory_work/INFRA/README.md`, PROTOCOL rules 9–16, and
`Theory_work/Wave3/HQ_DECISIONS.md` entries of 2026-11-12. HOLDS.md must have no HOLD on any consumed claim.

For each ticket, in order **W3-PSHARP** (branch `theory/W3-PSHARP` @ 0071ee0; council R2, manifest 4513e05a…) then
**W3-MISR** (branch `theory/W3-MISR` @ 2f0990e; council R2, manifest 217d6708…):
1. Dry run first in a disposable clone (`git clone --no-hardlinks` under your temp folder): merge the branch into
   origin/main (`--no-ff`), `manifest.py verify`/`bind` for the council round, staged ingest of the CHECKPOINT_3
   registry blocks, `check.py --acceptance <ids>` and `--consumed-vs`, full `check.py --quiet`. MISR: **leave out**
   Rem-SNR, Rem-P, Rem-U (no consumers; schema has no 'remark' kind) — ingest the other 7 from a carrier file
   `Theory_work/Wave3/W3-MISR/reviews/REGISTRY_accept.md` (copy of the CHECKPOINT_3 blocks minus those three), per the
   carrier rule. Record no supersession (C-MIS → MIS-R is the owner's call).
2. Only if the dry run has 0 problems / 0 acceptance ERROR: repeat on `main` for real — merge commit (no squash),
   `--record`, commit with a message naming the ticket, claims and council round, push. Run `check.py --quiet` after
   (0 ERROR required) and `test_lifecycle.py`.
3. If anything refuses, stop for that ticket, change nothing on main for it, and report the exact check id + message.

Final message (≤ 12 lines): per ticket, claims recorded as PROVED-CHECKED (ids), merge commit hash, check.py totals, or
the refusal.
