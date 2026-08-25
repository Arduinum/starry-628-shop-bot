from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.exc import SQLAlchemyError, InvalidRequestError, DBAPIError


from shop_app.settings import settings
from shop_app.utils.logger import logger
from shop_app.utils.errors import message_err


logger.name = __name__


def get_session(async_engine: AsyncEngine) -> AsyncSession:
    """Функция для получения сессии"""

    try:
        # подключаемся к бд асинхронно и создаём сессию
        return async_sessionmaker(
            bind=async_engine, 
            class_=AsyncSession,
            expire_on_commit=False
        )
    except (ConnectionError, TimeoutError, InvalidRequestError, DBAPIError, 
        SQLAlchemyError) as err:
        message = f'{err.__class__.__name__}: {err}'
        logger.error(f'{message} | {message_err.get('get_session_err')}')


async_engine = create_async_engine(settings.db_settings.url_db.unicode_string())
