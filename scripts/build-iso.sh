#!/bin/sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
ARTIFACTS="$ROOT/artifacts"
mkdir -p "$ARTIFACTS"
[ "$(id -u)" -eq 0 ] || { echo 'Run with sudo: sudo ./scripts/build-iso.sh' >&2; exit 1; }
command -v lb >/dev/null 2>&1 || { echo 'live-build is required.' >&2; exit 1; }
command -v xorriso >/dev/null 2>&1 || { echo 'xorriso is required.' >&2; exit 1; }
command -v rsvg-convert >/dev/null 2>&1 || { echo 'librsvg2-bin is required (rsvg-convert).' >&2; exit 1; }
command -v grub-mkstandalone >/dev/null 2>&1 || { echo 'grub-efi-amd64-bin is required.' >&2; exit 1; }
command -v mkfs.vfat >/dev/null 2>&1 || { echo 'dosfstools is required.' >&2; exit 1; }
command -v mcopy >/dev/null 2>&1 || { echo 'mtools is required.' >&2; exit 1; }
[ -f /usr/lib/ISOLINUX/isohdpfx.bin ] || { echo 'isolinux isohdpfx.bin is required.' >&2; exit 1; }
cd "$ROOT"
./scripts/check-project.sh
if [ -d "$ROOT/chroot" ]; then
  umount -R "$ROOT/chroot" 2>/dev/null || true
  umount -R "$ROOT/chroot/sys" 2>/dev/null || true
  umount -R "$ROOT/chroot/proc" 2>/dev/null || true
  umount -R "$ROOT/chroot/dev" 2>/dev/null || true
  umount -l "$ROOT/chroot/dev/pts" 2>/dev/null || true
  umount -l "$ROOT/chroot/dev" 2>/dev/null || true
fi
rm -rf config/binary config/bootstrap config/chroot config/common config/source .build .lock binary
rm -rf chroot || {
  # A previous interrupted live-build may leave root-owned apt directories.
  # Retry after a depth-first removal rather than masking the real build step.
  find chroot -depth -mindepth 1 -delete 2>/dev/null || true
  rm -rf chroot
}
rm -f "$ROOT"/*.iso "$ROOT"/*.hybrid.iso
chmod +x config/auto/config hooks/normal/*.chroot scripts/add-uefi-boot.sh includes.chroot/usr/local/bin/mll-help includes.chroot/usr/local/bin/mll-release includes.chroot/usr/local/bin/mll-install-profile includes.chroot/usr/local/bin/mll-network-isolation includes.chroot/usr/local/bin/drakonis-install-profile includes.chroot/usr/local/bin/drakonis-security-center includes.chroot/usr/local/bin/drakonis-network-tools includes.chroot/usr/local/bin/drakonis-help-center includes.chroot/usr/local/bin/drakonis-themes-manager includes.chroot/usr/local/bin/drakonis-first-run includes.chroot/usr/local/bin/drakonis-power-session includes.chroot/usr/local/bin/drakonis-control-center includes.chroot/usr/local/bin/drakonis-vault includes.chroot/usr/local/bin/drakonis-vault-ui includes.chroot/usr/local/bin/drakonis-software-center includes.chroot/usr/local/sbin/drakonis-initial-password includes.chroot/usr/local/libexec/drakonis-center.py includes.chroot/usr/local/libexec/drakonis-vault.py includes.chroot/usr/local/libexec/drakonis-vault-ui.py
config/auto/config
LOCAL_LIVE_BUILD="$ROOT/.live-build"
mkdir -p "$LOCAL_LIVE_BUILD/scripts/build"
# Ubuntu's live-build 3.0~a57 hard-codes xz for Debian rootfs images.
# Keep the override local and derive the compressor from LB_COMPRESSION.
sed 's/ -comp xz/ -comp ${LB_COMPRESSION}/' /usr/lib/live/build/lb_binary_rootfs > "$LOCAL_LIVE_BUILD/scripts/build/lb_binary_rootfs"
chmod 0755 "$LOCAL_LIVE_BUILD/scripts/build/lb_binary_rootfs"
COMPAT_BIN=$(mktemp -d)
cleanup_compat() { rm -rf "$COMPAT_BIN"; }
trap cleanup_compat EXIT INT TERM
if ! command -v rsvg >/dev/null 2>&1; then
  ln -s "$(command -v rsvg-convert)" "$COMPAT_BIN/rsvg"
  PATH="$COMPAT_BIN:$PATH" LIVE_BUILD="$LOCAL_LIVE_BUILD" lb build 2>&1 | tee "$ARTIFACTS/build.log"
else
  LIVE_BUILD="$LOCAL_LIVE_BUILD" lb build 2>&1 | tee "$ARTIFACTS/build.log"
fi
ISO=$(find "$ROOT" -maxdepth 1 -type f \( -name '*.hybrid.iso' -o -name '*.iso' \) -print -quit)
[ -n "$ISO" ] || { echo 'ISO was not produced.' >&2; exit 1; }
BASE_ISO="$ARTIFACTS/.drakonis-linux-bios.iso"
cp "$ISO" "$BASE_ISO"
./scripts/add-uefi-boot.sh "$BASE_ISO" "$ARTIFACTS/drakonis-linux-amd64.iso"
rm -f "$BASE_ISO"
sha256sum "$ARTIFACTS/drakonis-linux-amd64.iso" > "$ARTIFACTS/drakonis-linux-amd64.iso.sha256"
echo "Created $ARTIFACTS/drakonis-linux-amd64.iso"
