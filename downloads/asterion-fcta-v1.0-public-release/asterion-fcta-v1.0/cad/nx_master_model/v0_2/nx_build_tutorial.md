# Siemens NX Build Tutorial — ASTERION Master Skeleton V0.2

## 1. Create the native part

Create a new millimetre part named `AST-0001-MASTER-SKELETON.prt`. Set the absolute coordinate system so +X is forward, +Y is starboard and +Z is up. Save the part before constructing geometry.

## 2. Add global expressions

Open the Expressions tool and create the variables from `nx_expressions_v0_2.txt`. Depending on the NX release, use expression import or paste the entries manually. Confirm that all length expressions use millimetres, all angles use degrees, and the rotation speed uses rpm.

Do not replace formulas such as `ring_major_radius = ring_outer_radius - ring_minor_radius` with fixed numbers.

## 3. Create stable station datums

Create eight datum planes normal to the X-axis at STA_00 through STA_70. Name them exactly `DP_STA_00` through `DP_STA_70`. Drive each offset with its matching station expression.

Create the vehicle centreline and name it `AXIS_VEHICLE_X`.

## 4. Construct the spine envelope

Create a revolved or extruded cylindrical envelope with radius `spine_outer_radius` between STA_00 and STA_70. Create a second reference cylinder at `spine_truss_radius`. Keep both as construction or envelope objects rather than production solids.

## 5. Construct the ring envelopes

At `DP_STA_30` and `DP_STA_40`, sketch concentric circles using `ring_outer_radius` and `ring_major_radius - ring_minor_radius`. Extrude or sweep the envelope symmetrically to `ring_axial_width`.

Create 12 radial sector lines at `ring_sector_angle`. The sector geometry is the publication authority for repeated ring modules.

## 6. Construct solar-wing envelopes

At STA_50, create four radial hinge axes. The total tip-to-tip span is controlled by `solar_deployed_span`. Each wing consists of:

- a boom of length `solar_boom_length`, and
- an active panel region of length `solar_active_panel_length`.

Create stowed and deployed arrangements. Add a swept keep-out body through the deployment angle.

## 7. Construct radiator envelopes

Create six radiator hinge coordinate systems equally spaced around the X-axis. Build one panel envelope and pattern it six times. Keep the panel length aligned primarily with X and use `radiator_radial_offset` for clearance from the rings and spine.

## 8. Construct propulsion interfaces

At STA_10, create six coordinate systems at `propulsion_pod_radial_offset`. Pattern them at 60°. Create pod interface circles and axis lines. Add six plume keep-out cones beginning at the aft exit plane; the cones are clearance objects only.

## 9. Construct the Skimmer interface

At STA_70, create the docking plane and a `primary_docking_diameter` interface circle. Build the Skimmer as a reference envelope extending forward. The neutral model is only a placeholder: the detailed Skimmer must later be rebuilt with Studio Surface, Through Curves and curvature-continuity checks.

## 10. Publish geometry for WAVE linking

Create or organise named objects matching `wave_publication_map.csv`. Only approved centreline, datums, envelopes, interfaces and keep-outs may be linked into downstream parts.

## 11. Create arrangements

Create at least:

- `ARR_STOWED`
- `ARR_SOLAR_DEPLOYED`
- `ARR_RADIATORS_DEPLOYED`
- `ARR_ALL_DEPLOYED`
- `ARR_SKIMMER_SEPARATED`

## 12. Audit before release

Run the checklist in `nx_model_audit_checklist.md`. Export a Parasolid or STEP reference if your NX licence permits, plus JT or glTF for review. Record the NX release used and the exact export settings.
