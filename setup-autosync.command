#!/bin/zsh
# WM2026 Auto-Sync Einrichtung (macOS).
# Doppelklick im Finder ODER im Terminal:  zsh setup-autosync.command
# Richtet einen launchd-Dienst ein, der dieses Repo automatisch per "git pull"
# aktualisiert (alle 10 Minuten + bei jeder Anmeldung). iCloud verteilt die
# aktualisierten Dateien danach automatisch auf alle Geraete.
set -e

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$HOME/Library/Logs" "$HOME/Library/LaunchAgents"

# 1) Sync-Skript schreiben ($HOME bleibt fuer die Laufzeit erhalten)
cat > "$HOME/.wm2026-sync.sh" <<EOF
#!/bin/zsh
cd "$REPO_DIR" || exit 0
/usr/bin/git pull --quiet >> "\$HOME/Library/Logs/wm2026-sync.log" 2>&1
EOF
chmod +x "$HOME/.wm2026-sync.sh"

# 2) LaunchAgent schreiben
PLIST="$HOME/Library/LaunchAgents/com.wm2026.sync.plist"
cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>com.wm2026.sync</string>
  <key>ProgramArguments</key>
  <array><string>$HOME/.wm2026-sync.sh</string></array>
  <key>StartInterval</key><integer>600</integer>
  <key>RunAtLoad</key><true/>
  <key>StandardOutPath</key><string>$HOME/Library/Logs/wm2026-sync.log</string>
  <key>StandardErrorPath</key><string>$HOME/Library/Logs/wm2026-sync.log</string>
</dict>
</plist>
EOF

# 3) Dienst (neu) laden
launchctl unload "$PLIST" 2>/dev/null || true
launchctl load "$PLIST"

echo "✅ WM2026 Auto-Sync aktiv."
echo "   Repo:     $REPO_DIR"
echo "   Intervall: alle 10 Minuten + bei jeder Anmeldung"
echo "   Log:      ~/Library/Logs/wm2026-sync.log"
echo ""
echo "Zum Deaktivieren spaeter:"
echo "   launchctl unload ~/Library/LaunchAgents/com.wm2026.sync.plist"
