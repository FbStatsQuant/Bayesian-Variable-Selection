"""Pure independent Part I -> benchmark mapping under lead R-1.

This is B's normalized Python contract, NOT A's native schema. The parent
translates field names and one-based IDs without changing native behavior.
IDs here are sorted zero-based original column IDs, possibly with gaps.
E1/E2/E3 booleans mean failures. None explicitly denotes unavailable or
non-applicable evidence; omitted fields are errors. See ADAPTER_CRITERIA.md.
No production/prototype imports, I/O, truth, fitting, or scoring.
"""
from collections.abc import Mapping
from copy import deepcopy
import math
from numbers import Integral, Real


STATUSES = frozenset({
    "exact", "completed", "schedule_limit", "numerical_failure",
    "resource_limit", "invalid_input", "y_constant", "no_predictors",
})
SUCCESS_STATUSES = frozenset({"exact", "completed"})
REQUIRED_FIELDS = (
    "status", "selected", "pips", "original_indices", "runtime_s",
    "warnings", "messages", "flags",
)
REQUIRED_FLAGS = (
    "E1", "E2", "E3", "checks_passed_final", "low_empirical_ESS",
    "grid_unconverged", "local_limit", "escalated", "cut_group",
    "near_tie_truncated", "forced_pilot_steps", "exact_branch",
    "local_certified", "global_certified", "checks_passed_calibration",
)
FINAL_BUNDLE = (
    "E1", "E2", "E3", "low_empirical_ESS", "checks_passed_final",
)
IDENTIFIER_FIELDS = frozenset({
    "case_id", "dataset_id", "scale_key", "x_sha256", "y_sha256",
    "data_seed", "method_seed", "run_id",
})


def _ids(value):
    """Validate a materialized original-ID sequence without changing order."""
    if not isinstance(value, (list, tuple)):
        return False
    if any(isinstance(j, bool) or not isinstance(j, Integral) or j < 0
           for j in value):
        return False
    return all(left < right for left, right in zip(value, value[1:]))


def _finite_number(value):
    if isinstance(value, bool) or not isinstance(value, Real):
        return False
    try:
        return math.isfinite(value)
    except (OverflowError, TypeError, ValueError):
        return False


def validation_errors(record):
    """Return explicit mapping-contract errors; [] does not verify a fit.

    All required flags must be present even on early failures. On exact or
    failed fits callers may explicitly report non-applicable flags as None.
    A known final-check bundle must be complete and logically consistent.
    Native extra fields are opaque; their method semantics are checked by
    the separate Part I oracles/review, not reconstructed in this adapter.
    """
    if not isinstance(record, Mapping):
        return ["record must be a mapping"]
    errors = [f"missing required field: {key}" for key in REQUIRED_FIELDS
              if key not in record]
    if errors:
        return errors
    status = record["status"]
    if not isinstance(status, str) or status not in STATUSES:
        errors.append("unknown native status; timeout/not_run are reconciliation-only")
    successful = isinstance(status, str) and status in SUCCESS_STATUSES
    axis = record["original_indices"]
    axis_valid = _ids(axis)
    if not axis_valid:
        errors.append("original_indices must be sorted distinct nonnegative original IDs")
    selected = record["selected"]
    if selected is None:
        if successful:
            errors.append("successful result requires selected support")
    elif not _ids(selected):
        errors.append("selected must be sorted distinct nonnegative original IDs or None")
    elif axis_valid and not set(selected).issubset(axis):
        errors.append("selected contains IDs outside original_indices")
    pips = record["pips"]
    if pips is None:
        if successful:
            errors.append("successful result requires primary PIPs")
    elif not isinstance(pips, (list, tuple)):
        errors.append("pips must be an aligned list/tuple or None")
    else:
        if axis_valid and len(pips) != len(axis):
            errors.append("pips length differs from original_indices")
        if any(not _finite_number(v) or not 0 <= v <= 1 for v in pips):
            errors.append("primary PIPs must be finite probabilities in [0,1]")
    mpm = record.get("mpm")
    if mpm is not None:
        if not _ids(mpm):
            errors.append("mpm must be sorted distinct nonnegative original IDs or None")
        elif axis_valid:
            if not set(mpm).issubset(axis):
                errors.append("mpm contains IDs outside original_indices")
            if (isinstance(pips, (list, tuple)) and len(pips) == len(axis)
                    and all(_finite_number(v) and 0 <= v <= 1 for v in pips)):
                expected = tuple(j for j, p in zip(axis, pips) if p > 0.5)
                if tuple(mpm) != expected:
                    errors.append("mpm contradicts strict primary PIP>0.5 support")
    runtime = record["runtime_s"]
    if runtime is None:
        if successful:
            errors.append("successful result requires whole-fit runtime_s")
    elif not _finite_number(runtime) or runtime < 0:
        errors.append("runtime_s must be finite and nonnegative or None")
    for key in ("warnings", "messages"):
        conditions = record[key]
        if (not isinstance(conditions, (list, tuple))
                or any(not isinstance(v, str) for v in conditions)):
            errors.append(f"{key} must be a list/tuple of verbatim condition strings")
    flags = record["flags"]
    if not isinstance(flags, Mapping):
        errors.append("flags must be a mapping")
        return errors
    missing_flags = [key for key in REQUIRED_FLAGS if key not in flags]
    errors.extend(f"missing required flag: {key}" for key in missing_flags)
    for key in REQUIRED_FLAGS:
        if key not in flags:
            continue
        value = flags[key]
        if value is None:
            if status == "completed":
                errors.append(f"completed result requires evaluated flag: {key}")
        elif key == "forced_pilot_steps":
            if isinstance(value, bool) or not isinstance(value, Integral) or value < 0:
                errors.append("forced_pilot_steps must be a nonnegative integer or None")
        elif type(value) is not bool:
            errors.append(f"flag {key} must be a Python bool or None")
    if not any(key in missing_flags for key in FINAL_BUNDLE):
        bundle = [flags[key] for key in FINAL_BUNDLE]
        if any(v is None for v in bundle) and not all(v is None for v in bundle):
            errors.append("final-check bundle must be entirely available or entirely None")
        elif all(type(v) is bool for v in bundle):
            if flags["checks_passed_final"] != (not any(bundle[:4])):
                errors.append("checks_passed_final contradicts E1/E2/E3/low_empirical_ESS")
    if status == "exact":
        if "exact_branch" in flags and flags["exact_branch"] is not True:
            errors.append("exact result requires exact_branch=True")
        if "cut_group" in flags and flags["cut_group"] is not None:
            errors.append("exact branch requires cut_group=None")
    if status == "completed" and "exact_branch" in flags and flags["exact_branch"] is not False:
        errors.append("completed SMC result requires exact_branch=False")
    if flags.get("global_certified") is True and status != "exact":
        errors.append("global_certified requires exact status")
    return errors


