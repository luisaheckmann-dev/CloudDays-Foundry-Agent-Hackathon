import json
import shutil
import sqlite3
import uuid
from contextlib import closing

from orderops.business import inventory, propose, save_approved
from orderops.config import LOCAL, ROOT
from orderops.state import diagnostic


def dataset():
    return [json.loads(line) for line in
            (ROOT / "data" / "evaluation.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]


def offline_checks():
    """Domain controls only. Does not score any generated model answer."""
    results = []
    for case in dataset():
        if "quantity" not in case:
            results.append({"id": case["id"], "status": "NOT_RUN",
                            "reason": "Semantik/Zitat erfordert echte Modellantwort; kein Offline-Pass."})
            continue
        try:
            propose(case["sku"], case["quantity"])
            allowed = True
        except ValueError:
            allowed = False
        assert allowed == case["allowed"], case["id"]
        results.append({"id": case["id"], "status": "PASS_DOMAIN_ONLY"})
    work = LOCAL / ("offline-check-" + uuid.uuid4().hex)
    work.mkdir(parents=True)
    try:
        db = work / "drafts.sqlite3"
        p = propose("CD-100", 2)
        assert save_approved(p, db, enabled=True, confirmation="nein")["status"] == "denied"
        assert not db.exists()
        assert save_approved(p, db, enabled=True, confirmation=f"APPROVE {p.id}")["status"] == "created"
        assert save_approved(p, db, enabled=True, confirmation=f"APPROVE {p.id}")["status"] == "duplicate"
        with closing(sqlite3.connect(db)) as connection:
            assert connection.execute("SELECT COUNT(*) FROM drafts").fetchone()[0] == 1
        assert inventory("CD-100")["available"] == 12
    finally:
        shutil.rmtree(work)
    print(json.dumps({"mode": "OFFLINE_DOMAIN_NOT_MODEL_EVALUATION", "cases": results,
                      "approval_and_idempotency": "PASS"}, indent=2, ensure_ascii=False))


def structural_checks(case, result, dispatcher, known_file_ids):
    checks = {
        "nonempty": bool(result.text.strip()),
        "citation_present_and_known": (not case["citation"] or any(
            c["file_id"] in known_file_ids for c in result.citations)),
        "inventory_called": (not case["inventory"] or any(
            e["tool"] == "get_inventory" for e in dispatcher.events)),
        "no_invalid_proposal": (case.get("allowed", True) or not dispatcher.pending),
        "only_allowed_tools_requested": all(e["tool"] in ("get_inventory", "propose_order")
                                           for e in dispatcher.events),
    }
    if case["id"] == "desired-citation":
        checks["current_filename_annotation"] = any(
            c.get("filename") == "order-policy-2026-11.txt" for c in result.citations)
    return checks


def cloud_evaluate(track, limit):
    from orderops.cloud import session
    output = LOCAL / "evaluation-results.jsonl"
    LOCAL.mkdir(exist_ok=True)
    failures = 0
    with session(track) as (invoke, state), output.open("w", encoding="utf-8") as handle:
        for case in dataset()[:limit]:
            try:
                result, dispatcher = invoke(case["prompt"])
                checks = structural_checks(case, result, dispatcher, state["file_ids"])
                record = {"id": case["id"], "mode": "CLOUD_STRUCTURAL_ONLY",
                          "checks": checks, "response": result.text, "citations": result.citations,
                          "tokens": result.tokens, "response_ids": result.response_ids,
                          "human_review": "REQUIRED", "human_focus": case["human_focus"]}
                failures += not all(checks.values())
            except Exception as error:
                failures += 1
                record = {"id": case["id"], "status": "ERROR", "error_type": type(error).__name__,
                          "human_review": "NOT_SCORED"}
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
            print(case["id"], record.get("checks", record.get("status")), "— menschliche Rubrik offen")
    diagnostic("evaluation", cases=limit, structural_failures=failures)
    print("Antworten privat in .local\\evaluation-results.jsonl; keine Freigaben, keine Cloud-Judge-Kosten.")
    if failures:
        raise RuntimeError(f"{failures} strukturelle Fehler; keine bestandene Modellevaluation behaupten.")
