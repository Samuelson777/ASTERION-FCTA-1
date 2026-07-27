param(
    [Parameter(Mandatory=$true)]
    [string]$NxExecutable,
    [string]$OutputFolder = "$PSScriptRoot\..\native_output\NX_NATIVE",
    [switch]$Overwrite
)

$nxBin = Split-Path ([System.IO.Path]::GetFullPath($NxExecutable)) -Parent
$params = @{
    NxBin = $nxBin
    OutputFolder = $OutputFolder
    Gui = $true
}
if ($Overwrite) { $params.Overwrite = $true }
& (Join-Path $PSScriptRoot "run_asterion_builder.ps1") @params
exit $LASTEXITCODE
