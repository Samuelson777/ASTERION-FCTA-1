# Primary Load-Path Definition

## Docking load

A preliminary 25 kN axial compression is introduced at the forward docking frame and transferred through eight docking links into the longerons, frames and diagonals. The demonstration support is placed at the aft end for a ground-test-style static case. A flight free-body treatment must use inertial relief or balanced loads rather than an artificial fixed support.

## Propulsion and manoeuvre load

Six propulsion mounts transfer thrust and gimbal reactions into the frame at X = -16 m. The current line model includes mount booms but does not yet model gimbal stiffness, pod mass or thrust-vector eccentricity.

## Rotating-ring load

Each ring uses a 12,000 kg conceptual rotating mass. At 4.3 rpm and 12 m radius, the distributed radial force is 29,198.2 N per ring. It is divided across 12 outer nodes for the first global case. Sector-by-sector mass, bearing compliance and imbalance must be added later.

## Emergency braking

Stopping one ring in 120 seconds requires an idealised torque of approximately 6,484.2 N·m. Counter-rotating rings cancel nominal angular momentum only when their inertias and rates match; transient mismatch still loads the spine and attitude-control system.

## Local submodels required

- Ring spoke-to-hub fittings
- Bearing support and race
- Docking-link lugs
- Propulsion boom joints
- Longeron/frame node fittings
- Solar and radiator deployment hinges

Global beam stresses must not be used to approve these local features.
