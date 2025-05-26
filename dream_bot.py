import logging
import os
import random
from typing import Dict
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Словарь символов снов
DREAM_SYMBOLS = {
    # Животные
    'кот': ['независимость', 'интуиция', 'женственность'],
    'собак': ['верность', 'дружба', 'защита'],
    'птиц': ['свобода', 'духовность', 'новые возможности'],
    'рыб': ['подсознание', 'эмоции', 'интуиция'],
    'змея': ['трансформация', 'мудрость', 'скрытые страхи'],
    'лошад': ['сила', 'энергия', 'благородство'],
    'медвед': ['сила', 'материнство', 'защита'],
    'волк': ['инстинкты', 'свобода', 'одиночество'],

    # Природа
    'вода': ['эмоции', 'очищение', 'подсознание'],
    'море': ['глубокие чувства', 'неизвестность', 'бесконечность'],
    'огонь': ['страсть', 'разрушение', 'очищение'],
    'лес': ['неизвестность', 'рост', 'тайны'],
    'гора': ['препятствия', 'цели', 'духовный рост'],
    'дождь': ['очищение', 'обновление', 'печаль'],
    'солнце': ['энергия', 'жизненная сила', 'просветление'],
    'луна': ['интуиция', 'женственность', 'циклы'],

    # Действия
    'лет': ['свобода', 'освобождение', 'высокие цели'],
    'бег': ['бегство', 'спешка', 'движение к цели'],
    'плав': ['эмоциональное погружение', 'адаптация', 'течение жизни'],
    'пад': ['потеря контроля', 'страхи', 'неуверенность'],
    'танц': ['радость', 'самовыражение', 'гармония'],

    # Цвета
    'красн': ['страсть', 'энергия', 'гнев'],
    'син': ['спокойствие', 'мудрость', 'печаль'],
    'зелен': ['рост', 'природа', 'исцеление'],
    'желт': ['радость', 'интеллект', 'предупреждение'],
    'черн': ['неизвестность', 'тайна', 'трансформация'],
    'бел': ['чистота', 'новое начало', 'духовность'],

    # Объекты
    'дом': ['безопасность', 'семья', 'внутренний мир'],
    'машин': ['контроль', 'направление в жизни', 'прогресс'],
    'мост': ['переход', 'связь', 'преодоление препятствий'],
    'лестниц': ['продвижение', 'духовный рост', 'усилия'],
    'зеркал': ['самопознание', 'отражение', 'истина'],
    'ключ': ['решения', 'тайны', 'новые возможности'],
}

# Предсказания
PREDICTIONS = [
    "В ближайшее время тебя ждет приятный сюрприз! 🎁",
    "Скоро ты встретишь интересного человека 👤",
    "Новые возможности появятся на горизонте ✨",
    "Твоя интуиция поможет принять важное решение 🔮",
    "Ожидай положительные изменения в личной жизни 💕",
    "Творческое вдохновение скоро посетит тебя 🎨",
    "Финансовое благополучие не за горами 💰",
    "Время для новых начинаний уже близко 🌱",
    "Старые проблемы найдут свое решение 🔓",
    "Путешествие принесет новые впечатления 🌍"
]

# Стили анализа
ANALYSIS_STYLES = {
    'mystical': {
        'name': '🔮 Мистический',
        'prefix': 'Древние символы говорят...',
        'emojis': ['🔮', '✨', '🌙', '⭐', '💫']
    },
    'scientific': {
        'name': '🧠 Научный',
        'prefix': 'С точки зрения психологии...',
        'emojis': ['🧠', '📊', '🔬', '📈', '💡']
    },
    'fun': {
        'name': '😄 Веселый',
        'prefix': 'Твой сон говорит...',
        'emojis': ['😄', '🎉', '🎈', '🌈', '🎭']
    }
}


class DreamAnalyzerBot:
    def __init__(self):
        self.user_data = {}

    def analyze_dream(self, dream_text: str, style: str = 'mystical') -> Dict:
        """Анализирует сон и возвращает интерпретацию"""
        dream_lower = dream_text.lower()
        found_symbols = []
        meanings = []

        # Поиск символов в тексте сна
        for symbol, symbol_meanings in DREAM_SYMBOLS.items():
            if symbol in dream_lower:
                found_symbols.append(symbol)
                meanings.extend(symbol_meanings)

        # Если символы не найдены, используем общие интерпретации
        if not found_symbols:
            meanings = ['новые возможности', 'внутренние изменения', 'подсознательные желания']

        # Убираем дубликаты и берем до 3 значений
        unique_meanings = list(set(meanings))[:3]

        # Вычисляем "загадочность"
        mystery_level = min(10, len(found_symbols) * 2 + random.randint(3, 7))

        # Выбираем случайное предсказание
        prediction = random.choice(PREDICTIONS)

        return {
            'symbols': found_symbols,
            'meanings': unique_meanings,
            'mystery_level': mystery_level,
            'prediction': prediction,
            'style': style
        }

    def format_analysis(self, analysis: Dict) -> str:
        """Форматирует анализ для отправки пользователю"""
        style_info = ANALYSIS_STYLES[analysis['style']]
        emoji = random.choice(style_info['emojis'])

        result = f"{emoji} {style_info['name']} анализ сна:\n\n"
        result += f"{style_info['prefix']}\n\n"

        if analysis['symbols']:
            result += "📝 Найденные символы:\n"
            for symbol in analysis['symbols'][:5]:
                result += f"• {symbol}\n"
            result += "\n"

        result += "💭 Интерпретация:\n"
        for meaning in analysis['meanings']:
            result += f"• {meaning}\n"

        result += f"\n⭐ Уровень загадочности: {analysis['mystery_level']}/10\n"
        result += f"\n🔮 Предсказание: {analysis['prediction']}"

        return result


