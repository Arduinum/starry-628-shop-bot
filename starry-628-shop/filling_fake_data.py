from faker import Faker
from os import path, makedirs
from random import randint, choice
from pathlib import Path
from sqlalchemy import insert
from asyncio import run

from shop_app.database.models.shop_model import Category, Product
from shop_app.database.models.validators import CategoriesShop
from shop_app.database.cruds.main_crud import get_session, async_engine
from shop_app.database.cruds.category_crud import get_all_categories
from shop_app.utils.logger import logger
from shop_app.utils.utils import get_message
from shop_app.storage.s3_api import add_func_loop, upload_file
from shop_app.settings import settings


faker = Faker()
logger.name = __name__


def create_file(base_path: str, name: str) -> None:
    """Функция для создания файла"""

    if base_path and name:
        if not path.exists(base_path):
            makedirs(name=base_path)

        with open(
            file=f"{base_path}/{name}", 
            mode='w', 
            encoding='utf-8'
        ) as file:
            file.write(name.split('.')[0] if '.' in name else name)


def gen_fake_categories(count: int, fake: Faker) -> list[Category]:
    """Функция для генерирования фейковых данных для категории"""

    categories = [Category, []]

    for _ in range(count):
        categories[1].append({'title': fake.word(), 'is_active': True})
    return categories


async def gen_fake_products(categories_valid_models: list[CategoriesShop], 
data: dict) -> list[Product]:
    """Функция для генерирования фейковых данных для продукта"""

    products = [Product, []]
    base_path = f"{Path(__file__).resolve().parent}/test_file"
    image_base_path = f"{Path(__file__).resolve().parent.parent}/shop_app/storage"

    for _ in range(data.get('count')):
        random_category = choice(categories_valid_models)
        fake = data.get('fake')
        
        for _ in range(15):
            file_name = fake.file_name()
            file_path = f"{base_path}/{file_name}"
            create_file(base_path=base_path, name=file_name)

            if path.exists(file_path):
                products[1].append({
                    'image': data.get('name_image'),
                    'title': fake.word(),
                    'description': fake.sentence(),
                    'price': randint(1, 100000),  # 100к максимальная сумма
                    'name_file': file_name,
                    'category_id': random_category.id,
                    'is_active': True
                })

                await add_func_loop(
                    upload_file, 
                    base_path, 
                    data.get('file_bucket', file_name)
                )

    await add_func_loop(
        upload_file, 
        image_base_path, 
        data.get('img_bucket'), 
        data.get('name_image')
    )

    return products


async def add_fake_data(models_data_fake: list) -> None:
    """Асинхронная функция для работы для добавления фековых данных"""

    try:
        new_session = get_session(async_engine=async_engine)
        async with new_session() as async_session:
            for data in models_data_fake[1]:
                query = insert(models_data_fake[0]).values(**data)
                await async_session.execute(query)

            await async_session.commit()
            logger.info((f'{get_message("create_fake_data_table")} ' 
                        f'{models_data_fake[0].__tablename__}'))
    # Todo - временное решение. Нужно будет отловить конкретные ошибки.
    except Exception as err:
        message = f'{err.__class__.__name__}: {err}'
        logger.error(message)
        await async_session.rollback()


async def filling() -> None:
    """Функция для заполнения фейковыми данными"""

    #генерируем фейковые данные категорий для бд
    fake_categories = gen_fake_categories(count=25, fake=faker)
    
    # заполняем бд
    await add_fake_data(models_data_fake=fake_categories)

    categories_valid_vodels = await get_all_categories()

    data = {
        'count': len(categories_valid_vodels),
        'fake': faker,
        'file_bucket': 'files-bucket',
        'img_bucket': 'img-bucket',
        'name_image': 'test.jpg'
    }

    # генерируем фейковые данные продукта для бд
    fake_products = await gen_fake_products(
        categories_valid_models=categories_valid_vodels, 
        data=data
    )

    # создать bucket для файлов
    # await add_func_loop(create_bucket, 'files-bucket')

    # # создать bucket для картинок
    # await add_func_loop(create_bucket, 'img-bucket')

    # заполняем бд
    await add_fake_data(models_data_fake=fake_products)


def main():
    """Главная функция для вызова заполнения данных"""
    
    run(filling())
