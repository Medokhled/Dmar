#!/bin/bash

# 🚀 Original Bot Deployment Script
# سكريبت نشر البوت الأصلي

echo "🎯 Original Bot Deployment"
echo "=========================="

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git غير مثبت!"
    exit 1
fi

# Initialize git if not already done
if [ ! -d ".git" ]; then
    echo "📦 تهيئة Git..."
    git init
    git add .
    git commit -m "Original Bot Ready for Deployment"
    echo "✅ تم تهيئة Git"
fi

echo ""
echo "🚀 خيارات النشر:"
echo "1. Railway (مجاني)"
echo "2. Render (مجاني)"
echo "3. Heroku (مدفوع)"
echo "4. Vercel (مجاني)"
echo "5. Fly.io (مجاني)"
echo ""

read -p "اختر منصة النشر (1-5): " choice

case $choice in
    1)
        echo "🚂 النشر على Railway..."
        echo "1. اذهب إلى https://railway.app"
        echo "2. سجل دخول بحساب GitHub"
        echo "3. اضغط 'New Project'"
        echo "4. اختر 'Deploy from GitHub repo'"
        echo "5. اختر هذا المستودع"
        echo "6. انتظر حتى يكتمل النشر"
        ;;
    2)
        echo "🎨 النشر على Render..."
        echo "1. اذهب إلى https://render.com"
        echo "2. سجل دخول بحساب GitHub"
        echo "3. اضغط 'New +'"
        echo "4. اختر 'Web Service'"
        echo "5. اربط هذا المستودع"
        echo "6. اضبط الإعدادات واضغط 'Create Web Service'"
        ;;
    3)
        echo "🦊 النشر على Heroku..."
        echo "1. اذهب إلى https://heroku.com"
        echo "2. سجل دخول"
        echo "3. اضغط 'New' -> 'Create new app'"
        echo "4. اربط هذا المستودع"
        echo "5. اضغط 'Deploy Branch'"
        ;;
    4)
        echo "⚡ النشر على Vercel..."
        echo "1. اذهب إلى https://vercel.com"
        echo "2. سجل دخول بحساب GitHub"
        echo "3. اضغط 'New Project'"
        echo "4. اختر هذا المستودع"
        echo "5. اضغط 'Deploy'"
        ;;
    5)
        echo "🦅 النشر على Fly.io..."
        echo "1. اذهب إلى https://fly.io"
        echo "2. سجل دخول"
        echo "3. اضغط 'Launch App'"
        echo "4. اربط هذا المستودع"
        echo "5. اضغط 'Deploy'"
        ;;
    *)
        echo "❌ اختيار غير صحيح!"
        exit 1
        ;;
esac

echo ""
echo "✅ تم إعداد ملفات النشر!"
echo "📋 اتبع التعليمات أعلاه لإكمال النشر"
echo ""
echo "🔧 المتغيرات البيئية المطلوبة:"
echo "BOT_TOKEN=8059528086:AAFIZLlNJzo_nUplHlXzjyShla-DsT0RNYw"
echo "API_ID=29784596"
echo "API_HASH=4f330d47c4fa2a9732caa0036942c5a9"
echo "BOT_USERNAME=Facemedobookbot"
echo "ADMIN_ID=5509130673"
echo ""
echo "🎯 البوت جاهز للنشر!"