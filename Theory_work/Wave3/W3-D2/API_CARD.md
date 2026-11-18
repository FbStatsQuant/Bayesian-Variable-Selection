# W3-D2 — API blind-audit card (for HQ; pattern of `Theory_work/Wave3/API_AUDIT/audit_batch.py`, audit1)

**What.** One blind Message Batches request: "break the proof; findings only" on `W3-D2:Thm2X` and `W3-D2:Cor2X`.
**Builder (no API call):** `python3 Theory_work/Wave3/W3-D2/api_request_build.py <outdir>` from the worktree root →
`<outdir>/requests.json` + `<outdir>/MANIFEST.txt` (sha256 per source; any dropped line listed). HQ submits with its own key
and the existing `audit_batch.py submit/wait` flow (or by hand), per its API rules.
**Model / effort (HQ to confirm):** `claude-fable-5-2`, effort high (never above), max_tokens 64 000; about 11 k input tokens.
**Content (blind).** Ticket STATEMENT §§0–4 and PROOF; consumed excerpts: W3-MISR-R STATEMENT 25–108 (master) and
`lemmas/G2_corr.md` (its proof), W3-MISR STATEMENT 17–123, W3-POST STATEMENT 16–39, W3-READER `lemmas/R1_set_sizes.md`
6–46, READER_VERSIONS 26–30 and 262–281 (recorded Theorem 2), NOTATION 9–28. No reviews, LOG, PLAN, CHECKPOINT, REPORT.
**No status words:** status quotations (PROVED…, VERIFIED…, council/MANIFEST/scores, [REG-…], "(main …)") are redacted inside
lines; a line that still carries one is dropped. Test build (2026-11-17): 0 lines dropped except PROOF.md:3 (its status line);
the request text contains none of PROVED / CHECKED / council / PASS / unchecked.
**System text:** in the builder (`SYSTEM`): consumed results taken as true as stated; check their hypotheses where used;
attack the q = 0 instance, object identity, quantifiers/constants, thresholds in n, probability bookkeeping, deterministic
inequalities, the corollary's reduction and quotation; findings only, severity ERROR/GAP/MINOR with file:line and a
counterexample or missing argument; two closing lines `AUDIT <id> FINDINGS=<n>`.
**Use of the reply:** proof material only (v4 H3), never a review layer; any GAP/ERROR goes to the lead for a fix and an
Opus diff check before recording.
