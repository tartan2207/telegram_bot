from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from utils.gpt import ChatGptService
from keyboard.reply_keyboard import REPLY_KEYBOARD, get_remove_keyboard
from utils.util import load_message, send_image, send_text, show_main_menu, get_ai_service


async def start_func(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = load_message('main')
    await send_image(update, context, 'main')
    await send_text(update, context, text)
    await update.message.reply_text("Вибери кнопку для подальшої роботи", reply_markup=REPLY_KEYBOARD)
    commands= {"start": "Початок роботи — вітання та головне меню",
               "cancel":"Скасувати поточну дію",
               "clear": "Видалити історию спілкування користувача"
               }
    await show_main_menu(update, context, commands)
    context.user_data["ai_service"] = ChatGptService()
    context.user_data.clear()


async def remove_keyboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Клавіатуру очищено", reply_markup=ReplyKeyboardRemove())

async def cancel_func(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # context.user_data.clear()
    await update.message.reply_text("Чат завершено.", reply_markup=get_remove_keyboard())
    ai_service = get_ai_service(context)
    ai_service.message_list.clear()


async  def clear_func(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ai_service = get_ai_service(context)
    ai_service.message_list.clear()
    context.user_data.clear()
    await  update.message.reply_text("Історія видалена.")