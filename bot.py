from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8744398692:AAHz24SVquGOOoM8VLkMFhJuifX08NQUPVE"
ADMIN_ID = 1452361376

main_menu = ReplyKeyboardMarkup([
    ["📦 طلبات مجانية", "💰 طلبات مدفوعة"],
    ["💬 تواصل مع الدعم"]
], resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👑 اهلا بيك في شوب كراونز", reply_markup=main_menu)

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "📦 طلبات مجانية":
        await update.message.reply_text("اكتب طلبك المجاني")

    elif text == "💰 طلبات مدفوعة":
        await update.message.reply_text("اكتب طلبك المدفوع")

    elif text == "💬 تواصل مع الدعم":
        await update.message.reply_text("اكتب رسالتك")

    else:
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"📥 طلب جديد:\n{text}"
        )
        await update.message.reply_text("تم استلام طلبك ✅")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, handle))

app.run_polling()
