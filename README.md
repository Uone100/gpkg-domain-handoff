# GeoPackage Domain Handoff

Check whether allowable field values, range limits and labels survived a GIS layer export. Compare the source and delivered GeoPackage side by side before handing the result to a field team.

[Download v0.1.0 ZIP](https://github.com/Uone100/gpkg-domain-handoff/releases/download/v0.1.0/gpkg-domain-handoff-0.1.0.zip)

Install in a Codex project with Node.js 22.20 or newer:

```sh
npx skills add Uone100/gpkg-domain-handoff -a codex
```

## English quickstart

**[Follow the step-by-step tutorial](TUTORIAL.md)**

Download the named ZIP under **Assets** on the [release page](https://github.com/Uone100/gpkg-domain-handoff/releases/latest). Extract it and open a terminal in the folder that contains `SKILL.md`.

Python 3.9 or later with the standard sqlite3 module.

```sh
python examples/make_demo.py demo
python scripts/compare.py demo/source.gpkg sites demo/lost.gpkg sites
python scripts/compare.py demo/source.gpkg sites demo/good.gpkg sites
```

The first comparison reports `missing-binding` and exits with 1. The second reports `match` and exits with 0.

## Use as an Agent Skill

Extract the ZIP contents into `.agents/skills/gpkg-domain-handoff/` in a Codex project or `.claude/skills/gpkg-domain-handoff/` in a Claude Code project. Confirm that `SKILL.md` sits directly inside that folder, then start a new session. The tutorial includes an example request and the inputs to supply. You can also use the commands directly.

## Where the request came from

GIS users report losing domain information during processing. This comparison covers GeoPackage-to-GeoPackage handoffs. [QGIS processing request](https://github.com/qgis/QGIS/issues/54606) · [GeoPackage schema extension](https://www.geopackage.org/spec140/#extension_schema)
