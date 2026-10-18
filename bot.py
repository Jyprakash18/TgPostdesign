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
PREMIUM_URL = "https://t.me/your_premium_link"  # Aapka apna link jo har button par lagega
# ==========================================

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Saved template (Jab aap post forward karenge toh bot use yahan yaad kar lega)
SAVED_TEXT = None
SAVED_ENTITIES = None

def replace_links_in_entities(entities: list[MessageEntity], new_url: str) -> list[MessageEntity]:
    """Post ke saare Custom Emojis (Buttons/Boxes) ko waisa hi rakhta hai, bas unke andar ka Link aapke PREMIUM_URL se badal deta hai!"""
    if not entities:
        return []
    new_entities = []
    for ent in entities:
        # Copy entity
        ent_dict = ent.model_dump()
        if ent.type == "text_link":
            ent_dict["url"] = new_url
        new_entities.append(MessageEntity(**ent_dict))
    return new_entities

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.reply(
        "🔥 <b>Custom Emoji Post Cloner & Generator Ready!</b>\n\n"
        "<b>Kaise Use Karein (100% Exact Post Ke Liye):</b>\n"
        "1️⃣ <code>https://t.me/pbv2v3omvm0/3</code> par jayein aur us post ko <b>is Bot ko Forward karein</b> (Ya Copy-Paste karke bhejein).\n"
        "2️⃣ Bot turant uske saare Custom Emoji Boxes & Colorful Buttons ke andar <b>aapka PREMIUM_URL</b> laga kar wapas bhej dega!\n"
        "3️⃣ Phir /post_channel dabayein channel mein bhejne ke liye!",
        parse_mode="HTML"
    )

@dp.message(Command("post_channel"))
async def post_to_channel(message: types.Message):
    global SAVED_TEXT, SAVED_ENTITIES
    if not SAVED_TEXT:
        await message.reply("⚠️ Pehle woh post is bot ko Forward ya Copy-Paste karke bhejein!")
        return
    try:
        await bot.send_message(
            chat_id=CHANNEL_ID,
            text=SAVED_TEXT,
            entities=SAVED_ENTITIES,
            disable_web_page_preview=True
        )
        await message.reply("✅ 100% Exact Post aapke Channel mein bhej diya gaya!")
    except Exception as e:
        await message.reply(f"❌ Channel Error: {e}")

# Jab bhi aap koi Custom Emoji / Text-Button wala post bot ko Forward ya Paste karenge:
@dp.message(F.text | F.caption)
async def clone_custom_emoji_post(message: types.Message):
    global SAVED_TEXT, SAVED_ENTITIES

    # Commands ko ignore karein
    if (message.text and message.text.startswith("/")) or (message.caption and message.caption.startswith("/")):
        return

    raw_text = message.text or message.caption
    raw_entities = message.entities or message.caption_entities

    # Saare links ko aapke PREMIUM_URL se replace karein (Custom Emojis 100% safe rahenge!)
    updated_entities = replace_links_in_entities(raw_entities, PREMIUM_URL)

    SAVED_TEXT = raw_text
    SAVED_ENTITIES = updated_entities

    # 1. Turant chat mein naya post bhejein (Bina Forward tag ke + Aapke Link ke saath!)
    await message.answer(
        text=SAVED_TEXT,
        entities=SAVED_ENTITIES,
        disable_web_page_preview=True
    )

    # 2. HTML Code bhi dikhayein taaki aap Title/Text edit kar sakein
    await message.reply(
        "✅ <b>Done! Upar wala post 100% aapke link ke saath tayar hai!</b>\n"
        "👉 Channel mein bhejne ke liye /post_channel dabayein.",
        parse_mode="HTML"
    )

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
