from sqlalchemy import select, update, delete, insert
from sqlalchemy.exc import (
    IntegrityError, 
    SQLAlchemyError, 
    NoResultFound,
    OperationalError
)
from asyncpg.exceptions import UniqueViolationError
from pydantic import ValidationError

from shop_app.database.models.shop_model import Product
from shop_app.database.cruds.main_crud import get_session, async_engine
from shop_app.database.models.validators import (
    ProductsShop, 
    ProductShop,
    ProductCreateShop
)
from shop_app.utils.logger import logger
from shop_app.utils.errors import message_err


logger.name = __name__


async def get_category_products(category_id: int, is_admin: bool=False
) -> list[ProductsShop]:
    """
    Асинхронная функция для получения списка валидированных моделей 
    ProductShop
    """

    try:
        product = Product
        async with get_session(async_engine=async_engine) as async_session:
            query = select(
                product.id, 
                product.title,
                product.category_id,
                product.is_active).filter(category_id == product.category_id
                ).order_by(product.created_at.asc()) if is_admin else select(
                    product.id, 
                    product.title,
                    product.category_id,
                    product.is_active).filter(
                        True == product.is_active,
                        category_id == product.category_id
                ).order_by(product.created_at.asc())
            result = await async_session.execute(query)
            products = result.mappings().fetchall()
            
            return [
                ProductsShop.model_validate(
                    obj=accept, 
                    from_attributes=True
                ) for accept in products
            ]
    except ConnectionError as err:
        message = f'{err.__class__.__name__}: {err}'
        logger.error(message)
    except SQLAlchemyError as err:
        message = f'{err.__class__.__name__}: {err}'
        logger.error(message)
    except TimeoutError as err:
        message = f'{err.__class__.__name__}: {err}'
        logger.error(message)
    except NoResultFound as err:
        message = f'{err.__class__.__name__}: {err}'
        logger.error(message)
    except OperationalError as err:
        message = f'{err.__class__.__name__}: {err}'
        logger.error(message)
    except ValidationError as err:
        message = f'{err.__class__.__name__}: {err}'
        logger.error(message)


async def get_product(product_id: int) -> ProductShop:
    """
    Асинхронная функция для получения валидированной модели ProductShop
    """

    try:
        product = Product
        async with get_session(async_engine=async_engine) as async_session:
            query = select(
                product.id, 
                product.title, 
                product.description,
                product.price,
                product.name_file,
                product.name_image,
                product.category_id,
                product.is_active
            ).where(product_id == product.id)
            result = await async_session.execute(query)
            product = result.mappings().first()

            return ProductShop.model_validate(obj=product, from_attributes=True)
    except ConnectionError as err:
        message = f'{err.__class__.__name__}: {err}'
        logger.error(message)
    except SQLAlchemyError as err:
        message = f'{err.__class__.__name__}: {err}'
        logger.error(message)
    except TimeoutError as err:
        message = f'{err.__class__.__name__}: {err}'
        logger.error(message)
    except NoResultFound as err:
        message = f'{err.__class__.__name__}: {err}'
        logger.error(message)
    except OperationalError as err:
        message = f'{err.__class__.__name__}: {err}'
        logger.error(message)
    except ValidationError as err:
        message = f'{err.__class__.__name__}: {err}'
        logger.error(message)


async def add_product(product_valid_model: ProductCreateShop) -> bool | None:
    """Асинхронная функция для создания продукта"""

    try:
        product = Product
        async with get_session(async_engine=async_engine) as async_session:
            query = insert(product).values(**product_valid_model.model_dump())
            await async_session.execute(query)
            await async_session.commit()
    except IntegrityError as err:
        orig = err.orig
        
        while hasattr(orig, '__cause__') and orig.__cause__:
            orig = orig.__cause__
        
        if isinstance(orig, UniqueViolationError):
            message_error = message_err.get('dublicate_rec_product').replace(
                'title', 
                product_valid_model.title
            ).replace(
                'category_id', 
                str(product_valid_model.category_id)
            )
            logger.error(f'{message_error}')
        else:
            logger.error(f'{err.__class__.__name__}: {err}')
    except ConnectionError as err:
        message = f'{err.__class__.__name__}: {err}'
        logger.error(message)
    except SQLAlchemyError as err:
        message = f'{err.__class__.__name__}: {err}'
        logger.error(message)
    except TimeoutError as err:
        message = f'{err.__class__.__name__}: {err}'
        logger.error(message)
    except OperationalError as err:
        message = f'{err.__class__.__name__}: {err}'
        logger.error(message)
    except ValidationError as err:
        message = f'{err.__class__.__name__}: {err}'
        logger.error(message)
    else:
        return True


async def edit_product(product_valid_model: ProductShop) -> bool | None:
    """Асинхронная функция для редактирования продукта"""

    try:
        product = Product
        async with get_session(async_engine=async_engine) as async_session:
            query = update(product).where(
                product_valid_model.id == product.id
            ).values(**product_valid_model.model_dump())
            
            await async_session.execute(query)
            await async_session.commit()
    except IntegrityError as err:
        orig = err.orig
        
        while hasattr(orig, '__cause__') and orig.__cause__:
            orig = orig.__cause__
        
        if isinstance(orig, UniqueViolationError):
            message_error = message_err.get('dublicate_rec_product').replace(
                'title', 
                product_valid_model.title
            ).replace(
                'category_id', 
                str(product_valid_model.category_id)
            )
            logger.error(f'{message_error}')
        else:
            logger.error(f'{err.__class__.__name__}: {err}')
    except ConnectionError as err:
        message = f'{err.__class__.__name__}: {err}'
        logger.error(message)
    except SQLAlchemyError as err:
        message = f'{err.__class__.__name__}: {err}'
        logger.error(message)
    except TimeoutError as err:
        message = f'{err.__class__.__name__}: {err}'
        logger.error(message)
    except OperationalError as err:
        message = f'{err.__class__.__name__}: {err}'
        logger.error(message)
    except ValidationError as err:
        message = f'{err.__class__.__name__}: {err}'
        logger.error(message)
    else:
        return True


async def delete_product(product_id: int) -> bool | None:
    """Асинхронная функция для удаления продукта"""

    try:
        product = Product
        async with get_session(async_engine=async_engine) as async_session:
            query = delete(product).where(product_id == product.id)

            await async_session.execute(query)
            await async_session.commit()
    except ConnectionError as err:
        message = f'{err.__class__.__name__}: {err}'
        logger.error(message)
    except SQLAlchemyError as err:
        message = f'{err.__class__.__name__}: {err}'
        logger.error(message)
    except TimeoutError as err:
        message = f'{err.__class__.__name__}: {err}'
        logger.error(message)
    except OperationalError as err:
        message = f'{err.__class__.__name__}: {err}'
        logger.error(message)
    else:
        return True
