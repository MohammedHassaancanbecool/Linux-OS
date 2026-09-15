#!/bin/sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
ISO=${ISO:-$ROOT/artifacts/drakonis-linux-amd64.iso}
MODE=bios
RAM=${RAM:-4096}
HEADLESS=0
NETWORK=0
usage() {
  cat <<EOF
Usage: $0 [--bios|--uefi] [--headless] [--network] [iso]

Defaults: BIOS, ${RAM}M RAM, one virtual CPU without KVM, and no network.
KVM is enabled automatically when /dev/kvm is available.
EOF
}
while [ "$#" -gt 0 ]; do
  case "$1" in
    --bios) MODE=bios ;;
    --uefi) MODE=uefi ;;
    --headless) HEADLESS=1 ;;
    --network) NETWORK=1 ;;
    -h|--help) usage; exit 0 ;;
    -*) echo "Unknown option: $1" >&2; usage >&2; exit 2 ;;
    *) ISO=$1 ;;
  esac
  shift
done
command -v qemu-system-x86_64 >/dev/null 2>&1 || { echo 'qemu-system-x86_64 is required.' >&2; exit 1; }
[ -s "$ISO" ] || { echo "ISO not found: $ISO" >&2; exit 1; }
set -- qemu-system-x86_64 -m "$RAM" -smp 1 -cdrom "$ISO" -boot order=d
if [ -e /dev/kvm ] && [ -r /dev/kvm ] && [ -w /dev/kvm ]; then
  set -- "$@" -accel kvm -enable-kvm
  printf '%s\n' 'QEMU acceleration: KVM'
else
  set -- "$@" -accel tcg,thread=multi -cpu max
  printf '%s\n' 'QEMU acceleration: TCG (one virtual CPU; slower compatibility mode)'
fi
if [ "$MODE" = uefi ]; then
  CODE=${OVMF_CODE:-/usr/share/OVMF/OVMF_CODE_4M.fd}
  VARS_TEMPLATE=${OVMF_VARS:-/usr/share/OVMF/OVMF_VARS_4M.fd}
  VARS=${OVMF_VARS_FILE:-$ROOT/artifacts/qemu-OVMF_VARS.fd}
  [ -r "$CODE" ] || { echo "OVMF code not found: $CODE" >&2; exit 1; }
  [ -r "$VARS_TEMPLATE" ] || { echo "OVMF vars template not found: $VARS_TEMPLATE" >&2; exit 1; }
  if [ ! -e "$VARS" ]; then cp "$VARS_TEMPLATE" "$VARS"; fi
  set -- "$@" -drive "if=pflash,format=raw,readonly=on,file=$CODE" -drive "if=pflash,format=raw,file=$VARS"
fi
if [ "$NETWORK" -eq 0 ]; then
  set -- "$@" -nic none
else
  set -- "$@" -nic user,model=virtio-net-pci
fi
if [ "$HEADLESS" -eq 1 ]; then
  set -- "$@" -nographic
fi
exec "$@"
