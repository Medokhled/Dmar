#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Original Bot - البوت الأصلي
Exact copy from extracted files
"""

import logging
import os
import time
import requests
import json
import random
import string
import re
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Configure logging
logging.basicConfig(level=logging.INFO)

# Import config
from original_config import BOT_TOKEN, API_ID, API_HASH, BOT_USERNAME

# Initialize bot
bot = Client(
    'bot',
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="plugins"),
    parse_mode="html"
)

# Original functions from values.py
def make_ordinal(n):
    n = int(n)
    suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    return str(n) + suffix

def get_part_of_day():
    h = datetime.now().hour
    if h < 12:
        return "Good Morning <b>⛅</b>"
    elif h >= 11 and h < 16:
        return "Good Afternoon <b>🌣</b>"
    elif h >= 17 and h < 19:
        return "Good Evening <b>🌅</b>"
    elif h >= 19 and h < 24:
        return "Good Night <b>🌃</b> "
    else:
        return "Hello"

def lista(dets):
    arrays = re.findall(r'[0-9]+', dets)
    return arrays 

def get_email(): 
    generated_email = str(''.join(random.choices(string.ascii_uppercase + string.digits, k = 8))) + '@gmail.com'
    return generated_email.lower()

def get_username():  
    generated_username = str(''.join(random.choices(string.ascii_uppercase + string.digits, k = 8)))
    return generated_username.capitalize()

# Original start command from start.py
REPLY_MARKUP = InlineKeyboardMarkup([
    [
        InlineKeyboardButton('📒 MY ACCOUNT 📒', callback_data='myacc'),
        InlineKeyboardButton('🚪 GATES 🚪', callback_data='gates')
    ],
    [
        InlineKeyboardButton('🔒 CLOSE 🔒', callback_data='close')
    ]
])

@bot.on_message(filters.command(['start', f'start@{BOT_USERNAME}'], prefixes=['.','/','!'], case_sensitive=False) & filters.text)
async def start(Client, message):
    await Client.send_chat_action(message.chat.id, "typing")
    if message.reply_to_message is not None:
        message.text = message.reply_to_message.text
    dt_string = datetime.now().strftime(" %B %Y And Time Is %H-%M %p")
    day = make_ordinal(datetime.now().strftime("%d"))
    caption = f"""
<b>{get_part_of_day()} <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>[<code>{message.from_user.id}</code>],
How Are You?
I Am Jocasta. The Multi Functional Bot For You.
Today Is {day} Of {dt_string}.
Check And Click Down For More</b>    
"""
    await Client.send_message(
        chat_id=message.chat.id,
        text=caption,
        disable_web_page_preview=True,
        reply_to_message_id=message.message_id,
        reply_markup=REPLY_MARKUP
    )

# Original bin command from bin.py
@bot.on_message(filters.command('bin', prefixes=['.','/','!'], case_sensitive=False) & filters.text)
async def bin_command(Client, message):
    try:
        if message.reply_to_message is not None:
            message.text = message.reply_to_message.text
        msg = await message.reply_text(text="<b>Wait Collecting Information</b>", reply_to_message_id=message.message_id)
        await Client.send_chat_action(message.chat.id, "typing")
        
        try:
            input_text = lista(message.text)
            bin_code = input_text[0]
        except Exception as e:
            await msg.edit_text("Your Bin Is Empty.")
            return
        
        if len(bin_code) < 6:
            await msg.edit_text("Bin Is To Short")
            return
        
        req = requests.get("https://adyen-enc-and-bin-info.herokuapp.com/bin/" + bin_code)
        if req.status_code == 200:
            jsontext = req.json()
            text = f"""
