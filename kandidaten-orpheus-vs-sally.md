# Kandidaten-Bewertung: ORPHEUS vs. „Sally"

*Stand: Juni 2026. Quellen 2024–2026. Legende: **[BELEGT]** = durch Quelle gedeckt · **[EINSCHÄTZUNG]** = eigene Bewertung.*

> **Kernaussage:** Die beiden sind **keine vergleichbare Kategorie**. ORPHEUS ist eine **klinische** Spracherkennung (nah an unserem OP-Use-Case). Sally.io ist ein **allgemeiner Office-Meeting-Assistent** ohne Medizin-/KIS-Bezug. Für die OP-Lösung ist nur **ORPHEUS** wirklich relevant — als Wettbewerber *und* möglicher Partner.

---

## Steckbrief ORPHEUS

- **Anbieter:** IDM gGmbH (Innovative Digitale Medizin), gemeinnützige UKE-Ausgründung (Universitätsklinikum Hamburg-Eppendorf), gegr. 2024. **[BELEGT]**
- **Was es ist:** Medizinische KI-Spracherkennung (Sprache→Text), trainiert auf Fachterminologie; für alle Berufsgruppen. **[BELEGT]**
- **Funktionsumfang:** Diktat von Konsilen, Visiten, Befunden und **OP-Berichten** per Sprachnachricht; schreibt „an jeder Cursorposition" in jedes KIS/PVS, Word, E-Mail. **[BELEGT]**
- **OP-Eignung:** **Teilweise.** OP-**Berichte** per Diktat sind explizit dabei — aber **keine belegte sterile, hands-free, intraoperative Live-Dokumentation im OP-Saal.** **[BELEGT / EINSCHÄTZUNG]**
- **KIS-Integration:** Modell „**keine Schnittstellen, keine Konnektoren**" — universelle Texteingabe an Cursorposition. Eine **echte strukturierte API (HL7/FHIR)** ist im Material **nicht belegt** → bei IDM nachfragen. **[BELEGT / offene Frage]**
- **Datenschutz / Hosting:** Betrieb **ausschließlich in Deutschland**; on-premise (eigene GPUs), STACKIT-Cloud oder GWDG; keine internationalen Clouds; DSGVO. **[BELEGT]** → starkes Souveränitätsprofil.
- **Reifegrad / Verbreitung:** Produktiv seit Anfang 2025 am UKE; an **4 Unikliniken, 30+ weiteren Kliniken, 200+ ambulanten Einrichtungen**; ~**4,5 Mio. Audiodateien** transkribiert. **[BELEGT]** → im echten Klinikbetrieb bewährt.
- **Preis:** Kommerziell verfügbar, „fairer Preis" beworben — **keine öffentlichen Preise**. **[BELEGT]**
- **Verwandtes Produkt ARGO:** Generiert automatisch **Arztbrief-/Epikrise-Entwürfe** aus der Patientenakte. Zeigt: IDM geht über reine Spracherkennung hinaus Richtung strukturierter Dokumentation. **[BELEGT]**

## Steckbrief „Sally" (= Sally.io)

- **Anbieter:** Aliru GmbH, Mannheim (seit 2015). **[BELEGT]**
- **Was es ist:** Allgemeiner **KI-Meeting-Assistent** — Transkription, Zusammenfassungen, Task-Extraktion. **[BELEGT]**
- **Technik:** 98,8 % Genauigkeit, 103 Sprachen. **[BELEGT]**
- **Zielgruppe:** Office / Sales / Wissensarbeit; >50.000 Nutzer in >1.000 Unternehmen. **Kein Medizin-/Klinik-/OP-Bezug.** **[BELEGT]**
- **Integration:** 8.000+ Tools (HubSpot, Salesforce, Slack, Asana) — Office/CRM-Ökosystem, **kein KIS / HL7 / FHIR.** **[BELEGT]**
- **Datenschutz / Hosting:** DSGVO, AVV (Art. 28), deutsche Rechenzentren (Hetzner), EU-only, Daten-Masking vor LLM, ISO 27001/9001/14001. **[BELEGT]** → solides „Made in Germany", aber **nicht medizinisch zertifiziert**.
- **OP-/klinischer Use-Case:** **Nein.** **[BELEGT / EINSCHÄTZUNG]**

