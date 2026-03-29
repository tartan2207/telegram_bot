from telegram import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

REPLY_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("Дізнатися випадковий цікавий факт"), KeyboardButton("Задати питання чату GPT")],
        [KeyboardButton("Поговорити з відомою особистістю"), KeyboardButton("Взяти участь у квізі")],
        [KeyboardButton("Прибрати клавіатуру") ]
    ],

    resize_keyboard=True
)


def get_finish_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup([["Завершити"]], resize_keyboard=True)


def get_remove_keyboard() -> ReplyKeyboardRemove:
    return ReplyKeyboardRemove()