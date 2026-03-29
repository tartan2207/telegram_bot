from telegram.ext import filters, PicklePersistence, ApplicationBuilder, CommandHandler, MessageHandler

from config import config
from conversations.gpt_dialog import gpt_dialog_conversation_handler
from hendlers.bot_hendler import start_func, cancel_func, clear_func, remove_keyboard

from hendlers.person_hendler import show_person_keyboard
from conversations.persons_dialog import person_dialog_conversation_handler
from hendlers.question_hendler import random_question
from conversations.quiz_dialog import quiz_dialog_conversation_handler
from hendlers.quiz_hendler import show_quiz_keyboard
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='bot.log',
    filemode='a'
)

logger = logging.getLogger(__name__)




def main():

    persistence = PicklePersistence(filepath="bot_data.pickle")

    application = (
        ApplicationBuilder()
        .token(config.BOT_TOKEN )
        .persistence(persistence)
        .concurrent_updates(True)
        .build()
    )

    application.add_handler(CommandHandler("start", start_func))
    application.add_handler(CommandHandler("cancel", cancel_func))
    application.add_handler(CommandHandler("clear", clear_func))


    application.add_handler(MessageHandler(filters.Text(("Поговорити з відомою особистістю", )), show_person_keyboard))
    application.add_handler(person_dialog_conversation_handler())
    application.add_handler(MessageHandler(filters.Text(("Дізнатися випадковий цікавий факт",)), random_question))
    application.add_handler(MessageHandler(filters.Text(("Взяти участь у квізі",)), show_quiz_keyboard))
    application.add_handler(quiz_dialog_conversation_handler())
    application.add_handler(gpt_dialog_conversation_handler())
    application.add_handler(MessageHandler(filters.Text(("Прибрати клавіатуру",)), remove_keyboard))

    logger.info("Bot started")
    application.run_polling()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Bot stopped")

