# SHARP3 — triage of the 5 sharpness verdicts (W3-SAMP:D, LT♯, C, TR; W3-SCR:A1) — W3-READER leg 2, 2026-11-16

Author: W3-READER lead (Claude Opus 5.5, high). Inputs: `api/sharp3/f00–f04.md`, `VERDICTS.tsv` (HQ batch; also on main
at `Theory_work/Wave3/API_AUDIT/sharp3/`); the lemma lines each proposal cites (checked lines listed per item); the
W3-SAMP and W3-SCR STATEMENT and ASSUMPTION_MAP; the code where a proposal depends on it. Classes as
`API_AUDIT/sharp2/TRIAGE.md`: **A1** real and cheap, worth doing · **A2** cheap but low value · **B** real but known,
later ticket, superseded or out of scope (**B\*** known, undone, cheap) · **C** wrong, not an improvement, or
cosmetic/restatement · **D** unclear or open, needs a proof agent. Disposition rule (manager): real and cheap
improvements become **rider tickets after the freeze** unless they are trivial restatements; every proposal is
recorded in the better gate of rows 3.6 / 3.7.

## 0. Summary
- **5/5 IMPROVABLE-EASY; about 6 real findings, the rest restatements or constants.** As in sharp1/sharp2 the referee is
  generous: most "EASY" items state what the proof already gives or drop an unused premise.
