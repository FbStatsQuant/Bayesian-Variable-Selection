# W3-D2 — K1 line-check brief (Opus 5.5 high, fresh, blind; saved before launch 2026-11-17)

You are a blind line checker (PROTOCOL_v4 §3 step 3, Tier B) for ticket W3-D2 in the git worktree /home/fb31/BVS-wt/W3-D2.
Read-only except your reply file. Do not read LOG.md, CHECKPOINT_*.md or anything in `Theory_work/Wave3/W3-D2/reviews/`
except this brief. No git state changes; scratch, if any, only in /home/fb31/BVS-wt/W3-D2/.rc_tmp/ (delete at the end).

**Object.** `Theory_work/Wave3/W3-D2/PROOF.md` (P0–P4), proving `Theory_work/Wave3/W3-D2/STATEMENT.md` §1 (Theorem 2X with
clause (E)), §2 (Corollary 2X) and §3 (deterministic facts). Check every line: each step either follows, or is a citation
that says what the cited text says. Try to break it.

**Sources the proof cites (read the cited lines):**
- `Theory_work/Wave3/W3-MISR-R/STATEMENT.md` lines 25-46 (notation), 48-92 (§2: (N), (OV), CorG-min), 94-108 (§3, CorGb-plus:
  the master); its proof `Theory_work/Wave3/W3-MISR-R/lemmas/G2_corr.md` (constants, beta-min branch [R-3], non-empty T).
- `Theory_work/Wave3/W3-MISR/STATEMENT.md` lines 17-66 (§0: π_𝒞, configurations, constants), 108-123 (MIS-R (i) and its consequences).
- `Theory_work/Wave3/W3-POST/STATEMENT.md` lines 16-39 (coded target, outputs, m♯_n and its bound).
- `Theory_work/Wave3/W3-READER/lemmas/R1_set_sizes.md` (B1.3, B4.1).
- Recorded Theorem 2: `Theory_work/Wave3/W3-READER/READER_VERSIONS.md` lines 26-30 and 257-282; `Theory_work/Wave3/W3-READER/NOTATION.md` §1.
Registry (quoted; do not open the registry): `W3-MISR-R:CorGb-plus@1.0.1` "PROVED-CHECKED, conditional on W3-POST2:C,
W3-POST2:E, W3-POST2:A1, W3-POST2:A0, C-MIS:GDb, C-MIS:Prop-P; council R3, MANIFEST 052ea6df…, sol=10.0 PASS, opus=9.6 PASS";
`W3-READER:R1@1.0.2` "PROVED-CHECKED; council R3, MANIFEST 7aebdf2e…, sol=9.5 PASS, opus=9.4 PASS". Take these claims as given;
check that PROOF applies them within their hypotheses.

**Points to examine by name.** (1) The q = 0 instance of CorGb-plus (n × 0 matrix; (OV) with a = γ = τ² = 0 as a point mass).
(2) Identity of π_𝒞 with π. (3) The floor step: B4.1's domain (s ≤ K, n ≥ 3) and the threshold n* ≥ max(3, 2s₀).
(4) Dependence of C only on (s₀, A, M₀, c). (5) The deterministic facts P0 (HPM any tie rule; MPM strict threshold; S₀ ∉ Ω).
(6) Markov steps and b_n = O(r_n). (7) Corollary: energy bound via λ_max ≤ trace; beta-min; the recorded conclusions.
(8) STATEMENT §§1–3 faithfully copied in PROOF (no hypothesis used but not stated).

**Reply.** Write to `Theory_work/Wave3/W3-D2/reviews/K1_linecheck_opus.md`: a verdict per unit — P0, P1, P2, P3 —
VERIFIED / VERIFIED-WITH-AMENDMENTS / GAP / ERROR; findings K1-1, K1-2, …, each tagged C/S/F/E with line and fix; then one line
`K1-VERDICT: <overall>`. Then end.
