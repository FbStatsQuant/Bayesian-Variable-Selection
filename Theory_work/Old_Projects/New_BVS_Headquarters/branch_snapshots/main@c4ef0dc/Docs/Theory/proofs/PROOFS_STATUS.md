# v3 proof campaign — prove-first list (status)

Started 2026-10-22 on Felipe's instruction. The threads are managed by the v3 profiling lead (thread mcp:5e4b26e1…), acting for HQ.
Input: Decision Point 2 (`/projects/ml75/fb31/BVS/v3_profiling_20261020/reports/DP2_DECISIONS.md` on NOTS).

**Setup, per Felipe:**
- One thread per theorem, each led by Opus 5.5 (high).
- 6 threads on Claude Personal (CP) and 4 on Claude Work (CW).
- Each thread may use Sonnet/Haiku 5.5 assistants and exactly one Astra (high) session as consultant and reviewer.
- Protocol: proof.md, with these overrides: no Fable, no Sol, no Opus reviewers. A proof is final when the lead and Astra agree.
- Result label: "proved (lead Opus 5.5 + one Astra review); not adopted".

**Amendment 1 (2026-10-22).** Felipe put the lead in charge of the protocol, with three constraints: about 60% CP / 40% CW, at most 1–2 Fables in total for review, and Astra agents allowed. The review now runs in three stages:
- **Stage A, in each thread:** the Opus lead and Astra #1 reach a proof candidate.
- **Stage B, in each thread:** two fresh, independent reviewers (Astra #2 at high, and Opus 5.5 at xhigh on the thread's own account) review the candidate. Every fatal or gap finding is logged in CLAIMS_OF_FATAL_FLAWS.md and goes back to the reviewers for a ruling. A dispute still open after 3 rounds goes to an Astra judge (xhigh, fresh session).
- **Stage C, by the managing lead:** one detailed collected document, reviewed by 1 Fable 5.1 (high) thread on CP plus 1 Astra (xhigh). A 2nd Fable is held in reserve for an unresolved dispute only.

**Account load:**
- CP: 6 leads, 6 Opus reviewers and the Fable thread, 13 in all (≈ 62%).
- CW: 4 leads and 4 Opus reviewers, 8 in all (≈ 38%).

**Usage-limit rule (Felipe, 2026-10-22):**
- If Claude Personal or Claude Work hits its usage limit, the affected threads and agents are paused, not shut down or moved.
- Once the limit resets, each one resumes in the same thread from its STATUS.md resume point.

**Label after Stage B:** "proved (Opus 5.5 lead; independent reviews: Astra x2 + Opus xhigh; campaign review pending); not adopted".

**After all ten finish:**
1. Collect every proof into one detailed document.
2. Run Stage C (Fable 5.1 high on CP plus one Astra).

| Theorem | Parts | Account | Thread | Folder | Status |
|---|---|---|---|---|---|
| T09 kernel validity | all | CP | mcp:dbfa5484-526f-4213-aaeb-38fe5255a7ea | T09_T7_kernel_validity\ | proved (Stage B done); settled |
| T11 iid discovery identity | (iii) | CP | mcp:ac899439-2380-4302-a96a-22f422b71ce5 | T11_LLED_scoring_ledger\ | proved (Stage B done); settled |
| T12 frozen-run identities | all | CP | mcp:93aff517-48a5-46f5-9ef8-7becfded9287 | T12_T8_frozen_run_identities\ | proved (Stage B done); settled |
| T13 restricted ESS | all | CP | mcp:c1287ba9-238e-439d-888b-55f3f91a3ced | T13_T10_restricted_ESS\ | proved (Stage B done); settled |
| T14 first-moment lemma | (i) | CP | mcp:cad6f849-f42e-4160-bbf3-6bdbe943cdab | T14_LFM_first_moment_evidence\ | proved (Stage B done); settled |
| T15 occupancy | all | CP | mcp:cafe4852-83a2-40b4-9cae-e202e0776487 | T15_LOCC_occupancy\ | proved (Stage B done); settled |
| T20 local search | (i)–(ii) | CW | mcp:effed2fb-c77a-4cd6-9498-54fab876eb3c | T20_T15_local_search\ | proved (Stage B done); settled |
| T22 start-side inequalities | (i)(ii)(iv) | CW | mcp:bcab883e-034f-48da-beac-8e8e02c02bad | T22_T16_start_aggregation\ | proved (Stage B done); settled |
| T23 path-wise PIP bound | (ii) | CW | mcp:71f684c8-8896-4867-8b0a-a6ac21552466 | T23_T18_basin_prefix\ | proved (Stage B done); settled |
| T31 Markov coverage | (i) | CW | mcp:2d826eca-e021-4b43-aa26-104ba118fd9f | T31_T22_certificates\ | proved (Stage B done); settled |

**2026-10-22 16:55Z:** all 10 proved and settled. The collected document is being assembled into COLLECTED/ (Sonnet agent; verbatim, with acceptance checks). Stage C follows.

**Stage C launched (2026-10-22):**
- The collected document is COLLECTED/COLLECTED_PROOFS_v1.pdf: 157 pages, 0 errors, every proof verbatim (word match 98.3–100%), and the proof hashes match.
- Fable 5.1 (high) review thread on CP: mcp:8ba816ad-574f-488c-ba74-98c5025d6aeb. Phase 1 is a blind review.
- An independent Astra (xhigh) review runs in parallel; the packet is in a temp folder.
- Fable count: 1 of 2 (1 held in reserve).

**Stage C CLOSED (2026-10-22 18:10Z).**
- Fable 5.1 (blind, then rulings) and Astra xhigh both hold all ten proofs correct. No argument was opened and no judge was used. Fable count: 1 of 2.
- Edits applied: E12-1 and E12-2 (T12, PROOF_v6) and E23-1 (T23, STATEMENT.md and PROOF_v5).
- Final collected document: COLLECTED/COLLECTED_PROOFS_v2.pdf (157 pages, 0 errors). v1 is in COLLECTED/archive/. Reviews are in COLLECTED/review/.
- Final label: "proved (Opus 5.5 lead; independent reviews Astra x2 + Opus xhigh; campaign review Fable 5.1 + Astra: correct); not adopted". Adoption is Felipe's word.

## Wave 2 (launched 2026-10-22 ~18:55Z; OpenAI only: GPT-6 Astra (high) lead + 2 GPT-6.1 Sol (high) reviewers; Astra xhigh statement checker and judge)
Brief: WAVE2_BRIEF.md (also at C:\Users\felip\AppData\Local\Temp\proofbrief2.txt).

| Theorem | Parts | Thread | Folder | Status |
|---|---|---|---|---|
| T22 start concentration | (iii) under EXP′ + NL_η | mcp:98f5c42a-6d3a-4afc-bf16-e79281c7fcc9 | T22iii_T16_start_aggregation\ | proved (2 Sol verified); settled |
| T21 HPM composition | (C1), (a)–(f) | mcp:9a9669da-25f0-421f-80cd-1c3b616f5a1a | T21_T14H_HPM_composition\ | proved (2 Sol verified); settled |
| T27 start-mass law | (i) | mcp:1cbc576d-fc3d-4526-bc86-3863d5b79ddc | T27i_T20C_cancellation_budget\ | proved (2 Sol verified); settled |
| T25 PW2 variance bound | (iv) (+ optional PW2) | mcp:4669e7ce-dee4-4f44-a5f8-43d40c80048c | T25iv_T19_crossing_evidence\ | proved (2 Sol verified); settled |

**Wave-2 closing review (Felipe, 2026-10-22).** When all four wave-2 threads finish, one extra GPT-6 Astra (xhigh) thread reviews all four proofs for correctness:
- blind first, then ruling on the claims logs;
- citations of wave-1 results checked against COLLECTED_PROOFS_v2;
- output in proofs/WAVE2_REVIEW/.

The 30-minute check launches it.

**Wave 2 done (~19:30Z):** all 4 proved, both Sol reviewers verified. Closing review: Astra xhigh thread mcp:f2ee20dc-0f7a-4efe-9c43-3ebffe7b5c00 → proofs/WAVE2_REVIEW/.

**Wave-2 closing review DONE (19:44Z; Astra xhigh, thread settled).** All four verified, blind and final. No edits required. Every logged claim is resolved, wave-1 citations match, and there is no cycle.

Scope notes for future use:
- Keep EXP′/VIS/leakage, H03/H10/H24, H2/H3 and PW2 explicit.
- T22(iii) concentration and T27(i) cancellation describe different regimes; never combine them on one sequence.

See WAVE2_REVIEW/REVIEW.md.
