param(
    [string]$NxBin = "",
    [string]$OutputFolder = "",
    [switch]$Overwrite,
    [switch]$Gui
)

$ErrorActionPreference = "Stop"
$builderRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$journal = Join-Path $PSScriptRoot "asterion_nx_native_builder.py"
if ([string]::IsNullOrWhiteSpace($OutputFolder)) {
    $OutputFolder = Join-Path $builderRoot "native_output\NX_NATIVE"
}
$OutputFolder = [System.IO.Path]::GetFullPath($OutputFolder)

function Add-Candidate([System.Collections.Generic.List[string]]$list, [string]$path) {
    if (-not [string]::IsNullOrWhiteSpace($path)) {
        try {
            $full = [System.IO.Path]::GetFullPath($path.Trim('"'))
            if (-not $list.Contains($full)) { $list.Add($full) }
        } catch {}
    }
}

function Find-NxBin([string]$requested) {
    $candidates = New-Object 'System.Collections.Generic.List[string]'
    Add-Candidate $candidates $requested
    Add-Candidate $candidates $env:UGII_ROOT_DIR
    if ($env:UGII_BASE_DIR) {
        Add-Candidate $candidates (Join-Path $env:UGII_BASE_DIR "NXBIN")
        Add-Candidate $candidates (Join-Path $env:UGII_BASE_DIR "UGII")
    }

    foreach ($root in @($env:ProgramFiles, ${env:ProgramFiles(x86)}, "C:\Siemens")) {
        if ([string]::IsNullOrWhiteSpace($root) -or -not (Test-Path $root)) { continue }
        $siemensRoot = if ((Split-Path $root -Leaf) -ieq "Siemens") { $root } else { Join-Path $root "Siemens" }
        if (-not (Test-Path $siemensRoot)) { continue }
        Get-ChildItem -Path $siemensRoot -Directory -ErrorAction SilentlyContinue |
            Where-Object { $_.Name -match '^(NX|NX[0-9]|NX_)' } |
            Sort-Object Name -Descending |
            ForEach-Object {
                Add-Candidate $candidates (Join-Path $_.FullName "NXBIN")
                Add-Candidate $candidates (Join-Path $_.FullName "UGII")
            }
    }

    foreach ($candidate in $candidates) {
        if ((Test-Path (Join-Path $candidate "run_journal.exe")) -or
            (Test-Path (Join-Path $candidate "ugraf.exe"))) {
            return $candidate
        }
    }
    return $null
}

$resolvedNxBin = Find-NxBin $NxBin
if (-not $resolvedNxBin) {
    Write-Host "" 
    Write-Host "Siemens NX was not found automatically." -ForegroundColor Red
    Write-Host "Run this command with your NXBIN folder, for example:" -ForegroundColor Yellow
    Write-Host ".\nxopen\run_asterion_builder.ps1 -NxBin 'C:\Program Files\Siemens\NX2306\NXBIN'" -ForegroundColor Cyan
    Write-Host "You can locate NXBIN by right-clicking the Siemens NX shortcut and opening its file location."
    exit 2
}

$env:ASTERION_BUILDER_ROOT = $builderRoot
$env:ASTERION_NX_OUTPUT = $OutputFolder
$env:ASTERION_OVERWRITE = if ($Overwrite) { "1" } else { "0" }
$env:ASTERION_NX_RELAUNCHED = "1"

# These variables help run_journal when it is launched outside the NX Command Prompt.
$nxBase = Split-Path $resolvedNxBin -Parent
if (-not $env:UGII_BASE_DIR) { $env:UGII_BASE_DIR = $nxBase }
if (-not $env:UGII_ROOT_DIR) { $env:UGII_ROOT_DIR = $resolvedNxBin + [System.IO.Path]::DirectorySeparatorChar }
$env:PATH = $resolvedNxBin + ";" + $env:PATH

Write-Host "ASTERION builder root : $builderRoot"
Write-Host "NX binary folder      : $resolvedNxBin"
Write-Host "NX output folder      : $OutputFolder"
Write-Host "Overwrite existing    : $($Overwrite.IsPresent)"

if ($Gui) {
    $ugraf = Join-Path $resolvedNxBin "ugraf.exe"
    if (-not (Test-Path $ugraf)) {
        Write-Host "ugraf.exe was not found in $resolvedNxBin" -ForegroundColor Red
        exit 3
    }
    Write-Host "Launching NX. Then use Developer/Tools > Journal > Play and select:" -ForegroundColor Yellow
    Write-Host $journal -ForegroundColor Cyan
    Start-Process -FilePath $ugraf -WorkingDirectory $builderRoot
    exit 0
}

$runner = Join-Path $resolvedNxBin "run_journal.exe"
if (-not (Test-Path $runner)) {
    Write-Host "run_journal.exe was not found in $resolvedNxBin" -ForegroundColor Red
    Write-Host "Use the GUI fallback:" -ForegroundColor Yellow
    Write-Host ".\nxopen\run_asterion_builder.ps1 -NxBin '$resolvedNxBin' -Gui" -ForegroundColor Cyan
    exit 4
}

Write-Host "Running the ASTERION journal through Siemens NX..." -ForegroundColor Green
& $runner $journal
$exitCode = $LASTEXITCODE
if ($null -eq $exitCode) { $exitCode = 0 }

if ($exitCode -ne 0) {
    Write-Host "Siemens run_journal.exe returned exit code $exitCode." -ForegroundColor Red
    Write-Host "Try the GUI fallback or run this command from the Siemens NX Command Prompt." -ForegroundColor Yellow
    exit $exitCode
}

$log = Join-Path $OutputFolder "ASTERION_NX_BUILD_LOG.csv"
Write-Host "NX journal completed." -ForegroundColor Green
Write-Host "Review the build log: $log"
exit 0
