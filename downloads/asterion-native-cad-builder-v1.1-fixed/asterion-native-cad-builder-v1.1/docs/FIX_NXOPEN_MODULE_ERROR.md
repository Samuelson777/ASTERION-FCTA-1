# Fix: `ModuleNotFoundError: No module named NXOpen`

## Cause

The journal was started with ordinary Windows Python, VS Code, IDLE, or another external interpreter. `NXOpen` is loaded by Siemens NX; it is not a normal pip dependency.

## Recommended fix

1. Extract the package to a short local path such as `C:\ASTERION\native-builder`.
2. Double-click `RUN_ASTERION_BUILDER.bat`.
3. The launcher searches for Siemens NX and executes the journal using `run_journal.exe`.
4. Review `native_output\NX_NATIVE\ASTERION_NX_BUILD_LOG.csv`.

## When NX is not detected

Open Command Prompt in the package folder and provide your actual NXBIN folder:

```bat
RUN_ASTERION_BUILDER.bat -NxBin "C:\Program Files\Siemens\NX2306\NXBIN"
```

Change `NX2306` to your installed release. The folder must contain `run_journal.exe` and normally `ugraf.exe`.

## GUI fallback

```powershell
powershell -ExecutionPolicy Bypass -File .\nxopen\run_asterion_builder.ps1 `
  -NxBin "C:\Program Files\Siemens\NX2306\NXBIN" -Gui
```

Then, inside NX, choose **Developer/Tools > Journal > Play** and select:

```text
nxopen\asterion_nx_native_builder.py
```

## Do not do this

- Do not run `python asterion_nx_native_builder.py` directly.
- Do not use VS Code's **Run Python File** button.
- Do not install the unrelated PyPI package called `nxopen`; it is not Siemens NXOpen.

## If batch mode still fails

Run the same command from the **Siemens NX Command Prompt**, which initializes the NX environment before invoking `run_journal.exe`. The GUI fallback is also valid.
