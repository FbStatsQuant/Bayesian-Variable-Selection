No findings.

I checked the entire statement against `PROOF_v1.tex`, including:

- **C1, lines 63–90:** The strict-maximum argument, event decomposition, Markov bound, and boundedness argument converting H03 into \(E_0\delta_1\to0\) are valid.
- **(a), lines 92–178:** Fresh-stream conditioning supports the iid miss formula with the stated draw count. The nonlaunch term is retained. The H10 corollary, intensity scaling, boundary \(p\le C\sqrt n\), and exceptional start-mass event are handled correctly.
- **(b), lines 180–194:** SR scores truth under the stated execution-time condition, including at the feasibility cap. Round-start occupancy is appropriately distinguished.
- **(c), lines 196–253:** The stopped-opportunity recursion avoids conditioning on future exposure. The \(D=0\) and \(b=1\) cases, PX implication, actual neighbour-edge requirement, and conditional random lower bounds are consistent.
- **(d), lines 255–278:** Block subsets are feasible; table scoring and symmetry of feasible flip-or-swap neighbourhoods establish discovery. The argument correctly retains output usability separately.
- **(e), lines 280–368:** Uniform H24 bounds apply after past-measurable selection. The first-exit bound and endpoint-miss recursion establish repair, with availability and nonlaunch terms retained. The \(H=0\) convention and fixed-\(s_0,d\) asymptotics are consistent.
- **(f), lines 370–396:** Completed enumeration gives the global ordered maximum and exact finite evidence/PIP sums. The fixed-\(p\) branch inequality follows from \(N_0\ge n\), while completion remains an explicit requirement.

H03, H10, and H24 are used as hypotheses throughout. The proof does not establish their proposed primitive sufficient conditions or claim PIP accuracy on the SMC branch.

verified
