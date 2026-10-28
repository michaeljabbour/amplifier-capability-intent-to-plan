---
name: intent-to-plan
description: Use for complex requests, multi-role workflows, reviewable specifications, or a handoff before execution.
license: MIT
---

# Intent to Plan

Turn a complex request into a plan you can test and hand over.

## Preserve the request before formalizing it

Record the original request, intended user outcome, known constraints, available artifacts, and decisions already settled. Do not invent success thresholds, execution permission, or an agent because the template has a field. Use a lightweight checklist for small work; use the full grammar when ambiguity or coordination justifies it.

## Decompose into five questions

Use [five primitives](references/idd-five-primitives/METHOD.md): Intent/WHY (goal, success, scope, tradeoffs); Agent/WHO (capability and accountable owner); Context/WHAT (provided, inspected, discovered, missing); Behavior/HOW (reusable working rules); Trigger/WHEN (activation, prerequisites, confirmation). Mark each statement explicit, inferred, or unresolved. A model's confidence number is self-report, not correctness.

Use [decomposition checks](references/idd-decomposition-test/METHOD.md) to detect conflation. Ask whether a change in one responsibility unnecessarily forces a change elsewhere. Dependencies can be real: orthogonality is a useful design question, not permission to erase legitimate coupling. Preserve restrictive constraints wherever they affect execution.

## Compose a bounded plan

Apply [composition rules](references/idd-composition-rules/METHOD.md). Give each work unit one outcome, owner/performer, required inputs and revisions, outputs, acceptance evidence, prerequisites, failure/recovery, and an authority boundary. Declare parallel tasks only when inputs and edits are independent. Same agent identity does not imply parallelism. Declare each dependency and the artifact that crosses it; never assume a hidden shared context.

Keep user intent, design grammar, and execution machinery distinguishable. Reference an available agent by its real identity or assign an existing human/local performer. Do not invent a deployer, schedule, service, or permission merely to complete the diagram. Ask only a blocking question; continue independent authorized inspection while a decision is pending.

## Review before execution

Use [review](references/idd-review/METHOD.md) and the preserved anti-pattern reference. Inspect the actual plan for scope leakage, circular/implicit dependencies, unsupported criteria, absent inputs, redundant roles, and actions beyond authority. Return ready, revise, or blocked with reasons and the smallest correction. “Ready” means the plan meets its stated checks, not that its work happened.

## Optional compiler

[Recipe compilation](references/idd-recipe-compilation/METHOD.md) preserves the original mapping and examples. The retained `tool-idd` parser/compiler/hooks are optional prototype machinery. Their lexical parallelism detection and tests do not prove a current runtime recipe schema; validate generated output using the actual host recipe validator before running it. A provider failure or malformed parse must remain a visibly untrusted draft; never run fallback text automatically.

## Output

Return the original intent, five-primitives table with basis, dependency plan, acceptance checks, assumptions and owner decisions, review verdict, and next authorized action. Include generated recipes only as inspected/validated drafts at their actual evidence level.
