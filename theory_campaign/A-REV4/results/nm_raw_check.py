import math,random,json,datetime,platform,statistics
random.seed(20261102); rows=[]; raw=[]
for n in [64,256,1024]:
 residuals=[]; local=[]; truth=[]; start=[]
 for rep in range(256):
  u=math.sqrt(n-1)+random.gauss(0,1); v=random.gauss(0,1)
  yy=u*u+v*v+sum(random.gauss(0,1)**2 for _ in range(n-3)); scale=math.sqrt((n-1)/yy)
  z1=math.sqrt(n-1)*u*scale; z2=math.sqrt(n-1)*(.5*u+math.sqrt(.75)*v)*scale
  nu=.01+n/2; c=.02+n-1
  b1=-.5*math.log(n)-nu*math.log1p(-z1*z1/n/c)
  b2=-.5*math.log(n)-nu*math.log1p(-z2*z2/n/c)
  h=n*n; off=.5*(n*n-1); det=h*h-off*off
  t=n*(h*(z1*z1+z2*z2)-2*off*z1*z2)/det
  detg=n*n-.25*(n-1)**2
  b12=-.5*math.log(det/detg)-nu*math.log1p(-t/c)
  def norm(a):
   m=max(a); w=[math.exp(x-m) for x in a]; return [x/sum(w) for x in w]
  post=norm([math.log(.5),math.log(1/6)+b1,math.log(1/6)+b2,math.log(1/6)+b12])
  ini=norm([math.log(.5),math.log(1/6)+b1,math.log(1/6)+b2,math.log(1/6)+b1+b2])
  raw.append(dict(n=n,rep=rep,logBF_proxy=b2,posterior=post,start=ini)); residuals.append(b2-n/2*math.log(1/(1-.25/2))+.5*math.log(n));local.append(1/(1+math.exp(-b2)));truth.append(post[1]);start.append(ini[1])
 rows.append(dict(n=n,reps=256,proxy_logBF_remainder_sd=statistics.stdev(residuals),sd_over_sqrt_n=statistics.stdev(residuals)/math.sqrt(n),mean_local_proxy=sum(local)/256,mean_posterior_truth=sum(truth)/256,mean_start_truth=sum(start)/256))
print(json.dumps(dict(seed=20261102,host=platform.node(),utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),NM=rows),indent=2))

with open("nm_raw.json", "w") as f: json.dump(raw,f)
