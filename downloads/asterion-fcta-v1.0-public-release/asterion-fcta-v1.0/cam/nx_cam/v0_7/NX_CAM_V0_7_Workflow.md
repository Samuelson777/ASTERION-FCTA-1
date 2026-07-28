# Siemens NX CAM Version 0.7 workflow

## Purpose

This workflow demonstrates manufacturing planning and NX CAM competence using four representative ASTERION components. It does not claim that the full spacecraft can be manufactured on a home machine.

## Recommended NX structure

1. Create one manufacturing part file per demonstrator.
2. Add the design part as a reference component.
3. Create stock, MCS, clearance planes and fixtures.
4. Load only reviewed tools from `tool_library.csv`.
5. Build operations from `operation_plan.csv`.
6. Use IPW between setups and preserve stock allowance for finish operations.
7. Run full machine-tool simulation when a valid kinematic model and post are available.
8. Record collisions, warnings, cycle time and remaining stock.
9. Export setup sheets, tool lists, operation navigator screenshots and verified posted code.

## NX competencies demonstrated

- Manufacturing setup and geometry groups
- Workpiece/IPW management
- Planar milling and adaptive roughing
- Hole making and precision reaming
- Turning, boring and grooving
- Rest machining
- Thin-wall and profile finishing
- Tool-holder collision checking
- Fixture-aware simulation
- Post Builder/postprocessor governance
- Shop documentation and inspection planning

## Required portfolio screenshots

Capture the Operation Navigator, toolpath, material-removal verification, collision report, IPW comparison and final setup sheet for every demonstrator.
