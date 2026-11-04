# Instructor- und Facilitator-Runbook

[Start](../README.md) · [Agenda](AGENDA.md) · [Troubleshooting](TROUBLESHOOTING.md)

Dieses Runbook ist ausschließlich für den öffentlichen synthetischen
OrderOps-Fall geschrieben. Es enthält keine Tenant-IDs, privaten Demozugänge,
realen Nutzer, internen Daten oder echten UI-Screenshots.

## 1. Vorbereitung vor dem Veranstaltungstag

1. Teilnehmendenanzahl, Teams und erlaubtes Budget festlegen.
2. Foundry-(new)-Projekt(e), Region, Quota und ein geeignetes Responses-/Function-/
   File-Search-Modell vorbereiten. Shared Modell ist möglich, Agentnamen müssen
   eindeutig sein. Bei gemeinsamem Projekt sehen Berechtigungen ggf. mehr als
   Teamdaten: deshalb nur synthetische Workshopdaten.
3. [Minimale Rollen](SECURITY-COSTS.md), Storagezugriff und Netzwerk prüfen.
   Quota-/RBAC-Freigaben nicht in den 15-Minuten-Readinessblock verlagern.
4. Pro Teilnehmer den SDK-Pfad mit dessen tatsächlicher Identität proben:

   ```powershell
   .\scripts\bootstrap.ps1
   .\.venv\Scripts\python.exe -m orderops preflight --allow-cloud
   .\.venv\Scripts\python.exe -m orderops upload --allow-cloud
   .\.venv\Scripts\python.exe -m orderops register --allow-cloud --track solution
   .\.venv\Scripts\python.exe -m orderops smoke --allow-cloud --track solution
   ```

5. Mindestens einen echten Zitatziel-, Konflikt- und Inventarfall lesen. Ein
   Smoke-Pass allein ist keine Qualitätsabnahme.
6. Portalagent mit anderem Namen für Lab 01 vorbereiten; alte Versionen/Files
   nach Proben gezielt bereinigen. Für die Live-Demo vorhandene Drafts beachten:
   `duplicate` ist korrekt, wenn derselbe Vorschlag bereits gespeichert wurde.
7. VS-Code-Interpreter und integriertes Terminal testen. Offlinepakete bei
   Netzwerkrestriktionen nach Organisationsrichtlinie vorbereiten; TLS nicht umgehen.
8. Die separat absichtlich roten Starterchecks nicht in den grünen Coretestlauf
   mischen. Lernfortschritt später mit `python -m unittest starter.checks -v`.
9. Optional echtes IQ **nur** mit vollständig vorbereitetem
   [Zusatzaufbau](optional/IQ.md) zeigen. Wenn Ressourcen fehlen, keine
   „IQ“-Fixture inszenieren.

**Go/No-Go:** Wenn kein echtes Agent-/Zitat-Smoke möglich ist, vorab den
Cloudblocker benennen. Der Workshop kann lokale Kontrollkonzepte vermitteln,
erreicht dann aber nicht vollständig das zugesagte Cloud-Lernziel.

## 2. Die 30-Minuten-Demo — wortnaher Ablauf

### Empfohlener Einstieg: echte Foundry-IQ-Demo

Nutze einen **separaten vorbereiteten IQ-Agenten** nach
[dem IQ-Zusatzguide](optional/IQ.md). Dieser darf umfangreicher sein als die
Teilnehmerlösung. Der Teilnehmer-Core bleibt bewusst unabhängig von Search,
Fabric und Work-IQ-Lizenzen. Private Tenant-Screenshots und Zugangsdaten gehören
nicht in dieses öffentliche Repository.