> ⚠️ **Namensverwechslung möglich:** Es gibt kein eigenständiges *medizinisches* „Sally" im DACH-Markt. Verwechslungskandidat ist **Sully.ai** (US-Healthcare-Scribe, andere Schreibweise). Falls intern ein klinisches „Sally" gemeint war → Quelle nachreichen.

---

## Vergleichstabelle

| Kriterium | **ORPHEUS (IDM / UKE)** | **Sally.io (Aliru, Mannheim)** |
|---|---|---|
| Kategorie | Medizinische KI-Spracherkennung | Allgemeiner Meeting-Assistent |
| Medizin-/Klinik-Fokus | **Ja** (Kerngeschäft) | **Nein** (Office/Sales) |
| OP-/intraoperative Doku | **Teilweise** (OP-Berichte per Diktat) | **Nein** |
| KIS-Integration | „Cursor-überall"; strukturierte API unklar | Office/CRM, **kein KIS** |
| Datenschutz/Hosting | DE-only; on-prem / STACKIT / GWDG | DE/EU (Hetzner); DSGVO; AVV |
| „Made in Germany" | **Ja** | **Ja** |
| Reifegrad (Klinik) | Hoch: UKE + 30+ Kliniken, 4,5 Mio. Audios | **0 Klinikrelevanz** |
| Öffentliche Preise | Nein | Teilweise (SaaS) |
| Rolle für uns | Wettbewerber / Vorbild / mögl. Partner | Für OP-Use-Case irrelevant |

---

## Einordnung & Empfehlung

**ORPHEUS — relevant: Wettbewerber UND potenzieller Partner. [EINSCHÄTZUNG]**
- **Als Wettbewerber/Vorbild:** gleiches Segment (DACH, medizinische Sprache, KIS-Kontext, DE-Hosting), hoher Reifegrad. Wer hier antritt, misst sich an ORPHEUS.
- **Als Partner/Baustein:** IDM ist gemeinnützig und stellt Anwendungen explizit anderen Kliniken bereit → **Partnergespräch lohnt sich**, falls wir die Sprach-Engine (DE-souverän, on-prem-fähig) nicht selbst bauen wollen.
- **Unsere Lücke / Differenzierung:** ORPHEUS deckt OP-**Berichte per Diktat** ab — aber **keine belegte sterile, intraoperative Live-Doku** und **keine belegte strukturierte KIS-API.** Genau das ist unser Mehrwertfeld.

**„Sally" (Sally.io) — für den OP-Use-Case nicht relevant. [BELEGT / EINSCHÄTZUNG]**
- Kein Medizinprodukt, kein KIS, keine OP-Fähigkeit → weder Wettbewerber noch sinnvoller Baustein für die klinische Lösung. Allenfalls als generische Transkriptions-/DSGVO-Architektur-Referenz interessant.

## Drei offene Fragen an IDM (für ein Partnergespräch)
1. Gibt es eine **echte strukturierte API (HL7/FHIR)** für KIS-Datenfluss — über das „Cursor-überall"-Modell hinaus?
2. Wie verhält sich die Engine unter **realer OP-Akustik** (Lärm, Masken, mehrere Sprecher) und für **sterile, hands-free Live-Doku**?
3. **Lizenz-/Partnermodell und Preise** für eine Einbettung in unsere Software?

### Quellen (Auswahl)
IDM/ORPHEUS: idmedizin.de · medinfoweb.de · heise.de (UKE-Ausgründung) · uke.de (Digitale Helfer 2026, ARGO-PM) · gesundheitswirtschaft.at. Sally: sally.io (Start, About, GDPR). Verwechslung: sully.ai / ycombinator.com.
*Hinweis: idmedizin.de, heise.de, sally.io lieferten teils HTTP 403; Fakten aus konsistenten Suchindex-Snippets. Für die Partnerphase direkt bei IDM verifizieren.*
