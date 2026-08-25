from aiogram.types import CallbackQuery
from aiogram import Router

from shop_app.database.cruds.category_crud import get_all_categories 
from shop_app.database.cruds.product_crud import get_category_products
from shop_app.keyboards.shop_inline_keyboards import (
    menu_categories_inline_keyboard,
    menu_category_inline_keyboard
)
from shop_app.utils.utils import get_message
from shop_app.callbacks.callbacks import CategoryCallback, CategoriesCallback
from shop_app.settings import settings


router_shop = Router(name=__name__)


# асинхронные функции для отправки сообщений, работающие с CallbackQuery

@router_shop.callback_query(CategoriesCallback.filter())
async def categories_callback_action(call: CallbackQuery, 
    callback_data: CategoriesCallback):
    """
    Асинхронная функция для отправки данных, реагирующая на 
    CallbackQuery для категорий
    """
    
    chat_id = call.message.chat.id
    is_admin = True if settings.admin_id == chat_id else False
    categories = await get_all_categories(is_admin=is_admin)

    if categories:
        page = callback_data.page

        if page is None:
            await call.message.answer(
                text=get_message('categories_shop'),
                reply_markup=menu_categories_inline_keyboard(
                    categories=categories,
                    chat_id=chat_id
                )
            )
        else:
            await call.message.edit_reply_markup(
                reply_markup=menu_categories_inline_keyboard(
                    categories=categories,
                    page=page
                )
            )
    else:
        await call.message.answer(
            text=get_message('categories_not_found')
        )


@router_shop.callback_query(CategoryCallback.filter())
async def products_callback_action(call: CallbackQuery, \
    callback_data: CategoryCallback):
    """
    Асинхронная функция для отправки данных, реагирующая на 
    CallbackQuery для продуктов категории
    """
    
    category_id = callback_data.category_id
    chat_id = call.message.chat.id
    is_admin = True if settings.admin_id == chat_id else False
    products = await get_category_products(
        category_id=category_id, 
        is_admin=is_admin
    )

    if products:
        category = callback_data.title
        page = callback_data.page

        if page is None:
            await call.message.answer(
                text=f'{get_message('products_category')} {category}:\n\n',
                reply_markup=menu_category_inline_keyboard(
                    products=products,
                    chat_id=chat_id
                ),
                parse_mode=None
            )
        else:
            await call.message.edit_reply_markup(
                reply_markup=menu_category_inline_keyboard(
                    products=products, 
                    chat_id=chat_id,
                    page=page
                )
            )
    else:
        await call.message.answer(
            text=get_message('products_not_found')
        )
