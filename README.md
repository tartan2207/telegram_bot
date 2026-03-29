# GPT Multi-Task Bot
A versatile GPT-powered Telegram bot that combines an educational quiz, a generator of interesting facts, and a simulator for chatting with famous figures

## Basic functions

### Thematic quizzes
There are interactive quizzes in three categories:

 - **Mathematics**: From basic arithmetic to the fundamentals of calculus.
   
 -  **Programming**: Questions on Python, algorithms and data structures.
   
 -  **Biology**: Genetics, anatomy and the natural world.

The scoring system is retained even after the bot is restarted, thanks to Persistence.

### Random facts

Immediately get a random, fascinating fact from any field of knowledge. Perfect for killing a minute and learning something new.

### Conversations with outstanding individuals

A unique role-playing mode. Choose a conversation partner and ask them questions. The AI adapts its speech style and knowledge to match the chosen character.

### Free communication
‘Ask GPT’ mode — use the bot as your personal assistant to tackle any task or find information.

## Technical stack

-   **Python 3.12** — the primary development language.
    
-   **python-telegram-bot (v20)** — a modern asynchronous library for   developing Telegram bots..
    
-   **OpenAI API** — the bot’s ‘brain’ (GPT family models).
 
-   **PicklePersistence** — reliable saving of quiz progress and user settings to local storage.


## How to use

Enter the command /start.

Use the Reply keyboard at the bottom of the screen to select a mode:

Select  ‘Take part in the quiz’ to choose a category (Maths/Programming/Biology). Test your knowledge in your chosen category

Select  ‘Learn a random interesting fact’ for a one-off dose of knowledge.

Select  ‘Chat with a famous person’ to open the menu of notable figures.

At any time, you can tap  ‘Ask GPT a question’ to  simply chat with the AI.

## Implementation features

**Regular expressions**: The ^...$ pattern is used to handle callbacks, which prevents errors when buttons are clicked.

**Data security:** Clearing context.user_data when switching modes or resetting statistics.

**Prompt engineering:** Customised system instructions to limit the length of questions and maintain the ‘personality’ of the interlocutors.
