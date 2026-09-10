# Architecture

## Decision

Drakonis Linux is now an operating-system distribution build, not an Expo application. The source tree is intentionally declarative: `live-build` assembles a Debian Stable live image, package lists define the baseline, hooks apply small deterministic changes, and included files provide the safety boundary and user guidance.

## Layers

| Layer | Implementation | Rationale |
|---|---|---|
| Base OS | Debian Stable amd64 | Stable package lifecycle and broad hardware support |
| Desktop | XFCE and LightDM | Low resource use and predictable lab VM behavior |
| Connectivity | NetworkManager plus nftables helper | Easy switching between isolated and authorized lab networks |
| Analysis | Debian-packaged network, web, wireless, and forensic utilities | Reproducible installation and package provenance |
| Education | Legal-use notice, local help, release checklist | Reduces accidental misuse and clarifies limits |
| Delivery | Hybrid ISO, then tested VM export to OVA | ISO is the primary artifact; OVA is a tested appliance derivative |

The distribution does not automatically scan targets, execute user-provided shell strings, collect credentials, persist covertly, evade detection, or contact external targets on first boot. Tools remain general-purpose packages; their lawful use depends on the operator and network boundary.

## Package policy

The core profile contains packages available from Debian repositories. Optional tools with uncertain availability or separate licensing are kept disabled in `mll-optional.list.chroot_disabled`. Burp Suite is not redistributed because it is proprietary. Metasploit is not treated as a guaranteed core dependency; an operator may add it in a separately reviewed build after confirming repository provenance and licensing.

## Release boundary

The first version is a buildable engineering baseline, not a claim of parity with Kali Linux or Parrot Security. Feature parity requires hardware testing, installer testing, update policy, package curation, documentation, signed releases, vulnerability response, and repeated ISO/OVA boot validation.

## References

[1]: https://www.debian.org/releases/stable/ "Debian Stable release information"
[2]: https://live-team.pages.debian.net/live-manual/ "Debian Live Manual"
