import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN: str = os.environ["DISCORD_TOKEN"]
PRINTER_NAME: str = os.getenv("PRINTER_NAME", "mattngina")

MONITORED_CONTAINERS: list[str] = [
    container.strip()
    for container in os.getenv("MONITORED_CONTAINERS", "").split(",")
    if container.strip()
]
