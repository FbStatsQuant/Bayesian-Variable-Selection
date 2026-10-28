# SYNTHETIC current-A schema; local mock execution authorized by Amendment 2.
a <- commandArgs(TRUE); code <- a[1]; root <- a[2]
source(file.path(code, "registry.R")); source(file.path(code, "score.R")); source(file.path(code, "aggregate.R"))
source(a[3]) # Frozen, byte-identical A adapter; no core is loaded, compiled or fitted.
source(a[4]); policy <- mock_r1_policy()
policy_hash <- digest::digest(serialize(policy,NULL,version=3),algo="sha256",serialize=FALSE)
adapter_hash <- smcbvs_file_hash(a[3])
dir.create(root, recursive=TRUE, showWarnings=FALSE)
manifest <- list(); tm <- list(); cases <- list()
for (p in c(500L, 1000L)) for (sc in 1:6) for (rep in 1:11) {
  i <- length(cases)+1L
  id <- sprintf("p%04d_S%d_r%03d", p, sc, rep)
  # Deliberately equal array hashes on repeated synthetic designs are permitted.
  spec <- smcbvs_case_spec(id,"c100")
  ca <- data.frame(dataset_id=id, p=p, scenario=sc, replicate=rep, data_seed=spec$data_seed,
    fold_seed=spec$fold_seed, method_seed=spec$method_seed, x_sha256=strrep("a",64),
    y_c100_sha256=strrep("b",64), y_c050_sha256=strrep("c",64),
    foldid_sha256=strrep("d",64), file_sha256=strrep("e",64))
  cases[[i]] <- ca; manifest[[i]] <- ca
  td <- file.path(root,"truth",sprintf("p%04d",p)); dir.create(td,recursive=TRUE,showWarnings=FALSE)
  beta <- numeric(p); beta[1:14] <- rep(c(.8,1,1.2,1.4,1.6,1.8,.8),2)
  tr <- list(dataset_id=id,active=1:14,beta=beta)
  path <- file.path(td,paste0(id,".rds")); saveRDS(tr,path,version=3)
  tm[[i]] <- data.frame(dataset_id=id,file_sha256=file_sha256(path),active=paste(1:14,collapse=";"))
}
write_table(do.call(rbind,manifest),file.path(root,"inputs_manifest.csv"))
write_table(do.call(rbind,tm),file.path(root,"truth_manifest.csv"))
mapping <- list()
for (sk in c("c100","c050")) {
  bench_dir <- file.path(root,paste0("benchmark_",sk)); dir.create(bench_dir)
  smc_run <- paste0("SYNTHETIC_SMC_",sk); smc_dir <- file.path(root,smc_run); dir.create(smc_dir)
  scored <- list(); coverage <- list()
  for (i in seq_along(cases)) {
    ca <- cases[[i]]; p <- ca$p; case_id <- paste0(ca$dataset_id,"_",sk)
    outcome <- (i-1) %% 9
    st <- c("ok","ok","ok","ok","ok","warning","failed","timeout","not_run")[outcome+1]
    support <- switch(as.character(outcome), "0"=1:14, "1"=1:15, "2"=1:13,
      "3"=c(1:13,15), "4"=integer(), "5"=1:14, integer())
    flagged <- outcome == 5
    row_for <- function(m,r,role,run_id) {
      x <- as.data.frame(setNames(replicate(length(BASE_COLUMNS),NA_character_,simplify=FALSE),BASE_COLUMNS))
      vals <- list(study="SYNTHETIC_NOT_PRODUCTION",run_id=run_id,source_sha256=strrep("f",64),
        regime="H",p=p,scenario=ca$scenario,replicate=ca$replicate,scale_key=sk,
        scale=if(sk=="c100") 1 else .5,dataset_id=ca$dataset_id,case_id=case_id,
        data_seed=ca$data_seed,fold_seed=ca$fold_seed,method_seed=ca$method_seed,
        inputs_sha256=ca$file_sha256,x_sha256=ca$x_sha256,y_sha256=ca[[paste0("y_",sk,"_sha256")]],
        fold_sha256=ca$foldid_sha256,method_id=m,method_label="SYNTHETIC",package="fixture",package_version="1",
        rule_id=r,role=role,status=st,converged=if(st %in% FAILED_STATUSES) NA else TRUE,
        diag_flag=flagged,diag_codes=if(flagged) "ess_tau" else "",n_warnings=0,warnings="",messages="",error="",
        k=if(st %in% FAILED_STATUSES) NA else length(support),
        support=if(st %in% FAILED_STATUSES) NA else paste(support,collapse=";"),
        support_audit=if(st %in% FAILED_STATUSES) "1;2" else NA,runtime_s=as.numeric(i),host="SYNTHETIC",
        slurm_job_id=Sys.getenv("SLURM_JOB_ID"),slurm_array_task_id="NA",
        started_utc="2000-01-01T00:00:00Z",finished_utc="2000-01-01T00:00:01Z")
      for (nm in names(vals)) x[[nm]] <- as.character(vals[[nm]])
      x
    }
    # All fixture methods deliberately share one case outcome. Score it once with the
    # unchanged kernel, then set rule identities; avoid thousands of identical R calls.
    scored_template <- score_fit_rows(row_for("F1","cv_min","primary",basename(bench_dir)),1:14,NULL,p)
    for (m in names(REGISTRY)) {
      reg <- rules_of(m,TRUE)
      coverage[[length(coverage)+1]] <- data.frame(case_id=case_id,dataset_id=ca$dataset_id,p=p,
        scenario=ca$scenario,replicate=ca$replicate,method_id=m,state=if(i==12) "missing" else "complete")
      if(i==12) next
      for(j in seq_along(reg$rules)) {
        if(i==10 && j==1) next  # missing one registered rule without dropping expected case
        row <- scored_template; row$method_id <- m; row$rule_id <- reg$rules[j]; row$role <- reg$roles[j]
        scored[[length(scored)+1]] <- row
      }
    }
    if(i==12 || ca$replicate>10) next
    native_status <- c("completed","completed","completed","completed","completed","completed",
      "schedule_limit","numerical_failure","resource_limit")[outcome+1]
    flags <- list(E1=flagged,E2=FALSE,E3=FALSE,checks_passed_final=!flagged,
        low_empirical_ESS=FALSE,grid_unconverged=FALSE,local_limit=FALSE)
    if(i %in% c(20,21)) {native_status <- if(i==20) "y_constant" else "no_predictors"; support <- integer()}
    fake_fit <- mock_native_fit(p,if(st %in% FAILED_STATUSES && !i %in% c(20,21)) 1:2 else support,native_status,flags)
    fake_fit$timings$total <- i
    warnings <- if(flagged) "SYNTHETIC captured R warning" else character()
    messages <- character()
    outputs <- smcbvs_outputs(fake_fit,p)
    design <- as.list(row_for("SMCBVS","hpm","primary",smc_run)[1,])
    design <- design[setdiff(names(design),c("rule_id","role","status","converged","diag_flag","diag_codes",
      "n_warnings","warnings","messages","error","k","support","support_audit",TRUTH_COLUMNS))]
    design$method_seed <- ca$data_seed+4000000
    design$fold_seed <- NA; design$fold_sha256 <- NA
    design$source_sha256 <- adapter_hash; design$v3_source_sha256 <- adapter_hash; design$v3_version <- "3"
    design$adapter_mapping_status <- policy$mapping_status; design$adapter_policy_id <- policy$id
    design$adapter_policy_sha256 <- policy_hash
    rows <- mock_r1_rule_rows(fake_fit,outputs,design,policy,warnings=warnings,messages=messages)
    mapping[[length(mapping)+1]] <- rows[,c("v3_status","v3_flags_json","rule_id","status","converged","diag_flag","role")]
    if(i==10) rows <- rows[rows$rule_id!="pip05",,drop=FALSE]
    cd <- file.path(smc_dir,sprintf("p%04d",p),case_id); dir.create(cd,recursive=TRUE)
    csv <- file.path(cd,"SMCBVS.csv"); rds <- file.path(cd,"SMCBVS.rds")
    record <- list(rows=rows,fit=fake_fit,pip=outputs$pip,pip_primary_original=outputs$pip,hpm=outputs$hpm,mpm=outputs$mpm,
      estimates_available=outputs$estimates_available,adapter_policy=policy,adapter_policy_sha256=policy_hash,
      warnings=warnings,messages=messages,native_status=fake_fit$status,finished_utc="2000-01-01T00:00:01Z",label="SYNTHETIC fake core; never fitted")
    gc() # Release fixture temporaries before A's unchanged xz serializer allocates its encoder.
    mock_write_record(file.path(cd,"SMCBVS"),record)
  }
  write_table(do.call(rbind,scored),file.path(bench_dir,"scored_rows.csv"))
  write_table(do.call(rbind,coverage),file.path(bench_dir,"coverage.csv"))
  write_table(new_problems(),file.path(bench_dir,"problems.csv"))
  sg <- do.call(rbind,lapply(c(500L,1000L),function(p) data.frame(p=p,signal=sprintf("a%02d",1:14),
    index=1:14,beta=rep(c(.8,1,1.2,1.4,1.6,1.8,.8),2))))
  write_table(sg,file.path(bench_dir,"truth_signals.csv"))
  writeLines(c(paste("run_id:",basename(bench_dir)),"expect: synthetic | p: 500,1000"),file.path(bench_dir,"score_log.txt"))
  aggregate_run(bench_dir)
}
mapping_path <- file.path(root,"mock_mapping.csv")
write_table(unique(do.call(rbind,mapping)),mapping_path)
jsonlite::write_json(list(adopted=TRUE,mapping_status="adopted",mock_only=TRUE,
  policy_id=policy$id,policy_sha256=policy_hash,authority=policy$authority,mapping_csv_sha256=file_sha256(mapping_path)),
  file.path(root,"mock_mapping_ruling.json"),pretty=TRUE,auto_unbox=TRUE)
writeLines(c("SYNTHETIC fixture: no benchmark data/truth were read.",capture.output(sessionInfo())),file.path(root,"FIXTURE.txt"))
