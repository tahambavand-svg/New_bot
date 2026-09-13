from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import re

TOKEN = "8714507787:AAGKvBiUDfEkcY6iBioDD7hwYhG7pXPp-6w"

# نام کاربری مدیرها
ADMINS = [
    "WSTaha",
    "Behrad_n_90",
]

FOOTER = "\n\n🔵 M.E.N | Middle East News\n@middleeastnews_men"


def is_admin(update):
    username = update.effective_user.username

    if username is None:
        return False

    return username.lower() in [x.lower() for x in ADMINS]


def edit_text(text):
    # حذف لینک‌ها
    text = re.sub(r"https?://\S+|www\.\S+", "", text)

    # حذف هشتگ‌ها
    text = re.sub(r"#\S+", "", text)

    # حذف @username
    text = re.sub(r"@\w+", "", text)

    # حذف فاصله‌های اضافی
    text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text)
    text = text.strip()

    # اضافه کردن متن پایانی
    text += FOOTER

    return text


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update):
        await update.message.reply_text("⛔ شما اجازه استفاده از این بات را ندارید.")
        return

    await update.message.reply_text(
        "✅ بات M.E.N آماده است.\n"
        "متنت رو بفرست تا ویرایشش کنم."
    )


async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update):
        return

    text = update.message.text

    result = edit_text(text)

    await update.message.reply_text(result)


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message))

print("M.E.N Bot is running...")
app.run_polling()