## Drakonis Linux v6.0.0

Drakonis Linux v6.0.0 implements the supplied Kali XFCE/Debian design direction as an interactive XFCE desktop layer. The release keeps the Debian Stable base, Drakonis safety model, authorized-lab tooling, and verified BIOS/UEFI boot path while adding a cohesive desktop shell.

The image includes Plank Dock with launchers for the Drakonis Control Center, terminal, Thunar, and Firefox ESR. The desktop shell applies the DRAKONIS-Night theme, preserves four XFCE workspaces, enables compositing, and starts the Dock automatically.

The Drakonis Control Center provides native launch surfaces for Security Center, Network Tools, System Monitor, Software Center, Settings Center, Themes Manager, File Manager, Secure Web Browser, and Help Center. These are real local interactions using XFCE and Debian utilities; they do not automatically scan external targets or alter firewall policy.

The package set adds the desktop components required by the design layer, including Plank, YAD, Zenity, Mousepad, Thunar, XFCE notifications, and the existing authorized security-analysis tools. The design implementation covers the visual language and functional shell concepts from the 32-page design book; pixel-perfect equivalence still requires graphical VM acceptance at target resolutions.

Validation completed:

- `scripts/check-project.sh`: passed.
- ISO payload inspection: v6.0 Control Center, desktop shell, autostart, Dock launchers, and background present in `filesystem.squashfs`.
- Interactive package manifest: passed for Plank, YAD, Zenity, Mousepad, XFCE notifications, Thunar, and Firefox ESR.
- QEMU BIOS smoke test: reached ISOLINUX 6.04 without bootloader failure.
- QEMU/OVMF UEFI smoke test: reached GNU GRUB without boot failure.
- El Torito report: BIOS and UEFI entries present.

This ISO is for authorized defensive analysis, CTFs, owned networks, and isolated labs only.

SHA-256: `3d4f8be739ea5adea886227d89dd08e36d4818bcfad20677d4fdc092d4dcb7d6`
