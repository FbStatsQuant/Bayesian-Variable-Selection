# W3-READER — CHECKPOINT 1 (lead: Claude Opus 5.5, Claude Third, Owls; 2026-11-15)

Tier B (PROTOCOL_v4). No new key lemma appeared (all NEW bridges are arithmetic, a one-paragraph variance bound, and a
premise-matching assembly). HOLDS: none at any step (`Theory_work/Wave3/HOLDS.md`, worktree and main checkout).

## Deliverables (all in `Theory_work/Wave3/W3-READER/`)
| File | Content |
|---|---|
| `CLAIMS_CARD.md` | 9 rows (8 results + DIST placeholder): plain statement, verbatim status, what it buys, reader-version verdict, HQ notes |
| `READER_VERSIONS.md` | Theorems 1–9: reader statement, one line per assumption, master (id@version, file:lines, status), bridges marked, honest limits; bridge summary table |
| `NOTATION.md` | reader-facing setup and notation (model, prior as coded, posterior, outputs, design quantities, asymptotics, table) + internal traceability |
| `METHOD_INTUITION.md` | stage-by-stage overview, pipeline figure sketch, theorem-to-stage map, toy example; code pins (traceability) |
| `helpers/CODE_FACTS.md` | helper H1 (Opus 5.5, Claude Third): code-pinned facts, spot-checked by the lead |
| `numerics/toy_example.py`, `toy_example_out.txt` | toy example (leakage undone by the search from the start mode) |
| `reviews/S1_frozen/` + `MANIFEST_S1.txt`; `reviews/S1_fidelity_sol.md`; `reviews/S1_disposition.md` | the Sol fidelity read and its disposition |
| `LOG.md` | heartbeat |

## 1. The card (summary; full card in `CLAIMS_CARD.md`)
| # | Result | Status (verbatim, first clause) | Reader version |
|---|---|---|---|
| 1 | Posterior concentration, fixed design: $1-\pi(S_0\mid y)=O_P(\sqrt{\log n/n})$, HPM = MPM = $S_0$ | `W3-POST:Thm-1@1.0.0`: "T03♯: PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)" (council C3 passed; label pending) | clean |
| 2 | Same, random Gaussian design | + `W2-APP:POST@1.0.1`: "PROVED (by this seat, unchecked); R02 VERIFIED-WITH-AMENDMENTS, applied" | clean; unchecked input |
| 3 | Rate cannot be improved (every design; $\sqrt{\log p}$ attained) | `W3-PSHARP:B`, `:A`: "PROVED-CHECKED; …" | clean, no bridge |
| 4 | Omitted variables: concentration on the projected support, any residual variance | `W3-MISR:Cor-G(b)@1.0.0`: "PROVED-CHECKED, conditional on W3-POST2:C, W3-POST2:E, W3-POST2:A1, W3-POST2:A0, …" | clean; conditional |
| 5 | Start law concentrates ($1-n^{-c}$, $c<\tfrac12$, optimal) | `W3-START2:START-R@1.0.0`: "PROVED-CHECKED" | primitive, long; body theorem |
| 6 | **Main:** reported model $=S_0$, Gaussian rows, leakage up to $n^b$; always output | `W3-RM2:RM2-R`: "PROVED-CHECKED, conditional on W2-APP:POST; …" + RM-0, F-UNI "PROVED-CHECKED" | primitive, long |
| 7 | Reported model, fixed design | `W3-RM2:RM2-F`: "PROVED-CHECKED, conditional on SOP:TH09; …" | honest limit (sample-level) |
| 8 | Certified screening | `W3-SCR:A1@1.0.0`: "PROVED-CHECKED" | clean, no bridge |
| 9 | Distribution consistency | W3-DIST candidate (CP1), not proved | placeholder |

## 2. Bridges, ranked by importance and cost
| Rank | Bridge | Theorems | Mark | Importance | Cost | Who |
|---|---|---|---|---|---|---|
| 1 | `W2-APP:POST@1.0.1` (LSF ⇒ posterior events, Gaussian rows) | 2, 4, 6 | EXISTS-UNCHECKED | critical: every random-design headline | 1 Sol line check (84-line lemma) | **HQ-queued** (HQ_NOW sharp2 riders) |
| 2 | POST2 C/E/A1/A0 council diff round | 4 | EXISTS-UNCHECKED | high | council diff round on a frozen manifest | **HQ** (identified 11-15) |
| 3 | `SOP:TH09`/`W3-POST:Thm-1` registry label | 1, 7 | label | high (headline 1 reads "label pending") | HQ attestation (council C3 passed) | **HQ** |
| 4 | Delivery assembly (B6.6, B7.4): RM2 conclusions ⇒ F-UNI premises (S), (P), (V); method-premise table | 6, 7 | NEW | high: turns "if output then $S_0$" into $P(\hat S=S_0)\to1$ | ~1 page + premise table | W3-READER (Opus) |
| 5 | Local regressions ⇒ variance clause (B6.3) | 6 | NEW | medium | ½ page (proof already in READER_VERSIONS §6) | W3-READER |
| 6 | Set-size arithmetic (B1.1–B1.3, B2.1, B4.1, B6.1) | 1, 2, 4, 6 | NEW (arithmetic; B1.3 also cites [T03R] E2(ii)) | medium: makes statements explicit | 1 page + numeric check (done) | W3-READER |
| 7 | Gaussian nulls ⇒ (W-sph) (B3.2) | 3 | NEW (one line) | low | trivial | W3-READER |
| 8 | Raw-scale coefficients for Theorems 5–6 (B6.7) | 5, 6 | NEW (optional) | low–medium | medium | not proposed |

## 3. Plan for proving the NEW bridges (Tier B)
1. **Write** `lemmas/R1_set_sizes.md` (rank 6 + 7), `lemmas/R2_local_regression.md` (rank 5),
   `lemmas/R3_delivery_assembly.md` (rank 4: a premise-by-premise table of `W2-UNI:F-UNI` against RM2-F/R's
   configuration and the shipped code; the union bound for (S); input validity). One Opus leg, ~3–4 h. Each file
   carries "PROVED (by this seat, unchecked)" until checked.
2. **Line check** by Sol (one Tier-B check covering R1–R3), with a disposition file.
3. **Statement fixes** from S1 (§4) into `READER_VERSIONS.md` v0.2; STATEMENT-style changelog (STRONGER / WEAKER /
   EQUAL per edit).
4. **CP3 council** (v4): gate F (reader version = master + bridges) on a frozen manifest with the masters as inputs;
   HQ and the consultant check readability on the card (PROTOCOL_v4 H5).
5. Not ours but gating the card: ranks 1–3 (HQ).

## 4. Sol fidelity read (S1)
*Pending at the time of writing; filled in below when `reviews/S1_fidelity_sol.md` arrives.*

## 5. Decisions for HQ
1. **Headline list** (owner via consultant, H5): adopt rows 1–4, 6, 9 as abstract-level; 5, 7, 8 as body theorems?
2. **Theorem 6 length**: keep the full population list in the theorem (faithful) and a one-line verbal summary in the
   abstract — recommended.
3. **Theorem 7**: main text uses the explicit version (a) ($|Q\setminus S_0|\le(1-\delta)\log n$); version (b) as the
   strengthening — recommended.
4. **Sampler results**: add a 10th row ("printed PIPs and $\hat Z$ are consistent/unbiased") or keep them in the body?
5. Go for the proof leg of the NEW bridges (§3), Opus, Tier B.
