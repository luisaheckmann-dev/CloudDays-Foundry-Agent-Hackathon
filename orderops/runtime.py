import json
import time
from dataclasses import dataclass, field


@dataclass
class RunResult:
    text: str
    citations: list = field(default_factory=list)
    response_ids: list = field(default_factory=list)
    calls: int = 0
    tokens: int = 0
    latency_ms: int = 0


def citations_from(response):
    citations = []
    for item in response.output:
        if item.type != "message":
            continue
        for content in item.content:
            for annotation in getattr(content, "annotations", []):
                if annotation.type == "file_citation":
                    citations.append({"file_id": annotation.file_id,
                                      "filename": getattr(annotation, "filename", None),
                                      "index": getattr(annotation, "index", None)})
    return citations


def run_agent(client, reference, prompt, dispatcher, *, max_rounds=4, max_calls=6,
              max_output_tokens=1200, on_response=None):
    """Responses continuation, not classic Threads/Runs; injectable for offline tests."""
    if not 1 <= max_rounds <= 4 or not 1 <= max_calls <= 6:
        raise ValueError("Budget limits: 1..4 Responses, 1..6 local tool calls.")
    if not isinstance(prompt, str) or not prompt.strip() or len(prompt) > 8000:
        raise ValueError("Prompt: 1..8000 characters.")
    start = time.monotonic()
    result = RunResult("")
    request_input = prompt
    previous = None
    for round_index in range(max_rounds):
        kwargs = dict(input=request_input, max_output_tokens=max_output_tokens,
                      max_tool_calls=3, parallel_tool_calls=False,
                      extra_body={"agent_reference": reference})
        if previous:
            kwargs["previous_response_id"] = previous
        response = client.responses.create(**kwargs)
        if on_response:
            on_response(response)
        result.response_ids.append(response.id)
        usage = getattr(response, "usage", None)
        result.tokens += getattr(usage, "total_tokens", 0) or 0
        if getattr(response, "status", None) not in ("completed", None):
            raise RuntimeError(f"Response not completed: {response.status}; check budget/diagnostics.")
        result.citations.extend(citations_from(response))
        calls = [item for item in response.output if item.type == "function_call"]
        if not calls:
            result.text = response.output_text
            if not result.text.strip():
                raise RuntimeError("Empty response; do not count as success.")
            result.latency_ms = round((time.monotonic() - start) * 1000)
            return result
        if round_index == max_rounds - 1 or result.calls + len(calls) > max_calls:
            raise RuntimeError("Tool budget exhausted; no approval/write operation executed.")
        request_input = []
        for call in calls:
            result.calls += 1
            output = dispatcher.execute(call.name, call.arguments)
            request_input.append({"type": "function_call_output",
                                  "call_id": call.call_id, "output": output})
        previous = response.id
    raise RuntimeError("Response budget exhausted.")


def print_result(result):
    print(result.text)
    print("FILE-SEARCH CITATIONS:", json.dumps(result.citations, ensure_ascii=False))
    print(f"Diagnostics: {len(result.response_ids)} Responses, {result.calls} local tools, "
          f"{result.tokens} tokens, {result.latency_ms} ms.")
