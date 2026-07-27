# Run the ASTERION native-file builder in Siemens NX

## Recommended one-click method

1. Extract the package to a short Windows path, for example `C:\ASTERION\native-builder`.
2. Double-click `RUN_ASTERION_BUILDER.bat`.
3. The launcher discovers `NXBIN`, sets the ASTERION environment variables and invokes Siemens `run_journal.exe`.
4. Review `native_output\NX_NATIVE\ASTERION_NX_BUILD_LOG.csv`.

When NX is not found automatically, open Command Prompt in the package folder and run:

```bat
RUN_ASTERION_BUILDER.bat -NxBin "C:\Program Files\Siemens\NX2306\NXBIN"
```

Use the actual folder containing `run_journal.exe`.

## GUI method

```powershell
powershell -ExecutionPolicy Bypass -File .\nxopen\run_asterion_builder.ps1 `
  -NxBin "C:\Program Files\Siemens\NX2306\NXBIN" -Gui
```

In NX, choose **Developer/Tools → Journal → Play** and select `nxopen\asterion_nx_native_builder.py`.

## Why normal Python fails

`NXOpen` belongs to the Siemens NX runtime. Running the file with `python.exe`, Python 3.13, VS Code, IDLE or PyCharm outside NX produces `ModuleNotFoundError`. The revised journal now attempts to relaunch itself through NX and otherwise exits with instructions rather than a misleading traceback.

## Overwrite an earlier build

```bat
RUN_ASTERION_BUILDER.bat -Overwrite
```

Or combine options:

```bat
RUN_ASTERION_BUILDER.bat -NxBin "C:\Program Files\Siemens\NX2306\NXBIN" -Overwrite
```

## Outputs

NX uses `.prt` for component parts, assemblies and separate master-model drawings. The output is written under `native_output\NX_NATIVE`.

## Geometry limitation

The source models are STL meshes. NX saves genuine native `.prt` files containing facet/convergent bodies, but does not reconstruct sketches, parametric features, dimensions, WAVE links or assembly constraints.

## Drawing behaviour

The builder attempts A3 sheets with front, top, right and isometric views. If your NX release or licence does not support a drafting call, the linked drawing part is saved and the build log marks the item `PARTIAL` for manual completion.
