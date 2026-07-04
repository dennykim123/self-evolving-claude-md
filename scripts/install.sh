#!/bin/zsh
# Installs the harness: templates (with backup), Codex block append, weekly launchd job (macOS).
set -eu
HERE="$(cd "$(dirname "$0")/.." && pwd)"
OFFICE="$HOME/.claude/office"
STAMP=$(date +%Y%m%d-%H%M%S)
mkdir -p "$OFFICE" "$HOME/.claude/office/evolve-logs"

backup() { [ -f "$1" ] && cp "$1" "$1.bak-$STAMP" && echo "backup: $1.bak-$STAMP" || true; }

# 1) SSOT
backup "$OFFICE/HARNESS.md"
cp "$HERE/templates/HARNESS.md" "$OFFICE/HARNESS.md"

# 2) CLAUDE.md — never overwrite: append or create
if [ -f "$HOME/.claude/CLAUDE.md" ]; then
  if ! grep -q "HARNESS loader" "$HOME/.claude/CLAUDE.md"; then
    backup "$HOME/.claude/CLAUDE.md"
    { echo; echo "---"; echo; cat "$HERE/templates/CLAUDE.md"; } >> "$HOME/.claude/CLAUDE.md"
    echo "appended harness loader to existing ~/.claude/CLAUDE.md"
  else
    echo "~/.claude/CLAUDE.md already contains the loader — skipped"
  fi
else
  cp "$HERE/templates/CLAUDE.md" "$HOME/.claude/CLAUDE.md"
fi

# 3) Codex block — marker-bounded append
if [ -d "$HOME/.codex" ]; then
  if ! grep -q "HARNESS:START" "$HOME/.codex/AGENTS.md" 2>/dev/null; then
    backup "$HOME/.codex/AGENTS.md"
    { echo; cat "$HERE/templates/AGENTS-block.md"; } >> "$HOME/.codex/AGENTS.md"
    echo "appended harness block to ~/.codex/AGENTS.md"
  else
    echo "~/.codex/AGENTS.md already has the block — skipped"
  fi
fi

# 4) scripts
cp "$HERE/scripts/mine.py" "$HERE/scripts/evolve.sh" "$HERE/scripts/probes.sh" "$OFFICE/"
chmod +x "$OFFICE/evolve.sh" "$OFFICE/probes.sh"

# 5) weekly launchd job (macOS only)
if [ "$(uname)" = "Darwin" ]; then
  PLIST="$HOME/Library/LaunchAgents/com.harness.evolve.plist"
  CLAUDE_BIN_DIR="$(dirname "$(command -v claude || echo /usr/local/bin/claude)")"
  cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>com.harness.evolve</string>
  <key>ProgramArguments</key>
  <array><string>/bin/zsh</string><string>$OFFICE/evolve.sh</string><string>7</string></array>
  <key>StartCalendarInterval</key>
  <dict><key>Weekday</key><integer>1</integer><key>Hour</key><integer>9</integer><key>Minute</key><integer>23</integer></dict>
  <key>EnvironmentVariables</key>
  <dict><key>PATH</key><string>$CLAUDE_BIN_DIR:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin</string></dict>
  <key>StandardOutPath</key><string>$OFFICE/evolve-logs/evolve.out.log</string>
  <key>StandardErrorPath</key><string>$OFFICE/evolve-logs/evolve.err.log</string>
</dict>
</plist>
EOF
  launchctl unload "$PLIST" 2>/dev/null || true
  launchctl load "$PLIST"
  echo "weekly evolution job registered (Mon 09:23 local): com.harness.evolve"
else
  echo "non-macOS: register scripts/evolve.sh yourself via cron/systemd (weekly)"
fi

echo ""
echo "Installed. Next steps:"
echo "  1. Edit $OFFICE/HARNESS.md — make the rules yours (replace {PRINCIPAL})"
echo "  2. python3 $OFFICE/mine.py --days 30   # mine your own history, set your baseline"
echo "  3. $OFFICE/evolve.sh 7                 # or wait for Monday"
