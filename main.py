import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Halo! Aku cilllsfbot 🎵\n"
        "Ketik /play <judul lagu> buat coba.\n"
        "Contoh: /play taylor swift"
    )

async def play(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Ketik judulnya, contoh: /play taylor swift")
        return
    judul = " ".join(context.args)
    await update.message.reply_text(f"Siap! Lagi nyari lagu: {judul}...\n\nIni versi awal botnya, nanti kita upgrade biar bisa masuk Voice Chat ya.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("play", play))
    print("Bot jalan...")
    app.run_polling()
