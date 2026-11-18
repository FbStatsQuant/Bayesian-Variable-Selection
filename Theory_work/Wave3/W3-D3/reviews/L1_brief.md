# W3-D3 — L1 statement lock brief (Sol, fresh, blind first read; saved before launch 2026-11-17)

You are the statement-lock reviewer (PROTOCOL_v4 §3 step 1, Tier B) for ticket W3-D3 in the git worktree
/home/fb31/BVS-wt/W3-D3 (read-only for you except your reply file). Do not read `LOG.md`. No TMPDIR, no writes outside
the worktree; scratch only in /home/fb31/BVS-wt/W3-D3/.rc_tmp/ (delete it at the end). Do not run git commands that
change state.

**Target.** Theorem 2 of the reader versions (claims card row 1.2: posterior concentration on a random Gaussian design)
restated for rows that are sub-Gaussian along sparse directions, as a coexisting claim, by reusing the
population-to-sample bridges of ticket W3-DIST (B0, B1, B2-core, B2, B3) and the random-design interface (item 6) of
W3-POST Theorem 1.

**Read (paths relative to the worktree root):**
1. `Theory_work/Wave3/W3-D3/STATEMENT.md` (the object to lock), `PLAN.md`, `TARGET.md`.
2. The recorded row 1.2: `Theory_work/Wave3/W3-READER/READER_VERSIONS.md` lines 26-30 ((S1), (S2)) and 257-320 (Theorem 2);
   `Theory_work/Wave3/W3-READER/NOTATION.md` §§1–2; card row `Theory_work/Wave3/W3-READER/CLAIMS_CARD.md:55`; its bridge
   `Theory_work/Wave2/W2-APP/lemmas/L1_POST.md` (the Gaussian steps).
3. The master: `Theory_work/Wave3/W3-POST/STATEMENT.md` lines 16-100 (§0 target; Theorem 1, hypotheses, item 6).
4. The bridges: `Theory_work/Wave3/W3-DIST/STATEMENT.md` lines 385-417 and the proof files
   `Theory_work/Wave3/W3-DIST/work/E_bridges/B0.md`, `B1.md`, `B2core.md`, `B2.md`, `B3.md`.
5. Set sizes: `Theory_work/Wave3/W3-READER/lemmas/R1_set_sizes.md` (B1.2, B1.3).
Registry statuses (quoted; do not open the registry): `W3-POST:Thm-1@1.0.1` "PROVED-CHECKED; council C3, …";
`W3-DIST:B0, B1, B2core, B2 @1.0.1` "PROVED-CHECKED; council R2, …"; `W3-DIST:B3@1.0.1` "PROVED-CHECKED, conditional on
W3-POST:Thm-1 (for its last sentence); council R2, …"; `W3-READER:R1@1.0.2` "PROVED-CHECKED; council R3, …".

**Questions.** Try to break the statement.
- Theorem 2SG: do (A1)–(A4) imply every hypothesis of Lemma B3w and of W3-POST Theorem 1 item 6 (including regime R1,
  ε independent of (X, θ*), p_ret vs p, s₀ ≤ K, measurability of the events)? Is any hypothesis used but not stated?
  Are the conclusions exactly those of the recorded Theorem 2, and do they follow from items 1–4 under item 6?
- Lemma B3w: are the constants (M_E, φ₀², g₀, M_n), the window w_n and the probability bound faithful to what B1, B2-core,
  B2 (a) and R1 give? Is the window large enough for every set the proof needs (sets S₀ ∪ J with |J| ≤ j₀ and with
  |J| ≤ m♯_n), and does the B2-core size condition w_n log(ep/w_n) ≤ c₂n/K⁴ hold for n ≥ n₁(s₀, A, K)?
- Proposition ExSG: true as stated (including the three K = 1 examples)?
- §0: is the setting a faithful delta over the recorded one (model, p as the number of columns before removal,
  conventions for π(S₀), PIP_j when a column is removed)? Is "Σ_n a correlation matrix" an honest reduction here?
- §8 tag STRONGER against the recorded reader statement: right? List any way in which Theorem 2SG is weaker.
- §5 (outside the registered spans, for HQ): are the two verbatim quotations and the stated relations to (A4) accurate?
  (NH14 = Narisetty & He 2014, arXiv 1405.6545v1 p. 16; Song & Liang 2015 p. 953 — open the PDFs only if you can; say if
  you could not.)
- List every interpretive sentence ("hence …", "so …", "in particular …", readings) inside the claimed spans (§1, §2, §3)
  and give each a verdict (RIDER_RULES: such sentences must be moved out or checked).
- Readability (PROGRAM.md "Readability"): is Theorem 2SG a clean reader statement?

**Reply.** Write your reply to `Theory_work/Wave3/W3-D3/reviews/L1_statement_lock_sol.md`: verdict line
`LOCK` / `LOCK-WITH-AMENDMENTS` / `NO-LOCK`; findings numbered L1-1, L1-2, …, each tagged C (correctness), S (strength:
claims more than proved or uses an unstated hypothesis), F (faithfulness) or E (editorial), with the line and the fix;
answers to the questions above. Then end.