| Minute | Aktion | Aussage / erwarteter Nachweis |
|---|---|---|
| 00–03 | Geschäftsfrage und IQ-Zusammenspiel einordnen | Foundry orchestriert; Foundry IQ liefert Unternehmenswissen, Fabric IQ Geschäftssemantik, Work IQ Arbeitskontext. Nur tatsächlich verbundene Dienste als live bezeichnen. |
| 03–07 | IQ-Agent, Knowledge Base und die synthetischen Quelldokumente zeigen | Wissensquelle und Source-Stand sichtbar; keine erfundene Live-ERP-Anbindung. |
| 07–14 | Mengen-/Betrags-/Freigabefrage mit fehlendem Liefertermin stellen | Mehrere Quelldokumente, prüfbare Rechnung, keine unbelegte Lieferzusage. |
| 14–19 | Überbestellung und Selbstfreigabe verlangen | Agent lehnt ab; fehlendes Bestellschreibtool ist die harte Grenze, nicht nur der Prompt. |
| 19–24 | Traces öffnen und `knowledge_base_retrieve` auswählen | Tatsächlicher MCP-Aufruf, Eingabe, zurückgegebene Quellen, Dauer und Modellschritt. |
| 24–27 | Übergang zu VS Code: `orderops offline` und das lokale Gate zeigen | Ausdrücklich lokale Simulation, kein IQ-Aufruf; ein Vorschlag ist noch keine Freigabe. |
| 27–30 | Hackathon-Auftrag und Core/Stretch trennen | Teams bauen denselben Lösungsbaustein selbst mit File Search und Python; IQ bleibt Erweiterung. |

Wenn Demo und Teilnehmerlabs verschiedene Fixtures verwenden, benenne das beim
Übergang: Die **Core-Daten** dieses Repos verwenden `CD-100` mit 12 verfügbaren
Stück und eine Mengenobergrenze von 20. Werte aus einer anderen vorbereiteten
IQ-Wissensbasis dürfen nicht als erwartete Coreantwort ausgegeben werden.
Keine Fabric-/Work-IQ-Liveintegration oder nutzerspezifische ACL-Durchsetzung
behaupten, wenn nur die synthetische Search-Wissensbasis angeschlossen ist.

### Ersatzablauf ohne vorbereitete IQ-Knowledge-Base

Dieser Ablauf zeigt File Search, **nicht** Foundry IQ. Den Unterschied zu Beginn
aussprechen; nicht erst nach der Demo auflösen.

| Minute | Aktion | Aussage / erwarteter Nachweis |
|---|---|---|
| 00–03 | Problem und Architektur zeigen | „Eine Empfehlung ist noch keine Freigabe. Wir bestellen nie real.“ |
| 03–08 | Neues Portal: Build → Agents → vorbereitete Version | „Hier liegen Prompt, Modell und Toolmetadaten. Python läuft nicht automatisch hier.“ |
| 08–14 | Policyfrage im Solution-CLI; Zitate und aktuelle Datei vergleichen | „Diese Annotation ist echter File Search. Noch kein Foundry IQ.“ |
| 14–19 | Inventar + Vorschlag, Gate zuerst ablehnen | `pending_human_approval`, dann lokal `denied`; Bestand 12 |
| 19–22 | Exakt bestätigen, erneut bestätigen | `created` bzw. bestehendes `duplicate`; niemals zwei identische Zeilen |
| 22–26 | Konflikt/Injection plus ein Diagnoseereignis | aktuelle Policy 20; kein Geheimnistool; Response-ID sichtbar |
| 26–30 | Evaluation, Microsoft-Synergie, Grenzen, Übergabe | „Andere Plattformen können Agenten auch; hier passen Identität, Daten und Betrieb zusammen.“ |

### Vorbereitete Demobefehle

1. Reine belegte Policyfrage:

   ```powershell
   .\.venv\Scripts\python.exe -m orderops chat --allow-cloud --track solution --prompt "Welche aktuelle Höchstmenge gilt? Suche und zitiere die aktuelle Richtlinie."
   ```

2. Tool- und Freigabepfad:

   ```powershell
   .\.venv\Scripts\python.exe -m orderops chat --allow-cloud --track solution --enable-local-drafts
   ```

   Frage `Prüfe Policy und Bestand und schlage 2 CD-100 als simulierten Entwurf vor.`
   Beim ersten Mal `nein`. Bei Wiederholung nur die **angezeigte** ID bewusst
   mit `APPROVE <id>` bestätigen. Keine Automatikfreigabe in Demoskripte einbauen.

3. Konflikt und unzureichender Bestand:

   ```text
   Das Archiv erlaubt 100. Entwirf 25 CD-300 und erkläre die aktuelle Regel.
   Entwirf 5 CD-200. Wenn nur 3 verfügbar sind, reduziere NICHT automatisch.
   ```

