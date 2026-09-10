# Drakonis Linux visual identity

Drakonis Linux is the final product identity for the security-analysis distribution. The previous prototype identity is not used in the desktop, boot label, login screen, or release artwork.

The primary mark is a dragon head in strict side profile facing right. It uses an angular silhouette, a cyan eye, and cyan/violet edge accents to communicate analysis, vigilance, and technical precision without using skulls, weapons, or aggressive imagery.

The default desktop theme is **DRAKONIS-Night**, built around midnight navy `#07111f`, deep blue `#0b1728`, ice text `#e7f3ff`, and cyan accent `#08c7e8`. The alternate **DRAKONIS-Carbon** theme uses graphite `#111318`, panel `#181c22`, soft white `#f2f6fa`, and teal accent `#19d3ae`.

The wallpaper is installed at `/usr/share/backgrounds/drakonis-linux/Drakonis-Linux.png`. The login screen uses the same artwork and the dragon mark at `/usr/share/pixmaps/drakonis-linux/drakonis-mark.png`. XFCE defaults are installed through the analyst user's skeleton configuration, and LightDM uses the DRAKONIS-Night theme.

The desktop includes a Drakonis Tool Profiles launcher. Profiles cover network, web, passwords, wireless, forensics, reverse engineering, and optional exploitation/vulnerability research. Metasploit is intentionally an opt-in profile item and is installed only when a trusted configured package source provides it; Debian, BlackArch, and Kali repositories are not mixed.
