# STATUS — Pb4 (positive crossing result)

Protocol: theorem proving (`proof.md`), reduced for a non-interactive coordinated run (as in T3_T11, T6): statement frozen inside PROOF.md, lead Fable 5.1, one correctness round with three Opus (xhigh) and three Astra (xhigh) reviewers if time allows.

- 2026-10-15 — Inputs read: paper_draft.tex in full; proofs/T3_T11 §0–4, §6 (Lemma 3 exact decomposition, Lemma 4 three regimes, T11(iii)); proofs/T5 §0–2 (particle-system model (0.1), restricted run, Lemma 1 on non-crossing kernels).
- Next: mathematics. Strategy in play: (1) show that along the whole bridge, under T11(iii)+(R), q_phi concentrates on the chain of models between S0 and S̃0 (supersets of S0 inside S̃0), with explicit log-weights; (2) a single-site Gibbs sweep at q_phi has a deletion probability for each proxy that is exactly the conditional q_phi odds, so one sweep moves mass at the bridge's rate; (3) SMC error via a bounded-potential argument on the chain: potentials bounded by e^{c (phi_t-phi_{t-1}) n} ... need care; (4) negative example; (5) classification.

Resume point: nothing written yet beyond this file.
