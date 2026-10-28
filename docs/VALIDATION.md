# Local validation

Recorded 2026-10-28. These are actual packaging and native software/source checks, not comparative usefulness evidence.

## Additional compiler boundary probe

Status: **known native limitation**. Four authored pure-function cases: two controls passed, while negated and descriptive “parallel” language incorrectly grouped dependent assignments. The baseline source hashes, exact cases and limits are retained in [Compiler limits](COMPILER-LIMITS.md). No candidate compiler source was changed. The earlier regression-suite result below covers its stated test set and does not establish semantic scheduling correctness or current-runner acceptance.

## Parser/compiler/hooks regression suite

Status: **passed**.

`python -m pytest tests -q`

278 tests. Repaired request-construction failure handling, human-gated zero-confidence fallback, consistent no-Core result shape, and repeated-agent sequencing. Generated recipe schema/live runner acceptance still requires current-host validation.

## Portable packaging and install

Status: **passed**.

`python3 scripts/capability.py build; python3 scripts/capability.py check; python3 scripts/capability.py doctor; python3 scripts/capability.py install --dest <temporary-parent> (twice)`

All operations passed. No runtime activation or effectiveness measured.

## Skill discovery metadata

Status: **passed**.

`<yaml-enabled-python> /path/to/skill-creator/scripts/quick_validate.py skills/intent-to-plan`

Skill is valid. This is a structural check, not a behavioral benchmark.

The [dated machine-readable record](evaluations/2026-10-28/consolidation.json) retains source revisions, check scope, and limitations. Native runtime gates stay separate from installation. No public repository, current service, user installation, or personal source checkout was changed.
