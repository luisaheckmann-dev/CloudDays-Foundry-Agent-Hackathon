# Optionaler Stretch — echtes Foundry IQ, Fabric IQ und Work IQ

[Start](../../README.md) · [Architektur](../ARCHITECTURE.md) · [Quellen](../../SOURCES.md)

**Nicht Teil der Pflichtvoraussetzungen.** Vorbereitet als Instructor-Demo oder
nach abgeschlossenem Core, nicht als zusätzlicher Block in die 210 Minuten
hineinrechnen. Ohne diese Zusatzressourcen funktioniert der gesamte Pflichtpfad.
Die lokalen Dateien sind weder Fabric IQ noch Work IQ noch Foundry IQ.

## 1. Was wäre ein echter Integrationsnachweis?

| Baustein | Mindestnachweis | Reicht ausdrücklich nicht |
|---|---|---|
| Foundry IQ | existierende Azure-AI-Search-Knowledge-Base, Knowledge Source, tatsächlicher Retrieval-/MCP-Call, Quellenbelege | FileSearchTool umbenennen |
| Fabric IQ | tatsächliches Fabric-Item / semantischer Kontext und autorisierte Abfrage im Dienst, Quelle/Metrik nachvollziehbar | JSON aus `data` vorlesen |
| Work IQ | autorisierte echte Work-IQ-Abfrage gegen freigegebenen M365-Arbeitskontext mit Quellen | erfundene Mail-/Teamfixture |

Die genauen GA-/Previewgrenzen hängen von API-Version und Quelle ab.
Die aktuelle Search-Dokumentation unterscheidet **2026-04-01** für GA/minimale
extraktive Retrievalfunktionen und **2026-08-01-preview** für entsprechende
erweiterte/LLM-basierte Funktionen. Die hier referenzierten Portal-/Samplepfade
können Preview verwenden; keine pauschale GA- oder Produktionszusage.

## 2. Foundry IQ — separater Voraussetzungencheck

Vorher durch Instructor vollständig vorbereiten:

1. Eigenen oder ausdrücklich freigegebenen Azure-AI-Search-Service in unterstützter
   Region; passender Tarif für Managed Identity, RBAC aktiviert.
2. Synthetischen Index und Knowledge Source, daraus eine Knowledge Base.
   Eine Sammlung von Files/Vector Stores ist **keine** Search Knowledge Base.
3. Optional für LLM-Planung/Synthese: unterstütztes Azure-OpenAI-Deployment;
   Search-System-Managed-Identity mit **Cognitive Services User** auf der
   Modellressource. Modell/Region/Versionskompatibilität gesondert prüfen.
4. Provisionierende Identität: **Search Service Contributor** für KB/Index
   und **Search Index Data Contributor** für Daten.
5. Read-only Laufzeitidentität: **Search Index Data Reader** auf Search.
6. Neues Foundry-Projekt plus Rechte für RemoteTool-Verbindung.
7. Geprüfte Kosten und Cleanup-Ownershipliste.

Bei ACL-geschützten oder Remote-SharePoint-Quellen genügt eine globale
Serviceidentität **nicht** als Beleg für durchgängige Nutzerberechtigungen:
Quellberechtigungen, ACL-Metadaten und Nutzerkontextweitergabe gemäß
[offizieller Verbindungsanleitung](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/foundry-iq-connect)
testen. Ein für alle offener synthetischer Index beweist keine nutzerspezifische
Security Trimming.

## 3. Portalpfad mit vorbereiteter Knowledge Base

1. Öffne im richtigen **New Foundry**-Projekt **Build**.
2. Öffne **Knowledge**.
3. Verbinde den von der Lehrperson freigegebenen Search-Service oder wähle
   die dort vorbereitete Knowledge Base.
4. Wenn du selbst berechtigt anlegen darfst: wähle **Create knowledge base**,
   füge eine vorhandene Knowledge Source bzw. einen vorbereiteten Search-Index
   hinzu und prüfe Eigenschaften/Gültigkeit nach der
   [offiziellen KB-Anleitung](https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-how-to-create-knowledge-base).
   Bezeichnungen und Source-Dialoge hängen vom aktuellen Rollout ab.
5. Teste die Knowledge Base mit einer Frage, die nur der synthetische Index
   beantworten kann. Prüfe Retrievalantwort und Source References.
