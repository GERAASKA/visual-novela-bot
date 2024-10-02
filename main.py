import telebot
from telebot import types
import json

# Ваш токен бота
TOKEN = "7357009563:AAEP3C5wLUwPkT_-lgE9P2sY_7eCmvOmJgc"

# Создаем объект бота
bot = telebot.TeleBot(TOKEN)

# Состояния пользователей для трекинга этапов игры
user_states = {}

# Функция для загрузки данных из файла .json
def load_chapter(chapter_name):
    try:
        with open(f"Chapters/{chapter_name}.json", "r", encoding="utf-8") as file:
            chapter_data = json.load(file)
        return chapter_data
    except FileNotFoundError:
        return None  # Если файл не найден

# Экран 1: Начальный экран с логотипом и кнопкой "Начать"
@bot.message_handler(commands=["start"])
def start_game(message):
    user_id = message.chat.id

    # Создаем кнопку "Начать"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_button = types.KeyboardButton("Начать")
    markup.add(start_button)

    # Приветственное сообщение
    bot.send_message(
        user_id,
        "Добро пожаловать в текстовую игру! Нажмите 'Начать', чтобы продолжить.",
        reply_markup=markup
    )

# Экран 2: Пользовательское соглашение
@bot.message_handler(func=lambda message: message.text == "Начать")
def show_agreement(message):
    user_id = message.chat.id

    # Сохраняем состояние пользователя
    user_states[user_id] = "AGREEMENT"

    markup = types.InlineKeyboardMarkup()
    agree_button = types.InlineKeyboardButton(text="Согласен", callback_data="agree")
    disagree_button = types.InlineKeyboardButton(text="Не согласен", callback_data="disagree")
    markup.add(agree_button, disagree_button)

    bot.send_message(
        user_id,
        "Прежде чем начать игру, вы должны согласиться с пользовательским соглашением. "
        "Вы согласны?",
        reply_markup=markup
    )

# Обработка соглашения
@bot.callback_query_handler(func=lambda call: call.data in ["agree", "disagree"])
def handle_agreement(call):
    user_id = call.message.chat.id

    if call.data == "agree":
        # Пользователь согласен с соглашением, переходим в главное меню
        bot.send_message(user_id, "Спасибо! Теперь вы можете начать игру.")
        show_main_menu(user_id)
    else:
        # Пользователь не согласен с соглашением
        bot.send_message(user_id, "Вы не можете начать игру, не согласившись с пользовательским соглашением.")

# Экран 3: Главное меню
def show_main_menu(user_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    new_game_button = types.KeyboardButton("Новая игра")
    load_game_button = types.KeyboardButton("Загрузить")
    about_button = types.KeyboardButton("Об авторах")
    markup.add(new_game_button, load_game_button, about_button)

    bot.send_message(user_id, "Главное меню", reply_markup=markup)

# Экран 4: Загрузка глав
@bot.message_handler(func=lambda message: message.text == "Загрузить")
def load_game(message):
    user_id = message.chat.id

    # Меню выбора главы
    markup = types.InlineKeyboardMarkup()
    chapter_1 = types.InlineKeyboardButton(text="Глава 1", callback_data="chapter_1")
    chapter_2 = types.InlineKeyboardButton(text="Глава 2", callback_data="chapter_2")
    markup.add(chapter_1, chapter_2)

    bot.send_message(user_id, "Выберите главу для загрузки.", reply_markup=markup)

# Обработка загрузки главы
@bot.callback_query_handler(func=lambda call: call.data.startswith("chapter"))
def handle_chapter_selection(call):
    user_id = call.message.chat.id

    # Проверка доступа к главам
    if call.data == "chapter_2" and user_states.get(user_id) != "chapter_1_completed":
        bot.send_message(user_id, "Вы не можете начать главу 2, пока не завершите главу 1.")
    else:
        bot.send_message(user_id, f"Вы начали {call.data.replace('_', ' ')}!")
        user_states[user_id] = call.data

# Экран 5: Визуал самой игры (пример с главой 1)
@bot.message_handler(func=lambda message: message.text == "Новая игра")
def start_new_game(message):
    user_id = message.chat.id

    # Сохраняем состояние пользователя
    user_states[user_id] = "IN_GAME"

    # Загружаем сюжет для первой главы
    chapter_data = load_chapter("first")  # Можно выбрать по порядку или из меню
    
    if chapter_data:
        # Если файл загружен, отправляем текст и создаем кнопки
        story_text = chapter_data.get("text", "Текст главы не найден.")
        options = chapter_data.get("options", [])

        markup = types.InlineKeyboardMarkup()
        for option in options:
            option_button = types.InlineKeyboardButton(text=option['text'], callback_data=option['callback_data'])
            markup.add(option_button)

        bot.send_message(user_id, story_text, reply_markup=markup)
    else:
        bot.send_message(user_id, "Ошибка загрузки сюжета, попробуйте снова.")

# Экран 6: Доступ к меню во время прохождения
@bot.message_handler(commands=["menu"])
def in_game_menu(message):
    user_id = message.chat.id

    markup = types.InlineKeyboardMarkup()
    jump_button = types.InlineKeyboardButton(text="Перейти к загрузке глав", callback_data="jump")
    rules_button = types.InlineKeyboardButton(text="Правила", callback_data="rules")
    back_button = types.InlineKeyboardButton(text="Главное меню", callback_data="main_menu")
    markup.add(jump_button, rules_button, back_button)

    bot.send_message(user_id, "Меню игры:", reply_markup=markup)

# Обработка меню во время игры
@bot.callback_query_handler(func=lambda call: call.data in ["jump", "rules", "main_menu"])
def handle_in_game_menu(call):
    user_id = call.message.chat.id

    if call.data == "jump":
        load_game(call.message)
    elif call.data == "rules":
        bot.send_message(user_id, "Правила игры: ...")
    elif call.data == "main_menu":
        show_main_menu(user_id)

# Экран 7: Об авторах
@bot.message_handler(func=lambda message: message.text == "Об авторах")
def about_authors(message):
    user_id = message.chat.id

    # Отправляем информацию об авторах (вместо ссылки здесь текст или документ)
    bot.send_message(user_id, "Эту игру разработала команда XYZ. Спасибо за участие!")

# Обработка выбора игрока (например, направо или налево)
@bot.callback_query_handler(func=lambda call: call.data in ["right", "left", "house", "forest"])
def handle_game_choice(call):
    user_id = call.message.chat.id
    
    # Получаем выбор пользователя
    user_choice = call.data
    
    # Загружаем соответствующий сюжет в зависимости от выбора
    if user_choice == "house":
        chapter_data = load_chapter("second")
    elif user_choice == "forest":
        chapter_data = load_chapter("third")
    else:
        chapter_data = load_chapter("fourth")
    
    if chapter_data:
        # Отправляем текст и кнопки для следующего шага
        story_text = chapter_data.get("text", "Текст не найден.")
        options = chapter_data.get("options", [])
        markup = types.InlineKeyboardMarkup()
        for option in options:
            option_button = types.InlineKeyboardButton(text=option['text'], callback_data=option['callback_data'])
            markup.add(option_button)

        bot.send_message(user_id, story_text, reply_markup=markup)
    else:
        bot.send_message(user_id, "Ошибка загрузки следующего этапа.")

# Запуск бота
bot.polling(none_stop=True)
