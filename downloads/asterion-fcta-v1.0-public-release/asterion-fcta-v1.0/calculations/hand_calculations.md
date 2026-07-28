# Preliminary Hand Calculations

## Artificial gravity

For a rotating ring:

\[
a = \omega^2 r
\]

With 4.3 rpm and an occupied radius of 12 m:

\[
\omega = 4.3\frac{2\pi}{60} \approx 0.450\ \text{rad/s}
\]

\[
a \approx (0.450)^2(12) \approx 2.43\ \text{m/s}^2 \approx 0.248g
\]

This supports the initial 0.25 g design target.

## Electric-propulsion power baseline

Twelve nominal 12 kW thruster units produce a propulsion electrical demand of:

\[
P_{prop} = 12 \times 12\ \text{kW} = 144\ \text{kW}
\]

A 200–300 kW spacecraft power target leaves margin for avionics, habitation, thermal control, communications, battery charging, conversion losses, and degraded operation.

## Validation placeholders

Add the following during later versions:

- Central-spine beam deflection and stress
- Solar-mast Euler buckling
- Ring hoop force and spoke reaction
- Radiator energy balance
- Cabin flow-rate balance
- Skimmer dynamic-pressure and lift estimates
- Docking kinetic-energy absorption
