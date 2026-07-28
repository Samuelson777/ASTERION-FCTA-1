# Version 0.3 Release Notes

Version 0.3 converts the Version 0.2 envelope into a first analysable primary structure. The generated structure contains 222 nodes and 580 beam elements and exports as GLB, OBJ and STL. Solver inputs include CSV tables and APDL templates for static docking, free-free modal and linear buckling demonstrations.

## Main limitations

- Geometry is preliminary beam/tube representation, not manufacturing detail.
- No solved ANSYS database is included.
- Bearings, joint stiffness, pressure shells and local contacts are simplified or absent.
- Linear elastic isotropic aluminium is used throughout the initial line model.
- Load cases are portfolio design cases, not certified mission or launch requirements.
