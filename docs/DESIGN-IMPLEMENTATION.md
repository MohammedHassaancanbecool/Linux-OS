# Drakonis Linux 7.0 desktop design implementation

This document maps the supplied, rights-cleared Drakonis visual direction to the GNOME image implementation. The design uses the independent Drakonis identity and does not copy another distribution's trademarks or artwork.

| Design area | GNOME 7.0 implementation | Acceptance check |
|---|---|---|
| Indigo/blue-violet identity | `DRAKONIS-Night` GTK theme, GNOME dark color scheme, and branded wallpaper | Verify readable text and active-state contrast at 1920×1080 and 1280×720 |
| Cyan and violet accents | GTK selection, focus, hover, and progress colors | Keyboard focus remains visible; warning states remain distinct |
| Graphite terminal | GNOME Terminal profile with dark palette and transparent-style panel treatment | Confirm terminal text remains legible over the wallpaper |
| Dragon mark | Rights-cleared Drakonis wallpaper and login artwork | Mark remains visible without obscuring working windows |
| Branded login | GDM3 with Drakonis artwork and GNOME session | Boot-test GDM3 in the guest; verify manual username/password login |
| Centered dock | Plank autostarted inside GNOME, with GNOME Overview retained for workspace management | Dock launches Control Center, terminal, files, and Firefox |
| Profiles launcher | GNOME applications entries plus network, web, forensic, reverse, exploitation, and optional `redteam` profiles | Profile installer reports unavailable packages rather than using untrusted sources |
| Utility screens | Security Center, Network Tools, Help Center, Themes Manager, First Run, and Power & Session utilities | No automatic target discovery; destructive power actions require explicit confirmation |
| Interactive control center | GTK3/PyGObject app with searchable sidebar, cards, keyboard navigation, local command results, and 17 destinations | Verify at 1920×1080 and 1280×720 in a graphical VM |
| Safety boundary | Isolation helper, legal-use notice, no automatic discovery, persistence, or evasion helpers | Isolation and first boot are tested in a disposable lab |

## GNOME session policy

The image uses Debian Stable's `task-gnome-desktop`, GNOME Shell, GDM3, and NetworkManager. Four workspaces are configured on first login. The shell script applies the Drakonis theme through `gsettings`; Plank provides the centered dock shown in the supplied design while GNOME Overview remains available through the standard Activities entry and keyboard shortcut.

## Red-team boundary

The `redteam` profile is intended for owned systems, written-scope engagements, CTFs, and isolated training ranges. It uses Debian package resolution only. It does not add Kali, BlackArch, or arbitrary third-party APT sources, and it does not package credential theft, covert persistence, evasion, destructive payloads, or automated external targeting.

## Validation boundary

The ISO must be smoke-tested through BIOS and UEFI boot. Visual acceptance requires a graphical VM or physical test machine; serial boot output alone is not sufficient to certify GDM3 or GNOME rendering.
