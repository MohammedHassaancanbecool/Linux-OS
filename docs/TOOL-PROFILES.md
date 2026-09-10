# Tool profiles

The Debian image provides a stable core and optional installable profiles. The profiles are inspired by common BlackArch categories, but they use Debian package names and Debian repositories. They are not a repackaged copy of BlackArch.

| Profile | Typical capabilities |
|---|---|
| `network` | Discovery, DNS, routing, packet and service diagnostics |
| `web` | Web application assessment, HTTP inspection, fuzzing, and API utilities |
| `passwords` | Local password auditing and hash testing on authorized samples |
| `wireless` | Wireless diagnostics and capture tooling; requires compatible hardware and an isolated lab |
| `forensics` | Disk, file, metadata, malware triage, and memory-analysis utilities |
| `reverse` | Debugging, disassembly, binary inspection, tracing, and instrumentation |

Install one profile from a checkout:

```bash
sudo ./scripts/install-profile.sh network
sudo ./scripts/install-profile.sh web
```

The installer checks each package with `apt-cache`, installs packages available in the configured Debian repositories, and reports unavailable names without treating them as proof that an equivalent tool is safe or supported. Package names and availability vary by Debian release; review the transaction before use.

Tools that require proprietary licensing, vendor repositories, special hardware, or a different package format are not silently embedded in the ISO. Burp Suite remains operator-installed from its official vendor. BlackArch's own repository remains isolated to the separate Arch profile.

All use is restricted to systems, accounts, traffic, and data that the operator owns or is explicitly authorized to test. No profile enables automatic target discovery or external connections at first boot.

## Exploitation and vulnerability research

The `exploitation` profile includes `metasploit-framework`, `exploitdb`, `searchsploit`, and `set` when those packages are available from the configured Debian repositories. Metasploit is intentionally optional: the image does not mix Kali, BlackArch, or untrusted third-party APT sources into Debian. If `metasploit-framework` is unavailable, the installer reports it and the operator must use Rapid7's official package and licensing instructions in an isolated authorized lab.
