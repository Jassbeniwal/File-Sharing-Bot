# (©) CodexBotz – Production Safe Version

from aiohttp import web
from plugins import web_server

import pyromod.listen
from pyrogram import Client
from pyrogram.enums import ParseMode
from pyrogram.errors import FloodWait

import asyncio
from datetime import datetime

from config import (
    API_HASH,
    APP_ID,
    LOGGER,
    TG_BOT_TOKEN,
    TG_BOT_WORKERS,
    FORCE_SUB_CHANNEL,
    CHANNEL_ID,
    PORT
)

ascii_art = """
░█████╗░░█████╗░██████╗░███████╗██╗░░██╗██████╗░░█████╗░████████╗███████╗
"""

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Bot",
            api_id=APP_ID,
            api_hash=API_HASH,
            bot_token=TG_BOT_TOKEN,
            workers=TG_BOT_WORKERS,
            plugins={"root": "plugins"}
        )
        self.LOGGER = LOGGER
        self.invitelink = None
        self.db_channel = None

    async def start(self):
        try:
            await super().start()
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await super().start()

        me = await self.get_me()
        self.username = me.username
        self.uptime = datetime.now()

        # ================= FORCE SUB (SAFE) =================
        if FORCE_SUB_CHANNEL and FORCE_SUB_CHANNEL != "0":
            try:
                chat = await self.get_chat(FORCE_SUB_CHANNEL)
                link = chat.invite_link

                if not link:
                    link = await self.export_chat_invite_link(FORCE_SUB_CHANNEL)

                self.invitelink = link

            except Exception as e:
                self.LOGGER(__name__).warning(e)
                self.LOGGER(__name__).warning(
                    "Force Sub Channel error — bot will continue WITHOUT force sub"
                )
                self.invitelink = None

        # ================= DB CHANNEL (SAFE) =================
        if CHANNEL_ID and CHANNEL_ID != "0":
            try:
                self.db_channel = await self.get_chat(CHANNEL_ID)
                test = await self.send_message(self.db_channel.id, "Test")
                await test.delete()
            except Exception as e:
                self.LOGGER(__name__).warning(e)
                self.LOGGER(__name__).warning(
                    "DB Channel error — bot will continue WITHOUT DB channel"
                )
                self.db_channel = None

        self.set_parse_mode(ParseMode.HTML)

        self.LOGGER(__name__).info("Bot Running Successfully!")
        print(ascii_art)
        print("Welcome to CodeXBotz File Sharing Bot")

        # ================= WEB SERVER =================
        app = web.AppRunner(await web_server())
        await app.setup()
        await web.TCPSite(app, "0.0.0.0", PORT).start()

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped.")
