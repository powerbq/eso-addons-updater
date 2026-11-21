#!/bin/bash

set -euo pipefail

cd "$(dirname "$0")"

source=""
if [ -f assets/eso-addons-updater.svg ]; then
    source=assets/eso-addons-updater.svg
else
    for candidate in assets/eso-addons-updater.*; do
        case "${candidate##*.}" in
            png | jpg | jpeg | webp | gif | bmp | tif | tiff | avif)
                source="$candidate"
                break
                ;;
        esac
    done
fi

if [ -z "$source" ]; then
    echo "no source icon: expected assets/eso-addons-updater.<svg|png|jpg|webp|...>" >&2
    exit 1
fi

if command -v magick >/dev/null 2>&1; then
    im=(magick)
elif command -v convert >/dev/null 2>&1; then
    im=(convert)
else
    echo "ImageMagick is required (install 'magick' or 'convert')" >&2
    exit 1
fi

render() {
    "${im[@]}" -background none "$source" -resize "${1}x${1}" -strip "$2"
}

mkdir -p icons

# Windows: multi-size .ico embedded into the exe by build.rs.
"${im[@]}" -background none "$source" \
    -define icon:auto-resize=16,32,48,64,128,256 \
    -strip \
    icons/eso-addons-updater.ico

# macOS: assemble a PNG-based .icns ourselves (the modern types iconutil emits), so it renders on
# current macOS and is identical on every host. libicns/png2icns is not used (it writes classic
# ARGB / JPEG-2000 entries that recent macOS does not reliably display).
work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT
for size in 16 32 64 128 256 512 1024; do
    render "$size" "$work/$size.png"
done

icns=icons/eso-addons-updater.icns
python3 - "$icns" "$work" <<'PY'
import struct, sys

out, work = sys.argv[1], sys.argv[2]
entries = [
    (b"icp4", 16),
    (b"icp5", 32),
    (b"ic07", 128),
    (b"ic08", 256),
    (b"ic09", 512),
    (b"ic10", 1024),
    (b"ic11", 32),
    (b"ic12", 64),
    (b"ic13", 256),
    (b"ic14", 512),
]
chunks = []
for kind, size in entries:
    with open(f"{work}/{size}.png", "rb") as png:
        payload = png.read()
    chunks.append(kind + struct.pack(">I", len(payload) + 8) + payload)
body = b"".join(chunks)
with open(out, "wb") as icns:
    icns.write(b"icns" + struct.pack(">I", len(body) + 8) + body)
PY

echo "regenerated from $source:"
echo "  icons/eso-addons-updater.ico"
echo "  $icns"
