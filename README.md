# Intent to Plan

Turn a complex request into a plan you can test and hand over.

People and agents coordinating work whose goal, inputs, responsibilities, and timing can drift apart. Use for complex requests, multi-role workflows, reviewable specifications, or a handoff before execution.

## Optional compiler: known scheduling limit

The method produces a reviewable plan. Its retained optional compiler is a lexical prototype: it can group dependent steps when “parallel” appears in a negation or a description of a bug. A dated four-case probe passed two controls and failed both dependency cases. Do not execute its output without inspecting the dependencies and validating it with the actual host's current recipe validator. [Exact cases and source hashes](docs/COMPILER-LIMITS.md) preserve this finding; the earlier 278-test suite does not establish scheduling correctness.

## Install the portable method

```sh
python3 scripts/capability.py doctor
python3 scripts/capability.py install --dest ~/.agents/skills
```

Keep the complete `skills/intent-to-plan` folder together. Installation copies only that method, references, and license; it starts no service and installs no runtime. Use a different skills-parent path for your host.

## Choose the mode

- **Decompose** — The request mixes purpose, roles, evidence, norms, and timing. Five explicit primitives with source, assumptions, and unresolved questions.
- **Compose** — The components need an actionable dependency plan. A plan with inputs/outputs, dependencies, scope, authority, and acceptance evidence.
- **Review** — A plan is about to be executed or compiled. A defect list or a bounded ready judgment; execution is a separate action.

## What was consolidated

[Migration map](docs/MIGRATION.md) records the original source paths and current roles. Primary Git history, native engines, tests, examples, and evaluation assets remain in this checkout. [Native guide](docs/NATIVE-README.md) preserves the original project documentation; old install URLs and runtime claims there are historical and need current verification. [Validation](docs/VALIDATION.md) records actual checks and limits.

## Build the local site

```sh
python3 scripts/capability.py build
python3 scripts/capability.py check
```

Open `_site/index.html` or serve `_site` with a local static server. The downloadable ZIP is built from canonical method bytes. The fictional before/after example illustrates intended judgment; it is not a measured improvement. Nothing has been published or renamed remotely.
