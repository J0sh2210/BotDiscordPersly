import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
ID_AMIGOS = int(os.getenv("Idamigos"))

class Voz(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.canal_logs_id = ID_AMIGOS

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        canal = self.bot.get_channel(self.canal_logs_id)
        if not canal:
            return

        if before.channel is None and after.channel is not None:
            await canal.send(f"**{member.display_name}** entró a `{after.channel.name}`")
        elif before.channel is not None and after.channel is None:
            await canal.send(f"**{member.display_name}** salió de `{before.channel.name}`")

async def setup(bot):
    await bot.add_cog(Voz(bot))