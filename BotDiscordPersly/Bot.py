import discord
import os
import asyncio
from discord.ext import commands
from dotenv import load_dotenv

# Cargamos el Token desde el archivo .env
load_dotenv()
TOKEN = os.getenv('DiscordToken')

class MyBot(commands.Bot):
    def __init__(self):
        # Activamos todos los permisos (Intents)
        intents = discord.Intents.all()
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # Este bucle busca todos los archivos en la carpeta /cogs y los carga
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await self.load_extension(f'cogs.{filename[:-3]}')
                print(f'Módulo {filename} cargado correctamente.')

bot = MyBot()

@bot.event
async def on_ready():
    print(f'--- {bot.user.name} está ONLINE ---')

async def main():
    async with bot:
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())