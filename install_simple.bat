@echo off
:: UCS Optimizer 安装脚本
echo 正在安装 UCS Optimizer...
echo.
echo 执行命令: pip install .
echo.
:: 直接执行安装命令
pip install .
:: 检查安装结果
if %errorlevel% equ 0 (
    echo.
    echo ================================================
    echo 安装成功！
    echo ================================================
    echo 运行 'ucs-optimizer --help' 开始使用
    echo ================================================
) else (
    echo.
    echo ================================================
    echo 安装失败，请检查错误信息
    echo ================================================
)
echo.
pause