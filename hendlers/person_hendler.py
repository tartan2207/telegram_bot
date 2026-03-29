from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from conversations.dialog_state import DialogState
from keyboard.inline_keyboard import person_keyboard
from utils.util import get_ai_service, send_image, send_promt, send_answer, get_companion_stats, \
    check_companion


async def show_person_keyboard(update: Update,context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Виберить співрозмовника", reply_markup=person_keyboard)

async def handle_person_select(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from main import logger
    logger.info("Conversation started")
    person_id = update.callback_query.data
    query = update.callback_query
    await query.answer()
    ai_service = get_ai_service(context)
    stats = get_companion_stats(context)

    if person_id == "pers_7":
        await query.edit_message_reply_markup(reply_markup=None)
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Розмови закінчена")
        ai_service.message_list.clear()
        context.user_data.pop("companion_stats", None)
        return ConversationHandler.END

    if person_id == "pers_6":
        await check_companion(update, context)
        return DialogState.PERSON_CHOICE_STATE
    dialogue = None
    if person_id == "pers_1":
        dialogue = "talk_cobain"
    elif person_id == "pers_2":
        dialogue = "talk_hawking"
    elif person_id == "pers_3":
        dialogue = "talk_tolkien"
    elif person_id == "pers_4":
        dialogue = "talk_nietzsche"
    elif person_id == "pers_5":
        dialogue = "talk_queen"

    stats["companion"] = person_id
    context.user_data["companion"] = stats

    await send_image(update, context, dialogue)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Зачекайте декілька секунд...")
    response_text=await send_promt(ai_service,dialogue)

    if response_text:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=response_text)
        return DialogState.PERSON_DIALOG_STATE
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Вибачте, не вдалося отримати відповідь від ШІ.")
        return ConversationHandler.END


async def hendler_person_dialog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response_text=await send_answer(update,  context)
    await update.message.reply_text(response_text)
    return DialogState.PERSON_DIALOG_STATE


async def hendler_change_companion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await check_companion(update, context)
    return DialogState.PERSON_CHOICE_STATE