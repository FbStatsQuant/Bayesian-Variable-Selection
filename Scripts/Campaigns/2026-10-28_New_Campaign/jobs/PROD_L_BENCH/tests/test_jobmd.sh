#!/bin/bash
# test_jobmd.sh -- static checks of B/JOB.md of the benchmark wave (PROD_L_BENCH DESIGN.md sections 1, 4-6): executable as written, ABESS D54.3 disclosure, no-truth note.
#   bash test_jobmd.sh WORKDIR
source "$(dirname "$0")/lib.sh"
t_init "${1:-}" test_jobmd
SRCB=${PRODL_B_SRC:-$B}; J="$SRCB/JOB.md"; D="$SRCB/DESIGN.md"
[ -s "$J" ]; t_cond "JM00 JOB.md exists" $?

# ---- transfers: ABSOLUTE NOTS paths (nots_pull.py refuses relative ones before any transfer) ------------------------------------------------------
bad=$(grep 'nots_pull' "$J" | grep -E '(results|logs)/' | grep -v '/scratch/fb31/New_Campaign/' | wc -l | tr -d ' ')
t_eq "JM01 every nots_pull line naming results/ or logs/ uses the absolute /scratch/fb31/New_Campaign/ path" 0 "$bad"
grep -q '/scratch/fb31/New_Campaign/results/\${\?STAMP}\?_lowp_benchres' "$J"; t_cond "JM02 the pull of /scratch/fb31/New_Campaign/results/\${STAMP}_lowp_benchres is documented (ONE result folder)" $?
grep -q '/scratch/fb31/New_Campaign/logs/\${\?STAMP}\?_lowp_bench' "$J"; t_cond "JM03 the pull of /scratch/fb31/New_Campaign/logs/\${STAMP}_lowp_bench is documented" $?
grep -qE '(^|[^/A-Za-z_])results/\$\{?STAMP' "$J"; [ $? -ne 0 ]; t_cond "JM04 no relative results/\${STAMP}_... path remains" $?
grep -oE 'nots_pull\.py "[^"]*"( --delete)?' "$J" | grep '/runs/' | grep -q -e '--delete'; [ $? -ne 0 ]; t_cond "JM05 the home summaries (manifests, inventory_final, resubmit, JOBIDS.tsv) are pulled WITHOUT --delete" $?
for what in manifests resubmit JOBIDS; do grep -q "$what" "$J"; t_cond "JM06 the home summary '$what' has an explicit pull" $?; done

# ---- waves and commands -----------------------------------------------------------------------------------------------------------------------------
grep -q 'submit_bench.sh' "$J" && grep -q -e '--wave main' "$J"; t_cond "JM10 the main wave command (submit_bench.sh --wave main --profile ...) is documented" $?
grep -q 'make_resubmit.sh' "$J" && grep -qE 'submit_bench.sh[^`]*--wave r[0-9N]+[^`]*--pieces' "$J"; t_cond "JM11 the resubmission round: make_resubmit.sh STAMP rN once, then ONE submit_bench.sh --wave rN --pieces <pieces with a list>" $?
first_submit=$(grep -n 'submit_bench.sh.*--wave r' "$J" | head -n 1 | cut -d: -f1); n_before=$(head -n "${first_submit:-0}" "$J" | grep -c 'make_resubmit.sh')
[ "${n_before:-0}" -ge 1 ]; t_cond "JM12 make_resubmit.sh comes before the rN submission" $?
grep -qiE 'benchretry' "$J" && grep -qiE 'bench_rN|bench_r1|benchretry_r' "$J"; t_cond "JM13 the bench vs benchretry routing and the list names are documented" $?
grep -qiE 'next round|rN\+1|fresh wave name|new wave name' "$J"; t_cond "JM14 the next round uses a fresh wave name" $?
grep -q -e '--allow-concurrent-prodl' "$J"; t_cond "JM15 --allow-concurrent-prodl is documented as HQ-only" $?
grep -qiE 'lowpL_s\[?1' "$J" || grep -qiE 'PROD-L.*(queued|running)' "$J"; t_cond "JM16 the serialisation after the PROD-L SMC / repeat lane is documented" $?
grep -q -e '--check-drained' "$J" && grep -q -e '--profile withH --yes' "$J"; t_cond "JM17 retune: '--profile withH --yes' then '--check-drained' before PROD-H" $?
grep -qiE 'exit 3' "$J" && grep -qi 'triage' "$J" && grep -q -e '--until-terminal' "$J"; t_cond "JM18 the waiter: exit 3 = triage, --until-terminal for completion" $?
grep -q 'waiter.sh' "$J" && grep -q 'lowpB_' "$J"; t_cond "JM19 the waiter command with the lowpB_ prefix" $?
grep -qE 'reconcile_bench.py' "$J" && grep -qE 'make_manifests.sh[^`]*--piece bench' "$J" && grep -qE 'make_manifests.sh[^`]*--piece logs' "$J"; t_cond "JM20 reconcile_bench.py and the per-piece closes (--piece bench, --piece logs) are documented" $?
grep -q 'cleanup_bench.sh' "$J" && grep -q -e '--receipt' "$J"; t_cond "JM21 cleanup_bench.sh --yes --receipt is documented" $?
grep -q 'accept_bench.R' "$J" && grep -q -e '--results' "$J"; t_cond "JM22 the laptop acceptance accept_bench.R --results ... is documented" $?

