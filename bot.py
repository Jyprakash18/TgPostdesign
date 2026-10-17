import os
import io
import asyncio
import urllib.request
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BufferedInputFile
from PIL import Image, ImageDraw, ImageFont

# ==========================================
# ⚙️ CONFIGURATION (Apni Details Yahan Dalein)
# ==========================================
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
CHANNEL_ID = os.getenv("CHANNEL_ID", "@your_channel_username")
CHANNEL_TITLE = "MOVIE HUB"
POST_TITLE = "ALL YOUR ENTERTAINMENT IN ONE PLACE"
PREMIUM_URL = "https://t.me/your_premium_link"
# ==========================================

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def get_font(size: int, bold: bool = True):
    """Linux (Render) aur Windows dono ke liye clean font loader"""
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "arialbd.ttf" if bold else "arial.ttf"
    ]
    for path in font_paths:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()

def generate_card_image(include_fake_buttons: bool = True) -> bytes:
    """Pillow se Movie Hub style card RAM mein generate karta hai"""
    width = 600
    height = 780 if include_fake_buttons else 420
    bg_color = "#17212b"
    card_bg = "#131c26"
    border_col = "#24303f"

    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    font_h1 = get_font(34, True)
    font_sub = get_font(16, True)
    font_title = get_font(18, True)
    font_desc = get_font(14, False)
    font_btn = get_font(17, True)

    # 1. Top Banner Box
    draw.rounded_rectangle([20, 20, 580, 200], radius=18, fill="#0d141c", outline="#2b394a", width=2)
    draw.text((45, 55), f"🎬 {CHANNEL_TITLE}", fill="#ffffff", font=font_h1)
    draw.text((45, 105), POST_TITLE, fill="#93c5fd", font=font_sub)
    draw.rounded_rectangle([45, 145, 130, 151], radius=3, fill="#3b82f6")

    # 2. Row 1: Two Cards (Browse Movies | Video Quality)
    # Left Card
    draw.rounded_rectangle([20, 215, 292, 300], radius=14, fill=card_bg, outline=border_col, width=2)
    draw.rounded_rectangle([35, 232, 85, 282], radius=10, fill="#2563eb")
    draw.text((50, 245), "🎬", fill="#ffffff", font=font_title)
    draw.text((100, 235), "Browse Movies", fill="#ffffff", font=font_title)
    draw.text((100, 260), "Find your next watch", fill="#7f91a4", font=font_desc)
    draw.text((268, 245), ">", fill="#5c6c7c", font=font_title)

    # Right Card
    draw.rounded_rectangle([308, 215, 580, 300], radius=14, fill=card_bg, outline=border_col, width=2)
    draw.rounded_rectangle([323, 232, 373, 282], radius=10, fill="#2563eb")
    draw.text((338, 245), "TV", fill="#ffffff", font=font_title)
    draw.text((388, 235), "Video Quality", fill="#ffffff", font=font_title)
    draw.text((388, 260), "View available formats", fill="#7f91a4", font=font_desc)
    draw.text((555, 245), ">", fill="#5c6c7c", font=font_title)

    # 3. Row 2: Full Width Card (Premium Membership)
    draw.rounded_rectangle([20, 315, 580, 400], radius=14, fill=card_bg, outline=border_col, width=2)
    draw.rounded_rectangle([35, 332, 85, 382], radius=10, fill="#7c3aed")
    draw.text((48, 345), "VIP", fill="#ffffff", font=font_sub)
    draw.text((100, 335), "Premium Membership", fill="#ffffff", font=font_title)
    draw.text((100, 360), "See plans and benefits", fill="#7f91a4", font=font_desc)
    draw.text((555, 345), ">", fill="#5c6c7c", font=font_title)

    # 4. Optional Fake Buttons Section (For /post_fullcard)
    if include_fake_buttons:
        draw.line([(0, 420), (600, 420)], fill="#232e3c", width=2)
        draw.text((30, 438), "Get Full Access Now 👇", fill="#ffffff", font=get_font(22, True))

        buttons = [
            ("JOIN FREE", "#3b202c", "#7c3548", "#f472b6"),
            ("START HERE", "#143325", "#16a34a", "#4ade80"),
            ("UNLOCK VIP", "#1d9bf0", "#38bdf8", "#ffffff"),
            ("EXPLORE", "#3b202c", "#7c3548", "#f472b6"),
            ("JOIN CLUB", "#143325", "#16a34a", "#4ade80"),
        ]

        y_start = 485
        for label, bg_btn, border_btn, txt_col in buttons:
            draw.rounded_rectangle([55, y_start, 545, y_start + 46], radius=23, fill=bg_btn, outline=border_btn, width=2)
            text_str = f"✨  {label}  ✨"
            bbox = draw.textbbox((0, 0), text_str, font=font_btn)
            tw = bbox[2] - bbox[0]
            draw.text(((width - tw) // 2, y_start + 12), text_str, fill=txt_col, font=font_btn)
            draw.rectangle([510, y_start + 17, 522, y_start + 29], outline=txt_col, width=2)
            y_start += 56

    output = io.BytesIO()
    img.save(output, format="PNG")
    return output.getvalue()

# ==========================================================
# 🚀 COMMAND 1: /post_clickable (Header Image + 5 Real Buttons)
# ==========================================================
@dp.message(Command("post_clickable"))
async def send_clickable_post(message: types.Message):
    status = await message.reply("⏳ Generating Clickable Post...")
    try:
        img_bytes = generate_card_image(include_fake_buttons=False)
        photo = BufferedInputFile(img_bytes, filename="header.png")

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✨ 🎬 JOIN FREE 🪽 ✨", url=PREMIUM_URL)],
            [InlineKeyboardButton(text="✨ 🎬 START HERE 🪽 ✨", url=PREMIUM_URL)],
            [InlineKeyboardButton(text="✨ 🎬 UNLOCK VIP 🪽 ✨", url=PREMIUM_URL)],
            [InlineKeyboardButton(text="✨ 🎬 EXPLORE 🪽 ✨", url=PREMIUM_URL)],
            [InlineKeyboardButton(text="✨ 🎬 JOIN CLUB 🪽 ✨", url=PREMIUM_URL)],
        ])

        await bot.send_photo(
            chat_id=CHANNEL_ID,
            photo=photo,
            caption="🚀 <b>Get Full Access Now</b> ⤵️",
            parse_mode="HTML",
            reply_markup=keyboard
        )
        await status.edit_text("✅ Clickable Post Sent to Channel!")
    except Exception as e:
        await status.edit_text(f"❌ Error: {e}")

# ==========================================================
# 🎨 COMMAND 2: /post_fullcard (Full Card + 1 Main Button)
# ==========================================================
@dp.message(Command("post_fullcard"))
async def send_fullcard_post(message: types.Message):
    status = await message.reply("⏳ Generating Full Card Post...")
    try:
        img_bytes = generate_card_image(include_fake_buttons=True)
        photo = BufferedInputFile(img_bytes, filename="fullcard.png")

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="👉 С L I С K   H E R E 👈", url=PREMIUM_URL)]
        ])

        await bot.send_photo(
            chat_id=CHANNEL_ID,
            photo=photo,
            reply_markup=keyboard
        )
        await status.edit_text("✅ Full Card Sent to Channel!")
    except Exception as e:
        await status.edit_text(f"❌ Error: {e}")

# ==========================================================
# 🌐 RENDER DUMMY WEB SERVER (Keep-Alive Port Binding)
# ==========================================================
async def handle_ping(request):
    return web.Response(text="Bot is running smoothly on Render!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"🌐 Web server listening on port {port}")

async def main():
    await start_web_server()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
