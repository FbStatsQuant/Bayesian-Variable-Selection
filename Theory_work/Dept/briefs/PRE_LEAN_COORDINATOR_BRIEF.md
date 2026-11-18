# Pre-Lean pass, coordinator brief (owner GO via HQ, 2026-11-18)

**Read first, in full:** `Theory_work/Wave3/PRE_LEAN_PASS_BRIEF.md` on origin/main (83736209 or later). It is binding: targets T1–T6, Sol confirmations 1–5, the Fable role, the acceptance rules and the output layout.

**Your role.** You are the Sonnet coordinator, explicitly on claudeAgent_personal. You prepare the packets, run the Codex calls one at a time, collect the outputs and apply the adopted changes. **You do not rule on findings.** The manager's Fable child writes the ruling card for every target. Work on branch `theory/PRE-LEAN` from origin/main, in folder `Theory_work/Wave3/PRE_LEAN_PASS/<target>/`. Never push to main, and never edit registry files.

## Order (now)
**Widened by the owner on 11-18 (HQ brief, main f60744a4): "a whole pre-Lean check", covering every presented theorem and corollary on the card.** The order is T1 Astra → Sol-1 → T2 → Sol-2 → T3 → Sol-3 → T4 (now including Thm 1′) → Sol-4 → T5 → T7 (Thm 4, row 1.4) → T8 (Thm 7, row 3.2 + Thm 5, row 3.3) → T9 (row 3.5 + Thm 10, row 3.6 + pooling, row 4.1) → T10 (Thm 8, row 3.7). T6 (rows 3.1 + 3.1L + 3.1F) and Sol-5 come only after Cor 6L is recorded; the manager will tell you when. Empirical rows and remark 2.2 are out of scope.

## Per call
1. **Packet:** `<target>/PACKET.md`. It contains the exact claim ids, each with its verbatim main registry status and version; STATEMENT and PROOF spans as file:line on main; dependencies; and the single question to answer.
   - **Astra (T1–T5):** "break it". Look for a genuine flaw, a wrong step, an unstated hypothesis, or a step that would not compile in Lean.
   - **Sol (1–4):** final-text confirmation of a result whose last council round was Opus-only. Give per-claim ACCEPT/REJECT on the recorded text, with a verdict line `COUNCIL-VERDICT round=R<digits> manifest=<recorded digest> seat=sol score=… gates=…` bound to the recorded manifest. Look up each digest in the registry cell.
2. **Converter:** run the ingest converter (`ingest.py convert` on the relevant REPORT) and `manifest.py verify` locally before the call. Do not spend a Codex call on a format failure.
3. **The call:** delegate_task, provider `codex`, model `gpt-6.2-astra` or `gpt-6.2-sol`, `reasoningEffort: high`.
   - Give the model a short wrapper: it reads `<target>/PACKET.md` and the listed files, reading long files in chunks of 120 lines; it reads nothing else; it writes nothing; and its final message is its review. Put a first line `MODEL: <id> (codex, reasoningEffort high)` in the reply.
   - **One call at a time.** A re-call is allowed only on a tooling void, such as truncated input.
4. **Save** the reply verbatim as `<target>/CODEX_<model>.md`. Commit and push, then **report to the manager in ≤ 6 lines**: path, verdict, the count of findings, and anything urgent. The manager forwards it to the Fable.
5. **Wait for the manager's ruling card before the next call**, or continue in parallel if the manager says so. Apply the adopted changes:
   - adopt only localized proof simplifications with the statement unchanged;
   - each one gets one Opus diff check (fresh, claudeAgent_personal, high);
   - add a Sol 6.2 check only if the manager says the change is substantive;
   - statement changes are NOT applied: list them for HQ.
6. **SOL62_QUALITY:** after each 6.2 review (Astra or Sol), send the manager one line in the format `| date | target | type | F | N | B | S | reason |`, rated against what 6.1 would have done.

## Hygiene
- Scratch goes only under `<worktree>/.rc_tmp/`, with no redirects outside the worktree and no deletes.
- Every subagent is explicitly on claudeAgent_personal; the only exceptions are the Codex calls.
- Kill budget for the whole pass: about 3–4 days. Codex calls: about 15 in total (10 Astra, 5 Sol). Fable: about 10 passes.

## End
`PRE_LEAN_PASS/SUMMARY.md`, one page: findings, what changed, what was declined, and the Lean-readiness notes the Lean Department will use as blueprint input. Draft it from the Fable cards; the manager finalizes it.

## Consistency tier (owner 11-18: "especially crucial results like the consistency ones"; HQ brief main 668b413f)
These targets get extra treatment: **T4** (Thm 1, 1′ and the presented Thm 2), **T5** (Thm 9), **T6** (Thm 6, Cor 6L, Cor-FAMC), **T8's Thm 7** and **T9's Thm 10**.
- **Second adversarial read by Sol 6.2.** After each Astra call on these targets, run one blind adversarial read with `gpt-6.2-sol`, reasoningEffort high. Give it the same `PACKET.md` and the same "break it" wrapper, and **never show it Astra's reply.** Save the reply as `<target>/CODEX_gpt-6.2-sol_adv.md`. These are separate from the Sol final-text confirmations 1–5.
- **Fable proof walk.** The Fable does a full proof walk on these targets, and the manager routes its cards to HQ and the consultant. Nothing more for you to do, except to note the card path in your report.
- **Budget:** about 20 Codex calls in total (10 Astra, 5 Sol final-text, 5 Sol adversarial). Kill at about 4 days. Codex calls stay one at a time.
