from telegram.ext import  ConversationHandler, MessageHandler, filters
from conversations.dialog_state import DialogState
from hendlers.gpt_hendler import start_gpt_dialog_flow, handle_gpt_dialog


def gpt_dialog_conversation_handler() -> ConversationHandler:
    return ConversationHandler(
        entry_points=[
            MessageHandler(filters.Text(("Задати питання чату GPT",)), start_gpt_dialog_flow)
        ],
        states={
            DialogState.GPT_DIALOG_STATE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_gpt_dialog),
            ],
        },
        fallbacks=[]
    )
