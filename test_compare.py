from contextlib import closing
from pathlib import Path
import sqlite3
import tempfile
import unittest
from examples.make_demo import build
from scripts.compare import compare,definition_valid

class Handoff(unittest.TestCase):
    def test_domains(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)/"demo"
            build(root)
            src,good,lost=(root/(n+".gpkg") for n in ("source","good","lost"))
            before=src.read_bytes()
            self.assertEqual(compare(src,"sites",good,"sites")["result"],"match")
            self.assertEqual(compare(src,"sites",lost,"sites")["fields"][0]["status"],"missing-binding")
            self.assertEqual(compare(lost,"sites",src,"sites")["result"],"review")
            for sql,status in [
                ("UPDATE gpkg_data_column_constraints SET description='new'","changed-label"),
                ("DELETE FROM gpkg_data_column_constraints WHERE value='C'","changed-definition"),
                ("DELETE FROM gpkg_data_column_constraints","incomplete-result")]:
                with closing(sqlite3.connect(good)) as db,db:
                    db.execute(sql)
                self.assertEqual(compare(src,"sites",good,"sites")["fields"][0]["status"],status)
            self.assertEqual(src.read_bytes(),before)
            with self.assertRaises(ValueError):
                compare(src,"absent",good,"sites")

    def test_range_and_glob(self):
        self.assertTrue(definition_valid([("range",None,0,1,10,0,None)]))
        self.assertFalse(definition_valid([("range",None,10,1,0,1,None)]))
        self.assertTrue(definition_valid([("glob","A*",None,None,None,None,None)]))
