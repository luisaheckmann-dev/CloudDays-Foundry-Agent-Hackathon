import argparse
import json
import sys

from orderops.business import approval_gate, propose
from orderops.config import LOCAL, ROOT, check_packages
from orderops.runtime import print_result
from orderops.tools import Dispatcher


def parser():
    root = argparse.ArgumentParser(description="Contoso OrderOps — no real orders, no silent cloud fallback")
    sub = root.add_subparsers(dest="command", required=True)
    for name in ("preflight", "upload", "register", "chat", "smoke", "evaluate", "cleanup", "offline"):
        command = sub.add_parser(name)
        if name != "offline":
            command.add_argument("--allow-cloud", action="store_true", help="Explicit consent to cloud calls/costs")
        if name in ("preflight", "evaluate"):
            command.add_argument("--offline", action="store_true")
        if name in ("register", "chat", "smoke", "evaluate", "offline"):
            command.add_argument("--track", choices=("starter", "solution"), default="solution")
        if name in ("chat", "offline"):
            command.add_argument("--enable-local-drafts", action="store_true",
                                 help="Enable terminal approval gate, not automatic approval")
        if name == "chat":
            command.add_argument("--prompt")
        if name == "evaluate":
            command.add_argument("--limit", type=int, choices=range(1, 11), default=3)
        if name == "cleanup":
            command.add_argument("--confirm", required=True)
    return root


def offline_preflight():
    actual = check_packages()
    from azure.ai.projects.models import AgentReference, FileSearchTool, PromptAgentDefinition
    from orderops.business import inventory
    from orderops.tools import definitions
    assert inventory("CD-100")["available"] == 12
    assert not inventory("CD-999")["found"]
    assert propose("CD-100", 2).simulation
    assert len(definitions()) == 2
    definition = PromptAgentDefinition(model="LOCAL-SIGNATURE-CHECK", tools=[
        FileSearchTool(vector_store_ids=["LOCAL-NOT-A-CLOUD-ID"], max_num_results=3), *definitions()])
    assert definition.as_dict()["kind"] == "prompt"
    assert AgentReference(name="local", version="1").as_dict()["version"] == "1"
    print("OFFLINE OK:", sys.version.split()[0], json.dumps(actual))
    print("Fixtures and SDK serialization checked. Config/Credential/Project/Model: NOT_RUN.")


def offline(args):
    dispatcher = Dispatcher(args.track)
    print("OFFLINE — deterministic function simulation, NO Foundry/LLM/IQ call.")
    print(dispatcher.execute("get_inventory", '{"sku":"CD-100"}'))
    print("Local policy evidence (NO cloud citation annotation): data\\policy\\order-policy-2026-11.txt §2/§3")
    print(dispatcher.execute("propose_order", '{"sku":"CD-100","quantity":2}'))
    for proposal in dispatcher.pending.values():
        print(json.dumps(approval_gate(proposal, LOCAL / "drafts.sqlite3",
                                       enabled=args.enable_local_drafts), ensure_ascii=False))


def chat(args, *, smoke=False):
    from orderops.cloud import session
    with session(args.track) as (invoke, state):
        if smoke:
            prompt = ("Find the current policy using file_search, cite it and state the quantity limit. "
                      "Check CD-100 stock using get_inventory. Do not create drafts.")
            result, dispatcher = invoke(prompt)
            print_result(result)
            if not any(c["file_id"] in state["file_ids"] for c in result.citations):
                raise RuntimeError("SMOKE FAIL: no known File Search citation annotation.")
            if not any(e["tool"] == "get_inventory" and e["found"] for e in dispatcher.events):
                raise RuntimeError("SMOKE FAIL: no successful inventory call.")
            print("CLOUD SMOKE PASS: response + known citation annotation + local read-only function.")
            print("Not yet evidence of semantic quality or a check of all evaluation cases.")
            return
        count = 0
        while count < 10:
            try:
                prompt = args.prompt if args.prompt else input("OrderOps (exit to quit): ")
            except (EOFError, KeyboardInterrupt):
                break
            if prompt.strip().lower() in ("exit", "quit"):
                break
            result, dispatcher = invoke(prompt)
            print_result(result)
            for proposal in dispatcher.pending.values():
                outcome = approval_gate(proposal, LOCAL / "drafts.sqlite3",
                                        enabled=args.enable_local_drafts)
                print("LOCAL STATUS:", json.dumps(outcome))
            count += 1
            if args.prompt:
                break
        print("Session ended (maximum 10 independent requests; no unbounded conversation history).")


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        if args.command == "offline":
            offline(args)
            return 0
        if getattr(args, "offline", False):
            if args.allow_cloud:
                raise ValueError("--offline and --allow-cloud are mutually exclusive.")
            if args.command == "preflight":
                offline_preflight()
            else:
                from orderops.evaluation import offline_checks
                offline_checks()
            return 0
        if not args.allow_cloud:
            raise ValueError("Cloud blocked. Explicitly specify --allow-cloud or use --offline.")
        check_packages()
        from orderops import cloud
        if args.command == "preflight":
            cloud.preflight()
        elif args.command == "upload":
            cloud.upload()
        elif args.command == "register":
            cloud.register(args.track)
        elif args.command in ("chat", "smoke"):
            chat(args, smoke=args.command == "smoke")
        elif args.command == "evaluate":
            from orderops.evaluation import cloud_evaluate
            cloud_evaluate(args.track, args.limit)
        elif args.command == "cleanup":
            cloud.cleanup(args.confirm)
        return 0
    except Exception as error:
        print(f"ERROR [{type(error).__name__}]: {error}", file=sys.stderr)
        print("No offline fallback. Help: docs\\TROUBLESHOOTING.md", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    sys.exit(main())
