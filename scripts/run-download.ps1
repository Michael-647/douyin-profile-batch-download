param(
    [Parameter(Mandatory = $true)][string]$ProfileUrl,
    [Parameter(Mandatory = $true)][string]$OutputDirectory,
    [Parameter(Mandatory = $true)][string]$RuntimeDirectory,
    [int]$Limit = 0,
    [int]$Threads = 5
)

$ErrorActionPreference = "Stop"
$env:PYTHONUTF8 = "1"
$runtime = [System.IO.Path]::GetFullPath($RuntimeDirectory)
$output = [System.IO.Path]::GetFullPath($OutputDirectory)
$repo = Join-Path $runtime "douyin-downloader"
$python = Join-Path $repo ".venv/Scripts/python.exe"
$cookiesPath = Join-Path $runtime "cookies.json"
$configPath = Join-Path $runtime "private-config.yml"
$databasePath = (Join-Path $runtime "downloads.db").Replace("\", "/")
$outputYaml = $output.Replace("\", "/")

if (-not (Test-Path $python)) { throw "Run bootstrap.ps1 first: $python not found" }
if (-not (Test-Path $cookiesPath)) { throw "Capture login Cookies first: $cookiesPath not found" }
New-Item -ItemType Directory -Force -Path $output | Out-Null

$generator = @'
import json, pathlib, sys, yaml
profile, output, cookies_file, config_file, database, limit, threads = sys.argv[1:]
cookies = json.loads(pathlib.Path(cookies_file).read_text(encoding="utf-8"))
config = {
    "link": [profile], "path": output, "video": True, "music": False,
    "cover": False, "avatar": False, "json": True, "folderstyle": True,
    "download_pinned": True, "mode": ["post"], "number": {"post": int(limit)},
    "increase": {"post": False}, "thread": int(threads), "retry_times": 4,
    "proxy": "", "database": True, "database_path": database,
    "video_quality": "highest", "progress": {"quiet_logs": True},
    "browser_fallback": {"enabled": True, "headless": False, "max_scrolls": 240,
                         "idle_rounds": 8, "wait_timeout_seconds": 600},
    "cookies": cookies,
}
pathlib.Path(config_file).write_text(
    yaml.safe_dump(config, allow_unicode=True, sort_keys=False), encoding="utf-8"
)
'@

& $python -c $generator $ProfileUrl $outputYaml $cookiesPath $configPath $databasePath $Limit $Threads
Set-Location -LiteralPath $repo
& $python (Join-Path $repo "run.py") -c $configPath
exit $LASTEXITCODE
