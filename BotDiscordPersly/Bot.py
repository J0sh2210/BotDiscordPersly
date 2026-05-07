import discord
import os
import asyncio
from discord.ext import commands
from dotenv import load_dotenv

# Cargamos el Token
load_dotenv()
TOKEN = os.getenv('DiscordToken')

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # Carga automática de Cogs
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                try:
                    await self.load_extension(f'cogs.{filename[:-3]}')
                    print(f'Módulo {filename} cargado correctamente.')
                except Exception as e:
                    print(f'Error al cargar {filename}: {e}')
        
        # --- ESTA ES LA LÍNEA QUE FALTABA ---
        # Sincroniza los comandos "/" con Discord
        await self.tree.sync()
        print("Comandos slash sincronizados.")

bot = MyBot()

@bot.event
async def on_ready():
    print(f'--- {bot.user.name} está ONLINE ---')

async def main():
    if not TOKEN:
        print("ERROR: No se encontró el DiscordToken en las variables de entorno.")
        return
        
    async with bot:
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())