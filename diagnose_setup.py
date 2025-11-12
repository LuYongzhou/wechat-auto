#!/usr/bin/env python3
"""
GitHub Actions 设置脚本诊断工具
用于诊断和解决脚本运行问题
"""

import os
import sys
import platform
from pathlib import Path

def print_section(title):
    """打印章节标题"""
    print(f"\n{'='*50}")
    print(f"🔍 {title}")
    print(f"{'='*50}")

def test_environment():
    """测试环境信息"""
    print_section("环境信息检查")

    print(f"Python 版本: {sys.version}")
    print(f"平台系统: {platform.system()} {platform.release()}")
    print(f"工作目录: {os.getcwd()}")
    print(f"Python 可执行文件: {sys.executable}")

    # 检查编码
    print(f"文件系统编码: {sys.getfilesystemencoding()}")
    print(f"标准输出编码: {sys.stdout.encoding}")
    print(f"默认编码: {sys.getdefaultencoding()}")

def test_file_operations():
    """测试文件操作"""
    print_section("文件操作测试")

    # 测试目录创建
    test_dirs = ["test_dir1", "test_dir2/subdir"]
    for dir_path in test_dirs:
        try:
            os.makedirs(dir_path, exist_ok=True)
            print(f"✅ 目录创建成功: {dir_path}")
        except Exception as e:
            print(f"❌ 目录创建失败 {dir_path}: {e}")

    # 测试文件创建
    test_files = {
        "test_file.txt": "这是一个测试文件",
        "test_unicode.txt": "中文测试 Unicode测试 🚀"
    }

    for filename, content in test_files.items():
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ 文件创建成功: {filename}")
        except Exception as e:
            print(f"❌ 文件创建失败 {filename}: {e}")

def test_output_buffering():
    """测试输出缓冲"""
    print_section("输出缓冲测试")

    print("1. 普通打印输出")
    sys.stdout.flush()  # 强制刷新缓冲区

    print("2. 带换行符的输出", end='\n')
    sys.stdout.flush()

    print("3. 使用 stderr 输出", file=sys.stderr)

    # 测试即时输出
    for i in range(3):
        print(f"⏰ 即时输出测试 {i+1}/3", flush=True)
        import time
        time.sleep(1)

def test_imports():
    """测试必要的导入"""
    print_section("模块导入测试")

    required_modules = [
        "json",
        "pathlib",
        "threading",
        "datetime"
    ]

    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ 模块可用: {module}")
        except ImportError as e:
            print(f"❌ 模块导入失败 {module}: {e}")

def check_original_script():
    """检查原脚本"""
    print_section("原脚本检查")

    script_path = "setup_github_actions.py"

    if os.path.exists(script_path):
        print(f"✅ 原脚本存在: {script_path}")

        # 检查文件大小
        file_size = os.path.getsize(script_path)
        print(f"📏 文件大小: {file_size} 字节")

        # 读取前几行检查编码
        try:
            with open(script_path, "r", encoding="utf-8") as f:
                first_lines = [f.readline().strip() for _ in range(5)]
            print("📄 文件前5行:")
            for i, line in enumerate(first_lines, 1):
                print(f"  {i}: {line}")
        except UnicodeDecodeError as e:
            print(f"❌ 文件编码问题: {e}")
            # 尝试其他编码
            encodings = ['gbk', 'latin-1', 'cp1252']
            for encoding in encodings:
                try:
                    with open(script_path, "r", encoding=encoding) as f:
                        content = f.read(100)
                    print(f"✅ 可用编码: {encoding}")
                    break
                except:
                    continue
    else:
        print(f"❌ 原脚本不存在: {script_path}")

def run_original_script_safely():
    """安全运行原脚本"""
    print_section("安全运行原脚本")

    script_path = "setup_github_actions.py"

    if not os.path.exists(script_path):
        print("❌ 原脚本不存在，跳过运行")
        return

    try:
        print("🚀 开始执行原脚本...")

        # 读取脚本内容
        with open(script_path, "r", encoding="utf-8") as f:
            script_content = f.read()

        # 创建安全的执行环境
        global_env = {
            '__name__': '__main__',
            'os': os,
            'sys': sys,
            'json': __import__('json'),
            'Path': Path
        }

        # 分步执行脚本
        print("📝 执行脚本初始化部分...")
        sys.stdout.flush()

        # 只执行到第一个函数定义
        lines = script_content.split('\n')
        executing_lines = []

        for i, line in enumerate(lines):
            executing_lines.append(line)
            if line.strip().startswith('def ') and i > 10:  # 找到第一个函数定义
                break

        partial_script = '\n'.join(executing_lines)

        try:
            exec(partial_script, global_env)
            print("✅ 脚本初始化执行成功")

            # 尝试调用主函数
            if 'create_project_structure' in global_env:
                print("🔄 调用 create_project_structure()...")
                sys.stdout.flush()
                global_env['create_project_structure']()
                print("✅ 项目结构创建函数执行成功")

        except Exception as e:
            print(f"❌ 脚本执行出错: {e}")
            import traceback
            traceback.print_exc()

    except Exception as e:
        print(f"❌ 运行原脚本失败: {e}")
        import traceback
        traceback.print_exc()

def cleanup_test_files():
    """清理测试文件"""
    print_section("清理测试文件")

    test_items = [
        "test_dir1", "test_dir2",
        "test_file.txt", "test_unicode.txt",
        "test_script.py"
    ]

    for item in test_items:
        if os.path.exists(item):
            try:
                if os.path.isdir(item):
                    import shutil
                    shutil.rmtree(item)
                else:
                    os.remove(item)
                print(f"🧹 清理: {item}")
            except Exception as e:
                print(f"⚠️ 清理失败 {item}: {e}")

def main():
    """主函数"""
    print("🎯 GitHub Actions 设置脚本诊断工具")
    print("开始全面诊断...")

    try:
        test_environment()
        test_output_buffering()
        test_imports()
        check_original_script()
        test_file_operations()
        run_original_script_safely()

    except Exception as e:
        print(f"💥 诊断过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

    finally:
        cleanup_test_files()

    print_section("诊断完成")
    print("📋 请将上面的输出信息复制给我，以便进一步分析问题")

if __name__ == "__main__":
    main()