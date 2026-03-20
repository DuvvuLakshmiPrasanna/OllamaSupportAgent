$ErrorActionPreference = 'Stop'

Write-Host "Verifying required submission structure..."

$required = @(
    'README.md',
    'setup.md',
    'chatbot.py',
    'report.md',
    'requirements.txt',
    'prompts/zero_shot_template.txt',
    'prompts/one_shot_template.txt',
    'eval/results.md'
)

$missing = @()
foreach ($path in $required) {
    if (-not (Test-Path $path)) {
        $missing += $path
    }
}

if ($missing.Count -gt 0) {
    Write-Host "Missing required files:" -ForegroundColor Red
    $missing | ForEach-Object { Write-Host " - $_" -ForegroundColor Red }
    exit 1
}

$queryRows = Select-String -Path 'eval/results.md' -Pattern '^\|\s*\d+\s*\|'
$rows = $queryRows.Count
$queryIds = $queryRows | ForEach-Object {
    if ($_.Line -match '^\|\s*(\d+)\s*\|') { [int]$Matches[1] }
} | Sort-Object -Unique

Write-Host "Found response rows: $rows"
Write-Host "Found unique queries: $($queryIds.Count)"

if ($rows -lt 40 -or $queryIds.Count -lt 20) {
    Write-Host "Evaluation table check failed (need at least 40 rows and 20 unique queries)." -ForegroundColor Red
    exit 1
}

Write-Host "Submission verification passed." -ForegroundColor Green
