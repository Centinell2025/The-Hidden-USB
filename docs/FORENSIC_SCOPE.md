# The Hidden USB — Evidence design and limitations

**BEACON OF THE EAGLE LLC · CENTINELL SUITE DEFENSE**

## Evidence surfaces

- Device installation and mount events, with unrelated benign device activity
- Simulated registry drive-letter and volume-GUID mapping
- Simulated logon sessions and file operations
- USN-style file-reference, create and deletion observations
- Simulated removable transfer audit and change authorization
- Simulated DLP alert and source-clock uncertainty
- Real harmless ZIP specimen containing fictional CSV and README bytes
- SHA-256 inventory and a real queryable SQLite cache *derived* from source CSVs

## Trust and realism

Every stream is a **controlled educational simulation**, explicitly registered in `acquisition_register.csv`. The CSV exports **are not EVTX, registry hives, original NTFS USN journals, Windows memory images or a forensic USB image**. The recovered ZIP's integrity is independently reproducible from the delivered bytes, but its supposed origin remains fictional. Matching CSV values do not cryptographically authenticate a user, removable device or actual external transfer.

Distinguish hypotheses: authorized user activity, accidental policy violation, and unauthorized removable-media handling. All may be considered; conclusions must state what this *specific* evidence proves. The case should not be marketed as a confirmed criminal incident or certified Hard exercise.

## Verification

Use `sha256sum -c artifacts/SHA256SUMS.txt`, `python3 -m zipfile -l artifacts/recovered_export.zip`, and SQLite read-only mode. Use no real PII and no live malware. The final 18 questions are **machine-gradable candidates**; a separate instructor key, solution screenshots and two blind non-author solves are still required before a credible HTB submission.
