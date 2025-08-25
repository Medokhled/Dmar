#!/bin/bash

# Original Design Bot - بوت بالتصميم الأصلي
# تشغيل البوت بسهولة

echo "🎨 Original Design Bot - بوت بالتصميم الأصلي"
echo "============================================="

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
pip3 install python-telegram-bot==20.7 requests==2.31.0

# Check if installation was successful
if [ $? -eq 0 ]; then
    echo "✅ تم تثبيت المكتبات بنجاح"
else
    echo "❌ فشل في تثبيت بعض المكتبات"
    echo "جاري المحاولة مرة أخرى..."
    pip3 install --upgrade pip
    pip3 install python-telegram-bot==20.7 requests==2.31.0
fi

# Create banned bins file if not exists
if [ ! -f "bannedbin.txt" ]; then
    echo "📝 إنشاء ملف البينات المحظورة..."
    touch bannedbin.txt
    echo "# قائمة البينات المحظورة" > bannedbin.txt
    echo "# أضف البينات المحظورة هنا (سطر واحد لكل بين)" >> bannedbin.txt
fi

# Start the bot
echo "🚀 بدء تشغيل Original Design Bot..."
echo "💡 اضغط Ctrl+C لإيقاف البوت"
echo ""

python3 original_design_bot.py