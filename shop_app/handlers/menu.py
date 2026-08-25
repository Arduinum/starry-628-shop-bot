from aiogram.types import Message, CallbackQuery
from aiogram import Router
from aiogram.filters import Command

from shop_app.keyboards.shop_inline_keyboards import menu_shop_inline_keyboard
from shop_app.utils.utils import get_message
from shop_app.callbacks.callbacks import MainMenuCallback


router_menu = Router(name=__name__)


@router_menu.message(Command(commands='menu'))
async def shop_menu(message: Message):
	"""Асинхронная функция для отображения кнопочного меню магазина"""

	await message.answer(
		text=get_message('menu_shop'),
		reply_markup=menu_shop_inline_keyboard()
	)


@router_menu.callback_query(MainMenuCallback.filter())
async def shop_menu_callback_action(call: CallbackQuery):
	"""Асинхронная функция для отображения кнопочного меню магазина"""

	await call.message.answer(
		text=get_message('menu_shop'),
		reply_markup=menu_shop_inline_keyboard()
	)
