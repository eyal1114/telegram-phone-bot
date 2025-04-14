import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "שלום! כתוב את שם המותג והדגם של הטלפון שאתה מחפש.\n"
        "לדוגמה: samsung galaxy s23 ultra"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    brands = ['apple', 'samsung', 'xiaomi', 'google', 'oneplus']
    found_brand = None

    for brand in brands:
        if brand in text:
            found_brand = brand
            break

    if found_brand:
        model = text.replace(found_brand, "").strip().replace(" ", "-")
        link = f"https://yourstore.com/{found_brand}/{model}"
        await update.message.reply_text(f"🔗 הנה הקישור שלך:\n{link}")
    else:
        await update.message.reply_text(
            "📱 לא זיהיתי מותג. אנא כתוב:\nשם מותג + שם דגם\nלדוגמה:\napple iphone 13"
        )

if __name__ == '__main__':
    app = ApplicationBuilder().token(os.environ["BOT_TOKEN"]).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
