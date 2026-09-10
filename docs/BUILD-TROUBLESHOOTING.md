# Build troubleshooting

The repository was checked in the Manus Ubuntu build environment. `live-build` successfully bootstrapped the Debian Stable base and resolved the package indexes. The image assembly stopped in the Ubuntu-packaged `live-build 3.0~a57` helper while fetching `dists/stable/Contents-amd64.gz`; the current Debian mirror does not publish that legacy path. This is an incompatibility between the host's live-build version and the current Debian mirror layout, not a package-list or source-tree error.

For a production build, use a clean Debian Stable host and install the live-build version documented by the Debian Live team, or run the build in a Debian Stable container/VM. Then execute:

```bash
sudo ./scripts/check-project.sh
sudo ./scripts/build-iso.sh
```

If the host still invokes the legacy Contents fetch, upgrade live-build from the supported Debian package or apply the distribution's current live-build patch. Do not bypass signature checks or replace Debian mirrors with untrusted sources. After a successful ISO build, follow `docs/RELEASE-CHECKLIST.md` before exporting an OVA.
