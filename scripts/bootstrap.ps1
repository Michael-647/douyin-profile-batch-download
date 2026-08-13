param(
    [Parameter(Mandatory = $true)]
    [string]$RuntimeDirectory,
    [string]$PythonCommand = "python"
)

$ErrorActionPreference = "Stop"
$runtime = [System.IO.Path]::GetFullPath($RuntimeDirectory)
$repo = Join-Path $runtime "douyin-downloader"
New-Item -ItemType Directory -Force -Path $runtime | Out-Null

if (Test-Path (Join-Path $repo ".git")) {
    git -C $repo pull --ff-only
} elseif (Test-Path $repo) {
    throw "Runtime repository path exists but is not a Git checkout: $repo"
} else {
    git clone --depth 1 "https://github.com/jiji262/douyin-downloader.git" $repo
}

$venv = Join-Path $repo ".venv"
if (-not (Test-Path (Join-Path $venv "Scripts/python.exe"))) {
    & $PythonCommand -m venv $venv
}
$python = Join-Path $venv "Scripts/python.exe"
& $python -m pip install -r (Join-Path $repo "requirements.txt")
& $python -m pip install playwright

Write-Output "Runtime ready: $repo"
Write-Output "Capture Cookies with:"
Write-Output "& '$python' -m tools.cookie_fetcher --config '$runtime/private-config.yml' --output '$runtime/cookies.json' --include-all"
