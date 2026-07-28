# AST-TP-2101 — Thruster-gimbal bracket setup sheet

**Material:** Aluminium 6061-T6  
**Manufacturing route:** 3-axis mill, two setups  
**Finished envelope:** 160 × 120 × 113 mm  
**Release:** ASTERION FCTA-1 Version 0.7

## Operation sequence

| Setup | Op. | Operation | Tool | Estimated minutes |
|---|---:|---|---|---:|
| S1 | 10 | Face stock | T01 | 3.5 |
| S1 | 20 | Adaptive rough bracket envelope | T02 | 18.0 |
| S1 | 30 | Rest mill ears and bridge | T03 | 11.0 |
| S2 | 40 | Drill and ream gimbal bores | T05/T07 | 8.0 |
| S2 | 50 | Chamfer and deburr | T08 | 4.0 |

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
