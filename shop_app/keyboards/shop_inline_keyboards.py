from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from shop_app.database.models.validators import (
    CategoriesShop, 
    ProductsShop,
    ProductShop
)
from shop_app.callbacks.callbacks import (
    CategoriesCallback,
    CategoryCallback,
    ProductCallback,
    PopUpCallback,
    MainMenuCallback,
    CategoryEditCallback,
    CategoryCreateCallback,
    CategoryDeleteCallback,
    ProductDeleteCallback,
    ProductEditCallback,
    ProductCreateCallback
)
from shop_app.utils.utils import get_message
from shop_app.settings import settings


def menu_shop_inline_keyboard() -> InlineKeyboardMarkup:
    """Inline клавиатура с кнопочным меню для магазина"""

    builder = InlineKeyboardBuilder()
    builder.button(
        text=get_message('categories'), 
        callback_data=CategoriesCallback().pack()
    )
    return builder.as_markup()


def menu_categories_inline_keyboard(categories: list[CategoriesShop], 
    chat_id: int | None = None, page: int = 0) -> InlineKeyboardMarkup:
    """Inline клавиатура с кнопочным меню для категорий"""

    builder = InlineKeyboardBuilder()
    items_on_page = 6
    start = page * items_on_page
    end = start + items_on_page
    count_pages = (len(categories) + items_on_page - 1) // items_on_page

    for validated_model in categories[start:end]:
        builder.button(
            text=validated_model.title, 
            callback_data=CategoryCallback(
                category_id=validated_model.id,
                title=validated_model.title
            )
        )

    builder.adjust(3)
    buttons_row = list()
    
    if page > 0:  
        button_left = InlineKeyboardButton(  
            text=get_message('left'),  
            callback_data=CategoriesCallback(
                page=page - 1
            ).pack()
        )    
        buttons_row.append(button_left)
    else: 
        button_left_plug = InlineKeyboardButton(  
            text=get_message('plug'),  
            callback_data=PopUpCallback(
                text=get_message('answer_start_page')
            ).pack()
        )
        buttons_row.append(button_left_plug)
    

    button_num_page = InlineKeyboardButton(
        text=f'{str(page + 1)}/{count_pages}',
        callback_data='None'
    )
    buttons_row.append(button_num_page)

    if end < len(categories):  
        button_right = InlineKeyboardButton(  
            text=get_message('right'),  
            callback_data=CategoriesCallback(
                page=page + 1
            ).pack()
        )
        buttons_row.append(button_right)
    else:
        button_right_plug = InlineKeyboardButton(  
            text=get_message('plug'),  
            callback_data=PopUpCallback(
                text=get_message('answer_end_page')
            ).pack()
        )
        buttons_row.append(button_right_plug)

    builder.row(*buttons_row)
    buttons_row.clear()

    if chat_id == settings.admin_id:
        create_category = InlineKeyboardButton(
            text=get_message('add_category'),
            callback_data=CategoryCreateCallback().pack()
        )
        buttons_row.append(create_category)
    
    button_menu = InlineKeyboardButton(
        text=get_message('main_menu'),
        callback_data=MainMenuCallback().pack()
    )
    buttons_row.append(button_menu)

    builder.row(*buttons_row)
    return builder.as_markup()


