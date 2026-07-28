# Version 0.3 Model Acceptance Criteria

| Check | Acceptance criterion |
|---|---|
| Zero-length elements | None |
| Duplicate unmerged structural nodes | None unless intentionally connected by a joint element |
| Beam section assignment | Every element has one valid section ID |
| Material assignment | Every active element uses a reviewed material card |
| Geometry units | Millimetres |
| Solver force units | Newtons |
| Free-free modal check | First six modes behave as rigid-body modes near zero frequency |
| Supported modal check | No unintended mechanism modes |
| Static equilibrium | Reaction-force balance within 1% |
| Mesh refinement | Key displacement and load-path measures change by less than 5% |
| Hand correlation | Selected benchmark results within 10% |
| Buckling interpretation | Eigenvalue result labelled as ideal linear screening only |
| Stress reporting | Beam stress kept separate from local joint stress claims |
