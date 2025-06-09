import asyncio
import logging
import aiohttp

from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from gigachat import GigaChat

# Для авторизации запросов используйте ключ, полученный в проекте GigaChat API

with open("./token hakaton.txt") as token_file:
    TOKEN = token_file.read()

# Роутер для управления событиями в рамках некоторой общей темы
# в данном случае в рамках работы с формой ответов пользователя
form_router = Router()


# Класс, для описания "состояний" в которых может находиться бот
class CoordsForm(StatesGroup):
    favorite_subjects = State()
    unloved_subjects = State()
    exams = State()
    interesting = State()
    not_interesting = State()

@form_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    Функция для "реакции" на команду `/start`
    """
    await message.answer(
        (f"Привет, {message.from_user.full_name}! 👋\n\n Я чат бот 'Профессия для тебя' 😊 \n\nС "
          "моей помощью ты можешь узнать, какая профессия больше тебе подходит 👤\n\n"
          "Для этого тебе всего лишь надо будет написать:\n"
          "✅ Свои любимые предметы в школе \n✅ Свои нелюбимые предметы в школе\n✅ Экзамены, которые ты сдал или собираешься сдавать\n"
          "✅ А также написать чем ты интересуешься и что тебе вообще не интересно, чтобы исключить подобные профессии\n\n"
          "Для начала нажми /profession 😎"
        )
    )

@form_router.message(Command("help"))
async def command_help_handler(message: Message) -> None:
    """
    Функция для "реакции" на команду `/help`
    """
    await message.answer(
        f"❗Справочная информация...🤓\n\n"
        "Я простой бот для получения сведений о подходящей для тебя профессии 👤\n"
        "/profession - команда, с помощью которой можно получить сведения о подходящей для тебя профессии 😏\n"
        "/cancel - команда для отмены действий 🔙"
    )

@form_router.message(Command("cancel"))
@form_router.message(F.text.casefold() == "отмена")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """
    Функция для "реакции" на команду '/cancel' и на слово 'отмена'
    """
    current_state = await state.get_state()
    if current_state is None:
        await message.answer("Отменять пока нечего...")
        return

    await state.clear()
    await message.answer("Отменил все состояния и перешёл в обычный режим.")


@form_router.message(Command("profession"))
async def command_weather_coord_handler(message: Message, state: FSMContext) -> None:
    """
    Функция для "реакции" на команду `/profession`
    """
    await state.set_state(CoordsForm.favorite_subjects)
    await message.answer(
        "Вызвана команда подбора подходящей тебе профессии.\n"
        "Для продолжения напиши через запятую, какие предметы в школе тебе нравятся.\n"
        "Если предмет один, то напиши только его без знаков препинания.\n" 
        "Например: математика, английский язык, литература / математика.\n\n" 
        "Для отмены ввода - вызови команду /cancel или напиши слово 'отмена'."
    )

@form_router.message(CoordsForm.favorite_subjects)
async def process_favorite_subjects(message: Message, state: FSMContext) -> None:
    
    await message.answer(f"Хорошо! Теперь точно также напиши через запятую, какие предметы в школе тебе абсолютно не нравятся.\n"
                         "Если предмет один, то напиши только его без знаков препинания.\n\n"
                         "Для отмены ввода - вызови команду /cancel или напиши слово 'отмена'.")
    await state.update_data(favorite_subjects=message.text)
    await state.set_state(CoordsForm.unloved_subjects)

@form_router.message(CoordsForm.unloved_subjects)
async def process_unloved_subjects(message: Message, state: FSMContext) -> None:
    await message.answer(f"Отлично! Далее также через запятую напиши, какие экзамены ты сдал или собираешься сдавать\n"
                         "(Напиши все, включая русский язык и математику (с указанием уровня - базовая или профильная)).\n\n"
                         "Для отмены ввода - вызови команду /cancel или напиши слово 'отмена'.")
    await state.update_data(unloved_subjects=message.text)
    await state.set_state(CoordsForm.exams)

@form_router.message(CoordsForm.exams)
async def process_exams(message: Message, state: FSMContext) -> None:
    await message.answer(f"Осталось совсем чуть-чуть! Теперь напиши, какие профессии тебя интересуют "
                         "или чем ты любишь заниматься, что тебе по душе в следующем формате:\n"
                         "'Мне интересны профессии, связанные с... (например, животными)' /\n" 
                         "'Я люблю... (например, вышивать)' /\n"
                         "'Мне по душе... (например, спокойная работа)'\n"
                         "Можешь дописать все указанные фразы сразу, но через запятую.\n\n"
                         "Для отмены ввода - вызови команду /cancel или напиши слово 'отмена'.")
    await state.update_data(exams=message.text)
    await state.set_state(CoordsForm.interesting)

@form_router.message(CoordsForm.interesting)
async def process_interesting(message: Message, state: FSMContext) -> None:
    await message.answer(f"Последний параметр! Теперь напиши, какие профессии тебя не интересуют "
                         "или чем ты не любишь заниматься, что тебе не по душе в таком же формате:\n"
                         "'Мне не интересны профессии, связанные с... (например, животными)' /\n" 
                         "'Я не люблю... (например, вышивать)' /\n"
                         "'Мне не по душе... (например, спокойная работа)'\n"
                         "Можешь дописать все указанные фразы сразу, но через запятую.\n\n"
                         "Для отмены ввода - вызови команду /cancel или напиши слово 'отмена'.")
    data = await state.update_data(interesting=message.text)
    await state.set_state(CoordsForm.not_interesting)  

@form_router.message(CoordsForm.not_interesting)
async def process_not_interesting(message: Message, state: FSMContext) -> None:
    data = await state.update_data(not_interesting=message.text)
    favorite_subjects, unloved_subjects, exams, interesting, not_interesting  = data["favorite_subjects"], data["unloved_subjects"], data["exams"], data["interesting"], data["not_interesting"]
    with GigaChat(credentials="ZjY5MWE1NGItM2MxNy00YzE3LWI1YmEtZmMxNzExNmVhZTlmOjAwYzU0ZjYzLTkyZTEtNDk3Yi1iY2FkLWVlY2E4MTliNmQ4MA==", verify_ssl_certs=False) as giga:
        response = giga.chat(f"Какие профессии мне подойдут, если мне нравятся {favorite_subjects}; не нравятся {unloved_subjects}; я сдал (или планирую сдавать) экзамены по предметам: {exams}; при этом {interesting} и {not_interesting}?")
        itog = response.choices[0].message.content
        await message.answer(itog)
    await state.clear()
    
          

async def main() -> None:
    # Объект бота - отвечает за настройки бота (в первую очередь за токен)
    bot = Bot(token=TOKEN)

    dp = Dispatcher()

    # Подключаем к диспетчеру роутер обработки событий формы
    dp.include_router(form_router)
    
    # Запускаем бесконечный цикл запроса уведомлений от Телеграма
    await dp.start_polling(bot)


if __name__ == "__main__":
    # "Техническая" для получения сведений о работе бота в консоли приложения
    logging.basicConfig(level=logging.INFO)
    # Запуск awaitable объекта с помощью модуля asyncio
    asyncio.run(main())


