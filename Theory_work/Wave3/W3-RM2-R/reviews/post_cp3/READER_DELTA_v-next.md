# W3-RM2-R — READER_DELTA v-next (post-CP3; HQ card 14 AGREED, classification MIXED; HQ D74)

Written after CP3 under `reviews/post_cp3/` only (the ticket folder is frozen at MANIFEST_R3). No mathematics changes:
every sentence below restates `STATEMENT.md` v1.0 (locked) or the council-checked READER_DELTA v0.3 (R7.1–R7.4).
Base (read only): W3-READER `READER_VERSIONS.md` (rows thm6 v0.6, thm7 v0.4, standing conventions (S4)) and
`CLAIMS_CARD.md` v1.2, as of W3-READER commit 6a07d34c; copies in `base/` (sha256 prefixes 64214b22953bb883,
3cfd0b5595b17224). Merged result in `patched/`; `diff -u` in `READER_VERSIONS.diff`, `CLAIMS_CARD.diff`.
Markers in the merged text: [RM2R-1] (S4) additions, [RM2R-2] masters / method drift / bridges, [RM2R-3] thm6 error-split
remark, [RM2R-4] thm7 constant-level assumptions and remarks; [D71] marks the interpretive sentences, which stand outside
the theorem text as labelled interpretations.

## 1. Classification (card row 3.2 and the changelog read MIXED)
* **STRONGER:** Theorem 7's beta-min (A1), visibility (A3) and the (A5)(b) signal clause at the constant level (were
  θ*_min√(n/log n) → ∞, M_n → ∞, θ*²_min n/(|Q| + log n) → ∞); the core's mode form (RM0-plus: posterior input = S₀ is the
  unique score maximiser), in Theorems 6 and 7.
* **WEAKER:** the delivery clause now needs IDEAL-W⁺ (two code size ceilings lifted, added to (S4)(i)) and a narrower
  input domain (valid, non-degenerate input, added to (S4)(iv)); the implication edge DLV-0 ⇒ C-DLV:Prop-F is withdrawn
  (`W3-RM2-R/STATEMENT.md` dependency table).
* **EQUAL:** Theorem 6's assumptions (A1)–(A6); the output-conditional clause (which still leads, H5 card 14).

## 2. Method drift (rows 3.1 and 3.2; HQ D74)
C-DLV:Prop-F's method uses the LS0 move cap ℓ_n, not the shipped ℓ_n + |S̃₀|; the earlier delivery bridges to Prop-F and
W2-UNI:F-UNI (B6.6, B7.4) were therefore not about the shipped configuration as registered. Delivery for the shipped
method rests on W3-RM2-R:DLV-0 (code re-audited at the pin). In the merged text B6.6 and B7.4 are kept for the record and
marked superseded by the identities B6.6′ and B7.5 ((S4) ⇔ the delivery premises (D)).

## 3. Row 3.1 (Theorem 6) — conclusion and master change
Master: W3-RM2-R:RM2-R-plus (+ RM0-plus, DLV-0); it implies the previous master W3-RM2:RM2-R. The reader statement keeps
the output-conditional clause first; the delivery display is unchanged in form but now rests on (S4) as amended; the
error split is Remark (o). Card row 3.1 text: `patched/CLAIMS_CARD.md` row 3.1.

## 4. Row 3.2 (Theorem 7)
Assumptions (A1), (A3), (A5)(b) at the constant level with the constants in Remark (a) (M_V threshold, the 32/64 form of
the (A5)(b) clause, the (A5)(a) beta-min constant with a fixed D > 2 + 4A); error split in Remark (b); master
W3-RM2-R:RM2-F-plus; bridges B7.1′–B7.4′ (B7.2′, B7.3′, B7.4′ are R7.2–R7.4 of READER_DELTA v0.3, council-checked in
W3-RM2-R R2/R3).

## 5. Statuses
The masters' statuses are quoted from CP3 ("PROVED (by this seat, unchecked); …; LC-B VERIFIED", council R3 PASS) and
marked **requote verbatim once recorded** — the recorder's labels are to be pasted in place when W3-RM2-R is ingested.

## 6. Checks
`manifest.py verify` on MANIFEST_R3 after writing these files: see LOG (the ticket folder is untouched; `reviews/` is
outside the manifest).

## 7. Addition [RM2R-5] (manager, HQ wording rule): the two fixed integer limits, one sentence
Inserted after the delivery display of Theorems 6 and 7, in card row 3.1 (row 3.2 refers to it), and referenced from
(S4)(i):
> The delivery statement idealises two fixed integer limits in the code (a base search cap of $10^6$, `v3_run.R:96`, and a 32-bit integer bound $2^{31}-1$ on the search cap, `cpp/v3_core.cpp:474`): the first can bind only when $n+p+1$ exceeds $2^{10^6}$, the second only when the starting model has more than about $2.1\times10^9$ variables, which needs $n\gtrsim4.3\times10^9$ since $|\tilde S_0|\le\lfloor n/2\rfloor$; without the idealisation, delivery holds on the bounded domain $\mathfrak D=\{\lceil\log_2(n+p_{\mathrm{raw}}+1)\rceil\le10^6,\ \lceil\log_2(n+p_{\mathrm{raw}}+1)\rceil+\lfloor n/2\rfloor\le2^{31}-1\}$, and with it (IDEAL-W⁺) for every $n$ [RM2R-5].

Checked against Sol TR1 (`Theory_work/Dept/research/FUNI_transfer/TR1_sol.md` §1–2, THEORY-DEPT checkout) and DLV-0
(`W3-RM2-R/STATEMENT.md:80-89`, `lemmas/Q5_dlv0.md` (E5)). Adjustments to the suggested sentence: "n + p" → "n + p + 1"
(the base cap is ⌈log₂(n + p + 1)⌉ ≤ 10⁶); "about 2×10⁹" → "about 2.1×10⁹ … n ≳ 4.3×10⁹" (2³¹ − 1 − ℓ, and |S̃₀| ≤ ⌊n/2⌋);
the domain is written 𝔇, because in the master "(D)" names the delivery premises, not the domain (TR1 calls the same
set D, and its D_K ⊇ 𝔇 with min(p_raw, ⌊n/2⌋) in place of ⌊n/2⌋). 𝔇 is sufficient, not necessary (TR1 §2: exact-branch
inputs and small start modes outside 𝔇 also deliver). Not phrased as a limitation (owner rule).

## 8. Addition [RM2R-6] (HQ on IDEALW_BINDING): stated in the body as fact, right after the [RM2R-5] sentence
> Neither limit can bind unless $n+p+1>2^{10^6}$ or $n\gtrsim4\times10^9$, that is, at no feasible problem size [RM2R-6].

By the arithmetic of `IDEALW_BINDING.md` (no log grep needed, per HQ).
