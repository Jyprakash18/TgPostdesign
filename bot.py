import os
import io
import asyncio
import urllib.request
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import BufferedInputFile
from PIL import Image, ImageDraw, ImageFont

# ==========================================
# ⚙️ CONFIGURATION (Apni Details Yahan Dalein)
# ==========================================
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
CHANNEL_ID = os.getenv("CHANNEL_ID", "@your_channel_username")
CHANNEL_TITLE = "MOVIE HUB"
POST_TITLE = "LEAKED PREMIUM VAULT"
PREMIUM_URL = "https://t.me/your_premium_link"
# ==========================================

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Emoji & Thumbnail Cache taaki har baar fast generate ho
ASSET_CACHE = {}

def fetch_image_from_url(url: str, size: tuple) -> Image.Image:
    """HD Emojis aur small thumbnails download karke resize karta hai"""
    cache_key = (url, size)
    if cache_key in ASSET_CACHE:
        return ASSET_CACHE[cache_key]
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            img = Image.open(io.BytesIO(resp.read())).convert("RGBA")
            img = img.resize(size, Image.Resampling.LANCZOS)
            ASSET_CACHE[cache_key] = img
            return img
    except Exception:
        return None

def get_emoji_img(codepoint: str, size: int = 24) -> Image.Image:
    """Twemoji CDN se exact color emoji PNG lata hai"""
    url = f"https://cdnjs.cloudflare.com/ajax/libs/twemoji/14.0.2/72x72/{codepoint}.png"
    return fetch_image_from_url(url, (size, size))

def get_font(size: int, bold: bool = True):
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "arialbd.ttf" if bold else "arial.ttf"
    ]
    for path in font_paths:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()

