---
name: gpkg-domain-handoff
description: Compare field domains before handing off a processed GIS layer. Use when a user has a source GeoPackage and an exported GeoPackage and needs to check whether field constraints, choices and labels survived.
---

Collect the two local paths and the registered table name in each. Check the source actually contains a bound field domain. Use Python 3.9+ and run `python scripts/compare.py SOURCE.gpkg SOURCE_TABLE RESULT.gpkg RESULT_TABLE` from this Skill's directory.

Report each source domain field, its status and the concrete difference in bindings or definitions. Highlight missing columns, changed limits, lost labels and missing definitions. Exit 0 means all compared domains match, 1 calls for review, and 2 indicates invalid input. If there are no bound reference domains, ask for the pre-processing GeoPackage. Show the report before recommending a new export. Leave both databases untouched. For a reproducible handoff, follow [the English tutorial](TUTORIAL.md).
