#!/bin/sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
PROFILE=${1:-}
case "$PROFILE" in
  network|web|passwords|wireless|forensics|reverse|exploitation) ;;
  *) echo "Usage: sudo $0 {network|web|passwords|wireless|forensics|reverse|exploitation}" >&2; exit 2;;
esac
[ "$(id -u)" -eq 0 ] || { echo 'Run with sudo.' >&2; exit 1; }
command -v apt-get >/dev/null 2>&1 || { echo 'This profile installer requires Debian/Ubuntu apt.' >&2; exit 1; }
if [ -f "/usr/local/share/mll/package-profiles/$PROFILE.list" ]; then
  LIST="/usr/local/share/mll/package-profiles/$PROFILE.list"
else
  LIST="$ROOT/config/package-profiles/$PROFILE.list"
fi
[ -f "$LIST" ] || { echo "Missing profile: $PROFILE" >&2; exit 1; }
export DEBIAN_FRONTEND=noninteractive
apt-get update
available=''
missing=''
while IFS= read -r package; do
  [ -n "$package" ] || continue
  case "$package" in \#*) continue;; esac
  if apt-cache show "$package" >/dev/null 2>&1; then
    available="$available $package"
  else
    missing="$missing $package"
  fi
done < "$LIST"
if [ -n "$available" ]; then
  # shellcheck disable=SC2086
  apt-get install -y --no-install-recommends $available
fi
printf '%s\n' "Installed available packages for profile: $PROFILE"
if [ -n "$missing" ]; then
  printf '%s\n' "Not available in the configured repositories (review separately):$missing"
fi
