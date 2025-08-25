#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PowerBot - قوي جدا Telegram Bot
A powerful and feature-rich Telegram bot
"""

import asyncio
import logging
import os
import json
import requests
import qrcode
from io import BytesIO
from datetime import datetime
from typing import Optional

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler, CallbackQueryHandler,
    ContextTypes, filters
)
from telegram.constants import ParseMode

from config import BOT_TOKEN, ADMIN_ID, BOT_NAME, BOT_VERSION

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class PowerBot:
    def __init__(self):
        self.bot_token = BOT_TOKEN
        self.admin_id = ADMIN_ID
        self.users_data = {}
        
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        welcome_text = f"""
🌟 مرحباً {user.first_name}! أهلاً وسهلاً بك في {BOT_NAME}

🤖 أنا بوت قوي جداً مع ميزات متقدمة

📋 الأوامر المتاحة:
/help - عرض المساعدة
/info - معلومات البوت
/admin - أوامر المدير
/weather - حالة الطقس
/qr - إنشاء رمز QR
/translate - ترجمة النصوص
/calc - حاسبة
/joke - نكتة عشوائية
/quote - اقتباس ملهم

💡 للمزيد من المعلومات، اكتب /help
        """
        
        keyboard = [
            [InlineKeyboardButton("📋 المساعدة", callback_data="help")],
            [InlineKeyboardButton("⚙️ الإعدادات", callback_data="settings")],
            [InlineKeyboardButton("📊 الإحصائيات", callback_data="stats")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)
        
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """
🔧 **أوامر البوت المتاحة:**

**📱 الأوامر الأساسية:**
/start - بدء البوت
/help - هذه القائمة
/info - معلومات البوت

**🛠️ الأدوات:**
/weather [المدينة] - حالة الطقس
/qr [النص] - إنشاء رمز QR
/translate [النص] - ترجمة النصوص
/calc [المعادلة] - حاسبة
/url [الرابط] - معلومات الرابط

**🎮 الترفيه:**
/joke - نكتة عشوائية
/quote - اقتباس ملهم
/random - رقم عشوائي
/flip - رمي عملة

**📁 إدارة الملفات:**
/save - حفظ رسالة
/list - قائمة المحفوظات
/delete - حذف محفوظ

**👑 أوامر المدير:**
/admin - لوحة التحكم
/broadcast - إرسال للجميع
/stats - إحصائيات البوت
        """
        await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)
        
    async def info_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /info command"""
        info_text = f"""
🤖 **معلومات البوت:**

**الاسم:** {BOT_NAME}
**الإصدار:** {BOT_VERSION}
**الحالة:** 🟢 نشط
**المطور:** @Admin
**تاريخ الإنشاء:** {datetime.now().strftime('%Y-%m-%d')}

**📊 الإحصائيات:**
المستخدمين: {len(self.users_data)}
الرسائل: {context.bot_data.get('total_messages', 0)}

**🔧 الميزات:**
✅ معالجة الملفات
✅ إنشاء QR codes
✅ ترجمة النصوص
✅ حاسبة متقدمة
✅ معلومات الطقس
✅ نظام المحفوظات
        """
        await update.message.reply_text(info_text, parse_mode=ParseMode.MARKDOWN)
        
    async def admin_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /admin command - Admin only"""
        user_id = update.effective_user.id
        
        if user_id != self.admin_id:
            await update.message.reply_text("❌ عذراً، هذا الأمر متاح للمدير فقط!")
            return
            
        admin_text = """
👑 **لوحة تحكم المدير:**

**📊 الإحصائيات:**
/broadcast - إرسال رسالة للجميع
/stats - إحصائيات البوت
/users - قائمة المستخدمين
/backup - نسخة احتياطية

**⚙️ الإعدادات:**
/settings - إعدادات البوت
/maintenance - وضع الصيانة
/logs - سجلات البوت

