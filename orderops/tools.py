import importlib
import json
from dataclasses import asdict

from orderops.business import propose

SCHEMAS = {
    "get_inventory": {
        "type": "object", "properties": {"sku": {"type": "string"}},
        "required": ["sku"], "additionalProperties": False,
    },
    "propose_order": {
        "type": "object",
        "properties": {"sku": {"type": "string"}, "quantity": {"type": "integer"}},
        "required": ["sku", "quantity"], "additionalProperties": False,
    },
}


def definitions():
    from azure.ai.projects.models import FunctionTool
    return [
        FunctionTool(name="get_inventory", strict=True, parameters=SCHEMAS["get_inventory"],
                     description="Read-only synthetic inventory snapshot. Not a real ERP."),
        FunctionTool(name="propose_order", strict=True, parameters=SCHEMAS["propose_order"],
                     description="Validate one SIMULATED proposal in memory. Does NOT write or approve."),
    ]


class Dispatcher:
    def __init__(self, track="solution"):
        if track not in ("starter", "solution"):
            raise ValueError("Unbekannter Track.")
        self.lookup = importlib.import_module(f"{track}.inventory").get_inventory
        self.pending = {}
        self.events = []

    def execute(self, name, arguments):
        try:
            if name not in SCHEMAS:
                raise ValueError("Tool nicht zugelassen.")
            if len(arguments) > 4096:
                raise ValueError("Argumente zu groß.")
            args = json.loads(arguments)
            if not isinstance(args, dict) or set(args) != set(SCHEMAS[name]["required"]):
                raise ValueError("Ungültige Parameter; keine Freigabeparameter erlaubt.")
            if name == "get_inventory":
                result = self.lookup(**args)
            else:
                proposal = propose(**args)
                self.pending[proposal.id] = proposal
                result = {**asdict(proposal), "status": "pending_human_approval"}
        except (ValueError, TypeError, NotImplementedError) as error:
            result = {"error": str(error), "status": "rejected"}
        self.events.append({"tool": name, "status": result.get("status", "read_only"),
                            "found": result.get("found")})
        return json.dumps(result, ensure_ascii=False)
