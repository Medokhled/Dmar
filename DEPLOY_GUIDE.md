# 🚀 دليل نشر البوت على Railway

## 📋 المتطلبات
- حساب GitHub
- حساب Railway (مجاني)

## 🔧 خطوات النشر

### 1. رفع الكود على GitHub
```bash
git init
git add .
git commit -m "Original Bot Ready for Deployment"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### 2. النشر على Railway

1. **اذهب إلى** [railway.app](https://railway.app)
2. **سجل دخول** بحساب GitHub
3. **اضغط** "New Project"
4. **اختر** "Deploy from GitHub repo"
5. **اختر** المستودع الخاص بك
6. **انتظر** حتى يكتمل البناء

### 3. إعداد المتغيرات البيئية

في Railway Dashboard:
1. **اذهب إلى** Variables tab
2. **أضف** المتغيرات التالية:

```
BOT_TOKEN=8059528086:AAFIZLlNJzo_nUplHlXzjyShla-DsT0RNYw
API_ID=29784596
API_HASH=4f330d47c4fa2a9732caa0036942c5a9
BOT_USERNAME=Facemedobookbot
ADMIN_ID=5509130673
```

### 4. تشغيل البوت

1. **اذهب إلى** Deployments tab
2. **اضغط** "Deploy Now"
3. **انتظر** حتى يكتمل النشر
4. **تحقق من** Logs للتأكد من عدم وجود أخطاء

## ✅ التحقق من العمل

1. **افتح** Telegram
2. **ابحث عن** `@Facemedobookbot`
3. **أرسل** `/start`
4. **جرب** الأوامر:
   - `/bin 411111`
   - `/gen 411111`

## 🔧 استكشاف الأخطاء

إذا لم يعمل البوت:
1. **تحقق من** Logs في Railway
2. **تأكد من** صحة المتغيرات البيئية
3. **تحقق من** أن البوت مفعل في @BotFather

## 📞 الدعم

إذا واجهت أي مشكلة:
- تحقق من Logs في Railway
- تأكد من صحة التوكن والـ API credentials
- تأكد من أن البوت مفعل

---

**🎯 البوت جاهز للنشر!** 🚀