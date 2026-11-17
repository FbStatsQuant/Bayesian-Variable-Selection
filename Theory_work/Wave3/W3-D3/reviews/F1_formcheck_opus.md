# W3-D3 — F1 form check, seat `opus` (Claude Opus 5.5, high; fresh agent)

F1-VERDICT: FORM-ONLY

Reasons:
1. `manifest.py verify … MANIFEST_R2f.txt` gives `verify: OK MANIFEST c52866ef…a5d3`, which matches the brief.
   `diff MANIFEST_R2.txt MANIFEST_R2f.txt` shows only two changed lines: the MANIFEST header line and the `DEPS.tsv` row
   (cd76c429… → 85bcaa9e…). Every other per-file row and every #EXTRA line is identical, so DEPS.tsv is the only
   changed file.
2. `F1_form_diff.txt` (blobs 83eafaa6..aec66fa2; `git hash-object DEPS.tsv` = aec66fa2, so it is the current file)
   touches exactly the five rows S:B3w, S:ExSG, P:B3w, P:ExSG and R:registry. In each row only checked_sha, checked_by
   (→ `reviews/R2_council_opus.md`) and state (STALE → OK) change. The id, file:lines, uses and sha columns are
   unchanged, and the new checked_sha equals sha. The other five rows are untouched.
3. I recomputed the span hashes in memory with deps_hand.py's rule (header-delimited span, trailing blank lines
   trimmed, first 16 hex of sha256): S:B3w STATEMENT.md:59-80 2936d4aab6e60634; S:ExSG :82-90 a77b2844d9b4adda; P:B3w
   lemmas/B3w.md:12-134 0f1cd4bf262c570b; P:ExSG lemmas/ASSEMBLY.md:54-83 7e4c9265f8760d8c; R:registry REPORT.md:64-91
   e345cb9a2860d58a. All five match DEPS.tsv, and so do the line ranges. The other five rows also reproduce. I wrote no
   scratch copy, so `.rc_tmp/` was not used.
4. Section (b) of `R2_council_opus.md`, "The STALE DEPS rows, each re-checked in full", covers exactly S:B3w (:59-80),
   S:ExSG (:82-90), P:B3w (B3w :12-134), P:ExSG (ASSEMBLY :54-83) and R:registry (REPORT :64-91). It reports no finding.
   The seat also states that it recomputed all 10 span hashes on MANIFEST f5599604…, and the file it reviewed has the
   same span hashes as now.

Note: in the worktree, DEPS.tsv and LOG.md are modified but uncommitted. LOG.md is not in either manifest, so it does
not affect the verdict. I did not read it.
