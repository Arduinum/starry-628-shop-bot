from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from shop_app.callbacks.callbacks import (
    PopUpCallback, 
    CategoryEditCallback,
    CategoryEditFieldsCallback,
    CategoryCreateCallback,
    CategoryCreateFieldCallback,
    CategoryDeleteCallback,
    CategoryDeleteCrudCallback,
    ProductDeleteCallback,
    ProductDeleteCrudCallback,
    ProductEditCallback,
    ProductEditFieldsCallback,
    ProductCreateCallback,
    ProductCreateFieldCallback
)
from shop_app.settings import bot, settings
from shop_app.utils.utils import get_message
from shop_app.utils.logger import logger
from shop_app.database.cruds.category_crud import (
    get_category, 
    edit_category,
    add_category,
    delete_category
)
from shop_app.database.cruds.product_crud import (
    get_product,
    delete_product,
    edit_product,
    add_product
)
from shop_app.keyboards.admin_inline_keyboards import (
    menu_edit_category_inline_keyboard,
    menu_create_category_inline_keyboard,
    menu_delete_category_inline_keyboard,
    menu_delete_product_inline_keyboard,
    menu_edit_product_inline_keyboard,
    menu_create_product_inline_keyboard
)
from shop_app.utils.state_forms import (
    EditCategoryForm, 
    CreateCategoryForm, 
    EditProductForm,
    CreateProductForm
)
from shop_app.database.models.validators import (
    CategoryCreateShop, 
    ProductCreateShop
)
from shop_app.storage.s3_api import upload_file, add_func_loop


router_admin = Router(name=__name__)
logger.name = __name__


@router_admin.startup()
async def start_bot() -> None:
    """Асинхронная функция для отправки сообщения о запуске бота"""

    message = get_message('start_bot')
    logger.info(message)
    
    await bot.send_message(
        chat_id=settings.admin_id, 
        text=message
    )


@router_admin.shutdown()
async def stop_bot() -> None:
    """Асинхронная функция для отправки сообщения о остановке бота"""
    
    message = get_message('stop_bot')
    logger.info(message)

    await bot.send_message(
        chat_id=settings.admin_id, 
        text=message
    )


@router_admin.callback_query(PopUpCallback.filter())
async def pop_up_callback_action(call: CallbackQuery, 
    callback_data: PopUpCallback) -> None:
    """Асинхронная функция для отправки pop-up уведомлений"""

    await call.answer(text=callback_data.text, cache_time=10)


@router_admin.callback_query(CategoryEditCallback.filter(), 
F.from_user.id==settings.admin_id)
async def category_edit_callback_action(call: CallbackQuery,
    callback_data: CategoryEditCallback) -> None:
    """Асинхронная функция для редактирования категории админом"""

    category = await get_category(category_id=callback_data.category_id)

    if category:
        await call.message.answer(
            text=(f"{get_message('menu_edit')}Название: {category.title}\n"
                  f"Статус: {category.is_active}"), 
            reply_markup=menu_edit_category_inline_keyboard(category=category)
        )
    else:
        await call.message.answer(
            text=get_message('category_not_found')
        )


@router_admin.callback_query(CategoryEditFieldsCallback.filter(), 
F.from_user.id==settings.admin_id)
async def category_edit_fields_callback_action(call: CallbackQuery,
    state: FSMContext, callback_data: CategoryEditFieldsCallback) -> None:
    """Асинхронная функция для редактирования полей категории админом"""

    await state.set_state(EditCategoryForm.FIELDS)
    data = {'category_id': callback_data.category_id}

    if callback_data.title:
        data['title'] = callback_data.title
    
    if isinstance(callback_data.is_active, bool):
        category = await get_category(category_id=callback_data.category_id)
        is_active = False if callback_data.is_active else True
        category.is_active = is_active

        await edit_category(category_valid_model=category)
        await call.message.answer(
            f"{get_message('edit_success')} is_active={is_active}",
            parse_mode=None
        )
    else:    
        await state.update_data(data=data)
        await call.message.answer(
            text=f"{get_message('edit_field')} {callback_data.title}"
        )


