#!/usr/bin/env python3
"""IV.1 assessment integration. Local development permitted by Amendment 2."""
import argparse
import collections
import csv
import datetime
import hashlib
import html
import json
import math
import os
from pathlib import Path
import platform
import shutil
import statistics
import subprocess
import sys
import traceback

ROOT = Path(__file__).resolve().parent
OWNER = next((p for p in (ROOT, *ROOT.parents) if p.name == "pipeline"), ROOT)
RULING_SHA256 = "3bf2e514065ff4ccdaf5f2dd9ec82375df147f3bd6f308f75c965f5975bbe88a"
PINNED = {
    "registry.R": "cc19602b2780b3706c505d7b0d6984053c58bf68df96a001d4e3ad88106be1e0",
    "score.R": "ec3ac2e03748ac7f360a76bc8d6300d1f35ef2fdcd00f87c04c32ab2d1ecbc6b",
    "aggregate.R": "031d845dd8981a636881378893aa6ce2d782a87ebc6fe97d175af1c08a4e244f",
    "combine.R": "a79bec52141cf01d4ec3cc69fa939adcea395a48b232612c74e5a075aa98a1b2",
}
TABLES = ["rules_long", "T1", "T2", "T3", "T4_by_variable", "T4_by_group",
          "T5", "T6", "S_tables", "caps", "codes_by_rule"]
FAIL = {"failed", "timeout", "not_run"}
NA = {"", "NA"}


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def sha(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(65536), b""):
            h.update(block)
    return h.hexdigest()


def safe_read(path):
    p = Path(path).resolve()
    if "holdout" in {s.lower() for s in p.parts}:
        raise ValueError("holdout access refused")
    return p


def read(path):
    with safe_read(path).open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames or len(reader.fieldnames) != len(set(reader.fieldnames)):
            raise ValueError(f"missing/duplicate CSV header: {path}")
        return list(reader)


def write(path, rows, fields=None):
    rows = list(rows)
    if fields is None:
        fields = list(dict.fromkeys(k for row in rows for k in row))
    with Path(path).open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fields)
        w.writeheader()
        for row in rows:
            w.writerow({k: "NA" if v is None else v for k, v in row.items()})


def number(x):
    return None if x in NA or x is None else float(x)


def success(row):
    return row is not None and row["status"] in {"ok", "warning"}


def flag(row):
    return row is not None and row["diag_flag"] == "TRUE"


def passing(row):
    # Unavailable diagnostics never silently qualify as passing.
    return row is not None and row["diag_flag"] == "FALSE"


def exact(row):
    return int(success(row) and row["exact"] == "TRUE")


def stats(values):
    x = [float(v) for v in values]
    n = len(x)
    var = statistics.variance(x) if n > 1 else None
    return {"n": n, "sum": sum(x), "mean": statistics.mean(x) if n else None,
            "sample_variance": var, "mcse": math.sqrt(var/n) if var is not None else None}


def stratified(pairs):
    """Fixed scenario strata; observed denominator supplies each stratum weight."""
    groups = collections.defaultdict(list)
    for scenario, value in pairs:
        groups[scenario].append(value)
    n = sum(map(len, groups.values()))
    means = [stats(v) for v in groups.values()]
    if not n:
        return None
    if any(g["sample_variance"] is None for g in means):
        return None
    return math.sqrt(sum((g["n"]/n)**2 * g["sample_variance"]/g["n"] for g in means))


def metric(prefix, pairs):
    result = {prefix + "_" + k: v for k, v in stats([x[1] for x in pairs]).items()}
    result[prefix + "_mcse"] = stratified(pairs)
    return result


def quantile7(x, probability):
    if not x:
        return None
    x = sorted(x)
    pos = (len(x)-1)*probability
    lo = int(math.floor(pos)); hi = int(math.ceil(pos))
    return x[lo] + (pos-lo)*(x[hi]-x[lo])


class Audit:
    def __init__(self, out, config):
        self.out = out
        self.files = {}
        self.commands = []
        self.state = {"started_utc": utc(), "status": "running", "config": config,
                      "host": platform.node(), "python": sys.version,
                      "argv": sys.argv, "cwd": str(Path.cwd()),
                      "environment": {k: v for k, v in os.environ.items()
                                      if k.startswith("SLURM_") or k in
                                      {"LOADEDMODULES", "MODULEPATH", "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS"}}}

    def record(self, path):
        p = safe_read(path)
        self.files[str(p)] = {"sha256": sha(p), "bytes": p.stat().st_size}

    def command(self, argv, label):
        started = utc()
        with (self.out / (label + ".log")).open("w", encoding="utf-8") as log:
            proc = subprocess.Popen(list(map(str, argv)), stdout=log, stderr=subprocess.STDOUT)
            rc=proc.wait()
        self.commands.append({"argv": list(map(str, argv)), "started_utc": started,
                              "finished_utc": utc(), "exit_status": rc,"pid":proc.pid,
                              "log_sha256":sha(self.out/(label+".log"))})
        self.save()
        if proc.returncode:
            detail = (self.out / (label + ".log")).read_text(encoding="utf-8", errors="replace")[-4000:]
            raise RuntimeError(f"command failed ({proc.returncode}); see {label}.log\n{detail}")

    def save(self):
        self.state.update(files=self.files, commands=self.commands)
        (self.out / "manifest.json").write_text(json.dumps(self.state, indent=2), encoding="utf-8")


