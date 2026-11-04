# Sicherheit, Datenschutz, Berechtigungen und Kosten

[Start](../README.md) · [Architektur](ARCHITECTURE.md) · [Cleanup](labs/06-cleanup.md)

## Minimaler Zugriff statt pauschal Owner

Die genauen Berechtigungen hängen von Basic-/Standard-Agent-Setup,
Ressourcenverknüpfungen und Tenant-Richtlinien ab. Vor dem Workshop prüfen.
Foundry-Rollen wurden umbenannt; alte Anzeigen können noch „Azure AI …“ lauten.

| Identität / Tätigkeit | Kleinstmöglicher sinnvoller Scope / Rolle |
|---|---|
| Teilnehmer: Agenten erstellen/aufrufen | **Foundry User** am zugewiesenen Projekt; Modellzugriff auf dessen zugehöriger Foundry-Ressource gemäß Setup |
| Teilnehmer: Dateien in Projektstorage hochladen | **Storage Blob Data Contributor** am betroffenen Storage, wenn vom verwendeten File-Search-Setup benötigt |
| Instructor: neue Ressource/Modell/Projekt bereitstellen | dafür nötige Verwaltungsrolle nur auf dedizierter Workshopressource/RG, nicht dauerhaft bei allen Teilnehmenden |
| Role-Assignment-Verantwortlicher | Owner/User Access Administrator nur für berechtigte Administrierende am notwendigen Scope |
| Optional IQ: KB/Index erstellen | **Search Service Contributor** auf genau dem Search-Service |
| Optional IQ: Testdaten indexieren | **Search Index Data Contributor** auf genau dem Search-Service |
| Optional IQ: lesende Laufzeitidentität | **Search Index Data Reader** auf dem Search-Service |
| Optional IQ: Search ruft LLM auf | Search-Managed-Identity erhält **Cognitive Services User** auf der Modellressource |
| Optional IQ: Projekt-MCP-Verbindung erstellen | notwendige **Foundry Project Manager**-Berechtigung auf der Foundry-Ressource; nicht allen Teilnehmern geben |

Keine Rollenzuweisung erfolgt automatisch durch dieses Repo. Rechtefehler
beheben nicht die Programmcode-Validierung; umgekehrt ersetzt ein sicheres
lokales Gate keine Azure-RBAC- oder echte Backendautorisierung.

## Daten und Identitäten

- Nur synthetische Policies/Inventory hochladen. Keine echten Aufträge, PII,
  Mails, Teams-Chats, Kundendokumente oder Unternehmenssecrets.
- `.env.example` enthält ausschließlich Platzhalter; `.env`, `.local` und
  `.venv` sind ignoriert. Keine Access Tokens in Umgebungsdateien nötig.
- AzureCliCredential verwendet explizit den `az login`-Kontext. Optional pinnen
  entweder `AZURE_TENANT_ID` oder `AZURE_SUBSCRIPTION_ID` die richtige bereits
  angemeldete Identität pro Aufruf. Nicht beide zugleich setzen (CLI-Grenze).
  Die globale CLI-Standardsubscription bleibt unverändert.
  Kein stiller Managed-Identity-/VS-Code-Fallback.
- Bestehende Shell-Umgebungsvariablen haben Vorrang vor `.env`. Bei unerwartetem
  Projekt dies zuerst prüfen und bewusst korrigieren.
- Lokale Diagnose enthält IDs, Toolnamen, Status, Tokens und Dauer, keine
  Prompt-/Antwortvolltexte. Evaluationsergebnisse enthalten echte Modelltexte
  in `.local`, bleiben privat und sollen nach Nutzung entfernt werden.
- `.gitignore` verhindert nur Git-Commits, **nicht** OneDrive-Synchronisierung.
  Für private Ausgaben einen genehmigten lokalen Ordner außerhalb synchronisierter
  Verzeichnisse verwenden; der Workshop verwendet ausschließlich synthetische Daten.
- Cloudresponses und Uploads können dienstseitig gespeichert werden und sind
  im Manifest für gezieltes Cleanup erfasst. Dienstaufbewahrung/Auditretention
  nach Organisationsrichtlinie prüfen, Löschen ist keine Zusage sofortiger
  Entfernung aus allen Backups/Compliancekopien.
- Keine externen MCP-Server oder Internettools im Pflichtpfad. Prompt Injection
  als Datenproblem testen; keine echte Exfiltration zu Demonstrationszwecken.