@router_admin.message(EditCategoryForm.FIELDS, F.from_user.id==settings.admin_id, 
F.text.len() > 0)
async def category_edit_save_handler(message: Message, state: FSMContext):
    """
    Асинхронная функция для сохранения данных полей категории админом
    """
    
    data = await state.get_data()
    category_id = data.get('category_id')
    category = await get_category(category_id=category_id)
    await state.clear()

    if category:
        fields_dict = category.model_fields
        
        for key in data.keys():
            if fields_dict.get(key):
                setattr(category, key, message.text)
            
                await edit_category(category_valid_model=category)
                await message.answer(get_message('edit_success'))
    else:
        await message.answer(text=get_message('category_not_found'))


@router_admin.callback_query(CategoryCreateCallback.filter(), 
F.from_user.id==settings.admin_id)
async def category_create_callback_action(call: CallbackQuery) -> None:
    """Асинхронная функция для создания категории админом"""

    await call.message.answer(
        text=get_message('menu_create_category'),
        reply_markup=menu_create_category_inline_keyboard()
    )


@router_admin.callback_query(CategoryCreateFieldCallback.filter(), 
F.from_user.id==settings.admin_id)
async def category_create_field_callback_action(call: CallbackQuery,
    state: FSMContext, callback_data: CategoryCreateFieldCallback) -> None:
    """Асинхронная функция для создания нового поля категории админом"""

    if callback_data.title == get_message('status_button_pressed'):
        field_name = 'title'
        
        await state.set_state(CreateCategoryForm.FIELDS)
        await state.update_data(data={field_name: callback_data.title})
        await call.message.answer(
            text=f"{get_message('add_field')} {field_name}"
        )


@router_admin.message(CreateCategoryForm.FIELDS, 
F.from_user.id==settings.admin_id, F.text.len() > 0)
async def category_create_save_handler(message: Message, state: FSMContext):
    """
    Асинхронная функция для сохранения данных новой категории 
    админом
    """

    data = await state.get_data()
    await state.clear()
    
    if data.get('title'):
        category_valid_model = CategoryCreateShop
        await add_category(
            category_valid_create_model=category_valid_model(
                title=message.text,
                is_active=False
            )
        )
        fields_str = f"title: {message.text}\nis_active: False"
        await message.answer(
            text=f"{get_message('save_fields_info')}{fields_str}",
            parse_mode=None
        )


@router_admin.callback_query(CategoryDeleteCallback.filter())
async def category_delete_callback_action(call: CallbackQuery,
callback_data: CategoryDeleteCallback) -> None:
    """Асинхронная функция для удаления категории админом"""

    category = await get_category(category_id=callback_data.category_id)

    if category:
        await call.message.answer(
            text=f"{get_message('confirm_delete')} {category.title}?",
            reply_markup=menu_delete_category_inline_keyboard(category=category)
        )
    else:
        await call.message.answer(
            text=get_message('category_not_found')
        )


@router_admin.callback_query(CategoryDeleteCrudCallback.filter())
async def delete_category_crud_callback_action(call: CallbackQuery, 
callback_data: CategoryDeleteCrudCallback):
    """Асинхронная функция для удаления категории из бд"""

    del_category = await delete_category(category_id=callback_data.category_id)

    if del_category:
        await call.answer(text=f"{get_message('delete_success')}", cache_time=10)
    else:
        await call.answer(text=f"{get_message('delete_fail')}", cache_time=10)