def cases_from_manifest(config, audit):
    path = config["inputs_manifest"]
    audit.record(path)
    source = read(path)
    ids = [r["dataset_id"] for r in source]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate input dataset_id")
    cases = {}
    for row in source:
        p, sc, rep = (int(row[k]) for k in ("p", "scenario", "replicate"))
        if p not in {500, 1000} or sc not in range(1, 7):
            raise ValueError("unexpected input design")
        if rep not in range(1, 101):
            raise ValueError("unexpected input replicate")
        if row["dataset_id"] != f"p{p:04d}_S{sc}_r{rep:03d}":
            raise ValueError("dataset ID/design mismatch")
        for sk in ("c100", "c050"):
            case = dict(row, scale_key=sk, case_id=row["dataset_id"]+"_"+sk,
                        y_sha256=row[f"y_{sk}_sha256"])
            cases[case["case_id"]] = case
    # Two allowed designs: Amendment 1 (r1..10, 120 datasets / 240 cases) and the Campaign 2 full
    # design (BRIEF_CLAUDE: r1..100, 1,200 datasets / 2,400 cases). Nothing else is accepted.
    designs = {R: {"p": [500, 1000], "scenario": [1, 2, 3, 4, 5, 6],
                   "replicate": list(range(1, R+1)), "scale_key": ["c100", "c050"]} for R in (10, 100)}
    R = next((R for R, s in designs.items() if config.get("assessment_selector") == s), None)
    if R is None:
        raise ValueError("supply the exact Amendment 1 assessment_selector (r1..10) or the full design (r1..100), including both scales")
    selector = designs[R]
    selected = {cid: c for cid, c in cases.items() if int(c["replicate"]) <= R}
    wanted = {(p, sc, rep, sk) for p in (500, 1000) for sc in range(1, 7)
              for rep in range(1, R+1) for sk in ("c100", "c050")}
    actual = {(int(c["p"]), int(c["scenario"]), int(c["replicate"]), c["scale_key"]) for c in selected.values()}
    if actual != wanted or len(selected) != 24*R:
        raise ValueError(f"assessment selector must yield exactly {12*R} datasets / {24*R} cases")
    selected_ids = {c["dataset_id"] for c in selected.values()}
    write(audit.out/"selected_inputs_manifest.csv", [r for r in source if r["dataset_id"] in selected_ids])
    write(audit.out/"selected_cases.csv", [dict(case_id=k, dataset_id=v["dataset_id"],
          scale_key=v["scale_key"], x_sha256=v["x_sha256"], y_sha256=v["y_sha256"])
          for k,v in sorted(selected.items())])
    audit.record(audit.out/"selected_inputs_manifest.csv")
    audit.record(audit.out/"selected_cases.csv")
    audit.state["assessment_selection"] = dict(selector=selector, datasets=12*R, cases=24*R,
        selector_sha256=hashlib.sha256(json.dumps(selector,sort_keys=True,separators=(",",":")).encode()).hexdigest(),
        selected_cases_sha256=sha(audit.out/"selected_cases.csv"))
    return cases, selected


