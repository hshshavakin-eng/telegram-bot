from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN = "8744398692:AAHz24SVquGOOoM8VLkMFhJuifX08NQUPVE"
ADMIN_ID = 1452361376  # حط ايدي بتاعك

# تخزين مؤقت
user_data = {}

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📦 طلبات مجانية", callback_data="free")],
        [InlineKeyboardButton("💰 شراء كراونز", callback_data="buy")],
        [InlineKeyboardButton("👍 لايكات ومشاهدات", callback_data="likes")],
        [InlineKeyboardButton("👑 VIP", callback_data="vip")],
        [InlineKeyboardButton("📞 الدعم الفني", callback_data="support")],
    ]
    await update.message.reply_text(
        "👑 مرحباً بك في متجر Shop Crowns\nاختر الخدمة:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# التعامل مع الأزرار
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    user_data[user_id] = {}

    if query.data == "free":
        keyboard = [
            [InlineKeyboardButton("تغيير الاسم", callback_data="free_name")],
            [InlineKeyboardButton("تغيير الصورة", callback_data="free_pic")],
            [InlineKeyboardButton("تغيير الملامح", callback_data="free_face")],
            [InlineKeyboardButton("جمع معلومات", callback_data="free_info")],
        ]
        await query.message.reply_text("اختر الخدمة المجانية:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data.startswith("free_"):
        user_data[user_id]["service"] = query.data
        await query.message.reply_text("📩 ابعت ID أو اليوزر الخاص بك:")

# استقبال الرسائل
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text

    if user_id in user_data and "service" in user_data[user_id]:
        service = user_data[user_id]["service"]

        # إرسال الطلب للأدمن
        msg = f"""
📥 طلب جديد
👤 ID: {user_id}
📦 الخدمة: {service}
📌 البيانات: {text}
        """

        await context.bot.send_message(chat_id=ADMIN_ID, text=msg)

        await update.message.reply_text("⏳ تم استلام طلبك، انتظر التنفيذ")

        user_data[user_id] = {}

# تشغيل البوت
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
