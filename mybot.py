import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton

# Bot tokeningiz
TOKEN = "8858932432:AAHtO4z5ivP3WGK39c2kPChJgKfmpIL9jb4"

# GitHub Pages havolangiz
WEB_APP_URL = "https://anvarsolexov.github.io/my-mini-app/"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

# /start buyrug'i
@dp.message(Command("start"))
async def start_command(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🛍️ Do'konni Ochish",
                    web_app=WebAppInfo(url=WEB_APP_URL)
                )
            ]
        ]
    )
    
    await message.answer(
        "🌟 **Assalomu alaykum!**\n\n"
        "Do'kondan mahsulotni tanlang, to'lov qiling va SMS xabarnoma orqali avtomatik tarzda qabul qiling.",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

# Mini App'dan tanlangan mahsulotni qabul qilib oluvchi qism
@dp.message(lambda message: message.web_app_data is not None)
async def web_app_data_handler(message: types.Message):
    product_data = message.web_app_data.data
    
    # Bu yerda foydalanuvchiga karta va summani chiqaramiz
    await message.answer(
        f"✅ **Buyurtma qabul qilindi!**\n\n"
        f"📦 Mahsulot: {product_data}\n\n"
        f"💳 **Karta:** `986016065272996` (Anvar Solexov)\n\n"
        f"⏳ *Iltimos, ko'rsatilgan summani o'tkazing. SMS xabarnoma kelishi bilan to'lovingiz avtomatik tasdiqlanadi va mahsulotingiz beriladi!*",
        parse_mode="Markdown"
    )
    
    # BU YERDA SMS API INTEGRATSIYasi BO'LADI:
    # Sizning bank SMS xabarnomalarini o'qiydigan funksiyangiz yoki 
    # SMS serveringiz kelgan pullarni shu yerda tekshirib, to'g'ri kelsa
    # avtomatik ravishda quyidagi muvaffaqiyat xabarini yuboradi:
    
    # MISOQ UCHUN (SMS kelganda ishlaydigan kod):
    # await asyncio.sleep(10) # SMS kelishini kutish simulyatsiyasi
    # await message.answer("🎉 To'lovingiz SMS xabarnoma orqali tasdiqlandi! Buyurtmangiz bajarildi.")

async def main():
    print("Bot ishga tushdi va SMS tekshiruvga tayyor...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())