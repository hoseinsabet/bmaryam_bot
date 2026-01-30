import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# ------------------ تنظیمات ------------------
TOKEN = "8502895403:AAFR5Biw4xVNQ_VLg7aDp0SqIeM2yYg8pno"
CHANNELS = ["@bmaryamfal", "@shamtrapp"]
SUPPORT = "@thesabet"

# ---------- فال‌ها ----------
daily_fals = [
    "✨ امروز انرژی‌های مثبتی اطرافت هست. با اعتماد بنفس جلو برو.",
    "🌙 امروز یک خبر آرامش‌بخش می‌شنوی.",
    "🔥 یک تصمیم مهم امروز باید گرفته شود. نترس، موفق می‌شوی.",
    "🌼 روزی پر از اتفاقات کوچک اما لذت‌بخش برایت رقم می‌خورد.",
]

weekly_fals = [
    "🔮 این هفته مسیرهای تازه‌ای برایت باز می‌شود.",
    "🌟 در این هفته شخصی که انتظارش را نداشتی به تو نزدیک می‌شود.",
    "💫 این هفته یک فرصت مالی کوچک برایت پیش می‌آید.",
]

monthly_fals = [
    "📅 این ماه تغییری بزرگ در زندگی‌ات رخ می‌دهد.",
    "🌓 این ماه دوران آرامش بیشتری خواهی داشت.",
    "🌞 ماهی پر از امید، اتفاقات خوب و حرکت‌های مثبت در پیش داری.",
]

# ---------- منو ----------
def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔮 فال روزانه", callback_data="daily_fal")],
        [InlineKeyboardButton("🗓 فال هفتگی", callback_data="weekly_fal")],
        [InlineKeyboardButton("📅 فال ماهانه", callback_data="monthly_fal")],
        [InlineKeyboardButton("📜 انواع فال", callback_data="fal_menu")],
        [InlineKeyboardButton("💎 عضویت VIP", callback_data="vip")],
        [InlineKeyboardButton("📆 رزرو فال شخصی", callback_data="reserve")],
        [InlineKeyboardButton("ℹ️ درباره ما", callback_data="about")],
        [InlineKeyboardButton("🛠 پشتیبانی", callback_data="support")],
    ])

def fal_types_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔮 فال تاروت", callback_data="tarot")],
        [InlineKeyboardButton("☕ فال قهوه", callback_data="coffee")],
        [InlineKeyboardButton("🕯 فال شمع", callback_data="candle")],
        [InlineKeyboardButton("📖 فال حافظ", callback_data="hafez")],
        [InlineKeyboardButton("🔙 بازگشت", callback_data="back")],
    ])

# ---------- چک عضویت ----------
async def check_join(user_id, bot):
    for ch in CHANNELS:
        try:
            member = await bot.get_chat_member(chat_id=ch, user_id=user_id)
            if member.status == "left":
                return False
        except:
            return False
    return True

# ---------- شروع ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    if not await check_join(user.id, context.bot):
        await update.message.reply_text(
            "🚫 برای استفاده از ربات ابتدا در کانال‌ها عضو شوید:\n\n"
            "📌 @bmaryamfal\n📌 @shamtrapp\n\n"
            "بعد از عضویت، روی دکمه زیر بزنید 👇",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✔ عضو شدم", callback_data="check")],
                [InlineKeyboardButton("📌 عضویت در کانال اول", url="https://t.me/bmaryamfal")],
                [InlineKeyboardButton("📌 عضویت در کانال دوم", url="https://t.me/shamtrapp")],
            ])
        )
    else:
        await update.message.reply_text(
            f"🌸 خوش اومدی {user.first_name} عزیز!\n"
            "یک گزینه را انتخاب کن:",
            reply_markup=main_menu()
        )

# ---------- دکمه‌ها ----------
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "check":
        if not await check_join(query.from_user.id, context.bot):
            return await query.edit_message_text(
                "❌ هنوز عضو کانال‌ها نشده‌اید!\n\n"
                "📌 @bmaryamfal\n📌 @shamtrapp",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("✔ عضو شدم", callback_data="check")],
                ])
            )
        else:
            return await query.edit_message_text(
                "✔ تایید شد! حالا می‌تونی از ربات استفاده کنی:", 
                reply_markup=main_menu()
            )

    if query.data == "back":
        return await query.edit_message_text("منوی اصلی:", reply_markup=main_menu())

    if query.data == "daily_fal":
        return await query.edit_message_text(
            "🔮 *فال امروز:*\n\n" + random.choice(daily_fals),
            parse_mode=ParseMode.MARKDOWN, 
            reply_markup=main_menu()
        )

    if query.data == "weekly_fal":
        return await query.edit_message_text(
            "🗓 *فال هفتگی:*\n\n" + random.choice(weekly_fals),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=main_menu()
        )

    if query.data == "monthly_fal":
        return await query.edit_message_text(
            "📅 *فال ماهانه:*\n\n" + random.choice(monthly_fals),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=main_menu()
        )

    if query.data == "fal_menu":
        return await query.edit_message_text(
            "📜 لطفاً نوع فال را انتخاب کنید:", 
            reply_markup=fal_types_menu()
        )

    if query.data == "tarot":
        return await query.edit_message_text(
            "🔮 *فال تاروت:* \n\nبه زودی یک مسیر جدید برایت روشن می‌شود.",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=fal_types_menu()
        )

    if query.data == "coffee":
        return await query.edit_message_text(
            "☕ *فال قهوه:* \n\nشخصی از گذشته دوباره به تو نزدیک می‌شود.",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=fal_types_menu()
        )

    if query.data == "candle":
        return await query.edit_message_text(
            "🕯 *فال شمع:* \n\nناامیدی را کنار بگذار، روشنایی نزدیک است.",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=fal_types_menu()
        )

    if query.data == "hafez":
        return await query.edit_message_text(
            "📖 *فال حافظ:* \n\nدر انتظار خبری خوش باش که به زودی می‌رسد.",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=fal_types_menu()
        )

    if query.data == "vip":
        return await query.edit_message_text(
            "💎 *خدمات VIP:*\n\n"
            "✔ فال اختصاصی\n"
            "✔ انرژی‌درمانی\n"
            "✔ تحلیل رابطه\n"
            "✔ چک آینده نزدیک\n\n"
            f"برای دریافت VIP پیام بده:\n👉 {SUPPORT}",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=main_menu()
        )

    if query.data == "reserve":
        return await query.edit_message_text(
            "📆 *رزرو فال شخصی:*\n\n"
            f"برای رزرو پیام بده:\n👉 {SUPPORT}",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=main_menu()
        )

    if query.data == "about":
        return await query.edit_message_text(
            "ℹ️ *درباره ما:*\n\nارائه انواع فال و مشاوره انرژی مثبت 🌟",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=main_menu()
        )

    if query.data == "support":
        return await query.edit_message_text(
            f"🛠 *پشتیبانی:*\n\nبرای ارتباط:\n👉 {SUPPORT}",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=main_menu()
        )

# ---------- اجرای ربات ----------
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))
    app.run_polling()
