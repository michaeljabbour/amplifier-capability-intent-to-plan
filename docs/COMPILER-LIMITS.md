# Optional compiler scheduling limit

Recorded 2026-10-28 against candidate `95a3f54ad6bd504ad3347006cebf79437a0fa67b`.

The portable method remains a plan/dependency review procedure. The optional native compiler uses lexical concurrency markers; it does not prove semantic independence. It is a prototype requiring dependency inspection and validation by the actual current host recipe runner before execution.

The actual pure-function probe used these fictional assignments:

| Case | Expected group sizes | Actual | Result |
|---|---|---|---|
| “Migrate the schema. Do not run in parallel with the reader.” Then read the migrated schema. | 1, 1 | 2 | Failed |
| Inspect the “parallel execution bug,” then read the finding file and repair it. | 1, 1 | 2 | Failed |
| Two explicitly parallel, independent documentation reviews. | 2 | 2 | Passed |
| The same agent writes a manifest, then reads it to validate it. | 1, 1 | 1, 1 | Passed |

[Frozen protocol](evaluations/2026-10-28/compiler-boundary/PROTOCOL.json) and [actual result](evaluations/2026-10-28/compiler-boundary/compiler-probe.json) retain the exact input strings, baseline commit and grammar/compiler SHA256 values. The probe imported the actual modules without mounting the host tool. It made no parser/model/provider or recipe execution call. These four exposed authored cases are engineering evidence, not independent held-out tasks, user outcomes or an estimate of general failure frequency.

The research pass rejected a regex-only patch fitted to these cases. Any native scheduling promotion needs an explicit dependency/scheduling contract, separately frozen unseen cases and actual current-runner acceptance. Preserve this record under its original baseline when that work happens.
