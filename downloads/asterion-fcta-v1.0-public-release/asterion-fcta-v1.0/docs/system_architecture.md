# System Architecture

## Major assemblies

1. **ASA-100 Central Spine Assembly**
   - Primary truss
   - Docking nodes
   - Service tunnel
   - Propulsion load path
   - Power and fluid distribution interfaces

2. **ASA-200 Port Habitation Ring**
   - Twelve ring sectors
   - Spokes
   - Bearing interface
   - Internal habitation modules
   - Emergency refuge zone

3. **ASA-300 Starboard Habitation Ring**
   - Counter-rotating companion ring
   - Mirrored mechanical interfaces
   - Independent drive and braking system

4. **ASA-400 Power and Thermal Assembly**
   - Four deployable solar wings
   - Six deployable radiator panels
   - Power-conditioning modules
   - Thermal manifolds

5. **ASA-500 Propulsion Assembly**
   - Six detachable pods
   - Two electric thrusters per pod
   - Gimbals
   - Propellant tanks
   - Local thermal shielding

6. **ASA-600 Command, Navigation, and Service Assembly**
   - Flight-control volume
   - Sensors
   - Communication booms
   - Robotic servicing interface

7. **ASA-700 Skimmer Aeroshuttle**
   - Blended lifting body
   - Elevons
   - Split rudders
   - Landing gear
   - Docking and payload interface

8. **ASA-800 Mission Module Zone**
   - Science module
   - Cargo module
   - Tanker module
   - Deep-space sensor module

## Interface philosophy

All major assemblies should reference the NX master skeleton rather than directly referencing each other wherever possible. Interface control should use named datum coordinate systems, interface planes, bolt circles, clearance envelopes, and connection tables.

## Baseline coordinate system

- +X: forward along the central spine.
- +Y: starboard.
- +Z: vehicle zenith in the reference assembly orientation.
- Origin: geometric centre between the two habitation-ring bearing planes.

## Preliminary station locations

| Station | X position | Function |
|---|---:|---|
| STA-00 | -21.0 m | Aft propulsion envelope |
| STA-10 | -16.0 m | Propulsion interface frame |
| STA-20 | -8.0 m | Aft service and radiator interface |
| STA-30 | -2.5 m | Aft habitation-ring bearing |
| STA-40 | +2.5 m | Forward habitation-ring bearing |
| STA-50 | +9.0 m | Command/service module |
| STA-60 | +15.0 m | Mission-module zone |
| STA-70 | +21.0 m | Forward docking and Skimmer interface |
