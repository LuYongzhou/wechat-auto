#!/usr/bin/env python3
"""
修复版 GitHub Actions 自动化构建设置脚本
修复了缩进错误和其他潜在问题
"""

import os
import json
from pathlib import Path

def create_project_structure():
    """创建完整的项目结构"""
    print("📁 创建项目结构...")

    directories = [
        "src/wechatauto",
        "tests",
        "docs",
        ".github/workflows",
        "assets",
    ]

    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ 创建目录: {directory}")

    return Path(".")

def create_pyproject_toml():
    """创建项目配置文件"""
    print("📄 创建 pyproject.toml...")

    content = '''[build-system]
requires = [
    "briefcase>=0.3.0",
    "toga-android>=0.3.0",
]
build-backend = "briefcase.backends"

[tool.briefcase]
project_name = "WeChat Auto"
bundle = "com.github.wechatauto"
version = "1.0.0"
url = "https://github.com/YOUR_USERNAME/wechat-auto"
license = "MIT"
author = "GitHub Actions"
author_email = "actions@github.com"

[tool.briefcase.app.wechatauto]
formal_name = "WeChat Auto"
description = "微信消息自动化助手 - 通过GitHub Actions构建"
sources = ["src/wechatauto"]
requires = [
    "toga>=0.3.0",
]

# Android配置
[tool.briefcase.app.wechatauto.android]
permissions = [
    "android.permission.SYSTEM_ALERT_WINDOW",
    "android.permission.WRITE_EXTERNAL_STORAGE",
]

# 其他平台配置（用于本地测试）
[tool.briefcase.app.wechatauto.linux]
requires = ["toga-gtk>=0.3.0"]

[tool.briefcase.app.wechatauto.windows]
requires = ["toga-winforms>=0.3.0"]

[tool.briefcase.app.wechatauto.macos]
requires = ["toga-cocoa>=0.3.0"]
'''

    with open("pyproject.toml", "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ pyproject.toml 创建完成")

def create_github_workflow():
    """创建 GitHub Actions 工作流"""
    print("⚙️ 创建 GitHub Actions 工作流...")

    workflow_content = '''name: Build Android APK

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]
  workflow_dispatch:  # 允许手动触发

env:
  ANDROID_COMPILE_SDK: "33"
  ANDROID_BUILD_TOOLS: "33.0.0"
  ANDROID_SDK_TOOLS: "9477386"

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - name: 🛎️ 检出代码
      uses: actions/checkout@v4

    - name: 🐍 设置 Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'

    - name: 📦 安装 Python 依赖
      run: |
        python -m pip install --upgrade pip
        pip install briefcase toga

    - name: 🔧 创建 Android 项目
      run: |
        briefcase create android

    - name: 🏗️ 构建 APK
      run: |
        briefcase build android

    - name: 📦 上传 APK 制品
      uses: actions/upload-artifact@v4
      with:
        name: wechat-auto-apk
        path: android/bin/*.apk
'''

    workflow_file = ".github/workflows/build.yml"
    with open(workflow_file, "w", encoding="utf-8") as f:
        f.write(workflow_content)
    print(f"✅ GitHub Actions 工作流创建完成: {workflow_file}")

def create_app_files():
    """创建应用核心文件"""
    print("💻 创建应用代码...")

    # __init__.py
    init_content = '''"""
微信自动化助手
"""
__version__ = "1.0.0"
'''

    with open("src/wechatauto/__init__.py", "w", encoding="utf-8") as f:
        f.write(init_content)

    # app.py (简化版)
    app_content = '''import toga
from toga.style import Pack
from toga.style.pack import COLUMN

class WeChatAuto(toga.App):
    def startup(self):
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=10))
        
        title_label = toga.Label(
            '微信消息助手',
            style=Pack(padding=10, font_size=20, font_weight='bold')
        )
        
        message_input = toga.MultilineTextInput(
            placeholder='请输入消息内容...',
            style=Pack(padding=10, flex=1)
        )
        
        send_button = toga.Button(
            '发送消息',
            on_press=lambda widget: self.send_message(message_input.value),
            style=Pack(padding=10, background_color='#007AFF', color='white')
        )
        
        main_box.add(title_label)
        main_box.add(message_input)
        main_box.add(send_button)
        
        self.main_window = toga.MainWindow(title='微信助手', size=(400, 300))
        self.main_window.content = main_box
        self.main_window.show()
    
    def send_message(self, message):
        print(f"准备发送消息: {message}")

def main():
    return WeChatAuto('微信助手', 'com.github.wechatauto')
'''

    with open("src/wechatauto/app.py", "w", encoding="utf-8") as f:
        f.write(app_content)

    print("✅ 应用代码创建完成")

def create_readme():
    """创建 README 文件"""
    print("📝 创建 README.md...")

    readme_content = '''# 微信自动化助手

通过 GitHub Actions 自动构建的 Android 应用。

## 功能
- 微信消息自动化发送
- 多联系人支持
- 消息模板管理

## 构建
代码推送到 GitHub 后自动构建 APK。
'''

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    print("✅ README.md 创建完成")

def main():
    """主函数"""
    print("🚀 开始创建 GitHub Actions 自动化项目...")
    print("=" * 50)

    try:
        # 执行创建步骤
        create_project_structure()
        create_pyproject_toml()
        create_github_workflow()
        create_app_files()
        create_readme()

        print("=" * 50)
        print("🎉 项目创建完成！")
        print("")
        print("📋 下一步操作：")
        print("1. git add .")
        print("2. git commit -m '初始提交'")
        print("3. git push origin main")
        print("")
        print("🔧 GitHub Actions 将自动开始构建 APK")

    except Exception as e:
        print(f"❌ 创建过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()