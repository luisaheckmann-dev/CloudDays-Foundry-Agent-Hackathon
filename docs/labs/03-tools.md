# Lab 03 — Python-Tools und eine echte lokale Freigabegrenze

**35 Minuten · 01:50–02:25 · Ergebnis:** eigener read-only Adapter und ein
debuggter, technisch abgetrennter SIMULATIONS-Schreibpfad.
[Zurück](02-grounding.md) · [Weiter](04-evaluation.md)

**Vorbedingung:** Lab 02 fertig. Cloudvarianten benötigen ein erfolgreiches
Deployment. Der Freigabepfad lässt sich alternativ vollständig offline beweisen.
Du änderst nur `starter` und für Challenges gezielt Tests/Prompts, nicht die
Sicherheitsgrenze, um einen Test künstlich grün zu bekommen.

## 1. Einen absichtlich roten Lerncheck grün machen — 7 Minuten

1. Öffne [starter/inventory.py](../../starter/inventory.py).
2. Führe die **separaten** Teilnehmerchecks aus:

   ```powershell
   .\.venv\Scripts\python.exe -m unittest starter.checks -v
   ```

3. Beide Checks melden zunächst `NotImplementedError`. Das ist ein sichtbarer
   Lernauftrag, **kein** erfolgreicher Starter.
4. Ersetze den TODO durch einen Aufruf des bereits importierten
   `inventory(sku)` und gib dessen Ergebnis unverändert zurück.
5. Lies vorher [business.py](../../orderops/business.py), Funktion `inventory`:
   keine Schreiboperation, `found=False` für unbekannte SKU, Quellen-/Fixturemetadaten.
6. Wiederhole die Teilnehmerchecks und die Coretests:

   ```powershell
   .\.venv\Scripts\python.exe -m unittest starter.checks -v
   .\.venv\Scripts\python.exe -m unittest discover -s tests -v
   ```

**Erwartung:** beide Lernchecks und alle Coretests grün. Du hast keinen zweiten
Lagerbestand implementiert und die JSON-Datei nicht verändert.

**Recovery:** KeyError bei unbekannter SKU → nicht auf `available` zugreifen,
wenn `found=False`. Leere/ungültige SKU → Validierungsfehler beibehalten, nicht
in erfundene Ware umwandeln. Referenz in [solution/inventory.py](../../solution/inventory.py)
nur bewusst zur Hilfe nehmen.

## 2. Den Starter registrieren und den Toolloop nachvollziehen — 7 Minuten

1. Ergänze im [Starterprompt](../../starter/instructions.txt) Regeln:
   get_inventory vor Bestandsempfehlung; keine unbekannten SKUs erfinden;
   propose_order nur als Vorschlag; keine Freigabe behaupten.
2. Entferne die nun erledigte Lab-03-TODO-Zeile. Die Lab-04-Aufgabe darf noch offen sein.
3. Registriere eine neue Version:

   ```powershell
   .\.venv\Scripts\python.exe -m orderops register --allow-cloud --track starter
   .\.venv\Scripts\python.exe -m orderops smoke --allow-cloud --track starter
   ```

4. Öffne [runtime.py](../../orderops/runtime.py) bei `run_agent`.
5. Folge dieser Kette:
   `responses.create` → `function_call` → `Dispatcher.execute` →
   `function_call_output` mit **demselben call_id** → neuer Response mit
   **previous_response_id**.
6. Suche im Request das versionierte `agent_reference`; wir verwenden
   keine Classic-Threads-/Runs-Schleife.

**Erwartung:** Modell wählt FunctionTool, aber **dein** Prozess führt Python aus.
File Search läuft im Dienst. Maximal 4 Responses, 6 lokale Aufrufe und 3
dienstseitige Toolaufrufe pro Response; keine Endlosschleife oder stillen SDK-Retries.

**Checkpoint:** Erkläre dem Partner, warum registrierte Parameter keine
gehostete Implementierung sind.

## 3. VS-Code-Breakpoints setzen — 8 Minuten

1. Öffne **Run and Debug** (Ctrl+Shift+D).
2. Wähle **OrderOps: Cloud / Starter (Kosten!)** aus `launch.json`.
3. Setze durch Klick links neben der Zeile drei Breakpoints:
   - [runtime.py](../../orderops/runtime.py): `output = dispatcher.execute(...)`.
   - [tools.py](../../orderops/tools.py): `proposal = propose(**args)`.
   - [business.py](../../orderops/business.py): `if not enabled or confirmation != ...`.
