#!/bin/sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
ARTIFACTS="$ROOT/artifacts"
mkdir -p "$ARTIFACTS"
[ "$(id -u)" -eq 0 ] || { echo 'Run with sudo: sudo ./scripts/build-iso.sh' >&2; exit 1; }
command -v lb >/dev/null 2>&1 || { echo 'live-build is required.' >&2; exit 1; }
command -v xorriso >/dev/null 2>&1 || { echo 'xorriso is required.' >&2; exit 1; }
command -v rsvg-convert >/dev/null 2>&1 || { echo 'librsvg2-bin is required (rsvg-convert).' >&2; exit 1; }
cd "$ROOT"
./scripts/check-project.sh
rm -rf config/binary config/bootstrap config/chroot config/common config/source .build cache chroot binary
rm -f "$ROOT"/*.iso "$ROOT"/*.hybrid.iso
chmod +x config/auto/config hooks/normal/*.chroot includes.chroot/usr/local/bin/mll-help includes.chroot/usr/local/bin/mll-install-profile includes.chroot/usr/local/bin/mll-network-isolation
config/auto/config
RSVG_LINK_CREATED=false
if ! command -v rsvg >/dev/null 2>&1; then
  ln -s "$(command -v rsvg-convert)" /usr/local/bin/rsvg
  RSVG_LINK_CREATED=true
fi
cleanup_rsvg() { if [ "$RSVG_LINK_CREATED" = true ]; then rm -f /usr/local/bin/rsvg; fi; }
trap cleanup_rsvg EXIT INT TERM
lb build 2>&1 | tee "$ARTIFACTS/build.log"
ISO=$(find "$ROOT" -maxdepth 1 -type f \( -name '*.hybrid.iso' -o -name '*.iso' \) -print -quit)
[ -n "$ISO" ] || { echo 'ISO was not produced.' >&2; exit 1; }
cp "$ISO" "$ARTIFACTS/mobile-linux-lab-amd64.iso"
sha256sum "$ARTIFACTS/mobile-linux-lab-amd64.iso" > "$ARTIFACTS/mobile-linux-lab-amd64.iso.sha256"
echo "Created $ARTIFACTS/mobile-linux-lab-amd64.iso"
