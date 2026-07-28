# Naming and Numbering Conventions

## Part numbering

`AST-[assembly]-[part]-[revision]`

Examples:

- `AST-100-001-A` — central-spine forward longeron
- `AST-200-014-A` — habitation-ring spoke
- `AST-500-006-A` — thruster-gimbal bracket
- `AST-700-021-A` — Skimmer elevon rib

## Assembly numbering

- ASA-100 Central Spine
- ASA-200 Port Ring
- ASA-300 Starboard Ring
- ASA-400 Power and Thermal
- ASA-500 Propulsion
- ASA-600 Command and Service
- ASA-700 Skimmer
- ASA-800 Mission Modules

## NX naming rules

- Datums: `DATUM_[FUNCTION]_[INDEX]`
- Coordinate systems: `CSYS_[ASSEMBLY]_[INTERFACE]`
- Expressions: lower-case snake case
- Sketches: `SK_[FUNCTION]_[INDEX]`
- Bodies: `BODY_[FUNCTION]`
- WAVE links: `WAVE_[SOURCE]_[FEATURE]`

## ANSYS naming rules

Named selections should use:

- `NS_FIX_*`
- `NS_LOAD_*`
- `NS_CONTACT_*`
- `NS_RESULT_*`
- `NS_SYM_*`
