# FINAL erratum, §6 Delivery (IDEAL-W⁺ batch): before/after text, sentences checked, span check

Prepared 2026-11-16 06:25 CST by the Theory Dept implementation sub-agent (Claude Opus 5.5), at HQ's request: an in-place
erratum to the FINAL chapter before the freeze. The base is origin/main `8431b575`. FINAL and the shipped code are identical
on origin/main and on `dept/theory`.

- **Patch:** `patches/ERRATUM__FINAL__s6_delivery.tex.patch` (sha256 `5a72bc33…4692`). It applies with `patch -p1` to the
  origin/main files, giving exactly the after-files below.
- **Files touched:** `Theory_work/Wave1C/FINAL/sections/s6_delivery.tex` (sha256 `d2bd6624…1e5e` → `e1a4f623…c3ca`) and
  `Theory_work/Wave1C/FINAL/sections/s8_scope.tex` (sha256 `d2d84ed3…8932` → `f16643fd…19d`).
- **Sources:** A:IDEAL-W⁺ comes from `Theory_work/Dept/research/FUNI_NARROW/A_IDEALW_PLUS.md:10`, copied verbatim and only
  converted to LaTeX. 𝔇 and the (a)/(b) wording come from the batch, `patches/HQ_AUDIT-W1C__A2_propF_GROW.md.patch`. The
  reason is Sol TR1 §1–§2 (`Theory_work/Dept/research/FUNI_transfer/TR1_sol.md`). The code lines are on origin/main and at
  `493579a`: `Scripts/SMC_BVS/core/v3_run.R:96` (`le > 1e6`) and `Scripts/SMC_BVS/core/cpp/v3_core.cpp:474`
  (`cap_ll > numeric_limits<int>::max()` → `stop("LS0 move cap out of range")`).

## 1. What changes

Five sentences change in place and one erratum paragraph is appended. The patch adds no line before an existing line:
s6 goes from 63 to 67 lines, all new lines after the old last line `:63`, and s8 keeps its 19 lines.

| # | location | change |
|---|---|---|
| 1 | `s6:4` (summary at the head of §6) | P(no output)=0 is now (a) on the bounded domain 𝔇 under IDEAL-W and (b) for every admissible n under A:IDEAL-W⁺ |
| 2 | `s6:46` (Prop F, corrected form: cap a_n, allocation for `493579a`) | Every-n delivery is split into (a)/(b) in the batch's wording, and 𝔇 is defined. The consistency sentence P(Ŝ=S₀)→1 is put under (b). |
| 3 | `s6:54` (Prop F-GROW) | Delivery is split into (a)/(b), and the asymptotic P(Ŝ=S₀)→1 is put under (b) |
| 4 | `s6:56` (F-GROW proof outline, steps (2) and (3)) | The step "Theorem D's walk leaves only null exits" is restricted to 𝔇 under IDEAL-W, or every n under A:IDEAL-W⁺; TR1 marks exactly this inference as failing. The use of P(𝒪)=1 is marked "every n; clause (b)". |
| 5 | `s8:9` (scope item "Delivery for the shipped calibration") | "under IDEAL-W" becomes "with IDEAL-W on the bounded domain 𝔇 and with A:IDEAL-W⁺ for every n" |
| 6 | `s6:64-67` (new, after `\end{remark}`) | A dated erratum paragraph that lists the changed sentences and contains the required sentence "IDEAL-W never covered the application-level rejection predicates; IDEAL-W⁺ is the explicit form". It cites the two code lines with checkable `\srcq` (citecheck OK), shows why neither predicate fires on 𝔇, says that 𝔇 is sufficient, not necessary, and bounded, and keeps the C-DLV form unchanged. It ends with the A:IDEAL-W⁺ definition verbatim. |

**Left unchanged on purpose.** The following concern the *specified* method, which has neither validator. They are
spec-level and not exposed, and the erratum says so in one clause:

