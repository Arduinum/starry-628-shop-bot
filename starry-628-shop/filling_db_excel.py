import pandas as pd
from pathlib import Path
from asyncio import run


from shop_app.database.models.validators import (
    CategoryCreateShop, 
    ProductCreateShopAll
)
from shop_app.utils.logger import logger
from shop_app.utils.errors import EmptyFieldError, message_err
from shop_app.database.cruds.category_crud import get_category_id, add_category
from shop_app.database.cruds.product_crud import add_product
from shop_app.settings import settings
from shop_app.utils.utils import get_message


logger.name = __name__


def check_category_excel(path_excel: str) -> list[CategoryCreateShop] | None:
    """Функция для проверки excel документа с категориями"""

    try:
        doc_name = path_excel.split('/')[-1]
        logger.info(f'{get_message('start_check_excel')} "{doc_name}".')

        if not doc_name.endswith('.xlsx'): 
            logger.warning(get_message('excel_format')) 
            return None
        
        data_exсel = pd.read_excel(path_excel, sheet_name='Лист1')

        if data_exсel.isnull().any().any():
            raise EmptyFieldError(message_err.get(
                'field_doc_empty').replace('doc_name', doc_name))

        category_valid_models = list()
        names_fields = get_message('names_fields')
        
        for i, row in enumerate(data_exсel.iloc):
            if i != 0:
                valid_model = CategoryCreateShop(
                    title=row.get(names_fields.get('title')),
                    is_active=bool(row.get(names_fields.get('is_active')))
                )

                category_valid_models.append(valid_model)
    except EmptyFieldError as err:
        logger.error(f'{err.__class__.__name__}: {err}')
    except FileNotFoundError as err:
        field_doc_empty = message_err.get('excel_doc_not_found')
        logger.error(f'{field_doc_empty} - {err.__class__.__name__}: {err}')
    else:
        logger.info(get_message('excel_checked').replace('doc_name', doc_name))
        return category_valid_models


async def check_product_excel(path_excel: str) -> list[ProductCreateShopAll] | None:
    """Асинхронная функция для проверки excel документа с продуктами"""

    try:
        doc_name = path_excel.split('/')[-1]
        logger.info(f'{get_message('start_check_excel')} "{doc_name}".')

        if not doc_name.endswith('.xlsx'): 
            logger.warning(get_message('excel_format')) 
            return None
        
        data_exсel = pd.read_excel(path_excel, sheet_name='Лист1')
        
        if data_exсel.isnull().any().any():
            raise EmptyFieldError(message_err.get(
                'field_doc_empty').replace('doc_name', doc_name))
        
        product_valid_models = list()
        names_fields = get_message('names_fields')
        
        for i, row in enumerate(data_exсel.iloc):
            if i != 0:
                title_category = row.get(names_fields.get('title_category'))
                category_id = await get_category_id(title=title_category)

                valid_model = ProductCreateShopAll(
                    title=row.get(names_fields.get('title')),
                    description=row.get(names_fields.get('description')),
                    price=row.get(names_fields.get('price')),
                    name_image=row.get(names_fields.get('name_image')),
                    name_file=row.get(names_fields.get('name_file')),
                    category_id=category_id,
                    is_active=bool(row.get(names_fields.get('is_active')))
                )
                
                product_valid_models.append(valid_model)
    except EmptyFieldError as err:
        logger.error(f'{err.__class__.__name__}: {err}')
    except FileNotFoundError as err:
        field_doc_empty = message_err.get('excel_doc_not_found')
        logger.error(f'{field_doc_empty} - {err.__class__.__name__}: {err}')
    else:
        logger.info(get_message('excel_checked').replace('doc_name', doc_name))
        return product_valid_models


async def filling_catigories(valid_categories: list[CategoryCreateShop]) -> None:
    """Асинхронная функция для заполнения категорий"""

    table_name = 'Категория'
    if valid_categories:
        for valid_model in valid_categories:
            add_category_crud = await add_category(valid_model)
            
            if add_category_crud:
                logger.info(
                    get_message('crud_create_success').replace(
                        'title', 
                        valid_model.title
                    ).replace('table', table_name)
                )
            else:
                logger.warning(
                     get_message('crud_create_fail').replace(
                        'title', 
                        valid_model.title
                    ).replace('table', table_name)
                )


async def filling_products(valid_products: list[ProductCreateShopAll]) -> None:
    """Асинхронная функция для заполнения продуктов"""

    table_name = 'Продукт'

    if valid_products:
        for valid_model in valid_products:
            add_product_crud = await add_product(valid_model)

            if add_product_crud:
                logger.info(
                    get_message('crud_create_success').replace(
                        'title', 
                        valid_model.title
                    ).replace('table', table_name)
                )
            else:
                logger.warning(
                    get_message('crud_create_fail').replace(
                        'title', 
                        valid_model.title
                    ).replace('table', table_name)
                )    


def category_main() -> None:
    """Главная функция для вызова заполнения данных категории"""

    path_excel = (f'{Path(__file__).resolve().parent.parent}/'
                  f'{settings.excel_category_doc_path}')
    valid_model_categories = check_category_excel(path_excel=path_excel)
    
    run(filling_catigories(valid_categories=valid_model_categories))


async def product_filling_check() -> None:
    """
    Асинхронная функция для вызова проверки excel документа и заполнения
    данных продукта
    """

    path_excel = (f'{Path(__file__).resolve().parent.parent}/'
                  f'{settings.excel_product_doc_path}')
    valid_model_products = await check_product_excel(path_excel=path_excel) 

    await filling_products(valid_products=valid_model_products)


def product_main() -> None:
    """Главная функция для вызова корутины заполнения продукта данными"""

    run(product_filling_check())
