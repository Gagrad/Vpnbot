import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8694514740:AAGIetdnmFoUZlkId5ONHH5QJ91f5ZBjm-U"
CHANNEL_ID = "samoletvpn1"

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def check_subscription(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=f"@{CHANNEL_ID}", user_id=user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

@dp.message(Command("start"))
async def start(message: types.Message):
    if await check_subscription(message.from_user.id):
        await show_main_menu(message)
    else:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📢 Подписаться", url=f"https://t.me/{CHANNEL_ID}")],
            [InlineKeyboardButton(text="✅ Я подписался", callback_data="check_sub")]
        ])
        await message.answer("🚀 Подпишись на канал:", reply_markup=keyboard)

@dp.callback_query(lambda c: c.data == "check_sub")
async def check_sub_callback(callback: types.CallbackQuery):
    if await check_subscription(callback.from_user.id):
        await callback.message.delete()
        await show_main_menu(callback.message)
    else:
        await callback.answer("❌ Не подписан!", show_alert=True)

async def show_main_menu(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💰 Купить VPN", callback_data="buy")],
        [InlineKeyboardButton(text="🎁 Получить подарок", callback_data="gift")]
    ])
    await message.answer(
        "🔥 Привет! Это VPN, который:\n"
        "• Обходит глушилки\n"
        "• Работает 24/7\n"
        "• Подходит для всех соцсетей\n\n"
        "Выбери действие:",
        reply_markup=keyboard
    )

@dp.callback_query(lambda c: c.data == "buy")
async def buy_callback(callback: types.CallbackQuery):
    await callback.message.answer("🛒 Раздел покупки (скоро добавим выбор тарифов)")

@dp.callback_query(lambda c: c.data == "gift")
async def gift_callback(callback: types.CallbackQuery):
    await callback.message.answer("🎁 Раздел подарков (скоро добавим рефералку)")

async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
