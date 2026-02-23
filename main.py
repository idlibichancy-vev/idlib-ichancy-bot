import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_PATH = "/webhook"
WEBHOOK_SECRET = "supersecret"
BASE_URL = os.getenv("RAILWAY_STATIC_URL")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message()
async def echo(message: types.Message):
    await message.answer("🚀 البوت يعمل على Railway بنظام Webhook")

async def on_startup(bot: Bot):
    webhook_url = f"https://{BASE_URL}{WEBHOOK_PATH}"
    await bot.set_webhook(webhook_url, secret_token=WEBHOOK_SECRET)

async def on_shutdown(bot: Bot):
    await bot.delete_webhook()

async def main():
    app = web.Application()

    SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=WEBHOOK_SECRET,
    ).register(app, path=WEBHOOK_PATH)

    setup_application(app, dp, bot=bot)

    port = int(os.getenv("PORT", 8000))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)

    await on_startup(bot)
    await site.start()

    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
