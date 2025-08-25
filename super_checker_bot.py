#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Super Checker Bot - بوت فحص البطاقات القوي
Combines all card checking features from multiple bots
"""

import asyncio
import logging
import os
import json
import re
import random
import time
import requests
import hashlib
import base64
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from io import BytesIO

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler, CallbackQueryHandler,
    ContextTypes, filters
)
from telegram.constants import ParseMode

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class SuperCheckerBot:
    def __init__(self):
        self.bot_token = "8059528086:AAFIZLlNJzo_nUplHlXzjyShla-DsT0RNYw"
        self.admin_id = 5509130673
        self.users_data = {}
        self.check_results = {}
        self.banned_bins = set()
        self.waste_cards = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}
        
        # Load banned bins
        self.load_banned_bins()
        
    def load_banned_bins(self):
        """Load banned BINs from file"""
        try:
            if os.path.exists('banned_bins.txt'):
                with open('banned_bins.txt', 'r') as f:
                    for line in f:
                        self.banned_bins.add(line.strip())
        except Exception as e:
            logger.error(f"Error loading banned BINs: {e}")
            
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        welcome_text = f"""
🌟 مرحباً {user.first_name}! أهلاً وسهلاً بك في Super Checker Bot

🔍 أنا بوت فحص البطاقات القوي مع ميزات متقدمة

📋 الأوامر المتاحة:

🔐 **فحص البطاقات:**
/check [CC|MM|YYYY|CVV] - فحص بطاقة واحدة
/checkfile - فحص ملف البطاقات
/bin [BIN] - معلومات البين
/gen [BIN] - توليد بطاقات من البين

💳 **Stripe Checker:**
/stripe [CC|MM|YYYY|CVV] [SK] [AMOUNT] - فحص Stripe
/stripefile [FILE] [SK] [AMOUNT] - فحص ملف Stripe

🛠️ **الأدوات:**
/valid - البطاقات الصالحة
/dead - البطاقات الميتة
/stats - الإحصائيات
/clear - مسح النتائج

👑 **أوامر المدير:**
/admin - لوحة التحكم
/broadcast - البث الجماعي

💡 للمزيد من المعلومات، اكتب /help
        """
        
        keyboard = [
            [InlineKeyboardButton("🔍 فحص البطاقات", callback_data="check_cards")],
            [InlineKeyboardButton("💳 Stripe Checker", callback_data="stripe_check")],
            [InlineKeyboardButton("📊 الإحصائيات", callback_data="stats")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)
        
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """
🔧 **أوامر البوت المتاحة:**

**🔐 فحص البطاقات:**
/check [CC|MM|YYYY|CVV] - فحص بطاقة واحدة
/checkfile - فحص ملف البطاقات
/bin [BIN] - معلومات البين
/gen [BIN] - توليد بطاقات من البين

**💳 Stripe Checker:**
/stripe [CC|MM|YYYY|CVV] [SK] [AMOUNT] - فحص Stripe
/stripefile [FILE] [SK] [AMOUNT] - فحص ملف Stripe

**🛠️ الأدوات:**
/valid - البطاقات الصالحة
/dead - البطاقات الميتة
/stats - الإحصائيات
/clear - مسح النتائج

**👑 أوامر المدير:**
/admin - لوحة التحكم
/broadcast - البث الجماعي

