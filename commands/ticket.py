import discord
from discord import app_commands
from discord.ext import commands

from actions import printer


class TicketCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="ticket", description="Print a ticket on the receipt printer")
    @app_commands.describe(message="The text to print on the ticket")
    async def ticket(self, interaction: discord.Interaction, message: str) -> None:
        await printer.handle(interaction, message)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(TicketCog(bot))
