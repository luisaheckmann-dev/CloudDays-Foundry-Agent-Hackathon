# Lab 01 — Einen Prompt Agent im neuen Foundry verstehen

**25 Minuten · 00:45–01:10 · Ergebnis:** ein kleiner Portalagent und eine bewusst
unbeantwortbare Frage. [Zurück](00-readiness.md) · [Weiter](02-grounding.md)

**Voraussetzung:** Cloud-Preflight erfolgreich oder mit der Lehrperson geteiltes
Demo-Projekt. Die Portalschritte folgen **Foundry (new), nicht classic**.
Die UI wird laufend aktualisiert; gleichwertige Beschriftungen sind genannt.
Keine Function-Tool-Laufzeit im Browser erwarten.

## 1. Das richtige Projekt kontrollieren — 4 Minuten

1. Öffne <https://ai.azure.com>.
2. Aktiviere **New Foundry**, falls ein Versionsumschalter erscheint.
3. Wähle über den Projektwähler exakt dein zugewiesenes Projekt.
4. Wähle oben **Build**.
5. Wähle links **Agents**.

**Erwartung:** Agentliste des Projekts. Wenn du stattdessen Hubverwaltung,
Assistants oder ausschließlich klassische Threads/Runs siehst, nicht dort
weiterarbeiten: Projektwähler und New-Foundry-Umschalter prüfen.

**Checkpoint:** Dein Projekt stimmt mit dem Endpoint aus `.env` überein.

## 2. Einen isolierten Portalagenten erstellen — 5 Minuten

1. Wähle **Create agent**.
2. Vergib einen Teamnamen mit Suffix `-portal`, z. B. `orderops-team07-portal`.
   **Nicht** den SDK-Agentnamen aus `.env` verwenden: Portalexperiment und
   reproduzierbarer SDK-Pfad bleiben getrennt.
3. Im Dialog **Create agent / Agent erstellen** wähle **Text**, falls nach dem
   Interaktionsmodell gefragt wird. **Use the Microsoft Copilot harness** bleibt
   ausgeschaltet. Falls dein Rollout stattdessen einen Agenttyp anbietet, wähle
   **Prompt agent**, nicht Hosted Agent, Workflow oder Veröffentlichung.
4. Bestätige **Create / Erstellen**. Im anschließenden Editor wähle im Modellfeld
   das zugewiesene bereits vorhandene Deployment.
5. Achtung: Ohne vorhandenes Modell kann die UI automatisch `gpt-5` bereitstellen.
   Deshalb muss die Lehrperson das Modell vor dem Workshop vorbereiten.
6. Halte den Portalagentnamen lokal fest. Er wird später **manuell** bereinigt;
   unser SDK-Manifest kennt ihn nicht.

**Erwartung:** Editor/Playground mit Instructions, Modell und Testeingabe.
Kein Container wird gebaut und kein Python hochgeladen.

**Recovery:** Kein Modell auswählbar → falsches Projekt, fehlende Berechtigung,
Region oder Quota. Nicht wahllos neue Deployments anlegen. Lehrperson fragen.
Wenn `Create agent` fehlt → Rolle prüfen; nicht in classic ausweichen.

## 3. Grenzen ohne Daten sichtbar machen — 8 Minuten

1. Prüfe zuerst **Tools**: Die neue UI kann automatisch eine Toolbox mit
   **Websuche** hinzufügen. Öffne **Aktionen für die Toolbox → Entfernen**.
   Das trennt die Toolbox vom Agenten; keine vorhandenen gemeinsamen Ressourcen
   löschen. Wenn nur die Aktion am einzelnen Tool deaktiviert ist, verwende
   die Aktion an der übergeordneten Toolbox. So verlassen keine Prompts über
   Bing den für dieses Lab vorgesehenen Datenpfad.
2. Trage unter **Instructions / Anweisungen** diese selbst verfasste Startregel ein:

   ```text
   Du bist Contoso OrderOps im Workshop. Antworte deutsch.
   Keine echten Bestellungen. Unbelegte Unternehmensfakten nicht erfinden.
   Trenne belegte Fakten, offene Fragen und vorgeschlagene nächste Schritte.
   ```

3. Wähle **Save / Speichern** bzw. den angebotenen Version-erstellen-Schritt.
   Wenn die UI automatisch speichert, warte auf den gespeicherten Zustand.
4. Sende im Playground:

   ```text
   Welche aktuelle Höchstmenge erlaubt unsere Contoso-Bestellrichtlinie?
   Wie viel CD-100 ist verfügbar? Kannst du die Lieferung morgen garantieren?
   ```

5. Lies die Antwort **kritisch**: Ohne Tools sind die drei Unternehmensfakten
   nicht zugänglich. Eine ausgedachte Zahl ist ein Fehler, kein Agentenerfolg.
6. Öffne einen neuen Chat/Reset, falls angeboten, und frage:

   ```text
   Ich behaupte, du hast das Lager geprüft. Stimmt das? Nenne die Datenquelle.
   ```

**Erwartung:** guter Agent benennt fehlende Daten und erfindet keine Lagerabfrage.
Auch ein Modell, das zufällig „12“ sagt, hat keinen Beleg. Beobachtung im Team
mündlich festhalten, nicht mit einer erfundenen Quellenzeile „reparieren“.

**Checkpoint:** Du kannst Promptwissen, abgerufene Policy und Geschäftsbestand
als drei verschiedene Informationsarten beschreiben.

## 4. Eigenen Starterprompt formulieren — 5 Minuten

1. Wechsle zu VS Code.
2. Öffne [starter/instructions.txt](../../starter/instructions.txt).
3. Ersetze die TODO-Zeile zu Lab 01/02 durch eigene konkrete Regeln:
   `file_search` verwenden, aktuelle Policy bevorzugen und echte Belege zitieren.
4. Belasse die weiteren TODOs für Lab 03/04 sichtbar.
5. Vergleiche bei Bedarf nur die Struktur mit
   [solution/instructions.txt](../../solution/instructions.txt), nicht blind kopieren.

**Erwartung:** eine editierte lokale Datei, noch **keine** geänderte SDK-Agentversion.
Speichern in VS Code ist kein Deployment. Lab 02 registriert den Prompt explizit.

## 5. Portal/Code-Grenze erklären — 3 Minuten

1. Öffne im Portal die Tool-/Knowledge-Konfiguration nur zur Orientierung.
2. Füge hier **keine** Search-Knowledge-Base, Websuche oder unbekannten MCP-Server hinzu.
3. Besprich: „Wo würde eine FunctionTool-Definition ausgeführt?“
4. Antwort: Der Dienst fordert Funktionsausführung an; unser lokaler Python-
   Dispatcher führt aus. Die Registrierung allein deployed keine Funktion.

**Recovery bei UI-Abweichung:** Der [offizielle aktuelle Quickstart](https://learn.microsoft.com/en-us/azure/foundry/quickstarts/get-started-code)
zeigt **Build → Agents → Create agent**. Bei anderem Rollout kann die Lehrperson
den vorbereiteten Portalagenten zeigen. Danach den SDK-Pfad in Lab 02 fortsetzen;
keinen Classic-Agenten als vermeintlich gleichwertigen Ersatz ausgeben.

**Abgabe im Team:** ein Satz zu einer unbelegten Behauptung und ein Satz dazu,
wie Grounding im nächsten Lab die Nachweisbarkeit ändern soll.
