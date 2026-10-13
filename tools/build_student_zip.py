#!/usr/bin/env python3
"""Build a spoiler-free deterministic student ZIP from verified local artifacts."""
import sys,zipfile
from pathlib import Path
from verify_lab import verify
ROOT=Path(__file__).resolve().parents[1];A=ROOT/"artifacts"
OUT=ROOT/"dist"/"The-Hidden-USB-STUDENT.zip"
PAGES=["README.txt","PLAYER-INSTRUCTIONS.md","docs/FORENSIC_SCOPE.md","questions/INVESTIGATION.md"]
def build():
    verify()
    entries={n:(ROOT/n).read_bytes() for n in PAGES}
    entries.update({f"artifacts/{p.name}":p.read_bytes() for p in A.iterdir() if p.is_file()})
    OUT.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(OUT,"w") as z:
        for name in sorted(entries):
            info=zipfile.ZipInfo(name,(2026,9,17,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=0o644<<16
            z.writestr(info,entries[name])
    with zipfile.ZipFile(OUT) as z:
        assert z.testzip() is None
        assert all(z.read(n)==v for n,v in entries.items())
        assert not any(n.startswith(("tools/","tests/")) or "instructor" in n.lower() for n in z.namelist())
    print("PASS Hidden USB student archive:",OUT,len(entries),"verified members")
if __name__=="__main__":
    try:build()
    except (OSError,ValueError,AssertionError,zipfile.BadZipFile) as e:
        print("FAIL:",e,file=sys.stderr);sys.exit(1)
