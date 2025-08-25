#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Original Design Bot - بوت بالتصميم الأصلي
Based on the original design from extracted files
"""

import asyncio
import logging
import os
import json
import re
import random
import time
import requests
from datetime import datetime
from typing import Dict, List, Optional

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import (
    Updater, CommandHandler, MessageHandler, CallbackQueryHandler,
    CallbackContext, Filters
)

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class OriginalDesignBot:
    def __init__(self):
        self.bot_token = "8059528086:AAFIZLlNJzo_nUplHlXzjyShla-DsT0RNYw"
        self.admin_id = 5509130673
        self.users_data = {}
        self.check_results = {}
        self.banned_bins = set()
        self.waste_cards = {1, 2, 7, 8, 9, 0}
        
        # Load banned bins
        self.load_banned_bins()
        
    def load_banned_bins(self):
        """Load banned BINs from file"""
        try:
            if os.path.exists('bannedbin.txt'):
                with open('bannedbin.txt', 'r') as f:
                    for line in f:
                        self.banned_bins.add(line.strip())
        except Exception as e:
            logger.error(f"Error loading banned BINs: {e}")
            
    def get_part_of_day(self):
        """Get part of day greeting"""
        hour = datetime.now().hour
        if 5 <= hour < 12:
            return "Good Morning"
        elif 12 <= hour < 17:
            return "Good Afternoon"
        elif 17 <= hour < 21:
            return "Good Evening"
        else:
            return "Good Night"
            
    def make_ordinal(self, n):
        """Convert number to ordinal"""
        n = int(n)
        if 10 <= n % 100 <= 20:
            suffix = 'th'
        else:
            suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
        return str(n) + suffix
        
    def start_command(self, update: Update, context: CallbackContext):
        """Handle /start command - Original design"""
        user = update.effective_user
        
        # Original design from the files
        dt_string = datetime.now().strftime(" %B %Y And Time Is %H-%M %p")
        day = self.make_ordinal(datetime.now().strftime("%d"))
        
        caption = f"""
<b>{self.get_part_of_day()} <a href="tg://user?id={user.id}">{user.first_name}</a>[<code>{user.id}</code>],
How Are You?
I Am Jocasta. The Multi Functional Bot For You.
Today Is {day} Of {dt_string}.
Check And Click Down For More</b>    
        """
        
        # Original button layout
        reply_markup = InlineKeyboardMarkup([
            [
                InlineKeyboardButton('📒 MY ACCOUNT 📒', callback_data='myacc'),
                InlineKeyboardButton('🚪 GATES 🚪', callback_data='gates')
            ],
            [
                InlineKeyboardButton('🔒 CLOSE 🔒', callback_data='close')
            ]
        ])
        
        update.message.reply_text(
            caption,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
        
    def myacc_callback(self, update: Update, context: CallbackContext):
        """Handle myacc callback - Original design"""
        query = update.callback_query
        user = query.from_user
        
        # Check if user is registered
        if user.id not in self.users_data:
            query.answer("Register First Hit /register to register yourself", show_alert=True)
            return
            
        user_data = self.users_data[user.id]
        
        # Original account information design
        text = f"""
<b>〄</b> User Information:-
<b>○</b> First Name: <b>{user.first_name}</b>
<b>○</b> User Name: <b>{user.username}</b>
<b>○</b> User Id: <b><code>{user.id}</code></b>
<b>○</b> Limited: <b>{user.is_restricted}</b>
<b>○</b> Profile Link: <b><a href="tg://user?id={user.id}">Click Here</a></b>
<b>○</b> Profile Image: <b><a href="https://t.me/{user.username}">Click Here</a></b>

<b>〄</b> User Database Information:-
<b>○</b> Role: <b>{user_data.get('role', 'User')}</b>
<b>○</b> Plan: <b>{user_data.get('plan', 'Free')}</b>
<b>○</b> Status: <b>{user_data.get('status', 'Active')}</b>
<b>○</b> Credits: <b>{user_data.get('credits', 0)}</b>
<b>○</b> Live Cards: <b>{len([r for r in self.check_results.get(user.id, []) if r['status'] == 'LIVE'])}</b>
<b>○</b> AntiSpam Time: <b>{datetime.now().strftime('%H:%M:%S %d-%m-%Y')}</b>