# ---- must NOT carry PROD-L machinery that this bundle does not have -----------------------------------------------------------------------------------
for w in 's0_truthlock' 's0_lock' 's8_unlock' 'recover_truth' 'p5scan' 'make_p5_list'; do
  grep -q "$w" "$J"; [ $? -ne 0 ]; t_cond "JM30 JOB.md has no instruction about '$w' (no truth lock / unlock / P5 in the benchmark wave)" $?
done

# ---- section 14 operating notes: ABESS D54.3 disclosure and the no-truth note -------------------------------------------------------------------------------
S14=$(sed -n '/^#\+ *\(§ *\)\?14/,$p' "$J")
grep -qE '^#+ *(§ *)?14[.)]? .*[Oo]perating notes' "$J"; t_cond "JM40 a '14 ... Operating notes' section exists" $?
printf '%s\n' "$S14" | grep -qi 'ABESS'; t_cond "JM41 section 14 carries the ABESS note" $?
printf '%s\n' "$S14" | grep -q 'D54.3'; t_cond "JM42 ... citing D54.3" $?
printf '%s\n' "$S14" | grep -qiE 'exact size check|splicing|suboptimal|not performed'; t_cond "JM43 ... the disclosure that the ABESS exact size check is NOT performed" $?
printf '%s\n' "$S14" | grep -qiE 'no truth|truth is not|never (on|to) NOTS|no truth on NOTS'; t_cond "JM44 section 14 carries the no-truth note (no truth on NOTS; scoring happens later, elsewhere)" $?
printf '%s\n' "$S14" | grep -qiE 'clear_stale'; t_cond "JM45 section 14 covers the stale-artefact recovery (clear_stale.sh: lock dirs, hidden temps, incomplete method units)" $?
printf '%s\n' "$S14" | grep -qiE 'incomplete (method )?unit|manual repair'; t_cond "JM46 ... including the incomplete method unit the CLI refuses as 'manual repair'" $?
grep -qiE 'D54.3|ABESS' "$D"; t_cond "JM47 DESIGN.md itself states the ABESS D54.3 disclosure" $?
grep -qi 'invalid job id' "$J" "$SRCB/DESIGN.md" 2>/dev/null; [ $? -ne 0 ] || grep -i 'invalid job id' "$J" "$SRCB/DESIGN.md" | grep -viE '\b(no|not|never|removed|without|nor)\b' | wc -l | grep -q '^0$'; t_cond "JM48 no 'invalid job id' tolerance claim" $?

t_summary
