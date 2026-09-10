#!/bin/sh
set -eu

if ! command -v pacman >/dev/null 2>&1; then
  cat >&2 <<'EOF'
This helper is for an Arch Linux / BlackArch base only.
It is intentionally not executable on Drakonis Linux Debian.
Debian and Arch packages are not interchangeable; do not add BlackArch
repositories to Debian because that can corrupt the package graph.

Use the separate Arch-based profile documented in profiles/blackarch/README.md.
EOF
  exit 2
fi

[ "$(id -u)" -eq 0 ] || { echo 'Run as root.' >&2; exit 1; }
command -v curl >/dev/null 2>&1 || { echo 'curl is required.' >&2; exit 1; }

cat <<'EOF'
You are about to add the official BlackArch repository to an Arch system.
Only continue on a disposable, authorized lab machine.
The blackarch package group may install thousands of packages and require
substantial disk space. Review licenses and package changes before proceeding.
EOF
printf 'Type INSTALL-BLACKARCH-REPOSITORY to continue: '
read answer
[ "$answer" = 'INSTALL-BLACKARCH-REPOSITORY' ] || { echo 'Cancelled.'; exit 1; }

workdir=$(mktemp -d)
trap 'rm -rf "$workdir"' EXIT
cd "$workdir"
curl --fail --proto '=https' --tlsv1.2 -o strap.sh https://blackarch.org/strap.sh
printf '%s  %s\n' '00688950aaf5e5804d2abebb8d3d3ea1d28525ed' strap.sh | sha1sum -c -
chmod 0755 strap.sh
./strap.sh
pacman -Syu --needed
printf '%s\n' 'Repository enabled. To install the complete official group, review first:'
pacman -Sg blackarch | less
printf '%s\n' 'Then, only with explicit authorization: pacman -S blackarch'
