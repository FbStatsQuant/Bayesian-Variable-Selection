import itertools,json,math
from pathlib import Path
err=sum(abs(250*sum(s)-500)>100 for s in itertools.product((0,1),repeat=4))/16
out={'bounded_h_finite_R':{'R':4,'W':1,'island_H':[0,1000],'pi_h':500,'epsilon':100,'tail_probability':err,'claimed_bound':4/(4*100**2)},'B_D17_missing_eta':{'pi_truth':.3,'pi_other':.7,'A':.7/.3,'eta':3,'condition_holds':.7/.3<=3,'truth_is_mode':False}}
assert err==.625
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
