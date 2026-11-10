import json
import unittest
from types import SimpleNamespace as NS
from unittest.mock import Mock

from openai.types.responses import Response

from orderops.runtime import citations_from, run_agent
from orderops.tools import Dispatcher


def response(response_id, calls=None, text="Recommendation", status="completed"):
    return NS(id=response_id, output=calls or [], output_text=text, status=status,
              usage=NS(total_tokens=30))


def call(name="get_inventory", arguments='{"sku":"CD-100"}', call_id="call-1"):
    return NS(type="function_call", name=name, arguments=arguments, call_id=call_id)


class RuntimeTests(unittest.TestCase):
    def test_supported_response_continuation_and_agent_version(self):
        client = Mock()
        client.responses.create.side_effect = [response("resp-1", [call()]), response("resp-2")]
        reference = {"type": "agent_reference", "name": "local", "version": "7"}
        dispatcher = Dispatcher()
        recorder = Mock()
        result = run_agent(client, reference, "Check CD-100", dispatcher, on_response=recorder)
        self.assertEqual(result.calls, 1)
        self.assertEqual(result.tokens, 60)
        second = client.responses.create.call_args_list[1].kwargs
        self.assertEqual(second["previous_response_id"], "resp-1")
        self.assertEqual(second["input"][0]["call_id"], "call-1")
        self.assertEqual(second["input"][0]["type"], "function_call_output")
        self.assertEqual(json.loads(second["input"][0]["output"])["available"], 12)
        self.assertEqual(second["extra_body"]["agent_reference"]["version"], "7")
        self.assertEqual(recorder.call_count, 2)

    def test_multiple_calls_have_matching_outputs(self):
        client = Mock()
        client.responses.create.side_effect = [
            response("r1", [call(call_id="a"), call(call_id="b")]), response("r2")]
        run_agent(client, {}, "test", Dispatcher())
        outputs = client.responses.create.call_args.kwargs["input"]
        self.assertEqual([output["call_id"] for output in outputs], ["a", "b"])

    def test_round_budget_prevents_endless_loop(self):
        client = Mock()
        client.responses.create.side_effect = [response(str(i), [call()]) for i in range(10)]
        dispatcher = Dispatcher()
        with self.assertRaisesRegex(RuntimeError, "Tool budget"):
            run_agent(client, {}, "test", dispatcher, max_rounds=2)
        self.assertEqual(client.responses.create.call_count, 2)
        self.assertEqual(len(dispatcher.events), 1)

    def test_call_budget_checked_before_execution(self):
        client = Mock()
        client.responses.create.return_value = response("r", [call(), call()])
        dispatcher = Dispatcher()
        with self.assertRaises(RuntimeError):
            run_agent(client, {}, "test", dispatcher, max_calls=1)
        self.assertFalse(dispatcher.events)

    def test_empty_incomplete_and_error_do_not_pass(self):
        for candidate in (response("r", text=""), response("r", status="incomplete")):
            client = Mock()
            client.responses.create.return_value = candidate
            with self.subTest(candidate=candidate), self.assertRaises(RuntimeError):
                run_agent(client, {}, "test", Dispatcher())
        client.responses.create.side_effect = ConnectionError("offline")
        with self.assertRaises(ConnectionError):
            run_agent(client, {}, "test", Dispatcher())

    def test_input_and_budget_bounds(self):
        for prompt in ("", "x" * 8001):
            with self.assertRaises(ValueError):
                run_agent(Mock(), {}, prompt, Dispatcher())
        with self.assertRaises(ValueError):
            run_agent(Mock(), {}, "test", Dispatcher(), max_rounds=20)

    def test_real_sdk_response_citation_shape(self):
        value = Response.model_validate({
            "id": "resp-local", "object": "response", "created_at": 0, "status": "completed",
            "model": "fixture", "parallel_tool_calls": False, "tool_choice": "auto",
            "tools": [], "output": [{
                "id": "msg-local", "type": "message", "role": "assistant", "status": "completed",
                "content": [{"type": "output_text", "text": "Maximum 20",
                             "annotations": [{"type": "file_citation", "file_id": "file-local",
                                              "filename": "order-policy-2026-11.txt", "index": 0}]}],
            }],
        })
        self.assertEqual(value.output_text, "Maximum 20")
        self.assertEqual(citations_from(value)[0]["file_id"], "file-local")
        self.assertEqual(citations_from(value)[0]["filename"], "order-policy-2026-11.txt")
