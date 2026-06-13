#!/bin/zsh
# WM2026 – "Jetzt synchronisieren"-Button.
# Doppelklick im Finder holt sofort die neueste Prognose (git pull).
# Tipp: einmal in den Dock ziehen, dann ist es dein Ein-Klick-Button.
cd "$(dirname "$0")" || exit 1
echo "Hole aktuelle WM-2026-Prognose ..."
if /usr/bin/git pull; then
  echo ""
  echo "✅ Fertig – Dateien sind auf dem neuesten Stand."
else
  echo ""
  echo "⚠️  Konnte nicht aktualisieren (Internet/GitHub-Login pruefen)."
fi
echo "Fenster kann geschlossen werden."
