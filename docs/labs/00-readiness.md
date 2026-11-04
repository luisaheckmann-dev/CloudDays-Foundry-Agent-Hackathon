# Lab 00 — Readiness und ein ehrlicher Preflight

**15 Minuten · 00:30–00:45 · Ergebnis:** lokale Umgebung bereit; Cloudzugang
nachweisbar oder ein konkret benannter Blocker. [Agenda](../AGENDA.md) · [Weiter](01-portal.md)

## Voraussetzungen vor dem Workshop

Die Lehrperson stellt ein **Foundry-(new)-Projekt**, Region, Quota und ein
geeignetes Deployment bereit. Für Responses, Function Calling und File Search
muss das gewählte Modell tatsächlich unterstützt werden. Ein verfügbares,
kostengünstiges Mini-Modell ist sinnvoll; `gpt-5.4-mini` ist ein öffentliches
Samplebeispiel, **keine Verfügbarkeitsgarantie**. Du trägst den tatsächlichen
**Deploymentnamen**, nicht blind den Modellkatalognamen ein.

Du brauchst Python 3.11+, VS Code mit Microsoft-Python-/Python-Debugger-Erweiterung,
Azure CLI und Internet zu Azure/PyPI. Kein Fabric- oder M365-Copilot-Abonnement.
Die notwendigen Rollen stehen in [Sicherheit](../SECURITY-COSTS.md); keine
Subscription-Owner-Rolle als Teilnehmerstandard verwenden.

## 1. Projektordner und Terminal öffnen — 3 Minuten

1. Starte VS Code.
2. Wähle **File → Open Folder** und den Ordner `CloudDays-Foundry-Agent-Hackathon`.
3. Wähle **Terminal → New Terminal**.
4. Wähle im Terminalprofil **PowerShell**. Alle folgenden Pfade sind relativ
   zum geöffneten Repositoryordner, nicht zum übergeordneten Scout-Ordner.
5. Prüfe:

   ```powershell
   Get-Location
   python --version
   az version
   $env:PYTHONUTF8 = "1"
   ```

**Erwartung:** Python ≥3.11 und eine Azure-CLI-Version, keine Anmeldeinformationen
im Ausgabefenster. `Get-Location` zeigt den Workshopordner.

**Recovery:** `python` öffnet den Store oder fehlt → installierte Python-Version
über `py -0p` suchen; z. B. `py -3.14 -m venv .venv` statt `python -m venv .venv`.
Fehlt `az`, Installation durch IT/Lehrperson nachholen oder vorläufig offline arbeiten.

## 2. Isoliert installieren und lokal prüfen — 7 Minuten

1. Starte:

   ```powershell
   .\scripts\bootstrap.ps1
   ```

2. Wenn PowerShell die Skriptausführung blockiert: **keine organisationsweite
   ExecutionPolicy ändern**. Führe stattdessen einzeln aus:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\python.exe -m pip --disable-pip-version-check install -r requirements.txt
   .\.venv\Scripts\python.exe -m pip check
   .\.venv\Scripts\python.exe -m orderops preflight --offline
   ```

3. Öffne über **Ctrl+Shift+P → Python: Select Interpreter → Enter interpreter path**
   den Interpreter `.venv\Scripts\python.exe`.
4. Führe die Repositorytests aus:

   ```powershell
   .\.venv\Scripts\python.exe -m unittest discover -s tests -v
   ```

**Erwartung:** gepinnte SDKs `azure-ai-projects 2.10.0`, `azure-identity 1.27.0`,
`openai 3.42.1`; `No broken requirements found`; grüne Coretests.
Offline-Preflight meldet **Config/Credential/Projekt/Modell: NOT_RUN**.
Das ist korrekt und noch kein Cloudnachweis. Einmalig installierte Pakete
bleiben ausschließlich in der lokalen `.venv`.

**Checkpoint A:** Du kannst erklären, warum ein grüner Importtest keine
Modellverfügbarkeit oder Cloudberechtigung beweist.

**Recovery:** SSL/Proxy-Fehler → genehmigten Firmenproxy/Zertifikatpfad mit IT
prüfen, TLS nicht deaktivieren. Wheel-/Pythonfehler → unterstützte Pythonversion
mit frischer `.venv` verwenden; keine SDK-Einzelversion stillschweigend austauschen.
Gemischte 1.x/2.x-Pakete → richtigen VS-Code-Interpreter wählen und Bootstrap wiederholen.

## 3. Konfiguration, Identität, Projekt und Modell prüfen — 5 Minuten

1. Öffne <https://ai.azure.com> und melde dich mit dem Workshopkonto an.
2. Prüfe, dass **New Foundry** aktiv ist, falls der Umschalter angeboten wird.
3. Wähle das von der Lehrperson zugewiesene Projekt im Projektwähler.
4. Öffne die Projektübersicht und kopiere **Project endpoint**.
   Er muss `https://…services.ai.azure.com/api/projects/…` oder die dokumentierte
   `…ai.azure.com`-Variante enthalten. Kein Hub-Connection-String, kein
   `openai.azure.com`-Ressourcenendpoint.
