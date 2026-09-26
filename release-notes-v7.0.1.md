# Drakonis Linux 7.0.1

Drakonis Linux 7.0.1 is a packaging-size patch for the 7.0 GNOME release.

## Changes

- Keeps GNOME Shell, GDM3, Nautilus, Plank, Drakonis Control Center, themes, and security-analysis profiles.
- Removes host-side QEMU/OVMF utilities and development toolchains that are not needed inside the Live ISO.
- Keeps QEMU validation tools on the build host and documents the reduced image boundary.
- Produces an ISO below GitHub's 2 GiB release-asset limit.

The release remains Debian Stable amd64, safe-by-default, and intended only for authorized defensive analysis and isolated labs.
