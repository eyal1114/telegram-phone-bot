import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

# קישור מותאם אישית לכל מותג
brand_links = {
    "apple": "https://www.apple.com/",
    "samsung": "https://www.samsung.com/",
    "xiaomi": "https://www.mi.com/",
    "google": "https://store.google.com/",
    "oneplus": "https://www.oneplus.com/"
}

# קישורים מיוחדים לדגמים
model_links = {
    "samsung a12": "https://s.click.aliexpress.com/e/_oElDlWX"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "שלום! כתוב את שם המותג והדגם של הטלפון שאתה מחפש.\n"
        "לדוגמה: samsung galaxy s23 ultra"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    brands = ['apple', 'samsung', 'xiaomi', 'google', 'oneplus']
    found_brand = None
    found_model = None

    # חיפוש אחר המותג בטקסט של ההודעה
    for brand in brands:
        if brand in text:
            found_brand = brand
            break

    if found_brand:
        # אם המותג נמצא, נבדוק אם הדגם הוא samsung a12
        for model, link in model_links.items():
            if model in text:
                found_model = link
                break
        
        if not found_model:
            # אם לא נמצא דגם מיוחד, נחפש דגם כללי
            model = text.replace(found_brand, "").strip().replace(" ", "-")
            if found_brand in brand_links:
                found_model = f"{brand_links[found_brand]}{model}"
        
        await update.message.reply_text(f"🔗 הנה הקישור שלך:\n{found_model}")
    else:
        await update.message.reply_text(
            "📱 לא זיהיתי מותג. אנא כתוב:\nשם מותג + שם דגם\nלדוגמה:\napple iphone 13"
        )

if __name__ == '__main__':
    app = ApplicationBuilder().token(os.environ["BOT_TOKEN"]).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
