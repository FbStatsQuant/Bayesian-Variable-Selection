# MANIFEST_R2.txt = copy of MANIFEST_C2.txt (HQ recorder, 2026-11-15)

`MANIFEST_R2.txt` is a byte copy of `MANIFEST_C2.txt` (digest 96fd83cf3564e3f4a0ff5b98295c79a55868d9192e6987e9d40e936e5ad9541a).
The diff round was frozen as "C2", but both seats' verdict lines say `round=R2` and the CP3 tooling looks for the council
digest in `reviews/MANIFEST_*.txt` by its header, with the round named R<k>; both files are kept so the round's own name
(C2, the diff round after C1) and the tooling's name (R2) both resolve. Extra inputs of the round:
`INPUTS_C2.txt` (renamed from MANIFEST_C2_extra.txt: a `MANIFEST_*.txt` name is read as a manifest by the CP3 tooling and R06). The C1 state the diff was taken against was reconstructed (no C1 manifest or snapshot
existed); it is not pinned. The R2 seats read the full current files plus the diff (`C2_DIFF.md`, `C2_diff.patch`,
`C2_DEPENDENTS.md`).
