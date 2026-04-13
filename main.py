import telebot
from telebot import types
from wakeonlan import send_magic_packet
import os
import webbrowser
import pyautogui
import time
import psutil
import cv2 # Webcam için

# --- AYARLARIN ---
API_TOKEN = '8092265008:AAEtY0F4pE0fEInaMv-qYQZfOa-I-X-5X_U'
MAC_ADRESI = '7C:10:C9:4A:2B:65' 
DIS_IP = '78.182.3.1'
PORT = 9

bot = telebot.TeleBot(API_TOKEN)

# --- FONKSİYONLAR ---

def pencereleri_temizle():
    """Açık olan tarayıcıları kapatır ve masaüstüne döner."""
    pyautogui.hotkey('win', 'd')
    for proc in psutil.process_iter():
        try:
            if proc.name() in ["chrome.exe", "msedge.exe", "opera.exe"]:
                proc.terminate()
        except: pass

# --- MENÜ ---
def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    btns = [
        '🖥️ PC AÇ', '📸 Ekran Al', '🔌 PC Kapat',
        '🔍 Google Ara', '📺 YouTube Aç', '📷 WebCam Al',
        '🔊 Ses %100', '💬 Mesaj Yolla', '🧹 Temizle',
        '🔍 Durum', '🔒 Kilitle'
    ]
    markup.add(*(types.KeyboardButton(btn) for btn in btns))
    return markup

# --- KOMUTLAR ---

@bot.message_handler(commands=['start', 'panel'])
def start(message):
    bot.send_message(message.chat.id, "🛰️ **Fettah Master Kontrol Paneli Yayında!**\nEmrindeyim knk.", 
                     reply_markup=main_menu(), parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == '🖥️ PC AÇ')
def wake_up(message):
    try:
        send_magic_packet(MAC_ADRESI, ip_address=DIS_IP, port=PORT)
        bot.reply_to(message, "🚀 Sihirli paket gönderildi!")
    except Exception as e:
        bot.reply_to(message, f"❌ Hata: {e}")

@bot.message_handler(func=lambda m: m.text == '📸 Ekran Al')
def screenshot(message):
    ss = pyautogui.screenshot()
    ss.save("ss.png")
    with open("ss.png", "rb") as f:
        bot.send_photo(message.chat.id, f, caption="✅ Ekran görüntüsü alındı.")

@bot.message_handler(func=lambda m: m.text == '📷 WebCam Al')
def webcam(message):
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if ret:
        cv2.imwrite("cam.jpg", frame)
        cap.release()
        with open("cam.jpg", "rb") as f:
            bot.send_photo(message.chat.id, f, caption="✅ Kameradan görüntü alındı.")
    else:
        bot.reply_to(message, "❌ Kamera meşgul veya yok.")

@bot.message_handler(func=lambda m: m.text == '🧹 Temizle')
def clean(message):
    pencereleri_temizle()
    bot.reply_to(message, "🧹 Masaüstü temizlendi.")

@bot.message_handler(func=lambda m: m.text == '🔊 Ses %100')
def volume_up(message):
    for _ in range(50): pyautogui.press('volumeup')
    bot.reply_to(message, "🔊 Ses köklendi!")

@bot.message_handler(func=lambda m: m.text == '🔒 Kilitle')
def lock_pc(message):
    os.system("rundll32.exe user32.dll,LockWorkStation")
    bot.reply_to(message, "🔒 PC Kilitlendi.")

@bot.message_handler(func=lambda m: m.text == '🔌 PC Kapat')
def shutdown(message):
    bot.reply_to(message, "🔌 PC 30 saniye içinde kapanıyor...")
    os.system("shutdown /s /t 30")

# --- ARAMA MODÜLLERİ ---

@bot.message_handler(func=lambda m: m.text == '🔍 Google Ara')
def ask_google(message):
    msg = bot.send_message(message.chat.id, "🔍 Ne arayalım knk? (Kelimeyi yaz gönder)")
    bot.register_next_step_handler(msg, do_google)

def do_google(message):
    url = f"https://www.google.com/search?q={message.text}"
    webbrowser.open(url)
    bot.reply_to(message, f"✅ '{message.text}' aratıldı.")

@bot.message_handler(func=lambda m: m.text == '📺 YouTube Aç')
def ask_youtube(message):
    msg = bot.send_message(message.chat.id, "📺 Ne izleyeceksin? (İsmini yaz gönder)")
    bot.register_next_step_handler(msg, do_youtube)

def do_youtube(message):
    url = f"https://www.youtube.com/results?search_query={message.text}"
    webbrowser.open(url)
    bot.reply_to(message, f"🎥 '{message.text}' YouTube'da açıldı.")

@bot.message_handler(func=lambda m: m.text == '🔍 Durum')
def status(message):
    bot.reply_to(message, "✅ Evdeki PC: AKTİF\n🛰️ Render: BAĞLI")

# PC Açıldığında otomatik temizlik yap
pencereleri_temizle()
print("Fettah Master Bot Başlatıldı...")
bot.polling(none_stop=True)
