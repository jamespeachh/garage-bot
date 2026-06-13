# Garage Bot — Developer Guide

## What this bot is

A Discord bot that exposes slash commands. Each command is a thin router that delegates to a self-contained action module. Adding a new feature requires three small steps and touches no existing files except the registry.

---

## Project layout

```
garage-bot/
├── bot.py                    # Entry point — loads cogs, syncs commands, starts bot
├── config.py                 # Typed env-var access (load .env, expose constants)
├── requirements.txt
├── .env                      # Not committed — copy from .env.example
├── .env.example
│
├── commands/
│   ├── __init__.py           # ★ COMMAND REGISTRY — the only file to edit when adding a command
│   ├── ticket.py             # /ticket <message>
│   └── status.py             # /status
│
└── actions/
    ├── printer.py            # Business logic for /ticket — thermal receipt printer (win32print / ESC-POS)
    └── docker_status.py      # Business logic for /status — Docker container health checks
```

---

## How to add a new slash command

### Step 1 — Register it in `commands/__init__.py`

```python
COMMAND_COGS: list[str] = [
    "commands.ticket",
    "commands.status",
    "commands.your_command",  # ← add this line
]
```

### Step 2 — Create `commands/your_command.py`

This file is a discord.py **Cog** that defines the slash-command signature and its parameters. Keep it thin — it calls the action and nothing else.

```python
import discord
from discord import app_commands
from discord.ext import commands
from actions import your_module


class YourCommandCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="your_command", description="One-line description shown in Discord")
    @app_commands.describe(param="Description of each parameter")
    async def your_command(self, interaction: discord.Interaction, param: str) -> None:
        await your_module.handle(interaction, param)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(YourCommandCog(bot))
```

### Step 3 — Create `actions/your_module.py`

This file owns all business logic. It must expose a `handle` coroutine whose first argument is always `interaction: discord.Interaction`.

```python
import discord


async def handle(interaction: discord.Interaction, param: str) -> None:
    # ... your logic here ...
    await interaction.response.send_message("Done.")
```

That's it. No other files change.

---

## Slash command registry reference (`commands/__init__.py`)

| Cog path            | Command    | Description                                 |
|---------------------|------------|---------------------------------------------|
| `commands.ticket`   | `/ticket`  | Prints a receipt ticket on the thermal printer |
| `commands.status`   | `/status`  | Reports health of monitored Docker containers  |

---

## Action module contracts

Every file in `actions/` must follow this contract so the cog layer stays uniform:

- Expose an `async def handle(interaction: discord.Interaction, ...)` function.
- Call `await interaction.response.send_message(...)` (or `interaction.response.defer()` + followup) before returning.
- Raise no unhandled exceptions — catch errors and send a user-facing message.
- Import config values from `config.py`, never hard-code them.

---

## Configuration (`config.py` / `.env`)

| Variable              | Required | Description                                         |
|-----------------------|----------|-----------------------------------------------------|
| `DISCORD_TOKEN`       | Yes      | Bot token from the Discord Developer Portal         |
| `PRINTER_NAME`        | No       | Win32 printer name (default: `mattngina`)           |
| `MONITORED_CONTAINERS`| No       | Comma-separated Docker container names to watch     |

---

## Running locally

```bash
poetry install          # creates the virtualenv and installs all deps
cp .env.example .env    # fill in DISCORD_TOKEN and other vars
poetry run python bot.py   # start the bot
```

## Adding a new dependency

```bash
poetry add <package>                        # runtime dep
poetry add --dev <package>                  # dev-only dep
```

---

## Key dependencies

| Package        | Purpose                                                  |
|----------------|----------------------------------------------------------|
| `discord.py`   | Discord API client and slash-command framework           |
| `python-dotenv`| Loads `.env` into environment variables                  |
| `pywin32`      | `win32print` — Windows-only thermal printer access (skipped on macOS/Linux) |

---

## Conventions

- **Cog class names**: `<PascalCase>Cog` (e.g. `TicketCog`, `StatusCog`)
- **Cog file names**: match the slash command name (`ticket.py` → `/ticket`)
- **Action file names**: match the cog file name where possible; use descriptive names when the action is broader than the command (e.g. `docker_status.py`)
- **No business logic in cog files** — cogs are routing only
- **No Discord objects in action files beyond `interaction`** — keep actions testable
