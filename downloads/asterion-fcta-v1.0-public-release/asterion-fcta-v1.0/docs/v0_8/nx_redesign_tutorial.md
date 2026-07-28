# Siemens NX Version 0.8 Redesign Tutorial

## 1. Create the new arrangement

Duplicate the Version 0.4 assembly arrangement and name it `V0_8_OPTIMISED_STRUCTURE`.

## 2. Update the master skeleton

Set `spine_radius = 1800 mm`. Retain all X station coordinates and regenerate the eight octagonal spine rails through associative points. Verify that ring, tank, module and docking interfaces remain controlled by the master coordinate systems rather than by edge references.

## 3. Update frame members

- Longerons: 160 mm OD × 6 mm wall.
- Octagonal frames: 130 mm OD × 5 mm wall.
- Bay diagonals: 100 mm OD × 4 mm wall.

Create Part Family members for each tube family and replace the Version 0.3 frame components through assembly constraints.

## 4. Add ring torque braces

At each of the 24 outer ring nodes, create two diagonal braces to the nearest inner support nodes on opposite angular sides. Use 90 mm OD × 4 mm wall tubes. Pattern the seed braces by 30 degrees and mirror them to the second ring.

## 5. Add docking load spreaders

Create eight 100 mm OD × 4 mm wall struts between the docking ring and the corresponding octagonal nodes at X = 14,000 mm. Confirm that the struts form a continuous axial load path and do not intersect pressure modules or the Skimmer separation envelope.

## 6. Add propulsion longitudinal struts

For each of the six propulsion mounts, add one strut to X = −18,500 mm and one to X = −13,500 mm. Use 120 mm OD × 5 mm wall tubes. Check plume, radiator and maintenance clearances.

## 7. Validate the assembly

- update all WAVE links;
- run Examine Geometry;
- run static interference and clearance checks;
- update mass properties;
- verify the vehicle CG against `calculations/v0_8/updated_cg_loading_cases.csv`;
- export Parasolid or STEP for local shell submodels;
- export the line topology for ANSYS verification.

## 8. Drawing changes

Update the general arrangement, primary-structure assembly drawing, docking-interface drawing and ring-support drawing. Add revision clouds and identify Version 0.8 members with the `OPT` suffix.
