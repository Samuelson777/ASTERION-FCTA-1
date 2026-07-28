# Preliminary interface-control document

The authoritative machine-readable interface list is `analysis/ansys/v0_4/model/subsystem_interfaces.csv`.

## Rules

1. All component placement originates from the Version 0.2 master skeleton.
2. The primary structure remains the load-carrying parent for remote-mass and subsystem-interface definitions.
3. Rotating rings require explicit bearing stiffness, rotary fluid/electrical interfaces and emergency-braking load paths before detailed analysis.
4. Solar wings and radiators shall use deployed, feathered and stowed arrangements.
5. Propulsion-pod interfaces must transmit thrust, gimbal torque, handling loads and thermal distortion while remaining replaceable.
6. The Skimmer docking interface must support capture, hard-dock, electrical/fluid transfer and controlled separation states.
7. No bonded contact or rigid remote coupling is accepted without documenting the physical joint it represents.
