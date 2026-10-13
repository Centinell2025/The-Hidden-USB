<div align="center">
  <img src="https://raw.githubusercontent.com/Centinell2025/the-last-evidence-standing/main/branding/BEACON_SEAL.png" alt="Beacon of the Eagle LLC — logotipo corporativo" width="165" />
  <p><strong>BEACON OF THE EAGLE LLC</strong><br/><strong>CENTINELL SUITE DEFENSE</strong></p>
</div>

# The Hidden USB — Digital Forensics Sherlock

**Beacon of the Eagle LLC · Centinell Suite Defense**  
**Proposed category:** DFIR / Removable Media · **Target difficulty:** Hard candidate (not externally validated)

An analyst at a completely fictional Northbridge Systems investigates a removable-media insertion during maintenance. Correlate the recorded logon, USB device serial and volume mount, registry-style inventory, copied-file claims, USN-style create/delete, DLP alert, and authorization records. Reconcile a **real benign training archive** with SHA-256 without inventing exfiltration or a named attacker.

## Student laboratory — how to work

1. Open the [Hidden USB student archive workflow](https://github.com/Centinell2025/The-Hidden-USB/actions/workflows/validate.yml).
2. Choose the most recent successful execution; under *Artifacts*, download `hidden-usb-student`.
3. Extract `The-Hidden-USB-STUDENT.zip` and read `README.txt`, `PLAYER-INSTRUCTIONS.md`, `docs/FORENSIC_SCOPE.md` and the [18 exact questions](questions/INVESTIGATION.md).
4. Verify `artifacts/SHA256SUMS.txt` before answering. All required tools are free; live USB access is unnecessary.

To reproduce locally with Python 3:

```bash
python3 tools/build_lab.py
python3 tools/verify_lab.py
python3 -m unittest discover -s tests -v
python3 tools/build_student_zip.py
```

## Scientific and submission status

- Generated evidence includes actual ZIP specimen bytes and a real SQLite cache; the Windows-style logs and USB registry records are simulated.
- The ZIP contains **no instructor answers**; the public generator repository is not appropriate for blind solving.
- **Not yet HTB submission-approved:** requires an independently verified instructor key and write-up, blind test and difficulty calibration.
- No real organization is an incident victim. This is a safe educational training scenario, not a documented compromise or external certification.

© 2026 Beacon of the Eagle LLC — Centinell Suite Defense. Corporate emblem denotes authorship only.
