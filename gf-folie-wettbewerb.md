# Folie: Markt & Lücke — Audio KI im OP

> Eine Übersichtsfolie für die GF. Kernbotschaft oben, Beleg in der Mitte, Schlussfolgerung unten.

---

## 🎯 Kernbotschaft

**Ein großer, wachsender Markt — aber den OP-Saal bedient niemand. Genau da wollen wir rein.**

---

## Wer macht heute was?

| Anbieter | Was sie verkaufen | OP-Saal? |
|---|---|:---:|
| **Microsoft / Nuance** (Marktführer) | Arztbrief, Arzt-Patient-Gespräch | ❌ |
| **Solventum** (ehem. 3M) | Doku in die Klinik-Akte | ❌ |
| **Philips** | Sprach-Engine, Befundung | ❌ |
| **Abridge / Nabla / Suki** (Startups) | „Ambient" Arzt-Patient-Doku | ❌ |
| **MediaInterface** (DACH-Player) | Diktat „Made in Germany" | ❌ |
| **➜ Unsere Idee** | **Intraoperative Doku, per API ins KIS** | ✅ |

*Der OP existiert bislang nur als Uni-Forschung (TUM, UKE) — als Produkt ist er frei.*

```mermaid
flowchart LR
    A[Nuance / Microsoft]:::comp --> Z[Arztbrief &<br/>Arzt-Patient-Gespräch]:::busy
    B[Solventum]:::comp --> Z
    C[Philips]:::comp --> Z
    D[Abridge / Nabla / Suki]:::comp --> Z
    E[MediaInterface]:::comp --> Z
    F[★ Unsere Idee]:::us --> G[OP-Saal<br/>intraoperativ + KIS]:::gap

    classDef comp fill:#eef1f5,stroke:#9aa5b1,color:#333
    classDef busy fill:#ffe9c7,stroke:#f0a500,color:#333
    classDef us fill:#d4f4dd,stroke:#28a745,color:#143,font-weight:bold
    classDef gap fill:#d4f4dd,stroke:#28a745,color:#143,font-weight:bold
```

*Alle drängen in denselben Topf (orange). Der OP-Saal (grün) ist frei.*

---

## Warum der Markt ernst ist

- 💰 Microsoft kaufte Marktführer **Nuance für 19,7 Mrd. $**
- 📈 Markt Spracherkennung Medizin: **~2,6 → 7,5 Mrd. $** (bis 2035)
- 📈 „Ambient"-Doku: **3,8 → 18,6 Mrd. $** (bis 2034)

```mermaid
xychart-beta
    title "Marktgröße in Mrd. USD — heute vs. Prognose"
    x-axis ["Spracherk. 2026", "Spracherk. 2035", "Ambient 2025", "Ambient 2034"]
    y-axis "Mrd. USD" 0 --> 20
    bar [2.6, 7.5, 3.8, 18.6]
```

*Beide Segmente verdrei- bis verfünffachen sich im nächsten Jahrzehnt.*

---

## Warum wir das können — ohne großes Risiko

- 🔌 **Sprach-Engine kaufen wir zu** (fertige API, EU/DSGVO-konform, ~0,0065 $/Min) — wir bauen nur den OP-/KIS-Layer
- 🇩🇪 **„Made in Germany / DSGVO"** ist im Klinikmarkt ein Verkaufsargument
- ⏱️ **Fenster ist kurz (~12–24 Monate)** — die Großen wandern langsam Richtung Chirurgie

---

## 👉 Empfehlung

**Gebt mir 6 Wochen, um mit ~8–10 Kliniken zu sprechen. Danach lege ich eine klare Go/No-Go-Empfehlung mit Zahlen vor.**

*Quellen & Details: `wettbewerb.md` · Vorgehen: `gf-onepager.md` · Fahrplan: `audio-ki.md`*
