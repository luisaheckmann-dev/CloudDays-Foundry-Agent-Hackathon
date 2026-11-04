# Lab 02 — File Search, Indexstatus, Versionen und echte Zitate

**30 Minuten · 01:10–01:40 · Ergebnis:** eine versionierte, dateigestützte
Agentantwort. Danach **10 Minuten Pause**. [Zurück](01-portal.md) · [Weiter](03-tools.md)

**Voraussetzung:** `.env` korrekt, Cloud-Preflight erfolgreich. Alle Terminalbefehle
im Repositoryordner. Dieser Lab deployed **Agentdefinition + Tool-Metadaten**,
keine gehostete Python-Anwendung.

## 1. Synthetische Belege untersuchen — 4 Minuten

1. Öffne in VS Code
   [aktuelle Richtlinie](../../data/policy/order-policy-2026-11.txt).
2. Markiere Policy-ID, Gültigkeit, Maximum **20**, Bestandsgrenze und Freigabe.
3. Öffne [Archiv](../../data/policy/archive-policy-2025.txt).
4. Prüfe: Maximum 100 ist ausdrücklich **zurückgezogen**.
5. Öffne [Inventar](../../data/inventory.json). `CD-100` hat **12**, `CD-200`
   hat **3**, `CD-400` ist gesperrt. Kein Dokument behauptet ein Lieferdatum.

**Erklärung:** Die zwei Policy-Dateien werden indexiert. Der JSON-Snapshot bleibt
lokal und wird später per Pythonfunktion gelesen. Die Angriffsdatei unter
`data\adversarial` wird bewusst **nicht** hochgeladen.

**Checkpoint:** Du weißt vor dem Modellaufruf, welche Antworten sachlich richtig sind.

## 2. Hochladen und vollständige Indexierung abwarten — 8 Minuten

1. Öffne das integrierte PowerShell-Terminal.
2. Starte explizit:

   ```powershell
   .\.venv\Scripts\python.exe -m orderops upload --allow-cloud
   ```

3. Warte auf **beide** Meldungen `[completed]` und `File Search bereit`.
4. Öffne anschließend lokal:

   ```powershell
   Get-Content .local\cloud-state.json
   ```

5. Prüfe, dass `file_ids` zwei IDs enthält und `active_vector_store` gesetzt ist.
   Endpoints und IDs aus diesem ignorierten Manifest nicht veröffentlichen.

**Was der Code tut:** Store mit eintägiger Inaktivitätsablauffrist erstellen,
Datei hochladen (`purpose="assistants"` ist auch im neuen Files-API der
unterstützte Uploadzweck), dem Store zuordnen und Status pollen. Dieser Parameter
bedeutet **nicht**, dass wir das alte Assistants-/Threads-/Runs-API nutzen.
Je Datei maximal 180 Sekunden Polling; Netzwerkaufrufe zusätzlich begrenzt.

**Erwartung:** erst nach erfolgreicher Indexierung wird der Store aktiv gesetzt.
Ein Upload allein ist noch kein suchbereites Dokument.

**Recovery:**

- **403 Upload:** Rolle **Storage Blob Data Contributor** auf dem tatsächlich
  verwendeten Projektstorage und Foundry-Rolle durch Lehrperson prüfen.
- **failed/cancelled/Timeout:** keinen Erfolg behaupten. Fehlermeldung und
  Manifest behalten, Ursachen prüfen. Nach gezieltem
  [Cleanup](06-cleanup.md) erneut hochladen.
- **Bereits ein Store vorhanden:** nicht mehrfach hochladen. Für dieses Lab
  vorhandenen Store verwenden; das Programm blockiert versehentliche Duplikate.
- **Store abgelaufen:** Cleanup entfernt auch bereits fehlende Objekte sicher;
  danach Upload und Registrierung wiederholen.

## 3. Den ersten referenzfähigen Agenten registrieren — 5 Minuten

1. Für einen zuverlässigen ersten Grounding-Beweis nutze bewusst die Referenz:

   ```powershell
   .\.venv\Scripts\python.exe -m orderops register --allow-cloud --track solution
   ```

