# R2 diff-round review — seat `opus` (Claude Opus 5.5, high) — W3-AUDIT track A, batch T1–T10

Content reviewed: the frozen round R2 = R1d, `MANIFEST 93b6cfc7c2451428ff253b282561225273b9e54cf227520a6a80a1433a8110ff`
(`manifest.py verify … MANIFEST_R1d.txt` → `verify: OK`, run at the start of this review; `MANIFEST_R2.txt` is
byte-identical to `MANIFEST_R1d.txt`). Core = pin: `git diff --quiet 4676af6 -- Scripts/SMC_BVS/core` is clean.
`INPUTS_R1d.txt` differs from `INPUTS_R1.txt` only in its comment line.

Files read:
- my own R1 review, `BRIEF_R2_opus.md` and `DIFF_R1_to_R1d.patch` (all of it);
- the changed files in full where the patch did not show enough context: T2 STATEMENT/PROOF, T8 STATEMENT/PROOF, the
  T9 STATEMENT setting;
- the dependents where they use a changed object: T4 PROOF *Blocks*, T6 Setting and PROOF:4, T3 STATEMENT:30-53 and
  PROOF:48, T10 STATEMENT:20-33 and PROOF §2 (i) and X9;
- T1 STATEMENT (GW-iii, GW-iv) and T5 STATEMENT (CAL-b, CAL-d), which T8 v4 now relies on;
- the newly cited external lines: C-DLV STATEMENT:20-30, TDP_E:25-45, W1-N3 STATEMENT:100-112,
  D_theorem.md:30-50, W3-SAMP STATEMENT:88-106, PC_completed.md:8-22;
- `cpp/v3_blocks.h:1-150`.

I did not open the other seat's review or any disposition.

## Verdict summary

The diff repairs T2 (the partition is now an abstract map 𝔪, and a new clause (BLK-d) identifies the compiled code with
it on non-overflowing, allocation-successful executions), T8 (the (D-iv) consequence is re-derived on the uninterrupted
run, with no actual-𝒜 step) and T9 (the (H4) execution premise is restored for statements about what the compiled code
returns). It propagates the T2 execution premise to T4 (Setting) and to T6 (Setting). Every change is correct, and none
breaks a dependent.

My R1 E findings were applied where the file changed (E2, E3, and parts of E4 and E6). The rest are queued in
`ERRATA.md` with the repair text I proposed, as PROTOCOL_v4 §5.3 allows. I have no C, S or F finding, old or new.

## 1. My R1 findings

| R1 finding | state | note |
|---|---|---|
| E1 (T10 claim header lacks the arithmetic premise) | NOT RESOLVED in text; deferred as ERRATA ER-1 (verbatim my repair) | Acceptable: T10 is unchanged and byte-identical. The diff makes the chain more explicit: T10 X9 → "under T4 ENC" → T4 v3 Setting (no integer overflow, allocations succeed; IDEAL-W, MACH). So G2 still passes and the ERRATA item stays editorial. |
| E2 (T8 consequence went through W3-SAMP's actual-𝒜 (D-iii)) | RESOLVED | See §2 (T8) for the check. The STATEMENT line "with 𝒜 ⊆ 𝒜°" is gone, and the PROOF no longer passes through 1_𝒜. |
| E3 (T8 "executed N_e, T, L") | RESOLVED | The definition now reads "frozen N_e, T, L (those of 𝓒°, i.e. of the uninterrupted run; an actual final run stopped by the guard may execute fewer stages)". (OVL-a) and (OVL-d)(ii) say "frozen" as well. No "executed" remains in T8 except in the changelog. (OVL-b)'s last sentence, "On 𝒜 the actual (N_e, T, L) … equal the potential ones (T5 CAL-d)", now refers to the actual *frozen* values, which are calibration-time fields, so CAL-d applies. Correct. |
| E4 (version labels) | PARTLY RESOLVED; rest deferred (ER-2, ER-3, ER-4) | T2's changelog is now in order (v4 rows before v5, then v6). T9's header is bumped (v3/v3). T1 PROOF, T3 STATEMENT and T10 PROOF are deferred to ERRATA because those files are unchanged. Acceptable. |
| E5 (T1 omits `checkUserInterrupt`, `cpp/v3_core.cpp:552`) | NOT RESOLVED in text; deferred as ER-5 (my repair) | Acceptable (T1 unchanged; no clause affected). |
| E6 (statuses not traceable within the inputs) | RESOLVED in substance; one pointer deferred (ER-6) | `STATUS_EXTRACT.md` is new. I compared all 23 rows with `Theory_work/INFRA/registry/claims.tsv` (sha256 prefix `13662be78cc743f3`, last commit `a8a135d6`, as the extract states). Version, state, status, file and lines match verbatim for every row. This includes W3-RM:E4, W3-START2-R:IF-START and W3-START2-R:OVL, the three statuses I could not trace in R1. T8's IF-START quote now points to the extract. The T3 E4-status pointer is ER-6. |

## 2. Does the diff break anything?

**T2 v6.** C(X) is now 𝔪(X, B), the `make_blocks` algorithm read over unbounded integers and exact reals. (BLK-a)–(BLK-c)
are unchanged as mathematics, and new (BLK-d) identifies the compiled code with 𝔪.
- I checked (BLK-d) against `cpp/v3_blocks.h:1-150`. All p²-array indexing is in `size_t`: `(size_t)b * p + a` at
  `:15`, `(size_t)j * p + i` at `:63, 71`, and `:83, 96-97, 103`. The allocations at `:12, 54` are `(size_t)p * p`.
- The only `int` products on p are `2 * p - 1` (`:49`), with `next_node` and the loop counters bounded by 2p − 1.
- `2 * p` overflows exactly when p ≥ 2³⁰, so "in range iff p < 2³⁰" is right for the expression as coded.
- The comparisons (`pair_less`) and the max-update (`:96`) are on doubles, and EX-A reads them as exact in both
  programs.
- So, on executions with no overflow and with successful allocations, the native blocks equal 𝔪(X, B).
- (BLK-a) concerns the R-level B (`v3_isqrt`). The new header sentence "(BLK-a)–(BLK-c) concern the abstract map C(X)"
  is harmless for it.
- The binary64 remark is now scoped to (BLK-d) executions, which is consistent.
- The v6 changelog tag WEAKER (code identification) / EQUAL (abstract clauses) is right.

**T2 → T4 (blocks).** T4 v3 adds the same execution premise to its Setting, and PROOF *Blocks* now cites "T2 (BLK-d),
on the executions of the Setting". The premise covers the whole execution, so it also covers `build_tables` and
`start_mode`. ENC (a)–(c) are otherwise unchanged. The v3 changelog tag WEAKER is correct. No break.

**T2/T4 → T6.** T6 v2.1's Setting now says "C(X) (T2, on the executions of T4's Setting)". T6 PROOF:4 uses |C_b| ≤ B ≤ K
(BLK-a, BLK-b; ENC-a), which holds on those executions. (S), (Z) and (S′) are untouched, the PROOF is byte-identical
(`e5404b7dc54d`), and the tag EQUAL is right. No break.

