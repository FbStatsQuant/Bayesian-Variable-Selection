# Cheap check: re-point W3-RM2:Cont-F from W3-RM:RM-F to W3-RM2:RM2-F

W3-RM2:RM2-F implies W3-RM:RM-F (registry `implies`). Confirm that what W3-RM2:Cont-F uses (`stmt`) survives in W3-RM2:RM2-F (same event/rate/constants), then run `propagate.py confirm-repoint W3-RM2:Cont-F --from W3-RM:RM-F --to W3-RM2:RM2-F --checked-by <who/file>`; otherwise `reject-repoint` (the dependent simply stays on W3-RM:RM-F, which remains valid).