- the C-DLV-form Proposition F (cap ℓ_n; statusbox `s6:49`, and the last sentence of `s6:46`, "With the original LS0 cap
  a_n=ℓ_n, the original Lemma R envelopes suffice", which is a resource statement);
- Theorem D (`s6:11-13`);
- Corollary D′ (`s6:18-20`);
- the Setting/Allocation paragraphs (`s6:6`, `s6:8`).

## 2. Before / after (exact LaTeX fragments; the rest of each line is unchanged)

### `s6_delivery.tex:4`
Before:
```latex
$\PP(\text{no output})=0$ (Proposition~\ref{prop:F}, extended to the GROW class by Proposition~\ref{prop:FG}).
```
After:
```latex
$\PP(\text{no output})=0$ (a) on the bounded domain $\mathfrak D$ under IDEAL-W and (b) for every admissible $n$ under A:IDEAL-W$^{+}$ (Proposition~\ref{prop:F}, extended to the GROW class by Proposition~\ref{prop:FG}; erratum 2026-11-16 at the end of this section).
```

### `s6_delivery.tex:46` (Proposition F, corrected form)
Before:
```latex
Then for every admissible $n\ge3$, $\PP(\text{no output})=0$. On LH exact Gram,
```
After:
```latex
Then (a) under IDEAL-W, $\PP(\text{no output})=0$ for every admissible $n\ge3$ with $(n,p_{\rm raw})\in\mathfrak D$ $:=\{\ell_{\rm raw}\le10^6$ and $\ell_{\rm raw}+\lfloor n/2\rfloor\le2^{31}-1\}$, $\ell_{\rm raw}:=\lceil\log_2(n+p_{\rm raw}+1)\rceil$; and (b) with A:IDEAL-W$^{+}$ in place of IDEAL-W (IDEAL-W, and the two shipped rejection predicates $\texttt{le}>10^6$ (\texttt{Scripts/SMC\_BVS/core/v3\_run.R:96}) and $\ell+|\tilde S_0|>\texttt{INT\_MAX}$ (\texttt{Scripts/SMC\_BVS/core/cpp/v3\_core.cpp:474}) are false; definition in the erratum at the end of this section), for every admissible $n\ge3$, $\PP(\text{no output})=0$. Under (b), on LH exact Gram,
```
(The rest of the line is unchanged: "…$\PP(\Shat=S_0)\to1$ under the original unconditioned data law. CAL, … unnecessary. With the
original LS0 cap $a_n=\ell_n$, the original Lemma R envelopes suffice.")

### `s6_delivery.tex:54` (Proposition F-GROW)
Before:
```latex
Then, for every admissible $n\ge3$, $\PP(\text{no output})=0$, and along each such sequence
```
After:
```latex
Then (a) under IDEAL-W, $\PP(\text{no output})=0$ for every admissible $n\ge3$ with $(n,p_{\rm raw})\in\mathfrak D$ ($\mathfrak D$ as in Proposition~\ref{prop:F}); and (b) with A:IDEAL-W$^{+}$ in place of IDEAL-W, for every admissible $n\ge3$, $\PP(\text{no output})=0$, and along each such sequence
```

### `s6_delivery.tex:56` (F-GROW proof outline), two fragments
Before:
```latex
so Theorem D's walk leaves only null exits.
```
After:
```latex
so Theorem D's walk leaves only null exits, on $\mathfrak D$ under IDEAL-W and for every $n$ under A:IDEAL-W$^{+}$ (the two LS0 cap validators lie outside that walk; erratum below).
```
Before:
```latex
D′'s pathwise claim and $\PP(\Ocal)=1$ give
```
After:
```latex
D′'s pathwise claim and $\PP(\Ocal)=1$ (every $n$; clause (b)) give
```

### `s8_scope.tex:9`
Before:
```latex
Delivery is proved only for the fallback calibration of Proposition~\ref{prop:F}, under IDEAL-W, MACH, CONFIG and the amended allocation,
```
After:
```latex
Delivery is proved only for the fallback calibration of Proposition~\ref{prop:F}, under MACH, CONFIG and the amended allocation, with IDEAL-W on the bounded domain $\mathfrak D$ and with A:IDEAL-W$^{+}$ for every $n$ (erratum 2026-11-16, end of §\ref{sec:delivery}),
```

### `s6_delivery.tex:64-67` (new; blank line, erratum paragraph, blank line, definition)
```latex
\paragraph{Erratum (2026-11-16; HQ D78).} The every-$n$ delivery sentences of this section (the summary at its head, Proposition~\ref{prop:F} in its corrected form, Proposition~\ref{prop:FG} and step~(2) of its proof outline) and the delivery item of §\ref{sec:scope} previously asserted $\PP(\text{no output})=0$ for every admissible $n$ under IDEAL-W; they now read (a)/(b) as above. IDEAL-W never covered the application-level rejection predicates; IDEAL-W$^{+}$ is the explicit form. The shipped LS0 base-cap validator $\texttt{le}>10^6$ \srcq{PROD/v3_run.R:96}{le > 1e6} and the LS0 cap-range guard $\ell_n+|\tilde S_0|>\texttt{INT\_MAX}$ \srcq{PROD/cpp/v3_core.cpp:474}{LS0 move cap out of range} (the same lines at \texttt{493579a}) lie outside Theorem~\ref{thm:D}'s exit walk and can end an SMC-branch fit without output independently of resources (Sol review TR1, Theory Dept, \texttt{Theory\_work/Dept/research/FUNI\_transfer/TR1\_sol.md}, branch \texttt{dept/theory}). On $\mathfrak D$ neither fires: $\ell_n\le\ell_{\rm raw}\le10^6$ ($p\le p_{\rm raw}$) and $\ell_n+|\tilde S_0|\le\ell_{\rm raw}+K\le\ell_{\rm raw}+\lfloor n/2\rfloor\le2^{31}-1$; the exact-enumeration branch reaches neither check. $\mathfrak D$ is sufficient, not necessary, and bounded, so clause (a) carries no asymptotic conclusion; every asymptotic delivery or consistency conclusion above is under (b). Theorem~\ref{thm:D}, Corollary~\ref{cor:Dprime} and the C-DLV form of Proposition~F (cap $\ell_n$) concern the specified method, which has neither validator; they are unchanged. Definition (verbatim; registered assumption A:IDEAL-W$^{+}$):

\textbf{A:IDEAL-W$^{+}$ (IDEAL-W with the two LS0 cap ceilings lifted).} IDEAL-W, exactly as defined in C-DLV \texttt{STATEMENT.md:24-25}, and the two shipped rejection predicates $\texttt{le}>10^6$ (\texttt{Scripts/SMC\_BVS/core/v3\_run.R:96}, the LS0 base-cap validator; $\texttt{le}=\ell_n=\lceil\log_2(n+p+1)\rceil$ in the shipped configuration) and $\ell+|\tilde S_0|>\texttt{INT\_MAX}$ (\texttt{Scripts/SMC\_BVS/core/cpp/v3\_core.cpp:474}, the disjunct \texttt{cap\_ll > numeric\_limits<int>::max()} of the LS0 cap-range guard, \texttt{int} read as unbounded) are false. Nothing else is lifted: the other conditions of those two validators (numeric type, length, finiteness, integrality, \texttt{le < 0}, \texttt{o.ls0\_ell < 0}), every other validator, the $10^6$-maximiser start-mode enumeration cap with its tie-aware DP fallback, and every fallback and method cap are kept as coded. Like IDEAL-W and EX-A, A:IDEAL-W$^{+}$ is an idealisation of the machine and code; a larger allocation does not imply it.
```

## 3. Sentences checked for every-n delivery claims about shipped code (all of `Theory_work/Wave1C/FINAL/`)

Method: a grep of `consistency.tex` and `sections/*.tex` for "no output", "every admissible", "delivery", `\PP(\Ocal)`, U_n,
`prop:F` and `prop:FG`, then a reading of each hit in context.

| location | content | verdict |
|---|---|---|
| `consistency.tex:4-5` (title), agentnote `:15-22` | title "…delivery results…"; status of Prop F / F-GROW | No every-n claim. There is no abstract or intro; the agentnote quotes statuses only. Unchanged. |
| `s1_setting.tex:32` | "The delivery results (§6) add the idealisation premises IDEAL-W, MACH, CONFIG…" | A premise list, not an every-n claim. It stays true, because (a) uses IDEAL-W, and the (b) premise is stated in §6. Unchanged; HQ may add "A:IDEAL-W⁺ beyond 𝔇" as an option. |
| `s1_setting.tex:35` | "Delivery, P(𝒪)→1, is a fourth question (§6)" | Names the question only. Unchanged. |
| `s2_map.tex:24` | "Delivery under a declared polynomial allocation: Prop. F" | A pointer to Prop F, which is now restricted. Unchanged. |
| `s5_hpm.tex:83`, `:95` | "no delivery claim"; table cell "delivery: Prop. FG" | A disclaimer and a pointer. Unchanged. |
| `s6:4` | summary P(no output)=0 | **Changed (#1).** |
| `s6:6`, `s6:8` | Setting/Allocation, premises including IDEAL-W, cap ℓ_n | Spec-level (C-DLV form). Unchanged. |
| `s6:11-13` Thm D, `s6:14`, `s6:16` (O), `s6:18-20` Cor D′, statusbox `s6:21-23` | reduction U_n ⊆ SL_n ∪ N_n for the specified method, cap ℓ_n | The specified method has no validators, so these are not exposed. Unchanged. |
| `s6:26` | "schedule_limit is the only no-output path not excluded…" (C-DLV finding, specified method) | Spec-level, attributed to C-DLV. Unchanged. |
| `s6:29-44` (Prop F premises and allocation) | | Unchanged. (b) replaces IDEAL-W by A:IDEAL-W⁺ at `:46`. |
| `s6:46` | Prop F corrected form, every-n delivery and consistency | **Changed (#2).** |
| `s6:49` statusbox | statuses only (C-DLV form PROVED-CHECKED; corrected form A1/A4) | No claim text. Unchanged, and no `\st{}` edited (registry check C8). |
| `s6:54` | Prop F-GROW every-n delivery and consistency | **Changed (#3).** |
| `s6:56` | proof outline, steps (2) and (3) | **Changed (#4).** |
| `s6:58` statusbox | statuses only | Unchanged. |
| `s6:61-63` Remark | (3) "exclusion of every other no-output path is relative to the P1 exit inventory…; LS0 … paths are covered by premises"; (5) "a new preflight exit outside C-DLV's P1 inventory…" | Not every-n claims. (3) stays true, because the cap validators are now covered by the premises 𝔇 / A:IDEAL-W⁺. Unchanged. |
| `s7_impl.tex:10`, `:25` | MR1 description; "all results … for caps … (and ≤ ℓ_n+K for the delivery envelopes)" | About the cap range and envelopes; no every-n delivery claim. Unchanged. |
| `s7_impl.tex:36-56` (Lemma CAP setting, (L2), statement) | (L2) at `:39` says the cap-range exit "is excluded by IDEAL-W" | Already handled by the batch's separate `patches/ERRATUM__W1C-FINAL__sections_s7_impl.tex.patch` (E4, DIFF2 PASS). Not touched here. |
| `s7_impl.tex:72`, `:81` | "D′'s delivery form … hold … only under A1's amended allocation"; "delivery requires the amended allocation" | Necessary conditions, not every-n claims. Unchanged. |
| `s8_scope.tex:6` | "the ideal-machine delivery statement of Proposition F keep their stated finite-n scope" | Refers to the stated scope, which is now (a)/(b). Unchanged. |
| `s8_scope.tex:9` | "Delivery is proved … under IDEAL-W, MACH, CONFIG … on LH, … GROW" | **Changed (#5).** |
| `s8_scope.tex:14` | "delivery also assumes IDEAL-W (…unsupported_size…)" | An assumption statement, still true. Unchanged; HQ may add "and A:IDEAL-W⁺ beyond 𝔇" as an option. |
| `s9_prov.tex:24`, `:26`, `:27` | provenance rows for Prop F, F-GROW and C-ENG | Provenance only. Unchanged. |

## 4. Registry: no span moves

I read all of `Theory_work/INFRA/registry/` on origin/main, every column of `claims.tsv` (`file`, `lines`, `premises`,
`status_source`, `tex`), `assumptions.tsv`, `sharpness.tsv`, `tickets.tsv` and `events.log`, for references into
`Wave1C/FINAL/`. The references to s6 or s8 are:

| row | column | span | effect of this patch |
|---|---|---|---|
| C-DLV:Thm-D | `tex` | `s6_delivery.tex:11-13` | Content and position unchanged (span sha256 is the same before and after). |
| C-DLV:Prop-F | `tex` | `s6_delivery.tex:28-47` | **Position unchanged; content changed at `:46`.** The registry stores no `tex_sha256` for this row, so `check.py` C11-tex gives the same result as before: INFO "never reviewed". No row has a `file`, `lines` or `premises` span in s6 or s8. |
| events.log `:155-156` | — | the same two `tex` pointers | Historical record. Unchanged. |

- No line is inserted or removed before any cited line. s6 grows only after its old last line `:63`, and s8 keeps its line
  count.
- W1C-FINAL:Lemma-CAP (`s7_impl.tex:45-56`, premises `:36-43`, status_source `:64`) is in a file this patch does not touch.
- No other row of `claims.tsv`, and no row of the other registry tables, cites s6 or s8.

**For HQ: C-DLV:Prop-F's `tex` pointer.** The registry row is the C-DLV form (cap ℓ_n, specified method), and its registered
statement `C-DLV/lemmas/L4_delivery.md:79-84` is unchanged. Its `tex` pointer, however, spans FINAL's corrected-form
Proposition F (`s6:28-47`), and that span now carries the (a)/(b) split at `:46`. This is a re-check item for the paper
transcription, not a span move. No hash changes, because the row stores no `tex_sha256`.

## 5. Checks run

- **Patch application.** `patch -p1` on a fresh `git archive origin/main` copy of `FINAL/sections`, in the session scratch
  area. The result is byte-identical to the after-files.
- **citecheck.** `FINAL/citecheck.py` was run on a patched copy with the repo links, under `.rc_tmp/` and deleted afterwards.
  - The two new `\srcq` citations are OK: `PROD/v3_run.R:96` [le > 1e6] and `PROD/cpp/v3_core.cpp:474` [LS0 move cap out of
    range].
  - The 6 TOKEN-MISS lines in s1, s3, s7 and s8 are pre-existing; they are identical on the unpatched base.
- **LaTeX.** The full chapter does not build on this host, which lacks Cambria/Consolas and `xltabular`. A minimal LuaLaTeX
  harness with the chapter's macros builds s6+s8 with 0 errors and 0 missing characters, before and after. The patch adds 6
  overfull-hbox warnings, all from long `\texttt` paths; they are cosmetic.
- **Registry status words.** No `\st{…}` token is added or edited, so registry check C8 is unaffected.
