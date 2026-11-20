"""Make a small GeoPackage attribute layer and two example handoffs."""
import argparse
from contextlib import closing
from pathlib import Path
import sqlite3
from shutil import copyfile

def build(root):
    root.mkdir()
    source=root/"source.gpkg"
    with closing(sqlite3.connect(source)) as db, db:
        db.executescript("""
        PRAGMA application_id=1196444487;
        PRAGMA user_version=10300;
        CREATE TABLE gpkg_spatial_ref_sys(srs_name TEXT NOT NULL,srs_id INTEGER PRIMARY KEY,
            organization TEXT NOT NULL,organization_coordsys_id INTEGER NOT NULL,definition TEXT NOT NULL,description TEXT);
        INSERT INTO gpkg_spatial_ref_sys VALUES ('Undefined Cartesian',-1,'NONE',-1,'undefined',NULL),
            ('Undefined geographic',0,'NONE',0,'undefined',NULL),
            ('WGS 84',4326,'EPSG',4326,'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433]]',NULL);
        CREATE TABLE gpkg_contents(table_name TEXT PRIMARY KEY,data_type TEXT NOT NULL,identifier TEXT UNIQUE,
            description TEXT DEFAULT '',last_change DATETIME NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
            min_x DOUBLE,min_y DOUBLE,max_x DOUBLE,max_y DOUBLE,srs_id INTEGER REFERENCES gpkg_spatial_ref_sys(srs_id));
        CREATE TABLE sites(fid INTEGER PRIMARY KEY,status TEXT);
        INSERT INTO sites VALUES(1,'A');
        INSERT INTO gpkg_contents(table_name,data_type,identifier) VALUES('sites','attributes','sites');
        CREATE TABLE gpkg_extensions(table_name TEXT,column_name TEXT,extension_name TEXT NOT NULL,
            definition TEXT NOT NULL,scope TEXT NOT NULL,UNIQUE(table_name,column_name,extension_name));
        INSERT INTO gpkg_extensions VALUES ('gpkg_data_columns',NULL,'gpkg_schema','http://www.geopackage.org/spec/#extension_schema','read-write'),
            ('gpkg_data_column_constraints',NULL,'gpkg_schema','http://www.geopackage.org/spec/#extension_schema','read-write');
        CREATE TABLE gpkg_data_columns(table_name TEXT NOT NULL,column_name TEXT NOT NULL,name TEXT,title TEXT,
            description TEXT,mime_type TEXT,constraint_name TEXT,PRIMARY KEY(table_name,column_name),UNIQUE(table_name,name));
        CREATE TABLE gpkg_data_column_constraints(constraint_name TEXT NOT NULL,constraint_type TEXT NOT NULL,
            value TEXT,min NUMERIC,min_is_inclusive BOOLEAN,max NUMERIC,max_is_inclusive BOOLEAN,description TEXT,
            UNIQUE(constraint_name,constraint_type,value));
        INSERT INTO gpkg_data_columns(table_name,column_name,constraint_name) VALUES ('sites','status','site_status');
        INSERT INTO gpkg_data_column_constraints(constraint_name,constraint_type,value,description)
            VALUES ('site_status','enum','A','Active'),('site_status','enum','C','Closed');
        """)
    copyfile(source,root/"good.gpkg")
    copyfile(source,root/"lost.gpkg")
    with closing(sqlite3.connect(root/"lost.gpkg")) as db, db:
        db.execute("DELETE FROM gpkg_data_columns")

if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory",type=Path)
    build(parser.parse_args().directory)
