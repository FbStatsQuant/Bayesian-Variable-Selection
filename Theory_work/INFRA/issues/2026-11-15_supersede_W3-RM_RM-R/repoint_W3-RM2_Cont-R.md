# Cheap check: re-point W3-RM2:Cont-R from W3-RM:RM-R to W3-RM2:RM2-R

W3-RM2:RM2-R implies W3-RM:RM-R (registry `implies`). Confirm that what W3-RM2:Cont-R uses (`stmt`) survives in W3-RM2:RM2-R (same event/rate/constants), then run `propagate.py confirm-repoint W3-RM2:Cont-R --from W3-RM:RM-R --to W3-RM2:RM2-R --checked-by <who/file>`; otherwise `reject-repoint` (the dependent simply stays on W3-RM:RM-R, which remains valid).