**T2 → T10 §2 (i).** `check_B` needs B ∈ [1, 16], which comes from (BLK-a), the R-level B, independent of (BLK-d). No
break.

**T4 → T3 (start mode).** T3:32 still says `st` is "built from the partition C(X) of T2 (BLK)", without T6's new
execution qualifier. I checked whether any clause needs the native blocks to equal 𝔪(X, B):
- (OPC-a)–(OPC-c) are control-flow facts on completed runs.
- (OPC-d) needs 𝒦_n to be a function of (X, y). That holds for the coded setup → `start_mode` pipeline whatever its
  partition, because it uses no stream and no clock (T1 GW-i, T5 CAL-a).
- The only consumer that needs S̃₀ = S* is E4, and T3 routes it through "T4 ENC, and (H4)" ("Not claimed", T3:53). T4
  ENC now carries the premise.

So T3 is not broken. A pointer "(on the executions of T4's Setting)" at T3:32 would match T6 v2.1. That is a remark for
the ERRATA batch, not a finding (diff round: no new E).

**T4 → T9 setting; T9 v3.**
- The (H4) text matches its sources: TDP_E:33-34 ("(H4) integer counters fit, allocations succeed") and
  W1-N3 STATEMENT:106-109 (cap a positive `long`, K + 1, J + 1 and loop counters in `int`, |C_b| ≤ 31, allocations
  succeed, recursion completes).
- The "Two readings" split is sound. The DP and enumeration results and the costs are algorithmic statements; the
  "returns" statements are native and hold under (H4).
- (H4)'s integer and allocation parts follow from T4 v3's Setting (whole execution) together with |C_b| ≤ 16 (T2).
  Recursion completion is MACH. So the settings compose.