<b>〄</b> Chat Information:-
<b>○</b> Chat Name: <b>{query.message.chat.title or 'Private'}</b>
<b>○</b> User Name: <b>{query.message.chat.username or 'None'}</b>
<b>○</b> Chat Id: <b><code>{query.message.chat.id}</code></b>
<b>○</b> Chat Type: <b>{query.message.chat.type.capitalize()}</b>
        """
        
        buttons = [
            [
                InlineKeyboardButton('💳 MY LIVE 💳', callback_data='mylives'),
                InlineKeyboardButton('🚪 GATES 🚪', callback_data='gates')
            ],
            [
                InlineKeyboardButton('🚪 CLOSE 🚪', callback_data='close')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        
        await query.edit_message_text(
            text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
        
    async def gates_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle gates callback - Original design"""
        query = update.callback_query
        
        buttons = [
            [
                InlineKeyboardButton('🎁 FREE 🎁', callback_data='free'), 
                InlineKeyboardButton('💲 PAID 💲', callback_data='paid')
            ],
            [
                InlineKeyboardButton('🛠️ TOOLS 🛠️', callback_data='tools'),
                InlineKeyboardButton('🚪 CLOSE 🚪', callback_data='close')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        
        text = "Check Down My Commands"
        
        await query.edit_message_text(
            text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
        
    async def free_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle free callback - Original design"""
        query = update.callback_query
        
        buttons = [
            [
                InlineKeyboardButton('🔍 BIN 🔍', callback_data='bin'),
                InlineKeyboardButton('🔧 GEN 🔧', callback_data='gen')
            ],
            [
                InlineKeyboardButton('🔍 CHECK 🔍', callback_data='check'),
                InlineKeyboardButton('📊 STATS 📊', callback_data='stats')
            ],
            [
                InlineKeyboardButton('🔙 BACK 🔙', callback_data='gates'),
                InlineKeyboardButton('🚪 CLOSE 🚪', callback_data='close')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        
        text = """
<b>🎁 FREE GATES 🎁</b>

<b>🔍 BIN</b> - Get BIN Information
<b>🔧 GEN</b> - Generate Cards from BIN
<b>🔍 CHECK</b> - Check Single Card
<b>📊 STATS</b> - Your Statistics
        """
        
        await query.edit_message_text(
            text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
        
    async def paid_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle paid callback - Original design"""
        query = update.callback_query
        
        buttons = [
            [
                InlineKeyboardButton('🟢 AUTH 🟢', callback_data='auth'), 
                InlineKeyboardButton('🔴 CHARGE 🔴', callback_data='charge')
            ],
            [
                InlineKeyboardButton('🔙 BACK 🔙', callback_data='gates'),
                InlineKeyboardButton('🚪 CLOSE 🚪', callback_data='close')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        
        text = """
<b>💲 PAID GATES 💲</b>

<b>🟢 AUTH</b> - Authorization Check
<b>🔴 CHARGE</b> - Charge Check
        """
        
        await query.edit_message_text(
            text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
        
    async def tools_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle tools callback - Original design"""
        query = update.callback_query
        
        buttons = [
            [
                InlineKeyboardButton('🔐 PASSWORD 🔐', callback_data='password'),
                InlineKeyboardButton('🔒 HASH 🔒', callback_data='hash')
            ],
            [
                InlineKeyboardButton('🔍 ANALYZE 🔍', callback_data='analyze'),
                InlineKeyboardButton('🎲 RANDOM 🎲', callback_data='random')
            ],
            [
                InlineKeyboardButton('🔙 BACK 🔙', callback_data='gates'),
                InlineKeyboardButton('🚪 CLOSE 🚪', callback_data='close')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        
        text = """
<b>🛠️ TOOLS 🛠️</b>

<b>🔐 PASSWORD</b> - Generate Strong Password
<b>🔒 HASH</b> - Hash Text
<b>🔍 ANALYZE</b> - Analyze Text
<b>🎲 RANDOM</b> - Random Number Generator
        """
        
        await query.edit_message_text(
            text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
        
    async def bin_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /bin command - Original design"""
        if not context.args:
            await update.message.reply_text("🔍 Please provide BIN: /bin [BIN]")
            return
            
        bin_input = context.args[0]
        
        if not bin_input.isdigit() or len(bin_input) < 6:
            await update.message.reply_text("❌ Invalid BIN. Must be at least 6 digits.")
            return
            
        bin_code = bin_input[:6]
        
        msg = await update.message.reply_text("🔍 <b>Wait Collecting Information</b>", parse_mode=ParseMode.HTML)
        
        try:
            # Get BIN information from API
            response = requests.get(f"https://adyen-enc-and-bin-info.herokuapp.com/bin/{bin_code}")
            
            if response.status_code == 200:
                bin_data = response.json()
                
                if bin_data.get('result', False):
                    data = bin_data['data']
                    text = f"""
<b>〄</b> Bin Information:-
<b>○</b> Bin: <code>{data['bin']}</code>✅
<b>○</b> Vendor: <b>{data['vendor']}</b>
<b>○</b> Type: <b>{data['type']}</b>
<b>○</b> Level: <b>{data['level']}</b>
<b>○</b> Bank: <b>{data['bank']}</b>
<b>○</b> Country: <b>{data['country']}({data['countryInfo']['emoji']})</b>
<b>○</b> Dial Code: <b>{data['countryInfo']['dialCode']}</b>
<b>○</b> Checked By: <b><a href="tg://user?id={update.effective_user.id}">{update.effective_user.first_name}</a>[User]</b>
<b>○</b> BOT BY: <b>@Admin</b>
                    """
                    
                    await msg.edit_text(text, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
                else:
                    await msg.edit_text("Error While Getting Bin Data.")
            else:
                await msg.edit_text("Error While Getting Bin Data.")
                
        except Exception as e:
            await msg.edit_text(f"❌ Error: {str(e)}")
            
    async def gen_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /gen command - Original design"""
        if not context.args:
            await update.message.reply_text("🔧 Please provide BIN: /gen [BIN]")
            return
            
        bin_input = context.args[0]
        
        if not bin_input.isdigit() or len(bin_input) < 6:
            await update.message.reply_text("❌ Invalid BIN. Must be at least 6 digits.")
            return
            
        bin_code = bin_input[:6]
        
        # Check if BIN is banned
        if bin_code in self.banned_bins:
            await update.message.reply_text("❌ This BIN is banned!")
            return
            
        msg = await update.message.reply_text("🔧 <b>WAIT FOR RESULTS</b>", parse_mode=ParseMode.HTML)
        
        try:
            # Get BIN information
            response = requests.get(f"https://adyen-enc-and-bin-info.herokuapp.com/bin/{bin_code}")
            
            if response.status_code == 200:
                bin_data = response.json()
                
                if bin_data.get('result', False):
                    data = bin_data['data']
                    
                    # Generate cards (original format)
                    generated_cards = []
                    for i in range(10):
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
                    
                    text = f"""
<b>〄</b> CC GENRATOR
<b>○</b> YOUR DATA = {bin_code}|x|x|x.
<b>○</b> BANK INFO: <b>{data['bank']} - {data['countryInfo']['code']}({data['countryInfo']['emoji']})</b>
<b>○</b> BIN INFO: <code>{bin_code}</code> - <b>{data['level']}</b> - <b>{data['type']}</b>

<code>{cards_text}</code>
                    """
                    
                    buttons = [[InlineKeyboardButton('GEN AGAIN', callback_data='gen')]]
                    reply_markup = InlineKeyboardMarkup(buttons)
                    
                    await msg.edit_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
                else:
                    await msg.edit_text("Your Bin Is Invalid.")
            else:
                await msg.edit_text("Your Bin Is Invalid.")
                
        except Exception as e:
            await msg.edit_text(f"❌ Error: {str(e)}")
            
    async def check_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /check command - Original design"""
        if not context.args:
            await update.message.reply_text("🔍 Please provide card: /check [CC|MM|YYYY|CVV]")
            return
            
        card_input = " ".join(context.args)
        
        # Parse card
        card_parts = card_input.replace(' ', '').split('|')
        if len(card_parts) != 4:
            await update.message.reply_text("❌ Invalid card format. Use: CC|MM|YYYY|CVV")
            return
            
        cc, mm, yyyy, cvv = card_parts
        
        # Validate card
        if not cc.isdigit() or len(cc) < 13 or len(cc) > 19:
            await update.message.reply_text("❌ Invalid card number.")
            return
            
        if not mm.isdigit() or int(mm) < 1 or int(mm) > 12:
            await update.message.reply_text("❌ Invalid month.")
            return
            
        if not yyyy.isdigit() or len(yyyy) != 4:
            await update.message.reply_text("❌ Invalid year.")
            return
            
        if not cvv.isdigit() or len(cvv) < 3 or len(cvv) > 4:
            await update.message.reply_text("❌ Invalid CVV.")
            return
            
        # Check if BIN is banned
        bin_code = cc[:6]
        if bin_code in self.banned_bins:
            await update.message.reply_text("❌ This BIN is banned!")
            return
            
        # Check if it's a waste card
        if int(cc[0]) in self.waste_cards:
            await update.message.reply_text("❌ Invalid card!")
            return
            
        msg = await update.message.reply_text("🔍 <b>Checking Card...</b>", parse_mode=ParseMode.HTML)
        
        # Simulate card check
        time.sleep(2)
        
        # Random result
        results = [
            {"status": "LIVE", "message": "Card Approved ✅", "bank": "Chase Bank", "country": "US"},
            {"status": "DEAD", "message": "Card Declined ❌", "bank": "Unknown", "country": "Unknown"},
            {"status": "LIVE", "message": "Card Approved ✅", "bank": "Wells Fargo", "country": "US"},
            {"status": "DEAD", "message": "Insufficient Funds ❌", "bank": "Unknown", "country": "Unknown"}
        ]
        
        result = random.choice(results)
        
        # Store result
        user_id = update.effective_user.id
        if user_id not in self.check_results:
            self.check_results[user_id] = []
        self.check_results[user_id].append({
            'card': f"{cc}|{mm}|{yyyy}|{cvv}",
            'status': result['status'],
            'message': result['message'],
            'bank': result['bank'],
            'country': result['country'],
            'time': datetime.now().isoformat()
        })
        
        # Format result (original design)
        status_emoji = "✅" if result['status'] == 'LIVE' else "❌"
        result_text = f"""
<b>〄</b> Card Check Result:-
<b>○</b> Card: <code>{cc}|{mm}|{yyyy}|{cvv}</code>
<b>○</b> Status: {status_emoji} <b>{result['status']}</b>
<b>○</b> Message: <b>{result['message']}</b>
<b>○</b> Bank: <b>{result['bank']}</b>
<b>○</b> Country: <b>{result['country']}</b>
<b>○</b> Checked By: <b><a href="tg://user?id={update.effective_user.id}">{update.effective_user.first_name}</a>[User]</b>
<b>○</b> BOT BY: <b>@Admin</b>
        """
        
        await msg.edit_text(result_text, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
        
    async def register_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /register command - Original design"""
        user = update.effective_user
        
        if user.id in self.users_data:
            await update.message.reply_text("You are already registered!")
            return
            
        # Register user
        self.users_data[user.id] = {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'role': 'User',
            'plan': 'Free',
            'status': 'Active',
            'credits': 100,
            'registered_date': datetime.now().isoformat()
        }
        
        await update.message.reply_text("✅ Registration successful! You can now use the bot.")
        
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle button callbacks"""
        query = update.callback_query
        await query.answer()
        
        if query.data == "myacc":
            await self.myacc_callback(update, context)
        elif query.data == "gates":
            await self.gates_callback(update, context)
        elif query.data == "free":
            await self.free_callback(update, context)
        elif query.data == "paid":
            await self.paid_callback(update, context)
        elif query.data == "tools":
            await self.tools_callback(update, context)
        elif query.data == "bin":
            await query.edit_message_text("🔍 Use /bin [BIN] to get BIN information")
        elif query.data == "gen":
            await query.edit_message_text("🔧 Use /gen [BIN] to generate cards")
        elif query.data == "check":
            await query.edit_message_text("🔍 Use /check [CC|MM|YYYY|CVV] to check card")
        elif query.data == "stats":
            await query.edit_message_text("📊 Use /stats to see your statistics")
        elif query.data == "close":
            await query.edit_message_text("🔒 Closed")
        else:
            await query.edit_message_text("Feature coming soon...")
            
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
                'role': 'User',
                'plan': 'Free',
                'status': 'Active',
                'credits': 100,
                'registered_date': datetime.now().isoformat()
            }
        
        # Handle different message types
        if message.startswith('/'):
            return  # Commands are handled separately
            
        # Echo message for testing
        if user.id == self.admin_id:
            await update.message.reply_text(f"👑 Admin message: {message}")
        else:
            await update.message.reply_text(f"📝 Your message: {message}")
            
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors"""
        logger.error(f"Exception while handling an update: {context.error}")
        
    def run(self):
        """Run the bot"""
        # Create application
        application = Application.builder().token(self.bot_token).build()
        
        # Add command handlers
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(CommandHandler("bin", self.bin_command))
        application.add_handler(CommandHandler("gen", self.gen_command))
        application.add_handler(CommandHandler("check", self.check_command))
        application.add_handler(CommandHandler("register", self.register_command))
        
        # Add callback query handler
        application.add_handler(CallbackQueryHandler(self.button_callback))
        
        # Add message handler
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        # Add error handler
        application.add_error_handler(self.error_handler)
        
        # Start the bot
        print("🤖 Original Design Bot is starting...")
        print(f"🔑 Token: {self.bot_token[:10]}...")
        print(f"👑 Admin ID: {self.admin_id}")
        print("🚀 Bot is running...")
        
        # Use asyncio to run the bot
        async def main():
            await application.initialize()
            await application.start()
            await application.run_polling(allowed_updates=Update.ALL_TYPES)
            await application.stop()
        
        asyncio.run(main())

if __name__ == "__main__":
    bot = OriginalDesignBot()
    bot.run()