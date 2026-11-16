# S3 — method-pin sweep: 17 every-n shipped-code delivery claims SUSPECT (correctness event, HQ 11-16)

Note on each: every-n delivery; shipped validators `le ≤ 10⁶` (v3_run.R:96) / `ℓ+|S̃₀| ≤ INT_MAX` (v3_core.cpp:474) not covered by IDEAL-W

Same correctness event as W2-UNI:F-UNI (task S1, issues/2026-11-16_suspect_W2-UNI_F-UNI). Batch NARROW (A:IDEAL-W⁺ or (D)) follows as task S4, after F-UNI's S2.

Suspected (one sub-folder each, propagate's impact report):
- W2-LOC2:F-LOC2
- W2-FAC-S5:Thm-FAC-BCS-R
- W2-FAC-S5:L5
- W2-FAC-X:Thm-FAC-CS-iid
- W2-FAC-X:Thm-FAC-GL
- W2-FAC-A:Thm-FAC-L
- W2-LOC2:F-LOC2.exp
- W2-LOC2:F-LOC2.poly
- W2-FAC-S5:L5.C4-R
- W2-FAC-X:X10
- W2-FAC-A:Prop-F-FAC
- W2-FAC-B:Thm-FAC-CS
- W2-FAC-PK:Thm-FAC-PK
- HQ_AUDIT-W1C:A3
- W2-FAC-B:L5
- W2-FAC-XA:X4
- HQ_AUDIT-W1C:A2

Cascade (dependents the tool marked SUSPECT): 15
- HQ_AUDIT-W2:B1
- HQ_AUDIT-W2:B3
- HQ_AUDIT-W2:B4
- W2-APP:Family-map
- W2-APP:Thm-APP
- W2-FAC-B:Thm-FAC-CS(C1-M)
- W2-FAC-S5:KL
- W2-FAC-S5:L5.C3-R
- W2-FAC-X:Cor-FAC-NCS
- W2-FAC-X:X6
- W2-FAC-X:X6.X6.3
- W2-FAC-X:X6.X6.4
- W2-FAC-X:X7
- W2-FAC-X:X8
- W2-FAC-X:X9

Already SUSPECT dependents (F-UNI event): W2-FAC-S5F:C4, W2-UNI:F-UNI, W2-UNI:UNI-0, W2-UNI:UNI-1, W3-RM:Examples, W3-RM:RM-R, W3-RM:SAND-R, W3-RM:SAND-Rp