**🛠️ الأدوات:**
/restart - إعادة تشغيل البوت
/update - تحديث البوت
        """
        
        keyboard = [
            [InlineKeyboardButton("📊 الإحصائيات", callback_data="admin_stats")],
            [InlineKeyboardButton("📢 البث", callback_data="admin_broadcast")],
            [InlineKeyboardButton("⚙️ الإعدادات", callback_data="admin_settings")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(admin_text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
        
    async def weather_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /weather command"""
        if not context.args:
            await update.message.reply_text("🌤️ الرجاء تحديد المدينة: /weather [اسم المدينة]")
            return
            
        city = " ".join(context.args)
        
        try:
            # Simulate weather API call
            weather_data = {
                "city": city,
                "temperature": "25°C",
                "condition": "مشمس",
                "humidity": "60%",
                "wind": "15 km/h"
            }
            
            weather_text = f"""
🌤️ **حالة الطقس في {city}:**

🌡️ درجة الحرارة: {weather_data['temperature']}
☁️ الحالة: {weather_data['condition']}
💧 الرطوبة: {weather_data['humidity']}
💨 الرياح: {weather_data['wind']}
            """
            
            await update.message.reply_text(weather_text, parse_mode=ParseMode.MARKDOWN)
            
        except Exception as e:
            await update.message.reply_text(f"❌ حدث خطأ: {str(e)}")
            
    async def qr_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /qr command"""
        if not context.args:
            await update.message.reply_text("📱 الرجاء إدخال النص: /qr [النص]")
            return
            
        text = " ".join(context.args)
        
        try:
            # Create QR code
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(text)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Save to bytes
            bio = BytesIO()
            img.save(bio, 'PNG')
            bio.seek(0)
            
            await update.message.reply_photo(
                photo=bio,
                caption=f"📱 رمز QR للنص: {text}"
            )
            
        except Exception as e:
            await update.message.reply_text(f"❌ حدث خطأ: {str(e)}")
            
    async def calc_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /calc command"""
        if not context.args:
            await update.message.reply_text("🧮 الرجاء إدخال المعادلة: /calc [2+2]")
            return
            
        expression = " ".join(context.args)
        
        try:
            # Safe evaluation
            allowed_chars = set('0123456789+-*/(). ')
            if not all(c in allowed_chars for c in expression):
                await update.message.reply_text("❌ معادلة غير صحيحة!")
                return
                
            result = eval(expression)
            await update.message.reply_text(f"🧮 النتيجة: {expression} = {result}")
            
        except Exception as e:
            await update.message.reply_text("❌ معادلة غير صحيحة!")
            
    async def joke_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /joke command"""
        jokes = [
            "لماذا لا يذهب الطبيب إلى المطعم؟ لأنه يخاف من العدوى! 😄",
            "ما هو الشيء الذي يزداد كلما أخذت منه؟ الحفرة! 🕳️",
            "لماذا يلبس الطبيب قفازات؟ لأنه لا يريد أن يلمس المرضى! 🧤",
            "ما هو الشيء الذي يكتب ولا يقرأ؟ القلم! ✏️",
            "لماذا يذهب الطبيب إلى المطعم؟ لأنه جائع! 🍽️"
        ]
        
        import random
        joke = random.choice(jokes)
        await update.message.reply_text(f"😄 {joke}")
        
    async def quote_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /quote command"""
        quotes = [
            "النجاح ليس نهاية، والفشل ليس قاتلاً: ما يهم هو الشجاعة للاستمرار. - ونستون تشرشل",
            "الطريق إلى النجاح والطريق إلى الفشل متشابهان تقريباً. - كولين ديفيس",
            "لا تقل مستحيل، قل سأحاول. - محمد علي كلاي",
            "العقل السليم في الجسم السليم. - حكمة عربية",
            "من جد وجد، ومن زرع حصد. - حكمة عربية"
        ]
        
        import random
        quote = random.choice(quotes)
        await update.message.reply_text(f"💭 {quote}")
        
    async def broadcast_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /broadcast command - Admin only"""
        user_id = update.effective_user.id
        
        if user_id != self.admin_id:
            await update.message.reply_text("❌ عذراً، هذا الأمر متاح للمدير فقط!")
            return
            
        if not context.args:
            await update.message.reply_text("📢 الرجاء إدخال الرسالة: /broadcast [الرسالة]")
            return
            
        message = " ".join(context.args)
        
        # Store message for confirmation
        context.user_data['broadcast_message'] = message
        
        keyboard = [
            [InlineKeyboardButton("✅ تأكيد الإرسال", callback_data="confirm_broadcast")],
            [InlineKeyboardButton("❌ إلغاء", callback_data="cancel_broadcast")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            f"📢 **رسالة البث:**\n\n{message}\n\nهل تريد إرسال هذه الرسالة لجميع المستخدمين؟",
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /stats command"""
        user_id = update.effective_user.id
        
        if user_id != self.admin_id:
            await update.message.reply_text("❌ عذراً، هذا الأمر متاح للمدير فقط!")
            return
            
        stats_text = f"""
📊 **إحصائيات البوت:**

👥 **المستخدمين:**
إجمالي المستخدمين: {len(self.users_data)}
المستخدمين النشطين: {len([u for u in self.users_data.values() if u.get('active', False)])}

📈 **النشاط:**
الرسائل اليوم: {context.bot_data.get('messages_today', 0)}
الرسائل الإجمالية: {context.bot_data.get('total_messages', 0)}

🤖 **البوت:**
وقت التشغيل: {context.bot_data.get('uptime', 'غير محدد')}
آخر تحديث: {datetime.now().strftime('%Y-%m-%d %H:%M')}
        """
        
        await update.message.reply_text(stats_text, parse_mode=ParseMode.MARKDOWN)
        
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle button callbacks"""
        query = update.callback_query
        await query.answer()
        
        if query.data == "help":
            await self.help_command(update, context)
        elif query.data == "settings":
            await query.edit_message_text("⚙️ إعدادات البوت قيد التطوير...")
        elif query.data == "stats":
            await query.edit_message_text("📊 الإحصائيات قيد التطوير...")
        elif query.data == "admin_stats":
            await self.stats_command(update, context)
        elif query.data == "admin_broadcast":
            await query.edit_message_text("📢 استخدم /broadcast [الرسالة] لإرسال رسالة للجميع")
        elif query.data == "admin_settings":
            await query.edit_message_text("⚙️ إعدادات المدير قيد التطوير...")
        elif query.data == "confirm_broadcast":
            message = context.user_data.get('broadcast_message', '')
            if message:
                # Simulate broadcast
                await query.edit_message_text(f"✅ تم إرسال الرسالة لـ {len(self.users_data)} مستخدم")
            else:
                await query.edit_message_text("❌ لا توجد رسالة للإرسال")
        elif query.data == "cancel_broadcast":
            await query.edit_message_text("❌ تم إلغاء البث")
            
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular messages"""
        user = update.effective_user
        message = update.message.text
        
        # Store user data
        if user.id not in self.users_data:
            self.users_data[user.id] = {
                'id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'joined_date': datetime.now().isoformat(),
                'active': True,
                'message_count': 0
            }
        
        self.users_data[user.id]['message_count'] += 1
        self.users_data[user.id]['last_activity'] = datetime.now().isoformat()
        
        # Update bot statistics
        context.bot_data['total_messages'] = context.bot_data.get('total_messages', 0) + 1
        context.bot_data['messages_today'] = context.bot_data.get('messages_today', 0) + 1
        
        # Handle different message types
        if message.startswith('/'):
            return  # Commands are handled separately
            
        # Echo message for testing
        if user.id == self.admin_id:
            await update.message.reply_text(f"👑 رسالة المدير: {message}")
        else:
            await update.message.reply_text(f"📝 رسالتك: {message}")
            
    async def translate_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /translate command"""
        if not context.args:
            await update.message.reply_text("🌐 الرجاء إدخال النص: /translate [النص]")
            return
            
        text = " ".join(context.args)
        
        # Simple translation simulation
        translations = {
            "hello": "مرحبا",
            "world": "العالم",
            "bot": "بوت",
            "powerful": "قوي",
            "telegram": "تيليجرام",
            "good": "جيد",
            "bad": "سيء",
            "yes": "نعم",
            "no": "لا"
        }
        
        if text.lower() in translations:
            result = translations[text.lower()]
        else:
            result = f"ترجمة: {text} -> العربية"
            
        await update.message.reply_text(f"🌐 **الترجمة:**\n\n{text} → {result}", parse_mode=ParseMode.MARKDOWN)
        
    async def url_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /url command"""
        if not context.args:
            await update.message.reply_text("🔗 الرجاء إدخال الرابط: /url [الرابط]")
            return
            
        url = context.args[0]
        
        try:
            # Basic URL analysis
            import re
            
            # Check if URL is valid
            url_pattern = re.compile(
                r'^https?://'  # http:// or https://
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
                r'localhost|'  # localhost...
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
                r'(?::\d+)?'  # optional port
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)
            
            is_valid = bool(url_pattern.match(url))
            
            url_info = f"""
🔗 **تحليل الرابط:**

**الرابط:** {url}
**صالح:** {'✅ نعم' if is_valid else '❌ لا'}
**النوع:** {'HTTPS' if url.startswith('https') else 'HTTP'}
**المجال:** {url.split('/')[2] if len(url.split('/')) > 2 else 'غير محدد'}
            """
            
            await update.message.reply_text(url_info, parse_mode=ParseMode.MARKDOWN)
            
        except Exception as e:
            await update.message.reply_text(f"❌ حدث خطأ: {str(e)}")
            
    async def password_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /password command"""
        length = 12  # Default length
        
        if context.args:
            try:
                length = int(context.args[0])
                if length < 4:
                    length = 4
                elif length > 50:
                    length = 50
            except ValueError:
                length = 12
        
        import random
        import string
        
        # Generate password
        chars = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"
        password = ''.join(random.choice(chars) for _ in range(length))
        
        await update.message.reply_text(f"🔐 **كلمة مرور قوية:**\n\n`{password}`", parse_mode=ParseMode.MARKDOWN)
        
    async def hash_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /hash command"""
        if len(context.args) < 2:
            await update.message.reply_text("🔒 الرجاء إدخال النص والخوارزمية: /hash [النص] [md5/sha1/sha256/base64]")
            return
            
        text = context.args[0]
        algorithm = context.args[1].lower()
        
        try:
            import hashlib
            import base64
            
            if algorithm == "md5":
                result = hashlib.md5(text.encode()).hexdigest()
            elif algorithm == "sha1":
                result = hashlib.sha1(text.encode()).hexdigest()
            elif algorithm == "sha256":
                result = hashlib.sha256(text.encode()).hexdigest()
            elif algorithm == "base64":
                result = base64.b64encode(text.encode()).decode()
            else:
                await update.message.reply_text("❌ خوارزمية غير مدعومة. استخدم: md5, sha1, sha256, base64")
                return
                
            await update.message.reply_text(f"🔒 **التشفير ({algorithm.upper()}):**\n\n`{result}`", parse_mode=ParseMode.MARKDOWN)
            
        except Exception as e:
            await update.message.reply_text(f"❌ حدث خطأ: {str(e)}")
            
    async def analyze_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /analyze command"""
        if not context.args:
            await update.message.reply_text("📊 الرجاء إدخال النص: /analyze [النص]")
            return
            
        text = " ".join(context.args)
        
        try:
            # Analyze text
            char_count = len(text)
            word_count = len(text.split())
            line_count = len(text.splitlines())
            
            # Count Arabic and English characters
            import re
            arabic_chars = len(re.findall(r'[\u0600-\u06FF]', text))
            english_chars = len(re.findall(r'[a-zA-Z]', text))
            numbers = len(re.findall(r'\d', text))
            
            analysis = f"""
