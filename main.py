import discord
from discord.ext import commands
from discord.ui import Button, View
import pyautogui, os, webbrowser, cv2, time, psutil
from wakeonlan import send_magic_packet

# --- GÜVENLİ TOKEN ALMA ---
TOKEN = os.getenv("DISCORD_TOKEN") # Burayı böyle bırak, elle dokunma knk
MAC_ADRESI = '7C:10:C9:4A:2B:65' 
DIS_IP = '78.182.3.1'

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ... (Kodun geri kalanı aynı kalsın knk)

# --- FONKSİYONLAR ---
def pencereleri_temizle():
    pyautogui.hotkey('win', 'd')
    for proc in psutil.process_iter():
        try:
            if proc.name() in ["chrome.exe", "msedge.exe", "opera.exe", "brave.exe"]:
                proc.terminate()
        except: pass

# --- BUTONLU KONTROL PANELİ ---
class ControlPanel(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🖥️ PC AÇ", style=discord.ButtonStyle.success)
    async def open_pc(self, interaction: discord.Interaction, button: Button):
        send_magic_packet(MAC_ADRESI, ip_address=DIS_IP, port=PORT)
        await interaction.response.send_message("🚀 Sihirli paket fırlatıldı knk!")

    @discord.ui.button(label="📸 Ekran Al", style=discord.ButtonStyle.primary)
    async def ss_pc(self, interaction: discord.Interaction, button: Button):
        pyautogui.screenshot("ss.png")
        await interaction.response.send_message(file=discord.File("ss.png"))
        os.remove("ss.png")

    @discord.ui.button(label="🧹 Temizle", style=discord.ButtonStyle.secondary)
    async def clean_pc(self, interaction: discord.Interaction, button: Button):
        pencereleri_temizle()
        await interaction.response.send_message("🧼 Masaüstü tertemiz yapıldı.")

    @discord.ui.button(label="🔒 Kilitle", style=discord.ButtonStyle.danger)
    async def lock_pc(self, interaction: discord.Interaction, button: Button):
        os.system("rundll32.exe user32.dll,LockWorkStation")
        await interaction.response.send_message("🔒 PC Kilitlendi.")

# --- KOMUTLAR ---
@bot.event
async def on_ready():
    print(f'Fettah Discord Master ({bot.user}) Aktif!')
    pencereleri_temizle()

@bot.command()
async def panel(ctx):
    await ctx.send("🎮 **FETTAH MASTER KONTROL MERKEZİ** 🎮", view=ControlPanel())

@bot.command()
async def google(ctx, *, sorgu):
    webbrowser.open(f"https://www.google.com/search?q={sorgu}")
    await ctx.send(f"🔎 Google'da **{sorgu}** aranıyor...")

@bot.command()
async def yt(ctx, *, sorgu):
    webbrowser.open(f"https://www.youtube.com/results?search_query={sorgu}")
    await ctx.send(f"🎥 YouTube'da **{sorgu}** açıldı.")

@bot.command()
async def ses(ctx):
    for _ in range(50): pyautogui.press('volumeup')
    await ctx.send("🔊 Ses son seviyeye çekildi!")

@bot.command()
async def webcam(ctx):
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if ret:
        cv2.imwrite("cam.jpg", frame)
        cap.release()
        await ctx.send(file=discord.File("cam.jpg"))
        os.remove("cam.jpg")
    else:
        await ctx.send("❌ Kamera meşgul veya takılı değil knk.")

bot.run(TOKEN)