- The new (TDP-e) sentence ("never fires when execution reaches it … does not exclude allocation failures or
  process/stack failures (T10's X5 and MACH)") is accurate. It is what T10 X9 needs: the throw at
  `cpp/v3_start.h:261` is not reached, and allocation failures are already inventoried as X5.
- The v3 tag WEAKER for the native-return claims is right.

**T9 → T10 X9.** "X9 is unreachable (cap = 10⁶ ≥ 2 …; the root check passes by T9 TDP-e, under T4 ENC)" stays true on
the executions in T4's Setting, which are the IDEAL-W/MACH executions the C-DLV inventory is stated under (my E1 /
ER-1). No break.

**T8 v4 (consumer: W3-SAMP Theorem D (D-iv)).** I re-derived the new chain.
1. Pathwise inclusion:
   - On {completed} (sampler branch, ⊆ 𝒪), 𝒪 ⊆ 𝒜 ⊆ 𝒜° (T1 GW-iv).
   - The calibration record and every final island's statistical record equal P°'s (T1 GW-iii; `W3-SAMP:PC` (i)). So
     𝓜_r = 𝓜°_r, which is the set evaluated by P°'s island r run on 𝓒° and stream 9 + r. PC (i) explicitly includes
     rejected proposals in 𝓜_r (`PC_completed.md:18-20`).
   - Ŝ is the `hpm_better`-maximum of 𝓜 ⊇ 𝓜_r, with 𝓜 ⊆ Ω (PC (iii)).
   - Hence, by the deterministic step (`D_theorem.md:40-42`),
     completed ∩ {Ŝ ≠ S₀} ⊆ {S† ≠ S₀} ∪ (𝒜° ∩ {S₀ ∉ 𝓜°_r}).
2. Probability:
   - D-i (`W3-SAMP/STATEMENT.md:99-100`) is a statement about the potential island given the calibration record.
     T5 (CAL-b) makes it valid for (𝒜°, 𝓒°): 𝒜° ∈ σ(𝓒°), D_r is a function of 𝓒° (CAL-c), and the island's stream is
     not among streams 0–9 (H-U).
   - Integrating over 𝒜° gives P(𝒜° ∩ {S₀ ∉ 𝓜°_r}) ≤ E[1_𝒜°(1 − π₀(S₀))^{D_r}].
   - The final steps, (1 − x)^D ≤ e^{−Dx} and the e^{−c} + P(𝒜° ∩ {D_rπ₀ ≤ c}) split, are unchanged and correct.

   This is the bound I proposed in E2, reached more directly. It needs no clock measurability, and the tag EQUAL (same
   final bound) is right.
3. The consumer (D-iv) keeps its conclusion with P-OVL read on 𝒜°, which (OVL-b) and (OVL-d) supply.
4. The new citations, `D_theorem.md:40-42` and `W3-SAMP/STATEMENT.md:99-100`, are quoted correctly (CITECHECK 22/22 OK).

No break.

**Bookkeeping files.**
- The CHECK.md frozen-text hashes for T2, T4, T6, T8 and T9 match `sha256sum` of the files in the manifest:
  `2bc68097d046/59bb28806ce0`, `0a249f656260/7273c57b2095`, `0b5e2c57e5d9/e5404b7dc54d`, `f03afc297221/d8fa0b36fde8`,
  `ec3da65edd35/8eec9e60ec2b`.
- The CITECHECK totals (T2 91/91, T8 22/22, T9 37/37 OK) are consistent with the added citations.
- `ERRATA.md` maps my E1–E6 correctly.

**New findings: none (no C, S, F).**

Remarks for the ERRATA batch. These are not findings, since a diff round admits no new E:
- T6 STATEMENT header still says v2 while its changelog has v2.1 (same class as E4).
- T2 and T4 cite "IDEAL-W and MACH (`C-DLV/STATEMENT.md:24-25`)", but MACH is defined at `:27-30`. The range covers
  IDEAL-W only.
- T8's (OVL-c) quote "PROVED-CHECKED" for `W3-START2-R:OVL` could also point to `STATUS_EXTRACT.md`. The row is there
  and matches.
- T3:32 qualifier, as noted above.

## 3. Per-claim table

| id | decision |
|---|---|
| T1 GW (GW-i)–(GW-v) | ACCEPT |
| T2 BLK (BLK-a)–(BLK-d) | ACCEPT |
| T3 OPC (OPC-a)–(OPC-d) | ACCEPT |
| T4 ENC (ENC-a)–(ENC-c) | ACCEPT |
| T5 CAL-C (CAL-a)–(CAL-d) | ACCEPT |
| T6 START-X (Z), (S), (S′) | ACCEPT |
| T7 KER (KER-a)–(KER-d) | ACCEPT |
| T8 OVL (OVL-a)–(OVL-d), Consequence for (D-iv) | ACCEPT |
| T9 TDP (TDP-a)–(TDP-e), TDP-IMPL discharge | ACCEPT |
| T10 P1′, S.3′, D1 | ACCEPT |

## 4. Gates

No C, S or F finding of my own: **gates = PASS**.
- G1: the T2 (BLK-d), T8 v4 and T9 v3 steps were re-derived.
- G2/G3: the execution premises are now stated where used (T2, T4, T6, T9), and T10 is covered through T4.
- G4: the new quotations and the 23 status rows were checked verbatim.
- G6: the `v3_blocks.h` integer and index reading was checked.

## Overall score

**9.3 / 10.** The R1 C/S/F items the diff addresses are repaired cleanly and with correctly tagged changelogs. The
premise propagation to dependents is consistent. The status extract makes G4 checkable inside the package. I take
nothing off for the deferred E items.

## Not checked

- The HQ 11-16 "RIDER_RULES" ruling now cited in the T6–T9 CHECK.md rows ("better-theorem review skipped"). It is not
  an input; this is a process record, not a claim.
- Whether every `int`-overflow execution of `make_blocks` (p ≥ 2³⁰) ends in an exception before output. (BLK-d) does not
  claim it; it is IDEAL-W/MACH territory.
- The internal proofs of imported results (as in R1). I did not compile or run the C++.

COUNCIL-VERDICT round=R2 manifest=93b6cfc7c2451428ff253b282561225273b9e54cf227520a6a80a1433a8110ff seat=opus score=9.3 gates=PASS
