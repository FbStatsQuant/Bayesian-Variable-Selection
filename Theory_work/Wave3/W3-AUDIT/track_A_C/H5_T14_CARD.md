# H5 card — T14 REP into row 3.1 (D88) — **STRONGER**

Against: claims card v1.12, `Theory_work/Wave3/W3-READER/CLAIMS_CARD.md` at main 128e6a9a (row 3.1, line 69; reader
note line 109-110). Source: W3-AUDIT `track_A_X/T14_REP` (Lemma REP; Sol line check VERIFIED; council XR2 bound,
MANIFEST 5db04d3a…, sol 9.4 / opus 9.5); registry label is HQ's call. Row 3.2 needs no edit: its delivery clause is
"as 3.1, including its sentence on the two fixed integer limits" (line 70).

## Edit 1 — row 3.1, the integer-limit passage (replace the whole passage)
**Before** (v1.12, verbatim):
> The delivery statement idealises two fixed integer limits in the code (a base search cap of $10^6$, `v3_run.R:96`,
> and a 32-bit integer bound $2^{31}-1$ on the search cap, `cpp/v3_core.cpp:474`): the first can bind only when $n+p+1$
> exceeds $2^{10^6}$, the second only when the starting model has more than about $2.1\times10^9$ variables, which
> needs $n\gtrsim4.3\times10^9$ since $|\tilde S_0|\le\lfloor n/2\rfloor$; without the idealisation, delivery holds on
> the bounded domain $\mathfrak D=\{\lceil\log_2(n+p_{\mathrm{raw}}+1)\rceil\le10^6,\ \lceil\log_2(n+p_{\mathrm{raw}}+1)\rceil+\lfloor n/2\rfloor\le2^{31}-1\}$,
> and with it (IDEAL-W⁺) for every $n$ [RM2R-5]. Neither limit can bind unless $n+p+1>2^{10^6}$ or $n\gtrsim4\times10^9$,
> that is, at no feasible problem size [RM2R-6].

**After:**
> The delivery statement lifts two fixed integer limits in the code (a base search cap of $10^6$, `v3_run.R:96`, and a
> 32-bit integer bound $2^{31}-1$ on the search cap, `cpp/v3_core.cpp:474`); this idealisation, IDEAL-W⁺, costs nothing
> on any input the software can receive ($n, p \le 2^{31}-1$): R stores matrix dimensions as 32-bit integers, so in
> the shipped default configuration the base cap is $\lceil\log_2(n+p+1)\rceil\le32$ and the search cap at most
> $32+\lfloor n/2\rfloor\le2^{30}+31$, and neither limit can fire [T14-REP]. Every such input lies in the bounded domain
> $\mathfrak D=\{\lceil\log_2(n+p_{\mathrm{raw}}+1)\rceil\le10^6,\ \lceil\log_2(n+p_{\mathrm{raw}}+1)\rceil+\lfloor n/2\rfloor\le2^{31}-1\}$,
> on which delivery holds without IDEAL-W⁺ [RM2R-5]. IDEAL-W⁺ is used only by the asymptotic form ($n\to\infty$),
> whose large inputs exceed R's limits and already run on the idealised machine IDEAL-W.

## Edit 2 — reader note on 3.1 (line 109-110), for consistency
**Before:** "with the delivery conventions (S4) of C-DLV: on the bounded domain, and for every $n$ only under IDEAL-W⁺
[H5-7.3, FUNI-N]."
**After:** "with the delivery conventions (S4) of C-DLV: on every input the software can receive ($n, p\le2^{31}-1$,
all in the bounded domain), and for every $n$ only under IDEAL-W⁺ [H5-7.3, FUNI-N, T14-REP]."

## Tag: STRONGER
"Neither limit can bind … at no feasible problem size" (an informal remark, [RM2R-6]) becomes a proved code fact for
every R-representable input in the shipped default configuration. No premise is added or dropped: the 𝔇 clause and
the IDEAL-W⁺ clause of DLV-0 are unchanged; T14 shows representable inputs ⊂ 𝔇. Kept qualifications: default options
only (`v3.ls0_ell` unset; a user value > 10⁶ makes the validator fire by design); IDEAL-W's other integer obligations
(e.g. `2 * p - 1` in `int` for p ≥ 2³⁰) are unchanged. Never written as "IDEAL-W⁺ = IDEAL-W".

## Changelog line (v1.13 proposal)
v1.13 = v1.12 with [T14-REP] (W3-AUDIT track_A_X/T14_REP, XR2 bound): row 3.1 integer-limit passage and reader note —
IDEAL-W⁺ costs nothing on any input the software can receive ($n, p\le2^{31}-1$) — **STRONGER** (remark → proved).

## Source tag
[T14-REP] W3-AUDIT `Theory_work/Wave3/W3-AUDIT/track_A_X/T14_REP/{STATEMENT,PROOF}.md` (branch theory/W3-AUDIT), Lemma
REP (REP-a), (REP-b); code pin 4676af6 (`v3_run.R:95-97`, `cpp/v3_core.cpp:92, 473-474`).

## NARROW-note line (for the 19-claim NARROW)
"A:IDEAL-W⁺ costs nothing on any input the software can receive (n, p ≤ 2³¹ − 1): there the two predicates it lifts
are false in the shipped default configuration (T14 REP); the narrowing matters only for the asymptotic form beyond R's
limits."

## Consultant edits (H5 card 16, AGREE, binding; HQ 2026-11-16). They supersede Edit 1 and Edit 2 above where they differ.
1. **No overclaim.** Representable inputs still carry IDEAL-W obligations (e.g. `2*p − 1` in `int` for p ≥ 2³⁰). On 𝔇,
   delivery holds "under the remaining conventions (S4), without IDEAL-W⁺". Never imply that representable inputs need no
   idealisation at all.
2. **p_raw, not p:** write "n, p_raw ≤ 2³¹ − 1" (𝔇 is written in p_raw).
3. **Row 3.1, one sentence (replaces Edit 1's "After"):**
   > The delivery statement lifts two integer limits of the code (IDEAL-W⁺); in the default configuration neither can be
   > reached on any input R can represent ($n, p_{\mathrm{raw}} \le 2^{31}-1$) [T14-REP], so this matters only for the
   > $n\to\infty$ form.
   The caps (base cap ≤ 32, search cap ≤ 2³⁰ + 31), 𝔇, the code line references (`v3_run.R:96`, `cpp/v3_core.cpp:474`)
   and "on 𝔇 delivery holds under the remaining conventions (S4), without IDEAL-W⁺" move to the reader note on 3.1
   (Edit 2), with p_raw throughout.
Applied by W3-READER in its editorial round (B3), after T14 is recorded. Tag stays STRONGER.
