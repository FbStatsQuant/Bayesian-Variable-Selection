"""Write the unit and chunk tables of one run (Python 3 standard library only).

Units are keyed by dataset ID; seeds follow master section II.7 and are listed here for
audit only (the adapter derives and cross-checks them itself from the ID and the manifest):
    data seed   = base(p) + 10000 * scenario + replicate,  base = 1410000 (p=500), 1510000 (p=1000)
                  (development: 2410000, 2510000)
    method seed = data seed + 4000000
One array task = one dataset, running c100 then c050. Production orders p=1000 first (longest
tasks first, short tail) and cycles S1..S6 within each replicate, so every scenario is seen early.

    python make_tables.py production OUT_DIR
    python make_tables.py production_p OUT_DIR P              (one array per p: 500 or 1000)
    python make_tables.py list OUT_DIR DATASET[:SCALES] ...   (e.g. dev_p0500_S4_r001:c100)
"""
import sys
from pathlib import Path

BASE = {(False, 500): 1410000, (False, 1000): 1510000, (True, 500): 2410000, (True, 1000): 2510000}


def parse(dataset):
    dev = dataset.startswith("dev_")
    core = dataset[4:] if dev else dataset
    p_part, s_part, r_part = core.split("_")
    p, s, r = int(p_part[1:]), int(s_part[1:]), int(r_part[1:])
    assert p in (500, 1000) and 1 <= s <= 6 and 1 <= r <= 100, dataset
    assert dataset == ("dev_" if dev else "") + "p%04d_S%d_r%03d" % (p, s, r), dataset
    return dev, p, s, r


def write(out, chunks):
    out.mkdir(parents=True, exist_ok=True)
    units = ["case_id\tdataset_id\tp\tscenario\treplicate\tscale\tdata_seed\tmethod_seed\ttask"]
    rows = ["task\tdataset\tp\tscales"]
    for task, (dataset, scales) in enumerate(chunks, start=1):
        dev, p, s, r = parse(dataset)
        data_seed = BASE[(dev, p)] + 10000 * s + r
        rows.append("%d\t%s\t%d\t%s" % (task, dataset, p, ",".join(scales)))
        for scale in scales:
            assert scale in ("c100", "c050")
            units.append("%s_%s\t%s\t%d\t%d\t%d\t%s\t%d\t%d\t%d" % (
                dataset, scale, dataset, p, s, r, scale, data_seed, data_seed + 4000000, task))
    for name, lines in (("chunks.tsv", rows), ("units.tsv", units)):   # open(): Python 3.9-safe
        with open(out / name, "w", encoding="ascii", newline="\n") as f:
            f.write("\n".join(lines) + "\n")
    print("tasks", len(rows) - 1, "units", len(units) - 1, "->", out)


def main():
    mode, out = sys.argv[1], Path(sys.argv[2])
    if mode == "production":
        chunks = [("p%04d_S%d_r%03d" % (p, s, r), ("c100", "c050"))
                  for p in (1000, 500) for r in range(1, 101) for s in range(1, 7)]
        assert len(chunks) == 1200 and len(set(c[0] for c in chunks)) == 1200
    elif mode == "production_p":
        # GO_2400 C1: one array per p (tasks renumbered 1..600), same order as "production".
        p = int(sys.argv[3])
        assert p in (500, 1000)
        chunks = [("p%04d_S%d_r%03d" % (p, s, r), ("c100", "c050")) for r in range(1, 101) for s in range(1, 7)]
        assert len(chunks) == 600
    elif mode == "list":
        chunks = []
        for item in sys.argv[3:]:
            dataset, _, scales = item.partition(":")
            chunks.append((dataset, tuple(scales.split(",")) if scales else ("c100", "c050")))
    else:
        raise SystemExit(__doc__)
    write(out, chunks)


if __name__ == "__main__":
    main()
