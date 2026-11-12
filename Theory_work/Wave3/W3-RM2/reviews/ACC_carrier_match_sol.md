# ACC carrier transcription check

Compared the frozen REPORT.md:153-236 with W3-RM2_accept.md under all five permitted HQ differences. Statement and premise line spans below refer to the frozen STATEMENT.md unless another file is named. Shared C3 preamble spans are the contextual premises explicitly identified in the carrier header.

| claim | verdict | finding |
|---|---|---|
| W3-RM2:RM2-F | MATCH | C1:206-214; premises 47-95, 126-171, allowed 290-312; assumptions, consumes, implies, sharpness, binding, conclusion/rate/scope verbatim; dependencies and amended gates match; SOP condition and checkpoint line 12 match. |
| W3-RM2:RM2-R | MATCH | C2:216-218; premises 47-95, 172-202, allowed 290-312; assumptions, consumes, implies, sharpness, binding, conclusion/rate/scope verbatim; dependencies and amended gates match; POST condition and checkpoint line 13 match. |
| W3-RM2:Toolkit-b | MATCH | P0 bridge row 247; premise section 1:47-95; kind/dependencies match; checkpoint line 14 and R1 council cell match. |
| W3-RM2:SAND-F-b | MATCH | P1 bridge row 248; premises section 1 and section 3.1:126-171; kind/dependencies match; checkpoint line 15 and R1 council cell match. |
| W3-RM2:TL-F-b | MATCH | P2 bridge row 249; premises section 1 and section 3.1; kind/dependencies match; checkpoint line 16 and R1 council cell match. |
| W3-RM2:NA-W | MATCH | C3(a):223-225; section 1/3.1 premises and shared C3 preamble 220-222 correctly resolved; kind/dependencies match; checkpoint line 17 and R1 council cell match. |
| W3-RM2:W-conv | MATCH | C3(b):226-230, including the parenthetical special case; section 1/3.1 premises and shared C3 preamble 220-222 correctly resolved; kind/dependencies match; checkpoint line 18 and R1 council cell match. |
| W3-RM2:W-suff | MATCH | C3(c):231-234; section 1/3.1 premises and shared C3 preamble 220-222 correctly resolved; assumptions and assumption-level implies verbatim in notes; kind/dependencies match; checkpoint line 19 and R1 council cell match. |
| W3-RM2:Cont-F | MATCH | C4:236-240 is the whole referenced containment claim; premise section 3.1; kind/dependencies match; propagated SOP condition, checkpoint line 20 and R1 council cell match. |
| W3-RM2:SAND-R-b | MATCH | P7 bridge row 254; premises section 1/3.2; kind/dependencies match after permitted template-edge removal and use-label hyphenation. Template note is supported by L4_sandR_b.md:12 (proof re-run; no conclusion used as input); checkpoint line 21 and R1 council cell match. |
| W3-RM2:F-to-R | MATCH | P8 bridge row 255; premises section 1/3.2; kind/dependencies match; checkpoint line 22 and R1 council cell match. |
| W3-RM2:D-to-W | MATCH | P9 bridge row 256; premises section 1/3.2; assumptions and bracket note verbatim. Both permitted template edges are retained in notes only. L5_formR.md:108-117 states and proves D-loc^b; L2_NAR.md:79-85 supplies adaptive atom-tail computations and 102-105 the threshold expansion as claimed. Kind and empty consumption dependencies match; checkpoint line 23 and R1 council cell match. |
| W3-RM2:POST-R | MATCH | P10 bridge row 257; premises section 1/3.2 plus allowed section 5:290-312; kind and POST@hyp dependency match; POST condition, checkpoint line 24 and R1 council cell match. |
| W3-RM2:Cont-R | MATCH | C4:236-240 is the whole referenced containment claim; premise section 3.2; kind/dependencies match with permitted use-label hyphenation; propagated POST condition, checkpoint line 25 and R1 council cell match. |
| W3-RM2:Ex-PolyR | MATCH | C5:259-275; E2 premise is exactly its section 164-263; kind/dependencies match; POST/BC/IR conditions and versions match; unchecked status exactly matches checkpoint line 26; no council field upgrading it. |
| W3-RM2:Ex-PolyF | MATCH | C5:259-275; E3 premise is exactly its section 264-329; kind/dependencies match; SOP/BC/IR conditions and versions match; unchecked status exactly matches checkpoint line 27; no council field upgrading it. |
| W3-RM2:Ex-Proxy | MATCH | C5:259-275; E4 premise is exactly its section 330-384; kind/dependencies match; SOP condition, checkpoint line 28 and R1 council cell match. |
| W3-RM2:Ex-Equi | MATCH | C5:259-275; E5 premise is exactly its section 385-474, stopping before the examples table; kind/dependencies match; SOP condition, checkpoint line 29 and R1 council cell match. |

Claim inventory: exactly 18 source claims and 18 carrier claims; none missing, added, or duplicated. All 18 status strings equal the cited CHECKPOINT_4.md line exactly after removing its trailing claim identifier: 16 PROVED-CHECKED with the specified R1 cell, two unchecked examples. All transferred source note payloads and both conclusion/rate/scope payloads were checked as exact text; dependency differences are precisely the permitted template removals and hyphenated use labels. The carrier-resolved STATEMENT.md and L6_examples.md are byte-identical to the frozen copies. The cited L4/L5 note spans also agree in the resolved carrier tree.

ACC-VERDICT: ALL-MATCH
