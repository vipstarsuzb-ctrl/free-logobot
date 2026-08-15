import logging
import asyncio
import os
import urllib.parse
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from deep_translator import GoogleTranslator

# Tokenni Render Environment Variables orqali xavfsiz o'qiymiz
TOKEN = os.environ.get("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN topilmadi! Render Environment Variables qismini tekshiring.")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

class LogoState(StatesGroup):
    waiting_for_prompt = State()
    waiting_for_style = State()

translator = GoogleTranslator(source='auto', target='en')

@dp.message(Command("start"))
async def start_cmd(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "🎨 **Assalomu alaykum! Logo Yaratuvchi Botga Xush Kelibsiz!**\n\n"
        "O'zingiz xohlagan logo g'oyasini yozib yuboring (O'zbekcha yoki Inglizcha).\n\n"
        "💡 *Misol:* `Kofe do'koni uchun minimalist logo` yoki `Futbol jamoasi uchun burgut tasviri`"
    )
    await state.set_state(LogoState.waiting_for_prompt)

@dp.message(LogoState.waiting_for_prompt)
async def process_prompt(message: types.Message, state: FSMContext):
    user_text = message.text.strip()
    
    try:
        translated_text = translator.translate(user_text)
    except Exception:
        translated_text = user_text

    await state.update_data(prompt=translated_text, raw_text=user_text)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✨ Minimalist", callback_data="style_minimalist"),
                InlineKeyboardButton(text="🎯 Modern / Flat", callback_data="style_flat")
            ],
            [
                InlineKeyboardButton(text="🧊 3D Mascot", callback_data="style_3d"),
                InlineKeyboardButton(text="⚡ Vintage / Retro", callback_data="style_vintage")
            ],
            [
                InlineKeyboardButton(text="🚀 Neon / Cyberpunk", callback_data="style_neon")
            ]
        ]
    )

    await message.answer(
        f"📝 **G'oya:** `{user_text}`\n"
        f"🌐 *(Inglizcha:* `{translated_text}`*)*\n\n"
        "Endi logoyingiz uchun **stil tanlang**:",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    await state.set_state(LogoState.waiting_for_style)

@dp.callback_query(F.data.startswith("style_"), LogoState.waiting_for_style)
async def generate_logo(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    prompt = data.get("prompt")
    raw_text = data.get("raw_text")
    style_key = call.data.replace("style_", "")

    styles = {
        "minimalist": "minimalist vector logo, clean lines, simple, elegant, white background, 8k",
        "flat": "modern flat design logo, graphic illustration, professional, clean background, 8k",
        "3d": "3d mascot logo, detailed render, vibrant colors, clean background, 8k",
        "vintage": "vintage retro badge logo, classic typography, detailed emblem, 8k",
        "neon": "neon glowing logo, futuristic cyberpunk style, dark background, high contrast, 8k"
    }

    style_prompt = styles.get(style_key, "professional logo, vector art, 8k")
    full_prompt = f"{prompt}, {style_prompt}"
    encoded_prompt = urllib.parse.quote(full_prompt)

    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&seed=42&nologo=true"

    await call.message.edit_text("🎨 **Logoyingiz tayyorlanmoqda, iltimos kuting...**")

    try:
        await call.message.answer_photo(
            photo=image_url,
            caption=(
                f"✅ **Logoyingiz tayyor!**\n\n"
                f"📝 **Mavzu:** {raw_text}\n"
                f"🎨 **Stil:** {style_key.capitalize()}\n\n"
                f"🔄 Yangi logo yaratish uchun shunchaki yangi g'oya yuboring yoki /start bosing."
            )
        )
        await call.message.delete()
    except Exception as e:
        await call.message.answer("❌ Rasm yaratishda xatolik yuz berdi. Qaytadan urinib ko'ring.")
        print(f"Xatolik: {e}")

    await state.set_state(LogoState.waiting_for_prompt)

async def main():
    print("Logo bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
