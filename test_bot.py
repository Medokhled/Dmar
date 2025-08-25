#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Bot - بوت تجريبي بسيط
Simple test bot to verify functionality
"""

import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, CallbackContext, Filters

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

class TestBot:
    def __init__(self):
        self.bot_token = "8059528086:AAFIZLlNJzo_nUplHlXzjyShla-DsT0RNYw"
        self.admin_id = 5509130673
        
    def start_command(self, update: Update, context: CallbackContext):
        """Handle /start command"""
        user = update.effective_user
        
        welcome_text = f"""
<b>مرحباً {user.first_name}!</b>

أنا بوت تجريبي لاختبار الوظائف.

<b>الأوامر المتاحة:</b>
/start - هذه الرسالة
/bin [BIN] - معلومات البين
/test - اختبار بسيط

<b>مثال:</b>
/bin 453264
        """
        
        keyboard = [
            [InlineKeyboardButton("🔍 اختبار البين", callback_data="test_bin")],
            [InlineKeyboardButton("📊 الإحصائيات", callback_data="stats")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        update.message.reply_text(
            welcome_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
        
    def bin_command(self, update: Update, context: CallbackContext):
        """Handle /bin command"""
        if not context.args:
            update.message.reply_text("🔍 الرجاء إدخال البين: /bin [BIN]")
            return
            
        bin_input = context.args[0]
        
        if not bin_input.isdigit() or len(bin_input) < 6:
            update.message.reply_text("❌ البين غير صحيح. يجب أن يكون 6 أرقام على الأقل.")
            return
            
        bin_code = bin_input[:6]
        
        msg = update.message.reply_text("🔍 جاري جمع معلومات البين...")
        
        try:
            # Get BIN information from API
            response = requests.get(f"https://adyen-enc-and-bin-info.herokuapp.com/bin/{bin_code}")
            
            if response.status_code == 200:
                bin_data = response.json()
                
                if bin_data.get('result', False):
                    data = bin_data['data']
                    text = f"""
<b>〄</b> معلومات البين:-
<b>○</b> البين: <code>{data['bin']}</code>✅
<b>○</b> الشركة: <b>{data['vendor']}</b>
<b>○</b> النوع: <b>{data['type']}</b>
<b>○</b> المستوى: <b>{data['level']}</b>
<b>○</b> البنك: <b>{data['bank']}</b>
<b>○</b> البلد: <b>{data['country']}({data['countryInfo']['emoji']})</b>
<b>○</b> رمز الاتصال: <b>{data['countryInfo']['dialCode']}</b>
<b>○</b> تم الفحص بواسطة: <b>{update.effective_user.first_name}</b>
                    """
                    
                    msg.edit_text(text, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
                else:
                    msg.edit_text("❌ لم يتم العثور على معلومات البين.")
            else:
                msg.edit_text("❌ خطأ في الحصول على معلومات البين.")
                
        except Exception as e:
            msg.edit_text(f"❌ خطأ: {str(e)}")
            
    def test_command(self, update: Update, context: CallbackContext):
        """Handle /test command"""
        update.message.reply_text("✅ البوت يعمل بشكل صحيح!")
        
    def button_callback(self, update: Update, context: CallbackContext):
        """Handle button callbacks"""
        query = update.callback_query
        query.answer()
        
        if query.data == "test_bin":
            query.edit_message_text("🔍 استخدم /bin [BIN] لاختبار معلومات البين\nمثال: /bin 453264")
        elif query.data == "stats":
            query.edit_message_text("📊 البوت يعمل بشكل طبيعي!")
            
    def error_handler(self, update: Update, context: CallbackContext):
        """Handle errors"""
        logger.error(f"Exception while handling an update: {context.error}")
        
    def run(self):
        """Run the bot"""
        # Create updater
        updater = Updater(self.bot_token, use_context=True)
        dispatcher = updater.dispatcher
        
        # Add command handlers
        dispatcher.add_handler(CommandHandler("start", self.start_command))
        dispatcher.add_handler(CommandHandler("bin", self.bin_command))
        dispatcher.add_handler(CommandHandler("test", self.test_command))
        
        # Add callback query handler
        dispatcher.add_handler(CallbackQueryHandler(self.button_callback))
        
        # Add error handler
        dispatcher.add_error_handler(self.error_handler)
        
        # Start the bot
        print("🤖 Test Bot is starting...")
        print(f"🔑 Token: {self.bot_token[:10]}...")
        print(f"👑 Admin ID: {self.admin_id}")
        print("🚀 Bot is running...")
        
        updater.start_polling()
        updater.idle()

if __name__ == "__main__":
    bot = TestBot()
    bot.run()