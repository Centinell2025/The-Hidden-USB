#!/usr/bin/env python3
"""Forensic QA of synthetic USB case; no claim of real Windows acquisition."""
from __future__ import annotations
import csv,hashlib,sqlite3,sys,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];A=ROOT/"artifacts"
def req(ok,msg):
    if not ok:raise ValueError(msg)
def rows(name):
    with (A/name).open(newline="",encoding="utf-8") as f:return list(csv.DictReader(f))
def verify():
    items=(A/"SHA256SUMS.txt").read_text().splitlines();m={}
    for item in items:
        sha,sep,name=item.partition("  ")
        req(sep and len(sha)==64 and name and "/" not in name and ".." not in name,"invalid manifest item")
        req(name not in m,"duplicate artifact")
        m[name]=sha
    req(set(m)=={p.name for p in A.iterdir() if p.is_file()}-{"SHA256SUMS.txt"},"missing/extra artifact")
    for name,sha in m.items():
        req(hashlib.sha256((A/name).read_bytes()).hexdigest()==sha,f"changed evidence: {name}")
    dev=rows("usb_device_events.csv")
    reg=rows("mounted_device_registry.csv")
    users=rows("user_sessions.csv")
    file=rows("file_operations.csv")
    journal=rows("usn_journal_excerpt.csv")
    copies=rows("removable_transfer_audit.csv")
    alerts=rows("dlp_alerts.csv")
    tickets=rows("change_authorizations.csv")
    scope=rows("acquisition_register.csv")
    hashes=rows("specimen_hashes.csv")
    target=[x for x in dev if x["serial"]=="NBTRN-77A1" and x["action"]=="arrival"]
    req(len(target)==1 and target[0]["host"]=="nb-win-03" and target[0]["volume"]=="E:","USB arrival ambiguity")
    req(any(x["serial"]==target[0]["serial"] and x["drive_letter"]==target[0]["volume"] for x in reg),"registry/device join broken")
    req(len([x for x in users if x["user"]=="nb.morgan" and x["logon_id"]=="0x8e13"])==1,"user session ambiguity")
    target_file=[x for x in file if x["operation"]=="copy-asserted" and x["user"]=="nb.morgan"]
    req(len(target_file)==1 and target_file[0]["logon_id"]=="0x8e13" and target_file[0]["destination"].startswith("E:"),"file copy mismatch")
    req(any(x["path"]==target_file[0]["destination"] and x["reason"]=="FILE_CREATE" for x in journal),"USN copy corroboration failed")
    req(any(x["path"]==target_file[0]["destination"] and x["reason"]=="FILE_DELETE" for x in journal),"controlled deletion observation missing")
    req(any(x["ticket"]=="CHG-217" and x["status"]=="pending" and x["device_serial"]==target[0]["serial"] for x in tickets),"change permission ambiguity")
    req(any(x["event_id"]=="DLP-771" and x["device_serial"]==target[0]["serial"] for x in alerts),"DLP join broken")
    archive=(A/"recovered_export.zip").read_bytes()
    req(any(x["specimen"]=="recovered_export.zip" and x["sha256"]==hashlib.sha256(archive).hexdigest() and int(x["size_bytes"])==len(archive) for x in hashes),"archive integrity claim mismatch")
    with zipfile.ZipFile(A/"recovered_export.zip") as z:
        req(z.testzip() is None,"damaged recovered training ZIP")
        req(set(z.namelist())=={"training_records.csv","README.txt"},"unexpected ZIP member")
        data=z.read("training_records.csv")
    req(any(x["specimen"].startswith("training_records.csv") and x["sha256"]==hashlib.sha256(data).hexdigest() for x in hashes),"extracted member hash mismatch")
    req(any(x["event_id"]=="XFER-521" and x["bytes_claimed"]==str(len(archive)) for x in copies),"local transfer assertion inconsistent")
    req(len(scope)>=11 and all(x["origin_verified"]=="no" and x["real_personal_data"]=="no" for x in scope),"invalid independent-origin/PII claim")
    with sqlite3.connect(f"file:{(A/'timeline_cache.sqlite3').resolve().as_posix()}?mode=ro",uri=True) as db:
        req(db.execute("PRAGMA quick_check").fetchone()[0]=="ok","SQLite cache invalid")
        count=db.execute("SELECT count(*) FROM observations").fetchone()[0]
        req(count>225 and db.execute("SELECT count(*) FROM observations WHERE event_id='FILE-912'").fetchone()[0]==1,"derived cache lacks source trace")
    return dict(evidence_files=len(m),sql_events=count,reported_usb=target[0]["serial"],source_authenticity="unverified")
if __name__=="__main__":
    try:print("PASS Hidden USB synthetic DFIR:",verify())
    except (ValueError,OSError,KeyError,IndexError,sqlite3.Error,zipfile.BadZipFile) as e:
        print("FAIL:",e,file=sys.stderr);sys.exit(1)
