import os import random from telegram import Update from telegram.ext import ( ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters ) import google.generativeai as genai from dotenv import load_dotenv

Загрузка ключей из .env

load_dotenv() BOT_TOKEN = os.getenv("7718204976:AAGhQNlS9ulnqj_SatBQucQTsABVnOE9Co0") GEMINI_API_KEY = os.getenv("AIzaSyCc_3Ki5RbrGd5oMHA_KciW1DnzRf--pt0") REQUIRED_CHANNEL = os.getenv("@E7SHADOW")  # Например: @E7SHADOW

Настройка Gemini

genai.configure(api_key=GEMINI_API_KEY) model = genai.GenerativeModel("gemini-pro")

Автофразы поддержки

support_phrases = { "мне плохо": "Я с тобой. Всё наладится, даже если сейчас тяжело.", "я один": "Ты не один. Я рядом, чтобы поддержать тебя.", "помоги": "Я здесь. Расскажи, что случилось?", "устал": "Иногда нужно просто отдохнуть. Ты заслуживаешь покоя.", "не знаю как жить": "Жизнь сложна, но ты не один на этом пути. Я помогу насколько смогу." }

Проверка подписки

async def check_subscription(user_id, context): try: member = await context.bot.get_chat_member(REQUIRED_CHANNEL, user_id) return member.status in ["member", "administrator", "creator"] except: return False

Команда /start

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE): user_id = update.effective_user.id if not await check_subscription(user_id, context): await update.message.reply_text(f"Пожалуйста, подпишись на канал {REQUIRED_CHANNEL} чтобы пользоваться ботом.") return await update.message.reply_text("Привет! Я здесь, чтобы поддержать тебя. Просто напиши, как ты себя чувствуешь.")

Команда /help

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE): await update.message.reply_text("/hug – виртуальное объятие\n/quote – вдохновляющая цитата\n/talk – поговорить ни о чём\n/help – помощь")

Команда /hug

async def hug(update: Update, context: ContextTypes.DEFAULT_TYPE): await update.message.reply_text("Обнимаю тебя мысленно. Ты не один.")

Команда /quote

async def quote(update: Update, context: ContextTypes.DEFAULT_TYPE): quotes = [ "Каждый рассвет — это новый шанс.", "Ты сильнее, чем тебе кажется.", "Даже в темноте можно увидеть свет." ] await update.message.reply_text(random.choice(quotes))

Команда /talk

async def talk(update: Update, context: ContextTypes.DEFAULT_TYPE): await update.message.reply_text("Расскажи, что у тебя на душе. Даже если это просто мысли вслух — я рядом.")

Обработка обычных сообщений

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE): user_id = update.effective_user.id if not await check_subscription(user_id, context): await update.message.reply_text(f"Сначала подпишись на канал {REQUIRED_CHANNEL}.") return

msg = update.message.text.lower()
for trigger, reply in support_phrases.items():
    if trigger in msg:
        await update.message.reply_text(reply)
        return

response = model.generate_content(msg)
await update.message.reply_text(response.text)

Основной запуск

def main(): app = ApplicationBuilder().token(BOT_TOKEN).build() app.add_handler(CommandHandler("start", start)) app.add_handler(CommandHandler("help", help_cmd)) app.add_handler(CommandHandler("hug", hug)) app.add_handler(CommandHandler("quote", quote)) app.add_handler(CommandHandler("talk", talk)) app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)) print("Бот запущен.") app.run_polling()

if name == "main": main()