import time
from contextlib import contextmanager

from orderops.config import ROOT, Settings, check_packages
from orderops.runtime import run_agent
from orderops.state import diagnostic, read_state, save_state
from orderops.tools import Dispatcher, definitions


@contextmanager
def clients(settings):
    from azure.ai.projects import AIProjectClient
    from azure.identity import AzureCliCredential
    kwargs = {"tenant_id": settings.tenant} if settings.tenant else {}
    if settings.subscription:
        kwargs["subscription"] = settings.subscription
    with AzureCliCredential(process_timeout=20, **kwargs) as credential:
        with AIProjectClient(endpoint=settings.endpoint, credential=credential,
                             retry_total=0, connection_timeout=15, read_timeout=60) as project:
            with project.get_openai_client(timeout=60.0, max_retries=0) as api:
                yield credential, project, api


def preflight():
    settings = Settings.read()
    check_packages()
    with clients(settings) as (credential, project, api):
        credential.get_token("https://ai.azure.com/.default")
        deployments = list(project.deployments.list())
        match = next((d for d in deployments if d.name == settings.model), None)
        if match is None:
            raise ValueError("Deployment name not found in project. Check Models + endpoints; no fallback.")
        response = api.responses.create(model=settings.model, input="Reply with the single word READY.",
                                        max_output_tokens=512)
        state = read_state(settings, create=True)
        state["response_ids"].append(response.id)
        save_state(state)
        if response.status != "completed" or not response.output_text.strip():
            raise RuntimeError("Model probe incomplete; check model/quota/budget.")
        print(f"Cloud preflight OK: explicit CLI identity, project reachable, deployment {match.name}.")
        print("Responses model probe passed; Function/File Search capability is checked only by smoke.")


def upload():
    settings = Settings.read()
    state = read_state(settings, create=True)
    if state["active_vector_store"]:
        raise ValueError("A store already exists. Reuse it or run cleanup first; no duplicate upload.")
    with clients(settings) as (_, _, api):
        store = api.vector_stores.create(name=f"{settings.agent}-policies",
                                         expires_after={"anchor": "last_active_at", "days": 1})
        state["vector_store_ids"].append(store.id)
        save_state(state)
        for path in sorted((ROOT / "data" / "policy").glob("*.txt")):
            with path.open("rb") as handle:
                uploaded = api.files.create(file=handle, purpose="assistants")
            state["file_ids"].append(uploaded.id)
            save_state(state)
            api.vector_stores.files.create(vector_store_id=store.id, file_id=uploaded.id)
            deadline = time.monotonic() + 180
            while True:
                item = api.vector_stores.files.retrieve(vector_store_id=store.id, file_id=uploaded.id)
                if item.status == "completed":
                    break
                if item.status != "in_progress":
                    raise RuntimeError(f"Indexing {path.name}: {item.status}; check error and cleanup.")
                if time.monotonic() >= deadline:
                    raise TimeoutError("Indexing >180s; not ready. No agent registered; cleanup is possible.")
                time.sleep(2)
            print(f"Indexed: {path.name} -> {uploaded.id} [completed]")
        state["active_vector_store"] = store.id
        save_state(state)
        print("File Search ready (not Foundry IQ).")


def register(track):
    from azure.ai.projects.models import FileSearchTool, PromptAgentDefinition
    settings = Settings.read()
    state = read_state(settings)
    store = state["active_vector_store"]
    if not store:
        raise ValueError("No completed indexing. Run upload first.")
    instructions = (ROOT / track / "instructions.txt").read_text(encoding="utf-8")
    with clients(settings) as (_, project, _):
        definition = PromptAgentDefinition(
            model=settings.model, instructions=instructions,
            tools=[FileSearchTool(vector_store_ids=[store], max_num_results=3), *definitions()],
        )
        agent = project.agents.create_version(
            agent_name=settings.agent, definition=definition,
            description="Contoso OrderOps: synthetic workshop; client-side tools; no real orders.",
            metadata={"workshop": "clouddays-orderops", "track": track},
        )
        record = {"name": agent.name, "version": agent.version, "track": track}
        state["versions"].append(record)
        state["active_agent"] = record
        save_state(state)
        print(f"Registered: {agent.name} version {agent.version} / {track}.")
        print("Only prompt + tool metadata deployed. Python still runs locally, NOT in Foundry.")


@contextmanager
def session(track):
    settings = Settings.read()
    state = read_state(settings)
    active = state["active_agent"]
    if not active or active["track"] != track:
        raise ValueError(f"No active {track} agent. Run register --track {track}.")
    reference = {"type": "agent_reference", "name": active["name"], "version": active["version"]}
    with clients(settings) as (_, project, api):
        project.agents.get_version(agent_name=active["name"], agent_version=active["version"])

        def record(response):
            state["response_ids"].append(response.id)
            save_state(state)
            usage = getattr(response, "usage", None)
            diagnostic("response", response_id=response.id, agent_version=active["version"],
                       status=response.status, tokens=getattr(usage, "total_tokens", None))

        def invoke(prompt):
            dispatcher = Dispatcher(track)
            try:
                result = run_agent(api, reference, prompt, dispatcher, on_response=record)
            except Exception as error:
                diagnostic("run_failed", error_type=type(error).__name__)
                raise
            diagnostic("run_completed", response_id=result.response_ids[-1],
                       calls=result.calls, latency_ms=result.latency_ms,
                       citations=len(result.citations), tokens=result.tokens,
                       tools=dispatcher.events)
            return result, dispatcher

        yield invoke, state


def cleanup(confirm):
    from azure.core.exceptions import ResourceNotFoundError
    from openai import NotFoundError
    settings = Settings.read()
    state = read_state(settings)
    if confirm != settings.agent:
        raise ValueError("--confirm must exactly match FOUNDRY_AGENT_NAME; inspect the manifest first.")
    failures = []
    with clients(settings) as (_, project, api):
        groups = [
            ("versions", lambda v: project.agents.delete_version(
                agent_name=v["name"], agent_version=v["version"])),
            ("response_ids", lambda r: api.responses.delete(r)),
            ("vector_store_ids", lambda v: api.vector_stores.delete(v)),
            ("file_ids", lambda f: api.files.delete(f)),
        ]
        for key, delete in groups:
            for value in list(state[key]):
                try:
                    delete(value)
                except (ResourceNotFoundError, NotFoundError):
                    pass
                except Exception as error:
                    failures.append(f"{key}: {type(error).__name__}")
                    continue
                state[key].remove(value)
                if key == "versions" and value == state["active_agent"]:
                    state["active_agent"] = None
                if key == "vector_store_ids" and value == state["active_vector_store"]:
                    state["active_vector_store"] = None
                save_state(state)
    if failures:
        raise RuntimeError("Cleanup incomplete; keep the manifest and retry: " + ", ".join(failures))
    print("Only manifested agent versions, Responses, vector stores and files removed.")
    print("Project, model, Search, Storage, roles and resource group were NOT deleted.")
