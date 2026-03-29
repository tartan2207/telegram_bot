import os
from dotenv import load_dotenv, find_dotenv
from openai import AsyncOpenAI

load_dotenv(find_dotenv())


class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    OPENAI_TOKEN = os.getenv("GPT_TOKEN")
    OPENAI_CLIENT = AsyncOpenAI(api_key=OPENAI_TOKEN)


config = Config()
