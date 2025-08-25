# 🎯 Original Bot - البوت الأصلي

## معلومات سريعة ⚡

**التوكن:** `8059528086:AAFIZLlNJzo_nUplHlXzjyShla-DsT0RNYw`  
**آيدي المدير:** `5509130673`  
**الإصدار:** 1.0  
**الحالة:** جاهز للتشغيل ✅

## كيفية التشغيل 🚀

### الطريقة الأولى (الأسهل):
```bash
./start_original_bot.sh
```

### الطريقة الثانية:
```bash
python3 original_bot.py
```

## التصميم الأصلي 🎨

هذا البوت هو **نسخة طبق الأصل** من الملفات المستخرجة:

### 📱 **واجهة البداية:**
```
Good Morning [User Name][User ID] ⛅,
How Are You?
I Am Jocasta. The Multi Functional Bot For You.
Today Is 15th Of December 2024 And Time Is 10-30 AM.
Check And Click Down For More

[📒 MY ACCOUNT 📒] [🚪 GATES 🚪]
[🔒 CLOSE 🔒]
```

### 🎯 **القوائم التفاعلية:**

#### **MY ACCOUNT:**
```
〄 User Information:-
○ First Name: [Name]
○ User Name: [Username]
○ User Id: [ID]
○ Limited: [Status]
○ Profile Link: Click Here
○ Profile Image: Click Here

〄 User Database Information:-
○ Role: User
○ Plan: Free
○ Status: Active
○ Credits: 100
○ Live Cards: 0
○ AntiSpam Time: [Time]

〄 Chat Information:-
○ Chat Name: [Name]
○ User Name: [Username]
○ Chat Id: [ID]
○ Chat Type: [Type]
```

#### **GATES:**
```
Check Down My Commands

[🎁 FREE 🎁] [💲 PAID 💲]
[🛠️ TOOLS 🛠️] [🚪 CLOSE 🚪]
```

#### **FREE GATES:**
```
🎁 FREE GATES 🎁

🔍 BIN - Get BIN Information
🔧 GEN - Generate Cards from BIN
🔍 CHECK - Check Single Card
📊 STATS - Your Statistics

[🔍 BIN 🔍] [🔧 GEN 🔧]
[🔍 CHECK 🔍] [📊 STATS 📊]
[🔙 BACK 🔙] [🚪 CLOSE 🚪]
```

## الأوامر المتاحة 📋

### 🔍 **BIN Information:**
```
/bin [BIN]
```
**مثال:** `/bin 453264`

### 🔧 **Generate Cards:**
```
/gen [BIN]
```
**مثال:** `/gen 453264`

### 📝 **Start:**
```
/start
```

## نتائج الفحص 📊

### **BIN Information:**
```
〄 Bin Information:-
○ Bin: 453264✅
○ Vendor: VISA
○ Type: CREDIT
○ Level: CLASSIC
○ Bank: JPMORGAN CHASE BANK NA
○ Country: US(🇺🇸)
○ Dial Code: +1
○ Checked By: [User Name][User]
○ BOT BY: @Admin
```

### **Card Generation:**
```
〄 CC GENRATOR
○ YOUR DATA = 453264|x|x|x.
○ BANK INFO: JPMORGAN CHASE BANK NA - US(🇺🇸)
○ BIN INFO: 453264 - CLASSIC - CREDIT

4532640527811643|12|2025|123
4532640527811644|01|2026|456
4532640527811645|03|2027|789
...

[GEN AGAIN]
```

## الملفات المهمة 📁

- **`original_bot.py`** - البوت الرئيسي
- **`original_config.py`** - إعدادات البوت
- **`start_original_bot.sh`** - تشغيل سريع

## المتطلبات 🔧

### المكتبات المطلوبة:
- `pyrogram` - مكتبة تيليجرام
- `tgcrypto` - تشفير تيليجرام
- `requests` - طلبات HTTP

### الإعدادات المطلوبة:
1. **API_ID** - من https://my.telegram.org/auth
2. **API_HASH** - من https://my.telegram.org/auth
3. **BOT_TOKEN** - من @BotFather

## الإعداد ⚙️

1. اذهب إلى https://my.telegram.org/auth
2. احصل على API_ID و API_HASH
3. عدل ملف `original_config.py`:
```python
API_ID = 123456  # ضع API_ID الخاص بك
API_HASH = "your_api_hash_here"  # ضع API_HASH الخاص بك
```

## البينات المدعومة 🏦

### Visa:
- 4xxxxxxxxxxxxxxx

### Mastercard:
- 5xxxxxxxxxxxxxxx

### American Express:
- 3xxxxxxxxxxxxxx

### Discover:
- 6xxxxxxxxxxxxxxx

## الأمان 🔒

- ✅ **تحقق من صحة البطاقة** - Luhn algorithm
- ✅ **فلترة البينات المحظورة** - حظر البينات غير المرغوبة
- ✅ **نظام التسجيل** - تسجيل المستخدمين
- ✅ **حماية من الاستخدام المفرط** - rate limiting

## الدعم 💬

إذا واجهت أي مشكلة:
1. تأكد من تثبيت Python 3.8+
2. تأكد من تثبيت جميع المكتبات
3. تأكد من صحة API_ID و API_HASH
4. تأكد من صحة التوكن والآيدي

## المطور 👨‍💻

تم تطوير هذا البوت باستخدام الكود الأصلي من:
- Python Checker Bot
- Telegram Bot V1

---

**تم التطوير بـ ❤️ لإنشاء البوت الأصلي**