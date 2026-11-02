"""Conservative aggregate throttle for all fb31 arrays; unknown formats fail closed."""
import re
import subprocess


def count(text):
    jobs = {}
    for line in text.splitlines():
        parts = line.split("|")
        if len(parts) != 3:
            raise ValueError("unparseable squeue row")
        ident = parts[0].strip()
        if "_" not in ident:
            if not ident.isdigit():
                raise ValueError("unparseable squeue job")
            continue
        base, suffix = ident.split("_", 1)
        if not base.isdigit():
            raise ValueError("unparseable squeue array")
        state = jobs.setdefault(base, [0, 0])
        if suffix.isdigit():
            state[0] += 1
        else:
            m = re.fullmatch(r"\[[0-9,:-]+(?:%([0-9]+))?\]", suffix)
            if not m:
                raise ValueError("unparseable squeue array range")
            state[1] = max(state[1], int(m[1]) if m[1] else 100000)
    return sum(max(v) for v in jobs.values())


def check(requested):
    proc = subprocess.run(["squeue", "-h", "-u", "fb31", "-o", "%i|%j|%T"],
                          capture_output=True, text=True, check=True)
    current = count(proc.stdout)
    if current + requested > 100:
        raise ValueError(f"array throttle ceiling: other arrays {current} + requested {requested} > 100")
    return proc.stdout
