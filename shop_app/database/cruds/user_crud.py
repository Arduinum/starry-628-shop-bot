from sqlalchemy import select, insert
from sqlalchemy.exc import SQLAlchemyError, NoResultFound, OperationalError
from pydantic import ValidationError

from shop_app.database.models.shop_model import User
from shop_app.database.models.validators import UserCreate
from shop_app.database.cruds.main_crud import get_session, async_engine
from shop_app.utils.logger import logger


logger.name = __name__


async def add_user(user_valid_model: UserCreate) -> bool | None:
    """Асинхронная функция для добавления данных пользователя"""

    try:
        user = User
        async with get_session(async_engine=async_engine) as async_session:
            query = insert(user).values(**user_valid_model.model_dump())
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
    except ValidationError as err:
        message = f'{err.__class__.__name__}: {err}'
        logger.error(message)
    else:
        return True


async def check_chat_id(chat_id: int) -> bool | None:
    """Асинхронная функция для проверки chat_id пользователя"""

    try:
        user = User
        async with get_session(async_engine=async_engine) as async_session:
            query = select(user.chat_id).where(chat_id == user.chat_id)
            result = await async_session.execute(query)
            user_with_chat = result.mappings().first()
            
            if user_with_chat:
                return True
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
