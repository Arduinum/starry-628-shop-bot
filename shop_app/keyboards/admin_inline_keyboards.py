from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from shop_app.callbacks.callbacks import (
    CategoryEditFieldsCallback, 
    MainMenuCallback,
    CategoryCallback,
    CategoryCreateFieldCallback,
    CategoriesCallback,
    CategoryDeleteCrudCallback,
    ProductCallback,
    ProductEditFieldsCallback,
    ProductDeleteCrudCallback,
    ProductCreateFieldCallback
)
from shop_app.database.models.validators import CategoriesShop, ProductShop
from shop_app.utils.utils import get_message


def menu_edit_category_inline_keyboard(category: CategoriesShop
) -> InlineKeyboardMarkup:
    """Inline клавиатура с кнопочным меню для редактирования категории"""

    builder = InlineKeyboardBuilder()
    text = get_message('edit_field_button')
    
    builder.button(
        text=f"{text['edit']} {text['fields']['title']}",
        callback_data=CategoryEditFieldsCallback(
            category_id=category.id,
            title=category.title
        ).pack()
    )
    builder.button(
        text=f"{text['edit']} {text['fields']['is_active']}",
        callback_data=CategoryEditFieldsCallback(
            category_id=category.id,
            is_active=category.is_active
        ).pack()
    )
    
    builder.button(
        text=f"{get_message('category_back')} {category.title}",
        callback_data=CategoryCallback(
            category_id=category.id,
            title=category.title
        ).pack()
    )
    builder.button(
        text=get_message('main_menu'),
        callback_data=MainMenuCallback().pack()
    )
    builder.adjust(1)
    return builder.as_markup()


def menu_create_category_inline_keyboard() -> InlineKeyboardMarkup:
    """Inline клавиатура с кнопочным меню для создания категории"""

    builder = InlineKeyboardBuilder()
    text = get_message('create_field_button')

    builder.button(
        text=f"{text['create']} {text['fields']['title']}",
        callback_data=CategoryCreateFieldCallback(
            title=get_message('status_button_pressed')
        ).pack()
    )

    builder.button(
        text=f"{get_message('categories_back')}",
        callback_data=CategoriesCallback(page=None).pack()
    )
    builder.button(
        text=get_message('main_menu'),
        callback_data=MainMenuCallback().pack()
    )

    builder.adjust(1)
    return builder.as_markup()


def menu_delete_category_inline_keyboard(category: CategoriesShop
) -> InlineKeyboardMarkup:
    """Inline клавиатура с кнопочным меню для удаления категории"""

    builder = InlineKeyboardBuilder()
    buttons_row = list()

    builder.button(
        text=get_message('delete'),
        callback_data=CategoryDeleteCrudCallback(category_id=category.id).pack()
    )
    
    category_back = InlineKeyboardButton(
        text=f"{get_message('category_back')} {category.title}",
        callback_data=CategoryCallback(
            category_id=category.id,
            title=category.title
        ).pack()
    )
    buttons_row.append(category_back)
    
    button_menu = InlineKeyboardButton(
        text=get_message('main_menu'),
        callback_data=MainMenuCallback().pack()
    )
    buttons_row.append(button_menu)
    
    builder.row(*buttons_row)
    return builder.as_markup()


def menu_create_product_inline_keyboard(category_valid_model: CategoriesShop) -> InlineKeyboardMarkup:
    """Inline клавиатура с кнопочным меню для создания продукта"""

    builder = InlineKeyboardBuilder()
    text = get_message('create_field_button')

    builder.button(
        text=f"{text['create']} {text['fields']['title']}",
        callback_data=ProductCreateFieldCallback(
            title=get_message('status_button_pressed'),
            category_id=category_valid_model.id
        ).pack()
    )

    builder.button(
        text=f"{get_message('category_back')} {category_valid_model.title}",
        callback_data=CategoryCallback(
            category_id=category_valid_model.id,
            title=category_valid_model.title
        ).pack()
    )
    builder.button(
        text=get_message('main_menu'),
        callback_data=MainMenuCallback().pack()
    )

    builder.adjust(1)
    return builder.as_markup()


def menu_edit_product_inline_keyboard(product: ProductShop
) -> InlineKeyboardMarkup:
    """Inline клавиатура с кнопочным меню для редактирования продукта"""

    builder = InlineKeyboardBuilder()
    edit_text = get_message('edit_field_button')

    builder.button(
        text=f"{edit_text['edit']} {edit_text['fields']['title']}",
        callback_data=ProductEditFieldsCallback(
            product_id=product.id,
            title=product.title
        ).pack()
    )

    builder.button(
        text=f"{edit_text['edit']} {edit_text['fields']['description']}",
        callback_data=ProductEditFieldsCallback(
            product_id=product.id,
            description=product.description
        ).truncate_fields().pack()
    )

    builder.button(
        text=f"{edit_text['edit']} {edit_text['fields']['file']}",
        callback_data=ProductEditFieldsCallback(
            product_id=product.id,
            name_file=product.name_file
        ).truncate_fields().pack()
    )

    builder.button(
        text=f"{edit_text['edit']} {edit_text['fields']['price']}",
        callback_data=ProductEditFieldsCallback(
            product_id=product.id,
            price=product.price
        ).pack()
    )

    builder.button(
        text=f"{edit_text['edit']} {edit_text['fields']['is_active']}",
        callback_data=ProductEditFieldsCallback(
            product_id=product.id,
            is_active=product.is_active
        ).pack()
    )

    builder.button(
        text=f"{edit_text['edit']} {edit_text['fields']['category_id']}",
        callback_data=ProductEditFieldsCallback(
            product_id=product.id,
            category_id=product.category_id
        ).pack()
    )

    builder.adjust(2)

    buttons_row = list()

    product_back_button = InlineKeyboardButton(
        text=f"{get_message('product_back')} {product.title}",
        callback_data=ProductCallback(
            product_id=product.id,
            title=product.title
        ).pack()
    )
    buttons_row.append(product_back_button)

    main_menu_button = InlineKeyboardButton(
        text=get_message('main_menu'),
        callback_data=MainMenuCallback().pack()
    )
    buttons_row.append(main_menu_button)
    
    builder.row(*buttons_row)    
    return builder.as_markup()


def menu_delete_product_inline_keyboard(product: ProductShop
) -> InlineKeyboardMarkup:
    """Inline клавиатура с кнопочным меню для удаления категории"""

    builder = InlineKeyboardBuilder()
    buttons_row = list()

    builder.button(
        text=get_message('delete'),
        callback_data=ProductDeleteCrudCallback(product_id=product.id).pack()
    )
    
    product_back = InlineKeyboardButton(
        text=f"{get_message('product_back')} {product.title}",
        callback_data=ProductCallback(
            product_id=product.id,
            title=product.title
        ).pack()
    )
    buttons_row.append(product_back)
    
    button_menu = InlineKeyboardButton(
        text=get_message('main_menu'),
        callback_data=MainMenuCallback().pack()
    )
    buttons_row.append(button_menu)
    
    builder.row(*buttons_row)
    return builder.as_markup()
