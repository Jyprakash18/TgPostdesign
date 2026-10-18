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
# ⚙️ CONFIGURATION
# ==========================================
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
CHANNEL_ID = os.getenv("CHANNEL_ID", "@your_channel_username")
POST_HEADER = "BEST ❌❌❌ IN"
ADULT_TEXT = "This content is for adults only"
PREMIUM_URL = "https://t.me/your_premium_link"

GRID_ITEMS = [
    ("HARDCORE", "1f440"),   # 👀
    ("TEENAGER", "1f51e"),   # 🔞
    ("SPY CAM", "1f4f8"),    # 📸
    ("CHEATING", "1f494"),   # 💔/❤️‍🩹
    ("MASSAGE", "1f975"),    # 🥵
    ("CASTING", "1f3ac"),    # 🎬
]
# ==========================================

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
EMOJI_CACHE = {}

def get_emoji_png(code: str, size: int = 26) -> Image.Image:
    key = (code, size)
    if key in EMOJI_CACHE:
        return EMOJI_CACHE[key]
    url = f"https://cdnjs.cloudflare.com/ajax/libs/twemoji/14.0.2/72x72/{code}.png"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=4) as resp:
            im = Image.open(io.BytesIO(resp.read())).convert("RGBA")
            im = im.resize((size, size), Image.Resampling.LANCZOS)
            EMOJI_CACHE[key] = im
            return im
    except Exception:
        return None

def get_font(size: int, bold: bool = True, serif: bool = False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf" if serif else "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "arialbd.ttf"
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def create_exact_box_design() -> bytes:
    """
    Exact Red-Circle 6-Box Grid Table banavto (Seamless Telegram Dark Background sahit)
    """
    width, height = 600, 380
    bg_color = "#18222d"      # Exact Telegram Dark Message Bubble Color
    border_col = "#2b3847"    # Subtle Thin Rounded Grid Border

    img = Image.new("RGBA", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    font_header = get_font(23, bold=True, serif=True)
    font_cell = get_font(20, bold=True, serif=False)

    # 1. Top Header: "· BEST ❌❌❌ IN ✈️"
    draw.text((28, 22), "·", fill="#ff4d6d", font=font_header)
    draw.text((48, 22), "BEST", fill="#ffffff", font=font_header)
    
    emo_x = get_emoji_png("274c", 22)
    x_pos = 122
    for _ in range(3):
        if emo_x:
            img.paste(emo_x, (x_pos, 24), emo_x)
        x_pos += 26
    
    draw.text((x_pos + 4, 22), "IN", fill="#ffffff", font=font_header)

    # 2. 6-Box Rounded Table (2 Columns x 3 Rows)
    tx1, ty1, tx2, ty2 = 20, 72, 580, 355
    draw.rounded_rectangle([tx1, ty1, tx2, ty2], radius=16, fill=bg_color, outline=border_col, width=2)

    # Vertical Center Line
    mid_x = width // 2
    draw.line([(mid_x, ty1), (mid_x, ty2)], fill=border_col, width=2)

    # 2 Horizontal Row Lines
    row_h = (ty2 - ty1) // 3
    draw.line([(tx1, ty1 + row_h), (tx2, ty1 + row_h)], fill=border_col, width=2)
    draw.line([(tx1, ty1 + 2 * row_h), (tx2, ty1 + 2 * row_h)], fill=border_col, width=2)

    # Fill 6 Cells with Text + Emoji
    col_w = (tx2 - tx1) // 2
    for idx, (label, emo_code) in enumerate(GRID_ITEMS):
        r = idx // 2
        c = idx % 2
        cx = tx1 + c * col_w + col_w // 2
        cy = ty1 + r * row_h + row_h // 2

        emo = get_emoji_png(emo_code, 24)
        bbox = draw.textbbox((0, 0), label, font=font_cell)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]

        total_w = tw + (32 if emo else 0)
        start_x = cx - total_w // 2

        draw.text((start_x, cy - th // 2 - 2), label, fill="#ffffff", font=font_cell)
        if emo:
            img.paste(emo, (start_x + tw + 8, cy - 12), emo)

    out = io.BytesIO()
    img.convert("RGB").save(out, format="PNG")
    return out.getvalue()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.reply(
        "✅ <b>6-Box Design Generator Ready!</b>\n\n"
        "👉 /generate - Yahi chat madhye 6-Box Design + Clickable Button tayar kara\n"
        "👉 /post_channel - Direct Channel madhye pathva",
        parse_mode="HTML"
    )

@dp.message(Command("generate"))
async def cmd_generate(message: types.Message):
    img_bytes = create_exact_box_design()
    photo = BufferedInputFile(img_bytes, filename="box_grid.png")

    # Clickable Button khali
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👉 С L I С K   H E R E 👅", url=PREMIUM_URL)]
    ])

    await message.answer_photo(
        photo=photo,
        caption=f"🔞 <b><a href='{PREMIUM_URL}'>{ADULT_TEXT}</a></b> ⤵️",
        parse_mode="HTML",
        reply_markup=keyboard
    )

@dp.message(Command("post_channel"))
async def cmd_post_channel(message: types.Message):
    try:
        img_bytes = create_exact_box_design()
        photo = BufferedInputFile(img_bytes, filename="box_grid.png")
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="👉 С L I С K   H E R E 👅", url=PREMIUM_URL)]
        ])
        await bot.send_photo(
            chat_id=CHANNEL_ID,
            photo=photo,
            caption=f"🔞 <b><a href='{PREMIUM_URL}'>{ADULT_TEXT}</a></b> ⤵️",
            parse_mode="HTML",
            reply_markup=keyboard
        )
        await message.reply("✅ Channel madhye post pathvli ahe!")
    except Exception as e:
        await message.reply(f"❌ Error: {e}")

async def handle_ping(request):
    return web.Response(text="Bot is Running!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

async def main():
    await start_web_server()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
