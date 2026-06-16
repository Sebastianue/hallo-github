# Modular I/O Card Concept for Yuan SDVoE Devices
# Modulares I/O-Karten-Konzept für Yuan SDVoE-Geräte

> Status: Discussion proposal for Yuan / Diskussionsvorlage für Yuan
> Date / Datum: 2026-06-16
> Scope / Umfang: SDVoE (Software Defined Video over Ethernet) video transmission

---

# 🇩🇪 Deutsch

## 1. Ziel

Wir setzen im Bereich SDVoE (Software Defined Video over Ethernet) heute überwiegend
Geräte von Yuan ein. Aktuell müssen wir je nach gewünschter Videoschnittstelle
(DisplayPort, HDMI oder 12G-SDI) jeweils eine komplett eigene Karte bzw. ein
eigenes Gerät beschaffen und bevorraten. Das erhöht Varianten­vielfalt,
Lagerhaltung, Ersatzteil­aufwand und Qualifizierungs­aufwand.

**Wir möchten von Yuan eine modulare Produktarchitektur:**

- **Eine einheitliche Basis-Baugruppe** (immer identisch), die die gesamte
  Kernfunktion enthält (Encoding/Decoding, IP-/Netzwerk­anbindung, Steuerung,
  Stromversorgung).
- **Wechselbare Front-End-Module** für die physikalische Videoschnittstelle:
  - **DP** (DisplayPort)
  - **HDMI**
  - **SDI 12G** (abwärtskompatibel zu 3G/6G/HD-SDI)
- Die Basis-Baugruppe soll **sowohl in IOI-Boxen als auch in Geräten wie
  Clinios** einsetzbar sein.

Kurz gesagt: **eine Basis – drei (oder mehr) steckbare Schnittstellen – mehrere
Einbau-Plattformen.**

## 2. Konzept im Überblick

```
        +-------------------------------------------------+
        |              BASIS-BAUGRUPPE (immer gleich)     |
        |                                                 |
        |   [Video-Codec / FPGA-SoC]   [Netzwerk/IP-PHY]  |
        |   [Steuerung / CPU/MCU]      [Stromversorgung]  |
        |                                                 |
        |        +-----------------------------+          |
        |        |   STANDARD-MODULSTECKER     |          |
        |        |  (definierte Schnittstelle) |          |
        +--------+--------------+--------------+----------+
                                |
              +-----------------+-----------------+
              |                 |                 |
        +-----------+     +-----------+     +-------------+
        | DP-Modul  |     | HDMI-Modul|     | SDI-12G-Mod.|
        | DP-PHY    |     | HDMI-PHY  |     | 12G-SDI-PHY |
        | DP-Buchse |     | HDMI-Buc. |     | BNC + EQ/DRV|
        +-----------+     +-----------+     +-------------+

   Einbau in:  [ IOI-Box ]        und        [ Clinios u.a. ]
```

## 3. Basis-Baugruppe (gemeinsamer Kern)

Die Basis-Baugruppe ist in allen Varianten **physisch und elektrisch
identisch**. Sie enthält:

- Video-Encoding/-Decoding (SDVoE-Kernfunktion)
- IP-/Netzwerk-Anbindung (z. B. 1G/10G, je nach Bandbreitenbedarf)
- Steuerung/Management (Konfiguration, Firmware-Update, Status)
- Stromversorgung und Takt
- **Einen standardisierten Modulsteckverbinder** zum Front-End-Modul

Vorteil: Nur **eine** Basis muss entwickelt, gefertigt, qualifiziert,
zertifiziert und bevorratet werden.

## 4. Front-End-Module (wechselbar)

Jedes Modul ist eine kleine Tochterkarte, die ausschließlich das
**signal­spezifische Front-End** trägt:

| Modul       | Schnittstelle        | Wesentliche Bauteile                       |
|-------------|----------------------|--------------------------------------------|
| DP-Modul    | DisplayPort          | DP-PHY/Re-Driver, DP-Buchse                |
| HDMI-Modul  | HDMI                 | HDMI-PHY, HDMI-Buchse, HDCP-Handling       |
| SDI-12G-Mod.| 12G-SDI (abwärtskomp.)| 12G-SDI-PHY, Cable Equalizer/Driver, BNC  |

Anforderungen an die Module:

- Gleicher mechanischer und elektrischer Modulstecker bei allen Varianten
- **Automatische Erkennung** des gesteckten Modultyps durch die Basis
  (Modul-ID / EEPROM / Hardware-Kodierung)
