# ANSYS Mesh Strategy

## General rules

- Begin with the simplest valid idealisation.
- Use beam elements for truss members where local stress is not required.
- Use shell elements for thin panels and skins.
- Use solids only around local joints, brackets, contacts, and thick regions.
- Use symmetry whenever loads and geometry allow it.
- Remove cosmetic fillets, small fasteners, text, and non-structural detail.
- Use bonded contacts for early global studies; introduce realistic contacts only where they affect the result.

## Convergence method

1. Define one primary result metric before meshing.
2. Run coarse, medium, and refined meshes.
3. Record element count, solve time, and result metric.
4. Accept the mesh when the selected metric changes by less than 5% between the last two levels.
5. Investigate singularities separately; do not report singular peak stress as a design value.
