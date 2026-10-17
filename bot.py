import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BufferedInputFile
from playwright.async_api import async_playwright

# ==========================================
# ⚙️ CONFIGURATION (Yahan Apni Details Dalein)
# ==========================================
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
CHANNEL_ID = "@your_channel_username"          # Channel @username ya ID (e.g., -100123456789)
CHANNEL_TITLE = "🎬 MOVIE HUB"                 # Banner ka main title
POST_TITLE = "ALL YOUR ENTERTAINMENT IN ONE PLACE"  # Banner ka subtitle
PREMIUM_URL = "https://t.me/your_premium_link" # Jahan user click karke jayega
BANNER_BG_URL = "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=800"
# ==========================================

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def generate_html(include_fake_buttons: bool = True) -> str:
    """HTML/CSS template jo Movie Hub jaisa exact UI card banata hai"""
    fake_buttons_section = ""
    if include_fake_buttons:
        fake_buttons_section = """
        <div class="divider"></div>
        <div class="cta-title">🚀 Get Full Access Now ⤵️</div>
        <div class="btn btn-pink">✨ 🎬 JOIN FREE 🪽 ✨ <span class="square-icon">▢</span></div>
        <div class="btn btn-green">✨ 🎬 START HERE 🪽 ✨ <span class="square-icon">▢</span></div>
        <div class="btn btn-blue">✨ 🎬 UNLOCK VIP 🪽 ✨ <span class="square-icon">▢</span></div>
        <div class="btn btn-pink">✨ 🎬 EXPLORE 🪽 ✨ <span class="square-icon">▢</span></div>
        <div class="btn btn-green">✨ 🎬 JOIN CLUB 🪽 ✨ <span class="square-icon">▢</span></div>
        <div class="footer">
          <div class="reactions">
            <span class="react">🍿 2</span>
            <span class="react">👍 2</span>
            <span class="react">❤️ 1</span>
          </div>
          <div class="views">👁️ 8,932 &nbsp; 🕒 5:17 AM</div>
        </div>
        """

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8">
    <style>
      body {{
        margin: 0;
        padding: 0;
        background-color: #17212b;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji";
      }}
      .tg-post {{
        width: 500px;
        background-color: #17212b;
        padding: 16px;
        color: white;
        box-sizing: border-box;
      }}
      .banner {{
        width: 100%;
        height: 190px;
        border-radius: 14px;
        background: linear-gradient(90deg, #0b1117 42%, rgba(11,17,23,0.15)), 
                    url('{BANNER_BG_URL}') center/cover;
        display: flex;
        flex-direction: column;
        justify-content: center;
        padding-left: 22px;
        box-sizing: border-box;
        margin-bottom: 14px;
        border: 1px solid #232e3c;
      }}
      .banner h1 {{
        margin: 0;
        font-size: 30px;
        font-weight: 900;
        letter-spacing: 1px;
        color: #ffffff;
        text-shadow: 0 0 14px rgba(59, 130, 246, 0.8);
      }}
      .banner p {{
        margin: 8px 0 14px 0;
        font-size: 14px;
        color: #93c5fd;
        font-weight: 700;
        max-width: 260px;
        line-height: 1.35;
      }}
      .line {{
        width: 65px;
        height: 4px;
        background: #3b82f6;
        border-radius: 2px;
      }}
      .grid-row {{
        display: flex;
        gap: 10px;
        margin-bottom: 10px;
      }}
      .card {{
        background-color: #131c26;
        border: 1px solid #24303f;
        border-radius: 14px;
        padding: 12px 14px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex: 1;
      }}
      .card-left {{
        display: flex;
        align-items: center;
        gap: 12px;
      }}
      .icon-box {{
        width: 44px;
        height: 44px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
      }}
      .blue-icon {{ background: linear-gradient(135deg, #3b82f6, #1d4ed8); }}
      .purple-icon {{ background: linear-gradient(135deg, #8b5cf6, #6d28d9); }}
      .card-title {{ font-size: 15px; font-weight: 700; margin: 0; color: #f8fafc; }}
      .card-sub {{ font-size: 12px; color: #7f91a4; margin: 3px 0 0 0; }}
      .arrow {{ color: #5c6c7c; font-size: 22px; font-weight: bold; }}
      .divider {{
        height: 1px;
        background: #232e3c;
        margin: 16px -16px;
      }}
      .cta-title {{
        font-size: 20px;
        font-weight: 700;
        margin: 6px 0 16px 6px;
      }}
      .btn {{
        width: 90%;
        margin: 0 auto 10px auto;
        padding: 13px 18px;
        border-radius: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        font-size: 15px;
        letter-spacing: 0.6px;
        position: relative;
        box-sizing: border-box;
      }}
      .btn-pink {{
        background: rgba(131, 56, 75, 0.35);
        border: 1.5px solid #7c3548;
        color: #f472b6;
      }}
      .btn-green {{
        background: rgba(20, 83, 45, 0.45);
        border: 1.5px solid #16a34a;
        color: #4ade80;
      }}
      .btn-blue {{
        background: #1d9bf0;
        border: 1.5px solid #38bdf8;
        color: #ffffff;
      }}
      .square-icon {{
        position: absolute;
        right: 18px;
        font-size: 14px;
      }}
      .footer {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 16px;
        padding-top: 4px;
      }}
      .reactions {{ display: flex; gap: 8px; }}
      .react {{
        background: #202b36;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
        color: #e2e8f0;
      }}
      .views {{ font-size: 12px; color: #6c7883; }}
    </style>
    </head>
    <body>
    <div class="tg-post" id="card">
      <div class="banner">
        <h1>{CHANNEL_TITLE}</h1>
        <p>{POST_TITLE}</p>
        <div class="line"></div>
      </div>

      <div class="grid-row">
        <div class="card">
          <div class="card-left">
            <div class="icon-box blue-icon">🎬</div>
            <div>
              <p class="card-title">Browse Movies</p>
              <p class="card-sub">Find your next watch</p>
            </div>
          </div>
          <span class="arrow">›</span>
        </div>

        <div class="card">
          <div class="card-left">
            <div class="icon-box blue-icon">🖥️</div>
            <div>
              <p class="card-title">Video Quality</p>
              <p class="card-sub">View available formats</p>
            </div>
          </div>
          <span class="arrow">›</span>
        </div>
      </div>

      <div class="card">
        <div class="card-left">
          <div class="icon-box purple-icon">👑</div>
          <div>
            <p class="card-title">Premium Membership</p>
            <p class="card-sub">See plans and benefits</p>
          </div>
        </div>
        <span class="arrow">›</span>
      </div>

      {fake_buttons_section}
    </div>
    </body>
    </html>
    """

async def render_html_to_image(include_fake_buttons: bool) -> bytes:
    """Playwright se HTML ko HD PNG bytes mein convert karta hai"""
    html_content = generate_html(include_fake_buttons)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 500, "height": 900}, device_scale_factor=2)
        await page.set_content(html_content, wait_until="networkidle")
        card_element = await page.query_selector("#card")
        image_bytes = await card_element.screenshot(type="png")
        await browser.close()
        return image_bytes

# ==========================================================
# 🚀 COMMAND 1: /post_clickable (Photo + 5 Real Buttons)
# ==========================================================
@dp.message(Command("post_clickable"))
async def send_clickable_post(message: types.Message):
    status_msg = await message.reply("⏳ <b>Generating Clickable Post...</b>", parse_mode="HTML")
    try:
        # Sirf Upar ke Banner + 3 Cards ki photo banayega
        img_bytes = await render_html_to_image(include_fake_buttons=False)
        photo = BufferedInputFile(img_bytes, filename="post_header.png")

        # 5 Asli Clickable Telegram Buttons
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
        await status_msg.edit_text("✅ <b>Clickable Post Successfully Sent to Channel!</b>", parse_mode="HTML")
    except Exception as e:
        await status_msg.edit_text(f"❌ Error: {e}")

# ==========================================================
# 🎨 COMMAND 2: /post_fullcard (Exact Screenshot Image)
# ==========================================================
@dp.message(Command("post_fullcard"))
async def send_fullcard_post(message: types.Message):
    status_msg = await message.reply("⏳ <b>Generating Full Graphic Card...</b>", parse_mode="HTML")
    try:
        # Pura card (colorful buttons ke saath) ek single image mein banayega
        img_bytes = await render_html_to_image(include_fake_buttons=True)
        photo = BufferedInputFile(img_bytes, filename="movie_hub_full.png")

        # Neeche 1 Main Clickable Button
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="👉 С L I С K   H E R E   T O   J O I N 👈", url=PREMIUM_URL)]
        ])

        await bot.send_photo(
            chat_id=CHANNEL_ID,
            photo=photo,
            reply_markup=keyboard
        )
        await status_msg.edit_text("✅ <b>Full Card Post Successfully Sent to Channel!</b>", parse_mode="HTML")
    except Exception as e:
        await status_msg.edit_text(f"❌ Error: {e}")

async def main():
    print("🤖 Bot chalu ho gaya hai! Apne bot ko /post_clickable ya /post_fullcard bhejein.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
