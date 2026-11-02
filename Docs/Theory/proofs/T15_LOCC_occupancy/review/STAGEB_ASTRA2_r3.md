# Stage B — Astra #2 round 3 (session <uuid> resumed), confirmation on PROOF_v4, 2026-10-22

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
Round 3 (confirmation). Thank you. Both reviewers verified PROOF_v3 with exposition findings only, and both agree that no fatal or gap finding is outstanding. The author has made wording-only fixes for all of them, including your two findings (rows B2-1 and B2-2 of the updated CLAIMS_OF_FATAL_FLAWS.md) and two from the other reviewer (B2-3, B2-4). The folder now holds STATEMENT.md (v4; see the last bullet of section 5), PROOF_v4.tex and PROOF_v4.pdf, and the updated log. Please check PROOF_v4 against STATEMENT.md v4 (the changes from v3 are in section 6.2 'Construction', the end of the proof of (iv-b), the final 'Scope and use of hypotheses' remark, STATEMENT section 2's hypothesis-use note, and STATEMENT (iv) and (iv-b)). Confirm whether rows B2-1 to B2-4 are resolved and whether any finding of any severity remains, in the REPORT_FORMAT.md format. End with 'Verdict: verified' or 'Verdict: not verified'. Read only files in this folder; run nothing else.
codex
I’ll check the v4 wording against the statement and log, focusing on rows B2-1 through B2-4 and any remaining findings.
exec
"C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" -Command 'Get-Content -LiteralPath REPORT_FORMAT.md, STATEMENT.md, PROOF_v4.tex, CLAIMS_OF_FATAL_FLAWS.md -Encoding UTF8' in <PC_TEMP_PATH>
 succeeded in 3633ms:
# Review task and report format

You are an independent reviewer of a mathematical proof. This folder holds:
- STATEMENT.md: the precise statement (setting, hypotheses, conclusions (i)-(iv), scope remarks, and the changes relative to the source theorem file);
- PROOF_v2.tex and PROOF_v2.pdf: the proof (LaTeX source and compiled PDF; same content).

Read only the files in this folder. Do not fix the proof; report. Any step you cannot verify is a finding.

Check:
1. Is every step correct, and does the proof establish each of (i), (ii), (iii), (iv) exactly as stated in STATEMENT.md?
2. Does the proof use anything beyond the hypotheses in STATEMENT.md section 2 and elementary probability?
3. Is STATEMENT.md coherent and precise (quantifiers, conditioning, what is fixed given the calibration)? Is any claim of the source (as quoted or paraphrased in STATEMENT.md) left unproved?

Report format. Number your findings. Each finding gives:
- location (section / equation / line of the proof or of STATEMENT.md);
- severity: fatal (a conclusion is false or unproved as stated), gap (a step is missing or unjustified but likely fixable), or exposition (wording, notation, clarity);
- the claim;
- the evidence (a derivation, a counterexample, or the exact unsupported step).

End with one line: "Verdict: verified" or "Verdict: not verified".
# STATEMENT — T15 (L-OCC): occupancy from an evidence lower tail

Source: `theorems/T15_LOCC_occupancy.md` (SMC-BVS v3.0, METHODOLOGY_v3.md SHA-256 93043758058a6d422cca6ca4b6be8f3a9e8149b6f6de2e1bab1ce31c44b8019c), read with `theorems/00_COMMON.md`. Parts to prove: all.

## 1. Setting (compact; the method file is authoritative)

- **Target.** Ω = {S ⊆ [p] : |S| ≤ K} is a finite set of models. Each S ∈ Ω has a strictly positive unnormalised posterior weight γ₁(S) = ϖ(S)m(S) (prior × marginal likelihood). Z := Σ_{S∈Ω} γ₁(S) ∈ (0, ∞) is the evidence and π := γ₁/Z the posterior on Ω. For A ⊆ Ω, π(A) = Σ_{S∈A} π(S).
- **Calibration.** 𝓒 is the frozen output of the calibration phase (temperature grid 0 = φ₀ < φ₁ < … < φ_T = 1, budgets, N = N_e, and all other settings). It is measurable with respect to calibration random streams 0–9 and the data. "Successful 𝓒" means the calibration ended with a constructed grid and the final run is launched. P_𝓒 and E_𝓒 denote probability and expectation over the final-run randomness (streams 10–13) given 𝓒 and the data.
- **Final run, island r ∈ {1, 2, 3, 4}.** N particles drawn i.i.d. from the start law π₀; for t = 1, …, T: reweight by G_t(S) = exp{(φ_t − φ_{t−1})d(S)}, multinomial resampling, one move round at temperature φ_t; then L burn-in rounds and 4 measured rounds at φ = 1 (no reweighting in these terminal rounds). A move round is a list of elementary steps applied, for each particle, in a uniformly random order drawn independently of the particle's state.
- **Island evidence.** Ẑ_r := m(∅)Z̄₀ ∏_{t=1}^{T} (1/N) Σ_{i=1}^{N} G_t(S_i^{(t−1)}), the product over all stages (the terminal rounds contribute no factor). Here m(∅) > 0 is the marginal likelihood of the empty model, π₀ = γ₀/Z̄₀ is the composite start law with normaliser Z̄₀ = Σ_Ω γ₀ > 0 (γ₀ > 0), and d(S) is the real-valued discrepancy (all defined in `theorems/00_COMMON.md` §§1–2). Since every factor is a finite positive number (each G_t(S) = e^{(φ_t−φ_{t−1})d(S)} ∈ (0, ∞)), Ẑ_r is a finite, strictly positive random variable under EX-A. The proof uses only W_r ≥ 0. Write **W_r := Ẑ_r / Z**. Pooled evidence: Ẑ := ¼ Σ_r Ẑ_r, and W̄ := Ẑ/Z = ¼ Σ_r W_r.
- **Recording positions.** 𝒯 denotes the set of positions τ in island r's terminal part at which T12(i) is stated: (a) τ = "end of stage T" (after the stage-T resampling and move round); (b) any fixed elementary prefix within the L + 4 terminal rounds; (c) "immediately before a specified Gibbs label" in a terminal round, under the state-independent random order. q̂_{r,τ} is the empirical measure (1/N)Σ_i δ_{S_i(τ)} of island r's particle states at position τ.
- **Outside set and outside fraction.** 𝔄 ⊆ Ω is a set that is fixed given 𝓒 (𝓒- and data-measurable, independent of streams 10–13). f_r := q̂_{r,τ}(1_{𝔄ᶜ}) ∈ [0, 1], the fraction of island r's particles outside 𝔄 at a fixed τ ∈ 𝒯.

## 2. Hypotheses

- **EX-A** (exact arithmetic), **EX-S** (independent ideal uniform streams, with the method's stream separation), **CAL** (𝓒 uses streams 0–9 only; streams 10–13 are fresh; escalation is decided before any final randomness). These are standing assumptions of the setting.
- **(H-T12) Frozen-run identity** (the conclusion of the sibling conjecture T12(i), used here only as an explicit hypothesis): conditional on a successful 𝓒, for island r, each τ ∈ 𝒯, and every bounded function f on Ω that is fixed given 𝓒,

  E_𝓒[ Ẑ_r · q̂_{r,τ}(f) ] = Z · π(f).

  (At these positions the target is q_T = q₁ = π and Z_T = Z.) Parts (i)–(ii) use only the instance f = 1_{𝔄ᶜ}, and only the inequality E_𝓒[W_r f_r] ≤ π(𝔄ᶜ). The first claim of (iii), P_𝓒(W_r < c) ≤ B/(1 − c), uses only its own L¹ hypothesis; its "consequently" clause rests on (i)–(ii) and hence on the same instance of (H-T12). Part (iv) is a statement about abstract laws and uses no hypothesis; it shows that even the identity of (H-T12) for every test function does not yield the pooled form.

## 3. Conclusions

Fix a successful 𝓒, an island r, a position τ ∈ 𝒯, and a set 𝔄 fixed given 𝓒. Let f_r = q̂_{r,τ}(1_{𝔄ᶜ}) and W_r = Ẑ_r/Z.

**(i) Mean bound.** For every c ∈ (0, 1):
  E_𝓒 f_r ≤ min{ 1, π(𝔄ᶜ)/c + P_𝓒(W_r < c) }.

**(ii) Tail bound.** For every c, u ∈ (0, 1):
  P_𝓒(f_r > u) ≤ π(𝔄ᶜ)/(cu) + P_𝓒(W_r < c).

**(iii) Lower tail from an L¹ bound.** If E_𝓒|W_r − 1| ≤ B for a constant B ≥ 0, then for every c ∈ (0, 1), P_𝓒(W_r < c) ≤ B/(1 − c). Consequently (i) and (ii) hold with P_𝓒(W_r < c) replaced by B/(1 − c).

**(iv) The lower tail must be islandwise.** The bounds (i)–(ii) with the pooled lower tail P_𝓒(W̄ < c) in place of the islandwise P_𝓒(W_r < c) do not follow from the structure used, even with the identity of (H-T12) for every test function. (This is a non-implication about direct substitution; it does not assert that every conceivable occupancy bound must use islandwise evidence.) Precisely, fix c, u ∈ (0, 1) and a ∈ (0, cu/4].

(iv-a) There are four i.i.d. random pairs (W_r, f_r), r = 1, …, 4, with W_r > 0 (strictly), f_r ∈ {0, 1}, E W_r = 1 and E[W_r f_r] = a, such that, with W̄ = ¼ Σ_r W_r,
  E f_1 > a/c + P(W̄ < c)  and  P(f_1 > u) > a/(cu) + P(W̄ < c);
in particular, since min{1, x} ≤ x, also E f_1 > min{1, a/c + P(W̄ < c)}.

(iv-b) Moreover, let Ω′ be any finite set, π′ any probability on Ω′, 𝔄′ ⊆ Ω′ with π′(𝔄′ᶜ) = a, and N ≥ 1. (For example, the method's Ω and π whenever some 𝔄 ⊆ Ω has π(𝔄ᶜ) = a; such an 𝔄 exists for a := the smallest posterior mass of a single model whenever |Ω| ≥ 4/(cu), since that mass lies in (0, 1/|Ω|] ⊆ (0, cu/4].) Then the pairs of (iv-a) can be realised jointly with random populations (S_{r,1}, …, S_{r,N}) ∈ Ω′^N, r = 1, …, 4, such that the four pairs (W_r, (S_{r,i})_{i≤N}) are i.i.d., f_r = q̂_r(1_{𝔄′ᶜ}) for the empirical measure q̂_r = (1/N) Σ_i δ_{S_{r,i}}, and

  E[ W_r · q̂_r(g) ] = π′(g)  for every function g : Ω′ → ℝ,

which is the identity of (H-T12) with Ẑ_r := Z′ W_r for any constant Z′ > 0, for every test function g and not only for g ∈ {1, 1_{𝔄′ᶜ}}. Each island has one population; using it at every recording position (q̂_{r,τ} := q̂_r for all τ ∈ 𝒯) gives the identity at every position as well. The four islands of this example are i.i.d.; that property only strengthens the example and is not asserted here as a property of the method.

## 4. Scope remarks (from the theorem file; interpretations, not separate claims)

- (i)–(iii) are statements about the law of the final run given 𝓒 (calibration-conditional). They give no bound on the outside fraction of an already realised population; for a realised population its actual f_r must be used.
- Part (iv) formalises the theorem file's sentence "a pooled-evidence lower tail does not substitute" as a non-implication from the properties listed (W_r > 0, f_r a fraction in [0,1], i.i.d. islands, and the full identity (H-T12)). It does not claim that the SMC final run, for a particular data set and calibration, realises the counterexample law.

## 5. Changes relative to the theorem file

- None to the inequalities, their constants or their quantifiers.
- The theorem file's dependency on T12 ("Builds on: T12"; "prefixes as specified in T12") is stated as the explicit hypothesis (H-T12), as the run rules require for sibling conjectures. The positions 𝒯 are exactly those named in T12(i).
- The sentence on pooled lower tails is made precise as part (iv) (a non-implication), and the sentence on realised populations is kept as a scope remark (§4).
- Assumption EXP (and its replacement EXP′) is not used.
- v2 (after Astra round 1, exposition finding 1): in (iv) the example pairs are required to have W_r > 0 strictly (v1 allowed W_r ≥ 0), matching the strict positivity of actual island evidence, and a sentence fixes the scope of the heading. The inequalities of (i)–(iii) are unchanged.
- v3 (after Stage B, Opus exposition findings 1–5; no fatal or gap findings in any review): (iv) now holds for every a ∈ (0, cu/4] (v2: a = cu/4 only) and adds (iv-b), realising the example with particle populations that satisfy the full identity (H-T12) for every test function; the min{1,·} form is refuted explicitly; the sentence presenting island i.i.d. as a method property is removed; Ẑ_r's symbols and positivity are spelled out; the hypothesis-use note in §2 is made exact. (i)–(iii) unchanged.
- v4 (after Stage B round 2; both reviewers verified v3 with exposition findings only): wording only — the hypothesis-use note for (iii) separates its two claims; "full identity" replaced by "identity for every test function", with the single-population/every-position remark; the method's-Ω example states when a set of mass a exists. No mathematical content changed.
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
\title{T15 (L-OCC): occupancy from an evidence lower tail\\[2pt]\large Proof, version 4}
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

Fix $c,u\in(0,1)$ and $a\in(0,cu/4]$. Note $a<1/4$.

\subsection{Proof of (iv-a)}
Set
\[
  \varepsilon:=\frac12\min\Big\{c,\ \frac{4(1-c)}3,\ \frac{4a}3\Big\}>0,\qquad
  h:=4-3\varepsilon,\qquad
  b:=\frac{a-3\varepsilon/4}{h}.
\]
\emph{Elementary bounds on the constants.} Since $\varepsilon\le 2a/3\le cu/6<1/6$, we have $h\in(7/2,4)$. Since
$3\varepsilon/4\le a/2<a$, we have $b>0$; and $b<a/h<a/3<1/12$. Moreover $\varepsilon\le c/2<c$, and
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

\emph{The two right-hand sides.} Since $a\le cu/4$, $a/c\le u/4<1/4$ and $a/(cu)\le1/4$. Hence
\[
  \frac ac+\mathbb P(\bar W<c)<\frac{64}{256}+\frac{81}{256}=\frac{145}{256},\qquad
  \frac a{cu}+\mathbb P(\bar W<c)\le\frac{64}{256}+\frac{81}{256}=\frac{145}{256}.
\]
Since $145/256<192/256$, both
\[
  \mathbb E f_1> a/c+\mathbb P(\bar W<c)\qquad\text{and}\qquad \mathbb P(f_1>u)>a/(cu)+\mathbb P(\bar W<c)
\]
hold. As $\min\{1,x\}\le x$ for every real $x$, also $\mathbb E f_1>\min\{1,\ a/c+\mathbb P(\bar W<c)\}$. The pairs are
independent and identically distributed and satisfy $W_r>0$, $f_r\in\{0,1\}$, $\mathbb E W_r=1$ and
$\mathbb E[W_rf_r]=a$, which proves (iv-a). \qed

\subsection{Proof of (iv-b)}
Let $\Omega'$ be a finite set, $\pi'$ a probability on $\Omega'$, $\A'\subseteq\Omega'$ with $\pi'(\A'^c)=a$, and
$N\ge1$. Since $a\in(0,1)$, both $\pi'(\A'^c)=a>0$ and $\pi'(\A')=1-a>0$, so the conditional laws
\[
  \pi'_{\rm out}:=\pi'(\,\cdot\mid\A'^c),\qquad \pi'_{\rm in}:=\pi'(\,\cdot\mid\A')
\]
are well defined; $\pi'_{\rm out}$ is carried by $\A'^c$ and $\pi'_{\rm in}$ by $\A'$.

\emph{Construction.} Take the i.i.d.\ pairs $(W_r,f_r)$ of (iv-a). Independently across $r$, and given $(W_r,f_r)$,
draw $S_{r,1},\dots,S_{r,N}$ i.i.d.\ from $\pi'_{\rm out}$ if $f_r=1$ and from $\pi'_{\rm in}$ if $f_r=0$. (Formally:
let $(U_{r,i})$ and $(V_{r,i})$, $r\le4$, $i\le N$, be independent families of i.i.d.\ variables with laws
$\pi'_{\rm out}$ and $\pi'_{\rm in}$, independent of the pairs, and set $S_{r,i}:=U_{r,i}$ if $f_r=1$ and
$S_{r,i}:=V_{r,i}$ if $f_r=0$.) The four quadruples $\big(W_r,f_r,(U_{r,i})_i,(V_{r,i})_i\big)$ are i.i.d.: the
pairs $(W_r,f_r)$ are i.i.d., the families $(U_{r,i})$ and $(V_{r,i})$ are independent of each other and of the
pairs, and their laws do not depend on $r$. Since $(W_r,(S_{r,i})_i)$ is the same measurable function of each
quadruple, the four pairs $(W_r,(S_{r,i})_{i\le N})$ are i.i.d.

\emph{The outside fraction.} If $f_r=1$, every $S_{r,i}\in\A'^c$, so $\hat q_r(1_{\A'^c})=1$; if $f_r=0$, every
$S_{r,i}\in\A'$, so $\hat q_r(1_{\A'^c})=0$. Hence $f_r=\hat q_r(1_{\A'^c})$.

\emph{The identity.} Fix $g:\Omega'\to\mathbb R$ (bounded, as $\Omega'$ is finite). Since $(U_{r,i})$ and $(V_{r,i})$ are
independent of $(W_r,f_r)$,
\[
  \mathbb E\big[W_r\,\hat q_r(g)\,\big|\,W_r,f_r\big]
  =W_r\Big(f_r\,\pi'_{\rm out}(g)+(1-f_r)\,\pi'_{\rm in}(g)\Big),
\]
with $\pi'_{\rm out}(g)=\pi'(g1_{\A'^c})/a$ and $\pi'_{\rm in}(g)=\pi'(g1_{\A'})/(1-a)$. All variables involved are
bounded, so taking expectations and using $\mathbb E[W_rf_r]=a$ and $\mathbb E[W_r(1-f_r)]=\mathbb EW_r-\mathbb E[W_rf_r]=1-a$,
\[
  \mathbb E\big[W_r\,\hat q_r(g)\big]=a\cdot\frac{\pi'(g1_{\A'^c})}{a}+(1-a)\cdot\frac{\pi'(g1_{\A'})}{1-a}
  =\pi'(g1_{\A'^c})+\pi'(g1_{\A'})=\pi'(g).
