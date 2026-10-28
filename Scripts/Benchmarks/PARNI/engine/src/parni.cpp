// Published PARNI-B proposal, adapted to the campaign's exact Gaussian target.
// No author source is executed. Equations 28, 31, 33--35, Liang et al. (2022).
#include <Rcpp.h>
#include <unordered_map>
#include <vector>
#include <algorithm>
#include <cmath>
#include <cstdint>
#include <functional>
using namespace Rcpp;
// [[Rcpp::plugins(cpp11)]]

static double logadd(double a, double b) {
  const double m=std::max(a,b); return m+std::log(std::exp(a-m)+std::exp(b-m));
}
static double logistic(double x) {
  return x>=0 ? 1.0/(1.0+std::exp(-x)) : std::exp(x)/(1.0+std::exp(x));
}
static int count_bits(uint32_t x) { int n=0; while(x) { x &= x-1; ++n; } return n; }
struct Entry { double score; std::vector<double> beta; };
struct Target {
  int n,p; double yy; std::vector<double> gram,xy;
  std::unordered_map<uint32_t,Entry> cache;
  size_t cache_limit; double misses=0,hits=0;
  Target(const NumericMatrix& X,const NumericVector& y,size_t limit):
    n(X.nrow()),p(X.ncol()),yy(0),gram(p*p),xy(p),cache_limit(limit) {
    for(int i=0;i<n;++i) yy+=y[i]*y[i];
    for(int j=0;j<p;++j) {
      for(int i=0;i<n;++i) xy[j]+=X(i,j)*y[i];
      for(int k=0;k<=j;++k) {
        double g=0; for(int i=0;i<n;++i) g+=X(i,j)*X(i,k);
        gram[j*p+k]=gram[k*p+j]=g;
      }
    }
  }
  static double chol(std::vector<double>& m,int d) {
    double ld=0;
    for(int i=0;i<d;++i) for(int j=0;j<=i;++j) {
      double s=m[i*d+j]; for(int k=0;k<j;++k) s-=m[i*d+k]*m[j*d+k];
      if(i==j) { if(!(s>0) || !R_finite(s)) stop("Nonpositive Cholesky pivot in PARNI target");
        m[i*d+j]=std::sqrt(s); ld+=std::log(s); }
      else m[i*d+j]=s/m[j*d+j];
    }
    return ld;
  }
  Entry evaluate(uint32_t code) const {
    std::vector<int> ids; for(int j=0;j<p;++j) if(code&(uint32_t(1)<<j)) ids.push_back(j);
    int d=ids.size(); std::vector<double> lam(d*d),a(d*d),u(d),m(d);
    for(int j=0;j<d;++j) for(int k=0;k<d;++k) {
      double g=gram[ids[j]*p+ids[k]];
      lam[j*d+k]=(g+(j==k ? 1.0:0.0))/n;
      a[j*d+k]=g+lam[j*d+k];
    }
    double ld_l=chol(lam,d),ld_a=chol(a,d);
    for(int j=0;j<d;++j) {
      double z=xy[ids[j]]; for(int k=0;k<j;++k) z-=a[j*d+k]*u[k]; u[j]=z/a[j*d+j];
    }
    for(int j=d-1;j>=0;--j) {
      double z=u[j]; for(int k=j+1;k<d;++k) z-=a[k*d+j]*m[k]; m[j]=z/a[j*d+j];
    }
    double quad=yy; for(int j=0;j<d;++j) quad-=xy[ids[j]]*m[j];
    if(!R_finite(quad) || quad < -1e-10*std::max(1.0,yy)) stop("Invalid residual quadratic in PARNI target");
    quad=std::max(0.0,quad);
    Entry e; e.score=.5*(ld_l-ld_a)-(.01+n/2.0)*std::log(.02+quad)
      +d*std::log(.2)+(p-d)*std::log(.8);
    e.beta=std::vector<double>(p,0.0); for(int j=0;j<d;++j) e.beta[ids[j]]=m[j];
    return e;
  }
  Entry get(uint32_t code) {
    auto it=cache.find(code); if(it!=cache.end()) { ++hits; return it->second; }
    ++misses; Entry e=evaluate(code); if(cache.size()<cache_limit) cache.emplace(code,e); return e;
  }
};
struct Path {
  uint32_t proposal; double logqf=0,logqr=0,logaux=0,logalpha=0,logzratio=0;
  int distance=0;
};
// Reverse coordinate order retraces the identical intermediate models. Thus
// reverse step probabilities can be accumulated at the forward step itself.
static Path path_update(uint32_t initial,const std::vector<int>& order,
    const std::vector<double>& pip,double omega,const std::function<double(uint32_t)>& score,
    bool random,const std::vector<int>& flips) {
  Path out; uint32_t state=initial; double oldscore=score(initial),s=oldscore;
  const double logw=std::log(omega),logkeep=std::log1p(-omega);
  for(size_t r=0;r<order.size();++r) {
    int j=order[r]; bool bit=state&(uint32_t(1)<<j); uint32_t alternative=state^(uint32_t(1)<<j);
    double s2=score(alternative);
    // p(k_j=1|alternative) / p(k_j=1|state), A=min(1,pip/(1-pip)), D=min(1,(1-pip)/pip).
    double logodd=(bit ? 1.0:-1.0)*(std::log(pip[j])-std::log1p(-pip[j]));
    double logr=s2-s+logodd;
    double logchange=logw+std::min(0.0,logr),logz=logadd(logchange,logkeep);
    bool flip=random ? (R::runif(0,1)<std::exp(logchange-logz)) : (flips[r]!=0);
    if(flip) {
      double revchange=logw+std::min(0.0,-logr),revz=logadd(revchange,logkeep);
      out.logqf+=logchange-logz; out.logqr+=revchange-revz;
      out.logaux+=logodd; out.logzratio+=logz-revz;
      state=alternative; s=s2; ++out.distance;
    } else {
      out.logqf+=logkeep-logz; out.logqr+=logkeep-logz;
    }
  }
  out.proposal=state;
  out.logalpha=s-oldscore+out.logaux+out.logqr-out.logqf;
  if(std::abs(out.logalpha-out.logzratio)>1e-9*(1+std::abs(out.logalpha)))
    stop("PARNI reverse-path acceptance identity failed");
  return out;
}

