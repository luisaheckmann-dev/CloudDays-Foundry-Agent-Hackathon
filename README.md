# Azure: Building & Deploying AI Agents with Microsoft Foundry

**Cloud Days · 210 Minuten · Deutsch · Intermediate · Stand 04.11.2026**

## Contoso OrderOps: von Belegen zur kontrollierten Aktion

Baue einen **versionierten Foundry Prompt Agent**: Richtlinie suchen, synthetischen Bestand
mit lokalem Python prüfen, Empfehlung erklären und einen **lokalen simulierten Entwurf
nur nach expliziter menschlicher CLI-Freigabe** speichern. Keine echten Bestellungen.
Foundry ist die Agentenplattform; VS Code ist die lokale Tool-Laufzeit.

**Pflicht:** Azure-Zugang, vorbereitetes Foundry-Projekt (new), verfügbares Deployment,
Python 3.11+, VS Code, Azure CLI. **Nicht nötig:** Fabric Capacity oder M365-Copilot-Lizenz.
File Search ist hier **kein Foundry IQ**. Echte IQ-Integrationen sind separat optional.

## Loslegen

Repositoryordner in VS Code öffnen; alle Befehle im integrierten **PowerShell**-Terminal:

```powershell
.\scripts\bootstrap.ps1
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m orderops offline
```

Diese Befehle greifen **nicht** auf Azure zu. Falls Skriptausführung blockiert ist:
[Readiness](docs/labs/00-readiness.md) enthält den Weg ohne Policy-Änderung.

| Dein nächster Schritt | Guide |
|---|---|
| Ablauf und Lernziele | [210-Minuten-Agenda](docs/AGENDA.md) |
| Setup, Berechtigungen, Cloud-Preflight | [00 Readiness](docs/labs/00-readiness.md) |
| Agent im neuen Portal verstehen | [01 Portal](docs/labs/01-portal.md) |
| Datei-Upload, Index, Zitate, SDK-Version | [02 Grounding](docs/labs/02-grounding.md) |
| Eigene Python-Funktion + Freigabegate debuggen | [03 Code & Tools](docs/labs/03-tools.md) |
| Messen statt raten | [04 Evaluation & Diagnose](docs/labs/04-evaluation.md) |
| Team-Challenge | [05 Hackathon](docs/labs/05-hackathon.md) |
| Pitch & gezieltes Aufräumen | [06 Abschluss](docs/labs/06-cleanup.md) |

**Starter:** [starter](starter/inventory.py) enthält echte offene TODOs; dessen
separate Lernchecks sind anfangs absichtlich rot. **Referenz:** [solution](solution/inventory.py).
Nie stillschweigend zwischen Pfaden wechseln; `--track starter` bzw. `--track solution`.

## Für Lehrende

- [Demo- und Facilitator-Runbook](docs/INSTRUCTOR.md), [Architektur](docs/ARCHITECTURE.md)
- [Echtes Foundry IQ / Fabric IQ / Work IQ, optional](docs/optional/IQ.md)
- [Kosten, Datenschutz und Least Privilege](docs/SECURITY-COSTS.md)
- [Fehlerbehebung](docs/TROUBLESHOOTING.md), [Quellen](SOURCES.md), [MIT-Lizenz](LICENSE)

**Nachweisgrenze:** SDKs tatsächlich lokal installiert/Signaturen geprüft; Offline-Tests
und CLI ausführbar. Modell-Preflight und ein lesender Responses-/MCP-Aufruf gegen
einen separat vorbereiteten IQ-Agenten wurden zusätzlich live ausgeführt.
**Der vollständige Teilnehmerpfad File Search + lokale Funktionen ist damit noch
nicht live abgenommen.** Diesen Cloud-Smoke explizit nach Lab 02 ausführen:
`.\.venv\Scripts\python.exe -m orderops smoke --allow-cloud --track solution`.
Ein grüner Offline-Test ist kein bestandener Foundry-, IQ- oder Modellqualitätstest.
