from sqlalchemy import select, update, insert, delete
from sqlalchemy.exc import (
    IntegrityError, 
    SQLAlchemyError, 
    NoResultFound,
    OperationalError
)
from asyncpg.exceptions import UniqueViolationError 
from pydantic import ValidationError

from shop_app.database.cruds.main_crud import get_session, async_engine
from shop_app.utils.logger import logger
from shop_app.database.models.shop_model import Category
from shop_app.database.models.validators import CategoriesShop, CategoryCreateShop
from shop_app.utils.errors import message_err


logger.name = __name__


async def get_all_categories(is_admin: bool=False) -> list[CategoriesShop]:
    """
    Асинхронная функция для получения списка валидированных моделей 
    CategoryShop
    """
    
    try:
        category = Category
        async with get_session(async_engine=async_engine) as async_session: 
            query = select(
                category.id, 
                category.title, 
                category.is_active
            ).order_by(
                category.created_at.asc()) if is_admin else select(
                category.id, 
                category.title, 
                category.is_active
            ).filter(True == category.is_active).order_by(
                category.created_at.asc())
            result = await async_session.execute(query)
            categories = result.mappings().fetchall()
            
            return [
                CategoriesShop.model_validate(
                    obj=accept, 
                    from_attributes=True
                ) for accept in categories
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


async def get_category(category_id: int) -> CategoriesShop:
    """Асинхронная функция для получения категории по её id"""

    try:
        category = Category
        async with get_session(async_engine=async_engine) as async_session:
            query = select(
                category.id, 
                category.title,
                category.is_active
            ).where(category_id == category.id)
            result = await async_session.execute(query)
            category = result.mappings().first()
            
            return CategoriesShop.model_validate(
                obj=category, 
                from_attributes=True
            )
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


async def get_category_id(title: str) -> CategoriesShop:
    """Асинхронная функция для получения id категории по её названию"""

    try:
        category = Category
        async with get_session(async_engine=async_engine) as async_session:
            query = select(
                category.id, 
                category.title,
                category.is_active
            ).where(title == category.title)
            result = await async_session.execute(query)
            
            category = result.mappings().first()
            valid_category = CategoriesShop.model_validate(
                obj=category, 
                from_attributes=True
            )
            return valid_category.id
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


async def add_category(category_valid_model: CategoryCreateShop
) -> bool | None:
    """Асинхронная функция для создания категории"""

    try:
        category = Category
        async with get_session(async_engine=async_engine) as async_session:
            query = insert(category).values(
                **category_valid_model.model_dump()
            )
            await async_session.execute(query)
            await async_session.commit()
    except IntegrityError as err:
        orig = err.orig
        
        while hasattr(orig, '__cause__') and orig.__cause__:
            orig = orig.__cause__
        
        if isinstance(orig, UniqueViolationError):
            message_error = message_err.get('dublicate_rec_category').replace(
                'title', 
                category_valid_model.title
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


async def edit_category(category_valid_model: CategoriesShop) -> bool | None:
    """Асинхронная функция для редактирования категории"""

    try:
        category = Category
        async with get_session(async_engine=async_engine) as async_session:
            query = update(category).where(
                category_valid_model.id == category.id
            ).values(**category_valid_model.model_dump())
            
            await async_session.execute(query)
            await async_session.commit()
    except IntegrityError as err:
        orig = err.orig
        
        while hasattr(orig, '__cause__') and orig.__cause__:
            orig = orig.__cause__
        
        if isinstance(orig, UniqueViolationError):
            message_error = message_err.get('dublicate_rec_category').replace(
                'title', 
                category_valid_model.title
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


async def delete_category(category_id: int) -> bool | None:
    """Асинхронная функция для удаления категории"""

    try:
        category = Category
        async with get_session(async_engine=async_engine) as async_session:
            query = delete(category).where(category_id == category.id)

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
