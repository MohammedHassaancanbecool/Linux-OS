# Drakonis desktop design implementation

This document maps the supplied Debian XFCE design brief to the current image implementation. The design uses Drakonis branding rather than copying another distribution's trademarks or artwork.

| Design area | Current implementation | Acceptance check |
|---|---|---|
| Indigo/blue-violet identity | `DRAKONIS-Night` GTK/XFWM theme and branded wallpaper | Verify readable text and active-state contrast at 1920×1080 and a smaller display |
| Cyan and violet accents | GTK selection, focus, hover, and progress colors | Keyboard focus remains visible; error states remain reserved for warnings |
| Graphite terminal | `/etc/xdg/xfce4/terminal/terminalrc` with dark background and 86% background darkness | Confirm terminal text remains legible over the wallpaper |
| Large left-side mark | `branding/drakonis-wallpaper.png` installed as the desktop background | Windows do not obscure the primary working area unnecessarily |
| Branded login | LightDM greeter uses the wallpaper, mark, and DRAKONIS-Night theme | Login is boot-tested in the guest |
| Profiles launcher | Existing XFCE launcher plus network, web, forensic, reverse, exploitation, and optional `redteam` profiles | Profile installation reports unavailable packages instead of using untrusted sources |
| Utility screens | Security Center, Network Tools, Help Center, Themes Manager, First Run, and Power & Session terminal utilities with Applications entries | No automatic target discovery; destructive power actions require explicit confirmation |
| Interactive control center | GTK3/PyGObject application with searchable sidebar, cards, keyboard navigation, live command results, and 16 screen destinations | Verify at 1920×1080 and 1280×720 in the VM; actions remain local and authorization-scoped |
| Safety boundary | Isolation helper, legal-use notice, no automatic discovery, no persistence or evasion helpers | Isolation enable/disable and first boot are tested in a disposable lab |

The remaining larger screens in the brief—Workspace Overview, Software Center, a graphical Notification Center, and a full Settings Center—remain product work items. The first functional utility pass now provides safe XFCE-native terminal utilities for security status, local network inspection, help, themes, first-run guidance, and power/session actions.

## Red-team boundary

The `redteam` profile is intended for owned systems, written-scope engagements, CTFs, and isolated training ranges. It uses Debian package resolution only. It does not add Kali, BlackArch, or arbitrary third-party APT sources, and it does not package credential theft, covert persistence, evasion, destructive payloads, or automated external targeting.
