# Recovery-Karte: Diagnose vor Neuinstallation

[Start](../README.md) · [Readiness](labs/00-readiness.md)

**Grundregel:** Fehlerexitcode ist ein Fehler, kein automatischer Offline-Pass.
Nur synthetische, bereinigte Fehlermeldungen teilen. `.env`/Tokens nie posten.

| Symptom | Präzise Wiederherstellung |
|---|---|
| Falscher Arbeitsordner / `No module named orderops` | VS Code im Repositoryordner öffnen; `Get-Location`; `.\.venv\Scripts\python.exe -m orderops --help`. Nicht vom Parentordner aus ausführen. |
| `python` fehlt oder Store öffnet sich | `py -0p`, installierte 3.11+-Version wählen; `.venv` damit neu erstellen. |
| PowerShell blockiert `.ps1` | Einzelbefehle in Lab 00 ausführen; keine globale ExecutionPolicy ändern. |
| `ModuleNotFoundError azure...` | `.venv`-Interpreter wählen; `.\.venv\Scripts\python.exe -m pip install -r requirements.txt`, dann `-m pip check`. |
| 1.x/2.x-Mix oder alte OpenAI-Signaturen | `-m pip show azure-ai-projects openai azure-identity`; gepinnte Requirements in derselben `.venv` installieren. |
| Corporate Proxy / TLS | genehmigte Netzwerk-/CA-Konfiguration mit IT; niemals Zertifikatsprüfung deaktivieren. |
| `.env` Platzhalter / URL abgelehnt | echten Projektendpoint mit `/api/projects/NAME`, Deploymentnamen und eindeutigen Agentnamen setzen. Keine Keys nötig. |
| Trotz `.env` falsches Projekt | `Get-ChildItem Env:FOUNDRY*` lokal prüfen; alte Variablen bewusst entfernen, neues Terminal öffnen. Shellwerte haben Vorrang. |
| CredentialUnavailable / 401 | `az login`, `az account show`; bei Bedarf expliziten von Instructor vorgegebenen Tenant verwenden. |
| CLI verlangt nur einen Selektor | In `.env` entweder `AZURE_TENANT_ID` oder `AZURE_SUBSCRIPTION_ID` setzen, nicht beide. Bei mehreren angemeldeten Konten exakte Subscription-GUID verwenden; globale Standardsubscription muss nicht gewechselt werden. |
| 403 bei Projekt/Agent | Foundry-User-Scope und Rollenzuweisung prüfen; nach Propagation erneut anmelden. Keine pauschale Owner-Rolle verteilen. |
| 403 bei Upload | File-Search-Setup und tatsächliches Projektstorage prüfen; ggf. Storage Blob Data Contributor. |
| Deploymentname nicht gefunden | zugewiesenes Projekt und **Deploymentname**, nicht bloßen Modellnamen, prüfen. Preflight wiederholen. |
| 404 `agents` / falscher API-Pfad | neues Foundry-Projekt verwenden, nicht Hub-Connection-String/classic. SDK 2.10.0 und Projektendpoint kontrollieren. |
| 400 wegen Tool-/Modellunterstützung | Modell in Region tatsächlich für Responses + Function Calling + File Search freigegeben? Instructor wählt bewusst unterstütztes Deployment, dann Preflight/register/smoke. |
| 429 / Quota | Schleife stoppen. Retry-After/Quota mit Instructor prüfen; manuell später erneut oder bewusst anderes genehmigtes Deployment. |
| Timeout / Netzwerk | Endpoint/DNS/Private-Endpoint-Zugriff prüfen. Kein endloser Retry; fehlgeschlagene Cloudaktionen im Manifest kontrollieren. |
| Ingestion nicht completed | Fehlerstatus/Storage/Datei prüfen; nicht registrieren. Scoped cleanup, anschließend Upload erneut. |
| `Bereits ein Store vorhanden` | vorhandenen Store nutzen. Für absichtlichen Neuaufbau erst scoped Cleanup; nicht Manifest löschen und Ressourcen vergessen. |
| Store nach Veranstaltung nicht mehr nutzbar | eintägige Inaktivitätsablauffrist; gezielt bereinigen, neu hochladen und neue Agentversion registrieren. |
| Keine Zitatannotation | konkrete Policyfrage, richtigen Store und aktive Version prüfen; File Search explizit verlangen. Plaintext-Dateiname ist kein Ersatz. |
| `Kein aktiver starter-Agent` | `register --allow-cloud --track starter`. Starter und Solution werden nicht still gemischt. |
| Prompt geändert, Verhalten bleibt | Datei speichern **und** neue Version registrieren; Ausgabe/Manifestversion kontrollieren. |
| Starter-Inventar rejected | `NotImplementedError` in `starter\inventory.py` umsetzen; `python -m unittest starter.checks -v`. |
| Toolbudget erschöpft | unnötige Calls im Prompt vermeiden, klare Frage stellen. Keine Freigabe nach Fehler; Limits nicht blind entfernen. |
| Response `incomplete` | Ausgabe-/Reasoningbedarf und Modellwahl prüfen. Defaultbudget bewusst klein; erst freigegebenes geeignetes Modell wählen. Ein notwendiger Budgetedit in `runtime.py` erfordert erneute Tests und neue Kostenabschätzung. |
| Freigabe denied | Flag `--enable-local-drafts` **und** exakte angezeigte `APPROVE <id>`-Zeile nötig. `yes`, Modelltext und Pipes aus Agentantworten gelten nicht als Freigabe. |
| Schon beim ersten Demoauftritt `duplicate` | identischer Vorschlag wurde in derselben lokalen DB schon gespeichert. Korrektes Idempotenzverhalten; keine echte Bestellung. |
| SQLite gesperrt | eigene offenen DB-Viewer/Debuggerverbindungen schließen. Programm schließt Connections explizit. Keine beliebigen Systemprozesse beenden. |
| Windows/OneDrive sperrt `cloud-state.json` | Kurzzeitige Windows-Sperren werden begrenzt erneut versucht. Bei anhaltendem Fehler bleibt er sichtbar; `cloud-state.new` und vorhandenes Manifest sichern, eigene Datei-/Synczugriffe schließen und gezielt fortsetzen. Manifest nicht löschen, sonst fehlt die Cleanup-Zuordnung. Für echte private Daten einen genehmigten nicht synchronisierten Ordner nutzen. |
| Debugger wartet ohne Eingabe | integriertes Terminal verwenden; Debug Console ist kein `input()`-Terminal. |
| Keine Portaltraces | Telemetrieziel/Ansicht ggf. nicht vorhanden. Lokale Diagnosen + Response-IDs nutzen; kein automatischer OTel-Export in diesem Repo. |
| Cleanup Teilfehler | Manifest behalten, spezifischen Zugriff/Fehler korrigieren und denselben scoped Befehl wiederholen. |
| Manifest gehört zu anderem Projekt | alte `.env` wiederherstellen und alte Ressourcen gezielt bereinigen. Nicht mit fremden IDs weitermachen. |

## Reproduzierbarer lokaler Gesundheitscheck

```powershell
$env:PYTHONUTF8 = "1"
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m orderops preflight --offline
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m orderops offline
.\.venv\Scripts\python.exe -m orderops evaluate --offline
.\.venv\Scripts\python.exe scripts\check_links.py
```

Erst danach bei vorhandenen Rechten bewusst einen Cloud-Preflight/Smoke
ausführen. Keine erfolgreichen Offlinechecks als Live-Verifikation ausgeben.
