import os
import io
import time
import asyncio
import urllib.request
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BufferedInputFile, LinkPreviewOptions
from PIL import Image, ImageDraw, ImageFont

# ==========================================
# ⚙️ CONFIGURATION (Apni Details Yahan Dalein)
# ==========================================
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
CHANNEL_ID = os.getenv("CHANNEL_ID", "@your_channel_username")
RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL", "") # Render apne aap set karta hai
POST_HEADER = "BEST ❌❌❌ IN ✈️"
ADULT_TEXT = "This content is for adults only"
PREMIUM_URL = "https://t.me/your_premium_link"

# 6 Box ke Naam aur unke Emoji Codes (Apne hisaab se badal sakte hain)
GRID_ITEMS = [
    ("HARDCORE", "1f440"),   # 👀
    ("TEENAGER", "1f51e"),   # 🔞
    ("SPY CAM", "1f4f8"),    # 📸
    ("CHEATING", "2764-fe0f-200d-1f979"), # ❤️‍🩹 (fallback to 1f494)
    ("MASSAGE", "1f975"),    # 🥵
    ("CASTING", "1f3ac"),    # 🎬
]
# ==========================================

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

EMOJI_CACHE = {}
CACHED_CARD_FULL = b""
CACHED_CARD_TOP = b""

def get_emoji_png(code: str, size: int = 26) -> Image.Image:
    """Twemoji CDN se exact Apple/Telegram style HD emoji lata hai"""
    key = (code, size)
    if key in EMOJI_CACHE:
        return EMOJI_CACHE[key]
    urls = [
        f"https://cdnjs.cloudflare.com/ajax/libs/twemoji/14.0.2/72x72/{code}.png",
        "https://cdnjs.cloudflare.com/ajax/libs/twemoji/14.0.2/72x72/2764.png"
    ]
    for url in urls:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=4) as resp:
                im = Image.open(io.BytesIO(resp.read())).convert("RGBA")
                im = im.resize((size, size), Image.Resampling.LANCZOS)
                EMOJI_CACHE[key] = im
                return im
        except Exception:
            continue
    return None

