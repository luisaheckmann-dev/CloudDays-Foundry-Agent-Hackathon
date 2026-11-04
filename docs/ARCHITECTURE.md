# Architektur: was wirklich wo läuft

[Start](../README.md) · [Sicherheit & Kosten](SECURITY-COSTS.md)

```text
Mensch / VS Code / PowerShell
  │ explizit --allow-cloud + AzureCliCredential
  ▼
AIProjectClient (azure-ai-projects 2.10.0, Projects API v1)
  ├─ agents.create_version(PromptAgentDefinition)
  │    ├─ Deployment (vom Teilnehmer gewählt, kein Modell-Fallback)
  │    ├─ FileSearchTool → Vector Store → 2 synthetische Policy-Dateien
  │    └─ FunctionTool-METADATEN (keine Python-Bereitstellung)
  └─ get_openai_client() → Responses API
       ├─ agent_reference {name, version}; max. 4 Responses / Anfrage
       ├─ file_search: im Dienst ausgeführt → file_citation
       └─ function_call → lokaler Allowlist-Dispatcher (max. 6 Aufrufe)
            ├─ get_inventory → JSON-Snapshot, ausschließlich lesen
            └─ propose_order → validierter Vorschlag NUR im Speicher
                 │ pending_human_approval ≠ Speicherung
                 ▼
       LOKALES CLI-GATE außerhalb des Modells
       --enable-local-drafts UND exaktes APPROVE <id> am interaktiven Terminal
                 ▼
       .local/drafts.sqlite3 — SIMULATION, PK-idempotent, keine Bestellung
```

## Vertrauensgrenzen

- **Modelltexte sind keine Berechtigungsentscheidung.** Das Modell kann weder das
  Gate-Flag noch die Terminaleingabe setzen. `save_approved` ist nicht registriert.
- Nichtinteraktive/piped Standard-Eingabe wird vom CLI-Freigabegate verweigert;
  ein aus Modelltext weitergeleitetes `APPROVE` ist keine menschliche Bestätigung.
- `propose_order` und der Schreibpfad prüfen bekannte SKU, Ganzzahl (kein bool/float),
  1–20, Bestand und Sperre erneut. Aktuelle Policy ist als Workshop-Domainregel
  auch im Code erzwungen; Produktionsrichtlinien müssten versioniert zentral verwaltet werden.
- Policy-Dokumente sind Belege, keine ausführbaren Anweisungen. Eine Promptregel
  vermindert Injection-Risiken, beweist aber keine vollständige Abwehr. Die
  tatsächliche Sicherheitsgrenze ist die eingeschränkte Tool-Allowlist plus Code.
- Inventory ist ein statischer synthetischer Snapshot. Es gibt keine ERP-Verbindung,
  Reservierung, Subtraktion oder Lieferzusage.
- Idempotenz-ID = Hash aus Policy-ID, SKU und Menge. Zwei identische Vorschläge
  ergeben im **gesamten lokalen DB-Lebenszyklus** dieselbe Zeile. Für eine echte
  Order-API wäre eine autorisierte Geschäfts-/Request-ID und Transaktionslogik nötig.
- Ein lokaler Dateibesitzer kann Python/DB selbst ändern. Das Gate schützt vor
  Modell-gesteuertem Schreiben im unveränderten Workshopprogramm, nicht vor einem
  böswilligen Administrator. Kein Produktionsfreigabesystem oder Mehrnutzer-Backend.

## Ausführbare Dateien und klare Pfade

| Pfad | Verantwortung |
|---|---|
| [CLI](../orderops/__main__.py) | Explizite Cloudzustimmung, Chat, Smoke, getrennte lokale Freigabe |
| [Cloud](../orderops/cloud.py) | Clients, Upload/Index-Polling, versionierte Registrierung, gezieltes Cleanup |
| [Runtime](../orderops/runtime.py) | Unterstützter Responses-Toolloop mit `previous_response_id` und `call_id` |
| [Domain](../orderops/business.py) | Read-only Inventar, validierte Vorschläge, SQLite-Idempotenz |
| [Dispatcher](../orderops/tools.py) | Tool-Allowlist, strikte Parameter, keine dynamische Ausführung |
| [Starter](../starter/inventory.py) / [Solution](../solution/inventory.py) | Austauschbarer Inventaradapter; eigener Prompt pro Track |
| [Dataset](../data/evaluation.jsonl) | 10 synthetische Normal-/Negativfälle |

Die Version wird bei jeder SDK-Anfrage explizit referenziert. Eine neue
Registrierung setzt die aktive Version im ignorierten `.local/cloud-state.json`.
Ein Prompt-Edit allein ändert den Dienst **nicht**: erneut `register` ausführen.
Jede CLI-Chatfrage ist ein unabhängiger Kontext; nur die Toolfortsetzungen innerhalb
einer Frage sind verknüpft. So wächst kein unbegrenzter Verlauf.

## File Search und die drei IQ-Begriffe

| Baustein | Reale Bedeutung | Hier im Pflichtpfad |
|---|---|---|
| File Search | Agenttool mit Dateien und Vector Store, zitierfähige Retrieval-Ergebnisse | **Ja** |
| Foundry IQ | Azure AI Search Knowledge Base, agentic retrieval, Knowledge Sources, z. B. MCP | **Nein**; optional separat |
| Fabric IQ | Semantischer Geschäftskontext, z. B. Ontologien, semantische Modelle, Data Agents | **Nein**; JSON ist kein Fabric IQ |
| Work IQ | M365-Arbeitskontext aus Zusammenarbeit, Beziehungen und Arbeitsabläufen | **Nein**; ein Prompt/Fixture ist kein Work IQ |

## Warum Microsoft hier interessant ist — ohne Exklusivbehauptung

Foundry bündelt die Agentdefinition, Modellbereitstellung, Tools und betriebliche
Diagnose. Entra/RBAC, Azure AI Search und optionale Fabric-/M365-Kontexte können
innerhalb vorhandener Microsoft-Landschaften den Integrationsaufwand reduzieren.
Der Wert liegt in **passender Identität, Datenanbindung und Betrieb**, nicht darin,
dass andere Plattformen keine Agenten, RAG, Governance oder menschliche Freigaben könnten.
AWS und Databricks bieten ebenfalls Agent-, Retrieval- und Evaluationsbausteine.
Verglichen werden sollten reale Datenquellen, Berechtigungsweitergabe, Region,
Betriebsmodell, Kosten und Teamkompetenz. Diese Übung ist kein Featurebenchmark.

Hosted Agents sind ein **anderes Deploymentmodell**: ein ausführbarer Dienst/Container
mit zusätzlicher Infrastruktur. Eine FunctionTool-Definition lädt keine Python-Datei
in Foundry hoch. Siehe [optionale Erweiterungen](optional/IQ.md).
