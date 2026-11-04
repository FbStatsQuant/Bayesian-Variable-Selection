# FAILED_ATTEMPTS.md (theory architecture run, SMC-BVS v3)

None yet (2026-10-19).

- 2026-10-19, council round 1, Fable-C1 (representative): the agent's full reply exceeded the harness transport and arrived truncated (only the end of §2 from CA2-5, §3–§6 reached the lead; saved as council/r1_FABLE_C1_tail.md). A request to re-send in two parts was stopped by a model safeguard, so the original text is unrecoverable. Fix: re-run Fable-C1 round 1 with a fresh agent (still independent: it sees no other member's list) and a hard cap of 7,000 words. Do not ask an agent to re-send a long reply; cap lengths instead.

- 2026-10-20, send-back round: both Fable council agents (Fable-C1, Fable-C2) stalled with "no progress for 600s (stream watchdog did not recover)" while reading council/PROPOSAL_v1.md in parts; no reply produced. Relaunched as fresh agents with the same brief (two extra Fable calls). If it recurs, instruct the agent to read PROPOSAL_v1.md with offset/limit chunks of ≤ 150 lines.
- 2026-10-19/20 (overnight), send-back round: the first attempt to resume both Astra sessions failed on a DNS/network outage (codex websocket "No such host is known"); the operator preserved the failed logs (council/astra*/r4_attempt1_failed.log) and ran the one allowed retry of the same command after connectivity returned; both retries succeeded with the same session ids. Fable-C1's send-back answer was truncated in transport (second occurrence for that member); a short fresh summary of the lost head was obtained instead of a verbatim re-send (which a safeguard had blocked on 2026-10-19).
