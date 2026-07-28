# Siemens NX Primary-Structure Build Tutorial

## 1. Create the controlled parts

Create these native files on the NX workstation:

- `AST-1000-PRIMARY-STRUCTURE-ASM.prt`
- `AST-1100-SPINE-TRUSS.prt`
- `AST-1200-RING-SUPPORT-A.prt`
- `AST-1210-RING-SUPPORT-B.prt`
- `AST-1300-PROPULSION-FRAME.prt`
- `AST-1400-FORWARD-DOCK-FRAME.prt`

Keep `AST-0001-MASTER-SKELETON.prt` from Version 0.2 as the top-level geometry authority.

## 2. Import expressions

Create the expressions listed in `nx_expressions_v0_3.txt`. Preserve meaningful names and units. Do not dimension structural features with anonymous sketch dimensions when a controlled expression exists.

## 3. Spine truss

1. WAVE-link the vehicle centreline, truss-radius circle and station planes.
2. At the aft station create eight points on the truss-radius circle.
3. Use associative curves parallel to +X for the longeron axes.
4. Trim or divide them at each station plane.
5. Create transverse octagonal frames at all structural stations.
6. Add alternating diagonal curves between adjacent stations.
7. Use `Tube` for presentation solids, or retain centreline curves for idealisation.
8. Put centreline, simplified tube and interface geometry in separate reference sets.

## 4. Ring supports

1. WAVE-link the ring centre plane and 12 m centroid circle.
2. Pattern 12 outer nodes at 30-degree intervals.
3. Create 12 circumference segments and 12 radial spokes.
4. Connect the hub ring to the nearest central-truss nodes.
5. Keep bearing race, drive hardware and pressure-shell interfaces as separate future components.

## 5. Propulsion frame

Create six mount coordinate systems at 60-degree intervals and 3.2 m radius on X = -16 m. Build paired booms from nearby truss nodes to each mount. Publish each mount CSYS for propulsion-pod WAVE linking.

## 6. Docking frame

Create an eight-node, 800 mm radius frame 400 mm forward of the main truss end. Link each docking node to one longeron endpoint. Publish the docking axis, mating plane and keep-out cylinder.

## 7. Validation in NX

- Run Examine Geometry and Assembly Clearance.
- Check all tube centreline intersections.
- Confirm no zero-length or duplicate members.
- Measure mass using assigned preliminary material.
- Verify the ring and docking coordinate systems.
- Export Parasolid or STEP from the locally built native structure for ANSYS if permitted by the installed licence.
