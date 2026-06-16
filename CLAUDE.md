# CLAUDE.md

Leitfaden für KI-Assistenten (und Menschen), die in diesem Repository arbeiten.

## Projektüberblick

`hallo-github` ist ein persönliches Einstiegsprojekt ("Mein erstes Projekt auf
GitHub"). Zum jetzigen Zeitpunkt ist es im Wesentlichen eine leere Vorlage: Es
gibt noch keinen Anwendungscode, keine Build-Werkzeuge und keine Testsuite.

Aktuelle Inhalte:

- `README.md` — einzeilige Projektbeschreibung (auf Deutsch).
- `LICENSE` — GNU General Public License v3.0 (GPLv3).
- `CLAUDE.md` — diese Datei.

## Zustand des Repositories

Dies ist ein Repository in einem frühen Stadium mit einem einzigen Commit. Da es
noch keinen Quellcode gibt, **erfinde oder nimm nichts an** in Bezug auf
Build-System, Framework, Paketmanager oder Verzeichnisstruktur. Derzeit gibt es
keine Befehle zum Bauen, Ausführen, Linten oder Testen.

Sobald Code hinzugefügt wird, aktualisiere diese Datei und dokumentiere:

- Die gewählte(n) Sprache(n) und Laufzeitumgebung(en).
- Wie man Abhängigkeiten installiert, baut, ausführt und testet.
- Die Verzeichnisstruktur und wo die wichtigsten Module liegen.
- Projektspezifische Konventionen (Formatierung, Benennung, Commit-Stil).

## Lizenzierung

Das Projekt steht unter der **GPLv3**. Behalte dies beim Hinzufügen von Code im
Hinterkopf:

- Neue Quelldateien sollten mit der GPLv3 kompatibel sein.
- Sei vorsichtig beim Einbinden von Abhängigkeiten mit inkompatiblen Lizenzen.
- Bewahre die bestehende Datei `LICENSE`.

## Konventionen

- Die README ist auf Deutsch verfasst; behalte die bestehende Sprache beim
  Bearbeiten benutzerseitiger Dokumentation bei, sofern nicht anders gewünscht.
- Halte Änderungen klein und fokussiert, mit klaren, aussagekräftigen
  Commit-Nachrichten.

## Git-Workflow

- Standard-Branch: `master`.
- Entwickle auf einem Feature-Branch, committe mit aussagekräftigen Nachrichten
  und pushe mit `git push -u origin <branch-name>`.
- Erstelle keine Pull Requests, sofern nicht ausdrücklich darum gebeten wird.
