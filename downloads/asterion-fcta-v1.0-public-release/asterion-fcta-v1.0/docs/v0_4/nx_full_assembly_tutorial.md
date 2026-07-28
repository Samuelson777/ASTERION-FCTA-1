# Siemens NX full-assembly tutorial — Version 0.4

## 1. Create the controlled assembly

Create `AST-0000-ASTERION-FCTA-1-ASSY.prt`, add the Version 0.2 master skeleton as the first component, and fix only the skeleton at the absolute coordinate system. Add the Version 0.3 primary structure using WAVE-linked station and interface geometry.

## 2. Build reusable component families

Create one habitation-sector master part, one propulsion-pod master, one radiator master and one solar-panel segment master. Drive variants through inter-part expressions and part families rather than copying independent solids.

## 3. Place the rings

Publish ring-axis coordinate systems at X = -2500 mm and +2500 mm. Pattern each sector 12 times about +X. Maintain a separate rotating subassembly for each ring; do not constrain individual sectors directly to the non-rotating vehicle assembly.

## 4. Add axial modules and tanks

Constrain command, service, refuge, logistics and docking modules to their station planes. Place four tanks through a circular component pattern and retain explicit service clearances and removal paths.

## 5. Add deployable systems

Create NX arrangements for cruise-deployed, docking-safe, Skimmer-separated, maintenance and launch-package states. Use component positioning or motion simulation joints for solar, radiator and robotic-arm movement.

## 6. Integrate propulsion and Skimmer

Place six pods at the propulsion interface coordinate systems. Add plume keep-out cones from the master skeleton. Constrain the Skimmer to the forward docking coordinate system and provide a separate arrangement with the Skimmer suppressed.

## 7. Validate

Run assembly clearance, hard-interference, mass properties, centre-of-gravity, component naming, reference-set and broken-WAVE-link checks. Compare NX mass properties with the supplied CSV budget and explain all differences.
