# ─────────────────────────────────────────────────────────────────
#  SLASH COMMAND REGISTRY
#
#  This is the single source of truth for every slash command the
#  bot exposes.  To add a new command:
#
#    1. Add its cog path to COMMAND_COGS below.
#    2. Create  commands/<your_command>.py  (the slash-command cog).
#    3. Create  actions/<your_command>.py   (the business logic).
#
#  The bot loads every entry here on startup and syncs them to
#  Discord automatically.
# ─────────────────────────────────────────────────────────────────

COMMAND_COGS: list[str] = [
    "commands.ticket",   # /ticket <message> — sends to the thermal printer
    "commands.status",   # /status           — checks docker container health
]
