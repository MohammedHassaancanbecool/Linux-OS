# Boot validation for Drakonis Linux

The release ISO is validated as a hybrid BIOS/UEFI image rather than relying only on the exit status of `live-build`.

The Syslinux template includes `ldlinux.c32`, `libcom32.c32`, and `libutil.c32` in `/isolinux/`. QEMU BIOS reaches `ISOLINUX 6.04` without the former `Failed to load ldlinux.c32` or `Boot failed` errors.

The build adds an EFI El Torito image containing a standalone GRUB x86_64 EFI loader. QEMU with OVMF reaches the GNU GRUB menu, and the GRUB configuration searches for the `DRAKONIS_STABLE_X86_64` ISO label before loading `/live/vmlinuz` and `/live/initrd.img`.

The final ISO El Torito report contains both entries:

| Firmware path | Image |
|---|---|
| BIOS | `/isolinux/isolinux.bin` |
| UEFI | `/EFI/BOOT/efiboot.img` |

The QEMU smoke tests intentionally stop after the boot menu or firmware loader is reached. A complete XFCE graphical-session test still requires a graphical VM display or a physical test machine; serial QEMU is not a substitute for visual desktop acceptance testing.

## Supported QEMU launcher

Use `scripts/run-qemu.sh` to run the release ISO with one virtual CPU and networking disabled by default:

```bash
./scripts/run-qemu.sh --bios
./scripts/run-qemu.sh --uefi
```

The launcher enables KVM automatically when `/dev/kvm` is readable and writable. When KVM is unavailable, it selects TCG with one virtual CPU and `-cpu max` as a slower compatibility mode. Add `--network` only for an explicitly authorized lab network. Add `--headless` for serial or boot-smoke tests; this is not a substitute for graphical XFCE acceptance.
