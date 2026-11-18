# W3-D3 — K1 line check brief (Opus 5.5 high, fresh, blind; saved before launch 2026-11-17)

You are the line checker (PROTOCOL_v4 §3 step 3, Tier B) for ticket W3-D3 in the git worktree /home/fb31/BVS-wt/W3-D3
(read-only for you except your reply file). Do **not** read `LOG.md`, `CHECKPOINT_1.md`, or any file in
`Theory_work/Wave3/W3-D3/reviews/` other than this brief and `STATEMENT_v1.0_to_v1.1.diff`. Do not change git state. Scratch
only in /home/fb31/BVS-wt/W3-D3/.rc_tmp/ (delete it at the end). Python with numpy, if you want to compute:
/home/fb31/SMC_Theory_Department/ci/venv-numerics/bin/python.

**What is claimed.** `Theory_work/Wave3/W3-D3/STATEMENT.md` v1.1: Theorem 2SG (§1; posterior concentration on a random design
whose rows are sub-Gaussian along sparse directions), Lemma B3w (§2), Proposition ExSG (§3). Proofs:
`Theory_work/Wave3/W3-D3/lemmas/B3w.md` (B3w) and `Theory_work/Wave3/W3-D3/lemmas/ASSEMBLY.md` (Theorem 2SG, ExSG).

**Consumed results (status quoted; treat them as true, but check that each is used within its stated hypotheses and that
every quotation matches its source):**
- `Theory_work/Wave3/W3-POST/STATEMENT.md` lines 16-100 (target §0; Theorem 1, regime R1, hypotheses (E), (F_λ), (F_w), (BM),
  items 1–3 and 6) — `W3-POST:Thm-1@1.0.1` "PROVED-CHECKED; council C3, …".
- `Theory_work/Wave3/W3-DIST/work/E_bridges/B0.md`, `B1.md`, `B2core.md`, `B2.md` (part (a) and its proof identity) —
  "PROVED-CHECKED; council R2, …"; `B3.md` (the template that B3w adapts; its amendment A-2) — "PROVED-CHECKED, conditional on
  W3-POST:Thm-1 (for its last sentence); …".
- `Theory_work/Wave3/W3-READER/lemmas/R1_set_sizes.md` B1.2, B1.3 — `W3-READER:R1@1.0.2` "PROVED-CHECKED; council R3, …".
- Setting: `Theory_work/Wave3/W3-READER/READER_VERSIONS.md` lines 26-30 and 257-290 (recorded Theorem 2), `NOTATION.md` §§1–2.

**Tasks.**
1. **Line check** every step of `lemmas/B3w.md` (Steps 0–6, statement (a)–(c)) and `lemmas/ASSEMBLY.md` (Steps 1–4; ExSG (a),
   (b) including the in-place proof of Hoeffding's lemma). For each step: VERIFIED / VERIFIED-WITH-AMENDMENTS / GAP / FALSE.
   In particular: the window arithmetic of Step 0 (every set the proof needs has size ≤ w_n; the B2-core size condition for
   n ≥ n₁); the constants M_E, φ₀² = φ²/4, g₀ = φ²/8, M_n (units after the scale reduction B0); the completed pair and the
   measurability of 𝒜′_n (B3w (c)); the transfer from completed to actual outputs (ASSEMBLY Steps 3–4), including the
   conventions of STATEMENT §0 for removed columns; that every hypothesis of item 6 (and of R1) is met.
2. **Statement vs proof.** Does each proof prove exactly its statement in STATEMENT v1.1 (quantifiers, constants, the
   dependence of n₁ on (s₀, A, L) only)? Is any hypothesis used but not stated?
3. **Statement-change check (PROTOCOL_v4 §4.2) of v1.0 → v1.1**, from `reviews/STATEMENT_v1.0_to_v1.1.diff` and the changelog
   at the foot of STATEMENT.md: confirm or contest each row's tag. Of special interest: ExSG (b) (bounded features, L = K;
   tagged STRONGER on the companion claim) and the claim that the symbol change, the interface part (c) and the conventions
   are EQUAL for Theorem 2SG.
4. **Interpretive sentences.** List every "hence/so/in particular/this means/reading" sentence inside the claimed spans
   (STATEMENT §§1–3) and give each a verdict (checked / move out).
5. Read STATEMENT §5 (outside the spans): is each mathematical relation stated there (NH14's rows as the case Σ = I after
   centring; (A4) ⇒ Song–Liang Condition 1 for z = x − m_n; the converse fails; the 2b sentence) true as worded? You need not
   open the papers; the quotations were verified at the lock.

**Reply.** Write `Theory_work/Wave3/W3-D3/reviews/K1_linecheck_opus.md`: verdict line per file (VERIFIED /
VERIFIED-WITH-AMENDMENTS / NOT VERIFIED); findings numbered K1-1, K1-2, …, each tagged C (correctness), S (strength:
claims more than proved, or an unstated hypothesis), F (faithfulness to a source) or E (editorial), with file:line and the
fix; the per-step table; the statement-change table (row → CONFIRMED / CONTESTED); the interpretive-sentence list. Then end.
