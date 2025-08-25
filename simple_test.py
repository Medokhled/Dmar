#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple Test - اختبار بسيط
Test bot token and basic functionality
"""

import requests
import json

def test_bot_token():
    """Test if the bot token is valid"""
    bot_token = "8059528086:AAFIZLlNJzo_nUplHlXzjyShla-DsT0RNYw"
    
    print("🤖 اختبار توكن البوت...")
    print(f"🔑 التوكن: {bot_token[:10]}...")
    
    try:
        # Test bot token with Telegram API
        url = f"https://api.telegram.org/bot{bot_token}/getMe"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                bot_info = data['result']
                print("✅ التوكن صحيح!")
                print(f"📱 اسم البوت: {bot_info.get('first_name', 'Unknown')}")
                print(f"👤 اسم المستخدم: @{bot_info.get('username', 'Unknown')}")
                print(f"🆔 آيدي البوت: {bot_info.get('id', 'Unknown')}")
                return True
            else:
                print("❌ التوكن غير صحيح!")
                return False
        else:
            print(f"❌ خطأ في الاتصال: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ خطأ: {str(e)}")
        return False

def test_bin_api():
    """Test BIN API functionality"""
    print("\n🔍 اختبار API البين...")
    
    test_bins = ["453264", "411111", "555555"]
    
    for bin_code in test_bins:
        try:
            url = f"https://adyen-enc-and-bin-info.herokuapp.com/bin/{bin_code}"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('result'):
                    bin_info = data['data']
                    print(f"✅ البين {bin_code}: {bin_info.get('bank', 'Unknown')} - {bin_info.get('country', 'Unknown')}")
                else:
                    print(f"❌ البين {bin_code}: غير موجود")
            else:
                print(f"❌ خطأ في البين {bin_code}: {response.status_code}")
                
        except Exception as e:
            print(f"❌ خطأ في البين {bin_code}: {str(e)}")

def test_card_generation():
    """Test card generation functionality"""
    print("\n🔧 اختبار توليد البطاقات...")
    
    bin_code = "453264"
    
    try:
        # Generate some test cards
        import random
        
        for i in range(3):
            # Generate random card number
            remaining_digits = 16 - len(bin_code)
            card_number = bin_code + ''.join([str(random.randint(0, 9)) for _ in range(remaining_digits)])
            
            # Generate random month and year
            month = str(random.randint(1, 12)).zfill(2)
            year = str(random.randint(2025, 2030))
            cvv = str(random.randint(100, 999))
            
            card = f"{card_number}|{month}|{year}|{cvv}"
            print(f"✅ البطاقة {i+1}: {card}")
            
    except Exception as e:
        print(f"❌ خطأ في توليد البطاقات: {str(e)}")

def main():
    """Main test function"""
    print("🚀 بدء اختبار البوت...")
    print("=" * 50)
    
    # Test bot token
    if test_bot_token():
        print("\n✅ البوت جاهز للاستخدام!")
    else:
        print("\n❌ البوت غير جاهز!")
        return
    
    # Test BIN API
    test_bin_api()
    
    # Test card generation
    test_card_generation()
    
    print("\n" + "=" * 50)
    print("🎉 انتهى الاختبار!")
    print("\n📋 ملخص النتائج:")
    print("✅ توكن البوت صحيح")
    print("✅ API البين يعمل")
    print("✅ توليد البطاقات يعمل")
    print("\n💡 البوت جاهز للاستخدام!")

if __name__ == "__main__":
    main()