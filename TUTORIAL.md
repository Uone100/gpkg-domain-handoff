# Check a field team's GeoPackage before delivery

The sample source records site status as a code. Its field domain explains that A means Active and C means Closed. A processing result can retain the code A in every row while losing the binding that tells the recipient how to interpret it.

## Set up

Download the named ZIP under **Assets** on the [release page](https://github.com/Uone100/gpkg-domain-handoff/releases/latest). Extract it and open a terminal in the folder that contains `SKILL.md`.

Python 3.9 or later with the standard sqlite3 module.

## Compare the two example deliveries

Run the quickstart commands below separately.

```sh
python examples/make_demo.py demo
python scripts/compare.py demo/source.gpkg sites demo/lost.gpkg sites
python scripts/compare.py demo/source.gpkg sites demo/good.gpkg sites
```

 The first creates three files in a fresh directory. The second intentionally returns exit code 1. In its output, find field `status` with `missing-binding`: the source lists the two choices, and the delivered layer lacks that binding. The third command checks the intact export and reports `match`.

## Check a project handoff

Replace the four arguments to `scripts/compare.py`, in order, with the original GeoPackage, original registered table name, delivered GeoPackage and delivered table name. Use the actual table identifiers, which may differ from display aliases. Matching uses the original field names. The tool opens both databases read-only.

| Result | What to check |
| --- | --- |
| missing-field or missing-binding | Check the export field mapping and how the processing tool transfers domains. |
| changed-definition or changed-label | Compare the two definition arrays. Each row lists kind, value, minimum, minimum inclusive, maximum, maximum inclusive, and description. |
| renamed-domain | Verify the renamed domain is intentional before acceptance. |
| incomplete-source or incomplete-result | Recheck the metadata in the indicated package. |
| reference_has_domains is false | Obtain the original package with a bound reference domain. An empty baseline needs review. |

A missing file, unknown layer name or incompatible schema returns code 2. The comparison covers enum, range and glob constraints stored in the GeoPackage schema extension. A QGIS project-only widget, an Esri geodatabase or an intentionally renamed field needs a separate mapping or export. It checks definitions and bindings, not every feature's data values.

## Ask an agent

“Compare the field domains in the original sites layer and the clipped delivery. List the choices or labels that disappeared.” Provide both package paths and layer names.