<b>〄</b> Bin Information:-
<b>○</b> Bin: <code>{jsontext['data']['bin']}</code>✅
<b>○</b> Vendor: <b>{jsontext['data']['vendor']}</b>
<b>○</b> Type: <b>{jsontext['data']['type']}</b>
<b>○</b> Level: <b>{jsontext['data']['level']}</b>
<b>○</b> Bank: <b>{jsontext['data']['bank']}</b>
<b>○</b> Country: <b>{jsontext['data']['country']}({jsontext['data']['countryInfo']['emoji']})</b>
<b>○</b> Dial Code: <b>{jsontext['data']['countryInfo']['dialCode']}</b>
<b>○</b> Checked By: <b><a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>[User]</b>
<b>○</b> BOT BY: <b>@Admin</b>
            """
            await msg.edit_text(text, disable_web_page_preview=True)
        else:
            await msg.edit_text("Error While Getting Bin Data.")
    except Exception as e:
        print(e)

# Original gen command from gen.py
@bot.on_message(filters.command(["gen", "make"], prefixes=[".", "/", "!"], case_sensitive=False) & filters.text)
async def gen_command(Client, message):
    try:
        if message.reply_to_message is not None:
            message.text = message.reply_to_message.text
        text = f"""<b>WAIT FOR RESULTS</b>"""
        msg = await message.reply_text(text=text, reply_to_message_id=message.message_id)
        await Client.send_chat_action(message.chat.id, "typing")
        
        input_numbers = re.findall(r"[0-9]+", message.text)
        if len(input_numbers) == 0:
            await msg.edit_text("Your Bin Is Empty")
            return
        
        if len(input_numbers) == 1:
            cc = input_numbers[0]
            mes = 'x'
            ano = 'x'
            cvv = 'x'
        elif len(input_numbers[0]) < 6 or len(input_numbers[0]) > 16:
            await msg.edit_text("Your Bin Is Incorrect")
            return
        elif len(input_numbers) == 2:
            cc = input_numbers[0]
            mes = input_numbers[1]
            ano = 'x'
            cvv = 'x'
        elif len(input_numbers) == 3:
            cc = input_numbers[0]
            mes = input_numbers[1]
            ano = input_numbers[2]
            cvv = 'x'
        elif len(input_numbers) == 4:
            cc = input_numbers[0]
            mes = input_numbers[1]
            ano = input_numbers[2]
            cvv = input_numbers[3]
        else:
            if len(cc) > 15:
                await msg.edit_text("Your Bin Is Invalid.")
                return
        
        bin_code = cc[:6]
        res = requests.get("https://adyen-enc-and-bin-info.herokuapp.com/bin/" + bin_code)
        if res.status_code != requests.codes.ok or json.loads(res.text)['result'] == False:
            await msg.edit_text("Your Bin Is Invalid.")
            return
        
        bin_data = json.loads(res.text)
        
        # Generate cards (simplified version)
        generated_cards = []
        for i in range(10):
            remaining_digits = 16 - len(bin_code)
            card_number = bin_code + ''.join([str(random.randint(0, 9)) for _ in range(remaining_digits)])
            month = str(random.randint(1, 12)).zfill(2)
            year = str(random.randint(2025, 2030))
            cvv_gen = str(random.randint(100, 999))
            card = f"{card_number}|{month}|{year}|{cvv_gen}"
            generated_cards.append(card)
        
        cards_text = '\n'.join(generated_cards)
        
        text = f"""
<b>〄</b> CC GENRATOR
<b>○</b> YOUR DATA = {cc}|{mes}|{ano}|{cvv}.
<b>○</b> BANK INFO: <b>{bin_data['data']['bank']} - {bin_data['data']['countryInfo']['code']}({bin_data['data']['countryInfo']['emoji']})</b>
<b>○</b> BIN INFO: <code>{bin_code}</code> - <b>{bin_data['data']['level']}</b> - <b>{bin_data['data']['type']}</b>

<code>{cards_text}</code>
        """
        
        buttons = [[InlineKeyboardButton('GEN AGAIN', callback_data='gen')]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await msg.edit_text(text, reply_markup=reply_markup)
        
    except Exception as e:
        print(e)

# Callback handlers
@bot.on_callback_query()
async def callback_handler(Client, callback_query):
    if callback_query.data == "myacc":
        user = callback_query.from_user
        text = f"""
<b>〄</b> User Information:-
<b>○</b> First Name: <b>{user.first_name}</b>
<b>○</b> User Name: <b>{user.username}</b>
<b>○</b> User Id: <b><code>{user.id}</code></b>
<b>○</b> Limited: <b>{user.is_restricted}</b>
<b>○</b> Profile Link: <b><a href="tg://user?id={user.id}">Click Here</a></b>
<b>○</b> Profile Image: <b><a href="https://t.me/{user.username}">Click Here</a></b>

<b>〄</b> User Database Information:-
<b>○</b> Role: <b>User</b>
<b>○</b> Plan: <b>Free</b>
<b>○</b> Status: <b>Active</b>
<b>○</b> Credits: <b>100</b>
<b>○</b> Live Cards: <b>0</b>
<b>○</b> AntiSpam Time: <b>{datetime.now().strftime('%H:%M:%S %d-%m-%Y')}</b>

<b>〄</b> Chat Information:-
<b>○</b> Chat Name: <b>{callback_query.message.chat.title or 'Private'}</b>
<b>○</b> User Name: <b>{callback_query.message.chat.username or 'None'}</b>
<b>○</b> Chat Id: <b><code>{callback_query.message.chat.id}</code></b>
<b>○</b> Chat Type: <b>{callback_query.message.chat.type.capitalize()}</b>
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
        
        await callback_query.edit_message_text(
            text,
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )
    
    elif callback_query.data == "gates":
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
        
        await callback_query.edit_message_text(
            text,
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )
    
    elif callback_query.data == "free":
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
        
        await callback_query.edit_message_text(
            text,
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )
    
    elif callback_query.data == "close":
        await callback_query.edit_message_text("🔒 Closed")
    
    elif callback_query.data == "gen":
        await callback_query.answer("Use /gen [BIN] to generate cards")
    
    elif callback_query.data == "bin":
        await callback_query.answer("Use /bin [BIN] to get BIN information")

# Run the bot
if __name__ == "__main__":
    print("🤖 Original Bot is starting...")
    print(f"🔑 Token: {BOT_TOKEN[:10]}...")
    print("🚀 Bot is running...")
    
    try:
        bot.run()
    except Exception as e:
        print(f"Error: {e}")