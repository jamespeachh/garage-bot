import asyncio
import discord
from discord.ext import commands

import config
from commands import COMMAND_COGS


intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} slash command(s)")


async def main():
    async with bot:
        for cog_path in COMMAND_COGS:
            await bot.load_extension(cog_path)
            print(f"Loaded: {cog_path}")
        await bot.start(config.DISCORD_TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
