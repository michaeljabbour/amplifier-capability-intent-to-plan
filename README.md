# Intent to Plan

Turn the request into work someone can follow.

Watch the [73-second film](https://michaeljabbour.github.io/amplifier-capability-intent-to-plan/#film): a one-line request, an agent that pounces, and a plan that marks what was said, what was guessed and what is still open. The example in it is fictional.

A planning skill for complex requests. Separate the goal, people, inputs, working rules and timing, then connect them into a plan with explicit dependencies and acceptance checks.

[Explore the site](https://michaeljabbour.github.io/amplifier-capability-intent-to-plan/) · [Read the method](skills/intent-to-plan/SKILL.md) · [Install guide](docs/INSTALL.md)

## What you get

- **Preserve what was actually asked.** Keep stated requirements, inferences and unanswered decisions separate.
- **Make handoffs concrete.** Give each unit an outcome, owner, input revision, output and completion evidence.
- **Catch problems before execution.** Review hidden dependencies, missing inputs, invented thresholds and work beyond the granted scope.

## Install and try it

Requires Git and Python 3.11+. Run these commands from a terminal:

```sh
git clone https://github.com/michaeljabbour/amplifier-capability-intent-to-plan.git
cd amplifier-capability-intent-to-plan
python3 scripts/capability.py doctor
python3 scripts/capability.py install --dest ~/.agents/skills
```

The installer copies `skills/intent-to-plan` as a complete folder into your chosen skills parent. Use the discovery path supported by your agent. It starts no service and configures no provider. Restart or refresh skill discovery in your host, then ask:

```text
Use Intent to Plan on this request: improve our fictional onboarding flow and prepare a release. Separate explicit requirements from assumptions, identify missing baseline evidence, order design before implementation and make the release authority visible. Produce a plan only.
```

If your agent does not discover installed skills, point it directly at the complete folder and ask it to read `SKILL.md`. Reading the method needs no Python runtime. [Installation details](docs/INSTALL.md) cover conflict handling and optional native execution.

## How the work proceeds

1. **Decompose the request.** Use five questions: why, who, what, how and when; label the basis for each answer.
2. **Connect the work.** Declare prerequisites and the artifacts that cross them. Parallelize only genuinely independent work.
3. **Review the plan.** Return ready, revise or blocked with the smallest correction and next authorized action.

## Example output

Fictional worked example. It illustrates the intended output; it is not a measured result or a real customer story.

```text
Fictional plan: onboarding improvement
Why: remove a reported task breakdown
Evidence: baseline and affected steps unresolved
Order: inspect → decide → implement → verify
Handoff: accepted design and task checks cross to builder
Release: separate authorized action
Verdict: revise until the missing input is resolved
```

## What is checked

Recorded portable checks and the historical parser/compiler suite have separate evidence scopes. This local 0.3.0 review candidate makes the native compile tool draft-only. Available offline checks and their limits are recorded with the candidate; no current-host recipe execution is established. See [validation](docs/VALIDATION.md) and the [draft-only upgrade guide](docs/releases/0.3.0-draft-tool-contract.md).

## Optional native compiler: inspection only

Default `idd_compile` and `idd.compile` calls fail in this candidate. Explicit `mode: draft` returns a versioned JSON envelope containing `execution_ready: false` and a legacy YAML plan for inspection. Do not send that plan to the recipes tool. A draft does not grant approval, and this change supplies no host adapter. [Review the breaking changes and caller migration](docs/releases/0.3.0-draft-tool-contract.md).

The low-level compiler is unchanged from public main. It still uses lexical parallelism inference: a negated or descriptive “parallel” can group dependent assignments. The exposed four-case probe remains two passes and two failures. No scheduling repair or unsupported current-host compatibility claim is included. [Historical cases and source hashes](docs/COMPILER-LIMITS.md) remain preserved.

## Retained implementation and references

[Migration map](docs/MIGRATION.md) records the original source paths and current roles. Primary Git history, native engines, tests, examples, and evaluation assets remain in this checkout. [Native guide](docs/NATIVE-README.md) preserves the original project documentation; old install URLs and runtime claims there are historical and need current verification. [Validation](docs/VALIDATION.md) records actual checks and limits.

## Build the site

```sh
python3 scripts/capability.py build
python3 scripts/capability.py check
```

The static site includes a ZIP built from the canonical method, references and license. Runtime and provider setup remain separate from installing the portable method.

## Repository migration

This repository was renamed from `amplifier-skill-intent-to-plan` to `amplifier-capability-intent-to-plan`. Existing installed method names, bundle aliases and native interfaces stay the same. See the [migration guide](https://michaeljabbour.github.io/migration/) and [repository map](https://michaeljabbour.github.io/migration/mapping.json) for source URL updates.

## Optional coaching

For an explicitly requested practice or review checkpoint, use [the local coaching guide](skills/intent-to-plan/references/coaching-session.v1.md). It includes a fictional first task, a baseline, a bounded budget, stop rules and human-reviewed keep/revert. No learner trace is saved by default, and software checks do not establish human learning or outside-user usefulness.
