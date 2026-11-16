# naming fix for W3-POST2 (DRY RUN clone): aliases defined in W3-POST2/STATEMENT.md:11-13 + that span as premise
A=Theory_work/INFRA/registry/aliases.tsv
printf '%s\t%s\t%s\n' "[P1]" "SOP:TH09" "W3-POST(2) STATEMENT alias: locked T01/T02 proof (W3-POST2 STATEMENT.md:11)" \
 "[P3]" "SOP:TH09" "W3-POST(2) STATEMENT alias: locked T03 proof (W3-POST2 STATEMENT.md:11)" \
 "[T03R]" "SOP:TH128" "W3-POST(2) STATEMENT alias: restated T03 proof ARC/W1-T03R (W3-POST2 STATEMENT.md:11-12)" \
 "[L1a′]" "W3-POST:Lemma-1a'" "W3-POST2 STATEMENT.md:12-13" \
 "[LB]" "W3-POST:Prop-LB" "W3-POST2 STATEMENT.md:13" \
 "[W3P] Theorem 1" "W3-POST:Thm-1" "W3-POST2 STATEMENT.md:12 ([W3P] = W3-POST STATEMENT v1.4)" \
 "[POST]" "W2-APP:POST" "W3-POST(2) STATEMENT alias (W3-POST STATEMENT.md:12)" >> $A
for c in A0 A1 A2 B C D "D.D(a)" "D.D(b)" E E3.1; do
  P=$(python3 -c "import sys;sys.path.insert(0,'Theory_work/INFRA/tools');sys.dont_write_bytecode=True;import bvsreg as R;print(R.index(R.load_claims())['W3-POST2:$c']['premises'])")
  python3 Theory_work/INFRA/tools/registry.py set "W3-POST2:$c" "premises=Theory_work/Wave3/W3-POST2/STATEMENT.md:11-13; $P" --reason "dry run: alias definitions are premises" >/dev/null || echo "premise fail $c"
done
