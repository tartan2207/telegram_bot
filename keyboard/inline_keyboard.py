from telegram import InlineKeyboardMarkup, InlineKeyboardButton

class Person:
    def __init__(self,name:str, id:str)->None:
        self.name = name
        self.id=id
persons=[Person("Курт Кобейн","pers_1"),
         Person("Стівен Гокінг","pers_2"),
         Person("Дж.Р.Р. Толкін","pers_3"),
         Person("Фрідріх Ніцше","pers_4"),
         Person("Єлизавета II","pers_5"),
         Person("Вибрати нового співрозмовника","pers_6"),
         Person("Завершити поточну розмову","pers_7")
         ]



person_keyboard= InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton( person.name, callback_data=person.id)
        ]for person in persons
    ])



class Quiz:
    def __init__(self,name:str, id:str)->None:
        self.name = name
        self.id=id
quiz= [Quiz("Програмування","quiz_1"),
         Quiz("Математика","quiz_2"),
         Quiz("Біологія","quiz_3"),
         Quiz("Попередня тема","quiz_4"),
         Quiz("Результати квізу","quiz_5"),
         Quiz("Закінчити квіз","quiz_6")
      ]


quiz_keyboard= InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton( item.name, callback_data=item.id)
        ]for item in quiz
    ])

# THEME=[item.name for item in quiz]