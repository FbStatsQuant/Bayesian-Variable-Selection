# W3-D3 — API blind-audit card (for HQ; pattern of `Theory_work/Wave3/API_AUDIT/audit_batch.py`, audit1)

**What.** One blind Message Batches request: "break the proof; findings only" on `W3-D3:Thm2SG`, `W3-D3:B3w`, `W3-D3:ExSG`.
**Builder (no API call):** `python3 Theory_work/Wave3/W3-D3/api_request_build.py <outdir>` from the worktree root →
`<outdir>/requests.json` + `<outdir>/MANIFEST.txt` (sha256 per source; any dropped line listed). HQ submits with its own key
and the existing `audit_batch.py submit/wait` flow (or by hand), per its API rules.
**Model / effort (HQ to confirm):** `claude-fable-5-2`, effort high (never above), max_tokens 64 000 (128 000 if HQ's W-card
rule applies); about 20 k input tokens (62 k characters).
**Content (blind).** Ticket STATEMENT from the aliases line to the end of §4 (setting, Theorem 2SG, Lemma B3w,
Proposition ExSG, remarks; §§5–9 — class, inputs with statuses, dependencies, tag, changelog — are not sent), `lemmas/B3w.md`,
`lemmas/ASSEMBLY.md`; consumed excerpts: W3-POST STATEMENT 16–100 (target, Theorem 1 with item 6), W3-DIST bridge files
`B0.md` 7–40, `B1.md` 7–30, `B2core.md` 7–30, `B2.md` 22–55 (statement and proof of (a)), `B3.md` from line 7 (template, with
amendment A-2), W3-READER `lemmas/R1_set_sizes.md` 6–31, READER_VERSIONS 26–30 and 257–290 (recorded Theorem 2),
NOTATION 9–40. No reviews, LOG, PLAN, CHECKPOINT, REPORT.
**No status words:** status quotations are redacted inside lines; a line that still carries one is dropped. Test build
(2026-11-17): lines dropped only where a status quotation sits (B3w.md 44–45, ASSEMBLY.md 9–10, W3-POST STATEMENT 78, 90);
the request text contains none of PROVED / CHECKED / council / PASS / unchecked.
**System text:** in the builder (`SYSTEM`): consumed results taken as true as stated; check their hypotheses where used;
attack the window coverage, the constants after the scale reduction, the probability bounds and their thresholds, the
completion off the event where no column is removed and the measurability of the interface events, every hypothesis of
item 6 and its regime, the transfer to the actual outputs, and the MGF inequalities of ExSG (including the in-place proof
of Hoeffding's lemma); findings only, severity ERROR/GAP/MINOR with file:line and a counterexample or missing argument;
three closing lines `AUDIT <id> FINDINGS=<n>`.
**Use of the reply:** proof material only (v4 H3), never a review layer; any GAP/ERROR goes to the lead for a fix and an
Opus diff check before recording.
