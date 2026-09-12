# Drakonis Vault

Drakonis Vault is a local, offline-first case workspace for authorized defensive analysis. It creates a case directory under `~/Drakonis-Cases`, stores copied evidence files, records SHA-256 hashes and timestamps in a JSON Lines manifest, and records case events in an append-only event log.

## Commands

```bash
drakonis-vault create case-001 --purpose "authorized lab validation"
drakonis-vault add case-001 /path/to/result.txt
drakonis-vault status case-001
drakonis-vault verify case-001
drakonis-vault seal case-001
drakonis-vault list
```

Sealing verifies every recorded hash, marks the case sealed, and changes case files to read-only. A sealed case cannot accept additional evidence through the tool; create a new case or an explicitly documented derivative for new material. The GTK application is available as **Drakonis Vault** and as the **Case Workspace** page in Drakonis Control Center.

The feature is local by design. It does not upload evidence or contact external targets. Operators remain responsible for authorization, privacy, retention, and applicable evidence-handling requirements.
