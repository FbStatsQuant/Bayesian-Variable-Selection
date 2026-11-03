# Felipe's standing rules (binding for HQ and every thread)

Collected 2026-11-02 from the New Campaign charter, DECISIONS D1–D71, the GH handoff gap list and the HQ memory. The decision numbers (Dxx) refer to `Docs/HQ/DECISIONS.md`. Where an older rule was superseded, only the current one is written here.

## 1. Order, no clutter
- **One dated area per campaign**, with the same subfolder names in every location (local/repo, data store, NOTS home, NOTS scratch): `inputs/`, `manifests/`, `results/<run_id>/`, `logs/<run_id>/`.
- **Few, well-named reports.** No process files at the repo root. No scratch files left in the tree; work notes live in the campaign's own folder.
- **HQ alone owns** `STATUS.md`, `DECISIONS.md` and the README/layout. Threads report to HQ; they do not message each other. Anything for NOTS goes through HQ to OPS as a job bundle (folder + `JOB.md`: command, inputs, expected outputs, memory and time requests, acceptance check).
- **Settle every finished thread or delegate** as soon as its output is saved.
- **Old attempts are out of scope** (D6); only the shipped method matters.
- **No crawling.** Agents read only the paths their brief names. No scanning of R libraries, build caches, `.git`, old experiment folders, or whole disks (charter §2.5).
- **No arbitrary constants.** Every setting is a function of n, p or a stated principle; show its values at the study sizes.

## 2. NOTS storage (10 GB home quota, shared with Felipe's other work)
- **Campaign home footprint ≤ 0.5 GiB** (code, manifests, small inputs); **total home < 9.6 GiB** (D7). Every submission is preceded by the disk guard, and a run that would cross the ceiling is refused. D40's 9.70 GiB is a last resort only.
- **Bulky transient outputs go only to `/scratch/fb31/<Campaign>/`.** Download, sha256-verify, then delete. Scratch is purged, so never keep the only copy there.
- **No hefty data on NOTS**, including `/projects/ml75` (100 GB shared group quota).
- **Continuous clean-up:** a run is done only when its outputs are downloaded, verified and removed from NOTS and its temporaries pruned. Felipe must never have to clean NOTS himself.
- **D31 storage authority (Felipe, 2026-10-30):** HQ owns every NOTS storage decision; Felipe is not asked. To free space or remove heavy data:
  1. download it to the archive store;
  2. sha256-verify the copy;
  3. have Sol review the deletion list;
  4. erase it on NOTS;
  5. log it in the campaign `ops/CLEANUP_LOG.md`.
  - Never touch program installs in use, credentials, config, or open files.
  - Mention what was archived in the next milestone report.
- **Deletion only through tooling** (`verified_delete.sh`, copy → verify → delete), never ad-hoc commands. Never run two copy or move commands on one tree at once.
- **Benchmark freeze:** do not delete, move or chmod anything under `/projects/ml75/fb31/BVS/bench20261019/` or `/home/fb31/projects/BVS/Benchmarks/` until `RELOCATION_OK.md` exists. Reading and copying are fine.
- **Running NOTS jobs are never killed on a pause**; let them finish. Cancel jobs only by explicit ID, and only our own. Never touch other users' files.

## 3. SSH discipline
- **Only the OPS thread opens SSH to NOTS**, with batched commands, through the configured alias `ssh nots`. At most **two** concurrent connections (D76):
  - one bulk lane for long transfers;
  - one control lane for short commands (each ≤ 5 min, serialised).

  Otherwise it is one connection at a time.
  - The alias is pinned to the login node that hosts Felipe's live T3 server (loginx2 since 2026-10-28). Never connect to another login node directly.
  - Never touch `~/.claude/remote` or `.t3-recovery` on NOTS.
- **No connection bursts.** NOTS blocks a source after bursts (2026-10-22: all login nodes for ~20 min). After a timeout or reset, back off 15 minutes. Never hold a session more than about 1 hour.
  - OPS routes all ssh through the locking shim `ops/scaffold/sshlock` (global lock + stall bound).
- **Owls is a shared lab machine:** "don't monopolise".
  - Caps: ≤ 16 cores, ≤ 24 GB RAM, nice 19. Pause if load > 40 or < 30 GB free.
  - Never touch Felipe's own VS Code R session.
  - Bulk data goes only to the git-ignored `/home/fb31/BVS_GH/_data/`; check sizes first (the Owls quota is shared).
- **Credentials:** never repeat, store or put a password in a prompt or file. NOTS uses key auth.

