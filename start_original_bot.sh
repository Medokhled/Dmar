#!/bin/bash

# Original Bot - البوت الأصلي
# تشغيل البوت بسهولة

echo "🎯 Original Bot - البوت الأصلي"
echo "=============================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 غير مثبت!"
    echo "يرجى تثبيت Python3 أولاً"
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 غير مثبت!"
    echo "يرجى تثبيت pip3 أولاً"
    exit 1
fi

echo "✅ Python3 و pip3 مثبتان"

# Install requirements
echo "📦 تثبيت المكتبات المطلوبة..."
pip3 install --break-system-packages pyrogram tgcrypto requests

# Check if installation was successful
if [ $? -eq 0 ]; then
    echo "✅ تم تثبيت المكتبات بنجاح"
else
    echo "❌ فشل في تثبيت بعض المكتبات"
    echo "جاري المحاولة مرة أخرى..."
    pip3 install --upgrade pip
    pip3 install --break-system-packages pyrogram tgcrypto requests
fi

# Check config file
if [ ! -f "original_config.py" ]; then
    echo "❌ ملف الإعدادات غير موجود!"
    echo "يرجى إنشاء ملف original_config.py مع API_ID و API_HASH"
    exit 1
fi

# Start the bot
echo "🚀 بدء تشغيل Original Bot..."
echo "💡 اضغط Ctrl+C لإيقاف البوت"
echo ""

python3 original_bot.py