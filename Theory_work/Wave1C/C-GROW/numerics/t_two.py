import time
import d_common as d
for job in [(5,400,1.0,3200,0,True),(2,400,1.0,800,0,True)]:
    t=time.time(); r=d.run(job)
    print(job, round(time.time()-t,1),'s t_start',r['t_start'],'t_ls',r['t_ls'],'B',r['B'],'start_size',r['start_size'],'symdiff',r['symdiff'])
