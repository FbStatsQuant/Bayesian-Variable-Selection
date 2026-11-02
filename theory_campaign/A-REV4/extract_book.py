import subprocess,pathlib
p=pathlib.Path('theory_campaign/A-REV4/book_reproduction.py')
p.write_bytes(subprocess.check_output(['git','show','origin/theory/W2-BOOK:theory_campaign/W2-BOOK/scripts/frozen_run_exact.py']))
