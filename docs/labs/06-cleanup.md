# Lab 06 — Pitch, gezieltes Cleanup und Schlusskontrolle

**10 Minuten · 03:20–03:30 · Ergebnis:** Kurzbeweis und keine vergessenen eigenen
Workshopartefakte. [Zurück](05-hackathon.md) · [Start](../../README.md)

## 1. Pitch — 4 Minuten

1. Die Lehrperson wählt 2–3 Teams für je 60 Sekunden aus.
2. Zeigt eine echte Quelle und eine abgelehnte Freigabe oder einen Negativtest.
3. Benennt den ausgeführten Pfad: Cloud Prompt Agent **oder** lokale Simulation.
4. Sagt ausdrücklich, ob es einen echten IQ-Knowledge-Base-/MCP-Nachweis gab.
   Der normale File-Search-Pfad darf nicht so bezeichnet werden.

## 2. Nur manifestierte SDK-Artefakte entfernen — 3 Minuten

1. Beendet Chats/Debugger. Keine parallelen Upload-/Register-/Cleanup-Prozesse starten.
2. Prüft lokal das Manifest:

   ```powershell
   Get-Content .local\cloud-state.json
   ```

3. Kontrolliert Projektendpoint, Agentname und die aufgelisteten Versionen,
   Files, Vector Stores und Responses. Das Cleanup löscht **nur diese IDs**.
4. Kopiert den exakten Agentnamen aus eurer eigenen `.env` als Bestätigung:

   ```powershell
   .\.venv\Scripts\python.exe -m orderops cleanup --allow-cloud --confirm "EUER-EXAKTER-AGENTNAME"
   ```

5. Erwartung: nur manifestierte Agentversionen, Responses, Vector Stores und
   Files entfernt. Bereits fehlende Ressourcen (404) gelten als entfernt.
6. Bei Teilfehler bleibt das Manifest erhalten. Fehler prüfen und denselben
   Befehl erneut ausführen. **Nicht** zuerst das Manifest löschen.

**Nicht gelöscht:** Foundry-Projekt/-Ressource, Modell, Azure AI Search, Storage,
Rollen, Resource Group, fremde Agenten, Portalagent, lokale Drafts. Auch eine
eintägige Vector-Store-Ablauffrist ersetzt dieses Cleanup nicht; hochgeladene
Dateien separat zu entfernen ist Teil des Befehls.

**Recovery:** Kein Manifest → wahrscheinlich nur Portal/Offline gearbeitet;
keine Cloud-IDs erraten. Anderes Projekt im Manifest → ursprüngliche `.env`
wiederherstellen und dort gezielt bereinigen. 403 → Lehrperson räumt exakt
die notierten IDs auf, nicht die ganze geteilte Resource Group.

## 3. Portalagent und lokale Daten bewusst bereinigen — 3 Minuten

1. Öffnet im Portal **Build → Agents**.
2. Sucht **exakt euren eigenen `…-portal`-Agenten** aus Lab 01.
3. Prüft Name/Projekt. Öffnet dessen Menü **… → Delete** bzw. die verfügbare
   versionsbezogene Löschaktion und bestätigt nur diesen eigenen Agenten.
4. Prüft im SDK-Agenten, dass die manifestierten Versionen verschwunden sind.
   Eventuelle andere, nicht von diesem Repo angelegte Versionen bleiben bestehen.
5. Erst nach abgeschlossenem Cloudcleanup lokale Daten entfernen, wenn gewünscht:

   ```powershell
   # Nur eigene lokale Workshopartefakte, keine Azure-Ressourcen:
   if (Test-Path .local\drafts.sqlite3) { Remove-Item .local\drafts.sqlite3 }
   if (Test-Path .local\evaluation-results.jsonl) { Remove-Item .local\evaluation-results.jsonl }
   if (Test-Path .local\diagnostics.jsonl) { Remove-Item .local\diagnostics.jsonl }
   ```

6. `.env` bei gemeinsam genutztem Rechner ebenfalls bewusst entfernen; Azure CLI
   ggf. mit `az logout` abmelden. Auf dem eigenen Rechner nach eigener Policy handeln.

**Instructor-Nachlauf:** Eigene Workshop-Modelldeployments, Search-KBs/Indexes,
Storage, optionale Hosted-Agent-Compute und Observabilityressourcen prüfen.
Nur dedizierte, eindeutig zugeordnete Ressourcen mit Genehmigung entfernen.
Es gibt hier absichtlich **keinen** pauschalen Resource-Group-Löschbefehl.

**Letzter Checkpoint:** Was ist Agentdefinition, wo läuft Python, welche Quelle
ist echt, wer durfte schreiben, welche Kostenressourcen bleiben bestehen?
