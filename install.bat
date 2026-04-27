@echo off
echo 正在安装 UCS Optimizer...
cd /d "%~dp0"
pip install .
echo.
echo 安装完成！运行 'ucs-optimizer --help' 开始使用
pause