- Möglichst **werkzeugloser bzw. einfacher Tausch**
- Optional: Hot-Plug oder zumindest definierter Tausch im stromlosen Zustand

## 5. Modul-Schnittstelle (zu definieren mit Yuan)

Damit das Konzept tragfähig ist, muss Yuan eine **stabile, dokumentierte
Schnittstelle** zwischen Basis und Modul definieren. Aus unserer Sicht relevant:

- **Video-Datenpfad**: einheitlicher interner Videobus für alle Module
  (z. B. paralleles/serielles Videointerface), ausgelegt auf die höchste
  Datenrate (12G-SDI / 4K).
- **Steuerung**: I²C/SPI für Konfiguration, EDID/HDCP, Modul-Erkennung.
- **Versorgung**: definierte Spannungen und maximale Leistung pro Modul.
- **Mechanik**: definierter Steckverbinder, Bauhöhe, Befestigung,
  Toleranzen.
- **Detektion/ID**: eindeutige Kennung pro Modultyp + Revisionsstand.
- **EMV/Signalintegrität**: ausgelegt bis 12G-SDI bzw. 4K-Videoraten.

## 6. Plattform-Kompatibilität (IOI-Box und Clinios)

Die gleiche Basis-Baugruppe soll in unterschiedlichen Einbau-Plattformen laufen:

- **IOI-Box**: externe I/O-/Breakout-Lösung.
- **Clinios** (und vergleichbare Geräte): integrierte Plattform.

Daraus ergibt sich der Wunsch nach einem **gemeinsamen Formfaktor** der Basis
und – falls nötig – nur **unterschiedlichen Blenden/Halterungen (Brackets)** je
Plattform, nicht unterschiedlichen Leiterplatten. Bitte mit Yuan klären, welcher
gemeinsame Formfaktor (Maße, Steckerlage, Kühlung) beide Plattformen abdeckt.

## 7. Nutzen für uns

- **Weniger Varianten**: eine Basis statt mehrerer kompletter Karten.
- **Geringere Lager-/Ersatzteilkosten** und einfachere Logistik.
- **Schnellere Anpassung** an die jeweils benötigte Schnittstelle vor Ort.
- **Investitionsschutz**: neue Schnittstellen später als zusätzliches Modul.
- **Einheitliche Firmware/Management** über alle Schnittstellen hinweg.
- **Vereinfachte Qualifizierung/Zulassung** (Kern bleibt gleich).

## 8. Offene Punkte / Fragen an Yuan

1. Ist eine solche modulare Architektur grundsätzlich realisierbar?
2. Welcher interne Videobus/Schnittstelle ist für DP, HDMI **und** 12G-SDI
   gemeinsam machbar?
3. Welcher gemeinsame Formfaktor passt in IOI-Box **und** Clinios?
4. Wie erfolgt die Modul-Erkennung und das EDID/HDCP-Handling?
5. Hot-Plug möglich oder Tausch nur stromlos?
6. Roadmap/Zeithorizont und Mindestabnahmemengen (MOQ)?
7. Können bestehende Yuan-Bausteine/-Designs wiederverwendet werden?

## 9. Gewünschte Rückmeldung von Yuan

- Machbarkeits­einschätzung (technisch + zeitlich)
- Vorschlag für die Modul-Schnittstelle (Block-/Pin-Konzept)
- Vorschlag für den gemeinsamen Formfaktor
- Grobe Roadmap und kommerzielle Eckdaten

---

# 🇬🇧 English

## 1. Objective

In the SDVoE (Software Defined Video over Ethernet) area we predominantly use Yuan
devices today. At present, depending on the required video interface
(DisplayPort, HDMI or 12G-SDI) we have to purchase and stock a completely
separate card or device for each. This increases variant count, inventory,
spare-part effort and qualification effort.

**We would like Yuan to develop a modular product architecture:**

- **One common base assembly** (always identical) that contains the entire core
  function (encoding/decoding, IP/network connectivity, control, power).
- **Interchangeable front-end modules** for the physical video interface:
  - **DP** (DisplayPort)
  - **HDMI**
  - **SDI 12G** (backward compatible to 3G/6G/HD-SDI)
- The base assembly shall be usable **in IOI boxes as well as in devices such as
  Clinios**.

In short: **one base – three (or more) pluggable interfaces – multiple host
platforms.**

