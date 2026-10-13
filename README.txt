THE HIDDEN USB — DEFENSIVE DFIR STUDENT LABORATORY
Publisher: BEACON OF THE EAGLE LLC
Brand: CENTINELL SUITE DEFENSE
Difficulty proposed: HARD CANDIDATE, not HTB certified or accepted.

1. Read PLAYER-INSTRUCTIONS.md, docs/FORENSIC_SCOPE.md, questions/INVESTIGATION.md.
2. Extract this ZIP into a sandbox directory. Do not execute extracted unknown files.
3. Verify SHA-256 inventory:
      cd artifacts && sha256sum -c SHA256SUMS.txt
4. Investigate Windows-like exports, registry mapping, USB events, file operations,
   USN-style records, DLP alerts, approval state and recovered_export.zip.
5. For the delivered training ZIP:
      unzip -l artifacts/recovered_export.zip
      sha256sum artifacts/recovered_export.zip
6. Optional SQLite read-only cache:
      sqlite3 'file:artifacts/timeline_cache.sqlite3?mode=ro' '.tables'

All data are synthetic training fixtures and all organizations/users are
fictional. USB logs are not a verified original disk image. A synthetic
copy assertion does not, alone, prove actual device possession, a human
identity, data loss, exfiltration or the contents of a real client drive.

No instructor answers are distributed with the student ZIP.
© 2026 Beacon of the Eagle LLC / Centinell Suite Defense.
