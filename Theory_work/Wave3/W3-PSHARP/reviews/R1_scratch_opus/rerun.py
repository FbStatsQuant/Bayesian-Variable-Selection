import sys, os
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "numerics")))
import numpy as np
import a_orth, c_counter, b_check
a_orth.V1(np.random.default_rng(20261111))
rng = np.random.default_rng(20261114); c_counter.V1(rng); c_counter.E2()
b_check.F1(np.random.default_rng(20261112)); b_check.T1()
