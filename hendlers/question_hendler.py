from telegram import Update
from telegram.ext import ContextTypes

from keyboard.reply_keyboard import get_finish_keyboard
from utils.util import load_prompt, send_image, get_ai_service


async def random_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = load_prompt("random")
    await send_image(update, context, 'random')
    message = await update.message.reply_text("Зачекайте декілька секунд...")
    ai_service = get_ai_service(context)
    ai_service.set_prompt(prompt)
    response_text = await ai_service.send_message_list()
    error = "Error code 401"
    if error in response_text:
        await update.message.reply_text(response_text, reply_markup=get_finish_keyboard())
    await message.edit_text(response_text)