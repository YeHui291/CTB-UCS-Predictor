# UCS Optimizer 安装脚本
Write-Host "正在安装 UCS Optimizer..." -ForegroundColor Green

# 执行安装命令
pip install .

# 检查安装结果
if ($LASTEXITCODE -eq 0) {
    Write-Host "`n================================================" -ForegroundColor Green
    Write-Host "安装成功！" -ForegroundColor Green
    Write-Host "================================================" -ForegroundColor Green
    Write-Host "运行 'ucs-optimizer --help' 开始使用" -ForegroundColor Green
    Write-Host "================================================" -ForegroundColor Green
} else {
    Write-Host "`n================================================" -ForegroundColor Red
    Write-Host "安装失败，请检查错误信息" -ForegroundColor Red
    Write-Host "================================================" -ForegroundColor Red
}

# 等待用户按键
Write-Host "`n按任意键退出..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')