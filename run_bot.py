#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PowerBot Runner Script
تشغيل البوت بسهولة
"""

import sys
import os
import subprocess
import time

def check_dependencies():
    """فحص المكتبات المطلوبة"""
    print("🔍 فحص المكتبات المطلوبة...")
    
    required_packages = [
        'telegram',
        'requests',
        'python-dotenv',
        'aiohttp',
        'beautifulsoup4',
        'Pillow',
        'qrcode',
        'cryptography'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n📦 تثبيت المكتبات المفقودة...")
        for package in missing_packages:
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                print(f"✅ تم تثبيت {package}")
            except subprocess.CalledProcessError:
                print(f"❌ فشل في تثبيت {package}")
                return False
    
    return True

def check_config():
    """فحص إعدادات البوت"""
    print("\n⚙️ فحص إعدادات البوت...")
    
    try:
        from config import BOT_TOKEN, ADMIN_ID
        
        if not BOT_TOKEN or BOT_TOKEN == "YOUR_BOT_TOKEN":
            print("❌ لم يتم تعيين توكن البوت!")
            return False
            
        if not ADMIN_ID or ADMIN_ID == 0:
            print("❌ لم يتم تعيين آيدي المدير!")
            return False
            
        print(f"✅ توكن البوت: {BOT_TOKEN[:10]}...")
        print(f"✅ آيدي المدير: {ADMIN_ID}")
        return True
        
    except ImportError as e:
        print(f"❌ خطأ في استيراد الإعدادات: {e}")
        return False

def start_bot():
    """تشغيل البوت"""
    print("\n🚀 بدء تشغيل البوت...")
    
    try:
        from main import PowerBot
        
        bot = PowerBot()
        print("✅ تم إنشاء البوت بنجاح!")
        print("🤖 البوت يعمل الآن...")
        print("💡 اضغط Ctrl+C لإيقاف البوت")
        
        bot.run()
        
    except KeyboardInterrupt:
        print("\n⏹️ تم إيقاف البوت بواسطة المستخدم")
    except Exception as e:
        print(f"❌ خطأ في تشغيل البوت: {e}")

def main():
    """الدالة الرئيسية"""
    print("=" * 50)
    print("🤖 PowerBot - قوي جدا Telegram Bot")
    print("=" * 50)
    
    # فحص المكتبات
    if not check_dependencies():
        print("❌ فشل في تثبيت المكتبات المطلوبة")
        return
    
    # فحص الإعدادات
    if not check_config():
        print("❌ فشل في فحص الإعدادات")
        return
    
    # تشغيل البوت
    start_bot()

if __name__ == "__main__":
    main()