# Literal master II.9 transcription with II.4 covariance and LOWP_SPEC dev seeds.
root <- 'C:/Users/felip/AppData/Local/Temp/lowp_work/bench_smoke'
for (case in list(c(20,1,1),c(30,4,2),c(30,6,3))) {
 p<-case[1]; s<-case[2]; r<-case[3]; n<-200L; j<-seq_len(p); H<-outer((j-1)%/%5,(j-1)%/%5,'==')*1; I<-diag(p)
 Sigma<-switch(s,I,outer(j,j,function(x,y) .5^abs(x-y)),.7*H+.3*I,.85*H+.15*I,.3+ .4*H+.3*I,{rho<-.4+.1*((j-1)%/%5%%6); H*outer(rho,rho,function(x,y)x)+diag(1-rho)})
 seed<-if(p==20)2210000L else 2310000L; seed<-seed+10000L*s+r; RNGkind('Mersenne-Twister','Inversion','Rejection');set.seed(seed)
 X<-scale(matrix(rnorm(n*p),nrow=n)%*%chol(Sigma));attr(X,'scaled:center')<-NULL;attr(X,'scaled:scale')<-NULL; eps<-rnorm(n)
 b<-numeric(p); active<-c(3,7,14,16,25)[seq_len(if(p==20)4 else 5)]; b[active]<-c(1.4,-1,1.8,-1.2,.8)[seq_along(active)]; signal<-drop(X%*%b)
 Y<-sapply(c(c100=1,c075=.75,c050=.5,c035=.35,c025=.25),function(sc)sc*signal+eps)
 fold_seed<-(if(p==20)4210000L else 4310000L)+10000L*s+r;set.seed(fold_seed);foldid<-sample(rep(1:10,length.out=n));dataset_id<-sprintf('p%04d_S%d_r%03d',p,s,r)
 x<-list(X=X,Y=Y,foldid=foldid,dataset_id=dataset_id,p=as.integer(p),scenario=s,replicate=r,data_seed=seed,fold_seed=fold_seed,method_seed=seed+4000000L)
 dir<-file.path(root,'inputs',sprintf('p%04d',p));dir.create(dir,recursive=TRUE,showWarnings=FALSE);saveRDS(x,file.path(dir,paste0(dataset_id,'.rds')),compress=FALSE)
}
