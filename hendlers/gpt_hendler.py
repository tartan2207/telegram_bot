from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from conversations.dialog_state import DialogState
from keyboard.reply_keyboard import get_finish_keyboard, get_remove_keyboard
from utils.util import get_ai_service


async def start_gpt_dialog_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Напиши питання для GPT", reply_markup=get_finish_keyboard())
    return DialogState.GPT_DIALOG_STATE

async def handle_gpt_dialog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text.strip()
    ai_service = get_ai_service(context)
    if message == "Завершити":
        await update.message.reply_text("Розмову завершено.", reply_markup=get_remove_keyboard())
        ai_service.message_list.clear()
        return ConversationHandler.END
    ai_service.add_message(message)
    text = await ai_service.send_message_list()
    await update.message.reply_text(text, reply_markup=get_finish_keyboard())
    return DialogState.GPT_DIALOG_STATE


