#!/bin/sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
ARTIFACTS="$ROOT/artifacts"
ISO="$ARTIFACTS/mobile-linux-lab-amd64.iso"
mkdir -p "$ARTIFACTS"
[ -f "$ISO" ] || { echo "Build the ISO first: sudo ./scripts/build-iso.sh" >&2; exit 1; }
if ! command -v VBoxManage >/dev/null 2>&1; then
  cat >&2 <<'EOF'
VBoxManage is not installed. An OVA must be exported from a boot-tested VM.
On a virtualization host:
  VBoxManage createvm --name Mobile-Linux-Lab --register
  VBoxManage modifyvm Mobile-Linux-Lab --memory 4096 --cpus 2 --nic1 hostonly
  VBoxManage storagectl Mobile-Linux-Lab --name SATA --add sata --controller IntelAhci
  VBoxManage createhd --filename Mobile-Linux-Lab.vdi --size 32768
  VBoxManage storageattach Mobile-Linux-Lab --storagectl SATA --port 0 --device 0 --type hdd --medium Mobile-Linux-Lab.vdi
  VBoxManage storageattach Mobile-Linux-Lab --storagectl SATA --port 1 --device 0 --type dvddrive --medium mobile-linux-lab-amd64.iso
  # Boot, install, remove ISO, then verify the guest before exporting:
  VBoxManage export Mobile-Linux-Lab --output artifacts/mobile-linux-lab-amd64.ova
EOF
  exit 2
fi
VBoxManage --version
cat <<'EOF'
ISO is ready. Create a VM, install and boot-test it, then export only after completing docs/RELEASE-CHECKLIST.md.
EOF
