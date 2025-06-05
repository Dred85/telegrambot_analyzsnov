import logging
import os
import random
from typing import Dict
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
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
    'собака': ['верность', 'дружба', 'защита'],
    'птица': ['свобода', 'духовность', 'новые возможности'],
    'рыба': ['подсознание', 'эмоции', 'интуиция'],
    'змея': ['трансформация', 'мудрость', 'скрытые страхи'],
    'лошадь': ['сила', 'энергия', 'благородство'],
    'медведь': ['сила', 'материнство', 'защита'],
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
    'летать': ['свобода', 'освобождение', 'высокие цели'],
    'бегать': ['бегство', 'спешка', 'движение к цели'],
    'плавать': ['эмоциональное погружение', 'адаптация', 'течение жизни'],
    'падать': ['потеря контроля', 'страхи', 'неуверенность'],
    'танцевать': ['радость', 'самовыражение', 'гармония'],
    # Цвета
    'красный': ['страсть', 'энергия', 'гнев'],
    'синий': ['спокойствие', 'мудрость', 'печаль'],
    'зеленый': ['рост', 'природа', 'исцеление'],
    'желтый': ['радость', 'интеллект', 'предупреждение'],
    'черный': ['неизвестность', 'тайна', 'трансформация'],
    'белый': ['чистота', 'новое начало', 'духовность'],
    # Объекты
    'дом': ['безопасность', 'семья', 'внутренний мир'],
    'машина': ['контроль', 'направление в жизни', 'прогресс'],
    'мост': ['переход', 'связь', 'преодоление препятствий'],
    'лестница': ['продвижение', 'духовный рост', 'усилия'],
    'зеркало': ['самопознание', 'отражение', 'истина'],
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
    "Путешествие принесет новые впечатления 🌍",
    "Ты получишь важные новости 📩",
    "Скоро придет ясность в запутанной ситуации 🧭",
    "Ты обретешь нового друга 🐾",
    "Сны подскажут верное направление 🌙",
    "Улыбка незнакомца изменит твой день 😊",
    "Скоро появится шанс реализовать давнюю мечту 🌠",
    "Ты найдешь то, что давно искал 🔍",
    "Неожиданная встреча принесет радость 🎉",
    "Вдохновение придет откуда не ждали 🌬️",
    "Твои усилия наконец-то окупятся 📈",
    "Скоро ты узнаешь важную истину 🧘‍♂️",
    "Наступает период внутреннего роста 🌿",
    "Твоя доброта вернется сторицей 💞",
    "Ты будешь в центре внимания 🌟",
    "Ночь подарит яркие сны и подсказки 🛌",
    "Один шаг изменит всё 🔁",
    "Скоро будет повод для праздника 🥳",
    "Ты обретешь уверенность в себе 💪",
    "Чудо уже на пути к тебе ✨",
    "Старый знакомый напомнит о себе 📞",
    "Ты найдешь баланс и гармонию ⚖️",
    "Любовь проявится в неожиданных формах ❤️",
    "Предстоит удачная покупка 🛍️",
    "Ты получишь знак свыше ☁️",
    "Появится шанс исправить прошлое 🔁",
    "Ты заметишь то, что раньше упускал 👁️",
    "В тебе проснется скрытый талант 🧠",
    "Проект, над которым ты работаешь, принесет успех 💼",
    "Ты обретешь внутреннее спокойствие 🕊️",
    "Новая дверь откроется перед тобой 🚪",
    "Кто-то поделится с тобой мудростью 📜",
    "Ты вдохновишь других своим примером 🌟",
    "Твоя энергия привлечет позитивные события ⚡",
    "Ты получишь поддержку из неожиданного источника 🤝",
    "Появится возможность проявить себя 🎤",
    "Скоро ты поймешь, зачем всё это было 🔄",
    "Сбудется одно из твоих желаний 💫",
    "Ты будешь окружён заботой и теплом ☕",
    "Интуиция подскажет верный путь 🧭",
    "В твоей жизни наступает белая полоса 🏁"
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
            meanings = [
                'новые возможности',
                'внутренние изменения',
                'подсознательные желания',
                'эмоциональное освобождение',
                'потребность в отдыхе',
                'поиск смысла жизни',
                'страх перемен',
                'желание самореализации',
                'необходимость сделать выбор',
                'скрытая тревога',
                'путь к личностному росту',
                'неразрешённые чувства',
                'ожидание важного события',
                'внутренний конфликт',
                'стремление к гармонии',
                'желание быть услышанным',
                'подготовка к новому этапу',
                'поиск утраченного',
                'обострённая интуиция',
                'желание уйти от реальности',
                'готовность отпустить прошлое',
                'отражение повседневных переживаний'
            ]
        
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
        result = f"{emoji} {style_info['name']} анализ сна:\n"
        result += f"{style_info['prefix']}\n"
        
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
    welcome_text = """🌙 Добро пожаловать в Анализатор Снов! 🌙
Расскажи мне свой сон, и я помогу разгадать его тайный смысл!
Выберите команду:"""
    
    # Создаем кнопки для команд
    keyboard = [
        [
            InlineKeyboardButton("Помощь", callback_data='help'),
            InlineKeyboardButton("Выбрать стиль", callback_data='style'),
            InlineKeyboardButton("Моя статистика", callback_data='stats'),
            # InlineKeyboardButton("Новая кнопка", callback_data='test')

        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Отправляем приветственное сообщение с кнопками
    await update.message.reply_text(
        welcome_text,
        reply_markup=reply_markup
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    help_text = """🔮 Как пользоваться ботом:
1. Просто напиши свой сон в сообщении
2. Я найду символы и дам интерпретацию
3. Получи предсказание на основе сна!
🎨 Стили анализа:
• Мистический - загадочные толкования
• Научный - психологический подход  
• Веселый - легкие и позитивные трактовки"""
    
    # Создаем кнопки для выбора стиля
    keyboard = [
        [
            InlineKeyboardButton("🔮 Мистический", callback_data='style_mystical'),
            InlineKeyboardButton("🧠 Научный", callback_data='style_scientific')
        ],
        [
            InlineKeyboardButton("😄 Веселый", callback_data='style_fun')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(help_text, reply_markup=reply_markup)

async def style_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /style"""
    user_id = update.effective_user.id
    current_style = bot.user_data.get(user_id, {}).get('style', 'mystical')
    current_style_name = ANALYSIS_STYLES[current_style]['name']
    style_text = f"""🎨 Выберите стиль анализа:
Текущий стиль: {current_style_name}
• Мистический - загадочные толкования
• Научный - психологический подход
• Веселый - легкие и позитивные трактовки"""

    keyboard = [
        [
            InlineKeyboardButton("🔮 Мистический", callback_data='style_mystical'),
            InlineKeyboardButton("🧠 Научный", callback_data='style_scientific')
        ],
        [
            InlineKeyboardButton("😄 Веселый", callback_data='style_fun')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(style_text, reply_markup=reply_markup)

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /stats"""
    user_id = update.effective_user.id
    
    if user_id not in bot.user_data or 'dreams_count' not in bot.user_data[user_id]:
        await update.message.reply_text("У тебя пока нет проанализированных снов! Расскажи мне первый сон 😴")
        return
    
    user_stats = bot.user_data[user_id]
    dreams_count = user_stats.get('dreams_count', 0)
    total_mystery = user_stats.get('total_mystery', 0)
    avg_mystery = total_mystery / dreams_count if dreams_count > 0 else 0
    
    stats_text = f"""📊 Твоя статистика снов:
🌙 Проанализированных снов: {dreams_count}
⭐ Средний уровень загадочности: {avg_mystery:.1f}/10
🎨 Текущий стиль: {ANALYSIS_STYLES.get(user_stats.get('style', 'mystical'))['name']}"""
    
    await update.message.reply_text(stats_text)

async def analyze_dream_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Анализирует сон пользователя"""
    user_id = update.effective_user.id
    message_text = update.message.text
    
    # Получаем стиль пользователя, если нет - используем по умолчанию
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
    
    # Создаем кнопки для основных команд
    keyboard = [
        [
            InlineKeyboardButton("Помощь", callback_data='help'),
            InlineKeyboardButton("Выбрать стиль", callback_data='style'),
            InlineKeyboardButton("Моя статистика", callback_data='stats')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(response, reply_markup=reply_markup)

async def style_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик выбора стиля"""
    try:
        query = update.callback_query
        await query.answer()
        style = query.data.split('_')[1]  # получаем mystical, scientific, fun
        user_id = query.from_user.id
        
        if user_id not in bot.user_data:
            bot.user_data[user_id] = {}
        
        bot.user_data[user_id]['style'] = style
        style_name = ANALYSIS_STYLES[style]['name']
        
        # Кнопки главного меню
        keyboard = [
            [
                InlineKeyboardButton("Помощь", callback_data='help'),
                InlineKeyboardButton("Выбрать стиль", callback_data='style'),
                InlineKeyboardButton("Моя статистика", callback_data='stats')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            f"✅ Стиль изменён на {style_name}\n\n🌙 Расскажи свой сон, и я проанализирую его!",
            reply_markup=reply_markup
        )
    except Exception as e:
        logger.error(f"Ошибка в style_callback: {e}")
        await update.callback_query.message.reply_text("Произошла ошибка. Попробуйте позже.")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик основных кнопок (help, style, stats)"""
    try:
        query = update.callback_query
        await query.answer()
        user_id = query.from_user.id
        data = query.data
        
        if data == 'help':
            help_text = """🔮 Как пользоваться ботом:
1. Просто напиши свой сон в сообщении
2. Я найду символы и дам интерпретацию
3. Получи предсказание на основе сна!
🎨 Стили анализа:
• Мистический - загадочные толкования
• Научный - психологический подход  
• Веселый - легкие и позитивные трактовки"""
            
            keyboard = [
                [
                    InlineKeyboardButton("🔮 Мистический", callback_data='style_mystical'),
                    InlineKeyboardButton("🧠 Научный", callback_data='style_scientific')
                ],
                [
                    InlineKeyboardButton("😄 Веселый", callback_data='style_fun')
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(help_text, reply_markup=reply_markup)
        
        elif data == 'style':
            current_style = bot.user_data.get(user_id, {}).get('style', 'mystical')
            current_style_name = ANALYSIS_STYLES[current_style]['name']
            style_text = f"""🎨 Выберите стиль анализа:
Текущий стиль: {current_style_name}
• Мистический - загадочные толкования
• Научный - психологический подход
• Веселый - легкие и позитивные трактовки"""
            
            keyboard = [
                [
                    InlineKeyboardButton("🔮 Мистический", callback_data='style_mystical'),
                    InlineKeyboardButton("🧠 Научный", callback_data='style_scientific')
                ],
                [
                    InlineKeyboardButton("😄 Веселый", callback_data='style_fun')
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(style_text, reply_markup=reply_markup)
        
        elif data == 'stats':
            if user_id not in bot.user_data or 'dreams_count' not in bot.user_data[user_id]:
                await query.edit_message_text("У тебя пока нет проанализированных снов! Расскажи мне первый сон 😴")
                return
            
            user_stats = bot.user_data[user_id]
            dreams_count = user_stats.get('dreams_count', 0)
            total_mystery = user_stats.get('total_mystery', 0)
            avg_mystery = total_mystery / dreams_count if dreams_count > 0 else 0
            
            stats_text = f"""📊 Твоя статистика снов:
🌙 Проанализированных снов: {dreams_count}
⭐ Средний уровень загадочности: {avg_mystery:.1f}/10
🎨 Текущий стиль: {ANALYSIS_STYLES.get(user_stats.get('style', 'mystical'))['name']}"""
            
            await query.edit_message_text(stats_text)
    except Exception as e:
        logger.error(f"Ошибка в button_callback: {e}")
        await update.callback_query.message.reply_text("Произошла ошибка. Попробуйте позже.")


async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    admin_ids = list(map(int, os.getenv("ADMIN_IDS", "").split(",")))

    if user_id not in admin_ids:
        await update.message.reply_text("❌ У вас нет доступа к админ-панели.")
        return

    keyboard = [
        [InlineKeyboardButton("📋 Посмотреть пользователей", callback_data="admin_users")],
        [InlineKeyboardButton("📁 Экспортировать данные", callback_data="admin_export")],
        [InlineKeyboardButton("📢 Рассылка", callback_data="admin_broadcast")],
        [InlineKeyboardButton("⚙️ Управление символами", callback_data="admin_symbols")],
        [InlineKeyboardButton("📊 Статистика", callback_data="admin_stats")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🔐 Добро пожаловать в админ-панель!", reply_markup=reply_markup)



def main():
    """Запуск бота"""
    # Создаем приложение
    application = ApplicationBuilder().token(TOKEN).build()
    
    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("style", style_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("admin", admin_command))
    
    # Обработчики callback кнопок - ВАЖНО: порядок имеет значение!
    # Сначала более специфичные паттерны, потом общие

    application.add_handler(CallbackQueryHandler(button_callback, pattern="^(help|style|stats)$"))
    application.add_handler(CallbackQueryHandler(style_callback, pattern="^style_"))
    # Обработчик сообщений со снами
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, analyze_dream_message))
    
    # Запускаем бота
    print("Бот запущен ;)")
    application.run_polling()

if __name__ == '__main__':
    main()