- **No correctness problem found.** Every step I checked holds as written (§6); nothing escalated.
- **The two items the manager asked to settle:**
  1. **NC_r "for every island" in LT♯: not an extra requirement.** Given the calibration, the four final islands are
     identically distributed: the engine call `E.run_island(r, …)` uses `r` only to select the random stream
     (`Scripts/SMC_BVS/core/cpp/v3_core.cpp:444`, stream 9 + r) and to label the record (`cpp/v3_engine.h:278, 282`), and
     each stream is i.i.d. uniform and independent of the calibration (SI per island, `Theory_work/Wave1/W1-N1/STATEMENT.md`
     §2). Hence $P(\mathcal A\cap\{W_r<\eta\})$ does not depend on $r$, and NC_r for one $r$ is equivalent to NC_r for
     all $r\le4$. The HPM clause already uses island 1 only (`W3-SAMP/lemmas/LT_theorem.md:74-76`); the MPM clause
     tolerates one collapsed island (f01 (a)1, checked against LT Step 4); only the sup-norm PIP clause uses all four,
     which costs nothing by the equivalence. A weaker *pooled* non-collapse condition suffices for the HPM clause by a
     union bound ($P(S_0\notin\cup_r\mathcal M_r)\le4\delta/\eta+P(\bar W<\eta)$), which confirms the sharp1b f20 item.
     **Disposition: C (restatement) for "every r"; the pooled form A2 → remark at the next W3-SAMP edit.**
  2. **P-MAP in D: yes, localisable to $\mathcal A$.** The deterministic step (`W3-SAMP/lemmas/D_theorem.md:38-42`) gives
     $\{\text{completed}\}\cap\{\hat S\neq S_0\}\subseteq(\{\text{completed}\}\cap\{S^\dagger\neq S_0\})\cup(\{\text{completed}\}\cap\{S^\dagger=S_0\}\cap\{S_0\notin\mathcal M\})$,
     and $\{\text{completed}\}\subseteq\mathcal A$; so D-iii holds with $P(\mathcal A\cap\{S^\dagger\neq S_0\})$ in place of
     $P(S^\dagger\neq S_0)$, and D-iv needs only $P(\mathcal A\cap\{S^\dagger\neq S_0\})\to0$. **Disposition: C (trivial
     restatement; record in W3-SAMP's ERRATA at its next edit), no rider.** f00 route 1 (truth-free form, below) contains it.
- **One finding changes our own gate record (not a correctness issue):** f02's re-centring gives
  $E[|W_r-1|\mid\mathcal C]\le2\,\mathrm{TV}(\pi,\pi_0)$, attained at $N_e=T=1$. Consequence: P-START is **necessary**
  for Theorem C's evidence clause in C's stated scope (any frozen parameters), and an artefact only at production
  budgets. `GATES.md` row 3.6 necessity is revised accordingly (C2 in §3).

## 1. W3-SAMP:D (f00)
| # | proposal | checked against | class | disposition |
|---|---|---|---|---|
| D1 | Truth-free HPM exactness: $P(\text{completed}\cap\{\hat S\neq S^\dagger\})\le E[\mathbf 1_{\mathcal A}(1-\pi_0(S^\dagger))^{D_r}]$ | `D_theorem.md:6-29` (strong Markov, freezing: $S^\dagger$ is data-measurable, data fixed at the conditional level), `:38-42` (deterministic step uses only $S^\dagger\in\mathcal M$) — holds | **A1** | **rider after the freeze** ("SAMP-R1": restate D with target $S^\dagger$; a few lines). Gain: a purely computational statement, any design and sparsity. |
| D2 | Exact overlap $Q^*=D_r|\log(1-\pi_0(S_0))|$ in place of $Q_D$ | `D_theorem.md:56` relaxation $(1-a)^D\le e^{-aD}$ — holds | **A2** | gain only off production budgets ($D_r\to\infty$ in production makes them equivalent); remark at the next W3-SAMP edit |
| D3 | Set version of D-i | freezing step unchanged — holds | **C** | hook only; no gain alone |
| D4 | Method-level discovery (credit Gibbs/swaps/local search) | BT1 §3.2, deferred (`W3-SAMP/ASSUMPTION_MAP.md:36`) | **D** | open problem (needs design conditions); no ticket |
| D5 | KERNEL → its control-flow clause only | already said at `STATEMENT.md:97-98` | **C** | cosmetic |
| D6 | P-MAP localisation | see §0 item 2 | **C** | restatement (errata) |
| D7 | YWJ (2016) comparison: P-OVL plausibly unnecessary in the YWJ regime | referee is unsure it transfers (budget and size cap differ) | **D** | literature remark for GATES lit (row 3.6) |

## 2. W3-SAMP:LT♯ (f01)
| # | proposal | checked against | class | disposition |
|---|---|---|---|---|
| L1 | NC_r for every $r$ redundant | code + SI (§0 item 1) | **C** | restatement |
| L2 | Localise P-CONC to $\mathcal A$ in LT-e | `LT_theorem.md:66-76` uses $P(o_1>\epsilon/3)$, $P(\delta\ge\frac12)$; intersecting with $\mathcal A$ is valid since every other term carries $\mathbf 1_{\mathcal A}$ | **A2** | weaker hypothesis only when $P(\mathcal A)\not\to1$; in the post-freeze SAMP rider if opened |
| L3 | Drop "$o_1\le\frac14$" in LT-d via LT-b′ | LT-b′ gives $P(E_r\ge\frac12\mid\mathcal C)\le2g/\eta+P(W_r<\eta\mid\mathcal C)$ — holds | **A2** | same rider |
| L4 | LT-e′ ⇔ $\mathbf 1_{\mathcal A}o_1/W_r\to0$ | elementary equivalence — holds | **C** | restatement |
| L5 | $o_1/\eta$ trade-off attained (abstract IS witness) | abstract target, not the coded regression target | **D** | sharpness remark for LT-f |
| L6 | NC_r necessity: abstract witnesses both ways | abstract triangular arrays (TR converse example; trap sequence) | **D** | record as remark in LT-f ("abstract witnesses; coded realisation open") |
| L7 | **Rate under NC_r**: $\mathbf 1_{\mathcal A}o_1=O_P(r_n)$ + NC_r ⇒ $\mathbf 1_{\mathcal A}\|\mathrm{pip}-\mathbf 1_{S_0}\|_\infty=O_P(r_n)$ | LT-b′ $E[W_rE_r\mid\mathcal C]\le g\le21o_1$ and Markov — holds | **A1** | rider after the freeze (adds a rate route without P-START; not used by Theorem 10, which takes the C route) |
| L8 | Exact identity $E[W_r|\hat p_r(j)-\mathbf 1\{j\in S_0\}|\mid\mathcal C]=|\mathrm{PIP}_j-\mathbf 1\{j\in S_0\}|$; per-coordinate, $\ell^1$ forms | MR-c (`STATEMENT.md:112-113`) with $E[W_r\mid\mathcal C]=1$, $\hat p_r(j)\in[0,1]$ — holds | **A2** | same rider (cleaner sharpness statement) |
| L9 | Pool before Markov (constants ×4) | — | **C** | constants |
| L10 | NC_r from primitives via SMC variance bounds (conjecture) | not verified | **D** | open problem |

## 3. W3-SAMP:C (f02)
| # | proposal | checked against | class | disposition |
|---|---|---|---|---|
| C1 | **Re-centring: $E|W_r-1|\le2\,\mathrm{TV}(\pi,\pi_0)$**, no truth model; attained at $N_e=T=1$ | `C_theorem.md:34-52`: (1)–(3) hold for any centring constant; with $d^*=\log(\bar Z_1/\bar Z_0)$, $e^{a^*}=\pi/\pi_0$, $c=1$, $b_\pm=\mathrm{TV}$, so $\beta^*=2\,\mathrm{TV}$; at $T=1$ the coded $\hat Z$ uses only the initial draws (`cpp/v3_engine.h:316-322`), so at $N_e=1$, $E|W-1|=\sum\pi_0|w-1|=2\,\mathrm{TV}$ — holds | **A1** | **rider after the freeze** ("SAMP-R1", with D1, L7); also changes our necessity record (§5) |
| C2 | Necessity of TV → 0 for the evidence clause in C's any-parameter scope | from C1's attainment and $W\ge0$, $EW=1$ (convergence in probability ⇒ $L^1$) — holds | **A1** (as a sharpness record) | adopted now in `GATES.md` row 3.6 necessity; registry: P-START "NECESSARY-FOR-ROUTE (C's scope)" |
| C3 | C-ii untruncated, constant 2 | `C_theorem.md:25-30` — plausible, not re-derived | **A2** | rider (low value) |
| C4 | C-iv: $g+e_L\,\mathrm{TV}$ nesting TR-b | combines MR-b at $s=0$ with TR's Doeblin step — plausible | **A2** | rider |
| C5 | MPM $O(\bar\delta^2)$ under IND-T | union over two islands — plausible | **A2** | rider |
| C6 | Discovery $\delta_0^{N_e}$ not $\le\bar\delta$ | `C_theorem.md:58` already has the exponent — holds | **C** | restatement |
| C7 | $L^1$ mode free | bounded convergence — holds | **C** | restatement |
| C8 | $T=1$ addendum with $N_e$: $\min\{2\mathrm{TV},\sqrt{2M\,\mathrm{TV}/N_e}\}$ | not checked | **B\*** | park |
| C9 | $N_e$-dependent bound for general $T$; remove P-START for PIPs via mixing | open | **D** | open problem (also the honest-limit of Theorem 10) |
| C10 | log-tail coth constant | — | **C** | cosmetic |

## 4. W3-SAMP:TR (f03)
| # | proposal | checked against | class | disposition |
|---|---|---|---|---|
| T1 | **Keep $\|\mu-\pi\|_{TV}$**: hybrid bound $g+e_L(\delta+E[1-A^{br}_{r,T}])$; single premise $e_L(1-A^{br}_T)\to0$ | `TR_theorem.md:33-34` proves $(1-1/M)^L\|\mu-\pi\|_{TV}$ and then bounds the factor by 1 — holds | **A1** | rider after the freeze ("SAMP-R1"); unifies C, LT♯, TR |
| T2 | Concentration-free bias $|E\hat p_r(j)-\mathrm{PIP}_j|\le e_L$; rate clause; localised P-CONC | TV bound of TR-a; $o_j\in[0,1]$, $\pi(o_j)=\mathrm{PIP}_j$ — holds | **A2** | same rider |
| T3 | HPM/discovery clauses of TR dominated by D-iv | $\pi_0(S_0)\ge\pi(S_0)/M$ — holds | **C** | restatement (cite D) |
| T4 | Hoeffding across particles for MPM (needs product law given $\mathcal H$ from T12 (R3)) | not verified (the referee flags it) | **D** | open; proof agent if wanted |
| T5 | Local-move repair instead of global $M$ | open, needs design conditions | **D** | open problem |
| T6 | Minorisation $1/M$ sharp for the independence mechanism (Mengersen–Tweedie) | classical | **C** | literature remark (lit gate) |

## 5. W3-SCR:A1 (f04)
| # | proposal | checked against | class | disposition |
|---|---|---|---|---|
| S1 | Drop "fixed": add $\kappa b^2(n^2-1)\ge4\|\theta^*\|_2^2$; then $b_n\gtrsim\kappa^{-1}\sqrt{(M_n^2+\sigma^2)L_n/n}$ | `W3-SCR/lemmas/L3_screening.md:69` is the only use of fixedness ("let n be so large that …"); :70-75 uniform in $n$ — holds | **A1** | **rider after the freeze** ("SCR-R1"); reaches A1°'s rate from A1's proof |
| S2 | $\|\theta^*\|_1\le M$ → $\|X\theta^*\|^2\le M^2(n-1)$ and $\|\theta^*\|_2$ bound; $s_0$ may grow | $\ell^1$ enters only at L3:69-70 — holds | **A1** | same rider |
| S3 | Remove $M^2$ from $c_1$ via B2° + MC° | half-page rerun of L3:79-86, not checked | **A2** | same rider |
| S4 | Exponential rate $3e^{-c_3n}$ via SCR-A with $x\propto n$ | referee's own check; plausible | **A2** | same rider |
| S5 | Constant 200 → any $>64$ (proof as written) / $>4$ | L3:75 ($\rho^2\ge\kappa^2b^2/(64\tau_*^2c_1)$ needs only $>1$) — holds | **C** | constant |
| S6 | Necessity at $q=0$: linear cap in $\log p$, $\kappa^2b^2/\sigma^2$, $s_0L_n\lesssim n$ (via SCR-N) | SCR-N `STATEMENT.md:201-207` — referee's applications, plausible | **A2** (sharpness record) | adopted as remarks in `GATES.md` row 3.7 necessity |
| S7 | "$\|\theta^*\|_1\le M$ forces $s_0\le M/b$" vs "no bound on $s_0$" | true; A1 is a corollary with its own hypotheses (no error) | **C** | wording note for the reader version (Theorem 8 remark) |

## 6. Lines checked (no wrong mathematics found)
`W3-SAMP/lemmas/D_theorem.md:6-29, 36-58`; `LT_theorem.md:60-95`; `C_theorem.md:25-80`; `TR_theorem.md:26-36`;
`W3-SCR/lemmas/L3_screening.md:64-77`; code `cpp/v3_core.cpp:444`, `cpp/v3_engine.h:269-282, 316-322`.

## 7. Proposed post-freeze riders (for the manager)
- **SAMP-R1** (one Opus leg, ~½ day): D1 (truth-free D), C1 (TV re-centring, with C3–C5), T1–T2 (hybrid TR bound),
  L2, L3, L7, L8; errata D6, L1/L4. Effect on the card: row 3.6 conditions weaken (evidence clause under
  $\mathbf 1_{\mathcal A}\mathrm{TV}(\pi,\pi_0)\to0$; PIP clauses under the unified premise). READER_DELTA to row thm10.
- **SCR-R1** (one Opus leg, ~½ day): S1–S4. Effect: Theorem 8's (A2) becomes a beta-min at rate
  $\sigma\kappa^{-1}\sqrt{L_n/n}$ with bounded total signal, and the bound becomes exponential. READER_DELTA to row thm8.
