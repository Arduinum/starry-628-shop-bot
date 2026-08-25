from aiogram.types import Message
from aiogram import Router
from aiogram.filters import Command, CommandStart

from shop_app.keyboards.shop_inline_keyboards import menu_shop_inline_keyboard
from shop_app.utils.utils import get_message
from shop_app.database.cruds.user_crud import check_chat_id, add_user
from shop_app.database.models.validators import UserCreate


router_info = Router(name=__name__)


@router_info.message(CommandStart())
async def start_command(message: Message) -> None:
    """Асинхронная функция для отправки приветственного сообщения"""

    chat_id = await check_chat_id(chat_id=message.chat.id)

    if not chat_id:
        user_valid_model = UserCreate(
            chat_id=message.chat.id,
            user_name=message.chat.username,
            first_name=message.chat.first_name,
            last_name=message.chat.last_name
        )
        await add_user(user_valid_model=user_valid_model)
        await message.answer(text=get_message('privacy_policy'))
        await message.answer(
            text=get_message('start'),
            reply_markup=menu_shop_inline_keyboard()
        )
    else:
        person_title = f"{message.chat.first_name} {message.chat.last_name}" \
            if message.chat.last_name else message.chat.first_name
        text = f"{person_title} {'д'}{get_message('start')[1:]}"
        await message.answer(
            text=text, 
            reply_markup=menu_shop_inline_keyboard()
        )


@router_info.message(Command(commands='help'))
async def help_command(message: Message) -> None:
    """Асинхронная функция для отправки сообщения со списком команд"""

    await message.answer(text=get_message('help'))


@router_info.message(Command(commands='info'))
async def info_command(message: Message) -> None:
    """Асинхронная функция для отправки сообщения информации о боте"""

    await message.answer(text=get_message('info'))


@router_info.message(Command(commands='privacy'))
async def privacy_policy_command(message: Message) -> None:
    """Асинхронная функция для отправки политики конфиденциальности"""

    await message.answer(text=get_message('privacy_policy'))
