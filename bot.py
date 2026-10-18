import os
import json
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, MessageEntity, CopyTextButton

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

SAVED_POST_DATA = {}

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.reply(
        "🔥 <b>Abigail Post Cloner & Native Generator Ready!</b>\n\n"
        "<b>Step 1 (Sabse Best - 100% Same Post):</b>\n"
        "👉 <code>Abigail</code> channel se woh post seedha is bot mein <b>Forward</b> kar dein! Bot turant uska 6-Box Ghar aur Colorful Buttons aapke link (<code>PREMIUM_URL</code>) ke saath bana dega!\n\n"
        "<b>Step 2 (Commands):</b>\n"
        "👉 /generate - Saved post (ya Native Post) yahi chat mein banayein\n"
        "👉 /post_channel - Direct apne Channel mein bhejein\n"
        "👉 /inspect - Forward kiye gaye post ka asli secret structure dekhein",
        parse_mode="HTML"
    )

# ==========================================================
# 🧲 100% EXACT CLONER (Jab aap Abigail se post Forward karenge)
# ==========================================================
@dp.message(F.forward_origin | F.text | F.caption)
async def clone_abigail_post(message: types.Message):
    # Commands ko skip karein
    txt = message.text or message.caption or ""
    if txt.startswith("/"):
        return

    # 1. Text & Entities (6-Box Ghar aur Custom Emojis) निकाले और Link बदले
    raw_entities = message.entities or message.caption_entities or []
    new_entities = []
    for ent in raw_entities:
        d = ent.model_dump()
        if ent.type in ("text_link", "url"):
            d["type"] = "text_link"
            d["url"] = PREMIUM_URL
        new_entities.append(MessageEntity(**d))

    # 2. Inline Keyboard Buttons (Colorful Buttons) निकाले और Link बदले
    new_keyboard = None
    if message.reply_markup and message.reply_markup.inline_keyboard:
        new_rows = []
        for row in message.reply_markup.inline_keyboard:
            btn_row = []
            for btn in row:
                b_dict = btn.model_dump(exclude_none=True)
                # Har button ka link aapke PREMIUM_URL se badal dein
                if "url" in b_dict:
                    b_dict["url"] = PREMIUM_URL
                elif "web_app" in b_dict:
                    b_dict.pop("web_app", None)
                    b_dict["url"] = PREMIUM_URL
                elif "copy_text" in b_dict:
                    b_dict.pop("copy_text", None)
                    b_dict["url"] = PREMIUM_URL
                btn_row.append(InlineKeyboardButton(**b_dict))
            new_rows.append(btn_row)
        new_keyboard = InlineKeyboardMarkup(inline_keyboard=new_rows)

    # Save in memory
    SAVED_POST_DATA["text"] = txt
    SAVED_POST_DATA["entities"] = new_entities
    SAVED_POST_DATA["reply_markup"] = new_keyboard
    SAVED_POST_DATA["raw_dump"] = message.model_dump_json(exclude_none=True, indent=2)

    # Turant wapas bhejein
    await message.answer(
        text=txt,
        entities=new_entities,
        reply_markup=new_keyboard,
        disable_web_page_preview=True
    )
    await message.reply(
        "✅ <b>100% Exact Post Cloned with your Link!</b>\n"
        "👉 Channel mein bhejne ke liye /post_channel dabayein.\n"
        "👉 Iska code dekhne ke liye /inspect dabayein.",
        parse_mode="HTML"
    )

# ==========================================================
# 🔍 /inspect - POST KA ASLI STRUCTURE DEKHEIN
# ==========================================================
@dp.message(Command("inspect"))
async def cmd_inspect(message: types.Message):
    if "raw_dump" not in SAVED_POST_DATA:
        await message.reply("⚠️ Pehle `Abigail` channel se woh post is bot mein Forward karein!")
        return
    dump_str = SAVED_POST_DATA["raw_dump"][:3800]
    await message.reply(f"<pre>{dump_str}</pre>", parse_mode="HTML")

# ==========================================================
# ⚡ /generate & /post_channel
# ==========================================================
@dp.message(Command("generate"))
async def cmd_generate(message: types.Message):
    if "text" in SAVED_POST_DATA:
        await message.answer(
            text=SAVED_POST_DATA["text"],
            entities=SAVED_POST_DATA["entities"],
            reply_markup=SAVED_POST_DATA["reply_markup"],
            disable_web_page_preview=True
        )
    else:
        await message.reply("⚠️ Ek baar `Abigail` channel se woh post is bot (`Khadmod`) ko Forward kar dijiye, phir `/generate` hamesha wahi exact 6-Box Ghar aur Colorful Buttons banayega!")

@dp.message(Command("post_channel"))
async def cmd_post_channel(message: types.Message):
    if "text" not in SAVED_POST_DATA:
        await message.reply("⚠️ Pehle `Abigail` wala post is bot ko Forward karein!")
        return
    try:
        await bot.send_message(
            chat_id=CHANNEL_ID,
            text=SAVED_POST_DATA["text"],
            entities=SAVED_POST_DATA["entities"],
            reply_markup=SAVED_POST_DATA["reply_markup"],
            disable_web_page_preview=True
        )
        await message.reply("✅ 100% Exact Post aapke Channel mein chala gaya!")
    except Exception as e:
        await message.reply(f"❌ Channel Error: {e}")

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
    await dp.start_polling(bot, handle_signals=False)

if __name__ == "__main__":
    asyncio.run(main())
