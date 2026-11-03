#!/bin/bash
# final_inventory_remote.sh : (NOTS, via ssh nots 'bash -s' < this; control lane) HQ D92 READ-ONLY inventory of the campaign's own NOTS footprint:
# /scratch/fb31/New_Campaign and /home/fb31/projects/BVS/New_Campaign only (never the benchmark freeze, ~/.claude/remote, .t3-recovery).
SC=/scratch/fb31/New_Campaign; HC=/home/fb31/projects/BVS/New_Campaign
echo "date=$(date -u +%FT%TZ) host=$(hostname)"
echo "== squeue fb31"; squeue -h -u fb31 -o '%i %j %T' 2>&1; echo "(end)"
echo "== guard"; bash $HC/code/ops/guard.sh 0 2>&1 | tail -2
echo "== scratch depth 2 (KB, files)"; for d in $SC $SC/* $SC/*/*; do [ -e "$d" ] || continue; printf '%s\t%s KB\t%s files\t%s\n' "$(stat -c %F "$d" | cut -c1-4)" "$(du -sk "$d" 2>/dev/null | cut -f1)" "$(find "$d" -type f 2>/dev/null | wc -l)" "$d"; done
echo "== scratch upload/ files (name, bytes)"; find $SC/upload -maxdepth 2 -type f -printf '%s\t%p\n' 2>/dev/null | sort -k2 | head -60
echo "== home campaign depth 1-2 (KB, files)"; for d in $HC $HC/* $HC/*/*; do [ -e "$d" ] || continue; printf '%s\t%s KB\t%s files\t%s\n' "$(stat -c %F "$d" | cut -c1-4)" "$(du -sk "$d" 2>/dev/null | cut -f1)" "$(find "$d" -type f 2>/dev/null | wc -l)" "$d"; done
echo "== home campaign: symlinks / foreign-owned / non-regular"; find $HC $SC \( -type l -o ! -user fb31 -o ! -type f ! -type d \) -printf '%y %u %p\n' 2>/dev/null | head -20; echo "(end)"
echo "done"
