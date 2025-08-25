# 🤖 Original Telegram Bot - البوت الأصلي

## 📋 الوصف
بوت Telegram أصلي لفحص البطاقات وتوليدها - نسخة مطابقة تماماً للملفات المستخرجة.

## 🚀 النشر السريع

### Railway (مجاني)
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/new?template=https://github.com/YOUR_USERNAME/YOUR_REPO)

### Render (مجاني)
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

## 🔧 التثبيت المحلي

```bash
# استنساخ المستودع
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO

# تثبيت المتطلبات
pip install -r requirements.txt

# تشغيل البوت
python3 original_bot.py
```

## ⚙️ الإعداد

### 1. إنشاء البوت
1. اذهب إلى [@BotFather](https://t.me/BotFather)
2. أرسل `/newbot`
3. اتبع التعليمات
4. احفظ التوكن

### 2. الحصول على API Credentials
1. اذهب إلى [my.telegram.org](https://my.telegram.org/auth)
2. سجل دخول
3. اذهب إلى API Development Tools
4. احفظ API_ID و API_HASH

### 3. إعداد المتغيرات البيئية
أنشئ ملف `.env`:
```env
BOT_TOKEN=your_bot_token_here
API_ID=your_api_id_here
API_HASH=your_api_hash_here
BOT_USERNAME=your_bot_username
ADMIN_ID=your_admin_id
```

## 📱 الأوامر المتاحة

- `/start` - بدء البوت
- `/bin [BIN]` - معلومات البين
- `/gen [BIN]` - توليد البطاقات

## 🎯 الميزات

- ✅ تصميم أصلي مطابق تماماً
- ✅ فحص معلومات البين
- ✅ توليد البطاقات
- ✅ واجهة تفاعلية
- ✅ دعم متعدد اللغات

## 📁 هيكل الملفات

```
├── original_bot.py          # البوت الرئيسي
├── original_config.py       # الإعدادات
├── requirements.txt         # المتطلبات
├── Procfile                # ملف Railway
├── Dockerfile              # ملف Docker
├── railway.json            # إعدادات Railway
├── runtime.txt             # إصدار Python
├── .env                    # المتغيرات البيئية
├── .gitignore              # ملفات Git
├── DEPLOY_GUIDE.md         # دليل النشر
└── README.md               # هذا الملف
```

## 🔒 الأمان

- جميع البيانات محمية
- لا يتم حفظ أي معلومات شخصية
- الاتصال مشفر

## 📞 الدعم

إذا واجهت أي مشكلة:
1. تحقق من Logs
2. تأكد من صحة التوكن
3. تأكد من تفعيل البوت

## 📄 الترخيص

هذا المشروع مخصص للاستخدام التعليمي فقط.

---

**🎯 البوت جاهز للاستخدام!** 🚀