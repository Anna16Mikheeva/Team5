import pytest
from unittest.mock import MagicMock, AsyncMock
from aiogram.types import User

@pytest.fixture
def user():
    return User(
        id=123,
        first_name="Test",
        is_bot=False,
        last_name="User",
        username="test_user"
    )

@pytest.fixture
def message(user):
    msg = MagicMock()
    msg.from_user = user
    msg.text = "test"
    msg.answer = AsyncMock()
    msg.reply = AsyncMock()
    return msg

@pytest.fixture
def state():
    mock = MagicMock()
    mock.get_state = AsyncMock(return_value=None)
    mock.set_state = AsyncMock()
    mock.update_data = AsyncMock()
    mock.get_data = AsyncMock(return_value={})
    mock.clear = AsyncMock()
    return mock