# Datenschutz- & DSGVO-Konzept — OP-Audio-KI

*Erstellt für die Geschäftsführung · Stand: Juni 2026 · Vertraulich*

> ⚖️ **Hinweis:** Diese Übersicht ist eine fachliche Orientierung, **keine Rechtsberatung**. Vor Umsetzung ist eine Prüfung durch Datenschutz-/Medizinrecht (Anwalt + Datenschutzbeauftragte:r) erforderlich.

---

## Management Summary

| | |
|---|---|
| **Worum es geht** | Im OP werden **Patientendaten** (Gesundheitsdaten = besondere Kategorie, Art. 9 DSGVO) *und* **Mitarbeitendenstimmen** aufgezeichnet. Beides ist hochsensibel. |
| **Befund** | Machbar — **aber nur mit „Privacy & Security by Design"**. Zwei kritische Stellschrauben: (1) Mitbestimmung des **Betriebsrats** (Mitarbeiteraufnahme), (2) Rechtsgrundlage & Einwilligung für **Patientendaten**. |
| **Chance** | DSGVO-Konformität + **EU-Hosting / „Made in Germany"** ist im DACH-Klinikmarkt ein **Verkaufsargument**, kein reiner Kostenfaktor. |
| **Empfehlung** | Datenschutz **früh** (vor Entwicklung) klären — „Shift-left" senkt Kosten und Zulassungsrisiken. Frühzeitig Anwalt + Datenschutzbeauftragte:r einbinden. |
| **Nächster Schritt** | Checkliste (unten) abarbeiten; Rechts-/Security-Einschätzung einholen (Issue #5). |

---

## 1. Warum DSGVO hier besonders kritisch ist

- **Patientendaten = besondere Kategorie** (Art. 9 DSGVO) → strengere Anforderungen, in der Regel Einwilligung oder gesetzliche/behandlungsbezogene Grundlage nötig.
- **Aufnahme von Mitarbeitenden im OP** → Beschäftigtendatenschutz (§ 26 BDSG) **und Mitbestimmung des Betriebsrats** (§ 87 BetrVG). Dauerhafte Mikrofonaufnahme ohne Betriebsrat = Show-Stopper.
- **Stresskommunikation im OP** → Aufzeichnung kann haftungs- und arbeitsrechtlich heikel sein → spricht oft für **strukturierte OP-Bericht-Erfassung** statt Total-Mitschnitt.
- **Ärztliche Schweigepflicht** (§ 203 StGB) → Weitergabe/Verarbeitung durch Dritte (z. B. Engine-Anbieter) muss sauber geregelt sein.

---

## 2. Rechtsgrundlagen (zu prüfen)

| Thema | Grundlage | Anmerkung |
|---|---|---|
| Patientendaten verarbeiten | Art. 6 + Art. 9 DSGVO | Einwilligung und/oder Behandlungskontext; mit Anwalt klären |
| Mitarbeitendenstimmen | § 26 BDSG + § 87 BetrVG | **Betriebsvereinbarung** mit Betriebsrat erforderlich |
| Auftragsverarbeitung (Engine, Cloud) | Art. 28 DSGVO (AVV) | AV-Vertrag mit jedem Verarbeiter (z. B. STT-Anbieter) |
| Schweigepflicht | § 203 StGB | Verarbeiter auf Verschwiegenheit verpflichten |

---

## 3. Maßnahmen (technisch · organisatorisch · regulatorisch)

**Technisch**
- [ ] Ende-zu-Ende-Verschlüsselung (Übertragung *und* Speicherung)
- [ ] **Pseudonymisierung / Anonymisierung**, Masking sensibler Inhalte vor LLM-Aufruf
- [ ] Rollenbasierte Zugriffe + **Zero-Trust** (jeder Zugriff geprüft)
- [ ] **Sichere, standardisierte API** mit klarer Authentifizierung/Autorisierung
- [ ] **EU-Hosting oder On-Premise**, kein Transfer außerhalb der EU

**Organisatorisch**
- [ ] Audit-Trails, Monitoring, Anomalieerkennung
- [ ] **Löschkonzept** + Datenminimierung (nur erheben, was nötig ist)
- [ ] Schulungen für Klinik-/IT-Personal
- [ ] Incident-Response-Plan (dokumentiert *und* geübt)

**Regulatorisch**
- [ ] DSGVO, BDSG · MDR · **IEC 81001-5-1** · Cyber Resilience Act (CRA) · ggf. RED
- [ ] Datenschutz-Folgenabschätzung (DSFA) prüfen — bei Art.-9-Daten meist erforderlich
- [ ] Verarbeitungsverzeichnis, AVVs, technisch-organisatorische Maßnahmen (TOMs) dokumentieren

---

## 4. Spezielle OP-Risiken & Empfehlungen

| Risiko | Empfehlung |
|---|---|
| Betriebsrat blockiert Mitarbeiteraufnahme | Früh einbinden; Betriebsvereinbarung; ggf. nur sprecherbezogene OP-Bericht-Erfassung |
| Patienten-Einwilligung im Akutfall schwierig | Rechtsgrundlage im Behandlungskontext prüfen; Aufklärungsprozess definieren |
| Engine-Anbieter verarbeitet Patientendaten | EU-Anbieter mit AVV (z. B. Corti/EU); On-Prem-Option bevorzugen |
| „Alles aufzeichnen" zu invasiv | **Scope eingrenzen** auf strukturierte OP-Berichte statt Total-Mitschnitt |

---

## 5. DSGVO als Verkaufsargument

> Erfolg von DE-Anbietern (z. B. MediaInterface, ORPHEUS) zeigt: **Datensouveränität verkauft.** EU-Hosting/On-Prem, „Made in Germany" und nachweisbare Compliance sind im DACH-Klinikmarkt ein echtes Differenzierungsmerkmal — nicht nur Pflicht.

---

## 6. Offene Fragen an Anwalt / Datenschutzbeauftragte:n
1. Welche **Rechtsgrundlage** trägt die Patientendaten-Verarbeitung (Einwilligung vs. Behandlungskontext)?
2. Ist eine **DSFA** verpflichtend, und wie sieht sie aus?
3. Wie ist die **Mitarbeiteraufnahme** sauber über eine Betriebsvereinbarung lösbar?
4. Welche Speicher-/Löschfristen gelten für Audio + Transkript?
5. Reicht **EU-Hosting** oder ist **On-Premise** beim Zielkunden Pflicht?

*Bezug: Anstoß-Fachbeitrag „Ohne Security keine KI" (TQ-Group, 17.06.2026); siehe auch Sicherheits-Folie der Präsentation und `fahrplan.md` (Phase 2).*
