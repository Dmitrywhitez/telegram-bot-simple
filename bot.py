import os
import logging
from flask import Flask, request
import telegram

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Получаем токен из переменных окружения
TOKEN = os.environ.get('TELEGRAM_TOKEN')
if not TOKEN:
    raise ValueError("Нет токена! Добавь TELEGRAM_TOKEN в переменные окружения")

# Создаем приложение и бота
app = Flask(__name__)
bot = telegram.Bot(token=TOKEN)

@app.route('/')
def home():
    return "✅ Бот работает!"

@app.route('/health')
def health():
    return "healthy"

@app.route(f'/webhook', methods=['POST'])
def webhook():
    """Обработчик сообщений от Telegram"""
    try:
        # Получаем обновление от Telegram
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        logger.info(f"Получено сообщение: {update}")
        
        # Если есть сообщение
        if update.message and update.message.text:
            chat_id = update.message.chat.id
            text = update.message.text
            
            # Отвечаем в зависимости от команды
            if text == '/start':
                bot.send_message(chat_id=chat_id, text="Привет! Я простой бот! Отправь мне любое сообщение")
            else:
                bot.send_message(chat_id=chat_id, text=f"Ты написал: {text}")
        
        return 'ok', 200
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        return 'error', 500

@app.route('/setwebhook')
def set_webhook():
    """Установка вебхука (вызывается один раз)"""
    url = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}/webhook"
    bot.set_webhook(url=url)
    return f"Webhook установлен на {url}"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)