def validate_rows(rows, cases):
    seen = set()
    fits = collections.defaultdict(list)
    for r in rows:
        key = tuple(r[k] for k in ("case_id", "method_id", "rule_id"))
        if key in seen:
            raise ValueError(f"duplicate row key {key}")
        seen.add(key)
        fits[(r["case_id"], r["method_id"])].append(r)
        c = cases.get(r["case_id"])
        if c is None:
            raise ValueError(f"row outside authoritative design {key}")
        for col in ("x_sha256", "y_sha256"):
            if r[col] != c[col] or len(r[col]) != 64 or any(x not in "0123456789abcdef" for x in r[col]):
                raise ValueError(f"input hash mismatch {key}: {col}")
        for col in ("dataset_id", "scale_key"):
            if r[col] != c[col]:
                raise ValueError(f"design mismatch {key}: {col}")
        for col in ("p", "scenario", "replicate"):
            if float(r[col]) != float(c[col]):
                raise ValueError(f"design mismatch {key}: {col}")
        if r["regime"] != "H" or r["status"] not in FAIL | {"ok", "warning"}:
            raise ValueError(f"invalid regime/status {key}")
        if r["diag_flag"] not in {"TRUE", "FALSE", "NA"} or r["exact"] not in {"TRUE", "FALSE"}:
            raise ValueError(f"invalid scored flags {key}")
        if success(r):
            for col in ("fp", "fn", "tp"):
                v = number(r[col])
                if v is None or v < 0 or not v.is_integer():
                    raise ValueError(f"invalid successful score {key}: {col}")
            if exact(r) != int(float(r["fp"]) == 0 and float(r["fn"]) == 0):
                raise ValueError("exact score disagrees with FP/FN")
            if any(r[f"sel_a{i:02d}"] not in {"0", "1"} for i in range(1, 15)):
                raise ValueError("missing active-variable success score")
        elif r["exact"] != "FALSE" or any(r[k] not in NA for k in ("fp", "fn", "tp")):
            raise ValueError("failed rows must be non-recovery with unavailable FP/FN/TP")
    for key, fit in fits.items():
        shared = ["source_sha256", "run_id", "inputs_sha256", "x_sha256", "y_sha256", "fold_sha256",
                  "data_seed", "fold_seed", "method_seed", "runtime_s", "v3_status", "v3_flags_json",
                  "adapter_mapping_status", "adapter_policy_id", "adapter_policy_sha256"]
        for col in shared:
            if any(col in row for row in fit) and len({row.get(col, "NA") for row in fit}) != 1:
                raise ValueError(f"within-fit {col} differs: {key}")
        source_hash = fit[0]["source_sha256"]
        if len(source_hash) != 64 or any(c not in "0123456789abcdef" for c in source_hash):
            raise ValueError(f"invalid within-fit source identity: {key}")
        statuses = {r["status"] for r in fit}
        if len({r["diag_flag"] for r in fit if success(r)}) > 1:
            raise ValueError(f"within-fit successful diag_flag differs: {key}")
        # Master III.3.0 permits a single rule to fail a point check while other rules succeed.
        # Scheduler outcomes, by contrast, belong to the whole fit and cannot coexist with success.
        if statuses & {"timeout", "not_run"} and len(statuses) != 1:
            raise ValueError(f"inconsistent fit-wide scheduler status: {key}")


def cells(cases, sk):
    for p in ("500", "1000"):
        for sc in [str(s) for s in range(1, 7)] + ["pooled"]:
            selected = [c for c in cases.values() if c["scale_key"] == sk and int(c["p"]) == int(p)
                        and (sc == "pooled" or int(c["scenario"]) == int(sc))]
            if selected:
                yield p, sc, sorted(selected, key=lambda c: c["case_id"])


