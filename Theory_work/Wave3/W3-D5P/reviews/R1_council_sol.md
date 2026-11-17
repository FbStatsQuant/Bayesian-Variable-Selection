<!-- Council R1, seat sol: Codex gpt-6.1-sol, reasoningEffort high (pre-D122); brief reviews/BRIEF_R1_sol.md; MANIFEST 952d9840…; reply below verbatim -->
| id | decision |
|---|---|
| W3-D5P:LIST-K | ACCEPT |
| W3-D5P:LIST-CODE | ACCEPT |
| W3-D5P:LIST-R | REJECT |

LIST-R’s formal statement and L3 proof are valid conditional on IMPL-LIST. Its rejection concerns unfaithful derived text in the frozen review package.

**1. Findings**

1. **[F] The reader and card identify exact-branch PIPs with the wrong distribution.** [READER_DELTA.md:15](/home/fb31/BVS-wt/W3-D5P/Theory_work/Wave3/W3-D5P/READER_DELTA.md:15) defines the quantities by renormalising to the returned list, then applies them to every output run. [CARD.md:10](/home/fb31/BVS-wt/W3-D5P/Theory_work/Wave3/W3-D5P/CARD.md:10) likewise identifies list-renormalised probabilities with the printed fields without a branch distinction. SPEC §4 and STATEMENT §1 instead set exact-branch `pip_list = PIP` and `mpm_list = MPM`, irrespective of truncation of the enumeration’s store. A truncated store generally gives different PIPs. For example, with \(p=12\), \(K=12\), enumeration covers 4096 models while the store holds at most 481. The correct bounds for both branches do not establish the claimed identity of their definitions.

   **Fix:** Define the sampler fields by list renormalisation and the exact-branch fields by the exact posterior, as STATEMENT §1 does. Preserve this distinction in both proposals.

2. **[F] The derived texts overstate or leave unspecified the evidence error being bounded.** [CARD.md:14](/home/fb31/BVS-wt/W3-D5P/Theory_work/Wave3/W3-D5P/CARD.md:14) says the named fields, including `log_Z_list`, are within \(\varepsilon_n\) of the truth. The proved log-evidence bound is
   \[
   0\le \log Z-\log Z_{\mathcal T}\le-\log(1-\varepsilon_n),
   \]
   which can exceed \(\varepsilon_n\): at \(\pi(\mathcal T)=\pi(S_0)=0.6\), the error is approximately \(0.511>0.4\). [READER_DELTA.md:23](/home/fb31/BVS-wt/W3-D5P/Theory_work/Wave3/W3-D5P/READER_DELTA.md:23) displays unnormalised evidence and then calls “these errors” \(O_P(r_n)\); [CARD.md:10](/home/fb31/BVS-wt/W3-D5P/Theory_work/Wave3/W3-D5P/CARD.md:10) has the same ambiguity after its unnormalised evidence sandwich. LIST-R proves the **log-evidence error** rate. The sandwich also bounds the **relative evidence deficit** by \(\varepsilon_n\), but it does not give an absolute unnormalised error bound of \(\varepsilon_n\).

   **Fix:** Name the error explicitly: either \(|\log Z_{\mathcal T}-\log Z|\), with the logarithmic bound above and rate \(O_P(r_n)\), or \(1-Z_{\mathcal T}/Z\le\varepsilon_n\). Replace Option B’s blanket “within \(\varepsilon_n\)” sentence with the separate PIP, median-model, and evidence conclusions.

3. **[F] The registered conclusion and reader/card proposals drop the evidence availability qualification.** [REPORT.md:66](/home/fb31/BVS-wt/W3-D5P/Theory_work/Wave3/W3-D5P/REPORT.md:66) gives an unconditional inequality for `log_Z_list`; [CARD.md:10](/home/fb31/BVS-wt/W3-D5P/Theory_work/Wave3/W3-D5P/CARD.md:10) and [READER_DELTA.md:23](/home/fb31/BVS-wt/W3-D5P/Theory_work/Wave3/W3-D5P/READER_DELTA.md:23) similarly present evidence without qualification. STATEMENT (C3)(i) expressly restricts the evidence inequality to when `log_Z_list` is not NA, and qualifies exact-list membership by “when returned.” SPEC §4 permits exact-branch evidence to be NA when the store is not returned. These summaries therefore exceed the registered statement’s scope.

   **Fix:** Restore “when `log_Z_list` is not NA” throughout the evidence conclusions and rates, and “when returned” for exact-list membership. State the reader’s evidence quantity only where available.

No C finding remains against L1–L3 or the formal claim spans.

**2. Interpretive-sentence check**