def menu_category_inline_keyboard(products: list[ProductsShop], 
    chat_id: int, page: int = 0) -> InlineKeyboardMarkup:
    """Inline клавиатура с кнопочным меню для категории продуктов"""

    builder = InlineKeyboardBuilder()
    items_on_page = 6
    start = page * items_on_page
    end = start + items_on_page
    count_pages = (len(products) + items_on_page - 1) // items_on_page
    category_id = products[0].category_id

    for validated_model in products[start:end]:
        builder.button(
            text=validated_model.title, 
            callback_data=ProductCallback(
                product_id=validated_model.id,
                title=validated_model.title
            )
        )
    
    builder.adjust(3)
    buttons_row = list()

    if page > 0:  
        button_left = InlineKeyboardButton(  
            text=get_message('left'),  
            callback_data=CategoryCallback(
                category_id=category_id,
                page=page - 1
            ).pack()
        )    
        buttons_row.append(button_left)
    else:
        button_left_plug = InlineKeyboardButton(  
            text=get_message('plug'),  
            callback_data=PopUpCallback(
                text=get_message('answer_start_page')
            ).pack() 
        )
        buttons_row.append(button_left_plug)
    
    button_num_page = InlineKeyboardButton(
        text=f'{str(page + 1)}/{count_pages}',
        callback_data='None'
    )
    buttons_row.append(button_num_page)

    if end < len(products):  
        button_right = InlineKeyboardButton(  
            text=get_message('right'),  
            callback_data=CategoryCallback(
                category_id=category_id,
                page=page + 1
            ).pack()
        )
        buttons_row.append(button_right)
    else:
        button_right_plug = InlineKeyboardButton(  
            text=get_message('plug'),  
            callback_data=PopUpCallback(
                text=get_message('answer_end_page')
            ).pack() 
        )
        buttons_row.append(button_right_plug)
    builder.row(*buttons_row)
    buttons_row.clear()

    button_categories = InlineKeyboardButton(
        text=get_message('categories_back'),
        callback_data=CategoriesCallback(page=None).pack()
    )
    buttons_row.append(button_categories)

    button_menu = InlineKeyboardButton(
        text=get_message('main_menu'),
        callback_data=MainMenuCallback().pack()
    )
    buttons_row.append(button_menu)
    builder.row(*buttons_row)
    
    if chat_id == settings.admin_id:
        buttons_row.clear()
        category_edit_button = InlineKeyboardButton(
            text=get_message('edit'),
            callback_data=CategoryEditCallback(category_id=category_id).pack()
        )
        buttons_row.append(category_edit_button)
        
        category_create_button = InlineKeyboardButton(
            text=get_message('add_product'),
            callback_data=ProductCreateCallback(category_id=category_id).pack()
        )
        buttons_row.append(category_create_button)
        builder.row(*buttons_row)
        buttons_row.clear()

        category_delete_button = InlineKeyboardButton(
            text=get_message('delete_category'),
            callback_data=CategoryDeleteCallback(category_id=category_id).pack()
        )
        buttons_row.append(category_delete_button)
        builder.row(*buttons_row)

    return builder.as_markup()


def pay_product_inline_keyboard(product: ProductShop, category: CategoriesShop, 
    chat_id: int) -> InlineKeyboardMarkup:
    """Inline клавиатура продукта с кнопкой pay"""
 
    builder = InlineKeyboardBuilder()
    buttons_row = list()

    button_pay = InlineKeyboardButton(
        text=f"{get_message('pay_star')} {product.price}", 
        pay=True
    )
    buttons_row.append(button_pay)
    builder.row(*buttons_row)
    buttons_row.clear()

    if chat_id == settings.admin_id:
        button_edit_product = InlineKeyboardButton(
            text=f"{get_message('edit')} {product.title}",
            callback_data=ProductEditCallback(product_id=product.id).pack()
        )
        buttons_row.append(button_edit_product)

        button_delete_product = InlineKeyboardButton(
            text=get_message('delete_product'),
            callback_data=ProductDeleteCallback(product_id=product.id).pack()
        )
        buttons_row.append(button_delete_product)
    
    builder.row(*buttons_row)
    buttons_row.clear()

    button_category = InlineKeyboardButton(
        text=f"{get_message('category_back')} {category.title}",
        callback_data=CategoryCallback(
            category_id=category.id,
            title=category.title,
            page=None
        ).pack()
    )
    buttons_row.append(button_category)

    button_menu = InlineKeyboardButton(
        text=get_message('main_menu'),
        callback_data=MainMenuCallback().pack()
    )
    buttons_row.append(button_menu)
    builder.row(*buttons_row)
    return builder.as_markup()
