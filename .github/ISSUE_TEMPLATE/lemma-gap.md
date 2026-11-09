---
name: Lemma gap
about: A proof step does not go through (statement may stand)
title: "[gap] <claim id>: "
labels: [theory, lemma-gap]
---
**Claim** (registry id, file:lines, version): 
**Step that fails** (file:line) and why: 
**Does the statement survive?** yes (PATCH) / unknown (SUSPECT) / no (see retraction template)
**Uses affected** (`registry.py rdeps <id>`; which dependents use `@proof:` facts of this step): 
**Proposed action**: `propagate.py patch|suspect <id> --reason ... --dry-run` (attach the impact report)
