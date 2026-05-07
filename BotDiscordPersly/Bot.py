import discord
import os
import asyncio
from discord.ext import commands
from dotenv import load_dotenv

# Cargamos las variables de entorno
load_dotenv()
TOKEN = os.getenv('DiscordToken')
SERVER_ID = os.getenv('ServerId')


class MyBot(commands.Bot):
    def __init__(self):
        # Activamos todos los permisos (Intents)
        # RECUERDA: Deben estar activados también en el Discord Developer Portal
        intents = discord.Intents.all()
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # 1. Cargamos todos los archivos de la carpeta /cogs
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                try:
                    await self.load_extension(f'cogs.{filename[:-3]}')
                    print(f'✅ Módulo {filename} cargado correctamente.')
                except Exception as e:
                    print(f'❌ Error al cargar {filename}: {e}')
        
        # 2. Sincronización de comandos "/"
        # Cambia este ID por el de tu servidor para que aparezcan AL INSTANTE
        ID_MI_SERVIDOR = int(os.getenv('ServerId'))  # <--- REEMPLAZA ESTO

        try:
            guild = discord.Object(id=ID_MI_SERVIDOR)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
            print(f"🚀 Comandos sincronizados instantáneamente en el servidor: {ID_MI_SERVIDOR}")
        except Exception as e:
            print(f"⚠️ Error al sincronizar comandos: {e}")

bot = MyBot()

@bot.event
async def on_ready():
    print(f'--- {bot.user.name} está ONLINE y funcionando ---')
    print(f'Conectado a {len(bot.guilds)} servidores.')

async def main():
    if not TOKEN:
        print("❌ ERROR: No se encontró la variable 'DiscordToken'. Revisa Railway o tu .env")
        return
        
    async with bot:
        await bot.start(TOKEN)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot apagado manualmente.")