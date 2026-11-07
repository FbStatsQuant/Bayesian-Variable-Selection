> **Archive note.** In this archive, "02a" means `02_theory.md` (final state), "02b" means `02b_theory_campaign_history.md` (campaign history), and "REG-A"/"REG-B" or "registry A/B" mean parts A and B of `ID_REGISTRY.md`. Paths like `branch_snapshots/...` and `transcript/...` are relative to this folder.

# 03b. Reasoning record: decision log, dead ends, reversals, reviewer findings, trace index

Companion of `01_overview_and_timeline.md`. Thread positions are `[pos N]`; transcript parts are `transcript/part_01 … part_08` (message text) and `transcript/traces/traces_01 … traces_08` (HQ reasoning, delegate briefs, tool inputs). Branch files are `branch_snapshots/<BRANCH>/…`. IDs: `ID_REGISTRY_A.md` (TH01–TH22, CJ01–CJ27, DR, LIM, OB, DF, RL, MD, DS, CL) and `ID_REGISTRY_B.md` (TH101+, LM101+, CJ101+, RF101+, CE101+), always written `ID (native name)`; `no ID (…)` means the registry has no row for it.

Conventions. Text inside quotation marks is verbatim from the cited position. Everything else is a **Summary:** by the editor. Statuses are copied from the registries and never upgraded. "SF" = same-family (Claude) check, "XF" = cross-family (Astra/Sol) check. "Decider" is Felipe (user) or HQ (this thread's assistant, Opus 5.5 on Claude Personal) or a named meeting chair.

---

# (a) DECISION LOG

## A.1 Credits, accounts, billing, infrastructure

**DEC01. Credits first, with a stop rule** [pos 16, 19, 24, 53, 73, 180, 782].
- Decider: Felipe (credits first); HQ (stop rule and final synthesis run).
- Decision: spend the expiring cloud credits on theory; stop launching at about $30–40 left or the evening of Nov 4; one last session writes a synthesis; then back to subscriptions.
- Reasons: Felipe [pos 19] "The goal is not just to use the credits but to do actual work, we need to have a plan for when we need to transition from usage sources." HQ [pos 24] "Stop launching new sessions when either about $30–40 of credit is left, or it's around the evening of Nov 4, whichever comes first."
- Alternatives rejected: run theory locally on Claude Personal ("local Claude Personal agents won't spend either of the two credit pools" [pos 51]); fixed number of sessions with no balance checks (HQ asked Felipe to read the balance at checkpoints [pos 24, 355, 370]).
- Evidence: balance readings $245 (16:00), $244 (17:19), $239 (~17:22), "$21 of $250 left" (20:35, ledger).
- Outcome: stop line passed at 20:30; "That's past my stop line … so **no more cloud sessions.**" [pos 782]; W8-SYNTH was the last credit session; about $229 over Waves 2–8 [pos 784].
- Affected: all W2–W8 results (see timeline). Later reversal: none; the API credit became the next funding line (DEC12).

**DEC02. Model allocation: Opus on credits; Fable/Astra on subscriptions in separate threads** [pos 88, 90, 809, 905, 1061].
- Decider: Felipe.
- Reasons: [pos 88] "Those credits will evaporate soon if we spawn Fable a lot, and using them on Sonnet is not worth it in my opinion."
- Alternatives rejected: Sonnet on credits; Fable on credits (HQ later at [pos 905]: "I'm reserving Fable for the three hardest open problems, since it costs roughly 2.5× Opus per token").
- Evolution: [pos 164] balance CW/CP; [pos 384] "use as many threads as you want" in a CP window (Fable on CP); [pos 809] "use CW for all future agents for today"; [pos 1061] "use CW instead of CP".

**DEC03. Routines vs `claude --cloud`** [pos 238, 286–342].
- Decider: HQ, after Felipe's observations "this is claude cloud, i dont see anything" [pos 288] and "still 245" [pos 298].
- Decision: stop routines; launch every credit run through `claude --cloud` (tmux pseudo-TTY wrapper `launch_cloud.sh`).
- Reasons: [pos 305] "Routines are explicitly excluded from the cloud-session credit, so they bill your plan. Sessions started with `claude --cloud` from a terminal do count". Verified: [pos 333] "the 7-second `--cloud` test took the credit from $245 to $244, while your plan stayed at 71%."
- Evidence: weekly plan rose 65% → 71% during Wave 1 [pos 286]; research subagent "Research cloud session credit eligibility" [pos 303].
- Alternatives rejected: continuing with routines; relying on a billing lag explanation.
- Affected: Wave 1 results (TH198, TH199, TH201, TH218, TH128, TH136, TH241, TH242) were paid from the plan; Waves 2–8 from credits.
- Reversal: this reversed the HQ's own statement at [pos 238, 243] that Wave 1 spent the credits.

**DEC04. Opus vs Fable usage and effort level** [pos 88, 427, 572, 723, 809, 905].
- Decider: Felipe (effort and account rules); HQ (which tasks get Fable).
- Decision: Opus 5.5 at high effort as default; Fable 5.1 only for the hardest/most sensitive tasks (hard proofs, statement refinement, adversarial review); Sonnet/Haiku for clerical work; no max or xhigh.
- Reasons: Felipe [pos 427] "max mode is not necessary at all, bring back everything to xhigh"; [pos 723] "no xhigh, all high at most"; [pos 809] "Opus 5.5 as default for important things, if the task is very sensitive / difficult then Fable 5.1".
- Alternatives rejected: initial max-effort Fable runs were cancelled [pos 430, 451].

**DEC05. The "T37-first bend": parallel tracks and Felipe's gate** [pos 156, 158, 162, 185 (reasoning)].
- Decider: HQ proposed; Felipe clarified.
- Decision: HQ proposed Track B ("Opus 5.5 cloud runs on targets whose statements are already frozen, plus the T37 exploration") because the credits expire Nov 5; Felipe: "you need to work independetly, my task is to approve the target for theorems, once done you need to work fully autonomously" [pos 158 comment]. HQ withdrew its earlier "promise to ask before each escalation" [pos 162].
- Reasons: [pos 156] "This needs your approval because it bends the shortlist's rule that T37 comes first and the proof team waits for your green light." HQ reasoning [pos 185]: Felipe's "greenlight, deploy" "covers this campaign, and these Wave 1 items are card-production work that comes before G3 anyway."
- Evidence: shortlist table [pos 156]: T03/T01/T02, T07, T22+T27, T21, T12+T31, T26, T37, T38, T39.
- Affected: W1-T37R (TH199, TH201, RF101), W1-T38E (TH241, TH242, TH240), W1-T24G (TH218), W1-T03R (TH128), W1-EXP (TH136).

**DEC06. GitHub token and push path** [pos 208, 243–280].
- Decider: HQ asked; Felipe created a fine-grained token (contents + pull requests, one repo) pasted via a private card.
- Reasons: Owls had only a deploy key for the Lean repo [pos 208]. Alternative rejected: embedding documents in every prompt (still done for Wave 1, [pos 211–214]).

**DEC07. Owls guard rails and relocation to the laptop** [pos 426–480, 603–666].
- Decider: Felipe asked ("be very mindfuld w Owls usage" [pos 426]; "deploy sonnet / 6.1 sol agents to manage our connection to Owls" [pos 446]; "owls is shaky af, can you re launcg the threads on my Felipe Bedoya laptop instead" [pos 606]); HQ designed.
- Decision: OWLS-STEWARD (Sonnet, CW) built `owls_run` (2 cores per job, 8 total, single-threaded BLAS, low priority), a guard daemon and `POLICY.md`; heavy work to NOTS; guard as a systemd user unit; theory agents moved to the laptop via `t3_thread_launch` with worktrees (delegate_task cannot isolate worktrees on linked machines [pos 654]).
- Evidence: load ~708 on 80 cores; O-LS0 ~34 cores [pos 440].
- Later: a systemd user unit is also the long-job rule (DEC42).

**DEC08. API run caps and daily rate limits** [pos 908–911, 953].
- Decider: HQ. Decision: 8 API runs now; hold API-UMODEL and API-T03CONST; keep ~$20 reserve.
- Reasons: [pos 911] "Your Console's daily rate limits allow only about 100K Fable and 400K Opus output tokens per day". Hard $15 default cap per run ("`--max-budget-usd`" [pos 834]).

## A.2 The method: LS0, SR, start variants, spine

**DEC09. LS0 adoption** [pos 355, 372–374, 510, 514, 523–526, 774, 796, 1107].
- Decider: HQ advice; Felipe approved ("approved" [pos 523 comment]); conditional on the data check.
- Decision: LS0 (one deterministic local search from the exact start mode, centre emitted first) is part of the method.
- Reasons: HQ [pos 514] "**My advice: adopt LS0, but only after O-LS0's data check passes. Present it as part of the method from the start, not as a patch.**" Reasons given: "It closes the main theorem's biggest hole", "It costs almost nothing", "It needs no reruns", "It leaves the rest of the method's theory intact". Risk named: LS0 might find a model scoring above the truth where the method reports the truth.
- Evidence: O-LS0 [pos 770–774]: changed the reported HPM in 0 of 2,394 completed fits, recovery unchanged, cost <0.1%; S-ELS CJ222 (ELS-1): final local search made 0 moves in 2,394/2,394 fits. Caveat: most T38 premises fail at n=200 (π₀(S̃₀)>½ in 18/2,400; move cap in 1,968/2,400, ledger 20:33), so LS0's value is asymptotic.
- Alternatives considered: the route without LS0 (route b2); mixture of block starts (B-merge, TH181 Theorem B3, O-MIX), common-σ² tables (DEC11); backfit/residualised tables (DEC12).
- Affected: TH160, TH161, TH153, TH169, TH290 (T38-v3), TH05.b1LH; MD03 (LS0 in the shipped core); CJ213 (LS0 in production core, OPEN as an implementation premise at the audit); OB03 (N3).
- Later: [pos 1107] LS0 added to production in v3.1 because API-AUDIT [pos 1009] found it "exists only in a test export"; the headline question "LS0 vs no-LS0" stays open in the registry as CJ215 (D2 (T38-RECORD Part IV); Theorem 5(b) headline decision), resolved in the final list by TH05.b1LH (with LS0) and TH05.b2LH (labelled variant without LS0).

**DEC10. The SR audit** [pos 516–541].
- Decider: HQ ("Take care of this yourself" [pos 516 comment]).
- Decision: HQ checked the engine code for the "SR" reading (both Gibbs configurations count as scored and logged).
- Evidence: `v3_engine.h:102`; "No call ever scores a model without logging it" [pos 533]; "The SR assumption holds in the code." [pos 541]. Written to `campaign/HQ/SR_AUDIT.md`.
- Affected: CJ128 (SR; GUARD; stop-only coupling; IMPL-GUARD); LM191 (GUARD); later reconfirmed by API-AUDIT [pos 1009].

**DEC11. Common-σ² start tables rejected** [pos 616, 763, 796, 937, 1009, 1107].
- Decider: HQ recommended ("**Common-σ² start: reject.**" [pos 796]); recorded in the PR #1 amendments [pos 850]. Whether Felipe explicitly ruled is **UNCERTAIN**.
- Reasons: F-DRAFT flagged the shared plug-in σ² as a possible method change [pos 616]; "Two agents independently found it floods the start in study-like designs" [pos 796]; oracle σ² gives median log₁₀π₀(S₀) −690 and π₀(R₂)=0 (O-DILUTE, 480 fits); −1,303 in F-SIGMA IID500 (SYNTHESIS §6).
- Evidence: F-SIGMA (TH186 Theorem S2, TH187 Theorem S3, TH188 Theorem S4, TH176 Prop S), O-DILUTE, API-RESID ("A common σ̂² start fails, so that pilot is dropped" [pos 1009]), RF150 (Common plug-in sigma^2 is the right tool for the n = 200 dilution masking).
- Alternatives rejected: shared plug-in σ² ("vacuous as an improvement over v3" in the fixed-β regime, TH188).

**DEC12. Residualised/backfit start tables not adopted** [pos 796, 937, 1009, 1130, 1280, 1480].
- Decider: HQ, then the method meeting (decision 1).
- Decision: block (local-to-global) start kept; backfit start rejected for paper 1 (MD01).
- Reasons (final): "your ground rules; switching to backfit would mean a full re-run; no exact backfit sampler with a known normaliser exists, so its Ẑ would not be unbiased; there is no theorem for it" [pos 1480]. The earlier "at most 6 of 2,400" rationale was withdrawn: "The argument that the backfit start could gain at most 6 of 2,400 fits doesn't follow." [pos 1480].
- Evidence: pilot 378/480 favourable (SYNTHESIS §6); API-RESID backfit favourable in 78.7% of regenerated fits [pos 1130 says "79–92%"].
- Affected: CJ162 (Backfit start; residualised tables), CJ163; OB; Arm D recorded as v2 evidence only.

**DEC13. The spine correction ("tempering is needed" → "moving off the start is needed") and PR #1** [pos 796, 798, 800, 807, 850].
- Decider: Felipe ("Make all necessary changes then" [pos 798 comment]); HQ launched E-SPINE (Opus high, CW).
- Decision: change every statement saying the bridge or sampler is "needed" into "the run must move off its start, and v3's moves do that"; edits to `main` documents go in a pull request, not a push; T38/T39 conjecture files not edited because of the Oct 28 freeze hashes.
- Reasons: W7-SEP showed the claim false on LH [pos 796]: "A spine claim was refuted".
- Evidence: TH388 (Prop GU; greedy universality), RF104 (tempering is needed), RF264.
- Output: PR #1 https://github.com/FbStatsQuant/Bayesian-Variable-Selection/pull/1 (unmerged at [pos 850]; later status UNCERTAIN).

## A.3 API credit

**DEC14. API credit launcher on the Agent SDK** [pos 822–894].
- Decider: HQ (Felipe supplied the key via a private card).
- Decision: headless workers use the Agent SDK with a hard per-run cap and a separate config dir.
- Reasons: [pos 880] "Direct API calls work with the credit, but Claude Code isn't covered by the promotion, while the Agent SDK is and runs the same loop." Org: no payment method, $195 monthly limit [pos 867], so "Nothing can ever be charged to a card here".
- Alternatives rejected: Claude Code CLI with API key (refused: "credit balance is too low") [pos 874–877].
- Evidence: test run $0.002 [pos 890].

**DEC15. API wave allocation and caps** [pos 905–911].
- Decider: Felipe ("feel free to deploy Opus / Fables on those credits, get the most out of those credits" [pos 901]); HQ allocated.
- Decision: Fable on API-PXNGAP and API-N200 ($25 each); Opus on the rest ($10–15); API-VSTAB ($12) added after A-REV7; ~$20 reserve for repairs.
- Alternatives rejected: Fable for everything; running Astra/CW-covered tasks on the API.

## A.4 Control, phases, literature and reframing

**DEC16. Control over speed and the gated four-phase plan** [pos 949–953].
- Decider: Felipe set the rule; HQ designed the phases.
- Reasons: Felipe [pos 949] "I'd rather prioritize control and a solid base over speed".
- Decision: Phase 0 finish in-flight runs (no new launches); Phase 1 consolidate and fix; Phase 2 literature survey with decision memo; Phase 3 "airtight within our control"; "No new phase without your OK." [pos 953]. Scout-before-dive, hard caps.
- Alternatives rejected: HQ's earlier two tasks held for "tomorrow" were not started [pos 953].

**DEC17. Theorem-count recommendation (successive estimates)** [pos 957, 1348, 1650].
- Decider: HQ (advice), then the meeting.
- Estimates: 8 main + ~11 lemmas + ~5 remarks (frozen Oct 28) → "6–7 main results and 12–15 in the supplement" [pos 957] → "About 22 main theorems in total. Around 14 would go in paper 1" [pos 1348] → final: 8 main + 12 supplement cards [pos 1626, 1650].

**DEC18. One HQ per main theorem** [pos 959, 963, 1341, 1350, 1353].
- Decider: Felipe ("we will create one HQ per main theorem" [pos 959]); HQ designed (meta-HQ owns registry; dependency map; waves of 3–4).
- Reasons: "the more we decentralize the more tokens and computation I can manage to arrange" [pos 959].
- Scope narrowing: [pos 1350] "the new HQs are for Paper 1 - Bioemtrika level"; harder results become future work (CJ01–CJ27) [pos 1353].

**DEC19. Literature phase on the API credit** [pos 949, 953, 980–989, 1009].
- Decider: Felipe proposed ("we stop and browse for all related, or close literature" [pos 949]); HQ ran four Opus readers (~$8 cap each) on the API credit ("we seem to have still a lot of usage, can the literature search be done through those credits as well?" [pos 980]).
- Output: [pos 1009] verdicts.

**DEC20. Biometrika + Lean target and checkpoints** [pos 1015, 1018].
- Decider: Felipe. Decision: version 1 is the Biometrika paper; key results get Lean certificates; harder results wait.

**DEC21. Reframing the objectives: posterior accuracy first, parallel scaling as motivation** [pos 1020, 1028, 1030, 1040, 1044, 1046–1061].
- Decider: Felipe.
- Reasons: Felipe [pos 1020] "precision of the BVS part is not the main target neither is consistency or any theoretical property as there are already good BVS algorithms"; [pos 1030] "retire MCMC for BVS".
- Effects: HQ re-ranked the theory (accuracy of Ẑ, PIPs, joint inclusion > cross-block cost > parallel cost > selection accuracy [pos 1028]); LIT-PAR launched to falsify the gap claim [pos 1035]; thesis sentence [pos 1044] "In split-and-merge, correlation breaks correctness. In local-to-global SMC, correlation costs only sequential depth and particles, never correctness." (the "never correctness" half is known; "costs only depth" half open per THM-INV [pos 1107]).
- Reasoning trace: HQ [pos 1025] "The literature readers were assessing against the wrong target".

**DEC22. Two-track settlement plan; full authority** [pos 1055–1061].
- Decider: Felipe asked ("how are we going to settle things down?"); HQ proposed Track A (METH-AUDIT, A2 empirical) and Track B (THM-INV, THM-SYNTH, Astra cross-check); Felipe: "You have full authority execute your own plans, this what you need to bring me though: 1) Final proposal for the method we will ship 2) Specific list of theorems".
- Budget: ~$80 for tracks, ~$60 reserve [pos 1059].

## A.5 v3.1, selection, PIP, meeting

**DEC23. v3.1 = v3 + parallel execution layer** [pos 1072, 1107, 1296].
- Decider: HQ (under DEC22's authority).
- Decision: "ship v3 unchanged, plus a parallel execution layer (call it v3.1)": concurrent islands (bitwise identical), parallel local-search scans, stacking, Ẑ-weighted PIP reported, LS0 in production, `log_Z` NA fix on stopped fits.
- Reasons: [pos 1107] "none of the changes is a workhorse change"; "The real problem is in the code, not the method" (production code serial everywhere); "The study's 2,400 fits stand".
- Rejected (with reason): "Splitting a fixed particle budget into many small islands. It provably makes the equal-weight PIP worse."; "Shortening calibration. It weakens three existing theorems."; "A new move kernel to cut the sequential cost per particle … would break the move-path theorems."
- Evidence: METH-AUDIT (TH394 Prop W; TH397 Prop P; TH398 Cor V); bitwise check on 1 design at [pos 1107], 3 of 3 at [pos 1251]; 358 s → 189 s with 4 islands at once.
- Affected: MD04, MD05, MD12; DF12.

**DEC24. Ablation of the block start (local-to-global)** [pos 1111, 1130, 1136, 1163, 1184, 1201, 1280, 1467].
- Decider: HQ, with Felipe's constraint [pos 1132] "I'm open to dropping it but I need a very serious, irrefutable argument."
- Decision: run block start vs singleton blocks vs prior start on 12 designs (ABL-START), pre-register a decision rule; Outcomes 1/2/3.
- Reasons: HQ [pos 1111] "if the block start doesn't beat a plain independent-Bernoulli start at matched compute, the 'local-to-global' framing needs to change"; [pos 1136] "**Short answer: no, local-to-global doesn't hold back the parallel part.**"
- Result: Outcome 2 (block start kept, no cost or accuracy claim) because the rule made every design inconclusive (prior start's evidence off by >1 nat); [pos 1280] "That flaw in the rule is mine to own as HQ: I didn't catch it when the rule was set."; rule script fixed to a 9-design absolute gate (v2) [pos 1467].
- Affected: MD01; CJ166 (ABL-START Outcome 1 depth claim; not licensed); CJ164, CJ165 (ABL-CONF).

**DEC25. HPM stays primary; MPM secondary** [pos 1142, 1162, 1251; MD02].
- Decider: HQ proposed; method meeting seats unanimous.
- Reasons: [pos 1142] "**My view: HPM stays primary, because it's the rule that is easiest to prove for an SMC output.**" Error splits as P(reported ≠ S₀) ≤ P(exact posterior mode ≠ S₀) + P(S₀ is never scored); "Neither term needs the SMC weights to be accurate."
- Alternatives rejected: MPM with equal-weight or Ẑ-weighted PIPs, FDR rules, credible sets (all "inherit the PIP-accuracy problem"); a hybrid flag when MPM disagrees (no flag, MD02).
- Evidence: 2,394 completed fits: HPM recovered the true model in 1,829, MPM in 1,779 [pos 1251]. Affected: TH05 (M5), DF15.

**DEC26. Ẑ-weighted PIP primary; equal-weight secondary** [pos 1107, 1111 (worry 4), 1130 item 3, 1251; MD08].
- Decider: HQ via meeting. Reasons: only the Ẑ-weighted PIP provably converges as islands are added (TH397 Prop P; T31(i) PROVED-LOCKED); on 3 designs PIPs differ ≤ 0.0013 and MPMs never differ [pos 1296].
- Affected: TH01 (M1), TH17 (S-POOL), DF14.

**DEC27. Meeting mechanism and seats** [pos 1164, 1169, 1171, 1197–1201].
- Decider: Felipe proposed seats ("1 Fable 5.1 C.P, 1 Fable 5.1 CW, 1 Astra, all high reasoning" [pos 1164]); HQ designed; Felipe: "Make this meeting happen".
- Decision: written rounds (blind positions, chair's disagreement table, rebuttal, tests/proof checks), HQ approves but does not vote; seats return text, chair commits; frozen dossier with Felipe's rules verbatim.
- Reasons: [pos 1169] "settle disputes with evidence rather than votes".

**DEC28. (n,p) generality rule** [pos 1214, 1226, 1302].
- Decider: Felipe. Decision: every setting must be a modelling convention with a reason, an explicit function of (n,p) or X, or a declared resource budget; no separate p≪n/p≫n rule needed.
- Evidence: 49 settings audited (DF25); fixes e1–e8, wordings w1–w7 (MD13). "Soft spot": fixed budget constants (R=4, 4 measured rounds, ×4 tier, floors 2,500 and 1,000, ESS 0.90) [pos 1302].

**DEC29. Island-level depth only for paper 1; per-particle streams = v3.2** [pos 1251, 1263, 1302, 1304, 1467].
- Decider: HQ proposed; Felipe "All approved" [pos 1304 comment]. Trigger widened by HQ at [pos 1467] to the union: paper 1 claims particle-parallel depth OR shows any p>2,500 (Sol 2 audit finding F03).
- Reasons: "My plan is to claim island-parallel depth only for v1 and keep per-particle streams as v3.2, unless the theorem meeting needs it." [pos 1251].
- Affected: MD06; TH08 (M8 Prop D).

**DEC30. Budget growth rates allowed (growth rates only)** [pos 1302, 1304, 1639; RL06].
- Decider: Felipe approved HQ's recommendation: "My recommendation: yes, limited to growth rates only, with no other method change." [pos 1302]. See DEC41 for the later change.

**DEC31. Confirmatory local-to-global test ABL-CONF** [pos 1302, 1304, 1429–1433, 1486, 1655–1669].
- Decider: Felipe approved; HQ pre-registered. Design: 3 designs × 10 seeds × 3 starts + 24 reference fits + 4 checks = 118 fits, 75-minute cap, rule committed and dry-run before any fit [pos 1486].
- Result: see DEC47.

**DEC32. Sol 6.1 reviewers as HQ staff; Sol vs Astra** [pos 1228–1238, 1304, 1320, 1408–1414, 1480].
- Decider: Felipe suggested ("deploy two 6.1 Sol - high - workers as your employees" [pos 1304]); HQ made it a "low-stakes trial first" [pos 1320]; trial passed.
- Reasons: [pos 1238] Astra "is the most valuable check in the campaign"; keep Astra as standing referee, Sol as second referee. [pos 1480] "Both Sol reviews are in. They were worth it, so both Sol roles stay for the theorem meeting."
- Roles: Sol 1 proof checker (Fable seats' claims); Sol 2 auditor (chair summaries, approvals, rules dry-run); Opus checks Astra's claims (so each claim is checked by a different family).
- No API: [pos 1324] "Also, no API"; Sol runs through Codex subscription [pos 1335].

**DEC33. Sonnet/Haiku support roster** [pos 1337–1339]: Sonnet registrar, Sonnet citation checker, Sonnet data runner, Haiku clerks; "keep them out of every mathematical judgment" (HQ). Decider: HQ (Felipe: "you can deploy as many Sonnets and Haikus as necessary").

**DEC34. Theorem-meeting design** [pos 1357, 1361]: seats Fable CP, Fable CW, Astra, fresh-eyes Fable; chair Opus (CW); checkers Sol 1 and Opus; auditor Sol 2; inclusion criteria dry-run on the draft list before Round 1; fixed card format; rules inherited from the method meeting (frozen agenda, seat output tables, "PROVED (by this seat, unchecked)" only, long jobs detached, subscriptions only). Inheritance: statuses copied word for word; known false results carried forward [pos 1361].

**DEC35. Fresh eyes: Round 0 with fresh Fable (CP) and raw Astra** [pos 1363–1371, 1385–1415, 1567].
- Decider: Felipe proposed both ("a fresh set of eyes" [pos 1363]; "this 5th consultant just seats gives a first thorough plan of what theory to explore then he leaves the place" [pos 1368]); HQ designed isolation.
- Reasons: [pos 1366] "It counters the biggest risk to 'no rock unturned': every agent so far has been anchored on the same earlier theory work." Isolation by working directory and a method-only packet (theory sections stripped), not a hard sandbox [pos 1415].
- Result: 72 items (fresh Fable), 44 packages (raw Astra); both independently found that "orthogonal blocks still interact through the shared noise variance" [pos 1567].

## A.6 Sol findings, N9, rulings

**DEC36. Dispositions of the Sol findings (no method decision changed)** [pos 1454, 1467, 1473–1480, 1512; `AMENDMENT_HQ_01`].
- Decider: HQ (Opus editor applied).
- Decisions: binding proposal goals (§13.1, §5.3) may not be silently dropped: a failed proof "comes back to you for a method reconsideration or an explicit scope change" [pos 1480]; per-particle trigger = union; item-1 rule v2; backfit rationale withdrawn; 73 findings: 45 led to edits, 28 no change [pos 1512].
- Evidence: Sol 1: 60 claims (45 hold, 19 with corrections; 7 false; 6 gaps; 2 uncheckable); Sol 2: 13 findings, 4 decision-level.

**DEC37. N9 (kernel validity) as a closure gate** [pos 1454, 1457, 1467, 1480, 1543–1557, 1593].
- Decider: HQ.
- Decision: "'No open method questions' now holds only if N9 passes." [pos 1480]; Opus (CW) proves reversibility of every elementary move, self-adjointness of the uniformly random round, and exactness of the start sampler, against the production code.
- Result: "N9 passes. All 7 sub-claims are PROVED (candidate)" [pos 1550] (the agent's own report: 8 sub-claims [pos 1593]); negative controls fail as expected; method approved by HQ [pos 1557].
- Affected: OB09 (N9); TH12 (S-KERNEL); CL01.

**DEC38. Prior-start under-estimation: certified version** [pos 1467].
- Decider: HQ. Decision: replace "below the block start on 12 of 12" by the certified statement that the prior start's Ẑ is provably below Z on 10 of 12 designs (any scored model gives a lower bound on Z); block start 0/12, singleton 0/9. Both Sol reviewers reached the same 10/12.

**DEC39. Rulings on the chair's questions Q1–Q5** [pos 1608–1614, 1621–1624; `MEET-THM/evidence/…HQ_RULINGS…`].
- Decider: HQ (Felipe had delegated: "you have full autonomy wrt the specs of the meeting" [pos 1616]); Felipe may overrule at the final list.
- **Q1 §5.3 (RL01):** "the bridge form counts, with three conditions": (a) theorem controlling start-to-posterior distance by cross-block correlation (plus shared noise-variance term); (b) stability of the bridge as cross-block correlation grows from zero, on a correlated design family; (c) refutation of the one-shot form after an independent check. Reason: the literal one-shot reading "has been refuted for our method" (WS6(d), WS7), so the bridge is "the faithful reading". If any part lacks a route, "it comes back to me as an unmet goal. It doesn't get dropped."
- **Q2 §5.4 coverage (RL02):** read as "how far the computed credible quantities are from the exact posterior's" (posterior content + Monte Carlo error); frequentist coverage to future work (CJ01).
- **Q3 §5.4 TV/KL under masking (RL03):** "not mandatory": obligation with fallback; but paper 1 "must still prove at least one accuracy result for masked designs" (satisfied by TH04 masked-regime statement). CJ02 (FW2) future work.
- **Q4 Ĵ and cross-block proxy (RL04):** "allowed as reporting" if from existing quantities, no new random numbers, no feedback into the run.
- **Q5 stage count "continuous in ε" (RL05):** accepted as sandwich + local constancy at non-critical thresholds + continuous upper envelope; plus two conditions: real-valued parts must be continuous/Lipschitz in ε on a correlated family, and the paper must say the integer stage count can jump.
- Evidence: PC1 found T=3 between baseline counts {2,4} at ε=10⁻⁵ [pos 1621]; WS6(d)/WS7 VERIFIED WITH AMENDMENT.
- Affected: TH02 (M2), TH04 (M4), TH07 (M7), TH13 (S-IDENT), CJ01, CJ02, CJ22.

**DEC40. Item: sufficient growth rate kept theorem-side only (AMENDMENT_HQ_02 change)** [pos 1626, 1639; RL06].
- Decider: HQ.
- Decision: the second optional growth rate R′_n = 4⌈(n+p)⁶/4⌉ ("about 10¹⁷ islands at study sizes") "will be kept only as a sufficient rate inside the theorem, not as a method configuration"; the first optional rate R′ = 4⌈log₂(n+p+1)⌉ stays (ledger 05:45). All other items of `AMENDMENT_HQ_02_DEFINITIONS.md` (Ĵ, ε̂_× with companions, d added to 𝓗, read-only accumulator) approved. Affected: RL06; DF19, DF20, DF18; TH01.

**DEC41. Package approval and what goes to Felipe** [pos 1639–1650].
- Decider: HQ. Approved the package "with one change" (DEC40). Recommendations to Felipe: approve the list; scout HQ for the Song–Liang separation (CJ21, would become a ninth main theorem); Prop D (TH08) in main text; HQ readings of goals overrulable; wave 1 = M1, M3, foundations pack.

**DEC42. Long jobs as systemd units** [pos 1529–1541].
- Decider: HQ. Decision: all long Owls jobs launched with `systemd-run --user` (units under `app.slice`, outside the agent scope); rule written into Owls `POLICY.md`. Evidence: test unit survived outside every agent scope. Reason: [pos 1529] the rc 143 kills came from each agent's systemd scope.

**DEC43. LH-LOCK not relaunched** [pos 941–947]: its goal (general LH locking) "proved false" (A-REV7, RF208); added to every API agent brief "write long proofs across several files and commits, never in one giant response" [pos 947].

**DEC44. Account for study re-run: none** [pos 1107, 1296]: v3.1 changes nothing v3 computes; the 2,400 fits stand; joint summaries (pair inclusions, size distribution) cannot be computed from saved outputs (mid-run particle populations not saved) so an empirical paper section on them needs a new small run (≤20 seeds) [pos 1296].

**DEC45. T38-RECORD as statement of record** [pos 817–821, 913–919]: one statement of record `T38_STATEMENT.md` (v3 at `theory/T38-RECORD`) and a registry rebuild (431 results, 26 conflicts, LOCKABLE 48 → 55). TH290 (T38-v3).

**DEC46. Audit of the draft list size** [pos 1492]: dossier now says 24 draft entries (V1–V4, A1–A4, D1–D4, S1–S4, C1, R1–R7), not 19. See (c).

**DEC47. ABL-CONF verdicts accepted as pre-registered** [pos 1655–1669].
- Decider: HQ applied the pre-registered rule.
- Verdicts: Claim 2 (prior start under-estimates log evidence at equal budgets): LICENSED on all three designs (median −13.4/−10.8/−5.7 nats; CJ165). Claim 1 (block start cheaper at equal accuracy): INCONCLUSIVE overall (CJ164): S5 10/10 paired wins (~30% cheaper), S4 singleton start 0/10 delivered in 75 min vs block 9/10 ("holds_nondeliv"), S1 no difference. Paper can state Claim 2 as licensed and per-design costs as pre-registered results but "cannot say the block start is cheaper in general". 107 of 118 fits completed, 11 capped.

---

# (b) DEAD ENDS AND FAILED APPROACHES

Each entry: what was tried; why it failed; where (pos + branch file); what replaced it.

**B01. Literal T37 truth dominance and greedy repair.**
- Tried: T37 (CJ117) as filed 2026-10-28: finite-n truth dominance TD(d,m) implies greedy repair; the paper's Thm 3 route.
- Failed: RF101 (literal T37) / RF165 / CJ129 (TD): "REFUTED as written: false for d >= 1 on any design (Prop1-TD, V1-TDfails); false at d = 0 without positivity" (TH198 Prop1-TD, SF VERIFIED (W3-VT37R), XF VERIFIED (A-REV2)). Data: 1 of 2,394 fits favourable; local search repaired 0 [pos 178, 355, 370].
- Where: `W1-T37R/REPORT.md`, `W3-VT37R`, `A-REV2/REVIEW.md` §4.
- Replaced by: TH199 (Theorem A, refined T37(i): greedy repair holds exactly when TD′ holds, with positivity), TH201 (Theorem B (T37)), TH204 (Theorem W; PGD).

**B02. H24 and T24 with the 1/31! constant.**
- Tried: T24 terminal repair needing H24 (uniform exit) as T21 route (e) input.
- Failed: H24 false in correlated designs: CE1 (CE144) counterexample (SF VERIFIED* W2-VT24G, XF VERIFIED* A-REV1); "RETIRED (REGISTRY_v2 D): its asymptotic input (L+4)eta_n -> 0 is false in correlated designs" (CJ120, RF102, RF182). The blanket claim in CJ187 was retracted by A-REV1 / W6-FIXREV1 §9 (narrow version CE145). Exit probability ≥ 0.39 in every correlated scenario [pos 370].
- Where: `W1-T24G/REPORT.md`, `W2-VT24G`, `A-REV1/REVIEW.md` §5 (IND-T, Lemma U, CE1).
- Replaced by: TH218 (Theorem B, restated T24; polynomial constant ~1/(B+3)); T21 route TH239 (T21-e′).

**B03. Sharper T02 size cutoff.**
- Tried: m_n = s₀ + O(s₀ log n/log p) tail sharpening of T02(i) (W1-T03R).
- Failed: RF103 (T02 sharp size cutoff): REFUTED under G and R alone by CE111 (PropD-T03), duplicated columns [pos 342, 370].
- Replaced by: TH128 (T03♯) with exact BB(1,p) tail and weaker eigenvalue conditions.

**B04. Pooled Ẑ × pooled PIP is unbiased.**
- Tried: the pooled product as the island-combination estimator.
- Failed: RF226 (pooled Z-hat x pooled PIP unbiased): REFUTED by TH298 (Prop2(c); pooled x pooled PIP bias; −3/4 Cov), SF reproduced to 1e-58, XF VERIFIED (A-REV4, Owls 50-digit reproduction) [pos 550]; CE182.
- Replaced by: island-by-island form TH297 (Prop2 (a,b,d,e)); later Ẑ-weighted PIP.

**B05. Draft §5.3 weight stability under cross-block dependence (the draft's mechanism).**
- Tried: F-DRAFT/O-WSTAB/A-DRAFT attempt at the draft's Theorem 1.
- Failed: CJ251 (Section 5.3 Theorem 1; draft weight stability): "mechanism false for v3 tables (RF256)"; the discrepancy is driven by per-block σ² estimation ("dilution"), not cross-block correlation [pos 616]; F-DRAFT W2 ERROR with explicit feasible counterexample (A-REV4, RF265 (FD-NM)).
- Where: `F-DRAFT/`, `O-WSTAB/`, `A-REV4/REVIEW.md` §3.
- Replaced by: TH362 (Theorem W (ORTH) under H-ORTH), TH350 (Theorem WS3; exact BO structure of d), and the final bridge-form package TH02 (M2); the literal one-shot form is refuted for the shipped method (OWS-WS6d, OWS-WS7: VERIFIED WITH AMENDMENT).

**B06. "Tempering is needed" (the spine claim).**
- Tried: use the bridge's necessity as the paper's conceptual spine; W7-SEP set out to prove start-only discovery fails while v3 succeeds.
- Failed: RF104 / RF264: "REFUTED on LH by W7-SEP Prop GU (candidate-based); replaced by 'moving off the start is needed'". Start-only plus local search does reach S₀ on LH [pos 763].
- Where: `W7-SEP/`, `A-REV9/` ("restricted verdicts"), `E-SPINE/`, PR #1.
- Replaced by: TH388 (Prop GU; greedy universality), TH380/TH382 (SEP A/B); final: TH06 (M6; Theorem SEP + Lemma KL; start-only obstruction at LH threshold p²n, one-shot correction needs polynomially many draws). **Honest scope:** TH401 (Prop OB) and API-POS: masking on LH is a property of the start; no published BVS example has MCMC provably slow while SMC succeeds (LIT-MCMC open).

**B07. General LH locking and LH-LOCK.**
- Tried: prove BG3's premises on LH in general (LH-LOCK, Fable, CW).
- Failed: RF208 (OBG-LH-lock-general): "ERROR (A-REV7): C2 fails e.g. g=4, rho=0.85, psi=0.5; reproduced by Claude (API-VSTAB)" (explicit swap improves population fit by .004789313640313); the agent also died on the 64K output limit [pos 939–945].
- Where: `A-REV7/REVIEW.md` §5; `O-BGIBBS/`; ledger 21:55.
- Replaced by: TH261 (OBG-LH-lock; conditional fixed-p implication), TH276 (fixed-p component corollary on (CERT), API-VSTAB), TH275 (B2LH-subfamily(A7)); TH05.b2LH labelled variant.

**B08. SHARE-M(b) and Prop GU as a standalone no-LS0 route.**
- RF203 (SHARE-M(b)): "ERROR (A-REV3, retained A-REV6): quadratic expansion …"; TH253 (SHARE-M(a)) survives (SF VERIFIED W5-B2ENV 20,000 instances; XF VERIFIED A-REV3). Prop GU "GAP as standalone no-LS0 growing-p theorem" (TH388, A-REV7). [pos 919].

**B09. Common-σ² start (as a cure for dilution).** See DEC11. Tried: F-DRAFT suggestion [pos 616], O-MIX arm C, F-SIGMA theory. Failed: floods the start; TH176 (Prop S; ranking ceiling for every common σ²), TH186–TH188. Replaced by: block start with its σ² coupling decomposition TH03 (M3).

**B10. Residualised/backfit start.** See DEC12. CJ162, CJ163: "unproven candidate; no theorem, no SMC evidence"; "no exact backfit sampler with a known normaliser exists".

**B11. Mixture of block starts (B-merge).** O-MIX: TH181 (Theorem B3; (B-merge) on LH exact Gram) route (a) without LS0; SYNTHESIS §6: "does nothing for dilution"; not included in v3.1 (reason not recorded as a decision in the thread: **UNCERTAIN**; the method meeting kept the block start, MD01).

**B12. Weak-signal explanation of masking.** RF136 (WeakSignal; weak-signal masking conjecture): ERROR (W3-VEXP row 27, W3-PXN Prop W); RF142; replaced by dilution masking TH158 (PXN-W) and TH171–TH174 (O-DILUTE: TH172 Cor E1 V+C−log A identity). [pos 594, 763].

**B13. API-POS claim (paraphrase): rapid-mixing theorems apply to the LH family** (HQ at [pos 1009]: "API-POS said the rapid-mixing theorems apply to the linked-hub family. LIT-MCMC finds they don't, at least for our own posterior.") API-POS [pos 978] vs LIT-MCMC [pos 1009]: TH401 (Prop OB): hypotheses fail for our target in 12 of 12 study-like data sets by a factor ≥ p^0.87; (ii)–(iii) PROOF SKETCH. TH404 (Statement R3 MIX-POS) positions against YWJ/ZYVR. Net: the masked-start theorems repair a problem created by the start; they do not show the method beats MCMC.

**B14. Lemma 0(b) "every unrepaired centre is a posterior miss" and the "233 of 234" sample.** W3-VT37R reported 233 of 234 sampled centres with F(S₀) > F(centre) not repaired; S-ELS found all 541 unrepaired centres forced by Lemma 0 (CJ176, CJ179); logical claim false in general (CJ320 OPEN), true on the study data. TH200 (Prop F) partitions failures I/II/III. Replaced by CJ222/CJ223 data facts.

**B15. ABL-START cost comparison (A vs B).** Failed: pre-registered rule vacuous because arm C's poor evidence made every design inconclusive; arm B ran >4.6 h on S4 (killed at 23:31) [pos 1280, 1286, 1449]. Where: `MEET-v31/ITEM1_ABL_START.md`, `evidence/item1_scripts/HQ_NOTE_v2.md`. Replaced by: ABL-CONF with a declared 75-minute cap and non-delivery as a cost failure (CJ164, CJ165).

**B16. Song–Liang analytic separation (K97).** Tried repeatedly (THM-SYNTH C1, theorem-meeting Seats). Failed: "The meeting couldn't get a sound proof that their split-and-merge loses true predictors under correlation" [pos 1650]; PC1 wave marks item as not repaired. Now CJ21 (FW21; K97) in FUTURE_WORK; numerical counterexample LIT-PAR G4 (CL23) cited as labelled evidence; HQ recommends a scout HQ; also NM versions: CE208 (Prop M; ADRAFT-PropM; Prop NM-A) is the surviving naive-merge counterexample.

**B17. Literal "stage count continuous in ε".** RL05; integer step function; PC1 T=3 between {2,4} at ε=10⁻⁵ [pos 1621]. Replaced by sandwich + local constancy + continuous envelope.

**B18. Operational dead ends.** First routine runs billing the plan (DEC03); max-effort Fable relaunches; O-LS0 at ~34 cores; A-REV1/2 cancelled by T3 restarts; guard dying with T3; setsid-detached jobs killed by session teardown (DEC42); LH-LOCK 64K output; API CLI refused (DEC14); first meeting-thread launch with a remote-only branch [pos 1597]; N9 report overwritten by HQ [pos 1590].

**B19. Theorem-selection dead ends.** Draft list with 24 entries was reduced to 8 main + 12 supplement; 27 candidates to FUTURE_WORK (each with a reason), 6 drops DR01–DR06 (K12, K34, K66, K67, K91, K98); S-STGI card dissolved (TH21; dissents DS01–DS06).

---

# (c) REVERSALS AND CORRECTIONS OF HQ CLAIMS

Summary: the table lists claims made or relayed by HQ (some originate in earlier documents or in Felipe's own framing, as noted in the row) that were later corrected, with positions of the claim and the correction.

| # | HQ claim | Correction | Where |
|---|---|---|---|
| R01 | Wave 1 routines would spend the credits [pos 238, 243] | Routines bill the plan; only `claude --cloud` bills the credits | [pos 301, 305, 333] |
| R02 | Initial plan: `claude -p` with API key bills API credits [pos 59] | The promotional credit covers API and Agent SDK but not the Claude Code CLI | [pos 874–894] |
| R03 | "Tempering is needed" / "the bridge is needed" (spine) | "Moving off the start is needed"; RF104, RF264 | [pos 763, 796, 800] |
| R04 | "So T37 as written proves the wrong mechanism." [pos 178], then refinement | Original T37 false even at d=0; positivity added | [pos 178 vs 370] |
| R05 | H24 as T21 route (e) input | H24 false in correlated designs; Theorem B | [pos 327, 342] |
| R06 | T03 thresholds near 1.2·10⁵ (W1) | Thresholds start near n ≈ 2·10⁶ (A-REV2, W2-VT03R) | [pos 370, 568] |
| R07 | "none has had a review from a different model family yet" [pos 550], then A-REV1/2: "no core theorem has been overturned by the second model family" [pos 570] | Astra later found errors in about ten Claude results ("All but three now have repairs, but no repair has been re-checked by Astra yet") | [pos 550, 570, 796] |
| R08 | W8-SYNTH: O-LS0 data "has not landed" | Landed 20:24 (`theory/O-LS0` @ 02348e2) and passes | [pos 774, 793, 796] |
| R09 | "beta-min fails by about 100×" (THEORY_PRIORITIES) | At least 43×; RF105, RF129; also "favourable from n ≈ …" figure dropped | [pos 796; BRIEF.md] |
| R10 | Felipe: simulations unbeaten on exact recovery | At c=1 SMC-BVS 559/600 and 560/600 vs SuSiE 585/582, SSL 569/582, horseshoe 574/575; at c=0.5 best (370/600, 340/600) — **the c=1 accuracy correction** | [pos 931 vs 933] |
| R11 | O-LS0 "xhigh, ≤40 cores" | Cancelled; relaunched ≤2 cores | [pos 439–467] |
| R12 | LH-LOCK as a priority task | Goal refuted by A-REV7 | [pos 817 vs 919, 941] |
| R13 | API-POS: rapid-mixing theorems apply to LH | LIT-MCMC: they do not (hypotheses fail 12/12, factor ≥ p^0.87) — the API-POS rapid-mixing claim qualified by LIT-MCMC | [pos 978 vs 1009] |
| R14 | METH-AUDIT headline: bit-for-bit "3 of 3" designs | Only 1 of 3 had been run; re-ran two on Owls | [pos 1107 correction] → 3 of 3 [pos 1251] |
| R15 | HQ intuitive worry "We parallelise over particles, not over variables" | Felipe: "We are not trying no parallelize over variables"; worry withdrawn; per-move depth in p kept as stated cost | [pos 1111, 1113, 1117] |
| R16 | Felipe: "It runs on composite likelihood" [pos 1132] | Only the start π₀ is composite; target and reported numbers exact | [pos 1136] |
| R17 | Ablation rule: inconclusive when evidences differ by >1 nat | Rule vacuous; Outcome 2 "keep, no speed claim"; rule v2 enforces ≥9 conclusive designs | [pos 1280, 1467] |
| R18 | Prior start below block start "on 12 of 12" | Certified: Ẑ < Z on 10 of 12 (A 0/12, B 0/9) | [pos 1467] |
| R19 | MPM threshold ⅓ (one Fable seat) | ½ (proof check refuted ⅓); "top-store MPM threshold is ½, not ⅓" — **MPM ⅓ → ½** | [pos 1251, 1286] |
| R20 | "Ẑ can only fail downward" | Literally false | [pos 1251, 1492] |
| R21 | Limitation "no useful upper bound on Z" listed as inherent | Astra's analytic bound Z ≤ C_n(2b₀+yᵀy/(n+1))^{−ν} (OB17) showed it is not inherent; then Sol: "not proved"; then HQ [pos 1512]: "What's actually proved is narrower than the documents said. The properties behind the 95% lower bound don't imply a two-sided relative-error bound. That isn't the same as 'no upper bound on Z exists'." — **the "no upper bound on Z" narrowing**. LIM05, LIM06 | [pos 1286, 1480, 1512] |
| R22 | "PIP Monte Carlo SD ≤ 0.01" | Not a guarantee (resampling → dependence) | [pos 1302 vs 1480] |
| R23 | Backfit start: "The argument that the backfit start could gain at most 6 of 2,400 fits doesn't follow." [pos 1480] | Does not follow (Sol 1) | [pos 1009 vs 1480] |
| R24 | "Θ(p²) work" | Only when n = O(p) | [pos 1480] |
| R25 | Local-search scan-size bound | Wrong when cap K > p/2 | [pos 1480] |
| R26 | Draft theorem list has 19 items (THM-SYNTH summary) | 24 entries (V1–V4, A1–A4, D1–D4, S1–S4, C1, R1–R7) — **the 19 → 24 draft-list count** | [pos 1303, 1348, 1492] |
| R27 | Proposal §5.3 weight stability "has no theorem in the draft list"/"is empty" | "§5.3 isn't empty; O-WSTAB has results under an orthogonal idealisation, tiered v2 by THM-SYNTH" — **"§5.3 is empty" corrected** | [pos 1348 vs 1441, 1449] |
| R28 | Owls guard killed the ablation (923% over 8 cores) | "probably" T3 restarts; true cause: agent-scope teardown | [pos 1251 → 1263 → 1529] |
| R29 | N9 sub-claims: 7 vs 8 | HQ's own write-up counted 7; the agent's report counts 8 | [pos 1550 vs 1593] |
| R30 | Q1(b) "stage count continuous in ε" | Accepted only as sandwich + local constancy + continuous envelope | [pos 1624] |
| R31 | Second growth rate as method configuration | Theorem-side only (10¹⁷ islands) | [pos 1639] |
| R32 | Joint summaries available for the study | Not computable from saved outputs | [pos 1296] |
| R33 | Method meeting wording, corrected at [pos 1251]: "Memory: what's inherent is access to every predictor, not a private copy of XᵀX per worker." | What is inherent is access to every predictor (LIM02) | [pos 1251] |
| R34 | HQ promised to ask before each escalation | Withdrawn after Felipe's comment | [pos 162] |

---

# (d) REVIEWER FINDINGS THE THREAD RELIED ON

All cross-family reviewers are OpenAI models: **Astra** = GPT-6 Astra (`gpt-6-astra`), **Sol** = GPT-6.1 Sol (`gpt-6.1-sol`), both on Codex; billing: the OpenAI account, not Claude or API. Verdict-word counts below are rough tallies of table rows in each review file (`branch_snapshots/A-REVn/REVIEW.md`), meant as scale indicators, not official counts. "Registry" = `ID_REGISTRY_B`.

## D.1 Astra A-REV1–9 (2026-11-02)

| Review | Scope | Headline verdict (from the file) | Table-row tally (E/G/V) | Main IDs affected |
|---|---|---|---|---|
| **A-REV1** [pos 552–557] | Theorem B (restated T24), T38(b)-R, D2, E3, Lemma S, Prop U, IND-T, CE1 | "The finite Gibbs-path bound survives independent review after the F′ repair. The supplied package is not ready for an unqualified verification: Proposition U, Lemma S's attainment sentence, E3(ii), and Lemma U's printed limit contain errors"; corrected D2 constant right | 4 / 5 / 23 | TH218 (Theorem B), TH219 (B′), TH242 (D2), TH240 (E3′), TH241 (T38b-R), RF102, RF182 |
| **A-REV2** [pos 565–568] | T03♯, refined T37 (Theorem A), EXP′ | "Overall package verdict: GAP" with T03♯ conditional VERIFIED; constants 0.52 → 0.51; exact-ties edge case in TD′; missing hypothesis in a Lemma U bound; W3-VT37R repair R2 wrong (ignored inferior local maxima) | 8 / 2 / 19 | TH128, TH199, TH136, TH201, RF101, registry conflict C1 |
| **A-REV3** [pos 676, later] | W3-PXN (p≫n joint family), W4-SHARE, Prop M | "Overall W3-PXN: GAP as written. Overall W4-SHARE: GAP, with ERROR findings in the score-expansion and assembly claims." W3 Lemma B etc. VERIFIED; M(a) VERIFIED; M(b) ERROR | 3 / 6 / 14 | TH153, TH154, TH253, RF203; the p≫n GAP carried to A-REV5/6/8 |
| **A-REV4** | W2-T26, W2-BOOK/Lemma RO, F-DRAFT, A-DRAFT §2 | "Overall: GAP." F-DRAFT has "two explicit false formulas"; explicit counterexample for W2; pooled bias VERIFIED (Owls 50-digit) | 3 / 5 / 11 | TH295, TH298, RF226, RF265, CE208 |
| **A-REV5** [pos 807, 915–919] | Re-review of W6-FIXREV1/2 repairs of A-REV1/2 | "The principal repairs are mathematically sound within their stated restrictions. The complete repaired package is not VERIFIED: it retains ERRORs in ancillary assertions and GAPs in conditioning, cost, random-design extensions, and downstream propagation." | 17 / 11 / 44 | Downstream E3, R2, ESS, PXN; T38's c=2 iid-budget growth condition; W2-T26's exact-branch example false |
| **A-REV6** | Re-review of repairs to A-REV3/A-REV4 findings; candidate repairs; does W7-PART close p≫n? | "Overall verdict: GAP, with the original ERROR findings pre[served]"; "Only the restricted recovery premise; not the full result." (W7-PART B) | 16 / 24 / 22 | TH162, TH163, TH253, RF203, RF265 |
| **A-REV7** [pos 919] | No-LS0 masked routes (BG3, B2-LH, D2-LH, GU, F-SHARE F2) | "a no-LS0 masked theorem is available on an explicit exact-Gram LH subfamily": B2-LH VERIFIED conditional on STAB-LH; Astra-authored analytic STAB certificate; ERROR: unconditional LH swap locking; ERROR: "DOM is void when c=1" | 0 / 2 / 6 | TH258, TH272, TH269, TH261, RF208, TH388, TH275 |
| **A-REV8** | LS0 masked route (XV-MASKED-LS0) | "Overall verdict on the conditional consistency conclusion of Thm 5(b1): VERIFIED. It is a theorem about v3 plus LS0"; p≫n interface W_Lat flagged | 2 / 4 / 11 | TH290, TH160, TH153, TH169 |
| **A-REV9** | Certificates, masked PIPs/evidence variance, dilution, separation, partition, stage/weight results (+O-SWAP, W7-SEC) | restricted affirmative verdict on weight stability; certificate card repaired (R1, R2); O-SWAP predictions GAP; Cor B GAP; Sol helpers MASKED_PW2_CHECK, DILUTE_STAGES_CHECK | 4 / 8 / 20 | TH331, TH329, TH332, TH333, TH336–TH339, TH316–TH319, TH171–TH174, TH364–TH367, TH380–TH382, TH162–TH163, TH362 |

HQ's own summary of the A-REV1–A-REV9 contribution [pos 1238]: Astra caught errors after Claude passed them; registry item C1 (W3-VT37R repair stated as proved, Astra A-REV2 showed it wrong); counterexample to general LH locking (A-REV7, RF208); Prop M's sharing claim and the naive-merge proposition (A-REV3/4/6); GUARD wording (A-REV8); a data paragraph in the Bayes-rules proposition (A-REV4); parts of the per-fit certificates. Weaknesses: "Many of its GAP verdicts concern conventions or wording"; one self-review (ADRAFT-ThmA written and checked only by Astra).

## D.2 Sol (GPT-6.1) reviewers

- **Sol 1 (proof check of MEET-v31 final documents) and Sol 2 (audit)** [pos 1451–1480]: Sol 1 checked 60 claims: 45 hold (19 with corrections), 7 false, 6 gaps, 2 uncheckable; examples: backfit "6 of 2,400" does not follow; "PIP Monte Carlo SD ≤ 0.01" not a guarantee (resampling); "no useful upper bound on Z" not proved; local-search scan bound wrong when K>p/2; "Θ(p²) work" holds only when n=O(p). Sol 2: 13 findings, 4 decision-level (N9 gate; fallback plans silently dropping binding goals; C6 per-particle-streams trigger narrowing; item-1 rule script bug). Both reached the same 10/12 prior-start result. HQ dispositions applied in `AMENDMENT_HQ_01` (73 findings: 45 edits, 28 none). Original reports sat on Owls at `/home/fb31/hq_reviews/SOL1_proof_check.md`, `SOL2_audit.md`, `HQ_DISPOSITIONS.md`; the amendment is `MEET-v31/AMENDMENT_HQ_01.md` in the snapshots.
- **Theorem-meeting check waves** (`MEET-THM/evidence/W1_PC1, W1_PC2, W2_PC1, W2_PC2, CHK_INHERITED`): PC1 = Sol 6.1 (Codex) checking claims of Seats A, B, D; PC2 = Opus 5.5 (Claude Work) checking Seat C (Astra) and R0_E.
  - W1_PC1 (Sol): COUNTEREXAMPLE 11, NEEDS-HYPOTHESIS 25, AMBIGUOUS 12, TRUE-AS-WRITTEN 53; route: GAP 17, IMPLAUSIBLE 2, PLAUSIBLE 82; design DESIGN-FAILS 3.
  - W1_PC2 (Opus): 56 claim clauses: 54 TRUE-AS-WRITTEN, 2 AMBIGUOUS, 3 route GAPs.
  - W2_PC1 (Sol, 91 clause-review rows): TRUE-AS-WRITTEN 70, COUNTEREXAMPLE 9, NEEDS-HYPOTHESIS 8, AMBIGUOUS 4; GAP 23; DESIGN-FAILS 1; repaired 57, repaired differently 16, new 15, not repaired 3.
  - W2_PC2 (Opus): 29 claim rows all TRUE-AS-WRITTEN.
  - HQ's summary [pos 1650]: "Two rounds of proof checks by a different model family found 20 counterexamples in draft statements, and all were repaired or removed" (W1_PC1 11 + W2_PC1 9 = 20).
  - CHK_INHERITED (Sol): OWS-WS3 and OWS-WS4 VERIFIED (line by line); OWS-WS6(d), OWS-WS7, N9-KERNEL §§0–3 VERIFIED WITH AMENDMENT [pos 1626].
- **Auditor at close** (`MEET-THM/CLOSE_AUDIT.md`, Sol 6.1): "PASS WITH CORRECTIONS (#4–#10); the chair applied all of them": S-STGI dissolution not propagated through the registry; three placement dissents omitted from the minutes; N14(c) mislabeled as extra-search nesting in several charters. All 108 K-IDs have destinations; no status upgraded.

## D.3 PC1/PC2 of the method meeting (Opus 5.5, CW, 2026-11-03)

- `MEET-v31/evidence/2026-11-03_PC1_proof_check.md`: batched proof check; Claim 1 (analytic upper bound on Z, Seat C): PROVED (holds for m(S) as written); also the ½ threshold (⅓ refuted), counterexample to one claimed property, and others (HQ summary [pos 1286]: "confirmed three of Astra's claims, refuted one Fable seat's threshold (⅓ is wrong, it's ½), and found a counterexample to one claimed property").
- `…PC2_certificate_card.md`: certificate card; Lemma M and Theorem C4 by exact enumeration at p ≤ 12; joint output-event bound P(𝒪 ∩ {0.05Ẑ > Z}) ≤ 0.05·P(SMC ∩ 𝒜). Affected: TH04, OB06, OB07, OB13, OB17.

## D.4 F-REFEREE (2026-11-02)

`F-REFEREE/REFEREE_REPORT.md`, `RESPONSE_PLAN.md`: hostile JRSS-B referee report; "Recommendation: major revision. The theory section is unusually candid, internally consistent…". Eight major points: M1 asymptotics vs n=200 (thresholds ≈ 2·10⁶); M2 main theorem needs LS0 (not run in simulations); M3 masked regime without LS0 rests on unproved particle-level hypotheses; M4 favourable regime makes the sampler unnecessary — what does the bridge buy?; M5 2^B and vacuous rates; M6 novelty and missing comparison with rapid-mixing; M7 evidence and PIPs mean nothing in the masked regime; M8 verification status. Tally at the W8-SYNTH cut: "0 are done, 6 in progress, 2 open" [pos 796]; registry rows CJ303–CJ306 (F-REFEREE M1–M4). The one change that most raises the tier: a theorem for the algorithm as run, with growing-n simulations (LH-SCALE, never run).

## D.5 Other reviewers/verifiers relied on

- Same-family verifiers (Opus): W2-VT24G, W2-VT03R, W3-VT37R, W3-VT38E, W3-VEXP, W5-VMASK, W5-VPGD, W5-LOCKBOOK, W7-SEC (re-count of T32(i)), O-VCERT (0 violations in 476,160 exhaustive pairs for LM204 (Lemma M); B&B = brute force 80/80, 285,712 boxes on 48 designs for TH329), API-VSTAB (0 violations in 1,500 configurations), N9, registrar index (166 cited IDs; 51 author-only, 9 same-family only, 4 Astra only [pos 1492]).
- Lean (L-LEAN) fidelity: Fable + Astra "GREEN (statement fidelity only)" for TH418, TH420, TH422, TH423; library of 101 results, 0 `sorry` (25 files; `sorry` only in 4 frozen/fidelity copies [pos 1492]).
- Registry (S-REGISTRY / T38-RECORD): 431 results, 26 conflicts, LOCKABLE 48 → 55 [pos 919]; HQ's close: 37 conflicts logged between draft list and later sources [pos 1492].
- Close audit and meeting minutes: `MEET-THM/MINUTES.md`; dissents DS01–DS06.

---

# (e) TRACE INDEX

Trace file for a position: `traces_01` = pos 0–208, `traces_02` = 209–550, `traces_03` = 551–807, `traces_04` = 808–957, `traces_05` = 958–1107, `traces_06` = 1108–1238, `traces_07` = 1239–1361, `traces_08` = 1362–1676 (all under `transcript/traces/`). Within each file, items are headed `### [pos N] kind`. "Brief" = a delegate/launch/tool-input item containing the task brief; "reasoning" = the HQ's reasoning item at that position; "result" = the position where the HQ reads and interprets the output. Positions below are trace-item positions (they coincide with message positions in the transcript).

| Result / task ID | Brief / launch (trace pos) | Reasoning at decision / result interpretation (trace pos) |
|---|---|---|
| Credit plan, routines, smoke test | [pos 56, 70, 72, 100–117] RemoteTrigger | [pos 54, 66, 74, 89, 153] |
| W1-* (TH198, TH199, TH201, TH218, TH128, TH136, TH241, TH242; RF101, RF102, RF103) | task files [pos 201]; routines [pos 217–231] | plan [pos 185, 207, 213]; results [pos 325–326, 348–350 (W1 reports read)], billing [pos 299–305, 333–335] |
| Waves 2–4 | [pos 328–330, 334, 352–353, 364] (task specs, launcher, ledger) | verdict reading [pos 359–362]; wave 3 plan [pos 350] |
| LS0 (DEC09), O-LS0, O-LS0-WRAP, S-ELS (CJ222, CJ223) | O-LS0 [pos 399, 466]; WRAP [pos 759–760]; S-ELS [pos 715] | design [pos 373–383]; advice [pos 513–514]; adoption [pos 770–774, 790–796]; ledger entry [pos 772] |
| SR audit (CJ128, LM191) | — (HQ did it) | [pos 517–541]; write-up [pos 542] |
| F-SHARE, F-REFINE, F-PXN | [pos 393–397, 460–463] | [pos 429–439] (overload), [pos 505–510] (F-REFINE results) |
| Owls overload, guard, steward (DEC07) | steward [pos 458–459]; cron [pos 479]; systemd [pos 605] | [pos 429–447, 464, 472–477, 597–603] |
| A-REV1, A-REV2 (TH218, TH219, TH240, TH128, TH199, TH136) | [pos 401–406, 417–418, 468–471] | [pos 409–423] (restart cancellations), [pos 553–557], [pos 565–568]; fix tasks [pos 558, 569] |
| F-DRAFT / O-WSTAB / A-DRAFT (CJ251, TH362, TH350, CE208) | [pos 489–494] | [pos 483–486], [pos 614–616] |
| CP window: O-CERT (TH329, TH331), O-SWAP (TH336–339), O-DILUTE (TH171–174), O-BGIBBS (TH258), S-REGISTRY, S-PAPER | [pos 575–583, 588]; laptop [pos 646–664] | plan [pos 573]; laptop move [pos 607–644]; result of O-CERT [pos 701–706] |
| Final CP windows (O-PW2 TH316–319, O-MIX TH181, F-MASKPIP TH300–302, A-REV3, A-REV4) | [pos 673–677]; steer to all 12 [pos 684–695] | [pos 669–682], [pos 698–706] |
| Wave 7 + L-LEAN + S-ELS; F-REFEREE, F-SIGMA, O-STAGES, O-VCERT (TH186–188, TH364–367, TH332–333) | [pos 711, 714–715, 726–729] | gap analysis [pos 709, 712]; plan [pos 720–724]; status [pos 737–763] |
| W8-SYNTH (SYNTHESIS, BRIEF) | [pos 756] | [pos 757, 762, 790–796] |
| E-SPINE, PR #1 (RF104, RF264, TH388) | [pos 804] | [pos 799], [pos 846–850] |
| A-REV5–9 | [pos 801–803, 829–830] | [pos 814, 827, 914–919] |
| T38-RECORD (TH290), LH-LOCK (RF208) | [pos 818–820] | [pos 913–919], failure [pos 939–947] |
| API credit, launcher | key card [pos 859, 870]; launcher [pos 891] | [pos 823, 857–889] |
| API wave (TH161, TH334, TH275/276, TH308–311, TH370–372, TH402–404) | task specs [pos 906–911], VSTAB [pos 918] | allocation [pos 902–907]; results [pos 967–978]; resumes [pos 973–977] |
| Maturity assessment, estimate, airtight | — | [pos 928], [pos 932], [pos 936] |
| Control over speed; phases | memory save [pos 952] | [pos 950], [pos 956] |
| Literature phase LIT-* (TH401, RF130, CJ213) | [pos 986], [pos 1036] | [pos 981, 984], results [pos 995–1009], LIT-PAR [pos 1031–1038, 1070–1072] |
| Reframing (DEC21), Song–Liang | memory [pos 1026, 1033, 1042, 1057] | [pos 1025], [pos 1031], [pos 1041], [pos 1056] |
| METH-AUDIT, THM-INV, THM-SYNTH (v3.1 decision, TH394, TH397, TH398) | specs [pos 1066, 1102] | [pos 1062–1071], [pos 1085–1107] |
| Intuitive critique, selection rule, extraction matrix | — | [pos 1110], [pos 1114], [pos 1133], [pos 1139], [pos 1145–1152], [pos 1156–1161] |
| Method meeting (MD01–MD13, DS) | dossier [pos 1182–1185]; thread launch [pos 1197]; amendment 01 [pos 1220–1224] | design [pos 1165–1180]; progress [pos 1242–1251], [pos 1259–1263], [pos 1270–1286] |
| Parameter audit (DF25), size of change | — | [pos 1293–1295], [pos 1299–1301] |
| Theorem-meeting design, count, inheritance | — | [pos 1313–1316], [pos 1319–1320], [pos 1327–1339], [pos 1342–1348], [pos 1356], [pos 1360] |
| Fresh eyes (Round 0) | project creation [pos 1395–1396]; delegate/launch [pos 1401–1406]; packet [pos 1386–1394] | [pos 1364–1370, 1380–1384, 1397–1403, 1407] |
| Sol trial; dispositions; AMENDMENT_HQ_01 | [pos 1410–1413], [pos 1476–1477] | [pos 1407], audit reading [pos 1453–1456], [pos 1471–1475], [pos 1495–1511] |
| ABL-START / ABL-CONF (CJ164–CJ166) | spec [pos 1184, 1429]; delegate [pos 1431–1432]; schedule [pos 1485] | [pos 1419–1427], [pos 1483–1486], kill diagnosis [pos 1519–1541], verdict [pos 1653–1669] |
| N9 (OB09, TH12) | [pos 1457–1458], re-seen [pos 1514] | [pos 1453–1454], [pos 1516–1557], [pos 1586–1593] |
| Registrar index | [pos 1446–1447] | [pos 1488–1492] |
| Theorem-meeting launch and failure | chair brief [pos 1573]; launch [pos 1576], [pos 1600] | [pos 1566–1572], [pos 1577–1584], [pos 1595–1606] |
| Rulings Q1–Q4 (RL01–RL04) | send [pos 1612] | [pos 1609–1613] |
| Ruling Q5 (RL05) | send [pos 1623] | [pos 1622] |
| Close, approval, AMENDMENT_HQ_02 (RL06) | amendment commands [pos 1640] | [pos 1627–1639], [pos 1641–1650] |
| Final wake-up, ABL-CONF verdict | — | [pos 1653–1670] |