2. Lies Name und **Version** in der Ausgabe.
3. Öffne im Portal **Build → Agents**, aktualisiere die Liste und wähle den
   Agentnamen aus `.env` (nicht den separaten `-portal`-Agenten).
4. Wähle, falls angeboten, die gerade registrierte Version.
5. Kontrolliere Modell, Instructions und Tools. Falls die UI Tooldetails nicht
   vollständig zeigt, öffne [cloud.py](../../orderops/cloud.py):
   `PromptAgentDefinition` enthält FileSearchTool und zwei FunctionTools.
6. Keine Tools im Portal entfernen: Der reproduzierbare Versionsstand kommt aus Code.

**Erwartung:** `Registriert: … Version … / solution`.
`active_agent` im Manifest entspricht exakt diesem Stand. Weitere `register`-
Aufrufe erzeugen neue Versionen, kein In-place-Patching.

**Checkpoint:** „Agentdefinition deployed“ ist korrekt. „Python ins Portal
deployed“ wäre hier falsch.

## 4. Eine Antwort mit technischer Zitatannotation prüfen — 8 Minuten

1. Stelle eine reine Policyfrage über den CLI:

   ```powershell
   .\.venv\Scripts\python.exe -m orderops chat --allow-cloud --track solution --prompt "Welche aktuelle Mengenobergrenze gilt? Suche die Policy und zitiere order-policy-2026-11.txt."
   ```

2. Lies unter der Antwort **FILE-SEARCH-ZITATE**.
3. Prüfe `filename`, `file_id` und die bekannte ID aus `file_ids` im Manifest.
4. Öffne die lokale aktuelle Richtlinie und prüfe, ob die zitierte Aussage
   wirklich enthalten ist: **20, OPS-2026-11**.
5. Vergleiche mit der Aussage „Quelle: order-policy-2026-11.txt“ **ohne**
   Annotation. Dieser bloße Text wäre kein technischer Retrievalnachweis.
6. Teste den Gesamtpfad mit explizitem Cloud-Smoke:

   ```powershell
   .\.venv\Scripts\python.exe -m orderops smoke --allow-cloud --track solution
   ```

**Erwartung:** reale Antwort, bekannte Zitatannotation und erfolgreiche lokale
read-only Inventarfunktion. Der Smoke fragt keine Entwürfe an und bietet kein
Schreibgate an. Ein Pass belegt diese Integrationsstruktur, **nicht** die komplette
semantische Qualität, alle Modellfälle oder echtes IQ.

**Recovery:** Leere Zitatliste → Prompt muss File Search verlangen; richtigen
Store/Agentversion prüfen, Ingestionstatus prüfen. Kein Dateiname als
nachträgliches Fakezitat hinzufügen. `incomplete` → begrenztes Ausgabebudget/
Reasoningbedarf des gewählten Modells mit Lehrperson prüfen; kostenbewusst anderes
freigegebenes Deployment wählen und Preflight + register + smoke erneut ausführen.

## 5. Starter und Versionswechsel vorbereiten — 5 Minuten

1. Ergänze im [Starterprompt](../../starter/instructions.txt) deine Regeln für
   aktuelle vs. archivierte Policy und fehlende Lieferzusagen.
2. Erkläre dem Partner: Der erfolgreiche Solution-Smoke hat deine noch offene
   Starter-Inventarfunktion **nicht** implementiert.
3. Belasse die aktive Solution-Version für den Moment. Erst in Lab 03
   registrierst du ausdrücklich `--track starter`.
4. Stoppe vor der Pause jeden Chat mit `exit` bzw. `Ctrl+C`.

**Abschlusscheckpoint:** Du hast einen echten File-Search-Beleg und weißt, dass
dieser Pfad **kein Foundry IQ Knowledge-Base-/MCP-Pfad** ist. Falls Cloud-Smoke
fehlgeschlagen ist: Fehlerstatus bleibt offen, auch wenn Offline-Tests grün sind.
