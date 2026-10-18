import os
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import MessageEntity

# ==========================================
# ⚙️ CONFIGURATION (Apni Details Yahan Dalein)
# ==========================================
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
CHANNEL_ID = os.getenv("CHANNEL_ID", "@your_channel_username")
CHANNEL_TITLE = "🎬 MOVIE HUB"
POST_TITLE = "LEAKED PREMIUM VAULT"
PREMIUM_URL = "https://t.me/your_premium_link"
# ==========================================

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

SAVED_TEXT = None
SAVED_ENTITIES = None

def generate_text_post_structure() -> str:
    """
    Bina kisi Photo ke 100% Text-based 6-Box Grid + 6 Clickable Text Buttons
    generate karta hai (Jismein har item par PREMIUM_URL laga hai).
    """
    return (
        f"<b><a href='{PREMIUM_URL}'>{CHANNEL_TITLE}</a> — {POST_TITLE}</b>\n\n"
        f"<code>┌───────────────┬───────────────┐</code>\n"
        f"<code>│</code> 💋 <a href='{PREMIUM_URL}'><b>KISS</b></a>       <code>│</code> 💝 <a href='{PREMIUM_URL}'><b>ONLY FOR</b></a>   <code>│</code>\n"
        f"<code>│</code> <a href='{PREMIUM_URL}'><b>COMPILATION</b></a>  <code>│</code>    <a href='{PREMIUM_URL}'><b>YOU</b></a> 🔥    <code>│</code>\n"
        f"<code>├───────────────┼───────────────┤</code>\n"
        f"<code>│</code> 🎬 <a href='{PREMIUM_URL}'><b>FULL</b></a>       <code>│</code> 🔥 <a href='{PREMIUM_URL}'><b>LIVE CAMS</b></a>  <code>│</code>\n"
        f"<code>│</code> <a href='{PREMIUM_URL}'><b>MOVIES</b></a> 🍿     <code>│</code>    <a href='{PREMIUM_URL}'><b>WATCH</b></a> 📸  <code>│</code>\n"
        f"<code>├───────────────┼───────────────┤</code>\n"
        f"<code>│</code> 💎 <a href='{PREMIUM_URL}'><b>HD</b></a>         <code>│</code> 🔞 <a href='{PREMIUM_URL}'><b>FREE</b></a>       <code>│</code>\n"
        f"<code>│</code> <a href='{PREMIUM_URL}'><b>CONTENT</b></a> 📺    <code>│</code> <a href='{PREMIUM_URL}'><b>VIDEOS</b></a> 🔓     <code>│</code>\n"
        f"<code>└───────────────┴───────────────┘</code>\n\n"
        f"<b>Get Full Access Now</b> ⤵️\n\n"
        f"        ⚡ 🪽 <a href='{PREMIUM_URL}'><b>JOIN FREE</b></a> 🪽 ⚡\n\n"
        f"       ⚡ 🪽 <a href='{PREMIUM_URL}'><b>START HERE</b></a> 🪽 ⚡\n\n"
        f"       ⚡ 🪽 <a href='{PREMIUM_URL}'><b>UNLOCK VIP</b></a> 🪽 ⚡\n\n"
        f"         ⚡ 🪽 <a href='{PREMIUM_URL}'><b>EXPLORE</b></a> 🪽 ⚡\n\n"
        f"       ⚡ 🪽 <a href='{PREMIUM_URL}'><b>ENTER NOW</b></a> 🪽 ⚡\n\n"
        f"       ⚡ 🪽 <a href='{PREMIUM_URL}'><b>JOIN CLUB</b></a> 🪽 ⚡"
    )

# ==========================================================
# 👋 /start COMMAND
# ==========================================================
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.reply(
        "✅ <b>Pure Text Post Generator Bot Ready!</b>\n\n"
        "<b>Direct Commands:</b>\n"
        "👉 /generate - Yahi chat mein Pure Text Post (Grid + 6 Text Buttons) generate karein\n"
        "👉 /post_channel - Direct apne Telegram Channel mein post bhejein\n\n"
        "<b>Custom Emoji Cloner:</b>\n"
        "💡 <i>Agar aap kisi doosre channel ka post yahan Forward ya Copy-Paste karenge, toh bot uske saare links badal kar aapka PREMIUM_URL laga dega!</i>",
        parse_mode="HTML"
    )

# ==========================================================
# ⚡ /generate - DIRECT YAHI CHAT MEIN POST BANAYEIN
# ==========================================================
@dp.message(Command("generate"))
async def cmd_generate(message: types.Message):
    post_html = generate_text_post_structure()
    await message.answer(
        text=post_html,
        parse_mode="HTML",
        disable_web_page_preview=True
    )

# ==========================================================
# 📢 /post_channel - DIRECT CHANNEL MEIN BHEJEIN
# ==========================================================
@dp.message(Command("post_channel"))
async def cmd_post_channel(message: types.Message):
    global SAVED_TEXT, SAVED_ENTITIES
    try:
        # Agar user ne koi custom emoji post forward kiya tha, toh woh bhejein, warna default structure bhejein
        if SAVED_TEXT:
            await bot.send_message(
                chat_id=CHANNEL_ID,
                text=SAVED_TEXT,
                entities=SAVED_ENTITIES,
                disable_web_page_preview=True
            )
        else:
            await bot.send_message(
                chat_id=CHANNEL_ID,
                text=generate_text_post_structure(),
                parse_mode="HTML",
                disable_web_page_preview=True
            )
        await message.reply("✅ Post Successfully Channel mein bhej diya gaya!")
    except Exception as e:
        await message.reply(
            f"❌ <b>Channel Error:</b> {e}\n\n"
            f"👉 <i>Check karein ki bot channel mein Admin hai aur CHANNEL_ID sahi hai.</i>",
            parse_mode="HTML"
        )

# ==========================================================
# 🔄 AUTO-CLONER (Forward ya Copy-Paste karne par Link Replace karega)
# ==========================================================
@dp.message(F.text | F.caption)
async def clone_any_post(message: types.Message):
    global SAVED_TEXT, SAVED_ENTITIES

    raw_text = message.text or message.caption
    if raw_text.startswith("/"):
        return

    raw_entities = message.entities or message.caption_entities or []
    updated_entities = []

    for ent in raw_entities:
        data = ent.model_dump()
        if ent.type in ("text_link", "url"):
            data["type"] = "text_link"
            data["url"] = PREMIUM_URL
        updated_entities.append(MessageEntity(**data))

    SAVED_TEXT = raw_text
    SAVED_ENTITIES = updated_entities

    await message.answer(
        text=SAVED_TEXT,
        entities=SAVED_ENTITIES,
        disable_web_page_preview=True
    )
    await message.reply("✅ <b>Links Replaced with your PREMIUM_URL!</b>\nChannel mein bhejne ke liye /post_channel dabayein.", parse_mode="HTML")

# ==========================================================
# 🌐 RENDER KEEP-ALIVE WEB SERVER
# ==========================================================
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
