# Release acceptance checklist

A release such as 7.0.0 is not published until the following checks are recorded for the exact artifact hash.

| Check | Required result |
|---|---|
| Build host | Debian Stable or supported Ubuntu, clean checkout |
| Project checks | `./scripts/check-project.sh` passes |
| ISO build | `sudo ./scripts/build-iso.sh` completes without ignored errors |
| Integrity | SHA-256 file exists beside the ISO |
| Boot | ISO boots in BIOS and UEFI on x86_64 |
| Desktop | GNOME Shell starts and GDM3 presents the analyst account |
| Visual identity | Wallpaper, GDM3 artwork, DRAKONIS-Night, Plank dock, and four workspaces are present |
| Safety | Legal notice and `mll-help` are visible; no automatic network target activity occurs |
| Isolation | `sudo mll-network-isolation enable` blocks non-loopback output and `status` shows rules |
| Tools | `nmap --version`, `tshark --version`, `sqlmap --version`, `hydra -h`, `john --test` and `hashcat --version` are checked in the guest |
| Updates | Package update and reboot are tested in a disposable snapshot |
| VM | Guest installs to a virtual disk and reboots without the ISO |
| Documentation | Artifact hash, build date, package manifest, known issues, and test host are recorded |
| Vault | Case create/add/verify/report/seal flows pass in a temporary HOME |
| Software Center | Profile listing and package policy use only configured Debian repositories |
