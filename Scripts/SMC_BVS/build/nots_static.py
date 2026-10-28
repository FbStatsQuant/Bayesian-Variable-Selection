"""Local static/gate checks ONLY. subprocess.run is mocked; no SSH or R runs."""
import ast
from contextlib import redirect_stdout
from datetime import datetime, timezone
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
from unittest.mock import patch

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent


def main():
    syntax = []
    for path in sorted(HERE.glob("nots*.py")):
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        syntax.append(path.name)
    embedded = []
    for path in sorted(HERE.glob("nots*.sh")):
        lines = path.read_text(encoding="utf-8").splitlines()
        start = None
        for n, line in enumerate(lines):
            if "<<'PY'" in line:
                start = n + 1
            elif line == "PY" and start is not None:
                ast.parse("\n".join(lines[start:n]) + "\n", filename=f"{path.name}:{start+1}")
                embedded.append(f"{path.name}:{start+1}")
                start = None
        assert start is None, "Unterminated Python heredoc"
    spec = importlib.util.spec_from_file_location("nots_launcher_for_static", HERE / "nots_launch.py")
    launch = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(launch)
    real_read_bytes, real_read_text = Path.read_bytes, Path.read_text
    status = HERE.parents[1] / "STATUS.md"
    checked = []
    with tempfile.TemporaryDirectory(prefix="nots_static_", dir=HERE) as tmp:
        root = Path(tmp)
        deps = root / "deps.json"
        deps.write_text(json.dumps(dict(Rcpp="1.1.2", digest="0.6.39", jsonlite="2.0.0")))
        args = ["nots_launch.py", "observe", "--run", "static_only", "--evidence", str(root / "evidence"),
                "--module-init", "/explicit/module-init.sh", "--r-library", "/explicit/R/4.5.2",
                "--deps", str(deps), "--account", "explicit", "--partition", "explicit",
                "--cluster", "explicit", "--time", "00:10:00", "--mem-mb", "2048"]

        def run_case(label, initial, latest=None, allow=False):
            def read_bytes(path):
                return initial.encode() if path == status else real_read_bytes(path)
            def read_text(path, *a, **kw):
                if path == status:
                    return initial if latest is None else latest
                return real_read_text(path, *a, **kw)
            # Any accidental network path hits this mock, never a real process.
            with patch.object(sys, "argv", args), patch.object(Path, "read_bytes", read_bytes), \
                 patch.object(Path, "read_text", read_text), patch.object(launch.subprocess, "run", return_value=SimpleNamespace(returncode=0)) as mocked:
                error = None
                try:
                    with redirect_stdout(io.StringIO()):
                        launch.main()
                except SystemExit as exc:
                    error = str(exc)
                if allow:
                    assert error is None and mocked.call_count == 1
                    call = mocked.call_args.args[0]
                    assert call[0] == "ssh" and call.count("nots") == 1
                else:
                    assert error and "no network attempted" in error.lower(), error
                    assert mocked.call_count == 0
                checked.append(dict(case=label, pass_=True, network_calls=0, mocked_ssh_calls=mocked.call_count))
        for label, text in [
            ("empty", ""), ("current_negative", "NOTS: route repaired; Not yet open for runs.\n"),
            ("quoted", '> NOTS: open for runs\n'), ("inline", 'Until "NOTS: open for runs" appears\n'),
            ("suffix", "NOTS: open for runs later\n"), ("trailing_space", "NOTS: open for runs \n"),
            ("lowercase", "nots: open for runs\n"), ("leading_space", " NOTS: open for runs\n")]:
            run_case(label, text)
        with patch.object(launch, "__file__", str(HERE.parent / "snapshots/v1_r1/build/nots_launch.py")):
            run_case("frozen_launcher_uses_lead_gate", "NOTS: closed\n")
        run_case("gate_reclosed_before_ssh", "NOTS: open for runs\n", latest="NOTS: closed\n")
        # Reclosed case created evidence before its second gate; use another new path.
        args[args.index("--evidence") + 1] = str(root / "affirmative")
        run_case("exact_affirmative_CRLF", "# status\r\nNOTS: open for runs\r\n", allow=True)
    report = dict(status="PASS", numerical_runs=0, actual_network_calls=0,
                          utc=datetime.now(timezone.utc).isoformat(),
                          python_syntax=syntax, embedded_python_syntax=embedded,
                          gate_checks=checked, shell_syntax="NOT RUN; parent to check on Owls",
                          R_syntax="NOT RUN; parent to check on Owls",
                          source_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                              for p in sorted(HERE.glob('nots*')) if p.is_file() and p.suffix in {'.py','.sh','.R'}})
    data = json.dumps(report, indent=2) + '\n'
    (HERE / 'nots_static_evidence.json').write_text(data, encoding='utf-8')
    print(data)


if __name__ == "__main__":
    main()
