# W3-D3 — lead edits queued while the L1 lock reads STATEMENT v1.0 (applied in v1.1 after the lock reply)

Trigger: HQ ruling on the class-1 anchoring (via the manager, 2026-11-17): "class 1, stated precisely, plus a 2b backup
sentence", with the wording below.

Q1 (STATEMENT §5, REPORT, card text; outside the registered spans). HQ class-1 sentence, with one precision in brackets:
"Sub-Gaussian rows on sparse directions with arbitrary correlation. This contains Narisetty & He's (2014, Lemma 6.1)
isotropic sub-Gaussian rows as the special case Σ = I [for centred rows, with K a constant multiple of their
sub-Gaussian constant], and implies Song & Liang's Condition 1." NH14 cited from arXiv 1405.6545v1, pp. 16–17; "journal
version not checked".

Q2 (2b backup sentence). HQ's proposed wording "Light-tailed, correlated features are the ordinary situation (any bounded
or Gaussian-like predictors qualify)" is **not true for (A4) as written** and is not used: a bounded binary predictor with
P(x_j = 1) → 0 violates (A4) for every fixed K (PRECEDENTS B7b, the reason ZH08's bounded covariates were demoted; also
STATEMENT §4(b)). Lead's replacement, provable from ExSG plus Hoeffding's lemma, sent to the manager for HQ:
"Light-tailed, correlated features are the ordinary situation: Gaussian predictors qualify, and so do correlated
mixtures x = m + Lξ of independent features each confined to an interval of K standard deviations on either side of
its mean (for instance Rademacher or uniform features, K = 1)."
Support: new part (b) of Proposition ExSG — if ξ_k (mean 0, variance 1) takes values in an interval of length 2K, then
E exp(λξ_k) ≤ exp(K²λ²/2) (Hoeffding's lemma: E e^{λ(Y−EY)} ≤ exp(λ²(b − a)²/8) for Y ∈ [a, b]), so (A4) holds with K.
Tag: STRONGER on the companion claim ExSG (an added conclusion); goes to the statement-change check.