# Создаем экземпляр бота
bot = DreamAnalyzerBot()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    welcome_text = """
🌙 Добро пожаловать в Анализатор Снов! 🌙

Расскажи мне свой сон, и я помогу разгадать его тайный смысл!

Доступные команды:
/start - начать работу с ботом
/help - помощь
/style - выбрать стиль анализа
/stats - твоя статистика снов

Просто опиши свой сон в сообщении, и я проанализирую его! ✨
    """
    await update.message.reply_text(welcome_text)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    help_text = """
🔮 Как пользоваться ботом:

1. Просто напиши свой сон в сообщении
2. Я найду символы и дам интерпретацию
3. Получи предсказание на основе сна!

🎨 Стили анализа:
• Мистический - загадочные толкования
• Научный - психологический подход  
• Веселый - легкие и позитивные трактовки

Используй /style чтобы выбрать стиль анализа
    """
    await update.message.reply_text(help_text)


async def style_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /style"""
    keyboard = []
    for style_key, style_info in ANALYSIS_STYLES.items():
        keyboard.append([InlineKeyboardButton(
            style_info['name'],
            callback_data=f"style_{style_key}"
        )])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Выбери стиль анализа снов:",
        reply_markup=reply_markup
    )


async def style_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик выбора стиля"""
    query = update.callback_query
    await query.answer()

    style = query.data.split('_')[1]
    user_id = query.from_user.id

    if user_id not in bot.user_data:
        bot.user_data[user_id] = {}

    bot.user_data[user_id]['style'] = style
    style_name = ANALYSIS_STYLES[style]['name']

    await query.edit_message_text(f"Выбран стиль: {style_name}\nТеперь расскажи свой сон!")


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /stats"""
    user_id = update.from_user.id

    if user_id not in bot.user_data or 'dreams_count' not in bot.user_data[user_id]:
        await update.message.reply_text("У тебя пока нет проанализированных снов! Расскажи мне первый сон 😴")
        return

    user_stats = bot.user_data[user_id]
    dreams_count = user_stats.get('dreams_count', 0)
    total_mystery = user_stats.get('total_mystery', 0)
    avg_mystery = total_mystery / dreams_count if dreams_count > 0 else 0

    stats_text = f"""
📊 Твоя статистика снов:

🌙 Проанализированных снов: {dreams_count}
⭐ Средний уровень загадочности: {avg_mystery:.1f}/10
🎨 Текущий стиль: {ANALYSIS_STYLES.get(user_stats.get('style', 'mystical'))['name']}
    """

    await update.message.reply_text(stats_text)


async def analyze_dream_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Анализирует сон пользователя"""
    user_id = update.effective_user.id
    message_text = update.message.text

    # Получаем стиль пользователя, если нет — используем по умолчанию
    user_style = bot.user_data.get(user_id, {}).get('style', 'mystical')

    # Анализируем сон
    analysis = bot.analyze_dream(message_text, style=user_style)
    response = bot.format_analysis(analysis)

    # Обновляем статистику пользователя
    if user_id not in bot.user_data:
        bot.user_data[user_id] = {}

    bot.user_data[user_id]['dreams_count'] = bot.user_data[user_id].get('dreams_count', 0) + 1
    bot.user_data[user_id]['total_mystery'] = bot.user_data[user_id].get('total_mystery', 0) + analysis['mystery_level']
    bot.user_data[user_id]['style'] = user_style

    await update.message.reply_text(response)



async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик дополнительных кнопок"""
    query = update.callback_query
    await query.answer()

    if query.data == "change_style":
        keyboard = []
        for style_key, style_info in ANALYSIS_STYLES.items():
            keyboard.append([InlineKeyboardButton(
                style_info['name'],
                callback_data=f"style_{style_key}"
            )])

        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "Выбери новый стиль анализа:",
            reply_markup=reply_markup
        )

    elif query.data == "show_stats":
        user_id = query.from_user.id

        if user_id not in bot.user_data:
            await query.edit_message_text("У тебя пока нет статистики!")
            return

        user_stats = bot.user_data[user_id]
        dreams_count = user_stats.get('dreams_count', 0)
        total_mystery = user_stats.get('total_mystery', 0)
        avg_mystery = total_mystery / dreams_count if dreams_count > 0 else 0

        stats_text = f"""
📊 Твоя статистика снов:

🌙 Проанализированных снов: {dreams_count}
⭐ Средний уровень загадочности: {avg_mystery:.1f}/10
🎨 Текущий стиль: {ANALYSIS_STYLES.get(user_stats.get('style', 'mystical'))['name']}
        """

        await query.edit_message_text(stats_text)


def main():
    """Запуск бота"""

    # Создаем приложение
    application = Application.builder().token(TOKEN).build()

    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("style", style_command))
    application.add_handler(CommandHandler("stats", stats_command))

    # Обработчики callback кнопок
    application.add_handler(CallbackQueryHandler(style_callback, pattern="^style_"))
    application.add_handler(CallbackQueryHandler(button_callback, pattern="^(change_style|show_stats)$"))

    # Обработчик сообщений со снами
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, analyze_dream_message))

    # Запускаем бота
    print("Бот запущен...")
    application.run_polling()


if __name__ == '__main__':

    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("style", style_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CallbackQueryHandler(style_callback, pattern="^style_"))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, analyze_dream_message))

    application.run_polling()