## Lokale Freigabe: genaue Garantien

`propose_order` validiert und hält einen Vorschlag ausschließlich im Speicher.
Es ist kein Write-Tool. Ein Flag **und** eine exakte Terminalbestätigung sind
für die einzige Änderung, einen lokalen SQLite-Simulationsdatensatz, nötig.
Die Bestätigung muss zu SKU, Menge und Policy-Hash des angezeigten Vorschlags passen.
Vor Speicherung wird erneut validiert. SQL-Parameter und Primary Key erzwingen
Duplikatkontrolle; Bestand und andere Geschäftsdaten bleiben read-only.

Nicht garantiert: echte ERP-Reservierung, verteilte Mehrnutzerfreigabe,
Freigabe per M365-Identität, revisionssicheres Audit, echte Lieferfähigkeit.
Ein lokaler Dateibesitzer kann das Programm ändern. Für Produktion wären
serverseitige Autorisierung, Transaktionen, Rollen-/Vieraugenmodell und
immutable Audit erforderlich.

## Budgetgrenzen und Kostenfallen

- Jeder Cloudbefehl verlangt `--allow-cloud`; `--offline` wird nie automatisch
  als scheinbar erfolgreicher Ersatz verwendet.
- Pro Anfrage max. **4 Responses**, **6 lokale Function Calls**, je Response
  max. **3 dienstseitige Tool Calls**, **1200 Outputtokens** angefordert.
  Eingaben max. 8000 Zeichen; Chat max. 10 unabhängige Anfragen.
- Preflight: eine kleine Modellprobe bis 512 Outputtokens.
- Evaluation: standardmäßig 3, explizit höchstens 10 Fälle; keine automatischen
  LLM-Judge-Aufrufe. Bei zehn Fällen sind theoretisch bis zu 40 Responses und
  48.000 angeforderte Outputtokens möglich; Input-/Retrieval-/Reasoningtokens
  und jeweilige Abrechnung separat beachten. Das ist **kein Euro-Festpreis**.
- SDK-Retries sind deaktiviert; Fehler sichtbar. Manuelle Wiederholung kostet
  gegebenenfalls erneut. Upload pollt begrenzt und lädt nicht still doppelt hoch.
- File Search kann neben Modellkosten Speicher-/Toolkosten verursachen.
  Store läuft nach einem Tag Inaktivität ab; hochgeladene Files trotzdem gezielt löschen.
- Standard-Setups können bestehende Search-/Storage-Ressourcen verwenden.
  **Optional neu angelegtes Azure AI Search** hat eigene laufende Kosten,
  ebenso Hosted-Agent-Compute, Containerregistry und Telemetrie.
- Kein Fabric und kein M365 Work IQ im Pflichtpfad. Optional können zusätzliche
  Capacity-, Nutzungs- oder Lizenzkosten entstehen.

Instructor setzt vorher Kostenbudget und Alerts, Teamaufruflimit und ein
geeignetes Deployment fest. Azure-Budgetalarme sind in der Regel
**Benachrichtigungen, kein harter Ausgabenstopp**. Aktuelle Preise/Region/Modell
vor Ort prüfen; keine pauschale Kostenfreiheit versprechen.

Für Gruppen Quota vorab dimensionieren: Teams mal gleichzeitig gestartete
Anfragen mal gemessene Input-/Outputtokens pro Minute. Registrierung, Evaluation
und zehn Teams mit parallelen Requests dürfen nicht erstmals im Workshop auf
ein knappes Demo-Deployment treffen. Als Startplan höchstens zwei Teams je
Startwelle aufrufen lassen, 429 sichtbar behandeln und den genauen Quota-Wert
mit der Lehrperson vorab proben.

## Ressourcenbezogenes Cleanup

1. SDK-Manifest prüfen und über `cleanup` gezielt Versionen, Responses, Stores,
   Files löschen.
2. Den separaten eigenen Portalagenten manuell entfernen.
3. Optionale KB, Knowledge Source, Index, Connection, Toolbox, Hosted-Agent-
   Deployment nur nach eigener Ownershipliste und Freigabe entfernen.
4. Shared Modell/Foundry/Search/Storage/RG nicht pauschal löschen.
5. Noch kostenpflichtige dedizierte Infrastruktur mit Resource Owner nachbereinigen.