@router_admin.callback_query(ProductDeleteCallback.filter())
async def product_delete_callback_action(call: CallbackQuery,
callback_data: ProductDeleteCallback) -> None:
    """Асинхронная функция для удаления продукта админом"""

    product = await get_product(product_id=callback_data.product_id)

    if product:
        await call.message.answer(
            text=f"{get_message('confirm_delete')} {product.title}?",
            reply_markup=menu_delete_product_inline_keyboard(product=product)
        )
    else:
        await call.message.answer(
            text=get_message('product_not_found')
        )


@router_admin.callback_query(ProductDeleteCrudCallback.filter())
async def delete_product_crud_callback_action(call: CallbackQuery, 
callback_data: ProductDeleteCrudCallback):
    """Асинхронная функция для удаления продукта из бд"""

    del_product = await delete_product(product_id=callback_data.product_id)

    if del_product:
        await call.answer(text=f"{get_message('delete_success')}", cache_time=10)
    else:
        await call.answer(text=f"{get_message('delete_fail')}", cache_time=10)


@router_admin.callback_query(ProductEditCallback.filter(), 
F.from_user.id==settings.admin_id)
async def product_edit_callback_action(call: CallbackQuery,
    callback_data: ProductEditCallback) -> None:
    """Асинхронная функция для редактирования продукта админом"""

    product = await get_product(product_id=callback_data.product_id)

    if product:
        names_fields = get_message('names_fields')
        await call.message.answer(
            text=(f"{get_message('menu_edit')}"
                  f"{names_fields.get('title')}: {product.title}\n"
                  f"{names_fields.get('description')}: "
                  f"{'отсутствует' if not product.description \
                    else product.description}\n"
                  f"{names_fields.get('price')}: {product.price}\n"
                  f"{names_fields.get('name_file')}: "
                  f"{'отсутствует' if not product.name_file \
                    else product.name_file}\n"
                  f"{names_fields.get('id_category')}: {product.category_id}\n"
                  f"{names_fields.get('is_active')}: "
                  f"{'True' if product.is_active else 'False'}"), 
            reply_markup=menu_edit_product_inline_keyboard(product=product),
            parse_mode=None
        )
    else:
        await call.message.answer(
            text=get_message('category_not_found')
        )


@router_admin.callback_query(ProductEditFieldsCallback.filter(), 
F.from_user.id==settings.admin_id)
async def product_edit_fields_callback_action(call: CallbackQuery, 
state: FSMContext, callback_data: ProductEditFieldsCallback) -> None:
    """Асинхронная функция для редактирования полей продукта админом"""

    await state.set_state(EditProductForm.FIELDS)
    data = {'product_id': callback_data.product_id}
    text = get_message('edit_field')

    if callback_data.title:
        text = f"{text} {callback_data.title}"
        data['title'] = callback_data.title
    elif callback_data.description:
        text = f"{text} {callback_data.description}"
        data['description'] = callback_data.description
    elif callback_data.price:
        text = f"{text} {callback_data.price}"
        data['price'] = callback_data.price
    elif callback_data.category_id:
        text = f"{text} {callback_data.category_id}"
        data['category_id'] = callback_data.category_id
    
    if isinstance(callback_data.is_active, bool):
        product = await get_product(product_id=callback_data.product_id)
        is_active = False if callback_data.is_active else True
        product.is_active = is_active
        
        await edit_product(product_valid_model=product)
        await call.message.answer(
            f"{get_message('edit_success')} is_active={is_active}",
            parse_mode=None
        )
    elif callback_data.name_file:
        text = get_message('upload_file')
        text = f"{text} {callback_data.name_file}"
        await state.update_data(data=data)
        await call.message.reply(text=text)
    else:
        await state.update_data(data=data)
        await call.message.answer(text=text)


