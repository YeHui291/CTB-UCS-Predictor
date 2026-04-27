# UCS Optimizer install script
Write-Host "Installing UCS Optimizer..." -ForegroundColor Green

# Execute install command
pip install .

# Check installation result
if ($LASTEXITCODE -eq 0) {
    Write-Host "`n================================================" -ForegroundColor Green
    Write-Host "Installation successful!" -ForegroundColor Green
    Write-Host "================================================" -ForegroundColor Green
    Write-Host "Run 'ucs-optimizer --help' to get started" -ForegroundColor Green
    Write-Host "================================================" -ForegroundColor Green
} else {
    Write-Host "`n================================================" -ForegroundColor Red
    Write-Host "Installation failed, please check error messages" -ForegroundColor Red
    Write-Host "================================================" -ForegroundColor Red
}

# Wait for user input
Write-Host "`nPress any key to exit..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')