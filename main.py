import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv
import asyncpg

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# اتصال قاعدة البيانات
async def create_pool():
    return await asyncpg.create_pool(DATABASE_URL)

# قائمة رئيسية
def main_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="⚡ إنشاء حساب Ichancy")],
            [KeyboardButton(text="📥 شحن محفظة البوت"), KeyboardButton(text="📤 سحب من محفظة البوت")],
            [KeyboardButton(text="👤 معلومات الملف الشخصي")]
        ],
        resize_keyboard=True
    )
    return keyboard

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer(
        "🔷 أهلاً بك في Idlib Ichancy Bot\n\nاختر من القائمة:",
        reply_markup=main_menu()
    )

async def main():
    pool = await create_pool()
    dp["db"] = pool
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
