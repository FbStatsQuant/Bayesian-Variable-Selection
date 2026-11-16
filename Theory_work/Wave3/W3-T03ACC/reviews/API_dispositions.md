# W3-T03ACC — dispositions of HQ's blind API Fable audit (v4 H3: proof material, not a review layer)

Inputs: `api/t03acc-1.md`, `api/t03acc-2.md`, `api/VERDICTS.tsv` (also on main: `Theory_work/Wave3/API_AUDIT/t03acc/`).
Both samples: `AUDIT SOP:TH09 VERDICT=MINOR FINDINGS=0`, no GAP or ERROR ("the theorem is proved as stated"). Line numbers
in the audits match `sources/W1-T03R/PROOF.md` (checked: :79 = T02(i♯), :168 = conclusions, :172 = (C1)).
Never given to the blind council seats. Each slip goes to a Sol line-check batch as a **named point to check**; final
disposition after that batch.

| # | sample(s) | location | slip (summary) | lead's reading | goes to | disposition |
|---|---|---|---|---|---|---|
| A1 | 1, 2 | `PROOF.md:9` | "for p = 1 every statement below is trivial or void" is inaccurate for T03♯ (p = 1, s₀ = 1 is a real case); E1(b)/E2 divide by p − 1 | same point as STATEMENT §4 item 4 (raised before the audit arrived). Proposed repair (both samples): for p = 1, K = 1 and m♯_n ≤ K = 1 ≤ C_m log n directly; nothing else needs p ≥ 2 | LC-A (E1, E2(i)) and LC-B ((C1)) | pending LC-A/LC-B |
| A2 | 1 | `PROOF.md:172` with `:50`, `:59` | (C1) cites E2(i) without its side condition n ≥ 5 when s₀ = 0 | moot for the statement (s₀ ≥ 1, STATEMENT §4 item 1); otherwise absorbed in n ≥ n₀ | LC-B ((C1)) | pending LC-B |
| A3 | 2 | `PROOF.md:79-80` with `:16` | R_m written as Σ_{k=m+1}^K q_k/w(s₀) "for every integer m", but q_k is defined only for k ≥ 0; for m < 0 read as ϖ(Ω)/ϖ(S₀) | the record's definition uses max(m+1, 0) (STATEMENT §2), which is that reading; sup over m unaffected | LC-A (T02(i♯)) | pending LC-A |
| A4 | 2 | `PROOF.md:168` | J_n^∞ written without "j ∈ S₀" | harmless: θ*_j = 0 off S₀ and the threshold is positive. STATEMENT §3 clause 4 copies the record verbatim (also without "j ∈ S₀"); candidate E-level wording fix for ERRATA | LC-C ((C10), Assembly (iv)) | pending LC-C |

Use in CHECKPOINT_3: supporting evidence only.
