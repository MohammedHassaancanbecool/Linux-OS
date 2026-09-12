# Release acceptance checklist

A release such as v0.3.0 is not published until the following checks are recorded for the exact artifact hash.

| Check | Required result |
|---|---|
| Build host | Debian Stable or supported Ubuntu, clean checkout |
| Project checks | `./scripts/check-project.sh` passes |
| ISO build | `sudo ./scripts/build-iso.sh` completes without ignored errors |
| Integrity | SHA-256 file exists beside the ISO |
| Boot | ISO boots in BIOS and UEFI on x86_64 |
| Desktop | XFCE starts and LightDM presents the analyst account |
| Safety | Legal notice and `mll-help` are visible; no automatic network target activity occurs |
| Isolation | `sudo mll-network-isolation enable` blocks non-loopback output and `status` shows rules |
| Tools | `nmap --version`, `tshark --version`, `sqlmap --version`, `hydra -h`, `john --test` and `hashcat --version` are checked in the guest |
| Updates | Package update and reboot are tested in a disposable snapshot |
| VM | Guest installs to a virtual disk and reboots without the ISO |
| OVA | Exported OVA imports on a clean VirtualBox host and boots with host-only networking |
| Documentation | Artifact hash, build date, package manifest, known issues, and test host are recorded |

## Known limitations for the initial engineering baseline

This repository cannot certify an OVA without an available virtualization host. It also cannot claim support for every wireless chipset, GPU, ARM board, or proprietary tool. Those items require a hardware matrix and separate release work.
