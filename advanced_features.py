#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced Features for PowerBot
ميزات متقدمة للبوت القوي
"""

import asyncio
import aiohttp
import json
import hashlib
import base64
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import requests
from bs4 import BeautifulSoup
import re

class AdvancedFeatures:
    def __init__(self):
        self.cache = {}
        self.user_sessions = {}
        
    async def translate_text(self, text: str, target_lang: str = "en") -> str:
        """ترجمة النصوص"""
        try:
            # Simulate translation API
            translations = {
                "hello": "مرحبا",
                "world": "العالم",
                "bot": "بوت",
                "powerful": "قوي",
                "telegram": "تيليجرام"
            }
            
            if text.lower() in translations:
                return translations[text.lower()]
            else:
                return f"ترجمة: {text} -> {target_lang}"
        except Exception as e:
            return f"خطأ في الترجمة: {str(e)}"
            
    async def get_weather_real(self, city: str) -> Dict:
        """الحصول على معلومات الطقس الحقيقية"""
        try:
            # Using OpenWeatherMap API (you need to add your API key)
            api_key = "YOUR_API_KEY"  # Add your API key here
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ar"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            "city": city,
                            "temperature": f"{data['main']['temp']}°C",
                            "condition": data['weather'][0]['description'],
                            "humidity": f"{data['main']['humidity']}%",
                            "wind": f"{data['wind']['speed']} km/h"
                        }
                    else:
                        return {"error": "لا يمكن العثور على المدينة"}
        except Exception as e:
            return {"error": f"خطأ: {str(e)}"}
            
    async def web_scraper(self, url: str) -> Dict:
        """استخراج معلومات من المواقع الإلكترونية"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')
                        
                        # Extract title
                        title = soup.find('title')
                        title_text = title.text if title else "لا يوجد عنوان"
                        
                        # Extract meta description
                        meta_desc = soup.find('meta', attrs={'name': 'description'})
                        description = meta_desc.get('content', '') if meta_desc else "لا يوجد وصف"
                        
                        # Extract links
                        links = soup.find_all('a', href=True)
                        link_count = len(links)
                        
                        return {
                            "title": title_text,
                            "description": description[:200] + "..." if len(description) > 200 else description,
                            "links_count": link_count,
                            "url": url
                        }
                    else:
                        return {"error": f"خطأ في الوصول للموقع: {response.status}"}
        except Exception as e:
            return {"error": f"خطأ: {str(e)}"}
            
    async def generate_password(self, length: int = 12, include_symbols: bool = True) -> str:
        """توليد كلمة مرور قوية"""
        import random
        import string
        
        chars = string.ascii_letters + string.digits
        if include_symbols:
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
            
        password = ''.join(random.choice(chars) for _ in range(length))
        return password
        
    async def hash_text(self, text: str, algorithm: str = "md5") -> str:
        """تشفير النصوص"""
        try:
            if algorithm.lower() == "md5":
                return hashlib.md5(text.encode()).hexdigest()
            elif algorithm.lower() == "sha1":
                return hashlib.sha1(text.encode()).hexdigest()
            elif algorithm.lower() == "sha256":
                return hashlib.sha256(text.encode()).hexdigest()
            elif algorithm.lower() == "base64":
                return base64.b64encode(text.encode()).decode()
            else:
                return "خوارزمية غير مدعومة"
        except Exception as e:
            return f"خطأ في التشفير: {str(e)}"
            
    async def url_analyzer(self, url: str) -> Dict:
        """تحليل الروابط"""
        try:
            # Basic URL validation
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
                
            # Check if URL is accessible
            async with aiohttp.ClientSession() as session:
                async with session.head(url, allow_redirects=True) as response:
                    status_code = response.status
                    final_url = str(response.url)
                    
                    # Get response time
                    start_time = datetime.now()
                    async with session.get(url) as get_response:
                        response_time = (datetime.now() - start_time).total_seconds()
                        
                    return {
                        "original_url": url,
                        "final_url": final_url,
                        "status_code": status_code,
                        "response_time": f"{response_time:.2f}s",
                        "accessible": status_code == 200,
                        "redirected": url != final_url
                    }
        except Exception as e:
            return {"error": f"خطأ في تحليل الرابط: {str(e)}"}
            
    async def text_analyzer(self, text: str) -> Dict:
        """تحليل النصوص"""
        try:
            # Count characters
            char_count = len(text)
            word_count = len(text.split())
            line_count = len(text.splitlines())
            
            # Count Arabic and English characters
            arabic_chars = len(re.findall(r'[\u0600-\u06FF]', text))
            english_chars = len(re.findall(r'[a-zA-Z]', text))
            numbers = len(re.findall(r'\d', text))
            
            # Find most common words
            words = text.lower().split()
            word_freq = {}
            for word in words:
                if len(word) > 2:  # Ignore short words
                    word_freq[word] = word_freq.get(word, 0) + 1
                    
            most_common = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]
            
            return {
                "characters": char_count,
                "words": word_count,
                "lines": line_count,
                "arabic_chars": arabic_chars,
                "english_chars": english_chars,
                "numbers": numbers,
                "most_common_words": most_common
            }
        except Exception as e:
            return {"error": f"خطأ في تحليل النص: {str(e)}"}
            
    async def file_processor(self, file_data: bytes, file_type: str) -> Dict:
        """معالجة الملفات"""
        try:
            file_size = len(file_data)
            
            if file_type.startswith('image/'):
                # Process image
                from PIL import Image
                import io
                
                img = Image.open(io.BytesIO(file_data))
                return {
                    "type": "image",
                    "size": file_size,
                    "dimensions": img.size,
                    "format": img.format,
                    "mode": img.mode
                }
            elif file_type.startswith('text/'):
                # Process text file
                text_content = file_data.decode('utf-8', errors='ignore')
                analysis = await self.text_analyzer(text_content)
                return {
                    "type": "text",
                    "size": file_size,
                    "analysis": analysis
                }
            else:
                return {
                    "type": "unknown",
                    "size": file_size,
                    "message": "نوع ملف غير مدعوم"
                }
        except Exception as e:
            return {"error": f"خطأ في معالجة الملف: {str(e)}"}
            
    async def create_session(self, user_id: int) -> str:
        """إنشاء جلسة للمستخدم"""
        session_id = hashlib.md5(f"{user_id}{datetime.now()}".encode()).hexdigest()
        self.user_sessions[user_id] = {
            "session_id": session_id,
            "created_at": datetime.now(),
            "last_activity": datetime.now(),
            "data": {}
        }
        return session_id
        
    async def get_session_data(self, user_id: int) -> Optional[Dict]:
        """الحصول على بيانات الجلسة"""
        return self.user_sessions.get(user_id)
        
    async def update_session(self, user_id: int, data: Dict):
        """تحديث بيانات الجلسة"""
        if user_id in self.user_sessions:
            self.user_sessions[user_id]["last_activity"] = datetime.now()
            self.user_sessions[user_id]["data"].update(data)
            
    async def cleanup_sessions(self, max_age_hours: int = 24):
        """تنظيف الجلسات القديمة"""
        cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
        expired_sessions = [
            user_id for user_id, session in self.user_sessions.items()
            if session["last_activity"] < cutoff_time
        ]
        
        for user_id in expired_sessions:
            del self.user_sessions[user_id]
            
        return len(expired_sessions)