#!/usr/bin/env python
# 金属矿山充填体强度与碳排放智能预测系统 安装脚本
import os
import subprocess
import sys

def main():
    print("正在安装 金属矿山充填体强度与碳排放智能预测系统依赖包...")
    print(f"当前路径: {os.getcwd()}")

    # 安装依赖包
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print("\n依赖包安装成功！")
        print("Web 界面：运行 'streamlit run app.py' 开始使用")
        print("命令行：运行 'python -m ucs_optimizer --help' 查看可用命令")
    else:
        print("\n安装失败:")
        print(f"错误信息: {result.stderr}")
    
    input("\n按回车键退出...")

if __name__ == "__main__":
    main()