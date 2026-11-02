"""Offline noncompile isolation around the breaking draft-tool contract."""
from __future__ import annotations

import json
import unittest
from unittest.mock import patch

from amplifier_module_tool_idd import IDDCompileTool, IDDDecomposeTool, mount
from amplifier_module_tool_idd.parser import IDDParser
from helpers import FakeCoordinator, FakeProvider, VALID_DECOMPOSITION_JSON


def request_without_sdk(self, prompt, available_agents):
    return {"prompt": prompt, "agents": available_agents}


class TestNoncompileReleaseContract(unittest.IsolatedAsyncioTestCase):
    @patch.object(IDDParser, "_build_chat_request", request_without_sdk)
    async def test_draft_empty_default_is_state_selection_but_whitespace_is_invalid(self):
        provider = FakeProvider(VALID_DECOMPOSITION_JSON)
        coordinator = FakeCoordinator(providers={"fake": provider})
        await mount(coordinator)
        await coordinator.get_capability("idd.decompose")("Fictional API plan")
        state_before = coordinator.get_capability("idd.grammar_state").to_dict()
        events_before = list(coordinator.hooks._emitted)
        tool = IDDCompileTool(coordinator)
        omitted = await tool.execute({"mode": "draft"})
        empty = await tool.execute({"mode": "draft", "decomposition_json": ""})
        self.assertTrue(omitted.success)
        self.assertTrue(empty.success)
        self.assertEqual(json.loads(omitted.output), json.loads(empty.output))
        self.assertIs(json.loads(empty.output)["execution_ready"], False)
        callable_default = await coordinator.get_capability("idd.compile")(mode="draft")
        self.assertEqual(json.loads(callable_default.output), json.loads(empty.output))
        for value in [" ", "\n\t", '""']:
            with self.subTest(value=value):
                rejected = await tool.execute({"mode": "draft", "decomposition_json": value})
                self.assertFalse(rejected.success)
                self.assertEqual(json.loads(rejected.output)["status"], "invalid_input")
                self.assertNotIn("recipe_yaml", json.loads(rejected.output))
        self.assertEqual(coordinator.get_capability("idd.grammar_state").to_dict(), state_before)
        self.assertEqual(coordinator.hooks._emitted, events_before)
        self.assertEqual(len(provider._calls), 1)  # Only the earlier local fake decomposition.

    @patch.object(IDDParser, "_build_chat_request", request_without_sdk)
    async def test_decompose_still_returns_primitives_and_registers_state(self):
        provider = FakeProvider(VALID_DECOMPOSITION_JSON)
        coordinator = FakeCoordinator(
            config={"agents": {"explorer": {}, "zen-architect": {}, "builder": {}}},
            providers={"fake": provider},
        )
        result = await IDDDecomposeTool(coordinator).execute({"input": "Fictional API plan"})
        self.assertTrue(result.success)
        output = json.loads(result.output)
        expected = json.loads(VALID_DECOMPOSITION_JSON)
        self.assertEqual(output["intent"], expected["intent"])
        self.assertEqual(output["agents"], expected["agents"])
        self.assertEqual(output["trigger"], expected["trigger"])
        self.assertEqual(len(provider._calls), 1)  # A local fake, never a provider request.
        state = coordinator.get_capability("idd.grammar_state")
        self.assertEqual(state.status, "decomposed")
        self.assertEqual(state.steps_total, 3)
        self.assertEqual([c.name for c in state.criteria_status], expected["intent"]["success_criteria"])
        self.assertEqual([e["event"] for e in coordinator.hooks._emitted],
                         ["idd:intent_parsed", "idd:composition_ready"])

    @patch.object(IDDParser, "_build_chat_request", request_without_sdk)
    async def test_noncompile_callables_still_work_while_default_compile_blocks(self):
        provider = FakeProvider(VALID_DECOMPOSITION_JSON)
        coordinator = FakeCoordinator(providers={"fake": provider})
        await mount(coordinator)
        decompose = coordinator.get_capability("idd.decompose")
        result = await decompose("Fictional API plan")
        self.assertTrue(result.success)
        state = coordinator.get_capability("idd.grammar_state")
        update = coordinator.get_capability("idd.update_criterion")
        first = state.criteria_status[0].name
        update(first, True, "Synthetic assertion only")
        self.assertTrue(state.criteria_status[0].passed)
        events_before = list(coordinator.hooks._emitted)
        blocked = await coordinator.get_capability("idd.compile")()
        self.assertFalse(blocked.success)
        self.assertIs(json.loads(blocked.output)["execution_ready"], False)
        self.assertEqual(coordinator.hooks._emitted, events_before)
        await coordinator.get_capability("idd.resolve_intent")("completed", "Fictional mock receipt")
        event = coordinator.hooks._emitted[-1]
        self.assertEqual(event["event"], "idd:intent_resolved")
        self.assertEqual(event["data"]["status"], "completed")
        self.assertEqual(event["data"]["success_criteria"][0]["evidence"], "Synthetic assertion only")
        self.assertEqual(len(provider._calls), 1)


if __name__ == "__main__":
    unittest.main()
