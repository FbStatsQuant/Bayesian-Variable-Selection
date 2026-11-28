| id | part (A/B/C/D) | manuscript file:line | what it says | what the source says (file:line or page) | severity |
|---|---|---|---|---|---|
| A4-E1 | C | `Docs/Writing/manuscript/sections/appendices.tex:71` | The pilot step floor is `$1/T_i$`, although the step-ceiling row at excerpt line 68 renames that quantity to `$\Tmax_i$` (rendered as $T_i^{\max}$). One occurrence missed the intended symbol rename; write `$1/\Tmax_i$`. The numerical rule is unchanged. | `Scripts/SMC_BVS/core/cpp/v3_calib.h:38–43` uses `1.0 / Te`, where `Te` is the tier's step ceiling; `Scripts/SMC_BVS/core/v3_preprocess.R:27–30` supplies that ceiling. D1, `Docs/Writing/methodology/smc_bvs_method.tex:637–640`, calls the ceiling $T_i$ and consequently writes $1/T_i$. | E |

FIDELITY: FAITHFUL — C=0, S=0, F=0, E=1.