def get_font(size: int, bold: bool = True, serif: bool = False):
    if serif:
        paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        ]
    else:
        paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "arialbd.ttf" if bold else "arial.ttf"
        ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def draw_premierm_card(include_blue_button: bool = True) -> bytes:
    """
    100% Exact 'Premierm Support' Screenshot Generator:
    - 2x3 Rounded Table (HARDCORE, TEENAGER, SPY CAM, CHEATING, MASSAGE, CASTING)
    - '🔞 This content is for adults only ⤵️'
    - Solid Blue Pill Button: '👉 C L I C K   H E R E 👅 ↗'
    """
    width = 600
    height = 540 if include_blue_button else 310
    bg_color = "#17212b"      # Exact Telegram Dark Bubble Color
    border_col = "#293644"    # Subtle Grey-Blue Table Line

    img = Image.new("RGBA", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    font_cell = get_font(21, bold=True, serif=False)
    font_adult = get_font(22, bold=True, serif=True)
    font_btn = get_font(21, bold=False, serif=False)
    font_arrow = get_font(20, bold=True, serif=False)

    # ----------------------------------------------------
    # 1. 6-BOX ROUNDED TABLE (Exact Premierm Support Layout)
    # ----------------------------------------------------
    tx1, ty1, tx2, ty2 = 14, 10, 586, 292
    draw.rounded_rectangle([tx1, ty1, tx2, ty2], radius=18, fill=bg_color, outline=border_col, width=2)

    mid_x = width // 2
    row_h = (ty2 - ty1) // 3
    draw.line([(mid_x, ty1), (mid_x, ty2)], fill=border_col, width=2)
    draw.line([(tx1, ty1 + row_h), (tx2, ty1 + row_h)], fill=border_col, width=2)
    draw.line([(tx1, ty1 + 2 * row_h), (tx2, ty1 + 2 * row_h)], fill=border_col, width=2)

    col_w = (tx2 - tx1) // 2
    for idx, (label, emo_code) in enumerate(GRID_ITEMS):
        r = idx // 2
        c = idx % 2
        cx = tx1 + c * col_w + col_w // 2
        cy = ty1 + r * row_h + row_h // 2

        emo = get_emoji_png(emo_code, 26)
        bbox = draw.textbbox((0, 0), label, font=font_cell)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]

        total_w = tw + (34 if emo else 0)
        start_x = cx - total_w // 2

        draw.text((start_x, cy - th // 2 - 2), label, fill="#ffffff", font=font_cell)
        if emo:
            img.paste(emo, (start_x + tw + 8, cy - 13), emo)

    if include_blue_button:
        # ----------------------------------------------------
        # 2. "🔞 This content is for adults only ⤵️"
        # ----------------------------------------------------
        y_adult = 355
        emo_18 = get_emoji_png("1f51e", 25)
        if emo_18:
            img.paste(emo_18, (16, y_adult), emo_18)

        draw.text((48, y_adult - 1), ADULT_TEXT, fill="#ffffff", font=font_adult)
        ab = draw.textbbox((48, y_adult - 1), ADULT_TEXT, font=font_adult)
        end_x = ab[2] + 10

        # Red Curved Down Arrow (⤵️)
        draw.arc([end_x, y_adult + 2, end_x + 22, y_adult + 24], start=270, end=40, fill="#ff1e56", width=3)
        draw.polygon([(end_x + 18, y_adult + 19), (end_x + 26, y_adult + 17), (end_x + 22, y_adult + 26)], fill="#ff1e56")

        # ----------------------------------------------------
        # 3. SOLID BLUE PILL BUTTON (👉 C L I C K   H E R E 👅 ↗)
        # ----------------------------------------------------
        bx1, by1, bx2, by2 = 14, 435, 586, 505
        draw.rounded_rectangle([bx1, by1, bx2, by2], radius=35, fill="#249ef0")

        btn_text = "C L I C K   H E R E"
        tb = draw.textbbox((0, 0), btn_text, font=font_btn)
        btw = tb[2] - tb[0]
        btx = (width - btw) // 2
        bty = by1 + 22

        # Left Pointing Finger (👉)
        emo_point = get_emoji_png("1f449", 28)
        if emo_point:
            img.paste(emo_point, (btx - 46, by1 + 21), emo_point)

        # Center Spaced White Text
        draw.text((btx, bty), btn_text, fill="#ffffff", font=font_btn)

        # Right Tongue Emoji (👅)
        emo_tongue = get_emoji_png("1f445", 30)
        if emo_tongue:
            img.paste(emo_tongue, (btx + btw + 18, by1 + 21), emo_tongue)

        # Top-Right External Link Arrow (↗) inside blue button
        ax, ay = bx2 - 28, by1 + 14
        draw.line([(ax, ay + 12), (ax + 12, ay)], fill="#ffffff", width=2)
        draw.line([(ax + 3, ay), (ax + 12, ay)], fill="#ffffff", width=2)
        draw.line([(ax + 12, ay), (ax + 12, ay + 9)], fill="#ffffff", width=2)

    out = io.BytesIO()
    img.convert("RGB").save(out, format="PNG")
    return out.getvalue()

# ==========================================================
# 👋 COMMANDS
# ==========================================================
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.reply(
        "✅ <b>Exact 'Premierm Support' Post Bot Ready!</b>\n\n"
        "👉 /generate - Exact 2nd Screenshot Post (6-Box Table + Adult Text + Solid Blue CLICK HERE Button inside box)\n"
        "👉 /post_channel - Direct apne Channel mein bhejein",
        parse_mode="HTML"
    )

@dp.message(Command("generate"))
async def cmd_generate(message: types.Message):
    global CACHED_CARD_FULL
    status = await message.reply("⏳ Generating Exact Premierm Support Post...")
    try:
        if not CACHED_CARD_FULL:
            CACHED_CARD_FULL = draw_premierm_card(include_blue_button=True)

        # Method A: Agar RENDER_EXTERNAL_URL available hai toh LinkPreview se bhejega (No black timestamp box on image!)
        if RENDER_EXTERNAL_URL:
            preview_url = f"{RENDER_EXTERNAL_URL.rstrip('/')}/card.png?v={int(time.time())}"
            text_msg = (
                f"<a href='{preview_url}'>&#8203;</a>"
                f"<b><a href='{PREMIUM_URL}'>· {POST_HEADER}</a></b>\n"
                f"👉 <b><a href='{PREMIUM_URL}'>CLICK HERE TO OPEN LINK</a></b>"
            )
            await message.answer(
                text=text_msg,
                parse_mode="HTML",
                link_preview_options=LinkPreviewOptions(
                    url=preview_url,
                    prefer_large_media=True,
                    show_above_text=False
                )
            )
        else:
            # Fallback: Top Caption + Full Card
            photo = BufferedInputFile(CACHED_CARD_FULL, filename="premierm.png")
            caption = f"<b><a href='{PREMIUM_URL}'>· {POST_HEADER}</a></b>"
            await message.answer_photo(
                photo=photo,
                caption=caption,
                parse_mode="HTML",
                show_caption_above_media=True
            )
        await status.delete()
    except Exception as e:
        await status.edit_text(f"❌ Error: {e}")

@dp.message(Command("post_channel"))
async def cmd_post_channel(message: types.Message):
    global CACHED_CARD_FULL
    status = await message.reply("⏳ Sending to Channel...")
    try:
        if not CACHED_CARD_FULL:
            CACHED_CARD_FULL = draw_premierm_card(include_blue_button=True)

        photo = BufferedInputFile(CACHED_CARD_FULL, filename="premierm.png")
        caption = f"<b><a href='{PREMIUM_URL}'>· {POST_HEADER}</a></b>"
        await bot.send_photo(
            chat_id=CHANNEL_ID,
            photo=photo,
            caption=caption,
            parse_mode="HTML",
            show_caption_above_media=True
        )
        await status.edit_text("✅ Successfully Sent to Channel!")
    except Exception as e:
        await status.edit_text(f"❌ Channel Error: {e}")

# ==========================================================
# 🌐 RENDER WEB SERVER (Serves /card.png for Link Preview)
# ==========================================================
async def handle_ping(request):
    return web.Response(text="Bot is Running!")

async def handle_card_png(request):
    global CACHED_CARD_FULL
    if not CACHED_CARD_FULL:
        CACHED_CARD_FULL = draw_premierm_card(include_blue_button=True)
    return web.Response(body=CACHED_CARD_FULL, content_type="image/png")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle_ping)
    app.router.add_get("/card.png", handle_card_png)
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
