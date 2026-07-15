#!/bin/sh

set -u

DIR="$HOME/Library/Application Support/EsoAddonsUpdater"
BIN="$DIR/app-macos"

HERE=$(dirname "$0")
HERE=$(cd "$HERE" && pwd)

if [ ! -x "$BIN" ]; then
  mkdir -p "$DIR"
  cp "$HERE/app-macos" "$BIN"
  chmod +x "$BIN"
fi

exec "$BIN"
