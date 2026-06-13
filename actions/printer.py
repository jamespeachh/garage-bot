import asyncio
from datetime import datetime

import discord
from escpos.printer import Usb

# POS-58 USB IDs (Vendor: Winbond/YICHIP3121, Product: POS-58 Printer)
_VENDOR_ID  = 0x0416
_PRODUCT_ID = 0x5011


def _sync_print(username: str, message: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    p = Usb(_VENDOR_ID, _PRODUCT_ID)

    p.set(align="center", bold=True, double_height=True, double_width=True)
    p.text("TICKET\n")

    p.set(align="left", bold=False, double_height=False, double_width=False)
    p.text("---------------------------\n")

    p.set(bold=True)
    p.text("From: ")
    p.set(bold=False)
    p.text(f"{username}\n")

    p.set(bold=True)
    p.text("Message:\n")
    p.set(bold=False)
    p.text(f"{message}\n")

    p.text("---------------------------\n")
    p.text(f"Sent: {timestamp}\n")

    p.cut()
    p.close()


async def handle(interaction: discord.Interaction, message: str) -> None:
    try:
        username = interaction.user.display_name
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, _sync_print, username, message)
        await interaction.response.send_message("Ticket printed successfully!", ephemeral=True)
    except Exception as exc:
        await interaction.response.send_message(
            f"Failed to print ticket: {exc}", ephemeral=True
        )