def _diagnostics(flags):
    codes = [f"final_check_{key}" for key in ("E1", "E2", "E3")
             if flags[key] is True]
    codes.extend(key for key in ("low_empirical_ESS", "grid_unconverged", "local_limit")
                 if flags[key] is True)
    diagnostic = (flags["checks_passed_final"] is False
                  or any(flags[key] is True for key in (
                      "low_empirical_ESS", "grid_unconverged", "local_limit")))
    codes.extend(key for key in ("escalated", "cut_group", "near_tie_truncated")
                 if flags[key] is True)
    count = flags["forced_pilot_steps"]
    if count is not None and count > 0:
        codes.append("forced_pilot_steps")
    if flags["exact_branch"] is True:
        codes.append("exact_branch")
    if flags["local_certified"] is False:
        codes.append("local_certified_false")
    if flags["global_certified"] is True:
        codes.append("global_certified")
    return diagnostic, codes


def benchmark_rows(record, identifiers=None):
    """Map one normalized native record to [hpm, pip05] without mutation.

    Optional identifiers contain only IDENTIFIER_FIELDS; truth/scoring fields
    are not accepted there. Every native field survives in native_record.
    Primary PIPs/runtime/conditions are also exposed directly on each row.
    Failed support/k are None; an available selection (even empty) survives
    only in support_audit. Optional native mpm retains a failed PIP support
    even when PIPs are unavailable. Successful support_audit is None.
    Each row owns an independent deep copy of the native record and extras.
    """
    errors = validation_errors(record)
    if identifiers is None:
        identifiers = {}
    elif not isinstance(identifiers, Mapping):
        errors.append("identifiers must be a mapping")
    elif any(key not in IDENTIFIER_FIELDS for key in identifiers):
        errors.append("identifiers contain unsupported fields (no truth/scoring inputs)")
    if errors:
        raise ValueError("; ".join(errors))
    native_status = record["status"]
    failed = native_status not in SUCCESS_STATUSES
    status = ("failed" if failed else
              "warning" if record["warnings"] or record["messages"] else "ok")
    diag_flag, diag_codes = _diagnostics(record["flags"])
    hpm = None if record["selected"] is None else tuple(record["selected"])
    pip05 = ((None if record.get("mpm") is None else tuple(record["mpm"]))
             if record["pips"] is None else
             tuple(j for j, p in zip(record["original_indices"], record["pips"]) if p > 0.5))
    rows = []
    for rule, role, selection in (("hpm", "primary", hpm), ("pip05", "S0", pip05)):
        row = deepcopy(dict(identifiers))
        row.update({
            "method_id": "SMCBVS", "rule_id": rule, "role": role,
            "status": status, "native_status": native_status,
            "support": None if failed else selection,
            "k": None if failed else len(selection),
            "support_audit": selection if failed else None,
            "converged": None, "fold_seed": None, "fold_sha256": None,
            "diag_flag": diag_flag, "diag_codes": deepcopy(diag_codes),
            "warnings": deepcopy(record["warnings"]),
            "messages": deepcopy(record["messages"]),
            "primary_pips": deepcopy(record["pips"]),
            "original_indices": deepcopy(record["original_indices"]),
            "runtime_s": deepcopy(record["runtime_s"]),
            "native_record": deepcopy(record),
        })
        rows.append(row)
    return rows
