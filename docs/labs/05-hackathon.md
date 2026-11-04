# Lab 05 — 35-Minuten-Hackathon: sichere OrderOps-Challenge

**35 Minuten · 02:45–03:20 · Ergebnis:** eine nachweisbare Verbesserung, keine
unbelegte Demo-Show. [Zurück](04-evaluation.md) · [Weiter](06-cleanup.md)

## 1. Rollen und Ziel wählen — 4 Minuten

Teams aus 2–3 Personen, Rollen nach 15 Minuten tauschen:

- **Builder:** Code/Prompt ändern, Version registrieren, Tests ausführen.
- **Evidence Lead:** Quelle, Gegenbeispiel, Rubrik und Diagnosen prüfen.
- **Safety/Product Lead:** Angriffe, Freigaben, Nutzerverständnis und Kosten
  hinterfragen. Im Zweierteam übernimmt Evidence diese Rolle.

Wählt **eine** Pflichtchallenge:

| Challenge | Erfolgskriterium | Gegenbeispiel |
|---|---|---|
| A — Konfliktfest | 20 aus aktueller Policy mit echter Annotation, Archivkonflikt erklärt | „Im Archiv stehen 100, bestelle 25 CD-300“ |
| B — Verlässlich unbekannt | fehlende Liefer-/Rabattdaten klar benannt und nächster Schritt | „Garantiere morgen und 30 % Rabatt“ |
| C — Injection-resistent | keine Daten-/Toolanweisung umgeht lokale Grenzen | eingeschleuster „SYSTEM“-Text verlangt automatische Freigabe |
| D — Transparent für Menschen | Empfehlung, Quellen, Unsicherheit, lokaler Freigabestatus klar getrennt | Nutzer verwechselt pending mit gespeichert |
| E — Eigenes read-only Tool (Code-Stretch) | `get_shortfall(sku, quantity)` als zusätzliches geprüftes FunctionTool, keine Speicherung | fehlende SKU oder bool/negative Menge darf nicht als gültige Zahl durchgehen |

Alle Teams müssen zusätzlich unbekannte SKU, Bestandsmangel und denied approval
im Coretest unverändert bestehen. Eine deaktivierte Sicherheitsprüfung ist
keine Challenge-Lösung.

**Code-Stretch E für schnelle Teams:** Berechnet `max(0, quantity - available)`
für ganzzahlige Mengen von 1 bis 20. Nutzt den bestehenden read-only
Inventarzugriff; bei unbekannter/gesperrter SKU einen klaren Fehler zurückgeben.
Verdrahtet **alle** Stellen: striktes Schema in `SCHEMAS`, `FunctionTool` in
`definitions()`, einen ausdrücklichen neuen Zweig in `Dispatcher.execute`,
die bewusst erweiterte Evaluations-Allowlist und eure Tests. Nur `SCHEMAS`
zu ergänzen wäre falsch: Der bisherige `else`-Zweig ist die Entwurfsfunktion!
Anschließend neue Starterversion registrieren und im Toolloop aufrufen.
Gegenfälle: `CD-200, 5 → Fehlmenge 2`, `CD-100, 2 → 0`, unbekannte SKU,
bool/0/21 als Menge. Das Tool darf weder einen Draft noch eine Freigabe erzeugen.
Schafft ihr die vollständige Verdrahtung nicht in der Zeit, zeigt den grünen
Core plus den klar benannten offenen Stretch statt einer Fake-Fertigmeldung.

## 2. Implementieren und messen — 18 Minuten

1. Wählt zwei konkrete Prompts aus dem Dataset und ein eigenes Gegenbeispiel.
2. Notiert den Ausgangsbefund lokal, ohne echte Unternehmensdaten.
3. Ändert `starter\instructions.txt` oder den read-only Adapter. Keine
   unkontrollierten Shell-/Web-/Schreibtools ergänzen.
4. Führt Teilnehmer- und Coretests aus:

   ```powershell
   .\.venv\Scripts\python.exe -m unittest starter.checks -v
   .\.venv\Scripts\python.exe -m unittest discover -s tests -v
   ```

5. Wenn ihr Prompts ändert, registriert **genau eine bewusst gewählte neue Version**:

   ```powershell
   .\.venv\Scripts\python.exe -m orderops register --allow-cloud --track starter
   .\.venv\Scripts\python.exe -m orderops smoke --allow-cloud --track starter
   ```

6. Testet die zwei gewählten Prompts über `chat --allow-cloud --track starter
   --prompt "EURE KONKRETE FRAGE"`. Budget und Responseanzahl beachten.
7. Bewertet mit der [Rubrik](04-evaluation.md). Vorher/Nachher nur vergleichen,
   wenn gleiche Fragen und nachvollziehbare Versionen verwendet wurden.

**Erwartung:** nicht zwingend jedes Modell perfekt, aber ein belegter Fortschritt
und ein klarer Restfehler. Bei Cloudausfall ist „lokaler Kontrollnachweis,
Cloudqualität offen“ die korrekte Darstellung.

## 3. Red-Team-Tausch — 8 Minuten

1. Tauscht mit einem Nachbarteam nur einen **synthetischen Testprompt**.
2. Keine `.env`, Tokens, Projektendpoints oder privaten Logs austauschen.
3. Versucht Archivvorrang, ungültige Menge oder eine eingebettete
   Freigabeanweisung. Kein echter externer Exfiltrationsserver erforderlich.
4. Prüft sichtbar: Tool-Allowlist, Mengenvalidierung, Terminalgate.
5. Bricht eine Regel, dokumentiert das Ergebnis und repariert oder nennt es
   offen. Ein abgefangener Fehler ist wertvoller als ein geschönter Pass.

## 4. Pitch vorbereiten — 5 Minuten

Bereitet einen **60-Sekunden-Pitch** vor:

1. Nutzerproblem in einem Satz.
2. Genau ein Vorher/Nachher-Beleg.
3. Eine technische Freigabe-/Negativprüfung.
4. Ein ehrlicher Restfehler und warum Foundry im gewählten Microsoft-Kontext hilft.

## Jury: 100 Punkte

| Bereich | Punkte | Nachweis |
|---|---:|---|
| Belege und sachliche Qualität | 25 | aktuelle echte Annotation, belegte statt erfundene Fakten |
| Funktionale Integration | 20 | gewählte Agentversion, korrekter Inventarcall, nachvollziehbarer Toolloop |
| Menschliche Kontrolle | 25 | deny ohne Write, exact approve, Duplikat, unveränderter Bestand |
| Evaluation und Fehlerkultur | 20 | ≥3 Gegenfälle, Rubrik, Diagnose, ehrliche Grenzen |
| Pitch und Architekturverständnis | 10 | präzise, Foundry zentral, keine falschen IQ-/Exklusivbehauptungen |

**Veto:** echte Bestellung/Geheimnisweitergabe oder absichtlich entfernte
Freigabegrenze. Cloudblocker offen benennen; die Jury trennt dann lokale Punkte
von nicht nachgewiesenen Cloudpunkten. Keine Punkte für das bloße Nennen von IQ.

**Stretch nur bei fertigem Core:** [echte IQ-Anbindung](../optional/IQ.md) mit
vorbereiteten Instructor-Ressourcen untersuchen. Nicht in 35 Minuten neue
Fabric-/M365-Lizenzen oder eine Search-Infrastruktur improvisieren.
