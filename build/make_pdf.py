#!/usr/bin/env python3
"""Render the Yuan modular-interface proposal to PDF (DE + EN) using reportlab."""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Preformatted, ListFlowable, ListItem
)

NAVY = colors.HexColor("#0b3d66")
LIGHT = colors.HexColor("#e8eef4")
BORDER = colors.HexColor("#c9d6e2")
CODEBG = colors.HexColor("#f4f6f8")

styles = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=styles["Title"], fontName="Helvetica-Bold",
                    fontSize=19, textColor=NAVY, spaceAfter=4, alignment=0, leading=22)
META = ParagraphStyle("META", parent=styles["Normal"], fontSize=8.5,
                      textColor=colors.HexColor("#555555"), spaceAfter=14)
H2 = ParagraphStyle("H2", parent=styles["Heading2"], fontName="Helvetica-Bold",
                    fontSize=13, textColor=NAVY, spaceBefore=14, spaceAfter=6, leading=16)
BODY = ParagraphStyle("BODY", parent=styles["Normal"], fontSize=10.5, leading=14.5, spaceAfter=6)
BULLET = ParagraphStyle("BULLET", parent=BODY, spaceAfter=2, leftIndent=0)
CODE = ParagraphStyle("CODE", parent=styles["Code"], fontName="Courier",
                      fontSize=7.2, leading=8.4, backColor=CODEBG,
                      borderColor=BORDER, borderWidth=0.5, borderPadding=6)


def b(t):  # bold/navy inline
    return f'<b><font color="#0b3d66">{t}</font></b>'


def bullets(items):
    return ListFlowable(
        [ListItem(Paragraph(t, BULLET), leftIndent=12, value="•") for t in items],
        bulletType="bullet", start="•", leftIndent=14, spaceAfter=6,
    )


def numbered(items):
    return ListFlowable(
        [ListItem(Paragraph(t, BULLET), leftIndent=12) for t in items],
        bulletType="1", leftIndent=16, spaceAfter=6,
    )


def make_table(header, rows):
    data = [[Paragraph(b(h), BODY) for h in header]] + \
           [[Paragraph(c, BODY) for c in r] for r in rows]
    t = Table(data, colWidths=[35*mm, 45*mm, 90*mm], hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), LIGHT),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return t


DIAGRAM_DE = """\
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

   Einbau in:  [ IOI-Box ]        und        [ Clinios u.a. ]"""

DIAGRAM_EN = """\
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

   Installed in: [ IOI box ]        and        [ Clinios etc. ]"""