6. Öffne **Build → Agents** und einen **separaten** Stretch-Agenten, nicht den
   Pflichtagenten mit dessen manifestiertem File-Search-Vertrag.
7. Verbinde die Knowledge Base in der angebotenen Knowledge-/Tool-Konfiguration.
8. Frage nach einem konkreten Richtlinienfakt und prüfe den tatsächlichen
   Retrievalpfad sowie Quellen. Keine zusätzlichen Schreibtools hinzufügen.

Für den am 04.11.2026 sichtbaren deutschen Portalpfad:

1. **Erstellen → Wissen → Neue Ressource erstellen** zeigt mögliche
   Kapazitätsgrenzen. Ist eine Region ausgelastet, vor dem Erstellen eine
   verfügbare, organisatorisch zulässige Region wählen.
2. Im Azure-Portal den Tarif ausdrücklich kontrollieren. **Basic mit einer
   Replik und einer Partition** ist ein kleiner Managed-Identity-Demoaufbau;
   nicht versehentlich den Standardtarif oder mehrere Sucheineinheiten verwenden.
3. In Foundry die Search-Verbindung mit **Verwaltete Projektidentität** anlegen.
   Auf Search muss RBAC erlaubt sein (**Keys → API Access control → Both**
   oder **Role-based access control**, abhängig vom genehmigten Authentifizierungsplan).
4. **Erstellen einer Wissensdatenbank → Dateien hochladen** öffnet nach der
   Dateiauswahl **Wissensquelle erstellen**. Bei Embeddings gegebenenfalls
   **Grant access** nutzen: die **Search-Identität** benötigt Modellzugriff auf
   der richtigen Foundry-Ressource. Warten, bis die Dateien verarbeitet sind;
   „Quelle aktiv, 0 Dateien“ genügt nicht.
5. Für echte LLM-Planung ein unterstütztes Chatdeployment und
   **Abrufbegründungsaufwand: Niedrig** wählen. **Minimal** hat keine
   LLM-Abfrageplanung. **Extrahierte Daten** lässt den Agenten auf Quellen aufbauen.
6. Wissensdatenbank speichern, dann **In einem Agent verwenden** und den
   separaten IQ-Agenten auswählen. Neue gespeicherte Agentversion kontrollieren.
7. Auf **Search → Access control (IAM)** die **Foundry-Projektidentität**
   als **Search Index Data Reader** auf genau diesem Search-Service zuweisen.
   Das ist eine andere Richtung als Search → Modellzugriff.
   Keine Owner-/Contributor-Rolle als 403-Reparatur vergeben.
8. Nach RBAC-Propagation im neuen Chat erneut fragen. In
   **Agent → Ablaufverfolgungen → abgeschlossene Trace-ID** den
   **execute_tool … knowledge_base_retrieve**-Span öffnen und Ein-/Ausgabe prüfen.

**Erwartung:** Anfrage erreicht die Knowledge Base und liefert deren Quellen.
Je nach gewähltem Retrievalmodus erfolgt Planung/Synthese; ein minimaler
extraktiver Modus behauptet keine LLM-basierte Suchplanung.

**Recovery:** 403 → zugewiesene Laufzeitidentität und Search-Rolle prüfen;
leere Ergebnisse → Index, Source, Scope und Frage prüfen; keine verfügbare
Knowledge-Ansicht → aktuellen Rollout und offizielle Anleitung nutzen,
nicht File Search als Ersatz-IQ ausgeben.

## 4. SDK-/MCP-Pfad: genauen offiziellen Vertrag verwenden

Die [offizielle Anleitung „Connect Agents to Foundry IQ Knowledge Bases“](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/foundry-iq-connect)
zeigt den **Prompt-Agent-Pfad**:

1. Vorhandene KB besitzt einen Endpoint nach dem Muster
   `https://<search>.search.windows.net/knowledgebases/<kb>/mcp?api-version=2026-08-01-preview`.
2. Eine **RemoteTool-Projektverbindung** authentifiziert gegenüber diesem
   Endpoint, im dokumentierten Beispiel per **ProjectManagedIdentity**.
3. Der Prompt Agent erhält ein **MCPTool** mit passender Projektverbindung.
4. Exponiert wird gezielt **knowledge_base_retrieve**; keine fremden MCP-Tools
   pauschal freigeben.