**📋 أمثلة الاستخدام:**
/check 4532640527811643|12|2025|123
/bin 453264
/gen 453264
/stripe 4532640527811643|12|2025|123 sk_test_xxx 1000
        """
        await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)
        
    def parse_card(self, card_input: str) -> Optional[Dict]:
        """Parse card input and validate format"""
        try:
            # Remove spaces and split by |
            card_parts = card_input.replace(' ', '').split('|')
            
            if len(card_parts) != 4:
                return None
                
            cc, mm, yyyy, cvv = card_parts
            
            # Validate card number
            if not cc.isdigit() or len(cc) < 13 or len(cc) > 19:
                return None
                
            # Validate month
            if not mm.isdigit() or int(mm) < 1 or int(mm) > 12:
                return None
                
            # Validate year
            if not yyyy.isdigit() or len(yyyy) != 4:
                return None
                
            # Validate CVV
            if not cvv.isdigit() or len(cvv) < 3 or len(cvv) > 4:
                return None
                
            return {
                'cc': cc,
                'mm': mm,
                'yyyy': yyyy,
                'cvv': cvv,
                'bin': cc[:6]
            }
        except Exception:
            return None
            
    async def check_card(self, card_data: Dict) -> Dict:
        """Check a single card"""
        try:
            # Simulate card checking (replace with real API calls)
            card_str = f"{card_data['cc']}|{card_data['mm']}|{card_data['yyyy']}|{card_data['cvv']}"
            
            # Random result for demonstration
            results = [
                {"status": "LIVE", "message": "Card Approved ✅", "bank": "Chase Bank", "country": "US"},
                {"status": "DEAD", "message": "Card Declined ❌", "bank": "Unknown", "country": "Unknown"},
                {"status": "LIVE", "message": "Card Approved ✅", "bank": "Wells Fargo", "country": "US"},
                {"status": "DEAD", "message": "Insufficient Funds ❌", "bank": "Unknown", "country": "Unknown"}
            ]
            
            result = random.choice(results)
            result['card'] = card_str
            result['time'] = datetime.now().isoformat()
            
            return result
            
        except Exception as e:
            return {
                "status": "ERROR",
                "message": f"Error checking card: {str(e)}",
                "card": card_str,
                "time": datetime.now().isoformat()
            }
            
    async def check_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /check command"""
        if not context.args:
            await update.message.reply_text("🔍 الرجاء إدخال البطاقة: /check [CC|MM|YYYY|CVV]")
            return
            
        card_input = " ".join(context.args)
        card_data = self.parse_card(card_input)
        
        if not card_data:
            await update.message.reply_text("❌ تنسيق البطاقة غير صحيح. استخدم: CC|MM|YYYY|CVV")
            return
            
        # Check if BIN is banned
        if card_data['bin'] in self.banned_bins:
            await update.message.reply_text("❌ هذا البين محظور!")
            return
            
        # Check if it's a waste card
        if int(card_data['cc'][0]) in self.waste_cards:
            await update.message.reply_text("❌ بطاقة غير صالحة!")
            return
            
        msg = await update.message.reply_text("🔍 جاري فحص البطاقة...")
        
        # Check the card
        result = await self.check_card(card_data)
        
        # Store result
        user_id = update.effective_user.id
        if user_id not in self.check_results:
            self.check_results[user_id] = []
        self.check_results[user_id].append(result)
        
        # Format result message
        status_emoji = "✅" if result['status'] == 'LIVE' else "❌"
        result_text = f"""
🔍 **نتيجة فحص البطاقة:**

**البطاقة:** `{result['card']}`
**الحالة:** {status_emoji} {result['status']}
**الرسالة:** {result['message']}
**البنك:** {result['bank']}
**البلد:** {result['country']}
**الوقت:** {datetime.now().strftime('%H:%M:%S')}
        """
        
        await msg.edit_text(result_text, parse_mode=ParseMode.MARKDOWN)
        
    async def bin_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /bin command"""
        if not context.args:
            await update.message.reply_text("🔍 الرجاء إدخال البين: /bin [BIN]")
            return
            
        bin_input = context.args[0]
        
        if not bin_input.isdigit() or len(bin_input) < 6:
            await update.message.reply_text("❌ البين غير صحيح. يجب أن يكون 6 أرقام على الأقل.")
            return
            
        bin_code = bin_input[:6]
        
        msg = await update.message.reply_text("🔍 جاري جمع معلومات البين...")
        
        try:
            # Get BIN information from API
            response = requests.get(f"https://adyen-enc-and-bin-info.herokuapp.com/bin/{bin_code}")
            
            if response.status_code == 200:
                bin_data = response.json()
                
                if bin_data.get('result', False):
                    data = bin_data['data']
                    bin_info = f"""
🔍 **معلومات البين:**

