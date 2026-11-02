"""Explicit expected unit and immutable study input for the shared R validator."""
from pathlib import Path

STUDY = Path("/projects/ml75/fb31/BVS/bench20261019")
CODE = Path("/home/fb31/projects/BVS/New_Campaign/code/bench_v2/F3_AdaptiveLasso")


def args_for(root, run_id, source, unit, study=STUDY, code=CODE):
    _, p, scenario, replicate, scale, dataset, input_kind = unit
    prefix = root / f"p{p:04d}" / f"{dataset}_{scale}" / "F3"
    tree = study / "dev" if input_kind == "dev" else study
    manifest = tree / "manifests" / ("dev_inputs_manifest.csv" if input_kind == "dev" else "inputs_manifest.csv")
    input_path = tree / "inputs" / f"p{p:04d}" / f"{dataset}.rds"
    return list(map(str, (prefix, source, input_path, manifest, code, run_id, dataset, p, scenario, replicate, scale)))
