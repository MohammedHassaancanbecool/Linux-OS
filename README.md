# Drakonis Linux

Drakonis Linux is a Debian Stable XFCE security-analysis distribution for **authorized defensive analysis and isolated lab work**. It is an independent desktop product with its own identity, themes, artwork, and security-tool profiles.

The first release targets **x86_64 live ISO** and provides a documented path to an **OVA** appliance. It uses Debian packages wherever possible and does not redistribute proprietary software. Commercial tools such as Burp Suite must be installed by the operator from the vendor's official source and license terms.

> This project is not a license to test systems that you do not own or explicitly administer. Use the included isolation profile, snapshots, host-only networking, and training targets.

## Scope of the first build

| Area | Status |
|---|---|
| Debian Stable base | Configured through `live-build` |
| XFCE desktop | Configured |
| Offline-safe boot notice | Configured |
| Local analyst utilities | Nmap, Wireshark/TShark, SQLMap, Hydra, Gobuster, John, Hashcat, netcat, tcpdump; optional profiles cover additional utilities |
| Web testing | OWASP ZAP package availability is checked during build; Burp Suite is operator-installed |
| Exploitation frameworks | Metasploit is not silently bundled; an explicit opt-in profile is provided where a trusted package source is available |
| ISO | `scripts/build-iso.sh` |
| OVA | `scripts/build-ova.sh`, requires a VM image builder such as VirtualBox or Packer |
| Automated checks | `scripts/check-project.sh` |

## Build requirements

Build on a Debian Stable or Ubuntu host with root access, internet access, at least 30 GB free disk, and at least 8 GB RAM. The build host must have `live-build`, `debootstrap`, `xorriso`, `isolinux`, and `qemu-utils`. The repository includes a local Syslinux bootloader template to work around older live-build path assumptions. The repository does not require Node.js.

```bash
sudo apt-get update
sudo apt-get install -y live-build debootstrap xorriso isolinux qemu-utils git ca-certificates
./scripts/check-project.sh
sudo ./scripts/build-iso.sh
```

The result is written to `artifacts/` and includes a SHA-256 checksum. The build is intentionally reproducible from the package manifest and hook files, subject to Debian repository updates.

## BlackArch tool coverage

BlackArch packages target Arch Linux and are not compatible with Debian's package graph. The Debian ISO therefore does not mix BlackArch repositories into its APT sources. When the complete BlackArch catalog is required, use the separate Arch-based profile in `profiles/blackarch/` and run `scripts/install-blackarch-tools.sh` inside that Arch VM. The helper is opt-in, verifies the official bootstrap checksum, and requires an explicit confirmation before repository changes. This avoids presenting an unstable mixture of Debian and Arch packages as a supported release.

For practical Debian-native coverage, use the installable profiles in `config/package-profiles/` with `scripts/install-profile.sh`. Profiles cover network, web, passwords, wireless, forensics, reverse engineering, and exploitation. The installer installs only package names available from the configured Debian repositories and reports the rest for review.

## OVA path

An OVA is a virtual appliance export, not a different Linux distribution. The recommended path is:

1. Build and boot the ISO in a disposable VM.
2. Install to a virtual disk using the included post-install checklist.
3. Keep networking disabled or host-only while testing.
4. Export the tested VM with VirtualBox `VBoxManage export` or use the documented Packer workflow.

The sandbox used to develop this repository may not contain VirtualBox or KVM, so this repository provides the automation and validation checks but does not claim an OVA until it has been boot-tested and exported on a virtualization host.

## Safety model

The default profile is **safe-by-default**. It displays a legal-use notice, keeps tools local, avoids automatic target discovery, does not enable promiscuous capture by default, and does not ship credentials, exploit payloads, persistence, evasion, or data-exfiltration helpers. Network modes should be changed only for an explicitly authorized lab.

The distribution is intended for CTFs, owned test networks, defensive validation, malware-analysis sandboxes without internet access, and classroom exercises. Never connect an unpatched lab image directly to an untrusted production network.

## Repository layout

- `config/` contains live-build configuration and package profiles.
- `includes.chroot/` contains files copied into the image.
- `hooks/` contains deterministic post-install hardening and notice hooks.
- `scripts/` contains build, check, ISO test, and OVA guidance scripts.
- `docs/` contains architecture, threat model, and release acceptance criteria.

## License

The build scripts and documentation are released under the MIT License. Every included third-party package remains under its own license. Debian trademarks and package copyrights belong to their respective owners.

## References

[1]: https://www.debian.org/releases/stable/ "Debian Stable release information"
[2]: https://live-team.pages.debian.net/live-manual/ "Debian Live Manual"
[3]: https://www.virtualbox.org/manual/ch08.html "VirtualBox VBoxManage export documentation"
[4]: https://owasp.org/www-project-zap/ "OWASP ZAP project"
[5]: https://blackarch.org/downloads.html "BlackArch official downloads and installation instructions"
