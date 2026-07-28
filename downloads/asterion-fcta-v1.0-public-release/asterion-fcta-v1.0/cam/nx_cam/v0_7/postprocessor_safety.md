# Postprocessor and machine-safety requirements

The `.nc` examples in this repository are simulation-only teaching artefacts. They are not validated for any physical machine.

Before a real cut:

1. Select the exact controller and machine kinematic model.
2. Validate units, axis directions, work offsets, rotary conventions and tool-change position.
3. Confirm tool and holder gauge lengths.
4. Simulate stock, fixtures, spindle, table and enclosure.
5. Review every rapid move and retract plane.
6. Perform a supervised dry run above stock with reduced rapid/feed override.
7. Use single-block mode for the first prove-out.
8. Obtain approval from the responsible machine operator.

Never use generic posted code merely because it backplots correctly in a text viewer.
