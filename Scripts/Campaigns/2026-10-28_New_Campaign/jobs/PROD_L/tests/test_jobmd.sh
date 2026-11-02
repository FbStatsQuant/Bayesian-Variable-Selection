#!/bin/bash
# test_jobmd.sh -- static checks of B/JOB.md (F8 and F12 of R1_FIX_PLAN.md): the operating document must be executable as written.
#   bash test_jobmd.sh WORKDIR
source "$(dirname "$0")/lib.sh"
t_init "${1:-}" test_jobmd
SRCB=${PRODL_B_SRC:-$B}; J="$SRCB/JOB.md"; CH="$SRCB/CORE_HOURS.md"
[ -s "$J" ]; t_cond "JM00 JOB.md exists" $?

# ---- F8.1 nots_pull with ABSOLUTE NOTS paths (Sol: the relative results/... form is refused by ops/transfer/nots_pull.py before any transfer) ------------------
pulls=$(grep -n 'nots_pull' "$J" | grep -v '^\s*#' )
[ -n "$pulls" ]; t_cond "JM01 JOB.md contains nots_pull commands" $?
bad=$(grep 'nots_pull' "$J" | grep -E '(results|logs)/' | grep -v '/scratch/fb31/New_Campaign/' | wc -l | tr -d ' ')
t_eq "JM02 every nots_pull line that names a results/ or logs/ folder uses the absolute /scratch/fb31/New_Campaign/ path" 0 "$bad"
grep -q '/scratch/fb31/New_Campaign/results/\${\?STAMP}\?_lowp_' "$J"; t_cond "JM03 a pull of /scratch/fb31/New_Campaign/results/\${STAMP}_lowp_<piece> is documented" $?
grep -q '/scratch/fb31/New_Campaign/logs/\${\?STAMP}\?_lowp_prodL' "$J"; t_cond "JM04 a pull of /scratch/fb31/New_Campaign/logs/\${STAMP}_lowp_prodL is documented" $?
grep -qE '(^|[^/A-Za-z_])results/\$\{?STAMP' "$J"; [ $? -ne 0 ]; t_cond "JM05 no relative results/\${STAMP}_lowp_... path remains anywhere" $?
grep 'nots_pull' "$J" | grep -E 'runs/|manifests|inventory_final|/p5|resubmit|JOBIDS' | grep -q -e '--delete'; [ $? -ne 0 ]; t_cond "JM06 the home summaries (manifests, inventory_final, p5, resubmit, JOBIDS.tsv) are pulled WITHOUT --delete" $?
for what in manifests inventory_final p5 resubmit JOBIDS; do grep -q "$what" "$J"; t_cond "JM07 the home summary '$what' has an explicit pull" $?; done
grep -q '{.*,.*}' <(grep 'nots_pull' "$J"); [ $? -ne 0 ]; t_cond "JM08 no brace expression is passed to nots_pull as if it were a path list" $?

# ---- F8.2 the waiter ---------------------------------------------------------------------------------------------------------------------------------------
grep -qi 'exit 3' "$J" && grep -qi 'triage' "$J"; t_cond "JM10 the waiter's exit 3 is documented as TRIAGE only" $?
grep -qi 'exit 0' "$J" && grep -qiE 'all (jobs )?terminal' "$J"; t_cond "JM11 the waiter's exit 0 (all terminal) is documented" $?
grep -q 'WAVE_UNLOCK_VERIFIED' "$J"; t_cond "JM12 before reconcile / clear_stale / a later wave: WAVE_UNLOCK_VERIFIED in the wave's unlock record is required" $?

# ---- F8.3 resubmission rounds: lists for EVERY piece first, then ONE submit -----------------------------------------------------------------------------------------
grep -qiE 'for each incomplete piece[^.]*submit' "$J"; [ $? -ne 0 ]; t_cond "JM20 the old 'for each incomplete piece ... submit' instruction is gone" $?
grep -q 'make_resubmit.sh' "$J" && grep -qE 'submit_prodl.sh[^`]*--wave r[0-9N]+[^`]*--pieces' "$J"; t_cond "JM21 one submit_prodl.sh --wave rN --pieces <pieces with a list> command is documented" $?
first_submit=$(grep -n 'submit_prodl.sh.*--wave r' "$J" | head -n 1 | cut -d: -f1)
n_before=$(head -n "${first_submit:-0}" "$J" | grep -c 'make_resubmit.sh')
[ "${n_before:-0}" -ge 1 ]; t_cond "JM22 make_resubmit.sh commands come before the (single) rN submission" $?
for p in enum20 enum30 smc smcrep; do head -n "${first_submit:-0}" "$J" | grep 'make_resubmit' | grep -q "$p"; t_cond "JM23 the list for piece '$p' is made before the round is submitted" $?; done
grep -qiE 'next round|rN\+1|fresh wave name|new wave name' "$J"; t_cond "JM24 the next round uses a fresh wave name" $?

