
### exp2_p500.json  (72 datasets)

| scen | c | S0 locmax | S0 beaten by | median best del gain at S0 | median best add gain at S0 | d0 frac progress | centres: PD | reached | reached given PD | all-progress given reached | max moves |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.5 | 0.83 | {'del_truth': 1} | -5.9 | -1.8 | 0.730 | 0.99 | 0.83 | 0.84 | 0.99 | 3 |
| 1 | 1.0 | 1.00 | {} | -35.8 | -2.3 | 0.990 | 1.00 | 1.00 | 1.00 | 1.00 | 2 |
| 2 | 0.5 | 0.83 | {'del_truth': 1} | -3.7 | -2.1 | 0.694 | 0.99 | 0.83 | 0.84 | 0.98 | 3 |
| 2 | 1.0 | 0.83 | {'add_null': 1} | -32.0 | -0.9 | 0.989 | 1.00 | 0.83 | 0.83 | 1.00 | 2 |
| 3 | 0.5 | 0.83 | {'swap_truth->null': 1} | -7.7 | -1.4 | 0.889 | 1.00 | 0.83 | 0.83 | 0.98 | 3 |
| 3 | 1.0 | 1.00 | {} | -31.9 | -2.7 | 0.975 | 1.00 | 1.00 | 1.00 | 1.00 | 3 |
| 4 | 0.5 | 0.50 | {'swap_truth->null': 3} | -3.2 | -2.9 | 0.663 | 1.00 | 0.50 | 0.50 | 0.95 | 3 |
| 4 | 1.0 | 1.00 | {} | -34.7 | -1.5 | 1.000 | 1.00 | 1.00 | 1.00 | 1.00 | 3 |
| 5 | 0.5 | 0.33 | {'swap_truth->null': 2, 'add_null': 1, 'del_truth': 1} | -0.7 | -2.6 | 0.402 | 0.99 | 0.33 | 0.34 | 0.93 | 3 |
| 5 | 1.0 | 1.00 | {} | -27.3 | -2.4 | 0.971 | 1.00 | 1.00 | 1.00 | 1.00 | 2 |
| 6 | 0.5 | 0.50 | {'swap_truth->null': 3} | -1.8 | -1.5 | 0.546 | 1.00 | 0.50 | 0.50 | 0.98 | 3 |
| 6 | 1.0 | 1.00 | {} | -35.6 | -1.1 | 0.998 | 1.00 | 1.00 | 1.00 | 1.00 | 2 |

all centres: 1440; PD 0.998; reached 0.806
datasets with S0 local max: 58/72; their centres reached S0: 1.000; all-progress among reached 0.990
  not reached although S0 local max: 0; their PD: []; end (m,e,gain): []
move classes used on successful paths: {'add_truth': 584, 'swap_extra->truth': 1156, 'del_extra': 236, 'swap_truth->truth': 11, 'swap_null->null': 1}
move classes used on failed paths: {'swap_truth->truth': 47, 'swap_extra->truth': 255, 'del_truth': 65, 'del_extra': 54, 'add_truth': 85, 'add_null': 45, 'swap_null->null': 24, 'swap_truth->null': 157}
greedy move classes at the 105 d=0 states (m<=2), summed: {'add_truth': 6204, 'swap_truth->truth': 1286, 'local_max': 3, 'add_null': 42, 'swap_truth->null': 19, 'del_truth': 6}
posterior-miss margin lower bounds F(S*)-F(S0) when S0 not local max: median 1.30, range [0.20, 4.78]; S* (m,e): [(1, 0), (0, 1), (1, 0), (1, 1), (2, 2), (2, 1), (1, 1), (1, 1), (1, 1), (0, 1), (1, 0), (1, 1), (1, 1), (1, 1)]
