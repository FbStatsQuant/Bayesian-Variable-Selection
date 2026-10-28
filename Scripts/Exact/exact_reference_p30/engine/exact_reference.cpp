#include <Rcpp.h>
#include <cmath>
#include <cstdint>
#include <algorithm>
using namespace Rcpp;
// Origin: archived BVS_Astra/Coding/exact_reference.cpp.
// Exact subset enumeration with Cholesky extensions; no model pruning.
// Keep only the current Cholesky factors and running log-sum-exp totals.
// The recursion visits each subset once, extending its parent factorization.
// Added here: input checks, MAP output, and periodic user-interrupt checks.
// This is used only for the reference, never by the SMC sampler.
struct ExactState {
  int p, low, ids[32];
  double A[32][32], V[32][32], LA[32][32]{}, LV[32][32]{};
  double b[32], z[32]{}, quad[33]{}, ratio[33]{};
  double yty, exponent, constant, b0, lp0, lpodds;
  double maximum=R_NegInf, total=0, numer[32]{};
  uint64_t count=0;
  uint32_t map_code=0;
  double map_log_score=R_NegInf;
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
  void visit(int k,int next) {
    double lw=logml(k)+lp0+k*lpodds;
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
    count++;
    if((count & 65535)==0) Rcpp::checkUserInterrupt();
    for(int j=next;j<low;j++) {push(j,k);visit(k+1,j+1);}
  }
};
// [[Rcpp::export]]
List exact_chunk_cpp(List ctx,double lambda,int low,int high_code) {
  ExactState s(ctx,lambda,low);int k=0;
  if(!(lambda>0 && lambda<1) || high_code<0 || double(high_code)>=std::ldexp(1.0,s.p-low)) stop("Invalid prior or chunk code");
  for(int j=low;j<s.p;j++) if((high_code>>(j-low))&1) s.push(j,k++);
  s.visit(k,0);
  NumericVector num(s.p);
  for(int j=0;j<s.p;j++) num[j]=s.numer[j]>0?s.maximum+std::log(s.numer[j]):R_NegInf;
  return List::create(_["log_Z"]=s.maximum+std::log(s.total),_["log_pip_numerator"]=num,_["n_models"]=(double)s.count,_["map_code"]=(double)s.map_code,_["map_log_score"]=s.map_log_score);
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