# ---- F8.4 §14 operating notes ---------------------------------------------------------------------------------------------------------------------------------
grep -qE '^#+ *(§ *)?14[.)]? .*[Oo]perating notes' "$J"; t_cond "JM30 a '14 ... Operating notes' section exists" $?
sed -n '/^#\+ *\(§ *\)\?14/,$p' "$J" | grep -qi 'recover_truth\|safe.halt\|stale\|clear_stale'; t_cond "JM31 section 14 covers the safe-halt recoveries (recover_truth.sh / clear_stale.sh)" $?

# ---- F2 / F9 commands documented ---------------------------------------------------------------------------------------------------------------------------------
grep -q -e '--phase initial' "$J" && grep -q -e '--from-scan initial' "$J"; t_cond "JM40 the P5 sequence documents --p5-scan --phase initial and make_p5_list.sh --from-scan initial" $?
grep -q -e '--phase final' "$J"; t_cond "JM41 the final scan phase is documented" $?
grep -q 'p5r1' "$J"; t_cond "JM42 further P5 waves (p5r1) are documented" $?
grep -q -e '--check-drained' "$J" && grep -q -e '--profile withH --yes' "$J"; t_cond "JM43 retune: '--profile withH --yes' then '--check-drained' before PROD-H" $?

# ---- F12 wording ---------------------------------------------------------------------------------------------------------------------------------------------------------
for f in "$J" "$CH"; do
  grep -qi 'nominal' "$f" && grep -q '16' "$f" && grep -q '18' "$f"; t_cond "JM50 $(basename "$f"): 16 is labelled the nominal doubled core allocation and 18 the requested-wall ceiling" $?
  grep -qE '29,?160' "$f"; t_cond "JM51 $(basename "$f"): the wrapper bound 29,160 s (about 16.2) is stated" $?
done
grep -qE 'at most 16 (billed )?core-h' "$J" "$CH"; [ $? -ne 0 ]; t_cond "JM52 the unqualified 'at most 16 billed core-hours per P5 fit' statement is gone" $?

# ---- R2 M2: documentation matches the code; II1 / II2 operating notes ---------------------------------------------------------------------------------------------------
for f in "$SRCB/REUSE.md" "$SRCB/DESIGN.md" "$J"; do
  bad=$(grep -in 'invalid job id' "$f" 2>/dev/null | grep -viE '\b(no|not|never|removed|without|nor)\b' | wc -l | tr -d ' ')
  t_eq "JM60 $(basename "$f"): no claim that an 'invalid job id' answer is tolerated (every mention is a negation / removal)" 0 "$bad"
done
S14=$(sed -n '/^#\+ *\(§ *\)\?14/,$p' "$J")
printf '%s\n' "$S14" | grep -q 'truth_wave.sh" unlock'; t_cond "JM61 JOB.md section 14 contains the II2 recovery command (truth_wave.sh\" unlock ...)" $?
printf '%s\n' "$S14" | grep -q 'WAVE_UNLOCK.txt'; t_cond "JM62 ... writing LOG_RUN/truthlock/\$WAVE/WAVE_UNLOCK.txt" $?
printf '%s\n' "$S14" | grep -qi 'never create the verified marker by hand'; t_cond "JM63 ... and says never to create the verified marker by hand" $?
printf '%s\n' "$S14" | grep -q -e '--from-scan' && printf '%s\n' "$S14" | grep -q -e '--phase r1'; t_cond "JM64 JOB.md section 14 has the II1 note: fresh scan phase (--p5-scan --phase r1) then make_p5_list.sh --from-scan r1" $?
printf '%s\n' "$S14" | grep -qi 'append-only\|never overwrite'; t_cond "JM65 ... and that expected.tsv is append-only / never overwritten" $?
grep -q 'prodl_verify.py' "$SRCB/DESIGN.md" && grep -q 'stale_lib.sh' "$SRCB/DESIGN.md"; t_cond "JM66 DESIGN.md names the shared strict verifier prodl_verify.py and the stale definition stale_lib.sh" $?
grep -qiE 'expected_history|append-only' "$SRCB/DESIGN.md"; t_cond "JM67 DESIGN.md documents the append-only P5 inventory" $?
grep -qiE 'acknowledged' "$SRCB/DESIGN.md" && grep -q 'exit 4\|4 ' "$SRCB/DESIGN.md"; t_cond "JM68 DESIGN.md documents per-piece exceptions with STATUS / exit 0 1 2 4" $?
grep -qiE 'no.requeue' "$SRCB/REUSE.md" && grep -qiE 'CLOSED' "$SRCB/REUSE.md"; t_cond "JM69 REUSE.md covers the submit --no-requeue and CLOSED refusal" $?
grep -qiE 'restart' "$SRCB/REUSE.md"; t_cond "JM70 REUSE.md covers the common.sh restart guard" $?

t_summary
