
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import os

import os
TOKEN = os.getenv("8744398692:AAHz24SVquGOOoM8VLkMFhJuifX08NQUPVE")
ADMIN_ID = 1452361376

orders = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📦 طلبات مجانية", callback_data="free")],
        [InlineKeyboardButton("💸 شراء كراونز", callback_data="crowns")],
        [InlineKeyboardButton("👍 لايكات ومشاهدات", callback_data="likes")],
        [InlineKeyboardButton("👑 VIP", callback_data="vip")],
        [InlineKeyboardButton("📞 الدعم الفني", callback_data="support")]
    ]
    await update.message.reply_text(
        "👑 مرحباً بك في متجر Shop Crowns",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data == "free":
        keyboard = [
            [InlineKeyboardButton("تغيير الاسم", callback_data="free_name")],
            [InlineKeyboardButton("تغيير الصورة", callback_data="free_pic")],
            [InlineKeyboardButton("تغيير الملامح", callback_data="free_face")],
            [InlineKeyboardButton("جمع معلومات", callback_data="free_info")]
        ]
        await query.message.reply_text(
            "اختر الخدمة المجانية:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif "free_" in query.data:
        orders[user_id] = {"type": query.data}
        await query.message.reply_text("📌 ارسل اليوزر / ID الخاص بك:")

    elif query.data == "crowns":
        await query.message.reply_text(
            "اختر الكمية:\n20 كراون = 27 جنيه\n50 كراون = 67.5 جنيه\n100 كراون = 135 جنيه"
        )

    elif query.data == "support":
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"📞 طلب دعم من {query.from_user.first_name} | {query.from_user.id}"
        )
        await query.message.reply_text("✅ تم إرسال طلبك للدعم")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_id = user.id
    text = update.message.text

    if user_id in orders:
        orders[user_id]["data"] = text

        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"""
📥 طلب جديد

👤 الاسم: {user.first_name}
🆔 الايدي: {user.id}
📦 الخدمة: {orders[user_id]['type']}
📌 البيانات: {text}
"""
        )

        await update.message.reply_text("⏳ جاري تنفيذ طلبك...")
        await update.message.reply_text("✅ تم استلام الطلب")

        del orders[user_id]  # مهم

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user

    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=update.message.photo[-1].file_id,
        caption=f"📸 صورة دفع من {user.first_name} | {user.id}"
    )

    await update.message.reply_text("✅ تم استلام صورة الدفع")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

app.run_polling()