def build_tables(rows, cases, registry, out, signals):
    lookup = {(r["case_id"], r["method_id"], r["rule_id"]): r for r in rows}
    by_fit = collections.defaultdict(list)
    for (cid, mid, _), r in lookup.items():
        by_fit[(cid, mid)].append(r)
    summaries, paired, t4, runtimes, diagnostics, failures = [], [], [], [], [], []
    for reg in registry:
        m, rule, sk = (reg[k] for k in ("method_id", "rule_id", "scale_key"))
        for p, sc, cs in cells(cases, sk):
            rs = [lookup.get((c["case_id"], m, rule)) for c in cs]
            base = dict(reg, p=p, scenario=sc)
            row = dict(base, n_expected=len(cs), n_rows=sum(r is not None for r in rs),
                       n_success=sum(success(r) for r in rs), n_missing=sum(r is None for r in rs),
                       n_flagged=sum(flag(r) for r in rs))
            for st in sorted(FAIL):
                row["n_"+st] = sum(r is not None and r["status"] == st for r in rs)
            row["n_fail_total"] = len(cs)-row["n_success"]
            for name, val in (("exact_all", lambda r: exact(r)),
                              ("exact_passing", lambda r: exact(r)*int(passing(r))),
                              ("failure", lambda r: int(not success(r)))):
                row.update(metric(name, [(c["scenario"], val(r)) for c, r in zip(cs, rs)]))
            row.update(metric("exact_among_success", [(c["scenario"], exact(r)) for c, r in zip(cs, rs) if success(r)]))
            for name in ("tp", "fp", "fn"):
                row.update(metric(name, [(c["scenario"], number(r[name])) for c, r in zip(cs, rs) if success(r)]))
            for error in ("exact", "extra_only", "missed_only", "mixed", "failed"):
                row["err_"+error] = sum(r is not None and r["error_type"] == error for r in rs)
            row["n_k_gt_K"] = (sum(success(r) and number(r["k"]) is not None and number(r["k"])>37 for r in rs)
                                  if m in {"F1","F2","F3","F4","F4_SCAD","F5"} or rule.startswith(("ebic","bic","sic")) else None)
            summaries.append(row)
            failures.append({k: row[k] for k in list(base)+["n_expected", "n_rows", "n_success", "n_missing",
                                                          "n_failed", "n_timeout", "n_not_run", "n_fail_total", "n_flagged"]})
            codes = sorted({code for r in rs if r for code in r["diag_codes"].split(";") if code not in NA})
            for code in codes:
                diagnostics.append(dict(base, code=code, count=sum(r is not None and code in r["diag_codes"].split(";") for r in rs)))
            for native in ("v3_status", "v3_flags_json", "adapter_mapping_status", "adapter_policy_id", "converged", "status", "diag_flag"):
                for value, count in collections.Counter(r.get(native, "NA") for r in rs if r).items():
                    diagnostics.append(dict(base, code=native+"="+value, count=count))
            sg = signals.get(int(p), [])
            groups = collections.defaultdict(list)
            for i, signal in enumerate(sg, 1):
                idx = int(signal["index"])
                beta = float(signal["beta"])
                rho = 0.4+0.1*(((idx-1)//5) % 6)
                groups[("variable", f"a{i:02d}")].append(i)
                groups[("abs_beta", f"{abs(beta):.1f}")].append(i)
                groups[("rho_S6", f"{rho:.1f}")].append(i)
            for (group_type, group), active in groups.items():
                pairs = [(c["scenario"], sum(int(r[f"sel_a{i:02d}"]) for i in active)/len(active)
                          if success(r) else 0.0) for c, r in zip(cs, rs)]
                t4.append(dict(base, group_type=group_type, group=group, n_signals=len(active),
                               n_opportunities=len(cs)*len(active),
                               n_selected=sum(sum(int(r[f"sel_a{i:02d}"]) for i in active) if success(r) else 0 for r in rs),
                               **metric("selection", pairs)))
            # One runtime per fit, repeated rules do not create extra observations.
            if sc == "pooled" and rule == next(x["rule_id"] for x in registry if x["method_id"] == m and x["scale_key"] == sk):
                x = []
                for c in cs:
                    fit = by_fit.get((c["case_id"], m), [])
                    values = {r["runtime_s"] for r in fit}
                    if len(values) > 1:
                        raise ValueError("inconsistent runtime across rules")
                    if values:
                        v = number(next(iter(values)))
                        if v is not None:
                            if not math.isfinite(v) or v < 0:
                                raise ValueError("invalid runtime")
                            x.append(v)
                runtimes.append(dict(method_id=m, scale_key=sk, p=p, n_fits_with_runtime=len(x),
                                     median_s=statistics.median(x) if x else None,
                                     p95_s=quantile7(x, .95), max_s=max(x) if x else None))
            if m == "SMCBVS":
                continue
            for smc_rule in ("hpm", "pip05"):
                pairs = [(c, a, lookup.get((c["case_id"], "SMCBVS", smc_rule))) for c, a in zip(cs, rs)]
                pr = dict(base, smc_rule=smc_rule, n_expected=len(cs),
                          n_observed_pairs=sum(a is not None and b is not None for _, a, b in pairs),
                          wins=sum(exact(b)>exact(a) for _, a, b in pairs),
                          losses=sum(exact(b)<exact(a) for _, a, b in pairs),
                          ties=sum(exact(b)==exact(a) for _, a, b in pairs))
                for name, fun in (("exact", lambda r: exact(r)),
                                  ("passing", lambda r: exact(r)*int(passing(r))),
                                  ("failure", lambda r: int(not success(r)))):
                    pr.update(metric(name+"_difference", [(c["scenario"], fun(b)-fun(a)) for c,a,b in pairs]))
                for name in ("fp", "fn"):
                    pr.update(metric(name+"_difference", [(c["scenario"], number(b[name])-number(a[name]))
                                                          for c,a,b in pairs if success(a) and success(b)]))
                paired.append(pr)
    write(out/"study_metrics_mcse.csv", summaries)
    write(out/"paired_comparisons.csv", paired)
    write(out/"T4_mcse.csv", t4)
    write(out/"T5_runtime.csv", runtimes)
    write(out/"T6_diagnostics.csv", diagnostics)
    write(out/"failure_summary.csv", failures)
    return summaries, paired


def figures(summaries, out):
    # Inspectable SVG, no plotting dependency. All rules share the same probability scale.
    for sk in ("c100", "c050"):
        for p in ("500", "1000"):
            for sc in [str(s) for s in range(1, 7)]+["pooled"]:
                rs = [r for r in summaries if r["scale_key"] == sk and r["p"] == p and r["scenario"] == sc]
                height = 50+len(rs)*24
                svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="{height}" viewBox="0 0 1400 {height}">',
                       '<rect width="100%" height="100%" fill="white"/>',
                       f'<text x="8" y="20">PROVISIONAL exact recovery: {sk}, p={p}, scenario={sc}; bars 0 to 1; whiskers +/- MCSE</text>']
                for i, r in enumerate(rs):
                    y = 40+i*24; mean = r["exact_all_mean"]; se = r["exact_all_mcse"]
                    label = html.escape(f'{r["method_id"]}/{r["rule_id"]} ({r["role"]}) [{r["label"]}]')
                    svg.append(f'<text x="8" y="{y+12}" font-size="10">{label}</text>')
                    svg.append(f'<rect x="850" y="{y}" width="{400*mean}" height="15" fill="{"#176f58" if r["method_id"]=="SMCBVS" else "#527da1"}"/>')
                    if se is not None:
                        svg.append(f'<path d="M{850+400*max(0,mean-se)} {y+7} H{850+400*min(1,mean+se)}" stroke="black"/>')
                    svg.append(f'<text x="1260" y="{y+12}" font-size="11">{int(r["exact_all_sum"])}/{r["n_expected"]}</text>')
                (out/f"exact_{sk}_p{p}_S{sc}.svg").write_text("\n".join(svg+["</svg>"]), encoding="utf-8")


def run(config_path):
    config = json.loads(safe_read(config_path).read_text(encoding="utf-8-sig"))
    if config["mode"] not in {"synthetic", "assessment"}:
        raise ValueError("mode must be synthetic or assessment; full production is deferred")
    local_mock = config["mode"] == "synthetic"
    # Amendment 2 authorizes local development/testing. Resource gates apply only on Owls.
    if platform.system() == "Linux" and platform.node().lower().split(".")[0].startswith("owls"):
        if os.getpriority(os.PRIO_PROCESS, 0) < 19:
            raise RuntimeError("Owls execution requires nice -n 19")
        available_kib = next(int(line.split()[1]) for line in Path("/proc/meminfo").read_text().splitlines()
                             if line.startswith("MemAvailable:"))
        if os.getloadavg()[0] > 40 or available_kib < 30*1024*1024:
            raise RuntimeError("Owls shared-machine batch gate failed; parent must retry after 15 minutes")
    for name in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
        os.environ[name] = "1"
    out = Path(config["out"]).resolve()
    # Relocatable (F_analysis_claude): output_root is an explicit directory, default the output's parent.
    allowed = Path(config.get("output_root", out.parent)).resolve()
    if local_mock:
        for name in ("inputs_manifest", "truth_manifest", "truth_dir", "mapping_csv"):
            if not safe_read(config[name]).is_relative_to(allowed):
                raise ValueError("mock inputs must be generated fixture artifacts inside output_root")
    if not out.is_relative_to(allowed):
        raise ValueError("output must be within output_root")
    out.mkdir(parents=True, exist_ok=False)
    audit = Audit(out, config)
    try:
        audit.record(config_path)
        if config.get("source_inventory"):
            audit.record(config["source_inventory"])
        snapshot = out/"snapshot"; snapshot.mkdir()
        for path in sorted(ROOT.iterdir()):
            if path.is_file():
                audit.record(path); shutil.copy2(path, snapshot/path.name)
        if (ROOT/"vendor").is_dir():
            shutil.copytree(ROOT/"vendor", snapshot/"vendor")
            for path in (ROOT/"vendor").rglob("*"):
                if path.is_file(): audit.record(path)
        benchmark = safe_read(config["benchmark_scoring"])
        source_validation = []
        for directory in ("code", "derived_rules"):
            source = benchmark/directory
            for path in source.rglob("*"):
                if path.is_file(): audit.record(path)
            shutil.copytree(source, snapshot/"benchmark"/directory)
            for path in sorted(source.rglob("*")):
                if path.is_file():
                    copied = snapshot/"benchmark"/directory/path.relative_to(source)
                    original_hash, copied_hash = sha(path), sha(copied)
                    source_validation.append(dict(source=str(path), snapshot=str(copied),
                                                  source_sha256=original_hash, snapshot_sha256=copied_hash,
                                                  byte_identical=original_hash == copied_hash))
                    if original_hash != copied_hash:
                        raise ValueError("benchmark snapshot differs from source")
        write(out/"source_validation.csv", source_validation)
        code = snapshot/"benchmark"/"code"
        for filename, expected in PINNED.items():
            if sha(code/filename) != expected:
                raise ValueError(f"benchmark source version differs: {filename}; review pins explicitly")
        audit.record(config["truth_manifest"])
        ruling_path = config.get("mapping_ruling", ROOT/"vendor"/"RULINGS_LEAD.md")
        audit.record(ruling_path)
        if sha(ruling_path) != RULING_SHA256:
            raise ValueError("binding R-1 ruling hash mismatch; review the changed ruling explicitly")
        shutil.copy2(ruling_path, snapshot/"RULINGS_LEAD.md")
        audit.state["mapping_authority"] = dict(version="R-1",sha256=RULING_SHA256,path=str(ruling_path))
        if config.get("mapping_csv"): audit.record(config["mapping_csv"]) # optional fixture audit, never mapping authority
        if config["mode"] == "assessment":
            for name in ("ops_outputs",):
                audit.record(config[name])
            if not config["ops_outputs"]:
                raise ValueError("assessment requires C_ops/OUTPUTS.md")
        all_cases, cases = cases_from_manifest(config, audit)
        adapter = snapshot/"benchmark_adapter.R"
        def rcall(mode, dest, extra=(), label=None):
            dest.mkdir(parents=True, exist_ok=True)
            audit.command([config.get("rscript", "Rscript"), "--vanilla", adapter, mode, code, dest, *extra],
                          label or mode)
        rcall("registry", out/"registry")
        registry = read(out/"registry"/"registry.csv")
        rows = []; signals = {}
        reproduction = []; selection_checks = []; reproduced_runs = collections.defaultdict(list)
        reference_gaps = []
        for index, spec in enumerate(config["benchmark_sources"]):
            source = safe_read(spec["scored_dir"])
            dest = out/"reproduced_runs"/str(index)/source.name
            dest.mkdir(parents=True)
            for filename in ("scored_rows.csv", "coverage.csv", "problems.csv", "truth_signals.csv", "score_log.txt"):
                audit.record(source/filename); shutil.copy2(source/filename, dest/filename)
            problems = read(source/"problems.csv")
            if any(x["check"] not in {"case_missing", "case_incomplete", "missing_rule_row"} for x in problems):
                raise ValueError("benchmark source has blocking scoring problems")
            source_rows = read(source/"scored_rows.csv")
            if local_mock and any(r["study"] != "SYNTHETIC_NOT_PRODUCTION" for r in source_rows):
                raise ValueError("synthetic mode accepts labelled fixtures only")
            if config["mode"] == "assessment" and any(r["study"] == "SYNTHETIC_NOT_PRODUCTION" for r in source_rows):
                raise ValueError("assessment refuses synthetic study rows")
            source_scales = {r["scale_key"] for r in source_rows}
            if len(source_scales) != 1:
                raise ValueError("each benchmark scored source must have exactly one scale")
            source_scale = next(iter(source_scales))
            # Assert hashes and keys against the full manifest BEFORE filtering; this cannot
            # hide mismatched out-of-scope records. Revalidate the retained assessment AFTER.
            validate_rows(source_rows, all_cases)
            selected_rows = [r for r in source_rows if r["case_id"] in cases]
            validate_rows(selected_rows, cases)
            selection_checks.append(dict(source=str(source), rows_before=len(source_rows),
                rows_selected=len(selected_rows), rows_excluded=len(source_rows)-len(selected_rows),
                hash_assertions_before=True, hash_assertions_after=True))
            # Explicit identity aliases isolate a saved long-chain sensitivity after reproducing
            # its own published tables under its original method_id. Baseline files are unchanged.
            for row in selected_rows:
                row["method_id"] = spec.get("method_alias", {}).get(row["method_id"], row["method_id"])
            rows.extend(selected_rows)
            for s in read(source/"truth_signals.csv"):
                p = int(s["p"]); old = signals.setdefault(p, {}).get(s["signal"])
                if old and any(float(old[k]) != float(s[k]) for k in ("index", "beta")):
                    raise ValueError("benchmark signal map differs across sources")
                signals[p][s["signal"]] = s
            rcall("reproduce", dest, label=f"reproduce_{index:02d}")
            if spec.get("include_in_canonical_combine", not bool(spec.get("method_alias"))):
                reproduced_runs[source_scale].append(dest)
            declared = spec.get("tables", {})
            if declared and set(declared) != set(TABLES):
                raise ValueError("declare all 11 published tables and exact sort keys per source")
            for table, claim in declared.items():
                if "unavailable" in claim:
                    if not claim["unavailable"]: raise ValueError("reference gap needs a reason")
                    reference_gaps.append(dict(scope=str(source), table=table, reason=claim["unavailable"]))
                    continue
                ref = safe_read(claim["path"]); audit.record(ref)
                check_dir = out/f"compare_{index:02d}_{table}"
                rcall("compare", check_dir, [dest/(table+".csv"), ref, ",".join(claim["keys"])],
                      label=f"compare_{index:02d}_{table}")
                reproduction.extend(read(check_dir/"comparison.csv"))
        combined_claims = config.get("combined_references", {})
        if config["mode"] == "assessment" and set(combined_claims) != {"c100", "c050"}:
            raise ValueError("assessment requires both canonical combined-v7 reference sets")
        for sk, combined_spec in combined_claims.items():
            expected_version = "combined_v3_v7" if sk == "c100" else "combined_c050_v7"
            if combined_spec["version"] != expected_version:
                raise ValueError("canonical version must be explicit: "+expected_version)
            combined_dir = out/("reproduced_"+expected_version)
            rcall("combine", combined_dir, reproduced_runs[sk], label="combine_"+sk)
            if set(combined_spec["tables"]) != set(TABLES):
                raise ValueError("all 11 canonical combined tables must be declared")
            for table, claim in combined_spec["tables"].items():
                if "unavailable" in claim:
                    if not claim["unavailable"]: raise ValueError("reference gap needs a reason")
                    reference_gaps.append(dict(scope=expected_version, table=table, reason=claim["unavailable"]))
                    continue
                ref = safe_read(claim["path"]); audit.record(ref)
                if "run_id" not in claim["keys"]:
                    raise ValueError("combined comparison key must include run_id")
                check_dir = out/f"compare_combined_{sk}_{table}"
                rcall("compare", check_dir, [combined_dir/(table+".csv"), ref, ",".join(claim["keys"])],
                      label=f"compare_combined_{sk}_{table}")
                reproduction.extend(read(check_dir/"comparison.csv"))
        if not reproduction:
            raise ValueError("no explicit published table reproduction claims configured")
        # Reproduction agent supplies scored paths and canonical version labels explicitly.
        write(out/"published_reproduction.csv", reproduction)
        write(out/"published_reference_gaps.csv", reference_gaps, ["scope", "table", "reason"])
        write(out/"assessment_filter_checks.csv", selection_checks)
        smc_scales = set()
        for index, spec in enumerate(config["smc_sources"]):
            sk = spec["scale_key"]
            if sk not in {"c100", "c050"} or sk in smc_scales:
                raise ValueError("one SMC source per scale required")
            smc_scales.add(sk)
            results = safe_read(spec["results_dir"])
            # Explicit expected bundles only; never traverse truth or holdout trees.
            for c in cases.values():
                if c["scale_key"] != sk: continue
                bundle = results/f'p{int(c["p"]):04d}'/c["case_id"]
                if (bundle/"SMCBVS.csv").exists():
                    audit.record(safe_read(config["truth_dir"])/f'p{int(c["p"]):04d}'/(c["dataset_id"]+".rds"))
                for ext in ("csv", "rds", "sha256", "done"):
                    path = bundle/("SMCBVS."+ext)
                    if path.exists(): audit.record(path)
            dest = out/f"smc_{sk}"
            rcall("smc", dest, [results, out/"selected_inputs_manifest.csv", safe_read(config["truth_dir"]),
                                config["truth_manifest"], sk, config["mode"]], label=f"score_smc_{sk}")
            rows.extend(read(dest/"scored_rows.csv"))
            if (dest/"truth_signals.csv").exists():
                for s in read(dest/"truth_signals.csv"):
                    p = int(s["p"]); old = signals.setdefault(p, {}).get(s["signal"])
                    if old and any(float(old[k]) != float(s[k]) for k in ("index", "beta")):
                        raise ValueError("signal map differs across sources")
                    signals[p][s["signal"]] = s
        if smc_scales != {"c100", "c050"}:
            raise ValueError("both SMC scales must be explicitly supplied, even if every fit is missing")
        validate_rows(rows, cases)
        expected_benchmark = {(r["method_id"], r["rule_id"], r["scale_key"]) for r in registry}
        if config.get("additional_registry_csv"):
            audit.record(config["additional_registry_csv"])
            extra_registry = read(config["additional_registry_csv"])
            for reg in extra_registry:
                key = tuple(reg[k] for k in ("method_id", "rule_id", "scale_key"))
                if key in expected_benchmark or reg["method_id"] == "SMCBVS" or reg["scale_key"] not in {"c100", "c050"}:
                    raise ValueError("additional sensitivity registry conflicts with baseline")
                if not reg.get("label") or reg["role"] not in {"S0", "S1"}:
                    raise ValueError("sensitivity extension requires explicit label and role")
                expected_benchmark.add(key)
                registry.append(reg)
        actual_benchmark = {(r["method_id"], r["rule_id"], r["scale_key"]) for r in rows if r["method_id"] != "SMCBVS"}
        if actual_benchmark - expected_benchmark:
            # Long-chain sensitivities must be separate labelled sources, never replace baseline A3.
            raise ValueError("unregistered benchmark rule; extend reviewed registry before inclusion")
        for sk in ("c100", "c050"):
            for rule in ("hpm", "pip05"):
                registry.append(dict(method_id="SMCBVS", rule_id=rule, scale_key=sk,
                                     role="primary" if rule=="hpm" else "S0", label="v3 fixed method; binding lead ruling R-1"))
        write(out/"joined_scored_rows.csv", rows)
        write(out/"missing_rule_groups.csv", [dict(method_id=m, rule_id=r, scale_key=sk)
               for m,r,sk in sorted(expected_benchmark-actual_benchmark)], ["method_id", "rule_id", "scale_key"])
        signal_lists = {p: [items[k] for k in sorted(items)] for p,items in signals.items()}
        if any(len(signal_lists.get(p, [])) != 14 for p in (500, 1000)):
            raise ValueError("complete benchmark signal map required for T4")
        summaries, paired = build_tables(rows, cases, registry, out, signal_lists)
        figures(summaries, out)
        missing = sum(r["n_missing"] for r in summaries if r["scenario"] != "pooled")
        R = len(audit.state["assessment_selection"]["selector"]["replicate"])
        (out/"REPORT.md").write_text(
            f"# {'SYNTHETIC FIXTURE' if config['mode']=='synthetic' else f'PROVISIONAL {R}-replicate assessment'} analysis\n\n"
            "Unverified core units: run_pipeline.py; benchmark_adapter.R; r1_contract.R; native_contract.R. Independent Sol cell recount and Astra review remain required. "
            "Synthetic runs use a D-owned schema mock, not certification of A's updated adapter; final A-R1 integration remains pending.\n\n"
            f"Observed unique rule rows: {len(rows)}. Missing expected rule opportunities: {missing}. "
            f"Exactly {12*R} selected datasets / {24*R} paired-scale cases: replicates 1..{R}, S1..S6, p500/p1000. "
            f"Denominators are {R} per scenario cell and {6*R} per p/scale pooled; excluded replicates (if any) are not missing fits. "
            "See assessment_filter_checks.csv, selected_cases.csv, missing_rule_groups.csv and failure_summary.csv. "
            "All absent selected rows remain in denominators.\n\n"
            f"Published reproduction: {len(reproduction)} supplied reference tables compared after explicit key sort with R identical(), "
            f"including column types. Unavailable reference tables: {len(reference_gaps)}; see published_reference_gaps.csv. "
            "Regenerated tables without original references are not claimed independently reproduced. "
            "Byte equality is separate in published_reproduction.csv. Version names and paths are in manifest.json. "
            "Historical SUMMARY.md is not substituted for the supplied canonical version.\n\n"
            "Supplementary uncertainty uses sample variance / n. Scenario-pooled MCSE uses fixed scenario strata: "
            "sqrt(sum_h (n_h/N)^2 s_h^2/n_h). For conditional successful-only means, observed successful n_h fix the weights; "
            "pooled FP/FN and complete-success-pair MCSEs condition on observed successful stratum counts and do not include "
            "randomness of failure-driven mixture weights or selection. n<2 in a nonempty stratum gives NA. "
            "No pooling across scales. Paired differences are SMC minus comparator within the same case; FP/FN use complete-success pairs. "
            "Missing/failed rows are zero for exact/selection and unavailable for FP/FN. T4 group units are case selection proportions, "
            "with within-case dependence retained. Runtime p95 is type 7; median, p95 and max have no fabricated MCSE.\n\n"
            f"Replicates per cell: {R}. MCSE estimates are unstable at small n; zero observed sample variance "
            "and zero observed MCSE do not imply certainty or a zero population error rate.\n\n"
            "All registered and derived rules remain present, including completely absent groups. Long-chain sensitivity requires a separately "
            "reviewed registry extension and cannot overwrite A3 baseline. See CONTRACT.md for limitations and gate requirements.\n", encoding="utf-8")
        audit.state.update(status="completed_provisional", exit_status=0)
    except BaseException:
        audit.state.update(status="failed", exit_status=1, error=traceback.format_exc())
        raise
    finally:
        audit.state["finished_utc"] = utc()
        # Detect changing inputs/sources during the run, never silently claim an immutable snapshot.
        changed = [path for path, meta in audit.files.items() if not Path(path).exists() or sha(path) != meta["sha256"]]
        if changed:
            audit.state.update(status="failed_input_changed", exit_status=1, changed_inputs=changed)
        audit.save()
        active_error = sys.exc_info()[0] is not None
        try:
            outputs = [{"path": str(p.relative_to(out)), "sha256": sha(p), "bytes": p.stat().st_size}
                       for p in sorted(out.rglob("*")) if p.is_file() and p.name != "outputs_sha256.csv"]
            write(out/"outputs_sha256.csv", outputs)
        except Exception:
            audit.state.update(status="failed_output_audit",exit_status=1,output_audit_error=traceback.format_exc())
            audit.save()
            if not active_error: raise
        if changed:
            raise RuntimeError("inputs changed during analysis; audit manifest records paths")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True)
    run(parser.parse_args().config)
