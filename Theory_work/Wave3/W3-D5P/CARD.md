# W3-D5P — card text proposal for HQ (Corollary 6L; placement is HQ's)

Per D109, the hypotheses are stated as "those of Theorem 6", with nothing added, so any change to row 3.1's presented scope
carries over automatically. Statuses are left as placeholders until CP3 (filled verbatim from the passing council).

## Option A (recommended): a new row 3.1L directly under row 3.1

| Row | Claim (plain words) | Master / status | Why it matters | Notes |
|---|---|---|---|---|
| 3.1L (Cor 6L) | **The list the method returns gives consistent PIPs, median model and evidence on every Theorem 6 design.** Under the hypotheses of Theorem 6: on the same data event, every run that produces output (any seed, any calibration outcome) has the true model in its returned list of at most $40p+1$ best-scored models and reports it; the inclusion probabilities obtained by renormalising the posterior to that list are within $1-\pi(S_0\mid y)$ of the truth and of the exact posterior PIPs, the list evidence lies in $[\pi(S_0\mid y)Z,\,Z]$, and the list's median model is $S_0$ when $\pi(S_0\mid y)>\tfrac12$. Errors $O_P(\sqrt{\log n/n})$ on output; without "on output" under the delivery conventions (S4). These are the printed fields `pip_list`, `mpm_list`, `log_Z_list` (method companion of D105). The sampler's averaged `pip_primary`, `mpm` and `log_Z` are not covered outside row 3.6's scope. | `W3-D5P:LIST-R` (+ `LIST-K`, `LIST-CODE`): [status at CP3]; conditional on IMPL-LIST until Engineering's method commit is code-read. Inputs: `W3-RM2-R:RM2-R-plus@1.0.1`, `RM0-plus@1.0.1`, `DLV-0@1.0.1` "PROVED-CHECKED; council R3, …"; `W2-APP:POST@1.0.7` "PROVED-CHECKED". | Consistency of printed estimates (PIPs, median model, evidence) on AR and block designs, which row 3.6 does not reach; same hypotheses as the main theorem, parametric-up-to-log rate. Also closes the two links W3-DIST left unchecked (completed run = output; printed `hpm` = the reported model). | **short** corollary; READER: Corollary 6L under Theorem 6 (`READER_DELTA.md`) |

## Option B: a sentence added to row 3.6 ("Outside (A5): …")
"… row 3.1 still gives the reported-model result; on those designs, under the hypotheses of Theorem 6, the PIPs, median
model and evidence computed from the returned list (`pip_list`, `mpm_list`, `log_Z_list`) are within
$1-\pi(S_0\mid y)=O_P(\sqrt{\log n/n})$ of the truth on output (Corollary 6L) [W3-D5P]; consistency of the sampler's
averaged PIPs, MPM and $\hat Z$ is not claimed there."

## Tags vs the current card
Row 3.1: STRONGER (added conclusions; hypotheses and data event unchanged). Row 3.6: unchanged (Option A) or NEW-CLAIM
sentence (Option B). Row 3.5: unchanged (the list evidence is a deterministic sandwich, not an unbiasedness statement).
HQ (H5 card 15 D; dept/theory QUEUE.md, line 59): row 3.6 may be demoted to a remark after #5′; Option A is compatible with that.