def generate_abigail_style_card() -> bytes:
    """100% Exact Abigail Red-Circle Screenshot Generator (6 Grid + 6 Colorful Pill Buttons)"""
    width, height = 560, 790
    bg_color = "#17212b"      # Exact Telegram Dark Bubble Color
    border_col = "#2b3948"    # Exact Subtle Table Border
    text_blue = "#7cc5f8"     # Light Blue Grid Text Color (Exact match)

    img = Image.new("RGBA", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    font_grid = get_font(18, False)
    font_cta = get_font(22, False)
    font_btn = get_font(17, True)

    # ----------------------------------------------------
    # 1. TOP 6-BOX GRID TABLE (Exact Red Circle 1)
    # ----------------------------------------------------
    gx1, gy1, gx2, gy2 = 16, 12, 544, 336
    draw.rounded_rectangle([gx1, gy1, gx2, gy2], radius=16, fill="#17212b", outline=border_col, width=2)

    mid_x = width // 2
    row_h = (gy2 - gy1) // 3
    draw.line([(mid_x, gy1), (mid_x, gy2)], fill=border_col, width=2)
    draw.line([(gx1, gy1 + row_h), (gx2, gy1 + row_h)], fill=border_col, width=2)
    draw.line([(gx1, gy1 + 2 * row_h), (gx2, gy1 + 2 * row_h)], fill=border_col, width=2)

    # Grid Data: (Emoji Code, Line 1, Line 2, Thumbnail URL)
    thumb_urls = [
        "https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=100",
        "https://images.unsplash.com/photo-1517604931442-7e0c8ed2963c?w=100",
        "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=100",
        "https://images.unsplash.com/photo-1574375927938-d5a98e8ffe85?w=100",
        "https://images.unsplash.com/photo-1616530940355-351fabd9524b?w=100",
        "https://images.unsplash.com/photo-1518676590629-3dcbd9c5a5c9?w=100",
    ]

    grid_cells = [
        ("1f48b", "KISS", "COMPILATION", thumb_urls[0]),
        ("1f49d", "ONLY FOR", "YOU", thumb_urls[1]),
        ("1f3ac", "FULL", "MOVIES", thumb_urls[2]),
        ("1f525", "LIVE CAMS", "", thumb_urls[3]),
        ("1f48e", "HD", "CONTENT", thumb_urls[4]),
        ("1f51e", "FREE", "VIDEOS", thumb_urls[5]),
    ]

    col_w = (gx2 - gx1) // 2
    for idx, (emo_code, line1, line2, t_url) in enumerate(grid_cells):
        r = idx // 2
        c = idx % 2
        cx = gx1 + c * col_w + col_w // 2
        cy = gy1 + r * row_h + row_h // 2

        # Line 1 + Emoji
        emo_img = get_emoji_img(emo_code, 22)
        tb1 = draw.textbbox((0, 0), line1, font=font_grid)
        w1 = tb1[2] - tb1[0]
        total_w1 = (26 if emo_img else 0) + w1
        start_x1 = cx - total_w1 // 2

        if emo_img:
            img.paste(emo_img, (start_x1, cy - 36), emo_img)
            draw.text((start_x1 + 28, cy - 35), line1, fill=text_blue, font=font_grid)
        else:
            draw.text((start_x1, cy - 35), line1, fill=text_blue, font=font_grid)

        # Line 2 + Small Square Photo
        thumb_img = fetch_image_from_url(t_url, (28, 28))
        if line2:
            tb2 = draw.textbbox((0, 0), line2, font=font_grid)
            w2 = tb2[2] - tb2[0]
            total_w2 = w2 + (34 if thumb_img else 0)
            start_x2 = cx - total_w2 // 2
            draw.text((start_x2, cy - 6), line2, fill=text_blue, font=font_grid)
            if thumb_img:
                img.paste(thumb_img, (start_x2 + w2 + 6, cy - 8))
        else:
            if thumb_img:
                img.paste(thumb_img, (cx - 14, cy - 4))

    # ----------------------------------------------------
    # 2. "Get Full Access Now" + Red Curved Arrow
    # ----------------------------------------------------
    draw.text((18, 378), "Get Full Access Now", fill="#ffffff", font=font_cta)
    # Red Curved Arrow
    draw.arc([255, 370, 298, 415], start=260, end=35, fill="#ff1e56", width=4)
    draw.polygon([(292, 405), (305, 400), (298, 415)], fill="#ff1e56")

    # ----------------------------------------------------
    # 3. 6 COLORFUL PILL BUTTONS (Exact Red Circle 2)
    # ----------------------------------------------------
    wing_emo = get_emoji_img("1fabd", 22)  # 🪽 White Wing Emoji
    zap_emo = get_emoji_img("26a1", 20)    # ⚡ Zap/Spark Emoji

    # (Label, Width, Fill Color, Border Color, Text Color)
    buttons = [
        ("JOIN FREE", 390, "#372936", "#4d3548", "#ff758f"),
        ("START HERE", 420, "#243b35", "#2e5246", "#5ef38c"),
        ("UNLOCK VIP", 420, "#249ef0", "#38bdf8", "#ffffff"),
        ("EXPLORE", 380, "#372936", "#4d3548", "#ff758f"),
        ("ENTER NOW", 420, "#249ef0", "#38bdf8", "#ffffff"),
        ("JOIN CLUB", 400, "#243b35", "#2e5246", "#5ef38c"),
    ]

    y_btn = 435
    for label, bw, b_fill, b_border, t_col in buttons:
        bx1 = (width - bw) // 2
        bx2 = bx1 + bw
        draw.rounded_rectangle([bx1, y_btn, bx2, y_btn + 46], radius=23, fill=b_fill, outline=b_border, width=1)

        # Center Button Text
        tb = draw.textbbox((0, 0), label, font=font_btn)
        tw = tb[2] - tb[0]
        tx = (width - tw) // 2
        ty = y_btn + 13
        draw.text((tx, ty), label, fill=t_col, font=font_btn)

        # Left Emojis (⚡ 🪽)
        if wing_emo:
            img.paste(wing_emo, (tx - 30, y_btn + 12), wing_emo)
        if zap_emo:
            img.paste(zap_emo, (tx - 54, y_btn + 13), zap_emo)

        # Right Emojis (🪽 ⚡)
        if wing_emo:
            img.paste(wing_emo, (tx + tw + 8, y_btn + 12), wing_emo)
        if zap_emo:
            img.paste(zap_emo, (tx + tw + 32, y_btn + 13), zap_emo)

        # Right Small Square Icon (▢)
        draw.rounded_rectangle([bx2 - 26, y_btn + 15, bx2 - 14, y_btn + 27], radius=2, outline=t_col, width=2)

        y_btn += 56

    final_rgb = img.convert("RGB")
    output = io.BytesIO()
    final_rgb.save(output, format="PNG")
    return output.getvalue()

def build_top_text_link() -> str:
    """Photo ke upar dikhne wala Clickable Text Link (Exact Abigail Top Header)"""
    return (
        f"🔥 <b><a href='{PREMIUM_URL}'>{CHANNEL_TITLE} — {POST_TITLE}</a></b>\n"
        f"✨ <b><a href='{PREMIUM_URL}'>CLICK HERE TO UNLOCK FULL ACCESS</a></b> ✨"
    )

# ==========================================================
# 👋 COMMANDS
# ==========================================================
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.reply(
        "✅ <b>Exact Abigail-Style Post Bot Ready!</b>\n\n"
        "👉 /here_inside - Yahi chat mein Exact Red-Circle Box + Photo Textlink banayein\n"
        "👉 /post_inside - Direct Channel mein bhejein",
        parse_mode="HTML"
    )

@dp.message(Command("here_inside"))
async def send_here_inside(message: types.Message):
    status = await message.reply("⏳ Generating Exact Graphic Box...")
    try:
        img_bytes = generate_abigail_style_card()
        photo = BufferedInputFile(img_bytes, filename="card.png")
        # show_caption_above_media=True keeps Text Link on TOP and Card on BOTTOM inside 1 box!
        await message.answer_photo(
            photo=photo,
            caption=build_top_text_link(),
            parse_mode="HTML",
            show_caption_above_media=True
        )
        await status.delete()
    except Exception as e:
        await status.edit_text(f"❌ Error: {e}")

@dp.message(Command("post_inside"))
async def send_channel_inside(message: types.Message):
    status = await message.reply("⏳ Sending to Channel...")
    try:
        img_bytes = generate_abigail_style_card()
        photo = BufferedInputFile(img_bytes, filename="card.png")
        await bot.send_photo(
            chat_id=CHANNEL_ID,
            photo=photo,
            caption=build_top_text_link(),
            parse_mode="HTML",
            show_caption_above_media=True
        )
        await status.edit_text("✅ Successfully Sent to Channel!")
    except Exception as e:
        await status.edit_text(f"❌ Channel Error: {e}")

# ==========================================================
# 🌐 RENDER KEEP-ALIVE WEB SERVER
# ==========================================================
async def handle_ping(request):
    return web.Response(text="Bot is Live!")

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
