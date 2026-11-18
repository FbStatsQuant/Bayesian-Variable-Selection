# W3-D5P — card text proposal for HQ (Corollary 6L; placement is HQ's) — v0.3 after council R1 and diff round R2 [R1-sol-1..3, R1-opus-2, -3; R2-F-1, R2-E-1..5]

Per D109, the hypotheses are stated as "those of Theorem 6", with nothing added, so any change to row 3.1's presented scope
carries over automatically. Statuses are left as placeholders until CP3 (filled verbatim from the passing council).

## Option A (recommended): a new row 3.1L directly under row 3.1

| Row | Claim (plain words) | Master / status | Why it matters | Notes |
|---|---|---|---|---|
| 3.1L (Cor 6L) | **The list the method returns gives consistent PIPs, median model and evidence on every Theorem 6 design.** Under the hypotheses of Theorem 6: on the same data event, every run that produces output (any seed, any calibration outcome) reports the true model and holds it in its returned list of at most $40p+1$ best-scored models (on exact enumeration: in the enumeration's list). On the sampler, the printed `pip_list`, `mpm_list`, `log_Z_list` (method companion of D105) are the PIPs and median model of the posterior renormalised to that list and the log of the list's total unnormalised weight (the list evidence) [R2-E-4]; on exact enumeration, `pip_list` and `mpm_list` are the exact PIPs and median model. On Theorem 6's data event [R2-F-1], `pip_list` (on either branch) [R2-E-3] is within $\varepsilon_n:=1-\pi(S_0\mid y)$ of the truth and of the exact posterior PIPs; the list evidence satisfies $1-\varepsilon_n\le Z^{\mathrm{list}}/Z\le1$, i.e. $0\le\log Z-$`log_Z_list`$\le-\log(1-\varepsilon_n)$; `mpm_list` is $S_0$ when $\varepsilon_n<\tfrac12$. When $p\ge2$ for all large $n$, the PIP errors and the log-evidence error are $O_P(\sqrt{\log n/n})$ on output; allocation/delivery of the list fields is not claimed for the tagged method beyond output runs [T6-1]. The sampler's averaged `pip_primary`, `mpm` and `log_Z` are not covered outside row 3.6's scope. | `W3-D5P:LIST-R` (+ `LIST-K`, `LIST-CODE`): [status at CP3]; IMPL-LIST discharged at `method-v3.1.1-listpip` (main 7100bb3b, `reviews/IMPL_LIST_codeprint.md` §5); the v1.2/v1.3 statement change (NA_DROP) is under separate review (v1.2: NA_check_opus; Sol-5 (b) R1 FAIL, points b-1 to b-4 applied in v1.3; Sol-5b R3 8.7 FAIL, b-1 to b-4 fixed, b′-1 open; v1.4 not accepted, Sol-6 R5 8.4 FAIL; v1.5 scopes the delivery conclusion to output runs, HQ ruling option C, review pending; this is separate from IMPL-LIST, discharged at the tag). Inputs: `W3-RM2-R:RM2-R-plus@1.0.1`, `RM0-plus@1.0.1`, `DLV-0@1.0.1` "PROVED-CHECKED; council R3, …"; `W2-APP:POST@1.0.7` "PROVED-CHECKED". | Consistency of printed estimates (PIPs, median model, evidence) on AR and block designs that satisfy Theorem 6's conditions, which row 3.6 does not reach; same hypotheses as the main theorem, parametric-up-to-log rate. Also closes the two links W3-DIST left unchecked (completed run = output; printed `hpm` = the reported model). | **short** corollary; READER: Corollary 6L under Theorem 6 (`READER_DELTA.md`) |

## Option B: a sentence added to row 3.6 ("Outside (A5): …")
"… row 3.1 still gives the reported-model result; on those designs, under the hypotheses of Theorem 6 (for the rate: $p\ge2$ for all large $n$), on Theorem 6's data event (probability → 1) [R2-F-1],
`pip_list` (the list-renormalised PIPs; the exact PIPs on exact enumeration) [R2-E-5] is within $\varepsilon_n=1-\pi(S_0\mid y)
=O_P(\sqrt{\log n/n})$ of the truth and of the exact posterior PIPs on output, their median model (`mpm_list`) is $S_0$
when $\varepsilon_n<\tfrac12$, and the list evidence (`log_Z_list`) satisfies
$0\le\log Z-$`log_Z_list`$\le-\log(1-\varepsilon_n)$ (Corollary 6L) [W3-D5P]; consistency of the sampler's averaged
PIPs, MPM and $\hat Z$ is not claimed there."

## Tags vs the current card
Row 3.1: STRONGER (added conclusions; hypotheses and data event unchanged). Row 3.6: unchanged (Option A) or NEW-CLAIM
sentence (Option B). Row 3.5: unchanged (the list evidence is a deterministic sandwich, not an unbiasedness statement).
HQ (H5 card 15 D; dept/theory QUEUE.md, line 59): row 3.6 may be demoted to a remark after #5′; Option A is compatible with that.
