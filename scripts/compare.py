"""Compare bound field domains between two registered GeoPackage layers."""
import argparse
from contextlib import closing
import json
from pathlib import Path
import sqlite3

def definition_valid(rows):
    if not rows or len({r[0] for r in rows})!=1:
        return False
    kind=rows[0][0]
    if kind=="range" and len(rows)==1:
        _,value,lo,li,hi,ui,_=rows[0]
        return (value is None and isinstance(lo,(int,float)) and isinstance(hi,(int,float))
                and lo<hi and li in (0,1) and ui in (0,1))
    if kind not in ("enum","glob") or (kind=="glob" and len(rows)!=1):
        return False
    return all(isinstance(r[1],str) and r[2:6]==(None,)*4 for r in rows)

def read_layer(path, layer):
    with closing(sqlite3.connect(path.resolve().as_uri()+"?mode=ro",uri=True)) as db:
        db.execute("PRAGMA trusted_schema=OFF")
        db.execute("BEGIN")
        if db.execute("PRAGMA application_id").fetchone()[0]!=0x47504B47:
            raise ValueError("Expected a GeoPackage with a GPKG application ID")
        if not db.execute("SELECT 1 FROM gpkg_contents WHERE table_name=?",(layer,)).fetchone():
            raise ValueError("Layer is not registered: "+layer)
        fields={name for (name,) in db.execute("SELECT name FROM pragma_table_info(?)",(layer,))}
        if not fields:
            raise ValueError("Registered table has no readable fields: "+layer)
        tables={r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        domains={}
        if "gpkg_data_columns" not in tables:
            return fields,domains
        bindings=db.execute("SELECT column_name,constraint_name FROM gpkg_data_columns "
                            "WHERE table_name=? AND constraint_name IS NOT NULL ORDER BY column_name",(layer,))
        for name,domain in bindings:
            if name not in fields:
                raise ValueError("Domain binding references an absent field: "+name)
            rows=[]
            if "gpkg_data_column_constraints" in tables:
                rows=db.execute("SELECT constraint_type,value,min,min_is_inclusive,max,max_is_inclusive,description "
                                "FROM gpkg_data_column_constraints WHERE constraint_name=? "
                                "ORDER BY constraint_type,value,description",(domain,)).fetchall()
            domains[name]={"name":domain,"definition":rows}
    return fields,domains

def compare(source,source_layer,result,result_layer):
    _,reference=read_layer(source,source_layer)
    fields,target=read_layer(result,result_layer)
    report=[]
    for field,original in reference.items():
        actual=target.get(field)
        if not definition_valid(original["definition"]):
            status="incomplete-source"
        elif field not in fields:
            status="missing-field"
        elif actual is None:
            status="missing-binding"
        elif not definition_valid(actual["definition"]):
            status="incomplete-result"
        elif [r[:-1] for r in original["definition"]]!=[r[:-1] for r in actual["definition"]]:
            status="changed-definition"
        elif original["definition"]!=actual["definition"]:
            status="changed-label"
        elif original["name"]!=actual["name"]:
            status="renamed-domain"
        else:
            status="match"
        report.append(dict(field=field,status=status,source=original,result=actual))
    outcome="match" if report and all(r["status"]=="match" for r in report) else "review"
    return {"result":outcome,"fields":report,"reference_has_domains":bool(report)}

if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("source",type=Path)
    p.add_argument("source_layer")
    p.add_argument("result",type=Path)
    p.add_argument("result_layer")
    a=p.parse_args()
    try:
        report=compare(a.source,a.source_layer,a.result,a.result_layer)
    except (OSError,ValueError,sqlite3.Error) as exc:
        p.exit(2,f"{exc}\n")
    print(json.dumps(report,indent=2))
    raise SystemExit(0 if report["result"]=="match" else 1)
