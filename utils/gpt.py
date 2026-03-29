import openai

from config import config
from main import logger


class ChatGptService:
    def __init__(self):
        self.message_list = []

    async def send_message_list(self) -> str:
        print("Надсилаємо запит...")
        try:
            completion = await config.OPENAI_CLIENT.chat.completions.create(
                model="gpt-5-mini",
                messages=self.message_list,
                max_completion_tokens=3000,
                temperature=1
            )
        except (openai.RateLimitError, openai.AuthenticationError,openai.BadRequestError
               ,openai.APIStatusError) as e:
            error_message=f"Error code {e.status_code}: {e.body["message"]}"
            logger.error(error_message)
            return error_message
        except Exception as e:
            error_message = f"{type(e).__name__}- {e}"
            logger.error(error_message)
            return error_message
        else:
            message = completion.choices[0].message
            self.message_list.append(message)
            return message.content

    def set_prompt(self, prompt_text: str) -> None:
        self.message_list.clear()
        self.message_list.append({"role": "system", "content": prompt_text})


    def add_message(self, message_text: str) -> None:
        self.message_list.append({"role": "user", "content": message_text})

    async def send_question(self, prompt_text: str, message_text: str) -> str:
        self.message_list.clear()
        self.message_list.append({"role": "system", "content": prompt_text})
        self.message_list.append({"role": "user", "content": message_text})
        return await self.send_message_list()


