#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import uiautomator2 as u2
import time

def wechat_automation_interactive():
    """交互式微信自动化"""
    print("=" * 60)
    print("📱 微信自动化（交互式版）")
    print("=" * 60)

    try:
        # 连接设备
        d = u2.connect()
        print(f"✅ 连接成功: {d.info.get('productName', 'Unknown')}")

        # 启动微信
        print("🚀 启动微信...")
        d.app_start("com.tencent.mm")
        time.sleep(8)

        # 显示当前屏幕内容，帮助用户识别联系人
        print("\n📋 正在分析屏幕内容...")
        display_screen_contents(d)

        # 让用户选择联系人
        contact_name = select_contact_interactive(d)
        if not contact_name:
            return

        # 输入要发送的消息
        message = input("\n💬 请输入要发送的消息: ").strip()
        if not message:
            message = "你好！"

        print(f"\n🎯 开始发送消息给: {contact_name}")

        # 查找并点击联系人
        if find_and_click_contact(d, contact_name):
            time.sleep(3)
            send_message(d, message)
        else:
            print(f"❌ 无法找到联系人: {contact_name}")

    except Exception as e:
        print(f"❌ 执行失败: {e}")

def display_screen_contents(d):
    """显示屏幕上的文本内容，帮助用户识别联系人"""
    try:
        # 获取所有文本元素
        elements = d(className="android.widget.TextView")
        texts = []

        for element in elements:
            text = element.get_text()
            if text and text.strip() and len(text.strip()) > 1:
                texts.append(text.strip())

        # 去重并显示
        unique_texts = list(set(texts))
        print("\n📝 屏幕上找到的文本内容:")
        print("-" * 40)
        for i, text in enumerate(unique_texts[:25]):  # 只显示前25个，避免太多
            print(f"{i+1:2d}. {text}")
        print("-" * 40)

    except Exception as e:
        print(f"❌ 获取屏幕内容失败: {e}")

def select_contact_interactive(d):
    """让用户交互式选择联系人"""
    print("\n👤 请选择联系人:")
    print("1. 手动输入联系人名称")
    print("2. 从屏幕内容中选择")

    choice = input("请选择 (1 或 2): ").strip()

    if choice == "1":
        contact_name = input("请输入联系人名称: ").strip()
        return contact_name
    elif choice == "2":
        return select_from_screen_content(d)
    else:
        print("❌ 无效选择")
        return None

def select_from_screen_content(d):
    """从屏幕内容中选择联系人"""
    try:
        # 获取可能是联系人的文本（过滤掉系统文本）
        elements = d(className="android.widget.TextView")
        potential_contacts = []

        for element in elements:
            text = element.get_text()
            if text and text.strip():
                # 过滤条件：不是纯数字，不包含冒号，长度适中
                if (len(text.strip()) > 1 and
                        len(text.strip()) < 20 and
                        not text.strip().isdigit() and
                        ':' not in text and
                        '微信' not in text and
                        '通讯录' not in text and
                        '搜索' not in text):
                    potential_contacts.append((element, text.strip()))

        # 去重
        unique_contacts = []
        seen_texts = set()
        for element, text in potential_contacts:
            if text not in seen_texts:
                unique_contacts.append((element, text))
                seen_texts.add(text)

        print("\n📞 可能的联系人列表:")
        for i, (element, text) in enumerate(unique_contacts[:20]):  # 只显示前20个
            print(f"{i+1:2d}. {text}")

        try:
            choice = int(input("\n请选择联系人编号: ").strip())
            if 1 <= choice <= len(unique_contacts):
                selected_element, selected_text = unique_contacts[choice-1]
                selected_element.click()
                print(f"✅ 已选择: {selected_text}")
                return selected_text
            else:
                print("❌ 无效编号")
                return None
        except ValueError:
            print("❌ 请输入有效数字")
            return None

    except Exception as e:
        print(f"❌ 选择联系人失败: {e}")
        return None

def find_and_click_contact(d, contact_name):
    """查找并点击联系人"""
    print(f"🔍 查找联系人: {contact_name}")

    # 方法1：直接查找
    if d(text=contact_name).exists:
        d(text=contact_name).click()
        print(f"✅ 直接找到并点击: {contact_name}")
        return True

    # 方法2：通过搜索查找
    print("  尝试通过搜索查找...")
    search_selectors = [
        d(text="搜索"),
        d(description="搜索"),
        d(resourceId="com.tencent.mm:id/iw")
    ]

    for selector in search_selectors:
        if selector.exists:
            selector.click()
            time.sleep(2)

            # 输入搜索内容
            if d(className="android.widget.EditText").exists:
                d(className="android.widget.EditText").set_text(contact_name)
                time.sleep(3)

                # 点击搜索结果
                if d(text=contact_name).exists:
                    d(text=contact_name).click()
                    print(f"✅ 通过搜索找到: {contact_name}")
                    return True
            break

    # 方法3：滑动查找
    print("  尝试滑动查找...")
    width, height = d.window_size()
    for i in range(5):
        if d(text=contact_name).exists:
            d(text=contact_name).click()
            print(f"✅ 滑动找到: {contact_name}")
            return True
        d.swipe(width//2, height*0.7, width//2, height*0.3, 0.5)
        time.sleep(2)

    return False

def send_message(d, message):
    """发送消息"""
    print("💬 发送消息...")
    time.sleep(2)

    # 查找输入框
    input_selectors = [
        d(className="android.widget.EditText"),
        d(description="输入框"),
        d(resourceId="com.tencent.mm:id/anv")
    ]

    for selector in input_selectors:
        if selector.exists:
            selector.click()
            time.sleep(1)
            d.send_keys(message)
            time.sleep(1)

            # 发送消息
            if d(text="发送").exists:
                d(text="发送").click()
            else:
                d.press("enter")

            print(f"✅ 消息发送成功: {message}")
            return True

    print("❌ 找不到输入框")
    return False

if __name__ == "__main__":
    wechat_automation_interactive()

