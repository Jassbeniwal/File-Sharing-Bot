from aiohttp import web
from plugins import web_server

import pyromod.listen
from pyrogram import Client
from pyrogram.enums import ParseMode
import sys
import logging
from datetime import datetime
import asyncio

from config import API_HASH, APP_ID, LOGGER, TG_BOT_TOKEN, TG_BOT_WORKERS, FORCE_SUB_CHANNEL, CHANNEL_ID, PORT


ascii_art = """
░█████╗░░█████╗░██████╗░███████╗██╗░░██╗██████╗░░█████╗░████████╗███████╗
██╔══██╗██╔══██╗██╔══██╗██╔════╝╚██╗██╔╝██╔══██╗██╔══██╗╚══██╔══╝╚════██║
██║░░╚═╝██║░░██║██║░░██║█████╗░░░╚███╔╝░██████╦╝██║░░██║░░░██║░░░░░███╔═╝
██║░░██╗██║░░██║██║░░██║██╔══╝░░░██╔██╗░██╔══██╗██║░░██║░░░██║░░░██╔══╝░░
╚█████╔╝╚█████╔╝██████╔╝███████╗██╔╝╚██╗██████╦╝╚█████╔╝░░░██║░░░███████╗
░╚════╝░░╚════╝░╚═════╝░╚══════╝╚═╝░░╚═╝╚═════╝░░╚════╝░░░░╚═╝░░░╚══════╝
"""

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Bot",
            api_hash=API_HASH,
            api_id=APP_ID,
            plugins={
                "root": "plugins"
            },
            workers=TG_BOT_WORKERS,
            bot_token=TG_BOT_TOKEN
        )
        self.LOGGER = LOGGER

    async def start(self):
        await super().start()
        usr_bot_me = await self.get_me()
        self.uptime = datetime.now()

        if FORCE_SUB_CHANNEL:
            try:
                link = await self.export_chat_invite_link(FORCE_SUB_CHANNEL)
                self.invitelink = link
            except Exception as a:
                self.LOGGER.warning(f"Error getting invite link: {a}")
                self.LOGGER.warning("Bot can't Export Invite link from Force Sub Channel!")
                self.LOGGER.warning(f"Please Double check the FORCE_SUB_CHANNEL value and Make sure Bot is Admin in channel with Invite Users via Link Permission, Current Force Sub Channel Value: {FORCE_SUB_CHANNEL}")
                self.LOGGER.info("\nBot Stopped. Join https://t.me/CodeXBotzSupport for support")
                sys.exit(1)
        
        if CHANNEL_ID:
            try:
                db_channel = await self.get_chat(CHANNEL_ID)
                self.db_channel = db_channel
                test = await self.send_message(chat_id=db_channel.id, text="Test Message")
                await test.delete()
            except Exception as e:
                self.LOGGER.warning(f"Error with DB Channel: {e}")
                self.LOGGER.warning(f"Make Sure bot is Admin in DB Channel, and Double check the CHANNEL_ID Value, Current Value {CHANNEL_ID}")
                self.LOGGER.info("\nBot Stopped. Join https://t.me/CodeXBotzSupport for support")
                sys.exit(1)

        self.set_parse_mode(ParseMode.HTML)
        self.LOGGER.info(f"Bot Running..!\n\nCreated by \nhttps://t.me/CodeXBotz")
        self.LOGGER.info(f"Bot Started as @{usr_bot_me.username}")
        
        print(ascii_art)
        print("Welcome to CodeXBotz File Sharing Bot")
        print(f"Bot Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        self.username = usr_bot_me.username
        
        # Start web server
        try:
            app = web.Application()
            app.add_routes([web.get('/', lambda request: web.Response(text="Bot is running!"))])
            runner = web.AppRunner(await web_server())
            await runner.setup()
            site = web.TCPSite(runner, '0.0.0.0', PORT)
            await site.start()
            self.LOGGER.info(f"Web server started on port {PORT}")
        except Exception as e:
            self.LOGGER.error(f"Failed to start web server: {e}")
            # Don't exit if web server fails, bot can still function

    async def stop(self, *args):
        await super().stop()
        self.LOGGER.info("Bot stopped.")

# Add this to run the bot properly
async def main():
    bot = Bot()
    await bot.start()
    
    # Keep the bot running
    try:
        await asyncio.Event().wait()
    except (KeyboardInterrupt, SystemExit):
        await bot.stop()

if __name__ == "__main__":
    # Check if all required configs are present
    required_configs = ['API_HASH', 'APP_ID', 'TG_BOT_TOKEN']
    for config in required_configs:
        if not globals().get(config):
            print(f"Error: {config} is not set in config.py")
            sys.exit(1)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nBot stopped by user")
