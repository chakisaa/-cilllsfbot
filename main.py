import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped
import yt_dlp

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
STRING_SESSION = os.getenv("STRING_SESSION")

bot = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
assistant = Client("assistant", api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION)
call = PyTgCalls(assistant)

@bot.on_message(filters.command("start"))
async def start(_, m: Message):
    await m.reply_text("Halo! Aku cilllsfbot 🎵\nKetik /play <judul lagu> buat muterin lagu di VC.\nContoh: /play sadrah")

@bot.on_message(filters.command("play") & filters.group)
async def play(_, m: Message):
    if len(m.command) < 2:
        return await m.reply_text("Ketik judulnya, contoh: /play taylor swift")
    query = " ".join(m.command[1:])
    chat_id = m.chat.id
        msg = await m.reply_text(f"Siap! Lagi nyari lagu: {query}...")
    try:
        ydl_opts = {"format": "bestaudio/best", "noplaylist": True, "quiet": True, "default_search": "ytsearch"}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=False)
            if "entries" in info:
                info = info["entries"][0]
            url = info["url"]
            title = info.get("title", query)
        await call.play(chat_id, AudioPiped(url))
        await msg.edit_text(f"🎵 Sekarang muter: {title}")
    except Exception as e:
        await msg.edit_text(f"Gagal masuk VC: {e}")

@bot.on_message(filters.command(["stop", "end"]) & filters.group)
async def stop(_, m: Message):
    try:
        await call.leave_call(m.chat.id)
        await m.reply_text("Udah berhenti 👋")
    except:
        await m.reply_text("Lagi gak muter lagu kok.")

async def main():
    await bot.start()
    await assistant.start()
    await call.start()
    print("Bot jalan...")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
