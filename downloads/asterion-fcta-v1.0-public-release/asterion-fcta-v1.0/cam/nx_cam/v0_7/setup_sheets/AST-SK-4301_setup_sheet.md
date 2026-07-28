# AST-SK-4301 — Skimmer wing rib setup sheet

**Material:** Aluminium 2024-T3  
**Manufacturing route:** 3-axis profile milling  
**Finished envelope:** 220 × 30 × 28 mm  
**Release:** ASTERION FCTA-1 Version 0.7

## Operation sequence

| Setup | Op. | Operation | Tool | Estimated minutes |
|---|---:|---|---|---:|
| S1 | 10 | Face plate and profile rough | T01/T02 | 12.0 |
| S1 | 20 | Finish aerodynamic profile | T03 | 9.0 |

## NX CAM evidence to capture

1. Workpiece and MCS definition.
2. Tool and holder assembly.
3. In-process workpiece after each operation.
4. Toolpath verification with material removal.
5. Holder, fixture and rapid-move collision review.
6. Remaining-stock comparison.
7. Posted-code review against the approved machine configuration.

## Prove-out controls

- Verify stock dimensions and work offset physically.
- Run machine simulation with the actual machine tool and postprocessor.
- Use single block, feed override and dry-run above stock for first execution.
- Do not treat the included educational G-code as production-ready code.
