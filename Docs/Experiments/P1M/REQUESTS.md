# REQUESTS to HQ — NOTS queries (read-only; nothing submitted)

Format: id, exact command(s), why. Please paste the output under each item, or into `requests/R<id>.txt`.

## R1 Node inventory: memory, cores, threads per core, features (commons)
```
sinfo -p commons -N -o "%N %c %m %f %G %T" | sort -u -k2,4 | head -80
scontrol show node bb2u24c1 | egrep "CPUTot|ThreadsPerCore|CoresPerSocket|Sockets|RealMemory|AvailableFeatures"
scontrol show node bc12u01c1 2>/dev/null | egrep "CPUTot|ThreadsPerCore|RealMemory|AvailableFeatures"
```
Why: the memory per node bounds exact linkage (OD-5: about 180k at 251 GB) and the number of 1M islands per node. Threads
per core decides how threaded tasks are billed (R2). We also need to know whether any node has ≥ 1 TB of memory.

## R2 Billing of a threaded task
```
sacct -j 2692690 -o JobID,AllocCPUS,ReqCPUS,CPUTimeRAW,ElapsedRaw,NodeList
scontrol show partition commons | egrep "MaxTime|DefMemPerCPU|MaxMemPerNode|OverSubscribe|TRES"
```
Why: P6 found AllocCPUS = 2 per single-thread task. For G8 we need to know whether `--cpus-per-task=16` bills 16 or 32,
and whether 2 threads per allocated core pair are allowed (this could halve core-h).

## R3 Partition limits
```
scontrol show partition commons scavenge | egrep "PartitionName|MaxTime|MaxNodes|PreemptMode|GraceTime"
sacctmgr show assoc user=fb31 format=Account,Partition,MaxJobs,MaxSubmit,MaxTRES,GrpTRES -p
```
Why: the 24 h limit and the 150-task cap drive checkpoint design (G9) and the 1M wall time.

## R4 Storage quotas
```
quota -s 2>/dev/null; df -h /scratch/fb31 /home/fb31/projects/BVS 2>/dev/null; du -sh /scratch/fb31 2>/dev/null
```
Why: stores, RB arrays and checkpoints at 1M (several GB per island and fit) go to /scratch; we must plan the cleanup.

## R5 Per-phase records of the B3 runs (already on NOTS; read-only)
```
ls /scratch/fb31/w3scale/out/b3_p*/res | head; sacct -j 2698178,2698179,2698180 -o JobID,Elapsed,MaxRSS,NodeList -X
```
Why: the per-step µs at 10k/20k under revision D, the I and T per tier, and the peak RSS per phase feed the cost model. If
they are already in `origin/theory/W3-SCALE` results, point me to the file instead.

Nothing in this file asks for a submission.
