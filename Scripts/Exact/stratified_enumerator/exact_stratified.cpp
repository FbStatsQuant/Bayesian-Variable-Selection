#include <Rcpp.h>
#include <cmath>
#include <cstdint>
#include <algorithm>
using namespace Rcpp;
// Size-stratified exact enumeration. COPY of the frozen engine's exact_reference.cpp
// (sha256 263dde27...3c5f) with added per-size accumulators; the original Bernoulli
// accumulators (total, numer, maximum, MAP) are kept unchanged.
// Added per size k = 0..p: log Z_k = log sum_{|S|=k} m(S), log N_jk = log sum_{|S|=k, j in S} m(S)
// (m = marginal likelihood WITHOUT model prior), model count, and the top-TOP models by log m(S).
static const int TOP = 20;
struct ExactState {
  int p, low, ids[32];
  double A[32][32], V[32][32], LA[32][32]{}, LV[32][32]{};
  double b[32], z[32]{}, quad[33]{}, ratio[33]{};
  double yty, exponent, constant, b0, lp0, lpodds;
  double maximum=R_NegInf, total=0, numer[32]{};
  uint64_t count=0;
  uint32_t map_code=0;
  double map_log_score=R_NegInf;
  // stratified accumulators
  double smax[32], stot[32]{}, snumer[32][32]{};
  uint64_t scount[32]{};
  double tscore[32][TOP]; uint32_t tcode[32][TOP]; int tn[32]{};
  ExactState(List ctx, double lambda, int low_):low(low_) {
    NumericMatrix G=ctx["G"]; NumericVector x=ctx["Xty"];
    p=G.nrow(); if(p<1 || p>30 || low<0 || low>p) stop("Unsupported dimensions");
    double n=as<double>(ctx["n"]), tau=as<double>(ctx["tau"]);
    yty=as<double>(ctx["yty"]); b0=as<double>(ctx["b0"]);
    exponent=n/2+as<double>(ctx["a0"]);constant=as<double>(ctx["log_Cn"]);
    lp0=p*std::log1p(-lambda);lpodds=std::log(lambda)-std::log1p(-lambda);
    for(int i=0;i<p;i++) {b[i]=x[i]; for(int j=0;j<p;j++) {
      V[i][j]=(G(i,j)+(i==j?tau:0))/n; A[i][j]=G(i,j)+V[i][j];
    }}
    for(int k=0;k<32;k++){smax[k]=R_NegInf;for(int t=0;t<TOP;t++){tscore[k][t]=R_NegInf;tcode[k][t]=0;}}
  }
  void push(int j,int k) {
    ids[k]=j;
    double da=A[j][j],dv=V[j][j],rhs=b[j];
    for(int t=0;t<k;t++) {
      double a=A[j][ids[t]],v=V[j][ids[t]];
      for(int u=0;u<t;u++) {a-=LA[k][u]*LA[t][u];v-=LV[k][u]*LV[t][u];}
      a/=LA[t][t];v/=LV[t][t];LA[k][t]=a;LV[k][t]=v;
      da-=a*a;dv-=v*v;rhs-=a*z[t];
    }
    if(!(da>0 && dv>0)) stop("Nonpositive Cholesky pivot");
    LA[k][k]=std::sqrt(da);LV[k][k]=std::sqrt(dv);z[k]=rhs/LA[k][k];
    quad[k+1]=quad[k]+z[k]*z[k];ratio[k+1]=ratio[k]+0.5*(std::log(dv)-std::log(da));
  }
  double logml(int k) {
    double residual=2*b0+yty-quad[k];
    if(!(residual>0)) stop("Nonpositive residual");
    return constant+ratio[k]-exponent*std::log(residual);
  }
  // keep each size's list sorted by (score desc, code asc)
  void top_insert(int k,double lm,uint32_t code) {
    int n=tn[k];
    if(n==TOP && !(lm>tscore[k][n-1] || (lm==tscore[k][n-1] && code<tcode[k][n-1]))) return;
    int i=(n<TOP)?n:TOP-1;
    while(i>0 && (tscore[k][i-1]<lm || (tscore[k][i-1]==lm && tcode[k][i-1]>code))) {
      tscore[k][i]=tscore[k][i-1];tcode[k][i]=tcode[k][i-1];i--;
    }
    tscore[k][i]=lm;tcode[k][i]=code;
    if(n<TOP) tn[k]=n+1;
  }
  void visit(int k,int next) {
    double lm=logml(k);
    double lw=lm+lp0+k*lpodds;
    if(lw>=map_log_score) {
      uint32_t code=0;
      for(int t=0;t<k;t++) code|=(uint32_t(1)<<ids[t]);
      if(lw>map_log_score || code<map_code) {map_log_score=lw;map_code=code;}
    }
    if(lw>maximum) {
      double scale=std::exp(maximum-lw);total*=scale;
      for(int j=0;j<p;j++) numer[j]*=scale;
      maximum=lw;
    }
    double w=std::exp(lw-maximum);total+=w;
    for(int t=0;t<k;t++) numer[ids[t]]+=w;
    // ---- stratified part ----
    if(lm>smax[k]) {
      double scale=std::exp(smax[k]-lm);stot[k]*=scale;
      for(int j=0;j<p;j++) snumer[k][j]*=scale;
      smax[k]=lm;
    }
    double ws=std::exp(lm-smax[k]);stot[k]+=ws;
    for(int t=0;t<k;t++) snumer[k][ids[t]]+=ws;
    scount[k]++;
    if(tn[k]<TOP || lm>=tscore[k][TOP-1]) {
      uint32_t code=0;
      for(int t=0;t<k;t++) code|=(uint32_t(1)<<ids[t]);
      top_insert(k,lm,code);
    }
    // -------------------------
    count++;
    if((count & 65535)==0) Rcpp::checkUserInterrupt();
    for(int j=next;j<low;j++) {push(j,k);visit(k+1,j+1);}
  }
};
// [[Rcpp::export]]
List exact_stratified_chunk_cpp(List ctx,double lambda,int low,int high_code) {
  ExactState s(ctx,lambda,low);int k=0;
  if(!(lambda>0 && lambda<1) || high_code<0 || double(high_code)>=std::ldexp(1.0,s.p-low)) stop("Invalid prior or chunk code");
  for(int j=low;j<s.p;j++) if((high_code>>(j-low))&1) s.push(j,k++);
  s.visit(k,0);
  int p=s.p;
  NumericVector num(p);
  for(int j=0;j<p;j++) num[j]=s.numer[j]>0?s.maximum+std::log(s.numer[j]):R_NegInf;
  NumericVector lzk(p+1),cnt(p+1);
  NumericMatrix lnjk(p+1,p),tsc(p+1,TOP),tco(p+1,TOP);
  for(int k2=0;k2<=p;k2++) {
    lzk[k2]=s.stot[k2]>0?s.smax[k2]+std::log(s.stot[k2]):R_NegInf;
    cnt[k2]=(double)s.scount[k2];
    for(int j=0;j<p;j++) lnjk(k2,j)=s.snumer[k2][j]>0?s.smax[k2]+std::log(s.snumer[k2][j]):R_NegInf;
    for(int t=0;t<TOP;t++) {
      bool ok=t<s.tn[k2];
      tsc(k2,t)=ok?s.tscore[k2][t]:R_NegInf;tco(k2,t)=ok?(double)s.tcode[k2][t]:-1.0;
    }
  }
  return List::create(_["log_Z"]=s.maximum+std::log(s.total),_["log_pip_numerator"]=num,_["n_models"]=(double)s.count,
    _["map_code"]=(double)s.map_code,_["map_log_score"]=s.map_log_score,
    _["logZ_k"]=lzk,_["logN_jk"]=lnjk,_["count_k"]=cnt,_["top_score"]=tsc,_["top_code"]=tco);
}
// [[Rcpp::export]]
NumericVector model_logml_cpp(List ctx,List models) {
  NumericVector out(models.size());
  for(int m=0;m<models.size();m++) {
    ExactState s(ctx,0.2,0);IntegerVector indices=models[m];
    for(int k=0;k<indices.size();k++) s.push(indices[k]-1,k);
    out[m]=s.logml(indices.size());
  }
  return out;
}
