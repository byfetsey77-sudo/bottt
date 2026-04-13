import discord
from discord.ext import commands
from discord.ui import Button, View
import pyautogui, os, webbrowser, cv2, time, psutil
from wakeonlan import send_magic_packet

# --- AYARLAR ---
# Render Environment Variables'da 'DISCORD_TOKEN' adıyla kayıtlı olmalı
TOKEN = os.getenv("DISCORD_TOKEN")
MAC_ADRESI = '7C:10:C9:4A:2B:65' 
DIS_IP = '78.182.3.1'
PORT = 9

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# --- YARDIMCI ARAÇLAR ---
def pencereleri_temizle():
    """Hata almamak için try-except içine alınmış temizlik fonksiyonu."""
    try:
        pyautogui.hotkey('win', 'd')
        for proc in psutil.process_iter():
            if proc.name() in ["chrome.exe", "msedge.exe", "opera.exe", "brave.exe"]:
                proc.terminate()
    except Exception as e:
        print(f"Temizlik hatası: {e}")

# --- KONTROL PANELİ (Buton Yapısı) ---
class ControlPanel(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🖥️ PC AÇ", style=discord.ButtonStyle.success)
    async def open_pc(self, interaction: discord.Interaction, button: Button):
        try:
            send_magic_packet(MAC_ADRESI, ip_address=DIS_IP, port=PORT)
            await interaction.response.send_message("🚀 Sihirli paket fırlatıldı! PC uyanıyor knk.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Uyandırma hatası: {e}", ephemeral=True)

    @discord.ui.button(label="📸 Ekran Al", style=discord.ButtonStyle.primary)
    async def ss_pc(self, interaction: discord.Interaction, button: Button):
        try:
            pyautogui.screenshot("ss.png")
            await interaction.response.send_message(file=discord.File("ss.png"))
            os.remove("ss.png")
        except Exception as e:
            await interaction.response.send_message(f"❌ SS alınamadı: {e}", ephemeral=True)

    @discord.ui.button(label="🧹 Temizle", style=discord.ButtonStyle.secondary)
    async def clean_pc(self, interaction: discord.Interaction, button: Button):
        pencereleri_temizle()
        await interaction.response.send_message("🧼 Masaüstü tertemiz yapıldı.", ephemeral=True)

    @discord.ui.button(label="🔒 Kilitle", style=discord.ButtonStyle.danger)
    async def lock_pc(self, interaction: discord.Interaction, button: Button):
        try:
            os.system("rundll32.exe user32.dll,LockWorkStation")
            await interaction.response.send_message("🔒 PC Kilitlendi.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Kilitleme hatası: {e}", ephemeral=True)

# --- BOT OLAYLARI VE KOMUTLAR ---
@bot.event
async def on_ready():
    print(f'Sistem Hazır! Giriş: {bot.user}')
    # PC açıldığında otomatik pencereleri gizler
    pencereleri_temizle()

@bot.command()
async def panel(ctx):
    """Butonlu paneli kanala gönderir."""
    await ctx.send("🎮 **FETTAH REMOTE MASTER KONTROL**", view=ControlPanel())

@bot.command()
async def google(ctx, *, sorgu):
    """Google'da arama yapar."""
    webbrowser.open(f"https://www.google.com/search?q={sorgu}")
    await ctx.send(f"🔎 Google'da **{sorgu}** aranıyor...")

@bot.command()
async def yt(ctx, *, sorgu):
    """YouTube'da arama yapar."""
    webbrowser.open(f"https://www.youtube.com/results?search_query={sorgu}")
    await ctx.send(f"🎥 YouTube'da **{sorgu}** açıldı.")

@bot.command()
async def webcam(ctx):
    """Webcam'den fotoğraf çeker."""
    try:
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        if ret:
            cv2.imwrite("cam.jpg", frame)
            cap.release()
            await ctx.send(file=discord.File("cam.jpg"))
            os.remove("cam.jpg")
        else:
            await ctx.send("❌ Kamera görüntüsü alınamadı (Meşgul olabilir).")
    except Exception as e:
        await ctx.send(f"❌ Kamera hatası: {e}")

@bot.command()
async def ses(ctx):
    """Sesi fullemeye çalışır."""
    for _ in range(50): pyautogui.press('volumeup')
    await ctx.send("🔊 Ses seviyesi yükseltildi!")

# BOTU ÇALIŞTIR
bot.run(TOKEN)
