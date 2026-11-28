# LC1r2 brief — second re-check of T1 (GW) v3 and T2 (BLK) v3 (Claude Opus 5.5, high; new agent)

PROTOCOL_v4 §2A "re-check of a repaired lemma". Workspace (read only; write nothing): `/home/fb31/BVS-wt/W3-AUDIT`.

Read `Theory_work/Wave3/W3-AUDIT/track_A/reviews/LC1r_reply_opus.md` (findings on v2) and `.../LC1r_disposition.md`
(the lead's actions), then the current `.../track_A/T1_GW/STATEMENT.md`, `.../T1_GW/PROOF.md`,
`.../T2_BLK/STATEMENT.md`, `.../T2_BLK/PROOF.md`, and the code `Scripts/SMC_BVS/core/` (pin 4676af6 = HEAD).

Scope: only the v3 changes listed in the disposition and the STATEMENT changelogs. For each LC1r finding: RESOLVED /
NOT RESOLVED. Then try to break the rewritten parts: the leaf-field definition of 𝒱_op and "statistical state" (is any
statistical field still computed from an operational one? is any Boolean's clock dependence leaking outside the
Booleans?), (GW-i) as restated, (GW-iv) and Step 4 (both inclusions of 𝒜 = 𝒜° ∩ G; the allocation clause; 𝒜° ∈ σ(𝓒°)),
Step 5's exception exit; T2's setting-R premise and proof line. Tag findings C / S / F / E with file:line.
Last line: `LC1r2-VERDICT: T1=<VERIFIED|VERIFIED WITH AMENDMENTS|NOT VERIFIED>; T2=<…>`.
