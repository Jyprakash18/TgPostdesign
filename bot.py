import os
import io
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import BufferedInputFile, LinkPreviewOptions
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

# Latest generated image ko RAM mein rakhne ke liye taaki Telegram Link Preview use message ke ANDAR dikha sake
LATEST_CARD_BYTES = b""

def get_font(size: int, bold: bool = True):
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "arialbd.ttf" if bold else "arial.ttf"
    ]
    for path in font_paths:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()

def generate_exact_inside_card() -> bytes:
    """Bilkul Abigail/Movie Hub jaisa اندرونی (Inside-Message) Card banata hai (Bina square [] boxes ke)"""
    width, height = 600, 760
    bg_color = "#17212b"      # Exact Telegram Dark Message Background
    card_bg = "#131c26"
    border_col = "#263445"

    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    font_title = get_font(19, True)
    font_desc = get_font(14, False)
    font_cta = get_font(23, True)
    font_btn = get_font(18, True)

    # 1. 6-Box Grid Table (Bilkul 2nd Screenshot Jaisa)
    grid_top, grid_bottom = 15, 315
    grid_left, grid_right = 20, 580
    draw.rounded_rectangle([grid_left, grid_top, grid_right, grid_bottom], radius=16, fill=card_bg, outline=border_col, width=2)
    
    # Vertical & Horizontal Grid Lines
    mid_x = width // 2
    draw.line([(mid_x, grid_top), (mid_x, grid_bottom)], fill=border_col, width=2)
    draw.line([(grid_left, 115), (grid_right, 115)], fill=border_col, width=2)
    draw.line([(grid_left, 215), (grid_right, 215)], fill=border_col, width=2)

    grid_items = [
        ("BROWSE MOVIES", "Find your next watch", "#38bdf8"),
        ("ONLY FOR YOU", "Exclusive collection", "#f472b6"),
        ("FULL MOVIES", "4K & 1080p Bluray", "#4ade80"),
        ("LIVE STREAMS", "Watch non-stop", "#fb923c"),
        ("HD CONTENT", "All formats ready", "#a78bfa"),
        ("FREE VIDEOS", "Instant access", "#f87171"),
    ]

    for idx, (title, sub, col) in enumerate(grid_items):
        r = idx // 2
        c = idx % 2
        cx = grid_left + (c * 280) + 140
        cy = grid_top + (r * 100) + 50

        tb = draw.textbbox((0, 0), title, font=font_title)
        tw = tb[2] - tb[0]
        draw.text((cx - tw // 2, cy - 20), title, fill=col, font=font_title)

        sb = draw.textbbox((0, 0), sub, font=font_desc)
        sw = sb[2] - sb[0]
        draw.text((cx - sw // 2, cy + 6), sub, fill="#8a9aa9", font=font_desc)

    # 2. "Get Full Access Now" Section
    draw.text((25, 345), "Get Full Access Now", fill="#ffffff", font=font_cta)
    # Red Curved Arrow Draw
    draw.arc([275, 340, 315, 380], start=270, end=45, fill="#f43f5e", width=4)
    draw.polygon([(312, 368), (322, 365), (315, 377)], fill="#f43f5e")

    # 3. 6 Pill-Shaped Colorful Buttons (Inside Image)
    buttons = [
        ("JOIN FREE", "#3b202c", "#7c3548", "#f472b6"),
        ("START HERE", "#143325", "#16a34a", "#4ade80"),
        ("UNLOCK VIP", "#1d9bf0", "#38bdf8", "#ffffff"),
        ("EXPLORE", "#3b202c", "#7c3548", "#f472b6"),
        ("ENTER NOW", "#1d9bf0", "#38bdf8", "#ffffff"),
        ("JOIN CLUB", "#143325", "#16a34a", "#4ade80"),
    ]

    y_start = 400
    for label, bg_btn, border_btn, txt_col in buttons:
        draw.rounded_rectangle([65, y_start, 535, y_start + 46], radius=23, fill=bg_btn, outline=border_btn, width=2)
        
        text_str = f"⚡  {label}  ⚡"
        bbox = draw.textbbox((0, 0), text_str, font=font_btn)
        tw = bbox[2] - bbox[0]
        draw.text(((width - tw) // 2, y_start + 12), text_str, fill=txt_col, font=font_btn)
        
        # Small square icon on right (exact screenshot match)
        draw.rounded_rectangle([500, y_start + 16, 514, y_start + 30], radius=3, outline=txt_col, width=2)
        y_start += 56

    output = io.BytesIO()
    img.save(output, format="PNG")
    return output.getvalue()

# ==========================================================
# 👋 /start COMMAND
# ==========================================================
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.reply(
        "✅ <b>Inside-Text Post Generator Ready!</b>\n\n"
        "<b>Bina Bahari Grey Buttons ke (100% Text ke andar):</b>\n"
        "👉 /here_textbtn - Sare Clickable Buttons Text ke andar\n"
        "👉 /here_inside - Exact Screenshot Design (Bina bahari button ke)\n\n"
        "<b>Direct Channel Mein Bhejne Ke Liye:</b>\n"
        "👉 /post_textbtn - Channel mein Text-Buttons bhejein\n"
        "👉 /post_inside - Channel mein Exact Screenshot post bhejein",
        parse_mode="HTML"
    )

# ==========================================================
# 🔥 MODE 1: SARE BUTTONS PURE TEXT KE ANDAR (100% Clickable)
# ==========================================================
def build_in_text_post() -> str:
    """Sare buttons aur grid pure Telegram Text ke andar clickable links ke roop mein"""
    return (
        f"🎬 <b><a href='{PREMIUM_URL}'>{CHANNEL_TITLE} — {POST_TITLE}</a></b>\n\n"
        f"<blockquote>"
        f"🍿 <a href='{PREMIUM_URL}'><b>BROWSE MOVIES</b></a>   ┃   💎 <a href='{PREMIUM_URL}'><b>4K ULTRA HD</b></a>\n"
        f"────────────────────────\n"
        f"🔥 <a href='{PREMIUM_URL}'><b>TRENDING NOW</b></a>    ┃   📺 <a href='{PREMIUM_URL}'><b>WEB SERIES</b></a>\n"
        f"────────────────────────\n"
        f"👑 <a href='{PREMIUM_URL}'><b>PREMIUM VIP</b></a>     ┃   🔓 <a href='{PREMIUM_URL}'><b>FREE VIDEOS</b></a>"
        f"</blockquote>\n\n"
        f"🚀 <b>Get Full Access Now</b> ⤵️\n\n"
        f"<blockquote>      ✨ 🎬 <a href='{PREMIUM_URL}'><b>J O I N   F R E E</b></a> 🪽 ✨      ▢</blockquote>\n"
        f"<blockquote>     ✨ 🎬 <a href='{PREMIUM_URL}'><b>S T A R T   H E R E</b></a> 🪽 ✨     ▢</blockquote>\n"
        f"<blockquote>     ✨ 🎬 <a href='{PREMIUM_URL}'><b>U N L O C K   V I P</b></a> 🪽 ✨     ▢</blockquote>\n"
        f"<blockquote>       ✨ 🎬 <a href='{PREMIUM_URL}'><b>E X P L O R E</b></a> 🪽 ✨       ▢</blockquote>\n"
        f"<blockquote>     ✨ 🎬 <a href='{PREMIUM_URL}'><b>E N T E R   N O W</b></a> 🪽 ✨     ▢</blockquote>\n"
        f"<blockquote>     ✨ 🎬 <a href='{PREMIUM_URL}'><b>J O I N   C L U B</b></a> 🪽 ✨     ▢</blockquote>"
    )

@dp.message(Command("here_textbtn"))
async def send_here_textbtn(message: types.Message):
    await message.answer(
        text=build_in_text_post(),
        parse_mode="HTML",
        disable_web_page_preview=True
    )

@dp.message(Command("post_textbtn"))
async def send_channel_textbtn(message: types.Message):
    try:
        await bot.send_message(
            chat_id=CHANNEL_ID,
            text=build_in_text_post(),
            parse_mode="HTML",
            disable_web_page_preview=True
        )
        await message.reply("✅ Text-Button Post Channel mein bhej diya gaya!")
    except Exception as e:
        await message.reply(f"❌ Channel Error: {e}")

# ==========================================================
# 🎨 MODE 2: EXACT SCREENSHOT (Image + Text Inside 1 Box, NO Grey Buttons)
# ==========================================================
def build_caption_with_in_text_links() -> str:
    return (
        f"🔥 <b><a href='{PREMIUM_URL}'>{CHANNEL_TITLE}</a> — {POST_TITLE}</b>\n\n"
        f"⚡ <a href='{PREMIUM_URL}'><b>JOIN FREE</b></a>  |  "
        f"🚀 <a href='{PREMIUM_URL}'><b>START HERE</b></a>  |  "
        f"👑 <a href='{PREMIUM_URL}'><b>UNLOCK VIP</b></a>"
    )

@dp.message(Command("here_inside"))
async def send_here_inside(message: types.Message):
    img_bytes = generate_exact_inside_card()
    photo = BufferedInputFile(img_bytes, filename="inside_card.png")
    # show_caption_above_media=True se Text UPAR aayega aur Card NEECHE (Exact Abigail screenshot jaisa!)
    # Aur koi bahari grey button nahi hoga!
    await message.answer_photo(
        photo=photo,
        caption=build_caption_with_in_text_links(),
        parse_mode="HTML",
        show_caption_above_media=True
    )

@dp.message(Command("post_inside"))
async def send_channel_inside(message: types.Message):
    try:
        img_bytes = generate_exact_inside_card()
        photo = BufferedInputFile(img_bytes, filename="inside_card.png")
        await bot.send_photo(
            chat_id=CHANNEL_ID,
            photo=photo,
            caption=build_caption_with_in_text_links(),
            parse_mode="HTML",
            show_caption_above_media=True
        )
        await message.reply("✅ Exact Inside-Box Post Channel mein bhej diya gaya!")
    except Exception as e:
        await message.reply(f"❌ Channel Error: {e}")

# ==========================================================
# 🌐 RENDER WEB SERVER
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

