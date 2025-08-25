#!/bin/bash

# Super Checker Bot - بوت فحص البطاقات القوي
# تشغيل البوت بسهولة

echo "🔍 Super Checker Bot - بوت فحص البطاقات القوي"
echo "=============================================="

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
pip3 install -r requirements_super.txt

# Check if installation was successful
if [ $? -eq 0 ]; then
    echo "✅ تم تثبيت المكتبات بنجاح"
else
    echo "❌ فشل في تثبيت بعض المكتبات"
    echo "جاري المحاولة مرة أخرى..."
    pip3 install --upgrade pip
    pip3 install -r requirements_super.txt
fi

# Create banned bins file if not exists
if [ ! -f "banned_bins.txt" ]; then
    echo "📝 إنشاء ملف البينات المحظورة..."
    touch banned_bins.txt
    echo "# قائمة البينات المحظورة" > banned_bins.txt
    echo "# أضف البينات المحظورة هنا (سطر واحد لكل بين)" >> banned_bins.txt
fi

# Start the bot
echo "🚀 بدء تشغيل Super Checker Bot..."
echo "💡 اضغط Ctrl+C لإيقاف البوت"
echo ""

python3 super_checker_bot.py