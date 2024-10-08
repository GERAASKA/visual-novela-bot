# 
[ФИДЕС](https://t.me/fidess_bot) - это телеграм-бот, обучающая визуальная новелла, которая в игровой форме помогла бы юным пользователям лучше ориентироваться в данной сфере и не допускать ошибок, приводящих к серьезным последствиям, а также этот интерактивный формат учит детей безопасному поведению в интернете.

## Содержание

- [Описание](#описание)
- [Начало Работы](#начало-работы)
- [Использование](#использование)
- [Распределение людей внутри команды](#распределение)
- [Используемое API](#используемое-api)
- [Контактная информация](#контактная-информация)

## Описание 

ФИДЕС - проект обучающей игры в формате визуальной новеллы для чат-бота в Telegram поможет пользователям усваивать сложные темы через взаимодействие с сюжетом, принимая решения и наблюдая за их последствиями в игровом контексте. Такой способ подачи информации значительно повышает интерес к учебному процессу, делая его более динамичным и увлекательным.

## Использоание со стороны пользователя
 
1. Пользователь запускает бота, отправляя **/start**.
3. Бот присылает сообщения по сюжету.
4. Пользователь читает, иногда делает выбор, который влияет на дальнейший сюжет.
5. Пользователь получает полезную правовую информацию, которая поможет лучше ориентироваться в правововой сфере и не допускать ошибок.

## Логика бота

Импорт библиотек и установка логирования:
- **`config`**: Импорт токенов бота и API погоды из отдельного файла.
- **`Bot, types, Dispatcher, executor`** из aiogram: Компоненты для работы с телеграм-ботом.

Инициализация бота и диспетчера:
- Создание объекта бота (Bot) и диспетчера (Dispatcher) для обработки сообщений и команд.

Обработчик команды "/start":
- **`start_command`**: Ответ на команду "/start" приветствует пользователя.

Обработчик всех остальных сообщений:

## Используемое API

1. [Телеграм Bot API](https://t.me/BotFather) - телеграм бот, созданный для разработчиков, cоздающих ботов для Telegram.