def build_de():
    s = []
    s.append(Paragraph("Modulares I/O-Karten-Konzept für Yuan SDVoE-Geräte", H1))
    s.append(Paragraph("<b>Status:</b> Diskussionsvorlage für Yuan &nbsp;&nbsp;&nbsp; "
                       "<b>Datum:</b> 2026-06-16 &nbsp;&nbsp;&nbsp; "
                       "<b>Umfang:</b> SDVoE (Software Defined Video over Ethernet)", META))

    s.append(Paragraph("1. Ziel", H2))
    s.append(Paragraph(
        "Wir setzen im Bereich SDVoE (Software Defined Video over Ethernet) heute überwiegend "
        "Geräte von Yuan ein. Aktuell müssen wir je nach gewünschter Videoschnittstelle "
        "(DisplayPort, HDMI oder 12G-SDI) jeweils eine komplett eigene Karte bzw. ein eigenes "
        "Gerät beschaffen und bevorraten. Das erhöht Variantenvielfalt, Lagerhaltung, "
        "Ersatzteilaufwand und Qualifizierungsaufwand.", BODY))
    s.append(Paragraph(b("Wir möchten von Yuan eine modulare Produktarchitektur:"), BODY))
    s.append(bullets([
        f'{b("Eine einheitliche Basis-Baugruppe")} (immer identisch), die die gesamte '
        'Kernfunktion enthält (Encoding/Decoding, IP-/Netzwerkanbindung, Steuerung, Stromversorgung).',
        f'{b("Wechselbare Front-End-Module")} für die physikalische Videoschnittstelle: '
        f'{b("DP")} (DisplayPort), {b("HDMI")}, {b("SDI 12G")} (abwärtskompatibel zu 3G/6G/HD-SDI).',
        f'Die Basis-Baugruppe soll {b("sowohl in IOI-Boxen als auch in Geräten wie Clinios")} einsetzbar sein.',
    ]))
    s.append(Paragraph("Kurz gesagt: " + b("eine Basis – drei (oder mehr) steckbare Schnittstellen – "
                       "mehrere Einbau-Plattformen."), BODY))

    s.append(Paragraph("2. Konzept im Überblick", H2))
    s.append(Preformatted(DIAGRAM_DE, CODE))

    s.append(Paragraph("3. Basis-Baugruppe (gemeinsamer Kern)", H2))
    s.append(Paragraph("Die Basis-Baugruppe ist in allen Varianten " +
                       b("physisch und elektrisch identisch") + ". Sie enthält:", BODY))
    s.append(bullets([
        "Video-Encoding/-Decoding (SDVoE-Kernfunktion)",
        "IP-/Netzwerk-Anbindung (z. B. 10G, je nach Bandbreitenbedarf)",
        "Steuerung/Management (Konfiguration, Firmware-Update, Status)",
        "Stromversorgung und Takt",
        b("Einen standardisierten Modulsteckverbinder") + " zum Front-End-Modul",
    ]))
    s.append(Paragraph("Vorteil: Nur " + b("eine") + " Basis muss entwickelt, gefertigt, "
                       "qualifiziert, zertifiziert und bevorratet werden.", BODY))

    s.append(Paragraph("4. Front-End-Module (wechselbar)", H2))
    s.append(Paragraph("Jedes Modul ist eine kleine Tochterkarte, die ausschließlich das " +
                       b("signalspezifische Front-End") + " trägt:", BODY))
    s.append(make_table(
        ["Modul", "Schnittstelle", "Wesentliche Bauteile"],
        [["DP-Modul", "DisplayPort", "DP-PHY/Re-Driver, DP-Buchse"],
         ["HDMI-Modul", "HDMI", "HDMI-PHY, HDMI-Buchse, HDCP-Handling"],
         ["SDI-12G-Modul", "12G-SDI (abwärtskompatibel)", "12G-SDI-PHY, Cable Equalizer/Driver, BNC"]]))
    s.append(Spacer(1, 4))
    s.append(Paragraph("Anforderungen an die Module:", BODY))
    s.append(bullets([
        "Gleicher mechanischer und elektrischer Modulstecker bei allen Varianten",
        b("Automatische Erkennung") + " des gesteckten Modultyps durch die Basis "
        "(Modul-ID / EEPROM / Hardware-Kodierung)",
        "Möglichst " + b("werkzeugloser bzw. einfacher Tausch"),
        "Optional: Hot-Plug oder zumindest definierter Tausch im stromlosen Zustand",
    ]))

    s.append(Paragraph("5. Modul-Schnittstelle (zu definieren mit Yuan)", H2))
    s.append(Paragraph("Damit das Konzept tragfähig ist, muss Yuan eine " +
                       b("stabile, dokumentierte Schnittstelle") +
                       " zwischen Basis und Modul definieren. Aus unserer Sicht relevant:", BODY))
    s.append(bullets([
        b("Video-Datenpfad") + ": einheitlicher interner Videobus für alle Module "
        "(z. B. paralleles/serielles Videointerface), ausgelegt auf die höchste Datenrate (12G-SDI / 4K).",
        b("Steuerung") + ": I²C/SPI für Konfiguration, EDID/HDCP, Modul-Erkennung.",
        b("Versorgung") + ": definierte Spannungen und maximale Leistung pro Modul.",
        b("Mechanik") + ": definierter Steckverbinder, Bauhöhe, Befestigung, Toleranzen.",
        b("Detektion/ID") + ": eindeutige Kennung pro Modultyp + Revisionsstand.",
        b("EMV/Signalintegrität") + ": ausgelegt bis 12G-SDI bzw. 4K-Videoraten.",
    ]))

    s.append(Paragraph("6. Plattform-Kompatibilität (IOI-Box und Clinios)", H2))
    s.append(Paragraph("Die gleiche Basis-Baugruppe soll in unterschiedlichen Einbau-Plattformen laufen:", BODY))
    s.append(bullets([
        b("IOI-Box") + ": externe I/O-/Breakout-Lösung.",
        b("Clinios") + " (und vergleichbare Geräte): integrierte Plattform.",
    ]))
    s.append(Paragraph("Daraus ergibt sich der Wunsch nach einem " + b("gemeinsamen Formfaktor") +
                       " der Basis und – falls nötig – nur " +
                       b("unterschiedlichen Blenden/Halterungen (Brackets)") +
                       " je Plattform, nicht unterschiedlichen Leiterplatten. Bitte mit Yuan klären, "
                       "welcher gemeinsame Formfaktor (Maße, Steckerlage, Kühlung) beide Plattformen abdeckt.", BODY))

    s.append(Paragraph("7. Nutzen für uns", H2))
    s.append(bullets([
        b("Weniger Varianten") + ": eine Basis statt mehrerer kompletter Karten.",
        b("Geringere Lager-/Ersatzteilkosten") + " und einfachere Logistik.",
        b("Schnellere Anpassung") + " an die jeweils benötigte Schnittstelle vor Ort.",
        b("Investitionsschutz") + ": neue Schnittstellen später als zusätzliches Modul.",
        b("Einheitliche Firmware/Management") + " über alle Schnittstellen hinweg.",
        b("Vereinfachte Qualifizierung/Zulassung") + " (Kern bleibt gleich).",
    ]))

    s.append(Paragraph("8. Offene Punkte / Fragen an Yuan", H2))
    s.append(numbered([
        "Ist eine solche modulare Architektur grundsätzlich realisierbar?",
        "Welcher interne Videobus/Schnittstelle ist für DP, HDMI " + b("und") + " 12G-SDI gemeinsam machbar?",
        "Welcher gemeinsame Formfaktor passt in IOI-Box " + b("und") + " Clinios?",
        "Wie erfolgt die Modul-Erkennung und das EDID/HDCP-Handling?",
        "Hot-Plug möglich oder Tausch nur stromlos?",
        "Roadmap/Zeithorizont und Mindestabnahmemengen (MOQ)?",
        "Können bestehende Yuan-Bausteine/-Designs wiederverwendet werden?",
    ]))

    s.append(Paragraph("9. Gewünschte Rückmeldung von Yuan", H2))
    s.append(bullets([
        "Machbarkeitseinschätzung (technisch + zeitlich)",
        "Vorschlag für die Modul-Schnittstelle (Block-/Pin-Konzept)",
        "Vorschlag für den gemeinsamen Formfaktor",
        "Grobe Roadmap und kommerzielle Eckdaten",
    ]))
    return s


