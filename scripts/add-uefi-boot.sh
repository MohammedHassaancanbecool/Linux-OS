#!/bin/sh
set -eu
ISO=${1:?usage: add-uefi-boot.sh input.iso output.iso}
OUT=${2:?usage: add-uefi-boot.sh input.iso output.iso}
command -v grub-mkstandalone >/dev/null 2>&1 || { echo 'grub-mkstandalone is required.' >&2; exit 1; }
command -v mkfs.vfat >/dev/null 2>&1 || { echo 'dosfstools is required.' >&2; exit 1; }
command -v mcopy >/dev/null 2>&1 || { echo 'mtools is required.' >&2; exit 1; }
command -v xorriso >/dev/null 2>&1 || { echo 'xorriso is required.' >&2; exit 1; }
[ -f /usr/lib/ISOLINUX/isohdpfx.bin ] || { echo 'isohdpfx.bin is required.' >&2; exit 1; }
WORK=$(mktemp -d)
cleanup() { chmod -R u+w "$WORK" 2>/dev/null || true; rm -rf "$WORK"; }
trap cleanup EXIT INT TERM
TREE="$WORK/tree"
mkdir -p "$TREE"
xorriso -osirrox on -indev "$ISO" -extract / "$TREE" >/dev/null 2>&1
mkdir -p "$TREE/EFI/BOOT"
cat > "$WORK/grub.cfg" <<'EOF'
search --no-floppy --label DRAKONIS_STABLE_X86_64 --set=root
set timeout=5
set default=0
menuentry 'Drakonis Linux Live' {
  linux /live/vmlinuz boot=live components username=drakonis hostname=drakonis-linux quiet splash
  initrd /live/initrd.img
}
menuentry 'Drakonis Linux Live (failsafe)' {
  linux /live/vmlinuz boot=live components username=drakonis hostname=drakonis-linux noapic nolapic nomodeset
  initrd /live/initrd.img
}
EOF
grub-mkstandalone -O x86_64-efi -o "$WORK/BOOTX64.EFI" "boot/grub/grub.cfg=$WORK/grub.cfg"
dd if=/dev/zero of="$TREE/EFI/BOOT/efiboot.img" bs=1M count=16 status=none
mkfs.vfat "$TREE/EFI/BOOT/efiboot.img" >/dev/null
mmd -i "$TREE/EFI/BOOT/efiboot.img" ::EFI ::EFI/BOOT
mcopy -i "$TREE/EFI/BOOT/efiboot.img" "$WORK/BOOTX64.EFI" ::EFI/BOOT/BOOTX64.EFI
rm -f "$OUT"
xorriso -as mkisofs \
  -r -J -joliet-long \
  -V DRAKONIS_STABLE_X86_64 \
  -o "$OUT" \
  -isohybrid-mbr /usr/lib/ISOLINUX/isohdpfx.bin \
  -c isolinux/boot.cat \
  -b isolinux/isolinux.bin \
  -no-emul-boot -boot-load-size 4 -boot-info-table \
  -eltorito-alt-boot \
  -e EFI/BOOT/efiboot.img \
  -no-emul-boot -isohybrid-gpt-basdat \
  "$TREE" >/dev/null
printf '%s\n' "Created UEFI-capable ISO: $OUT"
