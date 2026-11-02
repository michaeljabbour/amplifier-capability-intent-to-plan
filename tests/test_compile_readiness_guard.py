"""Offline draft-tool contract checks; no host, provider or recipe execution."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import unittest
from unittest.mock import Mock

import yaml

from amplifier_module_tool_idd import IDDCompileTool, mount
from amplifier_module_tool_idd.compiler import IDDCompiler
from amplifier_module_tool_idd.grammar import GrammarState
from amplifier_module_tool_idd.parser import IDDParser
from helpers import FakeCoordinator, FakeProvider, VALID_DECOMPOSITION_JSON


def decomposition(confirmation="human"):
    data = json.loads(VALID_DECOMPOSITION_JSON)
    data["trigger"]["confirmation"] = confirmation
    return IDDParser()._dict_to_decomposition(data, raw_input="Fictional API plan")


class TestCompileReadinessGuard(unittest.IsolatedAsyncioTestCase):
    def test_current_tool_guidance_preserves_the_readiness_boundary(self):
        root = Path(__file__).resolve().parents[1]
        context = (root / "context/idd-awareness.md").read_text()
        self.assertIn("idd-compile-draft/v1", context)
        self.assertIn("mode: draft", context)
        self.assertIn("execution_ready: false", context)
        self.assertIn("Default calls are", context)
        self.assertIn("Do not pass the embedded `recipe_yaml`", context)
        self.assertNotIn("executable Amplifier recipe YAML (schema v1.7.0)", context)
        self.assertNotIn("This recipe can then be executed via the `recipes` tool", context)
        for name in ["idd-composer.md", "idd-spec-expert.md"]:
            with self.subTest(agent=name):
                guidance = (root / "agents" / name).read_text()
                self.assertIn("mode: draft", guidance)
                self.assertIn("execution_ready: false", guidance)
                self.assertIn("adapter", guidance)

    def test_surface_describes_draft_and_requires_explicit_mode(self):
        tool = IDDCompileTool(FakeCoordinator())
        self.assertIn("execution_ready=false", tool.description)
        self.assertIn("incompatible", tool.description)
        self.assertNotIn("ready for the recipes tool", tool.description)
        self.assertNotIn("schema v1.7.0", tool.description)
        self.assertEqual(tool.input_schema["required"], ["mode"])
        self.assertEqual(tool.input_schema["properties"]["mode"]["enum"], ["draft"])
        self.assertFalse(tool.input_schema["additionalProperties"])

    async def test_default_rejects_before_state_access_or_compilation(self):
        # This coordinator intentionally has no methods: the default must not
        # even consult mutable session state, much less execute or authorize.
        tool = IDDCompileTool(object())
        tool._compiler.compile_to_yaml = Mock(side_effect=AssertionError("must not compile"))
        for request in [{}, {"decomposition_json": VALID_DECOMPOSITION_JSON}]:
            with self.subTest(request_keys=list(request)):
                result = await tool.execute(request)
                self.assertFalse(result.success)
                payload = json.loads(result.output)
                self.assertEqual(payload["status"], "blocked")
                self.assertEqual(payload["schema"], "idd-compile-draft/v1")
                self.assertIs(payload["execution_ready"], False)
                self.assertNotIn("recipe_yaml", payload)
        tool._compiler.compile_to_yaml.assert_not_called()

    async def test_invalid_modes_and_types_never_compile(self):
        tool = IDDCompileTool(object())
        tool._compiler.compile_to_yaml = Mock(side_effect=AssertionError("must not compile"))
        for mode in [None, True, False, 1, 0, [], {}, "ready", "execute", "DRAFT", ""]:
            with self.subTest(mode=mode):
                result = await tool.execute({"mode": mode})
                self.assertFalse(result.success)
                payload = json.loads(result.output)
                self.assertEqual(payload["status"], "invalid_input")
                self.assertIs(payload["execution_ready"], False)
                self.assertNotIn("recipe_yaml", payload)
        tool._compiler.compile_to_yaml.assert_not_called()

    async def test_nonobject_input_is_rejected(self):
        tool = IDDCompileTool(object())
        for request in [None, [], "draft", True, 0]:
            with self.subTest(request=request):
                result = await tool.execute(request)
                self.assertFalse(result.success)
                self.assertEqual(json.loads(result.output)["status"], "invalid_input")

    async def test_unrecognized_flags_cannot_assert_readiness_or_approval(self):
        tool = IDDCompileTool(object())
        tool._compiler.compile_to_yaml = Mock(side_effect=AssertionError("must not compile"))
        for key in ["execution_ready", "approved", "execute", "require_execution_ready"]:
            with self.subTest(key=key):
                result = await tool.execute({"mode": "draft", key: True})
                self.assertFalse(result.success)
                self.assertEqual(json.loads(result.output)["status"], "invalid_input")
        tool._compiler.compile_to_yaml.assert_not_called()

    async def test_explicit_draft_preserves_legacy_plan_and_confirmation(self):
        for confirmation in ["human", "auto", "none"]:
            with self.subTest(confirmation=confirmation):
                data = json.loads(VALID_DECOMPOSITION_JSON)
                data["trigger"]["confirmation"] = confirmation
                tool = IDDCompileTool(FakeCoordinator())
                result = await tool.execute({"mode": "draft", "decomposition_json": json.dumps(data)})
                self.assertTrue(result.success)  # Draft production, never host readiness.
                payload = json.loads(result.output)
                self.assertEqual(payload["schema"], "idd-compile-draft/v1")
                self.assertEqual(payload["status"], "draft")
                self.assertIs(payload["execution_ready"], False)
                self.assertEqual(payload["recipe_format"], "idd-legacy-plan/v1")
                plan = yaml.safe_load(payload["recipe_yaml"])
                self.assertEqual(plan, IDDCompiler().compile(decomposition(confirmation)))
                self.assertEqual([step["role"] for step in plan["steps"]],
                                 ["investigator", "designer", "implementer"])
                self.assertEqual("approval" in plan, confirmation == "human")
                if confirmation == "human":
                    self.assertTrue(plan["approval"]["required"])

    async def test_explicit_draft_reads_state_without_mutation_or_events(self):
        provider = FakeProvider()
        coordinator = FakeCoordinator(providers={"fake": provider})
        state = GrammarState()
        state.decomposition = decomposition()
        state.status = "decomposed"
        coordinator.register_capability("idd.grammar_state", state)
        before = copy.deepcopy(state)
        capabilities_before = dict(coordinator._capabilities)
        request = {"mode": "draft"}
        result = await IDDCompileTool(coordinator).execute(request)
        self.assertTrue(result.success)
        self.assertEqual(state, before)
        self.assertEqual(request, {"mode": "draft"})
        self.assertEqual(coordinator._capabilities, capabilities_before)
        self.assertEqual(coordinator.hooks._emitted, [])
        self.assertEqual(coordinator._mounted, {})
        self.assertEqual(provider._calls, [])

    async def test_invalid_explicit_json_never_falls_back_to_session_plan(self):
        coordinator = FakeCoordinator()
        state = GrammarState()
        state.decomposition = decomposition()
        coordinator.register_capability("idd.grammar_state", state)
        tool = IDDCompileTool(coordinator)
        tool._compiler.compile_to_yaml = Mock(side_effect=AssertionError("must not compile"))
        for value in ["not-json", "[]", "null", "123", None, {}, [], True, 12]:
            with self.subTest(value=value):
                result = await tool.execute({"mode": "draft", "decomposition_json": value})
                self.assertFalse(result.success)
                payload = json.loads(result.output)
                self.assertEqual(payload["status"], "invalid_input")
                self.assertNotIn("recipe_yaml", payload)
        tool._compiler.compile_to_yaml.assert_not_called()

    async def test_explicit_draft_with_no_plan_reports_missing_decomposition(self):
        result = await IDDCompileTool(FakeCoordinator()).execute({"mode": "draft"})
        self.assertFalse(result.success)
        payload = json.loads(result.output)
        self.assertEqual(payload["status"], "missing_decomposition")
        self.assertNotIn("recipe_yaml", payload)

    async def test_compile_error_retains_unready_structured_error(self):
        tool = IDDCompileTool(FakeCoordinator())
        tool._compiler.compile_to_yaml = Mock(side_effect=ValueError("fixture compiler failure"))
        with self.assertLogs("amplifier_module_tool_idd", level="ERROR"):
            result = await tool.execute({
                "mode": "draft", "decomposition_json": VALID_DECOMPOSITION_JSON
            })
        self.assertFalse(result.success)
        payload = json.loads(result.output)
        self.assertEqual(payload["status"], "compile_failed")
        self.assertIs(payload["execution_ready"], False)
        self.assertNotIn("recipe_yaml", payload)

    async def test_programmatic_capability_has_same_default_guard_and_draft_mode(self):
        coordinator = FakeCoordinator()
        await mount(coordinator)
        compile_capability = coordinator.get_capability("idd.compile")
        blocked = await compile_capability(VALID_DECOMPOSITION_JSON)
        self.assertFalse(blocked.success)
        self.assertEqual(json.loads(blocked.output)["status"], "blocked")
        draft = await compile_capability(VALID_DECOMPOSITION_JSON, mode="draft")
        self.assertTrue(draft.success)
        self.assertIs(json.loads(draft.output)["execution_ready"], False)
        self.assertEqual(coordinator.hooks._emitted, [])


if __name__ == "__main__":
    unittest.main()
