# ASTERION FCTA-1 — Version 0.8 Optimisation Report

## Executive result

The selected H3 configuration increases idealised tube-structure mass from 7742.3 kg to 10423.4 kg, an increase of 2681.4 kg. In exchange, the independent frame model predicts:

- propulsion displacement reduction from 13.788 mm to 0.215 mm;
- misaligned-docking displacement reduction from 52.823 mm to 22.870 mm;
- first supported mode increase from 0.1308 Hz to 0.1964 Hz;
- balanced ring-braking displacement of 1.846 mm; and
- single-ring fault-braking displacement of 3.487 mm.

## Why H3 was selected

H3 is the lowest-mass tested candidate that meets the 25 mm docking criterion with useful margin while also satisfying the propulsion, braking, modal and mass targets. H4 improves docking displacement to about 20.2 mm but adds approximately 623 kg. H8 doubles ring-brace count, but docking response remains almost unchanged because docking flexibility is governed mainly by global spine depth.

## Physical interpretation

The propulsion improvement is large because the new longitudinal struts carry thrust axially instead of forcing the original in-plane booms to resist axial spacecraft load through bending. The docking improvement is governed by the 1.8 m spine radius, which increases global bending stiffness. Ring braking improves through triangulated torque paths and through the corrected counter-rotating load definition.

## Caution

The screening model may overpredict stiffness because all beam joints are ideal. The next authoritative ANSYS runs must include joint compliance, local shell models and sensitivity cases.
