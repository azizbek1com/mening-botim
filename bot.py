import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# === SOZLAMALAR ===
BOT_TOKEN = "8532312358:AAHFzgU8_xMxj66zy7yk0KSq-rlDUZ-Qn0k"
ADMIN_ID = 8532312358  # Sizning Telegram ID'ingiz

# === LOGGING ===
logging.basicConfig(level=logging.INFO)

# Foydalanuvchi ID'larini saqlash (xotira ichida)
user_map = {}  # { admin_message_id: user_chat_id }

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    user_id = message.chat_id

    # === ADMIN JAVOB YOZSA ===
    if user_id == ADMIN_ID:
        if message.reply_to_message:
            original_id = message.reply_to_message.message_id
            target_user_id = user_map.get(original_id)

            if target_user_id:
                await context.bot.send_message(
                    chat_id=target_user_id,
                    text=f"📩 Javob:\n\n{message.text}"
                )
                await message.reply_text("✅ Yuborildi!")
            else:
                await message.reply_text("❌ Bu xabarga javob berish mumkin emas.")
        else:
            await message.reply_text("ℹ️ Javob berish uchun xabarni Reply qiling.")
        return

    # === FOYDALANUVCHI YOZSA ===
    forwarded = await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=(
            f"📨 Yangi xabar!\n"
            f"👤 Foydalanuvchi ID: {user_id}\n"
            f"💬 Xabar:\n\n{message.text}"
        )
    )

    # Xabar ID'sini saqlaymiz
    user_map[forwarded.message_id] = user_id

    await message.reply_text("✅ Xabaringiz yuborildi! Tez orada javob berishadi.")


# === BOTNI ISHGA TUSHIRISH ===
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot ishga tushdi...")
app.run_polling()