\]
Multiplying by any constant $Z'>0$ gives $\mathbb E[(Z'W_r)\,\hat q_r(g)]=Z'\pi'(g)$, the identity of (H-T12) with
$\hat Z_r:=Z'W_r$, for every test function $g$. Each island has a single population; using it at every recording
position ($\hat q_{r,\tau}:=\hat q_r$ for all $\tau\in\mathcal T$) gives the identity at every position. This proves
(iv-b). \qed

\begin{remark}[Consistency with (i)--(iii)]
In the example of (iv-a), the islandwise bounds hold, as they must. Since $\varepsilon<c<h$,
$\mathbb P(W_1<c)=\mathbb P(W_1=\varepsilon)=3/4$, so $a/c+\mathbb P(W_1<c)\ge3/4+b=\mathbb E f_1$ because
$b<a/3<a/c$; and $a/(cu)+\mathbb P(W_1<c)\ge 3/4+b=\mathbb P(f_1>u)$ because $b<a/3<a/(cu)$. The pooled version fails
because of the event that island~1 has small evidence $W_1=\varepsilon$ and $f_1=1$ while another island has large
evidence $h$, which keeps $\bar W$ above $c$. Part (iv) is a non-implication about substituting the pooled lower
tail into (i)--(ii); it does not claim that the SMC final run, for a particular data set and calibration, realises
this law.
\end{remark}

