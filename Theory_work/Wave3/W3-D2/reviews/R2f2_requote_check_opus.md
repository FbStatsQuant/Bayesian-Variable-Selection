# W3-D2 R2f2 requote check (Opus one-shot, recorder-requested; NOT a council seat)

Reviewer: Claude Opus 5.5 (one-shot subagent, read-only), task D2, 2026-11-23, two rounds on the same agent. Subject: the CITATION-ONLY requote of STATEMENT.md §5 (lines 79, 81-83, 85-86) and of the
caveat (a) sentence (lines 105-107), and the DEPS.tsv S:inputs row, that turns the ticket's citecheck.py green after W3-MISR-R:CorGb-plus (1.0.1 → 1.0.2: condition list refreshed, HQ GO commit 5912ce6e),
W3-READER:R1 (1.0.2 → 1.0.3), W3-POST2:C (1.0.6 → 1.0.7) and W3-POST:Prop-LB (1.0.0 → 1.0.1, relabelled PROVED-CHECKED) changed in the registry.

Round 1 (diff without CorGb-plus), verbatim: "REQUOTE-VERDICT: PURE. Each quote matches claims.tsv character for character; only lines 79, 83 and 85-86 changed, both files 126 lines, spans 14-27, 29-48, 50-58, 60-64
byte-identical; DEPS.tsv only the S:inputs row (sha recomputed from lines 81-86, matches)."

Round 2 (diff with CorGb-plus), verbatim: "REQUOTE-VERDICT: PURE (the diff itself). 1. The four pins (CorGb-plus@1.0.2, R1@1.0.3, POST2:C@1.0.7, Prop-LB@1.0.1) and their statuses match claims.tsv character for character.
2. Only lines 79, 81-83 and 85-86 changed; both files 126 lines; spans 14-27, 29-48, 50-58, 60-64 byte-identical. 3. DEPS.tsv: only the S:inputs row; sha recomputed, matches. 4. Line 4 `@1.0.1`
is acceptable (describes where the ticket came from). Not acceptable as it stood: caveat (a), lines 105-107, still said Prop-LB is 'PROVED (by this seat, unchecked)' pointing to §5 and gave the old @1.0.1
condition list. Replace from 'rest on' through '(§5).' with: 'rest on `W3-MISR-R:CorGb-plus@1.0.2`, whose status is conditional on W2-APP:POST, C-MIS:GDb and C-MIS:Prop-P (§5; @1.0.1 listed W3-POST2:C, :E, :A1, :A0 and,
through W3-POST2:C, the then-unchecked `W3-POST:Prop-LB`).' Keep it to 3 lines." The recorder applied exactly this replacement (same line count) before the recording.
