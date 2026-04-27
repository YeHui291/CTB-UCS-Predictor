#!/usr/bin/env python
# UCS Optimizer 安装脚本
import os
import subprocess
import sys

def main():
    print("正在安装 UCS Optimizer...")
    print(f"当前路径: {os.getcwd()}")
    
    # 执行安装命令（使用 --user 选项避免权限问题）
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "--user", "."],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("\n安装成功！")
        print("运行 'ucs-optimizer --help' 开始使用")
    else:
        print("\n安装失败:")
        print(f"错误信息: {result.stderr}")
    
    input("\n按回车键退出...")

if __name__ == "__main__":
    main()