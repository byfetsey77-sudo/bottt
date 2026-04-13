import discord
from discord.ext import commands
from discord.ui import Button, View
import pyautogui, os, webbrowser, cv2, time, psutil
from wakeonlan import send_magic_packet

# --- AYARLAR ---
# Render panelinde 'DISCORD_TOKEN' anahtarıyla eklediğin şifreyi çeker
TOKEN = os.getenv("DISCORD_TOKEN")
MAC_ADRESI = '7C:10:C9:4A:2B:65' 
DIS_IP = '78.182.3.1'
PORT = 9

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# --- FONKSİYONLAR (HATA YÖNETİMLİ) ---
def temizlik_yap():
    """Açık tarayıcıları kapatır ve masaüstüne döner."""
    try:
        pyautogui.hotkey('win', 'd')
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] in ["chrome.exe", "msedge.exe", "opera.exe", "brave.exe"]:
                proc.terminate()
    except Exception as e:
        print(f"Temizlik sırasında hata: {e}")

# --- KONTROL PANELİ ---
class ControlPanel(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🖥️ PC AÇ", style=discord.ButtonStyle.success)
    async def pc_ac_buton(self, interaction: discord.Interaction, button: Button):
        try:
            send_magic_packet(MAC_ADRESI, ip_address=DIS_IP, port=PORT)
            await interaction.response.send_message("🚀 **Sihirli paket gönderildi!** PC uyanıyor knk.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Uyandırma başarısız: {e}", ephemeral=True)

    @discord.ui.button(label="📸 Ekran Al", style=discord.ButtonStyle.primary)
    async def ss_al_buton(self, interaction: discord.Interaction, button: Button):
        try:
            pyautogui.screenshot("ss.png")
            await interaction.response.send_message("📸 Ekran görüntüsü yükleniyor...", file=discord.File("ss.png"))
            os.remove("ss.png")
        except Exception as e:
            await interaction.response.send_message(f"❌ SS Hatası: {e}", ephemeral=True)

    @discord.ui.button(label="🧹 Temizle", style=discord.ButtonStyle.secondary)
    async def temizle_buton(self, interaction: discord.Interaction, button: Button):
        temizlik_yap()
        await interaction.response.send_message("🧼 Masaüstü tertemiz yapıldı!", ephemeral=True)

    @discord.ui.button(label="🔒 Kilitle", style=discord.ButtonStyle.danger)
    async def kilitle_buton(self, interaction: discord.Interaction, button: Button):
        try:
            os.system("rundll32.exe user32.dll,LockWorkStation")
            await interaction.response.send_message("🔒 PC Kilitlendi.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Kilitleme Hatası: {e}", ephemeral=True)

# --- OLAYLAR VE KOMUTLAR ---
@bot.event
async def on_ready():
    print(f'Sistem Aktif: {bot.user}')
    # PC bağlandığı an otomatik temizlik yapar
    temizlik_yap()

@bot.command()
async def panel(ctx):
    """Butonlu kumandayı kanala çağırır."""
    await ctx.send("🎮 **FETTAH MASTER KONTROL MERKEZİ** 🎮", view=ControlPanel())

@bot.command()
async def google(ctx, *, arama):
    """Google'da hızlı arama yapar."""
    webbrowser.open(f"https://www.google.com/search?q={arama}")
    await ctx.send(f"🔎 **{arama}** için Google araması açıldı knk.")

@bot.command()
async def yt(ctx, *, arama):
    """YouTube'da hızlı video açar."""
    webbrowser.open(f"https://www.youtube.com/results?search_query={arama}")
    await ctx.send(f"🎥 YouTube'da **{arama}** açıldı.")

@bot.command()
async def webcam(ctx):
    """Kameradan anlık foto atar."""
    try:
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        if ret:
            cv2.imwrite("webcam.jpg", frame)
            cap.release()
            await ctx.send(file=discord.File("webcam.jpg"))
            os.remove("webcam.jpg")
        else:
            await ctx.send("❌ Kamera görüntüsü alınamadı (Kapalı veya meşgul).")
    except Exception as e:
        await ctx.send(f"❌ Kamera Hatası: {e}")

# BOTU BAŞLAT
bot.run(TOKEN)
