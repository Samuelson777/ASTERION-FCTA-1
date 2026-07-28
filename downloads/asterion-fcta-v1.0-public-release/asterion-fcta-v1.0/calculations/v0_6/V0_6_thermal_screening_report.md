# ASTERION V0.6 Thermal Screening Report

## Status and limitation

This report contains independent algebraic screening calculations. It is not an ANSYS result report. The supplied data are intended to define, check and correlate models executed by the user in ANSYS Mechanical.

## Radiator sizing

Six radiator panels are represented, each with a 6 m × 2 m planform. Both faces radiate, giving an effective emitting area of **144.0 m²**. With emissivity 0.88, 120 kW internal waste heat, absorptivity 0.15, and a 10° solar-incidence screening case:

- absorbed solar load: **2.55 kW**;
- nominal equilibrium temperature: **361.38 K (88.23 °C)**;
- five-panel degraded equilibrium temperature: **377.91 K (104.76 °C)**.

The nominal case meets the provisional 370 K target. A one-panel loss remains below the provisional 390 K temporary limit, but coolant routing and local manifold temperatures require detailed modelling.

## Electronics cold plate

A 1.8 kW electronics load, 303 K coolant reference, and total lumped thermal resistance of 0.012 K/W produce a screening hotspot of **324.60 K**. The ANSYS model must replace this lumped resistance with channel convection, contact and spreading resistance.

## Habitat wall coupon

The screening stack is 4 mm aluminium, 50 mm MLI-equivalent continuum and 40 mm polyethylene. Between 295 K cabin temperature and a 230 K effective external boundary, the one-dimensional heat leak is **1.298 W/m²**. MLI is not a normal homogeneous solid; this equivalent conductivity must be correlated with a more appropriate radiation-layer representation.

## Thruster bracket thermal stress

A 180 W conducted heat load and 0.080 K/W path to a 320 K frame sink give a peak temperature of **334.40 K**. A deliberately conservative fully restrained estimate gives **22.85 MPa**, corresponding to a screening yield factor of **12.1** for 6061-T6. Local fillets, bolts, contact resistance and temperature-dependent strength remain unresolved.

## Design actions

1. Preserve two-sided radiator view to space; do not place deployed solar wings in the radiator view factor.
2. Add independent coolant loops so a single panel or pump failure does not remove the whole heat-rejection system.
3. Build cold-plate channel geometry and use a conjugate heat-transfer or correlated convection model.
4. Replace equivalent MLI conductivity with validated blanket performance data before claiming mission performance.
5. Map the thruster thermal field into Static Structural and evaluate bolt preload/contact sensitivity.