4. Starte mit **F5**. Das integrierte Terminal akzeptiert die menschliche Eingabe.
5. Frage:

   ```text
   Prüfe Policy und Bestand. Schlage einen simulierten Entwurf über 2 CD-100 vor.
   ```

6. Am ersten Breakpoint: **Variables** öffnen; `call.name`, `call.arguments`,
   `call.call_id` untersuchen.
7. Mit **F10** einzelne Schritte oder **F5** zum nächsten Breakpoint gehen.
8. Am Vorschlag prüfen: `quantity=2`, bekannte SKU und deterministische ID.
9. Bei der Terminalfrage zuerst **nein** eingeben.

**Erwartung:** `pending_human_approval` kommt vom Tool. Das Modell hat **noch
nichts gespeichert**. Nach „nein“ lautet der lokale Status `denied`.
Die Terminalentscheidung wird nicht als Modellparameter zurückgesendet.

**Recovery:** Kein Terminalinput → Debugkonfiguration muss
`console: integratedTerminal` verwenden, nicht Debug Console. Kein Breakpoint
im Vorschlag → Modell hat keinen Vorschlag angefordert; Ausgabe prüfen und
expliziter formulieren, nicht manuell einen Cloud-Pass behaupten.
Fehlender Starter-Agent → `register --track starter` erneut ausführen.

## 4. Freigabe, Duplikat und Bestand technisch prüfen — 8 Minuten

1. Ohne Gate-Flag:

   ```powershell
   .\.venv\Scripts\python.exe -m orderops offline --track starter
   ```

2. Erwartung: Inventar wird gelesen, Vorschlag entsteht, aber Schreibgate ist
   deaktiviert. Kein neuer Entwurf wird gespeichert.
3. Mit Gate-Flag:

   ```powershell
   .\.venv\Scripts\python.exe -m orderops offline --track starter --enable-local-drafts
   ```

4. Lies den angezeigten Entwurf. Bestätige **nur**, wenn du genau diese lokale
   Simulation willst, mit `APPROVE ` plus **exakt der angezeigten ID**.
   Für den unveränderten Datensatz ist sie `95103258c73acd7b`.
5. Wiederhole exakt denselben Befehl und dieselbe bewusste Bestätigung.
6. Erster Status: `created` (oder `duplicate`, falls zuvor schon freigegeben).
   Zweiter Status: **duplicate**, niemals eine zweite identische Zeile.
7. Prüfe nach erfolgreicher Freigabe:

   ```powershell
   Test-Path .local\drafts.sqlite3
   .\.venv\Scripts\python.exe -c "import sqlite3; c=sqlite3.connect(r'.local\drafts.sqlite3'); print(c.execute('SELECT id,payload FROM drafts').fetchall()); c.close()"
   Get-Content data\inventory.json
   ```

8. Bestand von CD-100 bleibt **12**. Es existiert keine echte Order, Reservierung
   oder ausgehende Bestellung. SQLite enthält nur Workshop-Simulationen.

**Wichtig:** Ohne Freigabe darf das Programm keine DB **anlegen**. Wenn schon
vorher eine DB existierte, darf es darin keine Zeile hinzufügen. Für diesen
Unterschied existiert ein isolierter Test, nicht nur `Test-Path`.

## 5. Negative Pfade und Abschluss — 5 Minuten

1. Stelle im Cloud-Starterchat:

   ```powershell
   .\.venv\Scripts\python.exe -m orderops chat --allow-cloud --track starter --enable-local-drafts
   ```

2. Teste nacheinander `5 CD-200`, `1 CD-999`, `1 CD-400` und `25 CD-300`.
3. Erwartung: Bestandsmangel, unbekannte SKU, Sperre und aktuelle Höchstmenge
   verhindern jeweils einen gültigen Vorschlag. Kein Approval-Prompt für diese Fälle.
4. Beende mit `exit`. Falls das Modell keinen Toolcall macht, wird kein
   Schreibpfad ausgeführt; das ist sicher, aber noch kein guter Funktionsnachweis.

**Abgabe:** Demonstriere eine Ablehnung und ein idempotentes Duplikat; nenne
den Breakpoint an der echten Vertrauensgrenze. Manipuliere keine Fixtures, um
eine unerlaubte Menge durchzulassen. Vollständiges [Architekturbild](../ARCHITECTURE.md).
