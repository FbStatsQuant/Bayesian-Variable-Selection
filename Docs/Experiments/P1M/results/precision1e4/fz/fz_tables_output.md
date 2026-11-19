## per-fit quantities (R'=64; engine eval record; targets M1<=0.05, M2<=0.005, M3<=0.5)
| fit | wave | M1 | M2 | M3 (robust) | HPM = S0 | occ_inhom | logZ - logZ_occ (3 se bound) | T | I_used | grid_unconv |
|---|---|---|---|---|---|---|---|---|---|---|
| ADJOPP-m1-I0-c1-s1 | P4 | 0.0155 | 0.00036 | 0.0217 (0.0190) | True | False | +0.0021 (0.0100) ok | 19 | 0 | True |
| ADJOPP-m1-I0-c2-s1 | P4 | 0.0154 | 0.00039 | 0.0252 (0.0252) | True | False | -0.0090 (0.0111) ok | 17 | 0 | True |
| AR-m1-I0-c1-s1 | A0 | 0.0129 | 0.00044 | 0.0242 (0.0230) | True | False | -0.0019 (0.0103) ok | 23 | 0 | True |
| AR-m1-I0-c2-s1 | P1 | 0.0138 | 0.00043 | 0.0235 (0.0241) | True | False | -0.0004 (0.0102) ok | 23 | 0 | True |
| ARweak-m1-I0-c1-s1 | P3 | 0.0118 | 0.00044 | 0.0180 (0.0154) | False | False | +0.0011 (0.0081) ok | 9 | 0 | True |
| ARweak-m1-I0-c2-s1 | P3 | 0.0115 | 0.00052 | 0.0211 (0.0230) | False | False | -0.0038 (0.0090) ok | 10 | 0 | True |
| ADJOPP-m1-c1-s1 | P3 | 0.0165 | 0.00036 | 0.0209 (0.0221) | True | False | -0.0010 (0.0100) ok | 21 | 3 | True |
| ADJOPP-m1-c2-s1 | P3 | 0.0142 | 0.00043 | 0.0215 (0.0203) | True | False | +0.0011 (0.0097) ok | 17 | 3 | True |
| AR-m1-c1-s1 | P1 | 0.0128 | 0.00052 | 0.0207 (0.0230) | True | False | -0.0011 (0.0091) ok | 20 | 3 | True |
| AR-m1-c2-s1 | P1 | 0.0138 | 0.00044 | 0.0215 (0.0205) | True | False | -0.0040 (0.0096) ok | 21 | 3 | True |
| ARweak-m1-c1-s1 | P2 | 0.0131 | 0.00046 | 0.0176 (0.0180) | False | False | -0.0001 (0.0082) ok | 9 | 3 | True |
| ARweak-m1-c2-s1 | P2 | 0.0127 | 0.00055 | 0.0162 (0.0144) | False | False | +0.0037 (0.0077) ok | 12 | 3 | True |
| ADJOPP-mc1-s1 | P4 | 0.0145 | 0.00039 | 0.0100 (0.0100) | True | False | +0.0043 (0.0066) ok | 64 | 3 | True |
| ADJOPP-mc2-s1 | P4 | 0.0144 | 0.00039 | 0.0108 (0.0113) | True | False | +0.0018 (0.0068) ok | 68 | 3 | True |
| AR-mc1-s1 | A0 | 0.0162 | 0.00054 | 0.0122 (0.0121) | True | False | -0.0012 (0.0076) ok | 84 | 3 | True |
| AR-mc2-s1 | P1 | 0.0138 | 0.00049 | 0.0122 (0.0121) | True | False | +0.0008 (0.0069) ok | 80 | 3 | True |
| ARweak-mc1-s1 | P2 | 0.0123 | 0.00052 | 0.0095 (0.0076) | False | False | -0.0014 (0.0058) ok | 44 | 3 | True |
| ARweak-mc2-s1 | P2 | 0.0124 | 0.00056 | 0.0093 (0.0090) | False | False | -0.0034 (0.0058) ok | 48 | 3 | True |

