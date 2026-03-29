from telegram import Update, Message,  BotCommand, BotCommandScopeChat, MenuButtonCommands
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from utils.gpt import ChatGptService


async def send_text(update: Update, context: ContextTypes.DEFAULT_TYPE,
                    text: str) -> Message:
    if text.count('_') % 2 != 0:
        message = f"Рядок '{text}' є невалідним з точки зору markdown. Скористайтеся методом send_html()"
        print(message)
        return await update.message.reply_text(message)

    text = text.encode('utf16', errors='surrogatepass').decode('utf16')
    return await context.bot.send_message(chat_id=update.effective_chat.id,
                                          text=text,
                                          parse_mode=ParseMode.MARKDOWN)


async def send_image(update: Update, context: ContextTypes.DEFAULT_TYPE,
                     name: str) -> Message:
    with open(f'resources/images/{name}.jpg', 'rb') as image:
        return await context.bot.send_photo(chat_id=update.effective_chat.id,
                                            photo=image)

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE,
                         commands: dict):
    command_list = [BotCommand(key, value) for key, value in commands.items()]
    await context.bot.set_my_commands(command_list, scope=BotCommandScopeChat(
        chat_id=update.effective_chat.id))
    await context.bot.set_chat_menu_button(menu_button=MenuButtonCommands(),
                                           chat_id=update.effective_chat.id)


def load_message(name):
    with open("resources/messages/" + name + ".txt", "r",
              encoding="utf8") as file:
        return file.read()


def load_prompt(name):
    with open("resources/prompts/" + name + ".txt", "r",
              encoding="utf8") as file:
        return file.read()


def get_ai_service(context: ContextTypes.DEFAULT_TYPE) -> ChatGptService:
    ai_service = context.user_data.get("ai_service")

    if not ai_service:
        new_service = ChatGptService()
        context.user_data["ai_service"] = new_service
        return new_service
    return ai_service


def get_quiz_stats(context: ContextTypes.DEFAULT_TYPE) -> dict:
    current_stats = context.user_data.get("quiz_stats")
    # if "quiz_stats" not in context.user_data:
    if not current_stats:
        context.user_data["quiz_stats"] = {"correct": 0, "total": 0, "last_topic":""}
        new_stats = context.user_data.get("quiz_stats")
        return new_stats
    return current_stats

def get_companion_stats(context: ContextTypes.DEFAULT_TYPE) -> dict:
    current_stats = context.user_data.get("companion_stats")
    if not current_stats:
        context.user_data["companion_stats"] = {"companion":""}
        new_stats = context.user_data.get("companion_stats")
        return new_stats
    return current_stats

async def send_promt(ai_service:ChatGptService ,prompt_name:str)-> str:
    prompt = load_prompt(prompt_name)
    ai_service.set_prompt(prompt)
    return await ai_service.send_message_list()


async def send_answer(update: Update, context: ContextTypes.DEFAULT_TYPE)->str:
    message = update.message.text.strip()
    ai_service = get_ai_service(context)
    ai_service.add_message(message)
    return  await ai_service.send_message_list()

async def check_companion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stats = get_companion_stats(context)
    if stats["companion"] == "":
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Співрозмовник  не вибраний ")
    else:
        ai_service = get_ai_service(context)
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Розмова закінчена. Можете вибрати нового співрозмовника")
        ai_service.message_list.clear()




