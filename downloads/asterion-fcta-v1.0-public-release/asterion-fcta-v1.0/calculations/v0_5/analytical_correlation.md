# V0.5 Analytical and Numerical Correlation Plan

## 1. Axial spine correlation

For a symmetric axial docking load, distribute the total force over eight longerons. Compare the hand value

`delta = P L / (8 E A)`

with the mean X displacement of the forward frame in the beam model. Because diagonals and transverse frames share load, exact agreement is not expected; a 10% target applies only after matching model assumptions.

## 2. Individual member buckling

For every compressive beam member calculate

`Pcr = pi^2 E I / (K L)^2`.

The Python screening uses K = 1.0. ANSYS eigenvalue buckling captures global interaction but remains an ideal linear bifurcation result. Use both, then investigate critical physical members with nonlinear imperfections.

## 3. Rotating ring

At radius 12 m and 4.3 rpm, acceleration is 2.433 m/s². A 12,000 kg ring therefore requires 29.2 kN total radial support force. Compare summed ANSYS reactions at the inner ring interface with this value and verify equilibrium to within 1%.

## 4. Braking torque

For a 120-second stop, each ring braking torque is 6.484 kN·m. Check that the vector sum of nodal tangential forces produces this torque about the vehicle X axis and negligible net translation.

## 5. Modal correlation

The included Python frequencies are only a trend check because remote inertias and beam mass are simplified. Compare mode families, not only mode numbers. Use Modal Assurance Criterion after mapping common structural nodes.
