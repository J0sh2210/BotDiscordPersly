import discord
from discord.ext import commands, tasks
import aiohttp
from datetime import time, datetime
import pytz
import dotenv 
import os

dotenv.load_dotenv()
ID_CANAL_OFERTAS = int(os.getenv("Idcanalofertas"))

# Definimos la zona horaria y la hora fuera de la clase para que el decorador la reconozca
zona_gt = pytz.timezone('America/Guatemala')
hora_gt = time(hour=14, minute=0, tzinfo=zona_gt)

class Juegos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.id_canal_publico = ID_CANAL_OFERTAS  # <--- TU ID DE CANAL
        self.anuncio_semanal.start()

    def cog_unload(self):
        self.anuncio_semanal.cancel()

    # Ahora el decorador usa "hora_gt" que ya está definida arriba
    @tasks.loop(time=hora_gt)
    async def anuncio_semanal(self):
        # Verificamos si hoy es Jueves (Lunes=0, Jueves=3)
        if datetime.now(zona_gt).weekday() != 3:
            return

        canal = self.bot.get_channel(self.id_canal_publico)
        if not canal:
            return

        url = "https://www.gamerpower.com/api/giveaways?type=game"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    await canal.send("🔔 **¡LLEGÓ EL JUEVES DE JUEGOS GRATIS!** 🎮")
                    
                    # Publicamos los 3 más importantes
                    for juego in data[:3]:
                        embed = discord.Embed(
                            title=juego['title'],
                            description=juego['description'],
                            color=discord.Color.blue()
                        )
                        embed.set_image(url=juego['image'])
                        embed.add_field(name="Plataforma", value=juego['platforms'])
                        embed.add_field(name="Link", value=f"[Reclamar aquí]({juego['gamerpower_url']})")
                        await canal.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Juegos(bot))