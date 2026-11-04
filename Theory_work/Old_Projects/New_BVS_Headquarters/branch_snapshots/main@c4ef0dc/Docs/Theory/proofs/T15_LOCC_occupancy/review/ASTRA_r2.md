# Astra review, round 2 (session <uuid> resumed), 2026-10-22

Packet: STATEMENT.md (v2), PROOF_v2.tex (PROOF_v1.tex and REPORT_FORMAT.md still present). Full codex log follows verbatim.

```
OpenAI Codex v0.163.0
--------
workdir: <PC_TEMP_PATH>
model: gpt-6-astra
provider: openai
approval: never
sandbox: read-only
reasoning effort: high
reasoning summaries: none
session id: <uuid>
--------
user
Round 2. Thank you for the review. In response to your exposition finding 1, the folder now holds a revised STATEMENT.md (part (iv) now requires W_r > 0 strictly, and one sentence fixes the scope of the heading; see also the last bullet of section 5) and a revised proof PROOF_v2.tex (only section 6, the proof of (iv), and its consistency remark changed: the example now uses a strictly positive small value epsilon instead of 0). Please re-read both files and review PROOF_v2.tex against the revised STATEMENT.md, in the same report format as REPORT_FORMAT.md, ending with 'Verdict: verified' or 'Verdict: not verified'. Read only files in this folder; run nothing else.
codex
I’ll re-read the report format and both revised files, then check the positive-evidence example and the proof against the revised statement.
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command 'Get-Content -LiteralPath REPORT_FORMAT.md, STATEMENT.md, PROOF_v2.tex -Encoding UTF8' in <PC_TEMP_PATH>
 succeeded in 265ms:
# Review task and report format

You are the independent reviewer of a proof. The folder holds:
- STATEMENT.md: the precise statement (definitions, hypotheses, conclusions (i)-(iv), scope remarks, and the changes relative to the source theorem file);
- PROOF_v1.tex: the proof (LaTeX source).

Read only these files. Do not fix the proof; report. Any step you cannot verify is a finding.

Check:
1. Is every step of the proof correct, and does it prove each of (i), (ii), (iii), (iv) exactly as stated in STATEMENT.md?
2. Does the proof use anything beyond the hypotheses listed in STATEMENT.md §2 (and elementary probability)?
3. Is STATEMENT.md internally coherent and precise (quantifiers, measurability, what is fixed given the calibration)? Is formalising the informal sentence "a pooled-evidence lower tail does not substitute" as the non-implication (iv) a fair reading, and is anything in the source claims (as quoted in STATEMENT.md) left unproved?

Report format. Number your findings. Each finding gives:
- location (section/equation/line of the proof or of STATEMENT.md);
- severity: fatal (a conclusion is false or unproved as stated), gap (a step is missing or not justified but likely fixable), or exposition (wording, notation, clarity);
- the claim;
- the evidence (a derivation, a counterexample, or the exact unsupported step).

End with one line: "Verdict: verified" or "Verdict: not verified".
# STATEMENT — T15 (L-OCC): occupancy from an evidence lower tail

Source: `theorems/T15_LOCC_occupancy.md` (SMC-BVS v3.0, METHODOLOGY_v3.md SHA-256 93043758058a6d422cca6ca4b6be8f3a9e8149b6f6de2e1bab1ce31c44b8019c), read with `theorems/00_COMMON.md`. Parts to prove: all.

## 1. Setting (compact; the method file is authoritative)

- **Target.** Ω = {S ⊆ [p] : |S| ≤ K} is a finite set of models. Each S ∈ Ω has a strictly positive unnormalised posterior weight γ₁(S) = ϖ(S)m(S) (prior × marginal likelihood). Z := Σ_{S∈Ω} γ₁(S) ∈ (0, ∞) is the evidence and π := γ₁/Z the posterior on Ω. For A ⊆ Ω, π(A) = Σ_{S∈A} π(S).
- **Calibration.** 𝓒 is the frozen output of the calibration phase (temperature grid 0 = φ₀ < φ₁ < … < φ_T = 1, budgets, N = N_e, and all other settings). It is measurable with respect to calibration random streams 0–9 and the data. "Successful 𝓒" means the calibration ended with a constructed grid and the final run is launched. P_𝓒 and E_𝓒 denote probability and expectation over the final-run randomness (streams 10–13) given 𝓒 and the data.
- **Final run, island r ∈ {1, 2, 3, 4}.** N particles drawn i.i.d. from the start law π₀; for t = 1, …, T: reweight by G_t(S) = exp{(φ_t − φ_{t−1})d(S)}, multinomial resampling, one move round at temperature φ_t; then L burn-in rounds and 4 measured rounds at φ = 1 (no reweighting in these terminal rounds). A move round is a list of elementary steps applied, for each particle, in a uniformly random order drawn independently of the particle's state.
- **Island evidence.** Ẑ_r := m(∅)Z̄₀ ∏_{t=1}^{T} (1/N) Σ_{i=1}^{N} G_t(S_i^{(t−1)}), the product over all stages (the terminal rounds contribute no factor). Under EX-A, Ẑ_r is a finite, strictly positive random variable. Write **W_r := Ẑ_r / Z**. Pooled evidence: Ẑ := ¼ Σ_r Ẑ_r, and W̄ := Ẑ/Z = ¼ Σ_r W_r.
- **Recording positions.** 𝒯 denotes the set of positions τ in island r's terminal part at which T12(i) is stated: (a) τ = "end of stage T" (after the stage-T resampling and move round); (b) any fixed elementary prefix within the L + 4 terminal rounds; (c) "immediately before a specified Gibbs label" in a terminal round, under the state-independent random order. q̂_{r,τ} is the empirical measure (1/N)Σ_i δ_{S_i(τ)} of island r's particle states at position τ.
- **Outside set and outside fraction.** 𝔄 ⊆ Ω is a set that is fixed given 𝓒 (𝓒- and data-measurable, independent of streams 10–13). f_r := q̂_{r,τ}(1_{𝔄ᶜ}) ∈ [0, 1], the fraction of island r's particles outside 𝔄 at a fixed τ ∈ 𝒯.

## 2. Hypotheses

- **EX-A** (exact arithmetic), **EX-S** (independent ideal uniform streams, with the method's stream separation), **CAL** (𝓒 uses streams 0–9 only; streams 10–13 are fresh; escalation is decided before any final randomness). These are standing assumptions of the setting.
- **(H-T12) Frozen-run identity** (the conclusion of the sibling conjecture T12(i), used here only as an explicit hypothesis): conditional on a successful 𝓒, for island r, each τ ∈ 𝒯, and every bounded function f on Ω that is fixed given 𝓒,

  E_𝓒[ Ẑ_r · q̂_{r,τ}(f) ] = Z · π(f).

  (At these positions the target is q_T = q₁ = π and Z_T = Z.) Only the instance f = 1_{𝔄ᶜ}, giving E_𝓒[W_r f_r] = π(𝔄ᶜ), and, in part (iv), the instance f ≡ 1, giving E_𝓒 W_r = 1, are used. For parts (i)–(iii), only the inequality E_𝓒[W_r f_r] ≤ π(𝔄ᶜ) is needed.

## 3. Conclusions

Fix a successful 𝓒, an island r, a position τ ∈ 𝒯, and a set 𝔄 fixed given 𝓒. Let f_r = q̂_{r,τ}(1_{𝔄ᶜ}) and W_r = Ẑ_r/Z.

**(i) Mean bound.** For every c ∈ (0, 1):
  E_𝓒 f_r ≤ min{ 1, π(𝔄ᶜ)/c + P_𝓒(W_r < c) }.

**(ii) Tail bound.** For every c, u ∈ (0, 1):
  P_𝓒(f_r > u) ≤ π(𝔄ᶜ)/(cu) + P_𝓒(W_r < c).

**(iii) Lower tail from an L¹ bound.** If E_𝓒|W_r − 1| ≤ B for a constant B ≥ 0, then for every c ∈ (0, 1), P_𝓒(W_r < c) ≤ B/(1 − c). Consequently (i) and (ii) hold with P_𝓒(W_r < c) replaced by B/(1 − c).

**(iv) The lower tail must be islandwise.** The bounds (i)–(ii) with the pooled lower tail P_𝓒(W̄ < c) in place of the islandwise P_𝓒(W_r < c) do not follow from the structure used. (This is a non-implication about direct substitution; it does not assert that every conceivable occupancy bound must use islandwise evidence.) Precisely: for every c, u ∈ (0, 1) there are a number a ∈ (0, 1) and four i.i.d. random pairs (W_r, f_r), r = 1, …, 4, with W_r > 0 (strictly, as for actual island evidence), f_r ∈ {0, 1} (so f_r ∈ {0, 1/N, …, 1} for every N), E W_r = 1 and E[W_r f_r] = a (the properties that (H-T12) gives with a = π(𝔄ᶜ), together with conditional independence and identical distribution of the islands given 𝓒), such that, with W̄ = ¼ Σ_r W_r,
  E f_1 > a/c + P(W̄ < c)  and  P(f_1 > u) > a/(cu) + P(W̄ < c).

## 4. Scope remarks (from the theorem file; interpretations, not separate claims)

- (i)–(iii) are statements about the law of the final run given 𝓒 (calibration-conditional). They give no bound on the outside fraction of an already realised population; for a realised population its actual f_r must be used.
- Part (iv) formalises the theorem file's sentence "a pooled-evidence lower tail does not substitute" as a non-implication from the properties listed. It does not claim that a particular data set and calibration realise the counterexample law.

## 5. Changes relative to the theorem file

- None to the inequalities, their constants or their quantifiers.
- The theorem file's dependency on T12 ("Builds on: T12"; "prefixes as specified in T12") is stated as the explicit hypothesis (H-T12), as the run rules require for sibling conjectures. The positions 𝒯 are exactly those named in T12(i).
- The sentence on pooled lower tails is made precise as part (iv) (a non-implication), and the sentence on realised populations is kept as a scope remark (§4).
- Assumption EXP (and its replacement EXP′) is not used.
- v2 (after Astra round 1, exposition finding 1): in (iv) the example pairs are required to have W_r > 0 strictly (v1 allowed W_r ≥ 0), matching the strict positivity of actual island evidence, and a sentence fixes the scope of the heading. The inequalities of (i)–(iii) are unchanged.
\documentclass[11pt]{article}
\usepackage[margin=1in]{geometry}
\usepackage{amsmath,amssymb,amsthm}
\usepackage{enumitem}
\newtheorem{theorem}{Theorem}
\newtheorem{lemma}{Lemma}
\theoremstyle{remark}
\newtheorem{remark}{Remark}
\newcommand{\Pc}{\mathbb{P}_{\mathcal C}}
\newcommand{\Ec}{\mathbb{E}_{\mathcal C}}
\newcommand{\A}{\mathfrak{A}}
\title{T15 (L-OCC): occupancy from an evidence lower tail\\[2pt]\large Proof, version 2}
\author{SMC-BVS v3 theory programme}
\date{2026-10-22}
\begin{document}
\maketitle

\section{Setting and hypotheses}

We use the notation of STATEMENT.md. $\Omega$ is the finite model space, $\pi=\gamma_1/Z$ the posterior with
evidence $Z\in(0,\infty)$, and $\mathcal C$ a successful frozen calibration; $\Pc$ and $\Ec$ are the probability and
expectation over the final-run randomness given $\mathcal C$ and the data. For an island $r$, $\hat Z_r$ is its
evidence estimate, which under EX-A is a finite, strictly positive random variable, and
\[
  W_r:=\hat Z_r/Z \in (0,\infty).
\]
Fix a recording position $\tau\in\mathcal T$ and a set $\A\subseteq\Omega$ fixed given $\mathcal C$, and let
\[
  f_r:=\hat q_{r,\tau}(1_{\A^c})=\frac1N\sum_{i=1}^N 1\{S_i(\tau)\notin\A\}\in[0,1].
\]
Since $\A$ is fixed given $\mathcal C$, the function $f=1_{\A^c}$ is bounded and fixed given $\mathcal C$, so
hypothesis (H-T12) applies to it and gives
\begin{equation}\label{eq:id}
  \Ec[W_r f_r]=\frac{\Ec[\hat Z_r\,\hat q_{r,\tau}(1_{\A^c})]}{Z}=\frac{Z\,\pi(1_{\A^c})}{Z}=\pi(\A^c).
\end{equation}
For parts (i)--(iii) only the inequality $\Ec[W_rf_r]\le\pi(\A^c)$ is used. The random variable $W_rf_r$ is
nonnegative, and by \eqref{eq:id} it is integrable.

Throughout, $r$, $\tau$ and $\A$ are fixed, and we drop the subscript $r$: $W=W_r$, $f=f_r$.

\section{Two elementary facts}

\begin{lemma}[Splitting at $c$]\label{lem:split}
Let $W\ge0$ and $f\in[0,1]$ be random variables on a common probability space, with $\mathbb E[Wf]\le a<\infty$.
Then for every $c>0$,
\[
  \mathbb E\big[f\,1\{W\ge c\}\big]\le a/c .
\]
\end{lemma}
\begin{proof}
On the event $\{W\ge c\}$ we have $W/c\ge1$ and $f\ge0$, hence $f\le fW/c$. Off this event,
$f\,1\{W\ge c\}=0\le fW/c$ because $f,W\ge0$. So pointwise
$f\,1\{W\ge c\}\le fW/c$, and taking expectations gives $\mathbb E[f1\{W\ge c\}]\le \mathbb E[fW]/c\le a/c$.
\end{proof}

\begin{lemma}[Markov]\label{lem:markov}
If $V\ge0$ is a random variable and $s>0$, then $\mathbb P(V\ge s)\le \mathbb E V/s$.
\end{lemma}
\begin{proof}
$s\,1\{V\ge s\}\le V$ pointwise; take expectations.
\end{proof}

\section{Proof of (i): the mean bound}

Fix $c\in(0,1)$. Since $0\le f\le1$, we have $\Ec f\le1$. Write $f=f\,1\{W\ge c\}+f\,1\{W<c\}$. By
Lemma~\ref{lem:split} with $a=\pi(\A^c)$ (justified by \eqref{eq:id}), $\Ec[f1\{W\ge c\}]\le\pi(\A^c)/c$. Since
$f\le1$, $\Ec[f1\{W<c\}]\le\Pc(W<c)$. Adding,
\[
  \Ec f\le \pi(\A^c)/c+\Pc(W<c).
\]
Together with $\Ec f\le1$ this is $\Ec f\le\min\{1,\ \pi(\A^c)/c+\Pc(W<c)\}$. \qed

\section{Proof of (ii): the tail bound}

Fix $c,u\in(0,1)$. Decompose
\[
  \{f>u\}\subseteq\big(\{f>u\}\cap\{W\ge c\}\big)\cup\{W<c\}.
\]
On $\{f>u\}\cap\{W\ge c\}$ we have $fW\ge fc>uc$, using $W\ge c>0$ and $f>u>0$. Hence
$\{f>u\}\cap\{W\ge c\}\subseteq\{fW\ge cu\}$. By Lemma~\ref{lem:markov} applied to $V=fW\ge0$ and $s=cu>0$, and by
\eqref{eq:id},
\[
  \Pc(fW\ge cu)\le \Ec[fW]/(cu)\le\pi(\A^c)/(cu).
\]
By the union bound,
\[
  \Pc(f>u)\le\pi(\A^c)/(cu)+\Pc(W<c). \qquad\qed
\]

\section{Proof of (iii): the lower tail from an $L^1$ bound}

Assume $\Ec|W-1|\le B$, and fix $c\in(0,1)$. On $\{W<c\}$, $|W-1|\ge 1-W>1-c>0$. Hence
$\{W<c\}\subseteq\{|W-1|\ge 1-c\}$, and Lemma~\ref{lem:markov} with $V=|W-1|$ and $s=1-c>0$ gives
\[
  \Pc(W<c)\le\Pc(|W-1|\ge1-c)\le\frac{\Ec|W-1|}{1-c}\le\frac{B}{1-c}.
\]
Substituting this bound into (i) and (ii) gives, for every $c,u\in(0,1)$,
\[
  \Ec f\le\min\Big\{1,\ \frac{\pi(\A^c)}{c}+\frac{B}{1-c}\Big\},\qquad
  \Pc(f>u)\le\frac{\pi(\A^c)}{cu}+\frac{B}{1-c}. \qquad\qed
\]

\section{Proof of (iv): the lower tail must be islandwise}

Fix $c,u\in(0,1)$ and set
\[
  a:=\frac{cu}4\in\Big(0,\frac14\Big),\qquad
  \varepsilon:=\frac12\min\Big\{c,\ \frac{4(1-c)}3,\ \frac{cu}3\Big\}>0,\qquad
  h:=4-3\varepsilon,\qquad
  b:=\frac{a-3\varepsilon/4}{h}.
\]
\emph{Elementary bounds on the constants.} Since $\varepsilon\le cu/6<1/6$, we have $h\in(7/2,4)$. Since
$\varepsilon<cu/3$, we have $3\varepsilon/4<cu/4=a$, so $b>0$; and $b<a/h<a/3<1/12$. Moreover $\varepsilon<c$, and
$\varepsilon\le 2(1-c)/3$ gives $3\varepsilon/4\le(1-c)/2$, hence
\begin{equation}\label{eq:h4}
  h/4=1-3\varepsilon/4\ \ge\ (1+c)/2\ >\ c .
\end{equation}

\emph{The law.} Let $(W_r,f_r)$, $r=1,\dots,4$, be i.i.d.\ copies of a pair $(W,f)$ with the three-point law
\[
  \mathbb P\big((W,f)=(\varepsilon,1)\big)=\tfrac34,\qquad
  \mathbb P\big((W,f)=(h,1)\big)=b,\qquad
  \mathbb P\big((W,f)=(h,0)\big)=\tfrac14-b .
\]
The probabilities are positive (as $0<b<1/12$) and sum to $1$. Clearly $W\in\{\varepsilon,h\}\subset(0,\infty)$, so
$W>0$ strictly, and $f\in\{0,1\}$. Also $\mathbb P(W=h)=1/4$ and $\mathbb P(f=1)=3/4+b$.

\emph{The required moment properties.}
$\mathbb E W=\tfrac34\varepsilon+\tfrac14h=\tfrac34\varepsilon+1-\tfrac34\varepsilon=1$, and
$\mathbb E[Wf]=\tfrac34\varepsilon+hb=\tfrac34\varepsilon+a-\tfrac34\varepsilon=a$.

\emph{The pooled lower tail.} Let $K:=\#\{r:W_r=h\}\sim\mathrm{Bin}(4,1/4)$. Then
$\bar W=\tfrac14\big(Kh+(4-K)\varepsilon\big)$. If $K=0$, then $\bar W=\varepsilon<c$. If $K\ge1$, then
$\bar W\ge h/4>c$ by \eqref{eq:h4}. Hence $\{\bar W<c\}=\{K=0\}$ and $\mathbb P(\bar W<c)=(3/4)^4=81/256$.

\emph{The two left-hand sides.} $\mathbb E f_1=\mathbb P(f_1=1)=\tfrac34+b>\tfrac34$. Since $f_1\in\{0,1\}$ and
$u<1$, $\{f_1>u\}=\{f_1=1\}$, so $\mathbb P(f_1>u)=\tfrac34+b>\tfrac34=\tfrac{192}{256}$.

\emph{The two right-hand sides.} $a/c=u/4<1/4$ and $a/(cu)=1/4$. Hence
\[
  \frac ac+\mathbb P(\bar W<c)<\frac{64}{256}+\frac{81}{256}=\frac{145}{256},\qquad
  \frac a{cu}+\mathbb P(\bar W<c)=\frac{64}{256}+\frac{81}{256}=\frac{145}{256}.
\]
Since $145/256<192/256$, both
\[
  \mathbb E f_1> a/c+\mathbb P(\bar W<c)\qquad\text{and}\qquad \mathbb P(f_1>u)>a/(cu)+\mathbb P(\bar W<c)
\]
hold. The pairs are independent and identically distributed and satisfy $W_r>0$, $f_r\in\{0,1\}$,
$\mathbb E W_r=1$ and $\mathbb E[W_rf_r]=a\in(0,1)$, which proves (iv). \qed

\begin{remark}[Consistency with (i)--(iii)]
In the example of (iv), the islandwise bounds hold, as they must. Since $\varepsilon<c<h$,
$\mathbb P(W_1<c)=\mathbb P(W_1=\varepsilon)=3/4$, so $a/c+\mathbb P(W_1<c)=u/4+3/4\ge3/4+b=\mathbb E f_1$ because
$b<a/3=cu/12<u/4$; and $a/(cu)+\mathbb P(W_1<c)=1\ge\mathbb P(f_1>u)$. The pooled version fails because of the
event that island~1 has small evidence $W_1=\varepsilon$ and $f_1=1$ while another island has large evidence $h$,
which keeps $\bar W$ above $c$. Part (iv) is a non-implication about substituting the pooled lower tail into
(i)--(ii); it does not claim that a particular data set and calibration realise this law.
\end{remark}

\begin{remark}[Scope]
Parts (i)--(iii) bound the law of $f_r$ under $\Pc$. They give no bound on the outside fraction of a realised
population. No property of the final run beyond (H-T12) and $0\le f_r\le1$, $W_r\ge 0$ is used; in particular,
assumption EXP (or EXP$'$) is not used.
\end{remark}

\end{document}

codex
No new fatal, gap, or exposition findings. All four conclusions are proved as revised.

1. **Location:** STATEMENT.md §3(iv), §4, and the last bullet of §5; PROOF_v2.tex §6 and its consistency remark.  
   **Severity:** exposition — round-1 finding resolved.  
   **Claim:** The revised example satisfies strict positivity, and the heading’s scope is now explicit.  
   **Evidence:** For every \(c,u\in(0,1)\), the prescribed constants satisfy
   \[
   0<\varepsilon\le cu/6<1/6,\qquad \varepsilon<c,\qquad
   7/2<h<4,\qquad h/4\ge(1+c)/2>c.
   \]
   Also \(3\varepsilon/4<a=cu/4\), so
   \[
   0<b=\frac{a-3\varepsilon/4}{h}<\frac a3<\frac1{12}.
   \]
   Thus all three probabilities are positive and sum to one, and both possible evidence values are strictly positive. The added sentence expressly restricts the non-implication to direct substitution of the pooled lower tail. This resolves the earlier scope concern.

The remaining verification is as follows.

In §§1–3, (H-T12) applies to the indicator of the calibration-fixed outside set and gives \(E_{\mathcal C}[W_rf_r]=\pi(\mathfrak A^c)\). Splitting according to \(W_r\ge c\), using \(f_r1_{\{W_r\ge c\}}\le W_rf_r/c\), and bounding the other contribution by \(P_{\mathcal C}(W_r<c)\) proves (i), including its minimum with \(1\).

In §4, the inclusion
\[
\{f_r>u,\ W_r\ge c\}\subseteq\{W_rf_r\ge cu\}
\]
and Markov’s inequality prove (ii) with the stated constants. In §5, the inclusion
\[
\{W_r<c\}\subseteq\{|W_r-1|\ge1-c\}
\]
proves (iii); both substitutions are valid. No boundary or integrability issue arises.

For the revised construction in §6,
\[
EW_r=\frac34\varepsilon+\frac14h=1,\qquad
E[W_rf_r]=\frac34\varepsilon+hb=a.
\]
The four pairs are i.i.d. If all four evidence values equal \(\varepsilon\), their average is below \(c\); if any equals \(h\), their average exceeds \(c\). Hence
\[
P(\bar W<c)=\left(\frac34\right)^4=\frac{81}{256}.
\]
Both left-hand sides in (iv) equal \(3/4+b>192/256\). The proposed pooled mean-bound right-hand side is below \(145/256\), and the tail-bound right-hand side equals \(145/256\). Both strict failures therefore hold for every prescribed \(c,u\). The revised consistency remark is correct.

No assumptions beyond the supplied setting, explicit hypotheses, and elementary probability are used. In particular, no independence between evidence and occupancy within an island is assumed, and neither EXP nor EXP′ is needed.

The statement’s conditioning, measurability, and quantifiers are coherent. The outside set and recording rule are fixed given calibration and data; (H-T12) explicitly covers the specified recording positions. Part (iv) remains an abstract non-implication, with algorithmic realisability expressly excluded. This is a fair reading of the quoted pooled-evidence warning. No quoted source claim within that stated scope remains unproved; T12 itself is appropriately an explicit hypothesis.

Verdict: verified
tokens used
27,630
No new fatal, gap, or exposition findings. All four conclusions are proved as revised.

1. **Location:** STATEMENT.md §3(iv), §4, and the last bullet of §5; PROOF_v2.tex §6 and its consistency remark.  
   **Severity:** exposition — round-1 finding resolved.  
   **Claim:** The revised example satisfies strict positivity, and the heading’s scope is now explicit.  
   **Evidence:** For every \(c,u\in(0,1)\), the prescribed constants satisfy
   \[
   0<\varepsilon\le cu/6<1/6,\qquad \varepsilon<c,\qquad
   7/2<h<4,\qquad h/4\ge(1+c)/2>c.
   \]
   Also \(3\varepsilon/4<a=cu/4\), so
   \[
   0<b=\frac{a-3\varepsilon/4}{h}<\frac a3<\frac1{12}.
   \]
   Thus all three probabilities are positive and sum to one, and both possible evidence values are strictly positive. The added sentence expressly restricts the non-implication to direct substitution of the pooled lower tail. This resolves the earlier scope concern.

The remaining verification is as follows.

In §§1–3, (H-T12) applies to the indicator of the calibration-fixed outside set and gives \(E_{\mathcal C}[W_rf_r]=\pi(\mathfrak A^c)\). Splitting according to \(W_r\ge c\), using \(f_r1_{\{W_r\ge c\}}\le W_rf_r/c\), and bounding the other contribution by \(P_{\mathcal C}(W_r<c)\) proves (i), including its minimum with \(1\).

In §4, the inclusion
\[
\{f_r>u,\ W_r\ge c\}\subseteq\{W_rf_r\ge cu\}
\]
and Markov’s inequality prove (ii) with the stated constants. In §5, the inclusion
\[
\{W_r<c\}\subseteq\{|W_r-1|\ge1-c\}
\]
proves (iii); both substitutions are valid. No boundary or integrability issue arises.

For the revised construction in §6,
\[
EW_r=\frac34\varepsilon+\frac14h=1,\qquad
E[W_rf_r]=\frac34\varepsilon+hb=a.
\]
The four pairs are i.i.d. If all four evidence values equal \(\varepsilon\), their average is below \(c\); if any equals \(h\), their average exceeds \(c\). Hence
\[
P(\bar W<c)=\left(\frac34\right)^4=\frac{81}{256}.
\]
Both left-hand sides in (iv) equal \(3/4+b>192/256\). The proposed pooled mean-bound right-hand side is below \(145/256\), and the tail-bound right-hand side equals \(145/256\). Both strict failures therefore hold for every prescribed \(c,u\). The revised consistency remark is correct.

No assumptions beyond the supplied setting, explicit hypotheses, and elementary probability are used. In particular, no independence between evidence and occupancy within an island is assumed, and neither EXP nor EXP′ is needed.

The statement’s conditioning, measurability, and quantifiers are coherent. The outside set and recording rule are fixed given calibration and data; (H-T12) explicitly covers the specified recording positions. Part (iv) remains an abstract non-implication, with algorithmic realisability expressly excluded. This is a fair reading of the quoted pooled-evidence warning. No quoted source claim within that stated scope remains unproved; T12 itself is appropriately an explicit hypothesis.

Verdict: verified
```
