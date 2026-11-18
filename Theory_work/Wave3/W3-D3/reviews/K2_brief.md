# W3-D3 — K2 re-check brief (Opus 5.5 high, new agent; saved before launch 2026-11-17)

You re-check repairs (PROTOCOL_v4 §2A "re-check of a repaired lemma": new agent of the finder's family) for ticket W3-D3
in the git worktree /home/fb31/BVS-wt/W3-D3 (read-only for you except your reply file). Do not read `LOG.md` or
`CHECKPOINT_1.md`. Do not change git state. Scratch only in /home/fb31/BVS-wt/W3-D3/.rc_tmp/ (delete it at the end).

**Inputs.** The line check `Theory_work/Wave3/W3-D3/reviews/K1_linecheck_opus.md` (findings K1-1 … K1-12), the lead's
disposition `reviews/K1_disposition.md`, and the repair diff `reviews/K1_repair.diff` (STATEMENT v1.1 → v1.2, `lemmas/B3w.md`,
`lemmas/ASSEMBLY.md`). Current files: `Theory_work/Wave3/W3-D3/STATEMENT.md` (v1.2), `lemmas/B3w.md`, `lemmas/ASSEMBLY.md`,
`REPORT.md` §6 (registry blocks), `DEPS.tsv`. Consumed sources as named in those files (W3-POST STATEMENT lines 16-100;
W3-DIST `work/E_bridges/B0.md`, `B1.md`, `B2core.md`, `B2.md`, `B3.md`; W3-READER `lemmas/R1_set_sizes.md`).

**Tasks.**
1. For each K1 finding: RESOLVED / NOT RESOLVED / RESOLVED-WITH-NEW-ISSUE, checking the repaired text, not only the diff.
   In particular K1-1: with θ⁰ supported on S₀, are B3w (c), Step 6 and ASSEMBLY Steps 2–4 now correct and consistent
   (supp θ° = S₀ on every outcome; 𝒜′_n measurable; item 6's outputs refer to S₀; transfer error ≤ P(𝒜_nᶜ))?
2. Re-check in full the DEPS rows that changed: STATEMENT §1 (Thm2SG), §2 (B3w), §5 (class, outside spans: mathematical
   relations only), §6 (inputs: every quoted status matches `Theory_work/INFRA/registry/claims.tsv` for that id@version);
   `lemmas/B3w.md` (whole); `lemmas/ASSEMBLY.md` "Theorem 2SG"; `REPORT.md` §6 (each REGISTRY block's statement/premise line
   ranges point at the right STATEMENT spans; assumptions and conclusions match STATEMENT; nothing claimed beyond it).
3. Statement-change check of v1.1 → v1.2: confirm or contest each 1.2 changelog row's tag and the retagged row 2 (K1-8).
4. List any interpretive sentence newly introduced inside the claimed spans (§§1–3) with a verdict.

**Reply.** Write `Theory_work/Wave3/W3-D3/reviews/K2_recheck_opus.md`: verdict line `RESOLVED` / `RESOLVED-WITH-AMENDMENTS` /
`NOT RESOLVED`; the per-finding table; findings numbered K2-1, … tagged C/S/F/E with file:line and the fix; the
statement-change table; per DEPS row re-checked: VERIFIED / VERIFIED-WITH-AMENDMENTS / NOT VERIFIED. Then end.
