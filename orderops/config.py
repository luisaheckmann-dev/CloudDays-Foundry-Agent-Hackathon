import os
import re
import sys
from dataclasses import dataclass
from importlib.metadata import version
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent
LOCAL = ROOT / ".local"
PINS = {"azure-ai-projects": "2.10.0", "azure-identity": "1.27.0", "openai": "3.42.1"}


def load_env():
    path = ROOT / ".env"
    if not path.exists():
        return
    for number, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            raise ValueError(f".env line {number}: expected KEY=VALUE.")
        key, value = line.split("=", 1)
        if not re.fullmatch(r"[A-Z][A-Z0-9_]*", key.strip()):
            raise ValueError(f".env line {number}: invalid key.")
        os.environ.setdefault(key.strip(), value.strip().strip("\"'"))


def check_packages():
    if sys.version_info < (3, 11):
        raise ValueError("Python 3.11+ required.")
    actual = {name: version(name) for name in PINS}
    if actual != PINS:
        raise ValueError(f"SDK version mismatch: {actual}; run scripts\\bootstrap.ps1.")
    return actual


@dataclass(frozen=True)
class Settings:
    endpoint: str
    model: str
    agent: str
    tenant: str = ""
    subscription: str = ""

    def __post_init__(self):
        if self.tenant and self.subscription:
            raise ValueError("Set only AZURE_TENANT_ID or AZURE_SUBSCRIPTION_ID, not both; "
                             "Azure CLI accepts only one selector for a token request.")

    @classmethod
    def read(cls):
        load_env()
        endpoint = os.environ.get("FOUNDRY_PROJECT_ENDPOINT", "").rstrip("/")
        model = os.environ.get("FOUNDRY_MODEL_DEPLOYMENT_NAME", "")
        agent = os.environ.get("FOUNDRY_AGENT_NAME", "")
        url = urlsplit(endpoint)
        if (url.scheme != "https" or not url.hostname
                or not url.hostname.endswith((".services.ai.azure.com", ".ai.azure.com"))
                or not re.fullmatch(r"/api/projects/[A-Za-z0-9._-]+", url.path)
                or url.query or url.fragment or url.username or url.port):
            raise ValueError("FOUNDRY_PROJECT_ENDPOINT: HTTPS project endpoint /api/projects/NAME required.")
        if any(not value or "YOUR" in value.upper() or "<" in value for value in (endpoint, model, agent)):
            raise ValueError(".env contains missing values/placeholders. Complete Lab 00.")
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,62}", agent):
            raise ValueError("FOUNDRY_AGENT_NAME: 1–63 letters/digits/-/_; choose a team-unique name.")
        subscription = os.environ.get("AZURE_SUBSCRIPTION_ID", "")
        if subscription and not re.fullmatch(
                r"[0-9a-fA-F]{8}(?:-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}", subscription):
            raise ValueError("AZURE_SUBSCRIPTION_ID must be a subscription GUID.")
        return cls(endpoint, model, agent, os.environ.get("AZURE_TENANT_ID", ""), subscription)