5. Öffne den Bereich **Models + endpoints** bzw. die Deploymentansicht unter
   **Build**. Kopiere den **Deploymentnamen** des zugewiesenen Modells.
6. Lege nur dann eine `.env` an, wenn noch keine existiert:

   ```powershell
   if (-not (Test-Path .env)) { Copy-Item .env.example .env }
   code .env
   ```

7. Ersetze in `.env` die drei `YOUR-…`-Platzhalter. Wähle einen eindeutigen
   Agentnamen wie `orderops-team07` (kein Personenname). Die Lehrperson kann
   entweder `AZURE_TENANT_ID` oder `AZURE_SUBSCRIPTION_ID` (GUID) vorgeben.
   Bei mehreren angemeldeten Konten ist die exakte Subscription besonders
   eindeutig. **Nicht beide setzen:** Azure CLI akzeptiert bei der Tokenabfrage
   nur einen dieser Selektoren. Die globale CLI-Standardsubscription bleibt unverändert.
   **Keine Keys eintragen.**
8. Melde dich bewusst per Azure CLI an; wähle das passende Workshopkonto und
   die von der Lehrperson genannte Subscription:

   ```powershell
   az login
   az account show --query "{subscription:name,tenant:tenantId}" -o table
   .\.venv\Scripts\python.exe -m orderops preflight --allow-cloud
   ```

**Erwartung:** explizite CLI-Identität, erreichbares Projekt, passendes Deployment,
erfolgreiche kleine Responses-Modellprobe. Dieser Schritt verursacht einen
kleinen echten Modellaufruf. Das Programm verwendet **AzureCliCredential**,
nicht eine unbemerkte andere Default-Credential-Kette.

**Checkpoint B:** Alle vier Cloudprüfungen erfolgreich? Dann Lab 01.
Andernfalls Fehlerstatus festhalten und [Recovery](../TROUBLESHOOTING.md) nutzen:

- **401 / CredentialUnavailable:** `az login` im richtigen Tenant; optional
  `az login --tenant "VON-DER-LEHRPERSON-GENANNTE-TENANT-ID"`.
- **403:** Lehrperson prüft die Rolle auf Projekt/Ressource und Rollenzuweisung;
  erneute Anmeldung nach Propagation, keine Owner-Eskalation auf Verdacht.
- **Deployment nicht gefunden:** Name und Projekt korrigieren, nicht auf ein
  anderes Modell automatisch ausweichen.
- **429:** keine Schleife starten; Zeit/Quota mit Lehrperson klären.
- **Keine Cloud nach 5 Minuten:** [Offline-Contingency](../INSTRUCTOR.md) verwenden
  und den fehlenden Cloudnachweis sichtbar markieren.

`.env` und `.local` sind ignoriert. Keine Kontodetails, Endpoints oder
Screenshots in öffentliche Dateien kopieren.
