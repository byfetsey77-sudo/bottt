import discord
from discord.ext import commands
from discord.ui import Button, View
import os
from wakeonlan import send_magic_packet

# Render Environment Variables'dan çekilir
TOKEN = os.getenv("DISCORD_TOKEN")
MAC_ADRESI = '7C:10:C9:4A:2B:65' 
DIS_IP = '78.182.3.1'
PORT = 9

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

class ControlPanel(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🖥️ PC AÇ", style=discord.ButtonStyle.success)
    async def open_pc(self, interaction: discord.Interaction, button: Button):
        try:
            send_magic_packet(MAC_ADRESI, ip_address=DIS_IP, port=PORT)
            await interaction.response.send_message("🚀 Sihirli paket fırlatıldı! PC uyanıyor.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Hata: {e}", ephemeral=True)

@bot.event
async def on_ready():
    print(f'Render Nöbetçi Botu Aktif!')

@bot.command()
async def panel(ctx):
    await ctx.send("🎮 **FETTAH REMOTE (RENDER)**", view=ControlPanel())

@bot.command()
async def ac(ctx):
    send_magic_packet(MAC_ADRESI, ip_address=DIS_IP, port=PORT)
    await ctx.send("✅ PC açma sinyali gönderildi!")

bot.run(TOKEN)
