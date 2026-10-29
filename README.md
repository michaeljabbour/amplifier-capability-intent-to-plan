# Intent to Plan

Turn the request into work someone can follow.

Watch the [73-second film](https://michaeljabbour.github.io/amplifier-skill-intent-to-plan/#film): a one-line request, an agent that pounces, and a plan that marks what was said, what was guessed and what is still open. The example in it is fictional.

A planning skill for complex requests. Separate the goal, people, inputs, working rules and timing, then connect them into a plan with explicit dependencies and acceptance checks.

[Explore the site](https://michaeljabbour.github.io/amplifier-skill-intent-to-plan/) · [Read the method](skills/intent-to-plan/SKILL.md) · [Install guide](docs/INSTALL.md)

## What you get

- **Preserve what was actually asked.** Keep stated requirements, inferences and unanswered decisions separate.
- **Make handoffs concrete.** Give each unit an outcome, owner, input revision, output and completion evidence.
- **Catch problems before execution.** Review hidden dependencies, missing inputs, invented thresholds and work beyond the granted scope.

## Install and try it

Requires Git and Python 3.11+. Run these commands from a terminal:

```sh
git clone https://github.com/michaeljabbour/amplifier-skill-intent-to-plan.git
cd amplifier-skill-intent-to-plan
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

The portable method is checked and the optional parser/compiler retains its software suite. A separate four-case probe exposed two scheduling failures in that prototype; generated recipes require dependency inspection and the current host validator. See [validation](docs/VALIDATION.md) for the exact checks and limits.

## Optional compiler: known scheduling limit

The optional compiler is a lexical prototype. It can group dependent steps when “parallel” appears in a negation or a bug description. A four-case probe passed two controls and failed both dependency cases. Inspect dependencies and validate generated recipes with the actual current host before execution. [Exact cases and source hashes](docs/COMPILER-LIMITS.md).

## Retained implementation and references

[Migration map](docs/MIGRATION.md) records the original source paths and current roles. Primary Git history, native engines, tests, examples, and evaluation assets remain in this checkout. [Native guide](docs/NATIVE-README.md) preserves the original project documentation; old install URLs and runtime claims there are historical and need current verification. [Validation](docs/VALIDATION.md) records actual checks and limits.

## Build the site

```sh
python3 scripts/capability.py build
python3 scripts/capability.py check
```

The static site includes a ZIP built from the canonical method, references and license. Runtime and provider setup remain separate from installing the portable method.
