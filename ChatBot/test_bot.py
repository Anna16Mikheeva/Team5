import pytest
from unittest.mock import patch, AsyncMock
from aiogram import types
from bot import (
    command_start_handler,
    command_help_handler,
    cancel_handler,
    command_weather_coord_handler,
    process_favorite_subjects,
    process_not_interesting,
    CoordsForm
)

# Помечаем все тесты как асинхронные.
pytestmark = pytest.mark.asyncio

#-----------------------------------------------------------

# Тесты

# Команда /start.
# Проверяет корректность ответа бота на команду /start.
@pytest.mark.asyncio
async def test_start_command(message):
    await command_start_handler(message)
    
    # Проверка, что бот отправил одно сообщение.
    message.answer.assert_awaited_once()
    # Проверка, что сообщение содержит приветствие.
    assert "Привет" in message.answer.call_args[0][0]
    # Проверка описания функционала.
    assert "Профессия для тебя" in message.answer.call_args[0][0]

# Команда /help.
# Проверяет корректность справочной информации.
@pytest.mark.asyncio
async def test_help_command(message):
    await command_help_handler(message)
    
    # Проверка, что бот отправил одно сообщение.
    message.answer.assert_awaited_once()
    # Заголовок.
    assert "Справочная информация" in message.answer.call_args[0][0]
    # Описание команды.
    assert "/profession" in message.answer.call_args[0][0]

# Команда /cancel в неактивном состоянии.
# Проверяет поведение при отмене с неактивным диалогом.
@pytest.mark.asyncio
async def test_cancel_handler_no_state(message, state):
    # Повторяем отсутствие состояния.
    state.get_state.return_value = None
    await cancel_handler(message, state)
    
    # Проверка вывода сообщения.
    message.answer.assert_awaited_once_with("Отменять пока нечего...")

# Команда /cancel в активном состоянии.
# Проверяет поведение при отмене с активного диалога.
@pytest.mark.asyncio
async def test_cancel_handler_with_state(message, state):
    # Повторяем активное состояния.
    state.get_state.return_value = "some_state"
    await cancel_handler(message, state)
    
    # Проверяем, что состояние очищено.
    state.clear.assert_awaited_once()
    # Проверка вывода сообщения.
    message.answer.assert_awaited_once_with("Отменил все состояния и перешёл в обычный режим.")

# Команда /profession.
# Проверка инициализации диалога по подбору профессии.
@pytest.mark.asyncio
async def test_profession_command(message, state):
    await command_weather_coord_handler(message, state)
    
    # Проверяем установлено ли правильное состояние.
    state.set_state.assert_awaited_once_with(CoordsForm.favorite_subjects)
    # Проверяем, что бот отправил сообщение один раз.
    message.answer.assert_awaited_once()
    # Проверка сообщения с инструкцией ответов.
    assert "напиши через запятую" in message.answer.call_args[0][0]

# Обработка любимых предметов.
# Сохранение любимых предметов и переход к слкдующему шагу.
@pytest.mark.asyncio
async def test_process_favorite_subjects(message, state):
    message.text = "математика, физика"
    await process_favorite_subjects(message, state)
    
    # Проверяем, что данные сохранены.
    state.update_data.assert_awaited_once_with(favorite_subjects=message.text)
    # Переход к следующему шагу.
    state.set_state.assert_awaited_once_with(CoordsForm.unloved_subjects)
    # Проверяем, что бот отправил сообщение один раз.
    message.answer.assert_awaited_once()
    # Запрашиваем нелюбимые предметы.
    assert "абсолютно не нравятся" in message.answer.call_args[0][0]

# Обработка того, что неинтересно.
@pytest.mark.asyncio
async def test_process_not_interesting(message, state):
    # Повторяем ввод.
    message.text = "не люблю рутину"
    # Подготавливаем данные.
    state.get_data.return_value = {
        "favorite_subjects": "математика",
       "unloved_subjects": "литература",
        "exams": "русский, математика",
        "interesting": "программирование"
    }
    
    # Используем моки.
    with patch('bot.GigaChat') as mock_giga:
        mock_giga.return_value.__enter__.return_value.chat.return_value.choices = [
            AsyncMock(message=AsyncMock(content="Тестовая рекомендация"))
        ]
        
        await process_not_interesting(message, state)
        # Проверяем ответ от нейросети.
        message.answer.assert_awaited_once_with("Тестовая рекомендация")
        # Очищаем состояние.
        state.clear.assert_awaited_once()
        