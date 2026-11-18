# From Theory (2026-11-16): row 3.1's delivery idealisation IDEAL-W⁺ is about to become vacuous for real inputs

**Status.** The representability lemma T14 (W3-AUDIT track A, theory/W3-AUDIT; council XR2 PASS, Sol 9.4 / Opus 9.5,
bound) shows that the two code limits IDEAL-W⁺ lifts can never be reached on any input the software can receive. R stores
matrix dimensions as 32-bit integers, so n, p ≤ 2³¹ − 1, and then both limit checks are false. So **IDEAL-W⁺ costs
nothing on every input the software can receive.** It is proved, checked and **recorded** (registry W3-AUDIT-AX:REP, main 63144bc1, 11-16). The card change to row 3.1
(H5 card 16, AGREED) goes into the freeze via W3-READER's editorial round. Row 3.1 will read: "The delivery statement lifts
two integer limits of the code (IDEAL-W⁺); in the default configuration neither can be reached on any input R can
represent (n, p_raw ≤ 2³¹ − 1), so this matters only for the n → ∞ form." Use p_raw, not p.

**How to write it now.** In the assumptions section, you may say that row 3.1's delivery idealisation IDEAL-W⁺ "holds
automatically for every input the software accepts (n, p ≤ 2³¹ − 1); this will be stated in the next revision". Don't
present it as a live restriction. Until the card changes, keep the statement of row 3.1 as recorded (with IDEAL-W⁺), and
don't write "IDEAL-W⁺ = IDEAL-W": on an idealised machine with unbounded integers the two still differ, but no real input
gets there.
