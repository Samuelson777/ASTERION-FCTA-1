# Risk Register — Initial

| ID | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| R-001 | Project grows beyond home-PC capability. | High | High | Use subsystem models, beams, shells, symmetry, and staged refinement. |
| R-002 | NX associative links become unstable. | Medium | High | Reference the master skeleton, use naming rules, and avoid circular WAVE links. |
| R-003 | Vehicle appears scientifically misleading. | Medium | High | Label speculative elements, retain conservation laws, and separate concept from validated performance. |
| R-004 | CFD cell count exceeds available limits. | High | Medium | Use half-model symmetry, local refinement, reduced domains, and 2D preliminary studies. |
| R-005 | Detailed assembly becomes too slow. | High | Medium | Use arrangements, lightweight representations, simplified parts, and envelope components. |
| R-006 | CAM output is mistaken for production-ready code. | Medium | High | Mark G-code educational, name the assumed machine, and require machine-specific verification. |
| R-007 | Thermal model lacks realistic boundary conditions. | Medium | High | Publish assumptions and perform sensitivity studies. |
| R-008 | Artificial-gravity ring introduces dynamic coupling not captured by simple models. | Medium | High | Begin with static rotating-load analysis, then add reduced transient studies. |
| R-009 | Public release includes restricted or proprietary data. | Low | High | Release original work and neutral exports only; review licences before publication. |
| R-010 | Results are presented without validation. | Medium | High | Require a hand calculation or benchmark for every major study. |
| R-011 | Ideal beam joints overpredict global stiffness. | High | High | Run joint-stiffness sensitivity cases and local connection submodels. |
| R-012 | Linear eigenvalue buckling is mistaken for nonlinear capacity. | Medium | High | Label as screening and add imperfections/nonlinear analysis in Version 0.5. |
| R-013 | Ring mass imbalance produces unmodelled dynamic loads. | Medium | High | Add sector masses, bearing compliance and transient braking sensitivity. |
| R-014 | Preliminary material properties are used outside valid temperature/product-form ranges. | Medium | High | Replace with source-controlled project allowables before detailed claims. |

