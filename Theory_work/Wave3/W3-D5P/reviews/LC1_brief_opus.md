# LC1 — blind line check of L1–L3 (Claude Opus 5.5, effort high; fresh agent)

You are a blind line checker (PROTOCOL_v4 §3 step 3) for ticket W3-D5P. Worktree (read-only for you):
`/home/fb31/BVS-wt/W3-D5P`. **Do not write, create or delete any file**; use read-only commands only. Do not read
`Theory_work/Wave3/W3-D5P/LOG.md`, `CHECKPOINT_*.md`, `reviews/` (other than this brief), `TARGET.md` or `READER_DELTA.md`.
Return your whole review as your final message.

## Task
Check, **line by line**, the three proof files against the locked statement and the sources. Your job is to break them.
- `Theory_work/Wave3/W3-D5P/STATEMENT.md` (v1.0 LOCKED; claims (C1) LIST-K §2, (C2) LIST-CODE §3, (C3) LIST-R §4; §1 objects)
- `Theory_work/Wave3/W3-D5P/lemmas/L1_listK.md` (proof of (C1); pure finite algebra)
- `Theory_work/Wave3/W3-D5P/lemmas/L2_listCODE.md` (proof of (C2); a code reading — **open every cited `file:line`** in
  `Scripts/SMC_BVS/core/` and verify it says what the proof claims; look for any code path the proof misses, e.g. another
  writer of the HPM or of the top store, another `emit = false` evaluation, a way for status to be "completed" without
  LS0 having run, a cache entry inserted without an offer, a top-store entry that can be evicted)
- `Theory_work/Wave3/W3-D5P/lemmas/L3_listR.md` (proof of (C3); assembly)
Sources to verify citations against: `Theory_work/Wave3/W3-RM2-R/STATEMENT.md` (:52-93, :116-182),
`Theory_work/Wave3/W3-RM/STATEMENT.md` (:32-68, :94-136), `Theory_work/Wave1C/C-DLV/lemmas/L4_delivery.md` (:60-77),
`Theory_work/Wave3/W3-SAMP/lemmas/CC_code_check.md` (CC2, CC5), `Theory_work/Wave2/W2-APP/lemmas/L1_POST.md` (:1-33),
and the field definitions in SPEC: `git -C /home/fb31/BVS-wt/W3-AUDIT show 523dda23:Theory_work/Wave3/W3-AUDIT/SPEC_LIST_PIP.md`.
Registry statuses (do not open the registry): W3-RM2-R:RM2-R-plus, RM0-plus, DLV-0 @1.0.1 "PROVED-CHECKED; council R3, …";
W3-SAMP:CC@1.1.2 "CODE-CHECKED (lead; SL1, LC1, SW1, both council seats)"; W2-APP:POST@1.0.7 "PROVED-CHECKED".

For each proof: does every step follow; is every cited line correct; does the proof prove exactly the statement's
clause (quantifiers: every admissible run, either branch, the common data event; t ∈ (0, ½); NA qualification;
p ≥ 2 for the rate); does any step use something not in its stated inputs. List every interpretive sentence
("hence", "i.e.", "in particular", "consequently") inside the claim spans of STATEMENT (C1)–(C3) and say whether the
proofs establish it.

## Output format
1. Per-object table: `| object | verdict |` with VERIFIED / VERIFIED-WITH-AMENDMENTS / REFUTED / NOT-EXAMINED for
   STATEMENT (C1), (C2), (C3) as proved, L1, L2, L3.
2. Findings `LC1-1, …`: file:line, what fails (counterexample / code line if possible), tag **C** (correctness), **S**
   (scope/quantifier), **F** (faithfulness to statement or source), or **E** (editorial), and a concrete fix.
3. The interpretive-sentence list with verdicts.
4. One line: `LC1-VERDICT: <VERIFIED | VERIFIED-WITH-AMENDMENTS | REFUTED>`.