## cost per fit vs the committed class model (billed core-h; setup / calibrate / islands(64) / merge / eval)
| fit | total | x model E | setup | calib | islands | merge | eval | soft | hard | verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| ADJOPP-m1-I0-c1-s1 | 5.510 | 0.96 | 0.031 | 0.120 | 5.186 | 0.147 | 0.027 | 8.6 | 14.4 | ok |
| ADJOPP-m1-I0-c2-s1 | 5.417 | 0.94 | 0.029 | 0.076 | 5.161 | 0.113 | 0.038 | 8.6 | 14.4 | ok |
| AR-m1-I0-c1-s1 | 5.545 | 0.96 | 0.033 | 0.107 | 5.188 | 0.184 | 0.033 | 8.6 | 14.4 | ok |
| AR-m1-I0-c2-s1 | 5.337 | 0.93 | 0.029 | 0.080 | 5.041 | 0.144 | 0.042 | 8.6 | 14.4 | ok |
| ARweak-m1-I0-c1-s1 | 4.087 | 0.71 | 0.031 | 0.098 | 3.807 | 0.122 | 0.029 | 8.6 | 14.4 | ok |
| ARweak-m1-I0-c2-s1 | 4.131 | 0.72 | 0.027 | 0.071 | 3.880 | 0.127 | 0.027 | 8.6 | 14.4 | ok |
| ADJOPP-m1-c1-s1 | 7.237 | 1.15 | 0.027 | 1.182 | 5.874 | 0.122 | 0.031 | 9.4 | 15.7 | ok |
| ADJOPP-m1-c2-s1 | 6.141 | 0.98 | 0.027 | 0.782 | 5.172 | 0.129 | 0.031 | 9.4 | 15.7 | ok |
| AR-m1-c1-s1 | 5.716 | 0.91 | 0.033 | 0.636 | 4.840 | 0.171 | 0.036 | 9.4 | 15.7 | ok |
| AR-m1-c2-s1 | 6.137 | 0.98 | 0.029 | 0.622 | 5.217 | 0.233 | 0.036 | 9.4 | 15.7 | ok |
| ARweak-m1-c1-s1 | 5.008 | 0.80 | 0.027 | 0.889 | 3.928 | 0.138 | 0.027 | 9.4 | 15.7 | ok |
| ARweak-m1-c2-s1 | 5.904 | 0.94 | 0.027 | 1.378 | 4.364 | 0.104 | 0.031 | 9.4 | 15.7 | ok |
| ADJOPP-mc1-s1 | 13.327 | 1.08 | 0.031 | 1.067 | 12.071 | 0.129 | 0.029 | 18.5 | 30.9 | ok |
| ADJOPP-mc2-s1 | 13.783 | 1.12 | 0.029 | 0.751 | 12.852 | 0.124 | 0.027 | 18.5 | 30.9 | ok |
| AR-mc1-s1 | 14.011 | 1.13 | 0.036 | 0.964 | 12.838 | 0.138 | 0.036 | 18.5 | 30.9 | ok |
| AR-mc2-s1 | 13.058 | 1.06 | 0.033 | 0.604 | 12.062 | 0.329 | 0.029 | 18.5 | 30.9 | ok |
| ARweak-mc1-s1 | 9.801 | 0.79 | 0.027 | 0.671 | 8.950 | 0.122 | 0.031 | 18.5 | 30.9 | ok |
| ARweak-mc2-s1 | 10.259 | 0.83 | 0.029 | 0.480 | 9.599 | 0.120 | 0.031 | 18.5 | 30.9 | ok |

## class means vs the committed model (G-B criterion: mean <= 1.5 E and no fit > 2.5 E)
| class | fits | mean total | E | mean/E | max fit | max/E | calib mean | islands mean | merge mean | G-B |
|---|---|---|---|---|---|---|---|---|---|---|
| m1 I3 | 6 | 6.02 | 6.28 | 0.96 | 7.24 | 1.15 | 0.915 | 4.899 | 0.150 | PASS |
| m1 I0 | 6 | 5.00 | 5.76 | 0.87 | 5.55 | 0.96 | 0.092 | 4.710 | 0.140 | PASS |
| m4 I3 | 6 | 12.37 | 12.36 | 1.00 | 14.01 | 1.13 | 0.756 | 11.395 | 0.160 | PASS |

sum of the 18 precision fits = 140.41 core-h
sum of all 20 fits (18 + A3 canary + XB) = 145.68 core-h

## ratios by dataset of cell means (islands only; c_X of the rule)
- AR islands mean: m1I3 5.028, m4I3 12.450 (x2.48), m1I0 5.114 (x1.02)
- ARweak islands mean: m1I3 4.146, m4I3 9.274 (x2.24), m1I0 3.843 (x0.93)
- ADJOPP islands mean: m1I3 5.523, m4I3 12.462 (x2.26), m1I0 5.173 (x0.94)

## R'=16 cost per fit estimated from the R'=64 stage costs (islands/4, merge/3.1 per quote_model.py): m1 I3 2.25, m1 I0 1.38 (saving 39%), m4 I3 3.72 (x1.65 of m1 I3)
calibration share of a fit at R'=64: m1 I3 15.2%, m1 I0 1.8%; calibration I0 / I3 = 0.100 (0.092 / 0.915 core-h); quote model assumed U(0.2, 0.5)
