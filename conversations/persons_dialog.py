from telegram.ext import MessageHandler, CallbackQueryHandler, ConversationHandler,  filters

from conversations.dialog_state import DialogState
from hendlers.person_hendler import handle_person_select, hendler_person_dialog, hendler_change_companion


def person_dialog_conversation_handler() -> ConversationHandler:
    return ConversationHandler(
        entry_points=[
            CallbackQueryHandler(handle_person_select, pattern="^pers_"),

        ],
        states={
            DialogState.PERSON_CHOICE_STATE: [
                CallbackQueryHandler(handle_person_select, pattern="^pers_")
            ],
            DialogState.PERSON_DIALOG_STATE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, hendler_person_dialog),
                CallbackQueryHandler(hendler_change_companion, pattern="^pers_6$")
            ],
        },
        fallbacks=[]
        # per_message = True
    )