// Test interface: exact prescribed path in a supplied finite target table.
// [[Rcpp::export]]
List parni_path_cpp(NumericVector logs,int initial,IntegerVector order,
                    IntegerVector flips,NumericVector pip,double omega) {
  int p=pip.size();
  if(p<1 || p>20 || logs.size()!=(1<<p) || order.size()!=flips.size() ||
     initial<0 || initial>=logs.size() || !(omega>0 && omega<1)) stop("Invalid fixed-path input");
  std::vector<int> ord(order.begin(),order.end()), fl(flips.begin(),flips.end());
  std::vector<double> pi(pip.begin(),pip.end()); std::vector<bool> seen(p,false);
  for(int &j:ord) { --j; if(j<0 || j>=p || seen[j]) stop("Invalid path order"); seen[j]=true; }
  for(double x:pi) if(!(x>0&&x<1)) stop("Invalid adaptive PIP");
  for(int x:fl) if(x!=0&&x!=1) stop("Invalid flip indicator");
  for(double x:logs) if(!R_finite(x)) stop("Nonfinite target score");
  auto f=[&logs](uint32_t s){ return logs[s]; };
  Path z=path_update(initial,ord,pi,omega,f,false,fl);
  return List::create(_["proposal"]=double(z.proposal),_["logq_forward"]=z.logqf,
    _["logq_reverse"]=z.logqr,_["log_neighborhood_ratio"]=z.logaux,
    _["log_acceptance_ratio"]=z.logalpha,_["log_normalizer_ratio"]=z.logzratio);
}

// [[Rcpp::export]]
List parni_scores_cpp(NumericMatrix X,NumericVector y,IntegerVector models) {
  if(X.nrow()!=y.size() || X.ncol()<1 || X.ncol()>30) stop("Invalid target dimensions");
  Target target(X,y,0); NumericVector scores(models.size()); NumericMatrix beta(models.size(),X.ncol());
  for(int i=0;i<models.size();++i) {
    if(models[i]<0 || double(models[i])>=std::pow(2.0,X.ncol())) stop("Invalid model code");
    Entry e=target.evaluate(models[i]); scores[i]=e.score;
    for(int j=0;j<X.ncol();++j) beta(i,j)=e.beta[j];
  }
  return List::create(_["log_score"]=scores,_["beta_mean"]=beta);
}

