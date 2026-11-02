# Theory campaign ledger (HQ = T3 thread "New BVS Headquarters", Owls)

Credits: $245 cloud-session credits (Personal), expire 2026-11-05 07:59 UTC (1:59 AM CST). Cloud runs = Opus 5.5 only.
Fable/Astra escalations: separate T3 threads on subscriptions (balance Claude Work / Claude Personal).

**BILLING (verified 2026-11-02):** routines (RemoteTrigger / triggers API) are EXCLUDED from the cloud credit and bill weekly plan usage. Sessions created with `claude --cloud` DO bill the credit (a test session moved it from $245 to $244 with the plan unchanged). Launch every credit run with `~/.config/bvs-hq/launch_cloud.sh TASK_ID` (tmux pseudo-TTY + `claude --cloud`; Personal config). Session URLs are logged in `~/.config/bvs-hq/cloud_sessions.log`. Monitor a session with RemoteTrigger get_run_log using session_id cse_<suffix of the session_ URL>.
Inputs: GH-PACK transfer landed on main as c4ef0dc (2026-11-02); Wave 1 prompts embedded what they needed. Later waves read from main.

## Wave 1 (created 2026-11-02 ~16:00 UTC, model claude-opus-5-5)
| Task | Routine | Branch | Scheduled |
|---|---|---|---|
| W1-T37R restate T37 | trig_0182js57bVQZahQ16SryUbwB | theory/W1-T37R | 16:01:30Z |
| W1-T24G Gibbs-path repair | trig_01WtU11nXb4xuqiFMothspbW | theory/W1-T24G | 16:03:00Z |
| W1-T38E T38 delivery/eligibility | trig_018hmxt6dY6i2rtYjwsxn2Co | theory/W1-T38E | 16:03:30Z |
| W1-T03R T02 tail + T03 restatement | trig_013YamuSQR6U3vJGbe9xqP5Z | theory/W1-T03R | 16:04:00Z |
| W1-EXP T22+T27 family, EXP' | trig_01NVzjRNzdF3a2T8Gt5vz8f2 | theory/W1-EXP | 16:04:30Z |

Smoke test: trig_01TdWXN5cb4qFMoyjMquAnrs (fired twice; branch theory/smoke-test; delete later).

Wave 1 billed weekly PLAN usage (routines), not credits.

## Wave 2 (2026-11-02 17:20 UTC, `claude --cloud`, Opus 5.5, credit-billed)
| Task | Session |
|---|---|
| W2-VT24G verify Theorem B | session_01PQxfqySzkCD7fJxcQ16eHT |
| W2-VT03R verify T03 sharp | session_01PQxfr3wMBDPm1AJwRgZsmz |
| W2-PREM Theorem B premises | session_01PQxfr1ST3w5Mbz1YDufpUz |
| W2-T26 evidence/PIP consistency | session_01PQxfr1MVeeqhgqNtppfaVU |
| W2-BOOK bookkeeping restatements | session_01PQxfr2ZraGSVTmp9m1RxzE |

## Wave 3 (2026-11-02 17:23 UTC, `claude --cloud`, Opus 5.5, credit-billed)
| Task | Session |
|---|---|
| W3-VT37R verify W1-T37R | session_01PQxfqzxWYPwNVkWrHY35WD |
| W3-VT38E verify W1-T38E | session_01PQxfr2yPS6HtgeUMUXxxxW |
| W3-VEXP verify W1-EXP | session_01PQxfqzbTFigWzgzVLBarjG |
| W3-PXN p >> n joint family | session_01PQxfqzMRuTfx7CzfyBXYqN |
| W3-PGD PGD/LD for refined T37 | session_01PQxfqzyBxybg1PmiQ8ArGV |

Credit readings: $245 (16:00), $244 (17:19, after 7 s test), $239 (~17:22, right after Wave 2 launch).

## Wave 4 (2026-11-02 ~17:55 UTC)
| W4-T38FULL assemble T38 | see cloud_sessions.log |
| W4-SHARE route b2 delivery | see cloud_sessions.log |

## Plan-funded team (2026-11-02 18:02 UTC; Claude Personal weekly plan, 29% left, resets ~21:00 UTC; Felipe: "use as many threads as you want")
| ID | Model | Task | Branch |
|---|---|---|---|
| F-SHARE | Fable 5.1 max (CP) | route b2 delivery crux | theory/F-SHARE |
| F-REFINE | Fable 5.1 max (CP) | P6 believed versions, confidence cards, architecture, next tasks | theory/F-REFINE |
| F-PXN | Fable 5.1 max (CP) | p >> n joint family, TD′ asymptotics, the masking vs dominance tension | theory/F-PXN |
| O-LS0 | Opus 5.5 xhigh (CP, Owls, <= 40 cores) | LS0 post hoc on the 2,400 regenerated datasets | theory/O-LS0 |
| A-REV1 | GPT-6 Astra high (Codex) | cross-family review: Theorem B, T38(b)-R, Lemma S, D2, E3 | theory/A-REV1 |
| A-REV2 | GPT-6 Astra high (Codex) | cross-family review: T03♯, refined T37, EXP′ (NOT STARTED: T3 connection errors; retry) | theory/A-REV2 |

### 18:20 UTC relaunch (after T3 restarts and the Owls overload)
F-PXN cancelled (superseded by W3-PXN). F-SHARE, F-REFINE relaunched at Fable xhigh (CP). O-LS0 relaunched light (≤2 cores via owls_run; NOTS if > ~6 core-hours). A-REV1, A-REV2 (Astra high) relaunched. OWLS-STEWARD (Sonnet 5.5, Claude Work) is building the guardrails in ~/.config/bvs-hq/owls/.

### 18:35 UTC: original-draft track (Felipe's first draft "Local-to-Global Bayesian Computation", copy in ~/.config/bvs-hq/inputs/)
| ID | Model | Task | Branch |
|---|---|---|---|
| F-DRAFT | Fable 5.1 high (CP) | map the draft's theory targets onto the current list; new target statements | theory/F-DRAFT |
| O-WSTAB | Opus 5.5 xhigh (CP) | prove the draft's weight-stability theorem (chi²/KL(pi‖pi0) vs cross-block dependence; ESS; regime dichotomy) | theory/O-WSTAB |
| A-DRAFT | GPT-6 Astra high | novelty audit vs the literature; E[h] consistency theorem; naive-merge-fails proposition | theory/A-DRAFT |

## Wave 5 (2026-11-02 18:40 UTC, `claude --cloud`, credit-billed; specs from F-REFINE NEXT_TASKS)
W5-VMASK, W5-VPGD, W5-B2ENV, W5-FAVIID, W5-LOCKBOOK (session URLs in ~/.config/bvs-hq/cloud_sessions.log).
F-REFINE DONE: theory/F-REFINE @ db708ca (CARDS.md, ARCHITECTURE.md, NEXT_TASKS.md).
