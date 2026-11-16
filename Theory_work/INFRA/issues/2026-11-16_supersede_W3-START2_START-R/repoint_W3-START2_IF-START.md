# Cheap check: re-point W3-START2:IF-START from W3-START2:START-R to W3-START2-R:START-R

W3-START2-R:START-R implies W3-START2:START-R (registry `implies`). Confirm that what W3-START2:IF-START uses (`proof`) survives in W3-START2-R:START-R (same event/rate/constants), then run `propagate.py confirm-repoint W3-START2:IF-START --from W3-START2:START-R --to W3-START2-R:START-R --checked-by <who/file>`; otherwise `reject-repoint` (the dependent simply stays on W3-START2:START-R, which remains valid).
