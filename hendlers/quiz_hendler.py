from telegram import Update
from telegram.ext import ConversationHandler, ContextTypes

from conversations.dialog_state import DialogState
from keyboard.inline_keyboard import  quiz_keyboard
from utils.util import get_ai_service, send_image, get_quiz_stats, send_promt, send_answer


async def show_quiz_keyboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_image(update, context, 'quiz')
    await update.message.reply_text("Зачекайте декілька секунд...")

    ai_service = get_ai_service(context)
    response_text=await send_promt(ai_service, "quiz")
    await update.message.reply_text(response_text)
    await update.message.reply_text("Почати квіз", reply_markup=quiz_keyboard)

async def handle_quiz_select(update: Update, context: ContextTypes.DEFAULT_TYPE):
        from main import logger
        logger.info("Quiz started")
        quiz_id = update.callback_query.data
        query = update.callback_query
        await query.answer()
        ai_service = get_ai_service(context)
        stats = get_quiz_stats(context)

        if quiz_id == "quiz_5":
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=f"Правільних відповідей {stats["correct"]} на {stats["total"]} питань.")
            await send_promt(ai_service, "quiz")
            return DialogState.QUIZ_CHOICE_STATE

        if quiz_id == "quiz_6":
            await query.edit_message_reply_markup(reply_markup=None)
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Квіз завершено")
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=f"Правільних відповідей {stats["correct"]} на {stats["total"]} питань.")
            ai_service.message_list.clear()
            context.user_data.pop("quiz_stats", None)
            return ConversationHandler.END

        TOPIC=["програмування","математика","біологія"]
        quiz_message = None
        if quiz_id=="quiz_1":
            quiz_message="програмування"
            stats["last_topic"] = quiz_message
            context.user_data["quiz_stats"] = stats
        elif quiz_id=="quiz_2":
            quiz_message = "математика"
            stats["last_topic"] = quiz_message
            context.user_data["quiz_stats"] = stats
        elif quiz_id == "quiz_3":
            quiz_message = "біологія"
            stats["last_topic"] = quiz_message
            context.user_data["quiz_stats"] = stats
        elif quiz_id == "quiz_4":
            if stats["last_topic"] not in TOPIC:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Вибачте але попередня тема не вибрана")
                return DialogState.QUIZ_CHOICE_STATE
            else:
                quiz_message = stats["last_topic"]


        ai_service.add_message(quiz_message)
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Генерую питання, почекайте...")
        response_text = await ai_service.send_message_list()

        if response_text:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=response_text)
            return DialogState.QUIZ_DIALOG_STATE
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text="Вибачте, не вдалося отримати відповідь від ШІ.")
            return DialogState.QUIZ_CHOICE_STATE

async def answer_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response_text = await send_answer(update, context)
    await update.message.reply_text(response_text)

    stats = get_quiz_stats(context)
    if "Правильно" in response_text:
        stats["correct"] += 1
    stats["total"] += 1
    context.user_data["quiz_stats"] = stats
    return ConversationHandler.END