## 2. Concept Overview

```
        +-------------------------------------------------+
        |            BASE ASSEMBLY (always identical)     |
        |                                                 |
        |   [Video codec / FPGA-SoC]   [Network/IP PHY]   |
        |   [Control / CPU/MCU]        [Power supply]     |
        |                                                 |
        |        +-----------------------------+          |
        |        |   STANDARD MODULE CONNECTOR |          |
        |        |     (defined interface)     |          |
        +--------+--------------+--------------+----------+
                                |
              +-----------------+-----------------+
              |                 |                 |
        +-----------+     +-----------+     +-------------+
        | DP module |     |HDMI module|     |SDI-12G mod. |
        | DP PHY    |     | HDMI PHY  |     | 12G-SDI PHY |
        | DP jack   |     | HDMI jack |     | BNC + EQ/DRV|
        +-----------+     +-----------+     +-------------+

   Installed in: [ IOI box ]        and        [ Clinios etc. ]
```

## 3. Base Assembly (Common Core)

The base assembly is **physically and electrically identical** across all
variants. It contains:

- Video encoding/decoding (the SDVoE core function)
- IP/network connectivity (e.g. 1G/10G, depending on bandwidth needs)
- Control/management (configuration, firmware update, status)
- Power supply and clocking
- **One standardized module connector** towards the front-end module

Benefit: only **one** base has to be developed, manufactured, qualified,
certified and stocked.

## 4. Front-End Modules (Interchangeable)

Each module is a small daughter card carrying only the **signal-specific
front-end**:

| Module       | Interface              | Key components                          |
|--------------|------------------------|-----------------------------------------|
| DP module    | DisplayPort            | DP PHY/re-driver, DP connector          |
| HDMI module  | HDMI                   | HDMI PHY, HDMI connector, HDCP handling  |
| SDI-12G mod. | 12G-SDI (backw. comp.) | 12G-SDI PHY, cable equalizer/driver, BNC |

Requirements for the modules:

- Identical mechanical and electrical module connector on all variants
- **Automatic detection** of the inserted module type by the base
  (module ID / EEPROM / hardware coding)
- Easy, ideally **tool-free, replacement**
- Optional: hot-plug, or at least a defined swap in the powered-off state

## 5. Module Interface (to be defined with Yuan)

For the concept to be viable, Yuan must define a **stable, documented
interface** between base and module. From our point of view the relevant items:

- **Video data path**: a common internal video bus for all modules
  (e.g. parallel/serial video interface), dimensioned for the highest data rate
  (12G-SDI / 4K).
- **Control**: I²C/SPI for configuration, EDID/HDCP, module detection.
- **Power**: defined voltages and maximum power per module.
- **Mechanics**: defined connector, height, mounting, tolerances.
- **Detection/ID**: unique identifier per module type + revision level.
- **EMC/signal integrity**: rated up to 12G-SDI / 4K video rates.

## 6. Platform Compatibility (IOI Box and Clinios)

The same base assembly shall run in different host platforms:

- **IOI box**: external I/O / breakout solution.
- **Clinios** (and comparable devices): integrated platform.

This leads to the wish for a **common form factor** of the base and – if
necessary – only **different brackets/faceplates** per platform, not different
PCBs. Please clarify with Yuan which common form factor (dimensions, connector
position, cooling) covers both platforms.

## 7. Benefits for Us

- **Fewer variants**: one base instead of several complete cards.
- **Lower inventory/spare-part cost** and simpler logistics.
- **Faster on-site adaptation** to the required interface.
- **Investment protection**: new interfaces later as an additional module.
- **Unified firmware/management** across all interfaces.
- **Simplified qualification/approval** (the core stays the same).

## 8. Open Items / Questions for Yuan

1. Is such a modular architecture feasible in principle?
2. Which internal video bus/interface is jointly feasible for DP, HDMI **and**
   12G-SDI?
3. Which common form factor fits into the IOI box **and** Clinios?
4. How is module detection and EDID/HDCP handling implemented?
5. Hot-plug possible, or swap only when powered off?
6. Roadmap/time horizon and minimum order quantities (MOQ)?
7. Can existing Yuan building blocks/designs be reused?

## 9. Requested Feedback from Yuan

- Feasibility assessment (technical + schedule)
- Proposal for the module interface (block/pin concept)
- Proposal for the common form factor
- Rough roadmap and commercial key data
