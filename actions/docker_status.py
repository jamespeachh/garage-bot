import asyncio

import discord

import config


async def _check_container(name: str) -> str:
    """Return a status emoji+label for a single Docker container."""
    try:
        proc = await asyncio.create_subprocess_exec(
            "docker",
            "inspect",
            "--format={{.State.Running}}",
            name,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()

        if proc.returncode != 0:
            # docker inspect exits non-zero when the container does not exist
            return "⚠️ Not found"

        output = stdout.decode().strip().lower()
        if output == "true":
            return "🟢 Running"
        elif output == "false":
            return "🔴 Stopped"
        else:
            return "⚠️ Not found"

    except Exception:
        return "⚠️ Error"


async def handle(interaction: discord.Interaction) -> None:
    """Handle the /status slash command — report Docker container health."""
    await interaction.response.defer()

    if not config.MONITORED_CONTAINERS:
        await interaction.followup.send(
            "No containers are configured. "
            "Set the `MONITORED_CONTAINERS` environment variable to a "
            "comma-separated list of container names."
        )
        return

    # Check all containers concurrently
    statuses: list[str] = await asyncio.gather(
        *[_check_container(name) for name in config.MONITORED_CONTAINERS]
    )

    all_running = all(s == "🟢 Running" for s in statuses)
    embed_color = discord.Color.green() if all_running else discord.Color.red()

    embed = discord.Embed(title="Docker Container Status", color=embed_color)

    for name, status in zip(config.MONITORED_CONTAINERS, statuses):
        embed.add_field(name=name, value=status, inline=False)

    await interaction.followup.send(embed=embed)
