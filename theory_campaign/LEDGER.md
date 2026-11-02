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
