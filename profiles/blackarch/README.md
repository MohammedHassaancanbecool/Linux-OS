# BlackArch complete-tool profile

BlackArch is an **Arch Linux-based** repository. Its packages cannot be installed safely as Debian `.deb` packages, and the BlackArch repository must not be added to the Debian Mobile Linux Lab image.

The official BlackArch project documents a repository group named `blackarch` that can install the complete tool set on an Arch system. This repository therefore keeps the Debian XFCE image stable and provides `scripts/install-blackarch-tools.sh` as an explicit, opt-in helper for a separate Arch-based VM or build profile.

## Recommended deployment

Use one of these supported layouts:

| Layout | Recommendation |
|---|---|
| Debian Mobile Linux Lab + selected Debian tools | Default, smaller and easier to update |
| Separate Arch/BlackArch VM | Use when the complete BlackArch package group is required |
| Dual-VM lab | Recommended for comparison and isolation |

The complete group may consume substantial storage and can introduce package conflicts. Review the package transaction and license notices before confirming installation. Keep the VM host-only or offline until its update and isolation policy is verified.

```bash
sudo ./scripts/install-blackarch-tools.sh
# After the repository is configured and reviewed:
sudo pacman -S blackarch
```

The helper verifies the SHA-1 value currently published by BlackArch for `strap.sh`, prompts for an explicit confirmation, and refuses to run when `pacman` is absent. It does not download or install the entire group automatically.

## References

[1]: https://blackarch.org/downloads.html "BlackArch official downloads and installation instructions"
[2]: https://github.com/BlackArch/blackarch "BlackArch official package repository"
