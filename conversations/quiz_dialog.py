from telegram.ext import ConversationHandler, MessageHandler, filters, CallbackQueryHandler

from conversations.dialog_state import DialogState
from hendlers.quiz_hendler import handle_quiz_select, answer_quiz


def quiz_dialog_conversation_handler() -> ConversationHandler:
    return ConversationHandler(
        entry_points=[
            CallbackQueryHandler(handle_quiz_select, pattern="^quiz_")

        ],
        states={
            DialogState.QUIZ_CHOICE_STATE: [
                CallbackQueryHandler(handle_quiz_select, pattern="^quiz_")
            ],
            DialogState.QUIZ_DIALOG_STATE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, answer_quiz)
            ],

        },
        fallbacks=[]
        # per_message=True
    )