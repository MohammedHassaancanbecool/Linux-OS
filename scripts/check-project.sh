#!/bin/sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
fail=0
for path in README.md config/auto/config config/package-lists/mll-core.list.chroot includes.chroot/etc/motd includes.chroot/usr/local/bin/mll-help includes.chroot/usr/local/bin/mll-network-isolation hooks/normal/0100-mll-hardening.chroot hooks/normal/0150-mll-tool-profiles.chroot docs/ARCHITECTURE.md docs/RELEASE-CHECKLIST.md docs/BUILD-TROUBLESHOOTING.md docs/TOOL-PROFILES.md profiles/blackarch/README.md scripts/build-iso.sh scripts/build-ova.sh scripts/install-blackarch-tools.sh scripts/install-profile.sh config/package-profiles/network.list config/package-profiles/web.list config/package-profiles/passwords.list config/package-profiles/wireless.list config/package-profiles/forensics.list config/package-profiles/reverse.list; do
  if [ ! -f "$ROOT/$path" ]; then echo "MISSING $path"; fail=1; fi
done
for path in config/auto/config includes.chroot/usr/local/bin/mll-help includes.chroot/usr/local/bin/mll-network-isolation hooks/normal/0100-mll-hardening.chroot hooks/normal/0150-mll-tool-profiles.chroot scripts/build-iso.sh scripts/build-ova.sh scripts/install-blackarch-tools.sh scripts/install-profile.sh; do
  sh -n "$ROOT/$path" || fail=1
done
if grep -RniE 'password[[:space:]]*[=:]|secret[[:space:]]*[=:]|api[_-]?key[[:space:]]*[=:]|private[_-]?key[[:space:]]*[=:]|BEGIN (RSA|OPENSSH|EC) PRIVATE KEY' "$ROOT/includes.chroot" "$ROOT/hooks" 2>/dev/null; then echo 'Potential secret-like content found'; fail=1; fi
# Safety terminology is intentionally discussed in the documentation. Restrict
# this automated check to image payloads and hooks, where executable behavior
# would matter.
if grep -RniE 'credential dump|steal' "$ROOT/includes.chroot" "$ROOT/hooks" 2>/dev/null; then echo 'Potentially unsafe payload wording found'; fail=1; fi
[ "$fail" -eq 0 ] && echo 'Project checks passed.'
exit "$fail"
