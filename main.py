import telebot
from telebot import types
from wakeonlan import send_magic_packet
import os

# --- AYARLARIN (Burayı kendine göre doldur knk) ---
API_TOKEN = '8092265008:AAEtY0F4pE0fEInaMv-qYQZfOa-I-X-5X_U'
MAC_ADRESI = '7C:10:C9:4A:2B:65' 
DIS_IP = '78.182.3.1'
PORT = 9

bot = telebot.TeleBot(API_TOKEN)

# --- KLAVYE MENÜSÜ ---
def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    # Satır 1
    btn1 = types.KeyboardButton('🖥️ PC AÇ')
    btn2 = types.KeyboardButton('📸 Ekran Al')
    btn3 = types.KeyboardButton('🔌 PC Kapat')
    # Satır 2
    btn4 = types.KeyboardButton('🔊 Ses %100')
    btn5 = types.KeyboardButton('💬 Mesaj Yolla')
    btn6 = types.KeyboardButton('📷 WebCam Al')
    # Satır 3
    btn7 = types.KeyboardButton('🛑 Görevi Bitir')
    btn8 = types.KeyboardButton('🔍 Durum')
    
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8)
    return markup

# /start Komutu
@bot.message_handler(commands=['start', 'panel'])
def start(message):
    bot.send_message(message.chat.id, "🛰️ **Fettah Ultra Kontrol Merkezi Yayında!**\n\nPC kapalıyken sadece 'PC AÇ' çalışır. PC açılınca tüm özellikler aktif olur knk.", 
                     reply_markup=main_menu(), parse_mode="Markdown")

# 1. PC AÇMA (WOL)
@bot.message_handler(func=lambda m: m.text == '🖥️ PC AÇ')
def wake_up(message):
    try:
        send_magic_packet(MAC_ADRESI, ip_address=DIS_IP, port=PORT)
        bot.reply_to(message, f"🚀 **Sihirli Paket Gönderildi!**\n📍 IP: {DIS_IP}\n⏳ PC uyanıyor, 1-2 dakikaya bağlanır.")
    except Exception as e:
        bot.reply_to(message, f"❌ Paket gitmedi: {e}")

# DİĞER KOMUTLAR (Bu komutlar evdeki PC'deki bot tarafından dinlenecek)
@bot.message_handler(func=lambda m: True)
def handle_commands(message):
    chat_id = message.chat.id
    txt = message.text

    if txt == '🔍 Durum':
        bot.send_message(chat_id, "📡 **Render Sunucusu:** Aktif ✅\n🖥️ **Evdeki PC:** (PC açılınca 'Ben geldim' yazacaktır)")
    
    elif txt == '💬 Mesaj Yolla':
        bot.send_message(chat_id, "⌨️ PC ekranında ne yazsın? (Örn: /msg Selam knk)")
        
    else:
        # Eğer PC kapalıysa ve bu butonlara basarsan Render "Sinyal gönderildi" der.
        # Evdeki bot bu mesajı görünce işlemi yapacak.
        bot.send_message(chat_id, f"📡 **Sinyal Gönderildi:** '{txt}'\n(PC açıksa işlem yapılır knk)")

print("Render Botu Başlatıldı...")
bot.polling(none_stop=True)
