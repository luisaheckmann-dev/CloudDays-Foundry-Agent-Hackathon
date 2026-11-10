import json
import time
from datetime import datetime, timezone

from orderops.config import LOCAL


def read_state(settings, *, create=False):
    path = LOCAL / "cloud-state.json"
    if path.exists():
        state = json.loads(path.read_text(encoding="utf-8"))
        if state["endpoint"] != settings.endpoint or state["agent_name"] != settings.agent:
            raise ValueError("Cloud manifest belongs to another project/agent. Clean up using the original .env first.")
        return state
    if not create:
        raise ValueError("No cloud manifest. Run upload and register first (Lab 02).")
    return {"endpoint": settings.endpoint, "agent_name": settings.agent,
            "vector_store_ids": [], "file_ids": [], "versions": [], "response_ids": [],
            "active_vector_store": None, "active_agent": None}


def save_state(state):
    LOCAL.mkdir(exist_ok=True)
    path = LOCAL / "cloud-state.json"
    pending = LOCAL / "cloud-state.new"
    pending.write_text(json.dumps(state, indent=2), encoding="utf-8")
    for attempt in range(7):
        try:
            pending.replace(path)
            return
        except PermissionError as error:
            # OneDrive and Windows scanners can briefly lock the destination.
            if getattr(error, "winerror", None) not in (5, 32, 33) or attempt == 6:
                raise
            time.sleep(min(0.05 * 2 ** attempt, 0.5))


def diagnostic(event, **fields):
    LOCAL.mkdir(exist_ok=True)
    record = {"time": datetime.now(timezone.utc).isoformat(), "event": event, **fields}
    with (LOCAL / "diagnostics.jsonl").open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")
