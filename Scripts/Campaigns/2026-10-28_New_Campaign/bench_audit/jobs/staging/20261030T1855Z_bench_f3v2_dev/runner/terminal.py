"""A job is absent only when a successful squeue query proves it."""
import re
import subprocess


def assert_absent(job):
    if not re.fullmatch(r"\d+", job):
        raise ValueError("invalid job id")
    result = subprocess.run(["squeue", "-h", "-r", "-u", "fb31", "-o", "%i"],
                            capture_output=True, text=True, check=True)
    for line in result.stdout.splitlines():
        ident = line.strip()
        if not re.fullmatch(r"\d+(?:_(?:\d+|\[[0-9,:\-%]+\]))?", ident):
            raise ValueError("unparseable squeue id")
        if ident.split("_", 1)[0] == job:
            raise ValueError("job queued or running: " + job)
