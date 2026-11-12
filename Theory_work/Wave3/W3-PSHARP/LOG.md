# W3-PSHARP — LOG

Agents started so far (model, provider, role): lead Claude Fable 5.2 (claudeAgent, high).
Claude-inference tally: all on Claude Work (claudeAgent); claude-personal not used.

- 2026-11-11 ~19:25 CST (start of run; first clock reading was 19:48). Branch `theory/W3-PSHARP` created from main @ 16a7f85. Read BRIEF; PROGRAM; PROTOCOL (rules
  9–16); LIFECYCLE §4–4.3; templates ASSUMPTION_MAP, COUNCIL_BRIEF; W3-POST STATEMENT v1.4, REPORT, lemmas L1a′, LB;
  W3-POST2 STATEMENT v1.2.1, lemmas A_occam, B_tail_approx, REPORT §§4–8; sharp1 TRIAGE; f15, f16, f17; registry rows
  (claims W3-POST:*, W3-POST2:*; A:COEF-REP; sharpness rows 190–221). HOLDS.md (main checkout): no holds.
- 19:48. orchestrator_capabilities checked (codex: gpt-6.1-sol, gpt-6-astra; claudeAgent: claude-opus-5-5).
  Numerics interpreter: `py -3.13 -I` (numpy 2.3.0, scipy 1.15.3, mpmath 1.3.0).
- Findings while reading / deriving:
  1. Tail, truncated mean and second moment of e^{χ²₁/2} re-derived (PLAN). The truncated mean at level p is exactly
     2√(log p/π).
  2. (a) extends beyond the brief at no cost: the lower bound needs only a null block that is either orthogonal
     (fixed design) or spherical and independent of ε (random design). The second covers **p ≫ n** (iid Gaussian
     columns, (log p)² = o(n)), so the √log question closes for every p = n^a, a > 0, not only a ≤ 1.
  3. Brief wording "rate r_n needs bounded s₀": on **every** design the corollary gives s₀ = O(√log n); bounded s₀ is
     forced on the witness designs of (a) (log p ≍ log n). Stated that way (STATEMENT B2).
  4. (c): f16's design works with a clean proof; it also gives a quantitative record (reference cost ≫ (log n)²
     breaks the conclusion).
  5. Rule 11: W3-POST2:A2 etc. are below PROVED-CHECKED, so (b) is proved directly from the definition of π
     (5 lines) instead of consuming A2; no claim is consumed in any proof.
- 19:51. STATEMENT.md v1.0, PLAN.md v1.0 written (Claim C constants fixed while re-deriving: k = ⌈12 log n⌉,
  n₀ = 200, C_b = 1200).
