Extended PURE check (v2, with the HQ rider: B3's later steps use only the two stated properties of the redefined event) of `T5/T5-R3_correction.patch` (fresh Opus subagent, claudeAgent_personal, high). The v1 mechanics-only check is kept as `T5-R3_PURE_check_opus_v1_mechanics.md` (PURE). Verbatim report (harness indent removed):

PURE-VERDICT: PURE

1. Mechanics: `git apply --check` passes from the repo root. The patch has one hunk (`@@ -95,8 +95,8 @@`) that replaces lines 98-99 with 2 lines, so the file stays at 104 lines. STATEMENT.md:409-414 is not touched, and the patch text matches the HQ brief.
2. Uses of 𝒜′_n, 𝒜_n and {p_ret = p} after the amendment:
   - L24-25 (statement): "(X, θ*)-measurable events 𝒜′_n ⊇ 𝒜_n". The measurability is P1: in item 6, (X, θ*) means the pair fed to the theorem, which is now the completed pair. The inclusion is P2.
   - L78 (Step 6): "ε independent of (X, θ*)". P1, plus the preserved fact that the completed pair is a function of the raw design only (A-2 L101).
   - L78-82 (Step 6 definition and measurability argument): superseded by A-2. The new wording defines 𝒜′_n on the completed pair with m♯_n from (n, p, s), and claims P1.
   - L82 "By Steps 1–5, 𝒜_n ⊆ 𝒜′_n": P2. It holds because 𝒜_n ⊆ 𝓔₁, and on 𝓔₁ the completed pair equals the actual pair, p_ret = p and |supp θ*| = s. That agreement is covered by the preserved L102 sentence.
   - L82-83 (R1 holds): uses p ≥ 2 (A2) on the fixed-p completed pair and s ≤ K. It uses neither P1 nor P2, and nothing beyond them is assumed about 𝒜′_n.
   - L86 "P(𝒜′_n) ≥ P(𝒜_n) → 1": P2 only.
   - L66-67, L84, L23 (Step 4 Remark, DIST-3, (vii)): use only 𝒜_n (through 𝒜_n ⊆ 𝓔₁ and B2 (e)), not 𝒜′_n.
   - L100 "outside {p_ret = p}": defines the replacement. It is not a property of 𝒜′_n, and {p_ret = p} is no longer intersected into 𝒜′_n.
   - L102-104 transfer: "agrees with the actual objects on the event of B1" is the preserved sentence about 𝓔₁. The "added error at most the probability of the complement" holds under either reading: P(𝒜′_nᶜ) ≤ P(𝒜_nᶜ) (P2), or P(𝓔₁ᶜ) ≤ P(𝒜_nᶜ) (𝒜_n ⊆ 𝓔₁). Both tend to 0 by (vii)/L86, so the sentence is still true as written.
3. No use of a property of 𝒜′_n outside P1 and P2 was found. The removed "∩ {p_ret = p}" is not relied on anywhere later.
4. Small wording notes, not defects:
   - L15 and L79 still say "m♯_n computed with p_ret". This agrees with the new (n, p, s) version on 𝓔₁ ⊇ 𝒜_n, and A-2 overrides it for 𝒜′_n.
   - L25 says "(X, θ*)-measurable", which here means measurable in the completed pair.
5. Consumers stay consistent:
   - STATEMENT.md:409-414 states the item-6 events only at the level "the events of [W3P] Theorem 1 item 6 hold with common constants". It says nothing about p_ret or the intersection.
   - The DEPS row `B3` (B1, B2-core; W3-POST:Thm-1@1.0.0 item 6) is unchanged. Its fingerprint 47ffb2b603de5cc0 belongs to the file, which is listed in MANIFEST_R2r, so the file needs the re-freeze already recorded in the patch header, as for any CORRECTION-ONLY patch.
