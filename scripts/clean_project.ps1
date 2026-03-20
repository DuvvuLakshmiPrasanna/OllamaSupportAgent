$ErrorActionPreference = 'Stop'

Write-Host "Cleaning local-only artifacts..."

$targets = @(
    'venv',
    '.venv',
    'env',
    'ENV',
    '__pycache__',
    '.pytest_cache',
    '.ipynb_checkpoints',
    'build',
    'dist',
    '.eggs',
    'htmlcov',
    '.coverage',
    'coverage.xml',
    '.DS_Store'
)

foreach ($target in $targets) {
    if (Test-Path $target) {
        Remove-Item -Recurse -Force $target
        Write-Host "Removed: $target"
    }
}

Get-ChildItem -Recurse -File -Include *.pyc, *.pyo, *.pyd | ForEach-Object {
    Remove-Item -Force $_.FullName
    Write-Host "Removed: $($_.FullName)"
}

Write-Host "Cleanup complete."
