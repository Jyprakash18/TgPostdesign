import os
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, MessageEntity

# ==========================================
# ⚙️ CONFIGURATION (Apni Details Yahan Dalein)
# ==========================================
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
CHANNEL_ID = os.getenv("CHANNEL_ID", "@your_channel_username")
POST_HEADER = "· BEST ❌❌❌ IN ✈️"
ADULT_TEXT = "🔞 This content is for adults only ⤵️"
PREMIUM_URL = "https://t.me/your_premium_link"
# ==========================================

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

SAVED_CUSTOM_TEXT = None
SAVED_CUSTOM_ENTITIES = None

def get_pure_text_box_message() -> str:
    """
    100% Pure Text Message (NO IMAGE!).
    Ismein <code> ke andar clickable links hain taaki mobile par 6-Box ki ek bhi line aage-peeche na ho!
    """
    return (
        f"<b><a href='{PREMIUM_URL}'>{POST_HEADER}</a></b>\n\n"
        f"<code>╭─────────────┬─────────────╮</code>\n"
        f"<code>│ </code><a href='{PREMIUM_URL}'><code>HARDCORE</code></a> 👀<code> │ </code><a href='{PREMIUM_URL}'><code>TEENAGER</code></a> 🔞<code> │</code>\n"
        f"<code>├─────────────┼─────────────┤</code>\n"
        f"<code>│ </code><a href='{PREMIUM_URL}'><code>SPY CAM </code></a> 📸<code> │ </code><a href='{PREMIUM_URL}'><code>CHEATING</code></a> ❤️‍🩹<code> │</code>\n"
        f"<code>├─────────────┼─────────────┤</code>\n"
        f"<code>│ </code><a href='{PREMIUM_URL}'><code>MASSAGE </code></a> 🥵<code> │ </code><a href='{PREMIUM_URL}'><code>CASTING </code></a> 🎬<code> │</code>\n"
        f"<code>╰─────────────┴─────────────╯</code>\n\n"
        f"<b><a href='{PREMIUM_URL}'>{ADULT_TEXT}</a></b>"
    )

def get_bottom_button() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👉 С L I С K   H E R E 👅", url=PREMIUM_URL)]
    ])

# ==========================================================
# 👋 /start COMMAND
# ==========================================================
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.reply(
        "✅ <b>100% Pure Text Post Bot Ready! (No Image!)</b>\n\n"
        "👉 /generate - Yahi chat mein <b>Pure Text Message</b> (6-Box + Link) banayein\n"
        "👉 /post_channel - Direct apne Channel mein Text Post bhejein\n\n"
        "💡 <b>Pro Trick:</b> Kisi bhi channel ka Custom Emoji Box wala post yahan Forward ya Copy-Paste karein—bot use aapke link ke saath clone kar dega!",
        parse_mode="HTML"
    )

# ==========================================================
# 💬 /generate - 100% TEXT MESSAGE (NO PHOTO!)
# ==========================================================
@dp.message(Command("generate"))
async def cmd_generate(message: types.Message):
    global SAVED_CUSTOM_TEXT, SAVED_CUSTOM_ENTITIES

    if SAVED_CUSTOM_TEXT:
        await message.answer(
            text=SAVED_CUSTOM_TEXT,
            entities=SAVED_CUSTOM_ENTITIES,
            disable_web_page_preview=True,
            reply_markup=get_bottom_button()
        )
    else:
        await message.answer(
            text=get_pure_text_box_message(),
            parse_mode="HTML",
            disable_web_page_preview=True,
            reply_markup=get_bottom_button()
        )

# ==========================================================
# 📢 /post_channel - DIRECT CHANNEL MEIN TEXT POST BHEJEIN
# ==========================================================
@dp.message(Command("post_channel"))
async def cmd_post_channel(message: types.Message):
    global SAVED_CUSTOM_TEXT, SAVED_CUSTOM_ENTITIES
    try:
        if SAVED_CUSTOM_TEXT:
            await bot.send_message(
                chat_id=CHANNEL_ID,
                text=SAVED_CUSTOM_TEXT,
                entities=SAVED_CUSTOM_ENTITIES,
                disable_web_page_preview=True,
                reply_markup=get_bottom_button()
            )
        else:
            await bot.send_message(
                chat_id=CHANNEL_ID,
                text=get_pure_text_box_message(),
                parse_mode="HTML",
                disable_web_page_preview=True,
                reply_markup=get_bottom_button()
            )
        await message.reply("✅ Pure Text Post Channel mein bhej diya gaya!")
    except Exception as e:
        await message.reply(f"❌ Channel Error: {e}")

# ==========================================================
# 🧲 CUSTOM EMOJI BOX CLONER (Forward/Paste Handler)
# ==========================================================
@dp.message(F.text | F.caption)
async def clone_exact_text_box(message: types.Message):
    global SAVED_CUSTOM_TEXT, SAVED_CUSTOM_ENTITIES

    raw_text = message.text or message.caption
    if not raw_text or raw_text.startswith("/"):
        return

    raw_entities = message.entities or message.caption_entities or []
    new_entities = []

    for ent in raw_entities:
        data = ent.model_dump()
        if ent.type in ("text_link", "url"):
            data["type"] = "text_link"
            data["url"] = PREMIUM_URL
        new_entities.append(MessageEntity(**data))

    SAVED_CUSTOM_TEXT = raw_text
    SAVED_CUSTOM_ENTITIES = new_entities

    await message.answer(
        text=SAVED_CUSTOM_TEXT,
        entities=SAVED_CUSTOM_ENTITIES,
        disable_web_page_preview=True,
        reply_markup=get_bottom_button()
    )
    await message.reply(
        "✅ <b>Exact Text Box Saved!</b>\n"
        "Ab jab bhi aap /generate ya /post_channel dabayenge, yahi exact Text Post aapke link ke saath jayega!",
        parse_mode="HTML"
    )

# ==========================================================
# 🌐 RENDER KEEP-ALIVE WEB SERVER (Fast Deploy Fix)
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
    await dp.start_polling(bot, handle_signals=False)

if __name__ == "__main__":
    asyncio.run(main())
