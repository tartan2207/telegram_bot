import enum


class DialogState(enum.IntEnum):
    PERSON_DIALOG_STATE = 1
    PERSON_CHOICE_STATE = 2
    QUIZ_DIALOG_STATE = 3
    QUIZ_CHOICE_STATE = 4
    GPT_DIALOG_STATE=5
