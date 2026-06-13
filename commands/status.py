import discord
from discord import app_commands
from discord.ext import commands

from actions import docker_status


class StatusCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="status", description="Check the health of monitored Docker containers")
    async def status(self, interaction: discord.Interaction) -> None:
        await docker_status.handle(interaction)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(StatusCog(bot))
