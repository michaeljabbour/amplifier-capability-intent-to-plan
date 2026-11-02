# Compile tool: inspection-only draft contract

The 0.3.0 compile-tool contract corrects the `idd_compile` tool's former claim that its
output was executable, matched recipe schema v1.7.0 and was ready for the recipes
tool. The installed recipe parser rejects the legacy step fields. A wording or
guard change does **not** repair that incompatibility or establish runtime use.

## Default is blocked

`idd_compile({})` and the callable `idd.compile(decomposition_json)` return a
failed tool result with a JSON envelope containing `schema: idd-compile-draft/v1`,
`status: blocked` and `execution_ready: false`. No draft is compiled and no
session state, provider, approval or recipe execution is invoked by that path.
There is no execution-ready mode, and extra approval/readiness flags are rejected.

## Explicit inspection

Request `mode: draft` to inspect a plan. It can use the current decomposition or
an explicit `decomposition_json` string. The callable capability accepts the same
keyword-only mode:

```python
result = await compile_capability(decomposition_json, mode="draft")
```

A successful **draft-production operation** returns JSON, never bare YAML:

```json
{
  "schema": "idd-compile-draft/v1",
  "status": "draft",
  "execution_ready": false,
  "message": "Inspection only; adapter and host/runtime validation required.",
  "recipe_format": "idd-legacy-plan/v1",
  "recipe_yaml": "...legacy YAML for inspection..."
}
```

`success: true` means only that the explicitly requested draft was produced.
It does not mean host acceptance, approval, authority or execution readiness.
Do not send `recipe_yaml` to the recipes tool. Nonempty malformed explicit JSON fails rather
than silently compiling a different decomposition from session state. An omitted
or default empty decomposition string intentionally selects the current session
state in explicit draft mode; whitespace is not that sentinel.

## Compatibility and remaining work

Tool consumers must stop assuming a successful raw YAML return. Existing default
calls now fail closed; draft consumers must explicitly request the mode and parse
the versioned envelope. The pure `IDDCompiler.compile` and `compile_to_yaml` APIs
remain unchanged for prototype inspection. Decomposition fields, legacy draft
roles, approval metadata and dependency/output references are not stripped.

A future versioned host adapter must preserve role, human approval, outputs and
fork/join meaning while mapping the legacy fields. It requires installed-parser
and actual runtime fixtures; dropping rejected keys is not sufficient. This patch
does not retrieve adapter source, implement that adapter or execute a recipe.
The original compiler oracle outcomes and frozen evidence remain unchanged.

The focused offline tests exercise the tool envelope/default/invalid-input gates,
draft data preservation and absence of provider/hook/state side effects. They
are authored contract tests, not held-out quality or human-use validation.
