# The Hidden USB — 18 defensible DFIR questions

**Fictional Northbridge Systems incident · NB-USB-0917 · Hard candidate, unverified.**  
All times are UTC. Source exports are simulations, not actual Windows registry hives, EVTX, MFT, USN journal acquisitions or a recovered customer drive. Justify each response with an exact source, event identifier and, when applicable, hash.

## Stage 1 — Identity and removable device

**Q01.** Which endpoint recorded the suspicious removable-device arrival? **Answer:** hostname.

**Q02.** Which account was logged onto that endpoint and linked to the USB arrival? **Answer:** account string.

**Q03.** What hexadecimal logon ID corresponds to that user's successful recorded session? **Answer:** `0x...`.

**Q04.** Which USB serial distinguishes the target device from the benign connected-device history? **Answer:** exact serial.

**Q05.** What is the complete simulated USB device instance ID matched by both the installation export and registry record? **Answer:** complete ID.

**Q06.** When was the target device first recorded as arrived? Do not use mount time. **Answer:** `YYYY-MM-DDTHH:MM:SSZ`.

**Q07.** Which simulated volume GUID links the registry record with the target serial? **Answer:** GUID including braces.

**Q08.** Which drive letter was assigned at mount? **Answer:** letter plus colon.

## Stage 2 — File operations, NTFS-style USN and hashes

**Q09.** What exact source file path was read before the removable copy assertion? **Answer:** Windows path.

**Q10.** Which file-operation event reports the copy assertion to the USB path? **Answer:** `FILE-NNN`.

**Q11.** Which hexadecimal file-reference value is shared by the removable `FILE_CREATE` and later `FILE_DELETE` observations? **Answer:** `0x...`.

**Q12.** What was the status of the change authorization for that device during the incident? Distinguish the unrelated approved device. **Answer:** exact status token.

**Q13.** Recompute SHA-256 of the actual delivered `recovered_export.zip` (not the claimed source file). Which 64-character digest identifies those delivered bytes? **Answer:** lowercase SHA-256.

## Stage 3 — Detection and correlation

**Q14.** Which exact DLP alert event matches the target serial and reported archive name? **Answer:** `DLP-NNN`.

**Q15.** What byte length does `removable_transfer_audit.csv` claim for the exported ZIP, and does the delivered specimen's length agree? Give the value, not a claim that USB content was independently imaged. **Answer:** integer bytes.

**Q16.** Which removable-media transfer event correlates the account, USB destination volume and ZIP object name? **Answer:** `XFER-NNN`.

**Q17.** When was the copied source file later marked with `FILE_DELETE` in the simulated USN excerpt? **Answer:** `YYYY-MM-DDTHH:MM:SSZ`.

**Q18.** The DLP collector's clock offset is **-4 seconds** using `recorded UTC = actual UTC + offset`. Normalize the `DLP-771` timestamp. This is a central estimate with eight seconds uncertainty. **Answer:** `YYYY-MM-DDTHH:MM:SSZ`.

## Incident commander determination — instructor-reviewed, not an exact flag

Reconcile insertion, login, file-read, local copy assertion, USN create/delete, DLP notification, export archive bytes and authorization status. Write an evidence matrix separating **observed in synthetic logs**, **verified within the delivered bytes**, **derived**, and **not established**. Explain why a locally claimed USB copy plus a small benign archive does not authenticate an original disk acquisition, prove harmful content, identify the physical person, or show Internet exfiltration.

Recommend an evidence-preserving response and a NO-GO / CONDITIONAL-GO / GO restoration gate. Provide the exact additional acquisition that would change each unsupported conclusion.

**Answers and instructor walkthrough are withheld from this student package.**
