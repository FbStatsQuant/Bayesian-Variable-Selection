# API-POS: referee-response task R3 (MIX-POS)

Copied verbatim from `theory/F-REFEREE:theory_campaign/F-REFEREE/RESPONSE_PLAN.md` §3, task R3. Run `git fetch origin` and read the branches it names; also read the campaign synthesis `theory/W8-SYNTH:theory_campaign/W8-SYNTH/SYNTHESIS.md` for the current state, and the open PR branch `theory/E-SPINE` (the story is now 'moving off the start is needed', not 'tempering is needed').

### R3. MIX-POS: positioning against the rapid-mixing literature

**Paper role:** the "Relation to computational guarantees" paragraph (M6). Reading and reasoning only.

**Claim to settle.** Whether LH (exact Gram and iid) satisfies the hypotheses of (a) Yang, Wainwright & Jordan (2016,
AoS 44(6)) and (b) Zhou, Yang, Vats & Roberts (2022, JRSS-B 84(5)); and, if so, what their theorems conclude on LH (mixing
time in n, p; starting state requirements; model-size bound s; the beta-min constant). Then state precisely what
Theorem 5 adds and what it does not. Also check Zanella & Roberts (2019) §4.5 and Griffin, Łatuszyński & Steel (2021,
Biometrika) for the same purpose. Verify every citation against the source PDF (titles, volumes, theorem numbers,
hypothesis names); the referee report quotes them from memory and says so.
**Inputs.** The papers (fetch to `Papers/` if absent and record the source); W1-EXP §4 (LH); T03♯ hypotheses; T38(c).
**Deliverable.** `theory_campaign/MIX-POS/REPORT.md`: a hypothesis-by-hypothesis table (their condition | holds on LH? |
proof or counterexample), their conclusion on LH, a draft of the paper paragraph (≤ 250 words) and a draft of the
one-sentence contribution statement. Honest status: if their results subsume HPM discovery on LH, say so.

**Web access:** you may use web search/fetch for primary sources; never invent citations; say which sources you actually read.
