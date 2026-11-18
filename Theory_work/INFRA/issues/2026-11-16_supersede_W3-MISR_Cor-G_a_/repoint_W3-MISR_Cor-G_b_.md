# Cheap check: re-point W3-MISR:Cor-G(b) from W3-MISR:Cor-G(a) to W3-MISR-R:CorG-min

W3-MISR-R:CorG-min implies W3-MISR:Cor-G(a) (registry `implies`). Confirm that what W3-MISR:Cor-G(b) uses (`stmt`) survives in W3-MISR-R:CorG-min (same event/rate/constants), then run `propagate.py confirm-repoint W3-MISR:Cor-G(b) --from W3-MISR:Cor-G(a) --to W3-MISR-R:CorG-min --checked-by <who/file>`; otherwise `reject-repoint` (the dependent simply stays on W3-MISR:Cor-G(a), which remains valid).
