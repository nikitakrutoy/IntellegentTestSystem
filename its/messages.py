# -*- coding: utf-8 -*-
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

backhome_keyboard = InlineKeyboardMarkup(inline_keyboard =
[
    [
        InlineKeyboardButton(text="Домой", callback_data = "0")
    ]
]
)

home_keyboard = InlineKeyboardMarkup(inline_keyboard =
[
    [
        InlineKeyboardButton(text="Take a test", callback_data = "1"),
        InlineKeyboardButton(text="Edit test", callback_data = "2"),
    ],
    [
        InlineKeyboardButton(text="Help", callback_data = "10")
    ],
]
)

create_keyboard = InlineKeyboardMarkup(inline_keyboard =
[
    [
        InlineKeyboardButton(text="Create test", callback_data = "5")
    ],
    [
        InlineKeyboardButton(text="Home", callback_data = "0")
    ]
]
)
error = '''\
                Oops something went wrong :c
                Trying to solve this'''
home ='''\
                What do you want to do?'''
answer_message = '''\
                Your answer: {0} | Right answer: {1}
                Result: {2}'''.decode(encoding='utf_8')
question_message = '''\
                ------------------------
                Question №{0}:
                {1}
                ------------------------
                Complexity: {2}'''.decode("utf-8")
question_message_full = '''\
                {0}
                Complexity: {1}
                Answer variants: {2}
                Answer: {3}

                '''.decode("utf-8")
test_message = '''\
                {0}
                Upper bound: {1} | Lower Bound: {2}
                Optimum: {3} баллов
                '''.decode("utf-8")
test_id = '''\
                Questions loading..'''
result_questions = '''\
                {0}. {1}
                Your answer: {2} {3}

                '''.decode("utf-8")
result = '''\
                <b>Your rating</b>: {0}'''.decode("utf-8")
not_create = '''\
                You haven't created any test yet '''
choose_text = '''\
                Чтобы добавить вопросы или посмотреть дополнительную информацию выберете тест. Справа от теста отображается его <b>номер</b>.'''
create_test = '''\
                Введите Название, кол-во вопросов и количество ошибок через запятую
                Пример: Test1 5 2'''
created = '''\
                Тест {0} создан! test_id: {1}'''.decode("utf-8")
add_questions = '''\
                Вопросы еще не добавлены.
                Далее напишите список из {0} основных вопросов
                и {1} или более запасных вопросов.
                Формат:
                Вопрос1 - Варианты ответов - Правильный ответ1
                Вопрос2 - Варианты ответов - Правильный ответ2
                ...
                Вопрос{0} - Варианты ответов{0} - Правильный ответ{0}
                Вопрос{2} - Варианты ответов{2} - Правильный ответ{2} - Сложность
                ...

                Обратите внимание, что начианя с {2} вопроса,
                указывается сложность вопроса, которая не превышает {0}
                Варианты ответа указывать через запятую.'''
added = '''\
                Вопросы успешно добавлены'''
help_message = '''\
                хелп! ай нид сомбади
                хелп! нот джаст энибади
                хелп! ю ноу а нид сомван
                хелп!'''
