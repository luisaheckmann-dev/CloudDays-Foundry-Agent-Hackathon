# 210 Minuten: Ablauf und Zielbild

[Start](../README.md) · [Lehrenden-Runbook](INSTRUCTOR.md)

**Zielgruppe:** Intermediate; Azure-Grundkenntnisse, grundlegendes Python/JSON,
Terminal und RBAC-Begriffe. Kein Machine-Learning-Training vorausgesetzt.
In Zweier-/Dreierteams arbeiten; Azure-Ressourcen und Quota sind **vor** der
Veranstaltung vorzubereiten. Die 15 Minuten Readiness reichen nicht für
Subscription-Freigaben, Netzwerkausnahmen oder Quota-Erhöhungen.

| Zeit ab Start | Minuten | Format / Ergebnis |
|---|---:|---|
| 00:00–00:30 | 30 | Instructor-Demo: Beleg → Inventar → Empfehlung → abgelehnter/freigegebener lokaler Entwurf |
| 00:30–00:45 | 15 | [00 Readiness](labs/00-readiness.md): Python, Rollen, Endpoint, Modell, Identität |
| 00:45–01:10 | 25 | [01 Portal](labs/01-portal.md): Prompt Agent im neuen Foundry, Grenzen ohne Wissen |
| 01:10–01:40 | 30 | [02 Grounding](labs/02-grounding.md): File Search, Indexstatus, Version, Quellen |
| 01:40–01:50 | 10 | **Pause**; keine Polling-/Chatprozesse laufen lassen |
| 01:50–02:25 | 35 | [03 Code & Tools](labs/03-tools.md): Python in VS Code, Toolloop, menschliches Gate |
| 02:25–02:45 | 20 | [04 Evaluation](labs/04-evaluation.md): Gegenbeispiele, Belege, Diagnose, Rubrik |
| 02:45–03:20 | 35 | [05 Hackathon](labs/05-hackathon.md): messbare Verbesserung und Angriffstest |
| 03:20–03:30 | 10 | [06 Pitch & Cleanup](labs/06-cleanup.md): Kurzbeweis und gezieltes Aufräumen |
| **Summe** | **210** | **3,5 Stunden einschließlich Pause** |

## Am Ende kannst du …

1. Einen **serverseitig registrierten, versionierten Prompt Agent** vom lokalen
   ausführenden Python-Prozess unterscheiden.
2. Echte File-Search-Zitatannotationen prüfen, statt einer hübschen Quellenbehauptung zu glauben.
3. Toolparameter serverunabhängig validieren und einen Schreibpfad technisch vom Modell trennen.
4. Grenzen von Offline-Tests, strukturellen Checks und semantischer Evaluation erklären.
5. Den Zusatznutzen von Foundry IQ, Fabric IQ und Work IQ korrekt einordnen, ohne
   weitere Lizenzen für den Pflichtpfad zu benötigen.

## Definition of Done des Pflichtpfads

- Eine eigene Starter-Funktion arbeitet read-only; Lernchecks sind grün.
- Mindestens eine reale Agentantwort mit prüfbarer aktueller Policy-Zitatannotation
  und getrennter Inventarquelle; fehlende Cloudrechte werden als Blocker notiert.
- Abgelehnte Freigabe erzeugt keine DB; exakte menschliche Freigabe höchstens eine
  Zeile pro Vorschlag; Bestand bleibt unverändert.
- Drei Gegenbeispiele und eine manuelle Bewertung, nicht nur Antwortlänge.
- Nur eigene Ressourcen entfernt oder eindeutig zum späteren Cleanup dokumentiert.

**Bei Cloudausfall:** [ehrlicher Offline-Modus](INSTRUCTOR.md) erlaubt Tools,
Validierung und Freigabe zu lernen. Er erfüllt ausdrücklich **nicht** den
Cloud-Agent-/Zitat-Nachweis. Niemand soll einen simulierten Cloud-Erfolg präsentieren.
