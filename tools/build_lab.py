#!/usr/bin/env python3
"""Generate safe fictional USB DFIR evidence with defensible provenance limits.

All records, identifiers and file contents are simulated; not a real Windows
registry hive, EVTX, MFT or disk image. Python stdlib only.
"""
from __future__ import annotations
import csv,hashlib,io,random,shutil,sqlite3,zipfile
from pathlib import Path
from datetime import datetime,timedelta,timezone
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"artifacts"
R=random.Random(1472026)
START=datetime(2026,9,17,9,50,tzinfo=timezone.utc)
def z(sec):return (START+timedelta(seconds=sec)).isoformat(timespec="seconds").replace("+00:00","Z")
def write_csv(name,data):
    with (OUT/name).open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,list(data[0]));w.writeheader();w.writerows(data)
def bg(i,host,category):
    return {"utc":z(i*23),"host":host,"event_id":f"{category}-BG-{i:03d}"}
def main():
    if OUT.is_symlink():raise RuntimeError("Refusing symlinked artifacts directory")
    if OUT.exists():shutil.rmtree(OUT)
    OUT.mkdir()
    dev=[]
    for i in range(39):
        d=bg(i,"nb-win-03","USB")
        d.update(serial=f"NBDECOY-{i:04d}",device_id=f"USB\\VID_1209&PID_0001\\NBDECOY-{i:04d}",action=["arrival","departure","enumeration"][i%3],volume=f"{chr(70+i%8)}:",user="unknown",source="simulated-event-export")
        dev.append(d)
    dev.extend([
        {"utc":"2026-09-17T10:13:44Z","host":"nb-win-03","event_id":"USB-702","serial":"NBTRN-77A1","device_id":"USB\\VID_1209&PID_0001\\NBTRN-77A1","action":"arrival","volume":"E:","user":"nb.morgan","source":"simulated-device-installation"},
        {"utc":"2026-09-17T10:14:02Z","host":"nb-win-03","event_id":"USB-703","serial":"NBTRN-77A1","device_id":"USB\\VID_1209&PID_0001\\NBTRN-77A1","action":"volume-mounted","volume":"E:","user":"nb.morgan","source":"simulated-mount-record"},
        {"utc":"2026-09-17T10:20:22Z","host":"nb-win-03","event_id":"USB-704","serial":"NBTRN-77A1","device_id":"USB\\VID_1209&PID_0001\\NBTRN-77A1","action":"departure","volume":"E:","user":"nb.morgan","source":"simulated-event-export"},
    ])
    dev.sort(key=lambda r:r["utc"]);write_csv("usb_device_events.csv",dev)
    registry=[dict(last_seen_utc="2026-09-17T10:14:02Z",host="nb-win-03",device_id="USB\\VID_1209&PID_0001\\NBTRN-77A1",serial="NBTRN-77A1",volume_guid="{NB-FICT-4432}",drive_letter="E:",origin_verified="no",source="simulated-registry-export")]
    registry.extend([dict(last_seen_utc=z(i*63),host="nb-win-03",device_id=f"USB\\VID_1209&PID_0001\\NBDECOY-{i:04d}",serial=f"NBDECOY-{i:04d}",volume_guid=f"{{NB-FICT-{i:04d}}}",drive_letter="F:",origin_verified="no",source="simulated-registry-export") for i in range(12)])
    write_csv("mounted_device_registry.csv",registry)
    users=[dict(utc=z(i*65),host="nb-win-03",event_id=f"LOGON-BG-{i:03d}",user=["backup.svc","nb.researcher","nb.support"][i%3],logon_id=f"0x{i+1800:x}",event="logon",result="success",source_ip=f"192.0.2.{30+i%20}") for i in range(35)]
    users.append(dict(utc="2026-09-17T10:12:57Z",host="nb-win-03",event_id="LOGON-404",user="nb.morgan",logon_id="0x8e13",event="logon",result="success",source_ip="192.0.2.55"))
    users.sort(key=lambda r:r["utc"]);write_csv("user_sessions.csv",users)
    file_events=[]
    for i in range(55):
        d=bg(i,"nb-win-03","FILE")
        d.update(user=["nb.researcher","backup.svc"][i%2],logon_id=f"0x{i+1800:x}",operation=["read","create","close"][i%3],path=f"C:\\Users\\Public\\Reports\\routine_{i:03d}.txt",destination="-",hash_claim="-")
        file_events.append(d)
    file_events.extend([
        dict(utc="2026-09-17T10:15:01Z",host="nb-win-03",event_id="FILE-911",user="nb.morgan",logon_id="0x8e13",operation="read",path="C:\\Research\\Ops\\orbital_budget_fy27.csv",destination="-",hash_claim="-"),
        dict(utc="2026-09-17T10:16:26Z",host="nb-win-03",event_id="FILE-912",user="nb.morgan",logon_id="0x8e13",operation="copy-asserted",path="C:\\Research\\Ops\\orbital_budget_fy27.csv",destination="E:\\Ops\\orbital_budget_fy27.csv",hash_claim="claimed-match"),
        dict(utc="2026-09-17T10:18:45Z",host="nb-win-03",event_id="FILE-913",user="nb.morgan",logon_id="0x8e13",operation="archive-export",path="E:\\Ops\\orbital_budget_fy27.csv",destination="E:\\Ops\\research_export.zip",hash_claim="unverified-local-assertion")
    ])
    file_events.sort(key=lambda r:r["utc"]);write_csv("file_operations.csv",file_events)
    journal=[dict(utc=z(i*45),host="nb-win-03",event_id=f"USN-BG-{i:03d}",file_reference=f"0x{i+1000:08x}",path=f"C:\\Windows\\Temp\\t{i:03d}.tmp",reason=["FILE_CREATE","DATA_EXTEND","CLOSE"][i%3],volume="C:",source="simulated-usn-export") for i in range(65)]
    journal.extend([
        dict(utc="2026-09-17T10:16:27Z",host="nb-win-03",event_id="USN-1001",file_reference="0x000020af",path="E:\\Ops\\orbital_budget_fy27.csv",reason="FILE_CREATE",volume="E:",source="simulated-usn-export"),
        dict(utc="2026-09-17T10:18:46Z",host="nb-win-03",event_id="USN-1002",file_reference="0x000020b0",path="E:\\Ops\\research_export.zip",reason="FILE_CREATE",volume="E:",source="simulated-usn-export"),
        dict(utc="2026-09-17T10:19:55Z",host="nb-win-03",event_id="USN-1003",file_reference="0x000020af",path="E:\\Ops\\orbital_budget_fy27.csv",reason="FILE_DELETE",volume="E:",source="simulated-usn-export")
    ])
    journal.sort(key=lambda r:r["utc"]);write_csv("usn_journal_excerpt.csv",journal)
    # The ZIP is a real readable benign file, not a copy of a real client's data.
    body=b"item,department,value\ntraining-only,fictional-research,2700\n"
    note=b"SIMULATED TRAINING ARCHIVE. No customer information.\n"
    container=io.BytesIO()
    with zipfile.ZipFile(container,"w") as zf:
        for name,data in (("training_records.csv",body),("README.txt",note)):
            zi=zipfile.ZipInfo(name,(2026,9,17,0,0,0));zi.compress_type=zipfile.ZIP_DEFLATED
            zf.writestr(zi,data)
    archive=container.getvalue()
    (OUT/"recovered_export.zip").write_bytes(archive)
    hashes=[
        dict(specimen="recovered_export.zip",record_id="HASH-201",source="actual-training-bytes",sha256=hashlib.sha256(archive).hexdigest(),size_bytes=len(archive),scope="verified-delivered-bytes-not-original-acquisition"),
        dict(specimen="training_records.csv (within archive)",record_id="HASH-202",source="actual-training-bytes",sha256=hashlib.sha256(body).hexdigest(),size_bytes=len(body),scope="derived-from-archive-not-independent")
    ]
    write_csv("specimen_hashes.csv",hashes)
    movement=[dict(utc=z(i*56),host="nb-win-03",event_id=f"XFER-BG-{i:03d}",user=["nb.support","backup.svc"][i%2],src_volume="C:",dst_volume="D:",object_name=f"routine_{i:03d}.bak",status="asserted",bytes_claimed=str(500+i)) for i in range(34)]
    movement.append(dict(utc="2026-09-17T10:18:46Z",host="nb-win-03",event_id="XFER-521",user="nb.morgan",src_volume="C:",dst_volume="E:",object_name="research_export.zip",status="local-copy-asserted",bytes_claimed=str(len(archive))))
    movement.sort(key=lambda r:r["utc"]);write_csv("removable_transfer_audit.csv",movement)
    alerts=[dict(utc=z(i*101),host="nb-dlp-01",event_id=f"DLP-BG-{i:03d}",user="nb.researcher",device_serial=f"NBDECOY-{i:04d}",object_name=f"routine_{i:03d}.txt",action="allow",policy="routine") for i in range(11)]
    alerts.append(dict(utc="2026-09-17T10:19:02Z",host="nb-dlp-01",event_id="DLP-771",user="nb.morgan",device_serial="NBTRN-77A1",object_name="research_export.zip",action="alert",policy="removable-media-review"))
    alerts.sort(key=lambda r:r["utc"]);write_csv("dlp_alerts.csv",alerts)
    approvals=[
        dict(ticket="CHG-217",host="nb-win-03",requester="nb.morgan",device_serial="NBTRN-77A1",status="pending",start_utc="2026-09-17T10:00:00Z",end_utc="2026-09-17T11:00:00Z"),
        dict(ticket="CHG-216",host="nb-win-03",requester="backup.svc",device_serial="NBDECOY-0001",status="approved",start_utc="2026-09-17T09:00:00Z",end_utc="2026-09-17T12:00:00Z"),
    ]
    write_csv("change_authorizations.csv",approvals)
    sensors=[dict(host="nb-win-03",source="usb_device_events.csv",clock_offset_seconds="0",uncertainty_seconds="2"),dict(host="nb-win-03",source="usn_journal_excerpt.csv",clock_offset_seconds="3",uncertainty_seconds="5"),dict(host="nb-dlp-01",source="dlp_alerts.csv",clock_offset_seconds="-4",uncertainty_seconds="8")]
    write_csv("clock_calibration.csv",sensors)
    scope=[dict(artifact=n,collection="fully-synthetic-partial-export",origin_verified="no",real_personal_data="no",limitations=("derived-not-independent" if n=="timeline_cache.sqlite3" else "no-original-image")) for n in [
        "usb_device_events.csv","mounted_device_registry.csv","user_sessions.csv","file_operations.csv","usn_journal_excerpt.csv","specimen_hashes.csv","removable_transfer_audit.csv","dlp_alerts.csv","change_authorizations.csv","clock_calibration.csv","timeline_cache.sqlite3","recovered_export.zip"]]
    write_csv("acquisition_register.csv",scope)
    with sqlite3.connect(OUT/"timeline_cache.sqlite3") as db:
        db.execute("CREATE TABLE observations(event_id TEXT PRIMARY KEY, timestamp_utc TEXT, source_artifact TEXT, host TEXT, actor TEXT, object TEXT, status TEXT)")
        for name,rows,actor,obj,state in [
            ("usb_device_events.csv",dev,"user","device_id","action"),
            ("user_sessions.csv",users,"user","logon_id","result"),
            ("file_operations.csv",file_events,"user","path","operation"),
            ("usn_journal_excerpt.csv",journal,"source","path","reason"),
            ("removable_transfer_audit.csv",movement,"user","object_name","status"),
            ("dlp_alerts.csv",alerts,"user","device_serial","action"),
        ]:
            for row in rows:
                db.execute("INSERT INTO observations VALUES (?,?,?,?,?,?,?)",(row["event_id"],row["utc"],name,row["host"],row[actor],row[obj],row[state]))
        db.commit()
    paths=sorted(x for x in OUT.iterdir() if x.is_file())
    (OUT/"SHA256SUMS.txt").write_text("".join(f"{hashlib.sha256(x.read_bytes()).hexdigest()}  {x.name}\n" for x in paths),encoding="utf-8")
    print(f"PASS: generated {len(paths)} safe synthetic USB forensic artifacts")
if __name__=="__main__":main()