@router_admin.message(F.from_user.id==settings.admin_id, F.document, 
EditProductForm.FIELDS)
async def file_save_handler(message: Message, state: FSMContext) -> None:
    """Асинхронная функция для сохранения файла от пользователя"""

    file_info = await bot.get_file(message.document.file_id)
    downloaded_file = await bot.download_file(file_info.file_path)

    if downloaded_file:
        result_upload = await add_func_loop(
            upload_file, 
            downloaded_file.getvalue(), 
            settings.storage_file,
            message.document.file_name
        )
        
        data = await state.get_data()
        product_id = data.get('product_id')
        await state.clear()
        product = await get_product(product_id=product_id)

        if result_upload and product:
            product.name_file = message.document.file_name
            await edit_product(product_valid_model=product)
            
            await message.answer(get_message('file_upload_success'))
        else:
            await message.answer(text=get_message('not_save_file_s3'))
    else:
        await message.answer(text=get_message('file_not_upload'))



@router_admin.message(EditProductForm.FIELDS, F.from_user.id==settings.admin_id, 
F.text.len() > 0)
async def product_edit_save_handler(message: Message, state: FSMContext):
    """
    Асинхронная функция для сохранения данных полей продукта админом
    """

    data = await state.get_data()
    product_id = data.pop('product_id')
    product = await get_product(product_id=product_id)
    await state.clear()

    if product:
        fields_dict = product.model_fields

        for key in data.keys():
            if fields_dict.get(key):
                if isinstance(data[key], int):
                    setattr(product, key, int(message.text))
                else:
                    setattr(product, key, message.text)
                await edit_product(product_valid_model=product)
                await message.answer(get_message('edit_success'))
    else:
        await message.answer(text=get_message('product_not_found'))


@router_admin.callback_query(ProductCreateCallback.filter(), 
F.from_user.id==settings.admin_id)
async def product_create_callback_action(call: CallbackQuery,
callback_data: ProductCreateCallback) -> None:
    """Асинхронная функция для создания продукта админом"""

    category = await get_category(category_id=callback_data.category_id)

    if category:
        await call.message.answer(
            text=get_message('menu_create_product'),
            reply_markup=menu_create_product_inline_keyboard(
                category_valid_model=category
            )
        )


@router_admin.callback_query(ProductCreateFieldCallback.filter(), 
F.from_user.id==settings.admin_id)
async def product_create_field_callback_action(call: CallbackQuery,
    state: FSMContext, callback_data: ProductCreateFieldCallback) -> None:
    """Асинхронная функция для создания нового поля продукта админом"""

    if callback_data.title == get_message('status_button_pressed'):
        field_name = 'title'
        
        await state.set_state(CreateProductForm.FIELDS)
        await state.update_data(data={
            field_name: callback_data.title,
            'category_id': callback_data.category_id
        })
        await call.message.answer(
            text=f"{get_message('add_field')} {field_name}"
        )


@router_admin.message(CreateProductForm.FIELDS, 
F.from_user.id==settings.admin_id, F.text.len() > 0)
async def product_create_save_handler(message: Message, state: FSMContext):
    """
    Асинхронная функция для сохранения данных нового продукта админом
    """

    data = await state.get_data()
    await state.clear()

    if data.get('title'):
        product_valid_model = ProductCreateShop
        
        new_product = await add_product(
            product_valid_model=product_valid_model(
                title=message.text,
                category_id=data.get('category_id')
            )
        )

        if new_product:
            names_fields = get_message('names_fields')
            # в json лучше поместить отсутствует и прочие значения что стандартизировать
            text = (f"{get_message('save_fields_info')}"
                    f"{names_fields.get('title')}: {message.text}\n"
                    f"{names_fields.get('description')}: отсутствует\n"
                    f"{names_fields.get('price')}: 0\n"
                    f"{names_fields.get('name_file')}: отсутствует\n"
                    f"{names_fields.get('name_image')}: default.jpg\n"
                    f"{names_fields.get('id_category')}: {data.get('category_id')}\n"
                    f"{names_fields.get('is_active')}: False") 
            await message.answer(text=text, parse_mode=None)
        else:
            await message.answer(
                text=get_message('create_product_fail'), 
                parse_mode=None
            )
