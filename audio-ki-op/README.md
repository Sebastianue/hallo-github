# Audio KI im OP — Projekt

**Idee:** Eine Lösung, die das während einer Operation Gesprochene per Mikrofon aufzeichnet, automatisch in Text umwandelt und **per API direkt ins Krankenhaus-Informationssystem (KIS)** schreibt.

**Status:** 🟡 Discovery / Validierung — *vor* der Entwicklung. Ziel ist eine fundierte **Go/No-Go-Entscheidung**.

**Umsetzungs-Ansatz:** Wir bauen die Sprach-Engine **nicht selbst**, sondern integrieren einen **Partner** in unser System. Zwei Kandidaten: **ORPHEUS** (klinisch erprobt, DE-souverän) und **Sally.io** (sehr anpassbar, bisher nur Konferenzen). Unseren Mehrwert — **sterile OP-Live-Doku + strukturierte KIS-API** — ergänzen wir obendrauf.

---

## Worum geht es?

Dokumentation im OP ist zeitaufwändig und unbeliebt. Spracherkennung ist technisch gelöst — der Engpass sind **Workflow-Integration, Datenschutz/Security und der Klinik-Einkauf**. Dieses Projekt prüft methodisch, ob sich die OP-Lösung lohnt und verkaufen lässt, bevor Entwicklungsbudget fließt.

**Die zentrale These:** Alle großen Anbieter (Nuance/Microsoft, Solventum, Philips, Abridge …) zielen auf Arztbrief und Arzt-Patient-Gespräch. Den **OP-Saal** bedient niemand vollständig — selbst ORPHEUS (Universitätsklinikum Hamburg-Eppendorf) nur per Diktat von OP-Berichten. **Sterile, intraoperative Live-Doku + echte KIS-API = unser Mehrwert** auf der Partner-Engine.

---

## Inhalt des Projekts

### 📊 Präsentation (für die Geschäftsführung)
| Datei | Zweck |
|---|---|
| [`praesentation/Audio-KI-OP-Praesentation.pptx`](praesentation/Audio-KI-OP-Praesentation.pptx) | 9-Folien-Deck im Firmen-Design — der GF-Pitch |
| `praesentation/assets/diagramme/` | Quellbilder der Diagramme (Markt, Lücke, Zeitplan, Go/No-Go, Schutzziele) |

### 📄 Dokumente
| Datei | Zweck |
|---|---|
| [`dokumente/interview-leitfaden.md`](dokumente/interview-leitfaden.md) | **Interview- & Validierungs-Leitfaden** — wie vorgehen, 20 Fragen, Zahlungsbereitschaft-Fokus, Tracking-Vorlage |
| [`dokumente/onepager-gf.md`](dokumente/onepager-gf.md) | **Halbseite für die GF** — Vorlage zum Ausfüllen mit echten Zahlen |
| [`dokumente/folie-markt-luecke.md`](dokumente/folie-markt-luecke.md) | Übersichtsfolie „Markt & Lücke" (Markdown-Variante) |
| [`dokumente/fahrplan.md`](dokumente/fahrplan.md) | **Discovery-Playbook** — Annahmen, Phasen, Interview-Leitfaden, Go/No-Go |
| [`dokumente/dsgvo-datenschutzkonzept.md`](dokumente/dsgvo-datenschutzkonzept.md) | **Datenschutz-/DSGVO-Konzept** für die OP-Audioaufnahme (GF-tauglich, mit Checkliste) |
| [`dokumente/wettbewerbsanalyse-orpheus.md`](dokumente/wettbewerbsanalyse-orpheus.md) | **Wettbewerbsanalyse mit Fokus ORPHEUS** (GF-tauglich, inkl. Management Summary) |
| [`dokumente/wettbewerb.md`](dokumente/wettbewerb.md) | Breite Wettbewerbsanalyse mit Quellen (Backup) |
| [`dokumente/kandidaten-orpheus-vs-sally.md`](dokumente/kandidaten-orpheus-vs-sally.md) | Bewertung der Kandidaten ORPHEUS vs. Sally |

---

## Der 6-Wochen-Fahrplan (Kurzfassung)

| Woche | Schwerpunkt |
|---|---|
| 1 | Kontakte & Termine zu ~8–10 Kliniken/OP-Teams |
| 1–3 | OP-Interviews · DSGVO/Recht & Security prüfen · Markt/Wettbewerb vertiefen (inkl. IDM/ORPHEUS) |
| 4–5 | Mockup / Solution-Test |
| 5–6 | LOI / Pilot anbahnen · Auswertung |
| 6 | **Go/No-Go-Empfehlung an die GF** |

Details und Checklisten: [`dokumente/fahrplan.md`](dokumente/fahrplan.md).

---

## Nächster Schritt

👉 **Mit 5 Leuten aus dem OP sprechen** (Chirurg:in, OP-Pflege, OP-Manager:in) und 3 Fragen stellen:
1. Wie läuft das Dokumentieren heute ab?
2. Was nervt daran am meisten?
3. Würde automatische Sprache→Text helfen — oder gibt es Bedenken?

Danach die Zahlen/Zitate in den [Onepager](dokumente/onepager-gf.md) eintragen und der GF vorlegen.

---

## Aufgaben / Tracking

Die konkreten Arbeitsschritte sind als **GitHub Issues** angelegt (Tab „Issues" im Repository) und folgen dem 6-Wochen-Fahrplan oben.

---

## Go / No-Go — Faustregeln
| Signal | Grünes Licht |
|---|---|
| Problem | Mehrere Häuser nennen denselben quantifizierbaren Schmerz unaufgefordert |
| Recht/Security | Datenschutz/Recht sagt „machbar mit Auflagen" |
| Zahlungsbereitschaft | ≥ 2 LOIs oder bezahlte Piloten |
| Technik | Erkennungsqualität im echten OP > Akzeptanzschwelle der Ärzt:innen |
