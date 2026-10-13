# The Hidden USB — Student investigation

**Author:** Beacon of the Eagle LLC — Centinell Suite Defense  
**Target difficulty:** Hard candidate, not independently measured.

Northbridge Systems, a completely fictional research company, reports unusual USB attachment during a maintenance window. The analyst must separate ordinary workstation activity from a correlated login, removable-media insertion, an asserted file copy, a USN-style creation/deletion pair, a DLP alert and a disputed authorization ticket.

Start with `README.txt` and verify `SHA256SUMS.txt`. Work through 18 exact-answer questions. Use free CSV tooling, Python 3, a ZIP reader and optional SQLite. The actual binary `recovered_export.zip` contains **only benign artificial data**. File hashes authenticate the delivered bytes, not the acquisition of a real USB device.

Every significant assertion must identify its event ID and collection boundary. The SQLite database is derived from the CSV exports, not a second original witness. Never imply that a suspicious account reveals a real human, that a copied file proves external Internet exfiltration, or that the fictional laboratory represents a real company breach.

The training exercise requires no live USB device, Windows endpoint, commercial tools, network scanning or exploitation.
