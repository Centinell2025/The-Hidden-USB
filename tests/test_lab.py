"""Synthetic USB evidence and spoiler-free student ZIP tests."""
import csv,hashlib,sqlite3,subprocess,sys,unittest,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];A=ROOT/"artifacts"
class CaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        subprocess.run([sys.executable,str(ROOT/"tools/build_lab.py")],check=True)
        subprocess.run([sys.executable,str(ROOT/"tools/verify_lab.py")],check=True)
    def test_evidence_sha256(self):
        items=(A/"SHA256SUMS.txt").read_text().splitlines()
        self.assertGreaterEqual(len(items),12)
        for line in items:
            digest,name=line.split("  ",1)
            self.assertEqual(hashlib.sha256((A/name).read_bytes()).hexdigest(),digest)
    def test_unique_usb_installation(self):
        with (A/"usb_device_events.csv").open(newline="") as f:
            q=[x for x in csv.DictReader(f) if x["serial"]=="NBTRN-77A1" and x["action"]=="arrival"]
        self.assertEqual(len(q),1)
    def test_training_archive_no_customer_records(self):
        with zipfile.ZipFile(A/"recovered_export.zip") as z:
            self.assertEqual(set(z.namelist()),{"README.txt","training_records.csv"})
            self.assertIn(b"fictional-research",z.read("training_records.csv"))
    def test_cache_not_an_independent_source(self):
        with (A/"acquisition_register.csv").open(newline="") as f:
            self.assertTrue(all(x["origin_verified"]=="no" for x in csv.DictReader(f)))
        with sqlite3.connect(f"file:{(A/'timeline_cache.sqlite3').as_posix()}?mode=ro",uri=True) as db:
            self.assertEqual(db.execute("PRAGMA quick_check").fetchone()[0],"ok")
    def test_18_questions(self):
        q=(ROOT/"questions/INVESTIGATION.md").read_text()
        for i in range(1,19):self.assertIn(f"**Q{i:02d}.**",q)
    def test_student_package(self):
        subprocess.run([sys.executable,str(ROOT/"tools/build_student_zip.py")],check=True)
        with zipfile.ZipFile(ROOT/"dist/The-Hidden-USB-STUDENT.zip") as z:
            self.assertIsNone(z.testzip())
            self.assertIn("questions/INVESTIGATION.md",z.namelist())
            self.assertIn("artifacts/recovered_export.zip",z.namelist())
            self.assertFalse(any(n.startswith(("tools/","tests/")) or "walkthrough" in n.lower() for n in z.namelist()))
if __name__=="__main__":unittest.main()