\begin{remark}[Scope and use of hypotheses]
Parts (i)--(iii) bound the law of $f_r$ under $\Pc$; they give no bound on the outside fraction of a realised
population. Parts (i) and (ii) use only $W_r\ge0$, $0\le f_r\le1$ and the instance $f=1_{\A^c}$ of (H-T12) (in
fact only $\Ec[W_rf_r]\le\pi(\A^c)$). The first claim of part (iii), $\Pc(W_r<c)\le B/(1-c)$, uses only its own hypothesis
$\Ec|W_r-1|\le B$ (which also makes $W_r$ integrable) and Markov's inequality, and not (H-T12); its
``consequently'' clause substitutes this bound into (i) and (ii), and so rests on the same instance of (H-T12) as
they do. Part (iv) concerns explicitly constructed laws
and uses no property of the final run. Assumption EXP (or EXP$'$) is not used anywhere.
\end{remark}

\end{document}
# CLAIMS_OF_FATAL_FLAWS — T15 (L-OCC)

## Fatal or gap findings

None. Six reviews so far, and none raised a fatal or gap finding:
- Astra #1, round 1, on PROOF_v1: verified; 1 exposition finding.
- Astra #1, round 2, on PROOF_v2: verified; no new findings.
- Stage B Astra #2, round 1, on PROOF_v2: verified; no findings.
- Stage B Opus 5.5 xhigh, round 1, on PROOF_v2: verified; 5 exposition findings.
- Stage B Astra #2, round 2, on PROOF_v3 + this log: verified; 2 exposition findings. Agrees that no fatal or gap finding is outstanding. Rulings: A1-1, O-1, O-2, O-3, O-5 resolved; O-4 partially resolved.
- Stage B Opus, round 2, on PROOF_v3 + this log: verified; 4 exposition findings. Agrees that no fatal or gap finding is outstanding. Rulings: O-1 to O-5 resolved.

## Exposition findings and the lead's answers (kept for the record)

| # | Reviewer | Finding (short) | Answer | Change |
|---|---|---|---|---|
| A1-1 | Astra #1 r1 | The (iv) example has W = 0 with probability 3/4, but actual island evidence is strictly positive. Heading scope needs care. | Accepted. | v2: example uses ε > 0; scope sentence added to (iv). |
| O-1 | Opus B r1 | (H-T12) gives the identity for every test function g, but the example checks only g ∈ {1, 1_{𝔄ᶜ}}. Opus suggested a populations-based extension. | Accepted; adopted as a strengthening. | v3: new (iv-b) realises the example with particle populations satisfying E[W q̂(g)] = π′(g) for all g, on any finite Ω′ (including the method's Ω, π) with π′(𝔄′ᶜ) = a. (iv) now holds for every a ∈ (0, cu/4]. |
| O-2 | Opus B r1 | Island i.i.d. given 𝓒 is presented as a method property, but it is not among the hypotheses. | Accepted. | v3: the claim about the method is removed; the example's i.i.d. property is described as only strengthening it. |
| O-3 | Opus B r1 | Z̄₀, d, m(∅), π₀ are undefined, and the positivity of Ẑ_r is asserted, not derived. | Accepted. | v3: the symbols are defined briefly with a pointer to 00_COMMON; positivity is derived from positive factors. The proof uses only W_r ≥ 0. |
| O-4 | Opus B r1 | The Scope remark misdescribes the hypothesis use of (iii) and (iv). | Accepted. | v3: the remark is rewritten part by part. |
| O-5 | Opus B r1 | (iv) refutes the pooled form of (i) without the min{1,·} and does not state that the min form is refuted too. | Accepted. | v3: the one-line step min{1,x} ≤ x is added to (iv-a) and its proof. |
| B2-1 | Astra #2 r2 = Opus r2 #1 | The i.i.d. justification in (iv-b) cites (W_r, U, V) and leaves out f_r. | Accepted (both reviewers raised it independently). | v4: the argument now uses the quadruples (W_r, f_r, U_r, V_r). |
| B2-2 | Astra #2 r2 = Opus r2 #2 | "Part (iii) does not use (H-T12)" holds only for its first claim; the "consequently" clause rests on (i)–(ii). | Accepted. | v4: the note in STATEMENT §2 and the proof's final remark separate the two claims. |
| B2-3 | Opus r2 #3 | (iv-b) gives the identity at one position, while "full identity" suggests all of 𝒯. | Accepted. | v4: "full identity" is replaced by "identity for every test function", plus a remark that reusing the population at every τ gives every position. |
| B2-4 | Opus r2 #4 | "The method's Ω and π" example needs some set of posterior mass exactly a. | Accepted. | v4: the example states when such a set exists (smallest atom, if #Ω ≥ 4/(cu)). |

Unified version after Stage B round 1: v3. After Stage B round 2 (wording only): STATEMENT.md (v4 bullet in §5) and proof/PROOF_v4.tex/.pdf. (i)–(iii) are unchanged in statement and proof since v1.

codex
No findings of severity **fatal**, **gap**, or **exposition** remain in PROOF_v4.tex against STATEMENT.md v4.

All four tracked items are resolved:

| Log row | Location | Ruling and evidence |
|---|---|---|
| **B2-1** | Proof §6.2, “Construction” | **Resolved.** The input blocks now include \(f_r\): \((W_r,f_r,U_r,V_r)\). These blocks are i.i.d., and each constructed island is the same measurable function of its block. The independence argument is correct. |
| **B2-2** | Statement §2; proof’s final scope remark | **Resolved.** Both passages distinguish the lower-tail estimate, which uses only the \(L^1\) assumption and Markov’s inequality, from the occupancy consequences, which inherit the weighted-moment assumption through (i)–(ii). |
| **B2-3** | Statement (iv), (iv-b); end of proof §6.2 | **Resolved.** The text specifies the identity for every test function and explicitly sets \(\widehat q_{r,\tau}=\widehat q_r\) at every recording position. Therefore the same identity holds at every position. This remains an abstract construction, consistently with the stated scope. |
| **B2-4** | Statement (iv-b), parenthetical example | **Resolved.** Application to the method’s target is expressly conditional on an outside set of mass \(a\). The sufficient example is correct: if \(M=|\Omega|\ge4/(cu)\), strict positivity gives \(0<\min_S\pi(S)\le1/M\le cu/4\). Taking the outside set to be a singleton attaining that minimum supplies an admissible \(a\). |

The remaining proof establishes the conclusions exactly as stated. Parts **(i)–(iii)** follow from the weighted-moment inequality, splitting, and Markov’s inequality. For every permitted \(c,u,a\), **(iv-a)** supplies strictly positive evidence with the required moments and simultaneous strict violations of both pooled bounds, including the minimum form.

In **(iv-b)**, the conditional sampling construction preserves the outside fraction and gives, for every test function \(g\),
\[
\mathbb E[W_r\widehat q_r(g)]
=a\,\pi'_{\mathrm{out}}(g)+(1-a)\,\pi'_{\mathrm{in}}(g)
=\pi'(g).
\]
Scaling by \(Z'>0\) and reusing the population at every position establish the asserted identity throughout.

The conditioning, quantifiers, and abstract-counterexample scope are coherent. No additional substantive hypothesis or non-elementary probability result is used. I agree with the updated log that no fatal or gap finding is outstanding; the previously outstanding exposition findings are now resolved as well.

Verdict: verified
tokens used
47,536
No findings of severity **fatal**, **gap**, or **exposition** remain in PROOF_v4.tex against STATEMENT.md v4.

All four tracked items are resolved:

| Log row | Location | Ruling and evidence |
|---|---|---|
| **B2-1** | Proof §6.2, “Construction” | **Resolved.** The input blocks now include \(f_r\): \((W_r,f_r,U_r,V_r)\). These blocks are i.i.d., and each constructed island is the same measurable function of its block. The independence argument is correct. |
| **B2-2** | Statement §2; proof’s final scope remark | **Resolved.** Both passages distinguish the lower-tail estimate, which uses only the \(L^1\) assumption and Markov’s inequality, from the occupancy consequences, which inherit the weighted-moment assumption through (i)–(ii). |
| **B2-3** | Statement (iv), (iv-b); end of proof §6.2 | **Resolved.** The text specifies the identity for every test function and explicitly sets \(\widehat q_{r,\tau}=\widehat q_r\) at every recording position. Therefore the same identity holds at every position. This remains an abstract construction, consistently with the stated scope. |
| **B2-4** | Statement (iv-b), parenthetical example | **Resolved.** Application to the method’s target is expressly conditional on an outside set of mass \(a\). The sufficient example is correct: if \(M=|\Omega|\ge4/(cu)\), strict positivity gives \(0<\min_S\pi(S)\le1/M\le cu/4\). Taking the outside set to be a singleton attaining that minimum supplies an admissible \(a\). |

The remaining proof establishes the conclusions exactly as stated. Parts **(i)–(iii)** follow from the weighted-moment inequality, splitting, and Markov’s inequality. For every permitted \(c,u,a\), **(iv-a)** supplies strictly positive evidence with the required moments and simultaneous strict violations of both pooled bounds, including the minimum form.

In **(iv-b)**, the conditional sampling construction preserves the outside fraction and gives, for every test function \(g\),
\[
\mathbb E[W_r\widehat q_r(g)]
=a\,\pi'_{\mathrm{out}}(g)+(1-a)\,\pi'_{\mathrm{in}}(g)
=\pi'(g).
\]
Scaling by \(Z'>0\) and reusing the population at every position establish the asserted identity throughout.

The conditioning, quantifiers, and abstract-counterexample scope are coherent. No additional substantive hypothesis or non-elementary probability result is used. I agree with the updated log that no fatal or gap finding is outstanding; the previously outstanding exposition findings are now resolved as well.

Verdict: verified
```