def build_en():
    s = []
    s.append(Paragraph("Modular I/O Card Concept for Yuan SDVoE Devices", H1))
    s.append(Paragraph("<b>Status:</b> Discussion proposal for Yuan &nbsp;&nbsp;&nbsp; "
                       "<b>Date:</b> 2026-06-16 &nbsp;&nbsp;&nbsp; "
                       "<b>Scope:</b> SDVoE (Software Defined Video over Ethernet)", META))

    s.append(Paragraph("1. Objective", H2))
    s.append(Paragraph(
        "In the SDVoE (Software Defined Video over Ethernet) area we predominantly use Yuan "
        "devices today. At present, depending on the required video interface (DisplayPort, HDMI "
        "or 12G-SDI) we have to purchase and stock a completely separate card or device for each. "
        "This increases variant count, inventory, spare-part effort and qualification effort.", BODY))
    s.append(Paragraph(b("We would like Yuan to develop a modular product architecture:"), BODY))
    s.append(bullets([
        f'{b("One common base assembly")} (always identical) that contains the entire core '
        'function (encoding/decoding, IP/network connectivity, control, power).',
        f'{b("Interchangeable front-end modules")} for the physical video interface: '
        f'{b("DP")} (DisplayPort), {b("HDMI")}, {b("SDI 12G")} (backward compatible to 3G/6G/HD-SDI).',
        f'The base assembly shall be usable {b("in IOI boxes as well as in devices such as Clinios")}.',
    ]))
    s.append(Paragraph("In short: " + b("one base – three (or more) pluggable interfaces – "
                       "multiple host platforms."), BODY))

    s.append(Paragraph("2. Concept Overview", H2))
    s.append(Preformatted(DIAGRAM_EN, CODE))

    s.append(Paragraph("3. Base Assembly (Common Core)", H2))
    s.append(Paragraph("The base assembly is " + b("physically and electrically identical") +
                       " across all variants. It contains:", BODY))
    s.append(bullets([
        "Video encoding/decoding (the SDVoE core function)",
        "IP/network connectivity (e.g. 10G, depending on bandwidth needs)",
        "Control/management (configuration, firmware update, status)",
        "Power supply and clocking",
        b("One standardized module connector") + " towards the front-end module",
    ]))
    s.append(Paragraph("Benefit: only " + b("one") + " base has to be developed, manufactured, "
                       "qualified, certified and stocked.", BODY))

    s.append(Paragraph("4. Front-End Modules (Interchangeable)", H2))
    s.append(Paragraph("Each module is a small daughter card carrying only the " +
                       b("signal-specific front-end") + ":", BODY))
    s.append(make_table(
        ["Module", "Interface", "Key components"],
        [["DP module", "DisplayPort", "DP PHY/re-driver, DP connector"],
         ["HDMI module", "HDMI", "HDMI PHY, HDMI connector, HDCP handling"],
         ["SDI-12G module", "12G-SDI (backward compatible)", "12G-SDI PHY, cable equalizer/driver, BNC"]]))
    s.append(Spacer(1, 4))
    s.append(Paragraph("Requirements for the modules:", BODY))
    s.append(bullets([
        "Identical mechanical and electrical module connector on all variants",
        b("Automatic detection") + " of the inserted module type by the base "
        "(module ID / EEPROM / hardware coding)",
        "Easy, ideally " + b("tool-free, replacement"),
        "Optional: hot-plug, or at least a defined swap in the powered-off state",
    ]))

    s.append(Paragraph("5. Module Interface (to be defined with Yuan)", H2))
    s.append(Paragraph("For the concept to be viable, Yuan must define a " +
                       b("stable, documented interface") +
                       " between base and module. From our point of view the relevant items:", BODY))
    s.append(bullets([
        b("Video data path") + ": a common internal video bus for all modules "
        "(e.g. parallel/serial video interface), dimensioned for the highest data rate (12G-SDI / 4K).",
        b("Control") + ": I²C/SPI for configuration, EDID/HDCP, module detection.",
        b("Power") + ": defined voltages and maximum power per module.",
        b("Mechanics") + ": defined connector, height, mounting, tolerances.",
        b("Detection/ID") + ": unique identifier per module type + revision level.",
        b("EMC/signal integrity") + ": rated up to 12G-SDI / 4K video rates.",
    ]))

    s.append(Paragraph("6. Platform Compatibility (IOI Box and Clinios)", H2))
    s.append(Paragraph("The same base assembly shall run in different host platforms:", BODY))
    s.append(bullets([
        b("IOI box") + ": external I/O / breakout solution.",
        b("Clinios") + " (and comparable devices): integrated platform.",
    ]))
    s.append(Paragraph("This leads to the wish for a " + b("common form factor") +
                       " of the base and – if necessary – only " +
                       b("different brackets/faceplates") +
                       " per platform, not different PCBs. Please clarify with Yuan which common "
                       "form factor (dimensions, connector position, cooling) covers both platforms.", BODY))

    s.append(Paragraph("7. Benefits for Us", H2))
    s.append(bullets([
        b("Fewer variants") + ": one base instead of several complete cards.",
        b("Lower inventory/spare-part cost") + " and simpler logistics.",
        b("Faster on-site adaptation") + " to the required interface.",
        b("Investment protection") + ": new interfaces later as an additional module.",
        b("Unified firmware/management") + " across all interfaces.",
        b("Simplified qualification/approval") + " (the core stays the same).",
    ]))

    s.append(Paragraph("8. Open Items / Questions for Yuan", H2))
    s.append(numbered([
        "Is such a modular architecture feasible in principle?",
        "Which internal video bus/interface is jointly feasible for DP, HDMI " + b("and") + " 12G-SDI?",
        "Which common form factor fits into the IOI box " + b("and") + " Clinios?",
        "How is module detection and EDID/HDCP handling implemented?",
        "Hot-plug possible, or swap only when powered off?",
        "Roadmap/time horizon and minimum order quantities (MOQ)?",
        "Can existing Yuan building blocks/designs be reused?",
    ]))

    s.append(Paragraph("9. Requested Feedback from Yuan", H2))
    s.append(bullets([
        "Feasibility assessment (technical + schedule)",
        "Proposal for the module interface (block/pin concept)",
        "Proposal for the common form factor",
        "Rough roadmap and commercial key data",
    ]))
    return s


def render(path, story):
    doc = SimpleDocTemplate(path, pagesize=A4,
                            leftMargin=20*mm, rightMargin=20*mm,
                            topMargin=18*mm, bottomMargin=18*mm,
                            title=os.path.basename(path))
    doc.build(story)
    print("wrote", path)


if __name__ == "__main__":
    out = os.path.expanduser("~/Downloads")
    os.makedirs(out, exist_ok=True)
    render(os.path.join(out, "Yuan-Modular-IO-Konzept-DE.pdf"), build_de())
    render(os.path.join(out, "Yuan-Modular-IO-Concept-EN.pdf"), build_en())
