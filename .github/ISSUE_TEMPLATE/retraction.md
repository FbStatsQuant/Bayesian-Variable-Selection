---
name: Retraction / narrowing / downgrade
about: A statement is false, too broad, or its evidence is weaker than recorded
title: "[retract|narrow|downgrade] <claim id>: "
labels: [theory, retraction]
---
**Claim** (registry id, file:lines, version, verbatim status): 
**Evidence** (counterexample / review file / failed gate): 
**Operation**: retract / narrow (`--still-covers` which uses?) / downgrade (new verbatim status)
**Impact report** (`propagate.py <op> <id> --reason ... --dry-run`, paste): 
**Headline?** if yes add `major-claim`; Felipe approves before `propagate.py` runs with `--apply`.
