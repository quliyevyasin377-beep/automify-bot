import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler, MessageHandler, filters

# Logging quraşdırması
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Sənin Telegram ID-n (bildirişlər bura gələcək)
ADMIN_ID = 8753322873

# Çoxdilli tərcümələr lüğəti
TRANSLATIONS = {
    "az": {
        "welcome": "Salam! Automify-a xoş gəlmisiniz. Zəhmət olmasa dil seçin:",
        "catalog": "🔘 Məhsullar / Xidmətlər",
        "catalog_text": "🔘 Məhsullar / Xidmətlər:\n- WhatsApp & Telegram Avtomatik Sifariş Botu\n- CRM İnteqrasiyası\n- AI Dəstəkli Müştəri Xidməti",
        "prices": "💎 Qiymətlər",
        "prices_text": "💎 Qiymətlər:\n1. Standart Paket: 30 AZN / ay\n2. Premium Paket: 60 AZN / ay",
        "order": "🛒 Sifariş Et",
        "order_prompt": "Sifariş vermək üçün zəhmət olmasa əlaqə nömrənizi və ya istifadəçi adınızı qeyd edin:",
        "order_success": "✅ Məlumatınız qəbul olundu! Tezliklə sizinlə əlaqə saxlayacağıq.",
        "support": "🛠 Dəstək",
        "support_text": "🛠 Dəstək: @automify_az\nEmail: quliyevyasin377@gmail.com",
        "lang_changed": "Dil Azərbaycan dilinə dəyişdirildi. Aşağıdakı menyudan seçin:",
    },
    "tr": {
        "welcome": "Merhaba! Automify'a hoş geldiniz. Lütfen dil seçin:",
        "catalog": "🔘 Ürün / Hizmetler",
        "catalog_text": "🔘 Ürün / Hizmetler:\n- WhatsApp & Telegram Otomatik Sipariş Botu\n- CRM Entegrasyonu\n- AI Destekli Müşteri Hizmetleri",
        "prices": "💎 Fiyatlar",
        "prices_text": "💎 Fiyatlar:\n1. Standart Paket: 600 TRY / ay\n2. Premium Paket: 1200 TRY / ay",
        "order": "🛒 Sipariş Ver",
        "order_prompt": "Sipariş vermek için lütfen iletişim numaranızı veya kullanıcı adınızı belirtin:",
        "order_success": "✅ Bilgileriniz alındı! En kısa sürede sizinle iletişime geçeceğiz.",
        "support": "🛠 Destek",
        "support_text": "🛠 Destek: @automify_az\nEmail: quliyevyasin377@gmail.com",
        "lang_changed": "Dil Türkçe olarak değiştirildi. Aşağıdaki menüden seçin:",
    },
    "en": {
        "welcome": "Hello! Welcome to Automify. Please select your language:",
        "catalog": "🔘 Products / Services",
        "catalog_text": "🔘 Products / Services:\n- WhatsApp & Telegram Automated Order Bot\n- CRM Integration\n- AI-Powered Customer Service",
        "prices": "💎 Prices",
        "prices_text": "💎 Prices:\n1. Standard Package: $20 / month\n2. Premium Package: $40 / month",
        "order": "🛒 Place Order",
        "order_prompt": "To place an order, please provide your contact number or username:",
        "order_success": "✅ Your information has been received! We will contact you soon.",
        "support": "🛠 Support",
        "support_text": "🛠 Support: @automify_az\nEmail: quliyevyasin377@gmail.com",
        "lang_changed": "Language changed to English. Choose from the menu below:",
    },
    "ru": {
        "welcome": "Здравствуйте! Добро пожаловать в Automify. Пожалуйста, выберите язык:",
        "catalog": "🔘 Продукты / Услуги",
        "catalog_text": "🔘 Продукты / Услуги:\n- Автоматический бот заказов WhatsApp & Telegram\n- Интеграция с CRM\n- Служба поддержки на базе ИИ",
        "prices": "💎 Цены",
        "prices_text": "💎 Цены:\n1. Стандартный пакет: 1500 RUB / мес\n2. Премиум пакет: 3000 RUB / мес",
        "order": "🛒 Сделать заказ",
        "order_prompt": "Для оформления заказа укажите номер телефона или имя пользователя:",
        "order_success": "✅ Ваши данные приняты! Мы свяжемся с вами в ближайшее время.",
        "support": "🛠 Поддержка",
        "support_text": "🛠 Поддержка: @automify_az\nEmail: quliyevyasin377@gmail.com",
        "lang_changed": "Язык изменен на русский. Выберите из меню ниже:",
    }
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("🇦🇿 Azərbaycan", callback_data="lang_az"),
            InlineKeyboardButton("🇹🇷 Türkçe", callback_data="lang_tr")
        ],
        [
            InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
            InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        await update.message.reply_text(TRANSLATIONS["az"]["welcome"], reply_markup=reply_markup)
    elif update.callback_query:
        query = update.callback_query
        await query.answer()
        await query.message.edit_text("Zəhmət olmasa dil seçin / Please select language:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("lang_"):
        lang_code = data.split("_")[1]
        context.user_data["lang"] = lang_code
        t = TRANSLATIONS[lang_code]

        keyboard = [
            [InlineKeyboardButton(t["catalog"], callback_data="menu_catalog")],
            [InlineKeyboardButton(t["prices"], callback_data="menu_prices")],
            [InlineKeyboardButton(t["order"], callback_data="menu_order")],
            [InlineKeyboardButton(t["support"], callback_data="menu_support")],
            [InlineKeyboardButton("🌍 Dilləri dəyiş / Change Language", callback_data="change_lang")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.edit_text(t["lang_changed"], reply_markup=reply_markup)
        return

    if data == "change_lang":
        await start(update, context)
        return

    lang = context.user_data.get("lang", "az")
    t = TRANSLATIONS[lang]

    if data == "menu_catalog":
        text = t["catalog_text"]
    elif data == "menu_prices":
        text = t["prices_text"]
    elif data == "menu_order":
        text = t["order_prompt"]
        context.user_data["waiting_for_order"] = True
    elif data == "menu_support":
        text = t["support_text"]
    else:
        text = "Seçim qəbul olundu."

    back_keyboard = [[InlineKeyboardButton("⬅️ Ana Menyu / Main Menu", callback_data=f"lang_{lang}")]]
    await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(back_keyboard))

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("waiting_for_order"):
        user = update.effective_user
        contact_info = update.message.text
        lang = context.user_data.get("lang", "az")
        t = TRANSLATIONS[lang]

        await update.message.reply_text(t["order_success"])

        admin_message = (
            f"🚨 **YENİ SİFARİŞ VAR!** 🚨\n\n"
            f"👤 Ad: {user.full_name}\n"
            f"🔗 İstifadəçi adı: @{user.username if user.username else 'Yoxdur'}\n"
            f"🆔 ID: `{user.id}`\n"
            f"📞 Məlumat/Nömrə: {contact_info}"
        )
        await context.bot.send_message(chat_id=ADMIN_ID, text=admin_message, parse_mode="Markdown")
        context.user_data["waiting_for_order"] = False

def main():
    TOKEN = "8838299100:AAFc_fOX0O8nnch1L93boQLbRhKsxXicdFY"
    
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Automify Bot işləyir və bildiriş sistemi aktivdir...")
    app.run_polling()

if __name__ == "__main__":
    main()