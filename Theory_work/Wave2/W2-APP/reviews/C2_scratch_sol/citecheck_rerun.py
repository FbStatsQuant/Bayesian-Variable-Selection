from pathlib import Path
import builtins, runpy
app = Path('C:/Users/felip/Bayesian-Variable-Selection/Theory_work/Wave2/W2-APP')
saved_open = builtins.open
def redirected_open(file, mode='r', *args, **kwargs):
    if any(x in mode for x in 'wax+'):
        target = Path(file).resolve()
        if target == (app/'reviews/CITECHECK.txt').resolve():
            file = app/'reviews/C2_scratch_sol/CITECHECK_rerun.txt'
        else:
            raise RuntimeError(f'Unexpected write: {file}')
    return saved_open(file, mode, *args, **kwargs)
builtins.open=redirected_open
runpy.run_path(str(app/'citecheck.py'),run_name='__main__')
