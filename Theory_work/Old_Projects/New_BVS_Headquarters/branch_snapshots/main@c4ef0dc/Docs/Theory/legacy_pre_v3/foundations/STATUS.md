# STATUS — foundations thread (F4, L4, L6, P6, P7)

Date: 2026-10-14.

- **Protocol:** theorem proving (`protocols/proof.md`), reduced for a non-interactive coordinated run.
- **Proof:** `PROOF.md` (this folder), written by the lead (Fable 5.1). Example 4.7 was revised after the numerical checks: the pair condition $(c-b)(bc-ad)=0$ is stated as necessary only, and "reversible iff $ad=bc$" is proved. PROOF.md is frozen for review round 1.
- **Numerical checks:** `check_foundations.py` → `check_foundations.out` (local, single seed `default_rng(1)`, exact enumeration where specified). 100 checks, 100 PASS, 0 FAIL, including C4.f-rev (sweep reversible iff $ad=bc$, 200/200) and C7.a' (Proposition 5.9 with $(a_0,a_1)=(3/4,1/4)$: $\mathbb E[\widehat Z]/Z=0.804884855\ldots$; reversed rule $1.195115\ldots$).
  - Earlier operator findings: the original pair criterion for Example 4.7 was not a full-reversibility criterion (now fixed in PROOF.md). On the C5 instance, the ESS rule of C6(d) never triggers at stages 1 or 2; supplementary instances that do trigger resampling are exactly unbiased.
- **Review round 1:** launched with 3 Opus (xhigh) and 3 Astra (GPT-6, xhigh) blind reviewers, angles A (line by line), B (structure) and C (adversarial). The packet is in `review/` (PACKET_README.md, PROOF.md verbatim copy, STATEMENTS_FROM_DRAFT.md). Astra runs: `review/run_astra.sh`, outputs in `review/astra_{A,B,C}/ASTRA_REVIEW_{A,B,C}.md` with run logs `astra_run.log`.
- **Findings:** `FINDINGS.md` (empty template in the layout of `proofs/T3_T11/FINDINGS.md`; to be filled by the lead with rulings).
- **Adoption:** not adopted. The core code (`check_foundations.py`) and the proof have not been adopted by the person; all results are provisional.
- **Resume point:** collect the six round-1 reports; record each finding in FINDINGS.md with a ruling; if accepted findings require it, save v1 as `review/PROOF_v1_prereview.md` and revise PROOF.md to v2; rerun `check_foundations.py`; decide on round 2.

## Update 2026-10-14: v2 and review round 2

- **Round 1 outcome:** six "not verified" verdicts (3 Opus, 3 Astra); no fatal error in any proof. The one fatal finding concerned the draft's wording of the resampling condition (unbiased counts "given the weights" instead of given the population); it is now Proposition 5.13 (exact counterexample, E[Pi_2] = 29/16 versus 7/4). Rulings: `FINDINGS.md` (maintained by the lead).
- **v2 written** 2026-10-14 after round 1: `PROOF.md`. v1 is kept at `review/PROOF.md`.
- **Numerical checks after v2:** `check_foundations.py` extended with C10 (Proposition 5.13: 29/16 vs 7/4, weights-only condition holds, counts (2,0) at (s1,s2)), C11 (Proposition 5.8 covariance identity, N in {1,2,3}, 60 random instances; the 41/16 case) and C12 (Theorem 5.7 with a randomised resampling decision). 111 checks, 111 PASS, 0 FAIL.
- **Round 2 launched:** three Opus reviewers resumed by the lead; three Astra sessions resumed by the operator (`review/run_astra_round2.sh`; prompts `review/astra_X/prompt_round2.txt`, logs `review/astra_X/astra_run_round2.log`, reports `review/astra_X/ASTRA_REVIEW_X_round2.md`).
- **Adoption:** not adopted.
- **Resume point:** collect the six round-2 reports, rule on them in FINDINGS.md, revise to v3 if needed, rerun the checks.

## Update 2026-10-14 (~20:30): v3 and review round 3

- **Round 2 outcome:** Opus B and C: "every step verified", with exposition notes. Astra A, B, C: no fatal finding; gap findings confined to prose (remarks, summaries, wording of side claims). Opus A's round-2 run was cut off by an API rate limit and is resumed for round 3.
- **v3 written** 2026-10-14 ~20:30 after round 2 (wording-only changes; all Astra round-2 gap and exposition findings accepted; rulings in `FINDINGS.md`). v2 is preserved at `review/PROOF_v2.md`, v1 at `review/PROOF.md`.
- **Round 3 launched** on the v2 -> v3 diff (`review/diff_v2_v3.txt`) with the same six reviewers: three Opus resumed by the lead, three Astra sessions resumed by the operator (`review/run_astra_round3.sh`; prompts `review/astra_X/prompt_round3.txt`, logs `review/astra_X/astra_run_round3.log`, reports `review/astra_X/ASTRA_REVIEW_X_round3.md`).
- **Adoption:** not adopted.
- **Resume point:** collect the six round-3 reports and rule on them in FINDINGS.md.

## Update 2026-10-14 (~21:30): round 3 outcome, final text

- **Round 3 outcome:** Opus A (rounds 2 and 3 combined), B and C: "every step verified", exposition notes only. Astra A, B, C: no fatal finding; one or two gap-level findings each, all in three explanatory sentences added in v3 (the parenthetical after the adaptive law, the sentence "not under the user's control", and pointers to reviewer scripts). Rulings in FINDINGS.md (round 3): all accepted.
- **Final text:** PROOF.md (header "Version 3, final text"); the round-3 text is preserved at review/PROOF_v3.md, v2 at review/PROOF_v2.md, v1 at review/PROOF.md. The post-round-3 wording changes are listed in FINDINGS.md 3.1-3.7 and were not re-reviewed (the protocol's three-round cap).
- **Verification status:** proofs of F4, L4, L6, P6, P7 verified step by step by the three Opus reviewers and, as to every proof step, by the three Astra reviewers; Astra verdicts remain "not verified" on prose items fixed afterwards. Numerical checks: check_foundations.py, 111 checks, 111 PASS.
- **Flags for the draft:** (1) L6(iii)-(v) need b_pi = p; (2) P6's neighbour-list example needs a symmetric list (k_max >= 1), and the neighbour-swap acceptance must carry the Hastings ratio; (3) Section 2.3 step 2(c) must condition on the population (Proposition 5.13).
- **Adoption:** not adopted.
- **Resume point:** none needed; the thread is complete. A future thread may re-review the post-round-3 wording (diff review/PROOF_v3.md PROOF.md).