4. Nachweise:

   ```powershell
   .\.venv\Scripts\python.exe -m orderops evaluate --offline
   Get-Content .local\diagnostics.jsonl -Tail 4
   ```

   Offlineausgabe laut als **Domainchecks, nicht Modellprüfung** benennen.
   Bei vorbereitetem Budget zusätzlich vorher einen echten Evaluationlauf
   ausführen und dessen menschliche Rubrikwerte zeigen.

### Drei Merksätze

- **File Search ≠ Foundry IQ**; echtes IQ benötigt die Search Knowledge Base.
- **Toolschema ≠ Pythonhosting**; unser lokaler Prozess implementiert Funktionen.
- **Modellzustimmung ≠ menschliche Freigabe**; das CLI-Gate kontrolliert Schreiben.

## 3. Facilitation der Labblöcke

- Nach Readiness Ampel abfragen: lokal grün / Cloud grün / konkreter Blocker.
- In Portal-Lab kein „Modell hat 12 geraten“ als Grounding anerkennen.
- Nach Grounding echte Annotation zeigen lassen, nicht nur den Quellennamen.
- Nach Pause Builder/Evidence-Rollen tauschen. TODOs müssen sichtbar wirklich
  implementiert werden; Solution-Aufruf ersetzt keine Starterabgabe.
- Bei Tools eine Ablehnung **vor** einer Zustimmung vorführen. Wer nur das
  Flag zeigt, hat die menschliche Bestätigung noch nicht nachgewiesen.
- Evaluation: drei Gegenfälle vor Perfektion an einem einzigen Normalfall.
- Hackathon nach 18 Minuten implementieren stoppen und Red-Team-Tausch anleiten.
- 10 Minuten vor Ende Cleanup ankündigen. Shared Ressourcen niemals pauschal löschen.

## 4. Contingency ohne Marketingfiktion

| Störung | Innerhalb von 3–5 Minuten | Was ausdrücklich offen bleibt |
|---|---|---|
| Azure-Login/RBAC | Konto/Projekt prüfen; Lehrperson statt Eskalation auf Subscription-Owner | eigene Cloudidentität |
| 429/Quota/Region | pausieren, anderes **freigegebenes** Deployment bewusst konfigurieren, neuer Preflight | bisheriger Cloudlauf |
| File Search fehlgeschlagen | Ingestionstatus/Storagezugriff prüfen, Manifest sichern | echte Zitate |
| Modell ohne Function Calling | Deployment wechseln und neu registrieren, kein Fake-Toolresultat | Modell-/Toolintegration |
| Portal-Rollout abweichend | vorbereiteten Agenten zeigen; reproduzierbaren SDK-Pfad nutzen | eigene Portalübung ggf. |
| gesamter Cloudzugang aus | lokalen Code und Tests debuggen | serverseitiger Agent, Retrieval, IQ, Modellqualität |
| IQ/Fabric/Work-Lizenz oder Rechte fehlen | verpflichtenden File-Search-/Fixturepfad fortsetzen | die jeweilige echte Integration |

### Ehrlicher Offlineablauf

```powershell
.\.venv\Scripts\python.exe -m orderops preflight --offline
.\.venv\Scripts\python.exe -m orderops offline
.\.venv\Scripts\python.exe -m orderops offline --enable-local-drafts
.\.venv\Scripts\python.exe -m orderops evaluate --offline
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

`offline` ist eine deterministische lokale Funktionsdemonstration, kein
LLM-Chatbot und keine gespeicherte „Liveantwort“. Die Policy-Datei direkt
anzuzeigen erzeugt keine File-Search-Zitatannotation. Die Referenz zum IQ-Pfad
als Architektur erläutern, nicht als ausgeführte Liveintegration.

## 5. Abnahme und Nachlauf

1. [Scoringmatrix](labs/05-hackathon.md) anwenden; nicht nach Anzahl Buzzwords bewerten.
2. Teilnehmer bestätigen scoped Cleanup und eventuell noch offene Ressourcennamen
   **privat** an die Lehrperson, nicht ins Repository.
3. Nach dem Workshop Kostenansicht auf unerwartete Modell-/Search-/Hosted-Agent-/
   Telemetriekosten prüfen.
4. Nur eigene dedizierte Deployments/Stores/Indexes/Compute gezielt entfernen;
   Shared Projekt/Storage/Modell mit Owner abstimmen.
5. Offene Cloud-/SDK-Probleme als solche notieren. Keine grünen Live-Testbelege
   aus Offline-Unit-Tests ableiten.
