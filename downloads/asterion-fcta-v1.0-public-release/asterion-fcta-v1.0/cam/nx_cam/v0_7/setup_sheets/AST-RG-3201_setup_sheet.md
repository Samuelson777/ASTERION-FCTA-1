# AST-RG-3201 — Ring-bearing housing setup sheet

**Material:** Aluminium 7075-T6  
**Manufacturing route:** CNC lathe + 3-axis mill  
**Finished envelope:** Ø180 × 75 mm  
**Release:** ASTERION FCTA-1 Version 0.7

## Operation sequence

| Setup | Op. | Operation | Tool | Estimated minutes |
|---|---:|---|---|---:|
| LATHE-1 | 10 | Face, rough OD and bore | T09 | 22.0 |
| LATHE-2 | 20 | Finish bearing seat and shoulders | T09/T10 | 17.0 |
| MILL-1 | 30 | Mill lugs and drill bolt circle | T02/T06 | 24.0 |

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