## 4. Approval-safe tooling (D37/D38)
A Bash permission prompt silently blocks an unattended agent, so every brief carries these rules:
- Use the Edit/Write tools for edits.
- Absolute paths.
- No `cd … &&`.
- No `rm` globs.
- No heredoc edits in Bash.
- One simple command per call.
- Scripts are written to a file and run by absolute path.

## 5. Model hierarchy and reviews (charter §4, Felipe 2026-10-29)

| Role | Models | Use |
|---|---|---|
| Managers | Opus 5.5 (high) | Plan, delegate, integrate, decide routine questions |
| Consultants (expensive; scoped hard questions, with HQ's agreement) | Fable 5.1, Astra | Fable: delicate judgment, leads theorem-statement refinement. Astra: adversarial checks, adjudication, theory |
| Default reviewer | Sol 6.1 (gpt-6.1-sol, high) | Independent review; worker only with a tight brief |
| Workers | Sonnet 5.5, Terra 6.1, Haiku 5.5, Luna | Bulk of the volume; Haiku/Luna clerical |

- **Spawning.** Claude workers via the native Agent tool; OpenAI workers or reviewers via `delegate_task`. Fable runs on the Claude Work account; Claude workers run on Claude Personal (confirm at bootstrap).
- **Every brief** names exact paths, inputs, the expected output and an acceptance check.
- **Workers never verify their own work.**
- **Reviews on everything that matters:** code, specs, conformance verdicts, cleanup deletion lists, job bundles before submission, scoring outputs, result tables.
  - Sol by default; Terra or Sonnet for numbers-only tie-outs.
  - The verdict and fixes are saved next to the deliverable in `review/`.
  - Purely clerical steps are not reviewed.
- **Proofs** need cross-family review (never a single Sol on a delicate proof). Fable-guided deep theory audits only on Felipe's express order.
- **Capacity:** at most 2–3 campaign threads at once. Fable calls are counted.
- **Usage limits:** when Claude Personal or Work hits its limit, pause and wait for the reset; never shut threads down or move them. Relaunching the same work after a crash is not new budget.

## 6. Review time-box (D48/D53)
- **At most two full Sol rounds per deliverable.** After that:
  - **class (i)** findings, which could change a scientific output (a duplicated or lost fit, wrong seed, allocation or record), are fixed with a test plus a narrow Sol check;
  - **class (ii)** findings, operator-recovery edge cases that halt safely, are documented in `JOB.md` with the manual resolution and accepted by HQ without a further round.
- A marginal clean-up must never stall NOTS work (D40).

## 7. Impeccable redeployment (D36)
"It's not a big deal if errors are found, but the second deployment must be impeccable." For every bundle:
- frozen code with a manifest;
- local tests including negative controls;
- Sol review to ACCEPT;
- a pilot before scale;
- an independent tie-out of the tables;
- no silent drops (full reconciliation).

Any fix is applied once, everywhere (both regimes), with a test that would have caught it.

Further:
- Any change to frozen code needs a new version number, a regression, a review and a ledger entry.
- No large runs on gambles: pilot first, then size the run. More than 10 seeds goes to NOTS.
- Memory safety: a measured memory request plus margin per job, and a memory pilot before enumerations.
- Use Sapphire Rapids nodes (`CONSTRAINT=sapphirerapids`) for timing-comparable runs.
- **Truth separation:** fitting code never reads sealed truth or holdout folders; truth is used only by scoring, after the fits.

## 8. Reporting style
- **Felipe sees only results**: plain, short, headline answers (the four headline questions of `Docs/PLAN.md` §2). Details stay in files.
- **Briefings are "so I can make choices"**, not "a Bible": concrete, with nothing important left out.
- **At p ≫ n, never present** Ẑ accuracy or PIP error against an exact reference (D22).
- **Never inflate a status:** "proved/locked" ≠ "adopted"; adoption is Felipe's word.
- Felipe often decides through inline comments on quoted text. Read them and record them in DECISIONS.

## 9. Autonomy
- **"Manage this yourself"** (Felipe, 2026-10-30): HQ handles routine operations without step-by-step relays: crashes, reviews, fixes, authorised clean-ups, NOTS storage (D31).
- **Message Felipe only for** milestones (production on NOTS, all experimental work done) and decisions that are genuinely his: scope, budget, method changes, adoption, deleting his own files, publishing.
- **Method changes** need the investment rule (`Docs/PLAN.md` §1.6) and Felipe's assent; LEVERS directions need his sign-off.
- **The theory proof swarm** starts only after Felipe's green light per confidence card.
- **Agents never commit or push** to this repo unless Felipe explicitly says so for that change.
- **Launch threads inside the GH project** ("tag with the project").