**البين:** `{data['bin']}` ✅
**البنك:** {data['bank']}
**النوع:** {data['type']}
**المستوى:** {data['level']}
**الشركة:** {data['vendor']}
**البلد:** {data['country']} {data['countryInfo']['emoji']}
**رمز البلد:** {data['countryInfo']['code']}
**رمز الاتصال:** {data['countryInfo']['dialCode']}
**تم الفحص بواسطة:** {update.effective_user.first_name}
                    """
                    
                    await msg.edit_text(bin_info, parse_mode=ParseMode.MARKDOWN)
                else:
                    await msg.edit_text("❌ لم يتم العثور على معلومات البين.")
            else:
                await msg.edit_text("❌ خطأ في الحصول على معلومات البين.")
                
        except Exception as e:
            await msg.edit_text(f"❌ خطأ: {str(e)}")
            
    async def gen_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /gen command"""
        if not context.args:
            await update.message.reply_text("🔧 الرجاء إدخال البين: /gen [BIN]")
            return
            
        bin_input = context.args[0]
        
        if not bin_input.isdigit() or len(bin_input) < 6:
            await update.message.reply_text("❌ البين غير صحيح. يجب أن يكون 6 أرقام على الأقل.")
            return
            
        bin_code = bin_input[:6]
        
        # Check if BIN is banned
        if bin_code in self.banned_bins:
            await update.message.reply_text("❌ هذا البين محظور!")
            return
            
        msg = await update.message.reply_text("🔧 جاري توليد البطاقات...")
        
        try:
            # Get BIN information
            response = requests.get(f"https://adyen-enc-and-bin-info.herokuapp.com/bin/{bin_code}")
            
            if response.status_code == 200:
                bin_data = response.json()
                
                if bin_data.get('result', False):
                    data = bin_data['data']
                    
                    # Generate cards
                    generated_cards = []
                    for i in range(10):  # Generate 10 cards
                        # Generate random card number
                        remaining_digits = 16 - len(bin_code)
                        card_number = bin_code + ''.join([str(random.randint(0, 9)) for _ in range(remaining_digits)])
                        
                        # Generate random month and year
                        month = str(random.randint(1, 12)).zfill(2)
                        year = str(random.randint(2025, 2030))
                        cvv = str(random.randint(100, 999))
                        
                        card = f"{card_number}|{month}|{year}|{cvv}"
                        generated_cards.append(card)
                    
                    cards_text = "\n".join(generated_cards)
                    
                    gen_info = f"""
🔧 **توليد البطاقات:**

**البين:** `{bin_code}` ✅
**البنك:** {data['bank']}
**البلد:** {data['country']} {data['countryInfo']['emoji']}
**النوع:** {data['type']}
**المستوى:** {data['level']}

**البطاقات المولدة:**
```
{cards_text}
```
                    """
                    
                    keyboard = [[InlineKeyboardButton("🔄 توليد مرة أخرى", callback_data=f"gen_{bin_code}")]]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    
                    await msg.edit_text(gen_info, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
                else:
                    await msg.edit_text("❌ البين غير صحيح.")
            else:
                await msg.edit_text("❌ خطأ في الحصول على معلومات البين.")
                
        except Exception as e:
            await msg.edit_text(f"❌ خطأ: {str(e)}")
            
    async def stripe_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /stripe command"""
        if len(context.args) < 4:
            await update.message.reply_text("💳 الرجاء إدخال البيانات: /stripe [CC|MM|YYYY|CVV] [SK] [AMOUNT] [CURRENCY]")
            return
            
        card_input = context.args[0]
        sk = context.args[1]
        amount = context.args[2]
        currency = context.args[3] if len(context.args) > 3 else "usd"
        
        card_data = self.parse_card(card_input)
        
        if not card_data:
            await update.message.reply_text("❌ تنسيق البطاقة غير صحيح.")
            return
            
        msg = await update.message.reply_text("💳 جاري فحص Stripe...")
        
        try:
            # Simulate Stripe check
            start_time = time.time()
            
            # Random result for demonstration
            results = [
                {"status": "HIT", "message": "Payment Succeeded ✅", "amount": amount, "currency": currency},
                {"status": "LIVE", "message": "Insufficient Funds", "amount": amount, "currency": currency},
                {"status": "DEAD", "message": "Card Declined", "amount": amount, "currency": currency}
            ]
            
            result = random.choice(results)
            end_time = time.time()
            total_time = end_time - start_time
            
            # Format result
            status_emoji = "✅" if result['status'] in ['HIT', 'LIVE'] else "❌"
            stripe_result = f"""
💳 **نتيجة فحص Stripe:**

**البطاقة:** `{card_data['cc']}|{card_data['mm']}|{card_data['yyyy']}|{card_data['cvv']}`
**الحالة:** {status_emoji} {result['status']}
**الرسالة:** {result['message']}
**المبلغ:** {result['amount']} {result['currency'].upper()}
**الوقت:** {total_time:.2f}s
            """
            
            await msg.edit_text(stripe_result, parse_mode=ParseMode.MARKDOWN)
            
        except Exception as e:
            await msg.edit_text(f"❌ خطأ: {str(e)}")
            
    async def valid_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /valid command"""
        user_id = update.effective_user.id
        
        if user_id not in self.check_results:
            await update.message.reply_text("📋 لا توجد نتائج فحص لك.")
            return
            
        valid_cards = [r for r in self.check_results[user_id] if r['status'] == 'LIVE']
        
        if not valid_cards:
            await update.message.reply_text("📋 لا توجد بطاقات صالحة.")
            return
            
        valid_text = "📋 **البطاقات الصالحة:**\n\n"
        for i, card in enumerate(valid_cards[:10], 1):  # Show first 10
            valid_text += f"**{i}.** `{card['card']}` - {card['bank']}\n"
            
        if len(valid_cards) > 10:
            valid_text += f"\n... و {len(valid_cards) - 10} بطاقة أخرى"
            
        await update.message.reply_text(valid_text, parse_mode=ParseMode.MARKDOWN)
        
    async def dead_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /dead command"""
        user_id = update.effective_user.id
        
        if user_id not in self.check_results:
            await update.message.reply_text("📋 لا توجد نتائج فحص لك.")
            return
            
        dead_cards = [r for r in self.check_results[user_id] if r['status'] == 'DEAD']
        
        if not dead_cards:
            await update.message.reply_text("📋 لا توجد بطاقات ميتة.")
            return
            
        dead_text = "📋 **البطاقات الميتة:**\n\n"
        for i, card in enumerate(dead_cards[:10], 1):  # Show first 10
            dead_text += f"**{i}.** `{card['card']}` - {card['message']}\n"
            
        if len(dead_cards) > 10:
            dead_text += f"\n... و {len(dead_cards) - 10} بطاقة أخرى"
            
        await update.message.reply_text(dead_text, parse_mode=ParseMode.MARKDOWN)
        
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /stats command"""
        user_id = update.effective_user.id
        
        if user_id not in self.check_results:
            await update.message.reply_text("📊 لا توجد إحصائيات لك.")
            return
            
        results = self.check_results[user_id]
        total = len(results)
        live = len([r for r in results if r['status'] == 'LIVE'])
        dead = len([r for r in results if r['status'] == 'DEAD'])
        
        stats_text = f"""
📊 **إحصائيات الفحص:**

**إجمالي البطاقات:** {total}
**البطاقات الصالحة:** {live} ✅
**البطاقات الميتة:** {dead} ❌
**نسبة النجاح:** {(live/total*100):.1f}%
        """
        
        await update.message.reply_text(stats_text, parse_mode=ParseMode.MARKDOWN)
        
    async def clear_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /clear command"""
        user_id = update.effective_user.id
        
        if user_id in self.check_results:
            del self.check_results[user_id]
            await update.message.reply_text("🗑️ تم مسح جميع النتائج.")
        else:
            await update.message.reply_text("📋 لا توجد نتائج للمسح.")
            
    async def admin_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /admin command"""
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
        
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle button callbacks"""
        query = update.callback_query
        await query.answer()
        
        if query.data == "check_cards":
            await query.edit_message_text("🔍 استخدم /check [CC|MM|YYYY|CVV] لفحص بطاقة")
        elif query.data == "stripe_check":
            await query.edit_message_text("💳 استخدم /stripe [CC|MM|YYYY|CVV] [SK] [AMOUNT] لفحص Stripe")
        elif query.data == "stats":
            await self.stats_command(update, context)
        elif query.data.startswith("gen_"):
            bin_code = query.data.split("_")[1]
            context.args = [bin_code]
            await self.gen_command(update, context)
        elif query.data == "admin_stats":
            await query.edit_message_text("📊 إحصائيات المدير قيد التطوير...")
        elif query.data == "admin_broadcast":
            await query.edit_message_text("📢 استخدم /broadcast [الرسالة] لإرسال رسالة للجميع")
        elif query.data == "admin_settings":
            await query.edit_message_text("⚙️ إعدادات المدير قيد التطوير...")
            
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
        
        # Handle different message types
        if message.startswith('/'):
            return  # Commands are handled separately
            
        # Echo message for testing
        if user.id == self.admin_id:
            await update.message.reply_text(f"👑 رسالة المدير: {message}")
        else:
            await update.message.reply_text(f"📝 رسالتك: {message}")
            
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
        application.add_handler(CommandHandler("check", self.check_command))
        application.add_handler(CommandHandler("bin", self.bin_command))
        application.add_handler(CommandHandler("gen", self.gen_command))
        application.add_handler(CommandHandler("stripe", self.stripe_command))
        application.add_handler(CommandHandler("valid", self.valid_command))
        application.add_handler(CommandHandler("dead", self.dead_command))
        application.add_handler(CommandHandler("stats", self.stats_command))
        application.add_handler(CommandHandler("clear", self.clear_command))
        application.add_handler(CommandHandler("admin", self.admin_command))
        
        # Add callback query handler
        application.add_handler(CallbackQueryHandler(self.button_callback))
        
        # Add message handler
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        # Add error handler
        application.add_error_handler(self.error_handler)
        
        # Start the bot
        print("🤖 Super Checker Bot is starting...")
        print(f"🔑 Token: {self.bot_token[:10]}...")
        print(f"👑 Admin ID: {self.admin_id}")
        print("🚀 Bot is running...")
        
        application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    bot = SuperCheckerBot()
    bot.run()