// [[Rcpp::export]]
List parni_run_cpp(NumericMatrix X,NumericVector y,IntegerVector seeds,
    int warmup,int samples,double pi0,double eps,int cache_limit) {
  const int p=X.ncol(),chains=seeds.size();
  if(p<1 || p>30 || X.nrow()!=y.size() || chains!=4 || warmup<0 || samples<4 ||
     !(pi0>0&&pi0<.5) || !(eps>0&&eps<.5) || cache_limit<1) stop("Invalid sampler controls");
  Target target(X,y,cache_limit); List result(chains); NumericVector meanbeta(p,0.0);
  Function setseed("set.seed");
  for(int c=0;c<chains;++c) {
    setseed(seeds[c]);
    uint32_t state=0;
    if(c==1) state=(uint32_t(1)<<p)-1;
    if(c>=2) for(int j=0;j<p;++j) if(R::runif(0,1)<(c==2?.2:.5)) state|=uint32_t(1)<<j;
    uint32_t initial=state;
    std::vector<double> adap(p,.2),rbsum(p,0.0);
    NumericMatrix rb(samples,p); IntegerMatrix indicator(samples,p);
    IntegerVector model(samples),size(samples),jump(samples),neighborhood(samples),accepted(samples);
    NumericVector lp(samples),acceptprob(samples),omega_trace(warmup+1);
    IntegerVector warm_model(warmup+1); NumericVector warm_lp(warmup+1);
    double omega=.5,zomega=0;
    omega_trace[0]=omega; warm_model[0]=int(state); warm_lp[0]=target.get(state).score;
    auto score=[&target](uint32_t s){ return target.get(s).score; };
    for(int t=0;t<warmup+samples;++t) {
      if(t%1000==0) checkUserInterrupt();
      std::vector<int> order;
      for(int j=0;j<p;++j) {
        bool bit=state&(uint32_t(1)<<j);
        double ratio=adap[j]/(1-adap[j]);
        double eta=std::min(1.0,bit?1.0/ratio:ratio);
        if(R::runif(0,1)<eta) order.push_back(j);
      }
      for(int j=int(order.size())-1;j>0;--j) {
        int k=std::min(j,int(std::floor(R::runif(0,1)*(j+1)))); std::swap(order[j],order[k]);
      }
      Path z=path_update(state,order,adap,omega,score,true,std::vector<int>());
      double ap=std::exp(std::min(0.0,z.logalpha));
      bool accept=R::runif(0,1)<ap; if(accept) state=z.proposal;
      Entry e=target.get(state);
      for(int j=0;j<p;++j) {
        bool bit=state&(uint32_t(1)<<j);
        double stoggle=target.get(state^(uint32_t(1)<<j)).score;
        double r=logistic(bit ? e.score-stoggle : stoggle-e.score);
        if(t<warmup) rbsum[j]+=r;
        else { rb(t-warmup,j)=r; indicator(t-warmup,j)=int(bit); }
      }
      if(t<warmup) {
        for(int j=0;j<p;++j) adap[j]=pi0+(1-2*pi0)*rbsum[j]/(t+1.0);
        zomega+=std::pow(t+1.0,-.7)*(ap-.65);
        omega=eps+(1-2*eps)*logistic(zomega);
        omega_trace[t+1]=omega; warm_model[t+1]=int(state); warm_lp[t+1]=e.score;
      } else {
        int i=t-warmup; model[i]=int(state); size[i]=count_bits(state); lp[i]=e.score;
        jump[i]=accept?z.distance:0; neighborhood[i]=order.size(); accepted[i]=int(accept); acceptprob[i]=ap;
        for(int j=0;j<p;++j) meanbeta[j]+=e.beta[j]/(double(samples)*chains);
      }
    }
    result[c]=List::create(_["seed"]=seeds[c],_["initial_model"]=int(initial),
      _["model"]=model,_["indicator"]=indicator,_["rb"]=rb,_["model_size"]=size,
      _["log_target"]=lp,_["accepted"]=accepted,_["acceptance_probability"]=acceptprob,
      _["hamming_jump"]=jump,_["neighborhood_size"]=neighborhood,
      _["warmup_model"]=warm_model,_["warmup_log_target"]=warm_lp,
      _["warmup_omega"]=omega_trace,_["frozen_omega"]=omega,_["frozen_adaptive_pips"]=wrap(adap));
  }
  return List::create(_["chains"]=result,_["beta"]=meanbeta,
    _["cache_size"]=double(target.cache.size()),_["cache_hits"]=target.hits,_["cache_misses"]=target.misses,
    _["cache_limit"]=cache_limit);
}