5. Antwortquellen sowie Identitäts-/Berechtigungsfluss separat prüfen.

Dieses Repo registriert diese Verbindung **nicht automatisch** und enthält
keinen scheinbaren KB-Client, der intern die lokale Fixture liest.
Folge bei tatsächlicher Einrichtung dem vollständigen offiziellen Beispiel;
Preview-ARM-Verbindungsvertrag und Projekt-ID nicht aus dem Core-Manifest erraten.

## 5. Optional: ausführbares Python als Hosted Agent — anderer Pfad

**Exakte Referenz:** [Foundry-Samples / Responses / 17-foundry-iq-toolbox](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents/agent-framework/responses/17-foundry-iq-toolbox).
Das Beispiel enthält `provision_kb.py`, `toolbox.yaml`, Hookskripte, Manifest
und einen echten Responses-Host.

Am **04.11.2026** geprüfter Quellstand:

- `FoundryChatClient` kommt aus `agent_framework.foundry`.
- `FoundryToolbox` und `ResponsesHostServer` kommen in dessen `main.py` aus
  **`agent_framework_foundry_hosting`**. Nicht blind ältere Importzeilen kopieren.
- Sample-Pythonvoraussetzung laut `pyproject.toml`: **≥3.13**.
- Modellbeispiel `gpt-5.4-mini` bewusst durch ein tatsächlich verfügbares
  unterstütztes Deployment ersetzen, nicht dessen Verfügbarkeit versprechen.

### Isolierter Instructor-Aufbau

Diese Befehle sind **Anleitungen**, bei der Repositoryerstellung nicht ausgeführt.
Nur nach Genehmigung in einer separaten ignorierten Arbeitskopie verwenden:

```powershell
# Aus dem Workshop-Repository, Core-.venv bleibt unberührt.
New-Item -ItemType Directory -Path .local\iq-reference -Force | Out-Null
Set-Location .local\iq-reference
azd version
azd ext install microsoft.foundry
az login
azd ai agent init -m "https://github.com/microsoft-foundry/foundry-samples/blob/main/samples/python/hosted-agents/agent-framework/responses/17-foundry-iq-toolbox/azure.yaml"
```

1. Im Init-Dialog eigenes freigegebenes Foundry-Projekt und tatsächliches Modell
   wählen. Keine unbekannte Subscription oder automatische neue Infrastruktur bestätigen.
2. Vor Provisioning die erzeugten Dateien und die aktuelle Sample-README lesen.
   Der top-level `postprovision`-Hook muss ausdrücklich registriert sein und auf
   den tatsächlich erzeugten `src\<agent-name>\hooks\postprovision.ps1` zeigen.
   Service-scoped Hooks sind dafür nicht gleichwertig.
3. Den vorhandenen genehmigten Search-Service konfigurieren:

   ```powershell
   azd env set AZURE_SEARCH_ENDPOINT "https://EUER-SEARCH-SERVICE.search.windows.net"
   ```

4. Erst nach Ressourcen-/Kostenprüfung `azd provision` gemäß Sample ausführen.
   Der Hook erstellt Index/KB, RemoteTool-Verbindung und Toolbox.
5. `TOOLBOX_ENDPOINT` zeigt anschließend auf den Foundry-Toolbox-MCP-Endpoint;
   die Toolbox vermittelt zur echten Search-KB.
6. Mit dem im Sample dokumentierten lokalen Hostingablauf starten und in einem
   zweiten Terminal testen:

   ```powershell
   azd ai agent invoke --local "What can you tell me about the Earth at night?"
   ```

7. Nur bei explizit gewolltem Cloudhosting dem offiziellen
   [Hosted-Agent-Deploymentguide](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/deploy-hosted-agent)
   folgen. Für die neu erzeugte Agentidentität die nötige Search-Reader-Rolle
   **nach** deren Erzeugung am korrekten Scope prüfen.

**Unterschied:** Beim Hosted Agent wird ausführbarer Pythoncode tatsächlich als
Dienst bereitgestellt. Unser Pflicht-`register` stellt nur einen Prompt Agent
mit Toolmetadaten bereit und ist kein Hosted-Agent-Deployment.

