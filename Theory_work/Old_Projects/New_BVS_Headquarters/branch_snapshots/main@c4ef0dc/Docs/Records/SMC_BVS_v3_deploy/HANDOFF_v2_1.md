# HANDOFF v2.1: the study-layer freeze (for HQ's independent reviewer)

Author: Campaign 2 OPS lead (Claude Opus 5.5), 2026-10-23. Authority: BRIEF_CLAUDE.md "Required fixes" 1; AUDIT_SUMMARY decision 1; AUDIT_A_CODE F1, F3, F5 (F2 optional).

## What v2.1 is

v2.1 is A's frozen v2 snapshot with four study-layer files changed. **The method core (`code/core/**`, 20 files) is byte-identical to v2**: `freeze_v2_1.py` asserts it file by file against v2's SHA256SUMS. Nothing statistical changes.

| Identity | Value |
|---|---|
| Base: A v2 SHA256SUMS | `b56100b3740e818fa2b7011216448972bcdb86f7d01a7c4a2c92fd61470dad5a` (archive 17bdd21a…e1ff) |
| v2.1 SHA256SUMS (95 lines, same file set as v2) | `908a70ca38314ef8fa1980fd0002efd37eabdd2dd0ca392f2f405858548f309b` |
| v2.1 manifest.json | `adf94e042ec36778c34006cd489e894f17053bbe76d4785e3f2434fccd1150ca` |
| v2.1 archive `E_ops_claude/artifacts/v2_1.tar.gz` | `34903264f9c024dbea11b411ef41f1295b4ceff7ebe2ae403100a85c3839e5e9` |
| Unified diff, all 4 files (`E_ops_claude/checks/v2_to_v2_1.diff`) | `d392f8ace2369d33762007c0ada661ce395c1f46f3881a5fecde26d6596243ec` |
| Local copy | `E_ops_claude/v2_1/` |
| NOTS copy (read-only after the cache build) | `/home/fb31/projects/BVS/SMC_BVS_v3/deploy/claude/code/v2_1/` |

## The diff, item by item

| File | Change | Finding | Why it is safe |
|---|---|---|---|
| `code/study/adapter.R` l.167 | `sort(unique(files))` → `sort(unique(files), method = "radix")`, with a comment | **F1**: the aggregate `source_sha256` depended on the collation locale | Radix sort is C-locale byte order on every host. The hash is still computed over the same (label, sha) pairs; only their order is fixed. The aggregate value changes from v2's, as it would anyway, because adapter.R changed. |
| `code/study/adapter.R` l.382–383 (old) | Removed the `stop("infrastructure memory allocation failure; …")` special case, with a comment in its place | **F3**: an R-level `cannot allocate` / `bad_alloc` error is now recorded like every other R error from the fit | The error falls through the existing generic path: `native = "adapter_error"`, `fit = NULL`, both rules `failed` (R-1), `error` verbatim, `.done` written. This matches the benchmark's outer tryCatch (AUDIT_A_CODE F3: the benchmark records `failed`). D's native contract accepts `adapter_error` with `fit = NULL` (`D_analysis/pipeline/native_contract.R:14–17`). Scheduler kills (no `.done`) remain infrastructure events for the runner. |
| `code/study/adapter.R` l.412 | `adapter_version = "2-R1"` → `"2.1-R1"` | provenance | Not used by D's pipeline (grep). |
| `code/study/README.md`, `SCHEMA.md` | One sentence each, describing the F3 behaviour | docs | SCHEMA.md keeps its CRLF line endings (as in v2). |
| `smoke/test_adapter_contract.R` | The OOM check now expects a recorded failed unit (`.done`, `failed`, `adapter_error`, `fit = NULL`, verbatim error, resume-skip). New F1 check: the aggregate hash is identical under C, C.UTF-8 and en_US.utf8. It has power only if some tested locale really collates the hashed paths differently from C, and the test asserts that it does. Version check updated to 2.1-R1. | tests | — |

**Not changed:**
- **F2** (exact-branch `log_Z_lower95`) would change core file `v3_fit.R`. The brief keeps the core untouched, and no study fit takes the exact branch.
- **F5** is implemented in the runner, not in the study layer: `--hours` = the unit limit L; the hard kill is at L + 5 min (ASSUMPTIONS.md #3).

## Evidence on NOTS (GCC 14.3.0, R 4.5.2)

All on v2.1. Details are in NOTS_READINESS.md; logs are in `evidence/`.
- **Regression.** A's 32-seed prototype regression: **32/32 PASS**, job 2358209.
- **Contract test.** The v2.1 adapter contract test passes with **77 checks**, including:
  - "v2.1 F3: R-level OOM is a recorded failed unit";
  - "v2.1 F1: aggregate source hash is independent of the collation locale" (locales C, en_US.UTF-8, en_US.utf8, C.UTF-8).
- **B's battery.** It runs on its frozen v2 payload, which has the same core, and **passes**: job 2358210.
- **Tiny-p SMC versus exact.** **PASS**: 40 fits, jobs 2358265–67.
- **Dev smokes.** The two dev smokes through the v2.1 adapter are **bit-identical** to the Owls v2 smokes on every statistical output and rule row. The v2.1 aggregate source hash is `b28719e6…4e23` on every NOTS run.
- **e2e fit.** One real e2e fit (p1000_S4_r001 c050) ran through the production runner: ok/ok.

## What the reviewer should attack

1. Can the F3 path ever write `.done` for a unit whose process was actually killed by the scheduler? It should not: a kill skips R entirely.
2. Does any downstream reader rely on the old OOM behaviour (no `.done`)? I found none in D's pipeline; F_analysis is the consumer.
3. Is radix order identical between the R 4.4/4.6 (laptop, Owls) and 4.5.2 (NOTS) implementations for these ASCII paths? It should be: byte order.