Pointers below refer to [STATEMENT.md](/home/fb31/BVS-wt/W3-D5P/Theory_work/Wave3/W3-D5P/STATEMENT.md).

| Location | Interpretive sentence or clause | Verdict |
|---|---|---|
| C1, line 67 | Real-valued \(F\), “so \(0<Z<\infty\)” | Proved by finiteness of Ω and positivity of its exponential weights; L1 setting and Step 0. |
| C1(b), line 70 | “in particular” the PIP discrepancy bound | Proved by L1(b), taking the coordinate-inclusion events. |
| C1(d), lines 72–73 | “hence” the evidence sandwich and logarithmic error bound | Proved by L1(d), monotonicity of log and \(\log(1+x)\le x\). |
| C2(i), line 83 | “i.e.” completed iff the run is in \(\mathcal O\) | Proved by L2 B1’s return-path and `estimates_available` audit. |
| C2(i), line 86 | “in particular” on \(\mathcal K_n\), \(S_0\in\mathcal M^{run}\) | Proved by L2 B3–B4. |
| C2(v), lines 94–95 | “Consequently” unique global mode implies list membership and `hpm = S₀` | Proved by L2 F using (ii)–(iv). |
| C3 preamble, line 101 | “so that” \(P(\mathcal G_n^+)\to1\) | Proved by the consumed RM2-R-plus conclusions and RM0-plus(b⁺); L3 Step 0. |
| C3(iii), lines 122–124 | Delivery holds, “so” the probability conclusions hold without “on output” | Proved by L3 Step 3 using DLV-0. |
| C3(iii), line 125 | “i.e.” the errors are \(O_P(r_n)\) | Proved by L3 Step 3’s threshold-sequence argument, with evidence restricted to its availability set. |

**3. Sweep duties**

(1) **Statement copies versus lemmas.** Every clause of C1(a)–(e) is established by the corresponding part of L1. C2(i)–(v) maps to L2 B–F, supported by A. C3(i)–(iii) maps to L3 Steps 1–3. I found no missing formal clause.

(2) **Quantifiers and uniformity.** The common event depends only on data. The LS0 argument covers every admissible output run, including cache histories and calibration outcomes; the exact branch is treated separately. The strict \(t\in(0,\tfrac12)\) and median threshold are respected. The formal rate requires eventual \(p\ge2\). The reader’s inherited (S2) already imposes \(2\le p\le n^A\), so its rate needs no additional hypothesis. NA qualifications are correct formally but lost in the derived texts identified above.

(3) **Lemma scope and downstream use.** L3 verifies distinctness, exact scores, nonemptiness, and truth inclusion before invoking L1. Its exact-branch argument correctly uses L1(e) for PIPs and L1(d) for available store evidence. The code audit found no missed successful-run HPM writer, cache insertion without prior membership, completed path bypassing LS0, or eviction of the best entry. The extra HPM offer is confined to numerical failure.

(4) **REPORT and REGISTRY.** Claim IDs, formal statement pointers, proof pointers, and status-source pointers match. The recorded LIST-R status retains IMPL-LIST as open; the consumed statuses agree with the brief. The substantive mismatch is the missing availability qualification in REPORT’s LIST-R registry conclusion, finding 3.

(5) **DEPS and verification.** All six DEPS rows’ SHA prefixes match their files. Manifest verification passed before and after review. The core diff against 4676af6 is empty. I reran the 20,000-case LIST-K check: no violations. I inspected the frozen end-to-end script and output but did not rerun its compiling workflow. I did not execute `citecheck.py`, which writes a review file.

(6) **CARD and READER_DELTA.** Both inherit “those of Theorem 6,” with no additional data hypothesis. Their output definitions and evidence wording nevertheless exceed or differ from LIST-R, as findings 1–3 detail. Their proposal status does not remove the brief’s faithfulness requirement.

**4. Six gates**

- **correct — PASS:** The formal claims, mathematical proofs, and successful-run code links check out.
- **strength — FAIL:** The derived evidence wording asserts more than the formal bounds establish.
- **faithfulness — FAIL:** Exact-branch definitions and evidence availability differ from SPEC and STATEMENT.
- **lit — PASS:** TARGET fairly distinguishes changed outputs, coded-budget guarantees, and unbiasedness versus consistency against the supplied comparison record.
- **necessity — PASS:** No unsupported necessity claim was found.
- **better — PASS:** TARGET §4 dispositions cover the credible stronger candidates within scope.

COUNCIL-VERDICT round=R1 manifest=952d9840170cc7b4f740493c451f91952a1f1077e3ed8574328cf4f1bd21f00a seat=sol score=7.5 gates=FAIL