**Cleanup:** Sample-Ressourcen stehen nicht im Core-Manifest. Eigene KB,
Knowledge Source, Index, Connection, Toolbox, Agentversion/Compute und optional
neu erzeugte Infrastruktur anhand separater Ownershipliste aufräumen. Kein
unbesehenes `azd down` auf geteilten Projekten.

## 6. Fabric IQ — nur mit vorbereitetem Geschäfts-/Semantikkontext

**Separate Voraussetzungen:** passender Fabric-Workspace und Capacity/Lizenz
für die konkret eingesetzten Features, freigegebene Items, Rollen und
Tenantsettings. Teilnehmer benötigen dies **nicht** für den Core.
Referenzen: [Fabric IQ](https://learn.microsoft.com/en-us/fabric/iq/overview) und
[Microsoft IQ Samples](https://github.com/microsoft/iq-samples).

Instructor-Demo:

1. Einen ausschließlich synthetischen Geschäftsbestand in einem echten Fabric-
   Item vorbereiten und seine fachliche Semantik zeigen, z. B. „verfügbar“
   im Unterschied zu „physisch“ und „reserviert“.
2. Vorhandenes semantisches Modell/Ontology-/Data-Agent-Szenario mit richtiger
   Item- und Workspaceberechtigung wählen; Previewstatus jeweils offenlegen.
3. Einen tatsächlichen Dienstaufruf durchführen und Antwort/Abfrage gegen
   die Quelldaten prüfen. Ein gesonderter read-only Adapter kann diesen Kontext
   später in Foundry integrieren, ist **nicht im Core enthalten**.
4. Identität, Datenfrische und definierte Kennzahl benennen.

**Erwartung:** semantischer Geschäftskontext aus Fabric ist nachgewiesen.
Nur Daten aus Fabric zu exportieren und später lokal zu lesen ist höchstens
ein Exportfixture, keine aktuelle Fabric-IQ-Liveintegration.

**Fallback:** `data\inventory.json` mit Kennzeichnung „lokaler synthetischer
Snapshot“ verwenden. Gleiches Geschäftsproblem, **kein** Fabric-IQ-Nachweis.

## 7. Work IQ — nur genehmigter M365-Arbeitskontext

Aktuelle Referenz: [Microsoft Work IQ CLI](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/work-iq/cli).
Die am 04.11.2026 geprüfte Seite nennt Node.js, administrativen Consent, einen
Copilot-Studio-Nutzungsabrechnungsplan und die Nutzerzuordnung dazu. Lizenz-,
Pay-as-you-go- und Tenantvoraussetzungen **für den konkreten Zugang** prüfen;
„jeder braucht M365 Copilot“ wäre ebenso pauschal falsch wie „immer kostenlos“.

Instructor-Demo ausschließlich mit freigegebenem Demokonto/-kontext:

1. Aktuellen unterstützten Work-IQ-CLI-Build nach Organisationsrichtlinie
   auswählen und isoliert vorbereiten, nicht global ungefragt installieren.
2. Nutzungsbedingungen selbst prüfen/akzeptieren und nur genehmigten
   Tenant-Consent verwenden. Kein Consent wird durch dieses Repo erteilt.
3. Eine bewusst synthetische, freigegebene Demoarbeitsquelle nutzen, z. B.
   Projektbesprechung zur fachlichen Bestellpriorität.
4. Einen tatsächlichen `workiq ask -q "..."`- oder genehmigten MCP-Aufruf
   ausführen; Quelle und berechtigten Kontext nachvollziehen.
5. Ergebnis zunächst als **separate Work-IQ-Demo** bezeichnen. Ohne zusätzliche
   unterstützte Verbindung ist es nicht automatisch Tool des Core-Foundry-Agenten.
6. Keine echten Mails/Personen/Ergebnisse in dieses Repository oder öffentliche
   Screenshots übernehmen; keine Work-IQ-Schreibtools ungeprüft aktivieren.

**Fallback:** fachliche Rückfrage „Welcher Kontext fehlt uns?“ besprechen.
Keine erfundene Mail als echte Work-IQ-Ausgabe präsentieren.

## 8. Abschließende Beweisfrage

„Welcher Dienst wurde mit welcher Identität wirklich aufgerufen, was war dessen
Quelle, und welche Integration ist nur geplant?“ Wenn diese Frage nicht
beantwortet werden kann, bleibt der entsprechende IQ-Teil **nicht verifiziert**.
