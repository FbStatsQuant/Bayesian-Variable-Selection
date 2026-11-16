# T1 · Lemma GW — CHECK (Tier B per PROTOCOL_v4 §2, §2A NORMAL)

Status (lead's label): **PROVED; Claude line check VERIFIED WITH AMENDMENTS (all applied); OpenAI layers pending at the
gate.** Not "PROVED-CHECKED": PROTOCOL_v4 §2A requires the Sol lock, a Sol line check and the OpenAI council seat.

Frozen text (sha256, first 12 hex, 2026-11-16 17:04 CST): STATEMENT v4 `6e83ae6c1e92`, PROOF v4 `87bbb1d6303c`.
Code of record: `Scripts/SMC_BVS/core/` at 4676af6 (= HEAD for the core).

| Tier B step (PROTOCOL_v4 §3, step 4 omitted) | who (NORMAL) | state | record |
|---|---|---|---|
| 1 statement lock | Sol, fresh | **pending (gate)** | — |
| 2 better-theorem review | only if the statement is new — it is a code lemma with no CP1 target; lead proposes to skip, HQ to rule | **HQ ruling** | — |
| 3 line check | Sol (NORMAL); Codex held for the gate | Claude stand-in done: LC1 (Opus, blind) → LC1r → LC1r2 (Opus, new agents), all **VERIFIED WITH AMENDMENTS**, no C/F finding open | `../reviews/LC1_*`, `LC1r_*`, `LC1r2_*` (brief, reply verbatim, disposition) |
| statement-change check (§4.2) for the changelog rows not EQUAL | Sol, new agent | **pending (gate)**; rows: v2 (GW-iv), (GW-v), (GW-i) termination STRONGER; v3 (GW-iv) WEAKER/STRONGER | STATEMENT changelog |
| 5 sweep duties → council briefs | — | at council | — |
| 6 citation check | script | **0 MISS** (232 citations) | `CITECHECK.txt` (track_A/citecheck.py) |
| 7 council R1 | Sol (OpenAI seat, Tier B) + Opus (Claude seat), blind | **pending (gate)** | — |

What LC1 found that mattered (all applied, none a failing step): `fit$peak_memory_kb` and environment readings were not
classed; the "statistical state" needed leaf-field granularity; the interface to W3-SAMP's 𝒜 and to CAL needed its
own clause (now (GW-iv): 𝒜 = 𝒜° ∩ G ⊆ 𝒜°, 𝒜° ∈ σ(𝓒°)); the premise "complete scans" is also discharged (GW-v).

**Downstream reading to flag (F, for HQ / the W3-SAMP owner, no edit made):** `W3-SAMP/STATEMENT.md:39-41` says
𝒜 ∈ σ(𝓒) for the *actual* calibration event; with the clock-driven guard that holds only for the potential pair
(𝒜°, 𝓒°). The fix is a reading, not a repair: read W3-SAMP with 𝒜° throughout (its conditional arguments "given 𝓒
on 𝒜" then hold verbatim, since 𝒜° ∈ σ(𝓒°)); its conclusions P(𝒜° ∩ ·), P(completed ∩ ·) then transfer to the actual
𝒜 because 𝒜 ⊆ 𝒜°. The price: an interface premise written with 1_𝒜 (P-START "1_𝒜·o₀ → 0", proved only under (A5);
P-OVL; P-OVL∞) must be read with 1_𝒜°. Whether the proofs of those premises (e.g. `W3-START2-R:IF-START`) already give
the 𝒜° form is not checked here — to confirm with T8 (OVL), which uses P-START. A one-line reading note in W3-SAMP's
REPORT would record it.

Lean target: **no** (code fact).