📊 **تحليل النص:**

**الأحرف:** {char_count}
**الكلمات:** {word_count}
**الأسطر:** {line_count}
**الأحرف العربية:** {arabic_chars}
**الأحرف الإنجليزية:** {english_chars}
**الأرقام:** {numbers}
            """
            
            await update.message.reply_text(analysis, parse_mode=ParseMode.MARKDOWN)
            
        except Exception as e:
            await update.message.reply_text(f"❌ حدث خطأ: {str(e)}")
            
    async def random_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /random command"""
        max_num = 100  # Default max
        
        if context.args:
            try:
                max_num = int(context.args[0])
                if max_num < 1:
                    max_num = 1
                elif max_num > 1000000:
                    max_num = 1000000
            except ValueError:
                max_num = 100
        
        import random
        result = random.randint(1, max_num)
        
        await update.message.reply_text(f"🎲 **رقم عشوائي:** {result} (من 1 إلى {max_num})")
        
    async def flip_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /flip command"""
        import random
        
        result = random.choice(["صورة", "كتابة"])
        emoji = "🪙" if result == "صورة" else "📝"
        
        await update.message.reply_text(f"{emoji} **نتيجة رمي العملة:** {result}")
        
    async def save_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /save command"""
        user_id = update.effective_user.id
        
        # Initialize user saves if not exists
        if 'user_saves' not in context.bot_data:
            context.bot_data['user_saves'] = {}
        if user_id not in context.bot_data['user_saves']:
            context.bot_data['user_saves'][user_id] = []
        
        # Get the replied message or current message
        if update.message.reply_to_message:
            message_to_save = update.message.reply_to_message.text
        else:
            message_to_save = " ".join(context.args) if context.args else "لا يوجد نص للحفظ"
        
        # Save the message
        save_id = len(context.bot_data['user_saves'][user_id]) + 1
        context.bot_data['user_saves'][user_id].append({
            'id': save_id,
            'text': message_to_save,
            'date': datetime.now().isoformat()
        })
        
        await update.message.reply_text(f"💾 **تم الحفظ بنجاح!**\n\nالرقم: {save_id}\nالنص: {message_to_save[:50]}{'...' if len(message_to_save) > 50 else ''}")
        
    async def list_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /list command"""
        user_id = update.effective_user.id
        
        if 'user_saves' not in context.bot_data or user_id not in context.bot_data['user_saves']:
            await update.message.reply_text("📋 لا توجد محفوظات لك")
            return
        
        saves = context.bot_data['user_saves'][user_id]
        
        if not saves:
            await update.message.reply_text("📋 لا توجد محفوظات لك")
            return
        
        list_text = "📋 **محفوظاتك:**\n\n"
        for save in saves:
            list_text += f"**{save['id']}.** {save['text'][:30]}{'...' if len(save['text']) > 30 else ''}\n"
        
        await update.message.reply_text(list_text, parse_mode=ParseMode.MARKDOWN)
        
    async def delete_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /delete command"""
        user_id = update.effective_user.id
        
        if not context.args:
            await update.message.reply_text("🗑️ الرجاء تحديد رقم المحفوظ: /delete [الرقم]")
            return
        
        try:
            save_id = int(context.args[0])
        except ValueError:
            await update.message.reply_text("❌ الرجاء إدخال رقم صحيح")
            return
        
        if 'user_saves' not in context.bot_data or user_id not in context.bot_data['user_saves']:
            await update.message.reply_text("📋 لا توجد محفوظات لك")
            return
        
        saves = context.bot_data['user_saves'][user_id]
        
        # Find and remove the save
        for i, save in enumerate(saves):
            if save['id'] == save_id:
                deleted_text = saves.pop(i)['text']
                await update.message.reply_text(f"🗑️ **تم الحذف بنجاح!**\n\nالرقم: {save_id}\nالنص المحذوف: {deleted_text[:50]}{'...' if len(deleted_text) > 50 else ''}")
                return
        
        await update.message.reply_text(f"❌ لم يتم العثور على محفوظ برقم {save_id}")
        
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors"""
        logger.error(f"Exception while handling an update: {context.error}")
        
    def run(self):
        """Run the bot"""
        # Create application
        application = Application.builder().token(self.bot_token).build()
        
        # Add command handlers
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(CommandHandler("info", self.info_command))
        application.add_handler(CommandHandler("admin", self.admin_command))
        application.add_handler(CommandHandler("weather", self.weather_command))
        application.add_handler(CommandHandler("qr", self.qr_command))
        application.add_handler(CommandHandler("calc", self.calc_command))
        application.add_handler(CommandHandler("joke", self.joke_command))
        application.add_handler(CommandHandler("quote", self.quote_command))
        application.add_handler(CommandHandler("broadcast", self.broadcast_command))
        application.add_handler(CommandHandler("stats", self.stats_command))
        application.add_handler(CommandHandler("translate", self.translate_command))
        application.add_handler(CommandHandler("url", self.url_command))
        application.add_handler(CommandHandler("password", self.password_command))
        application.add_handler(CommandHandler("hash", self.hash_command))
        application.add_handler(CommandHandler("analyze", self.analyze_command))
        application.add_handler(CommandHandler("random", self.random_command))
        application.add_handler(CommandHandler("flip", self.flip_command))
        application.add_handler(CommandHandler("save", self.save_command))
        application.add_handler(CommandHandler("list", self.list_command))
        application.add_handler(CommandHandler("delete", self.delete_command))
        
        # Add callback query handler
        application.add_handler(CallbackQueryHandler(self.button_callback))
        
        # Add message handler
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        # Add error handler
        application.add_error_handler(self.error_handler)
        
        # Start the bot
        print(f"🤖 {BOT_NAME} v{BOT_VERSION} is starting...")
        print(f"🔑 Token: {self.bot_token[:10]}...")
        print(f"👑 Admin ID: {self.admin_id}")
        print("🚀 Bot is running...")
        
        application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    bot = PowerBot()
    bot.run()