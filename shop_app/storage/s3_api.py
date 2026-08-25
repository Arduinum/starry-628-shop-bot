import asyncio
from botocore.exceptions import ClientError
from boto3.exceptions import S3UploadFailedError
from typing import Any, Awaitable

from shop_app.utils.logger import logger
from shop_app.storage.client import s3
from shop_app.utils.errors import message_err


logger.name = __name__


async def add_func_loop(func, *args) -> Awaitable[Any]: 
    """Асинхронная функция для добавления функции в отдельный поток""" 
    
    loop = asyncio.get_event_loop() 
    result = await loop.run_in_executor(None, func, *args)
    return result


def create_bucket(name_bucket: str) -> bool | None:
    """Функция для отправки api запроса на создание bucket"""

    try: 
        s3.create_bucket(Bucket=name_bucket)
    except ClientError as err:
        if err.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
            message = (f"{message_err.get('backet_exists_err')} - "
                       f"{err.__class__.__name__}: {err}")
            logger.error(message)
    except AttributeError as err:
        message = (f"{message_err.get('atrr_not_exists_err')} - "
                   f"{err.__class__.__name__}: {err}")
        logger.error(message)
    else:
        return True


def get_file(name_bucket: str, name_file: str) -> None | bytes:
    """Функция для получения файла в байтах из bucket"""

    try:
        s3.head_object(Bucket=name_bucket, Key=name_file)
        response = s3.get_object(Bucket=name_bucket, Key=name_file)
        file = response['Body'].read()  # сохраняем файл в озу
        return file
    except ClientError as err:
        if err.response['Error']['Code'] == '404': 
            message = (f"{name_file} "
                       f"{message_err.get('file_not_found_backet_err')} "
                       f"{name_bucket} - {err.__class__.__name__}: {err}")
            logger.error(message)
    except AttributeError as err:
        message = (f"{message_err.get('atrr_not_exists_err')} - "
                   f"{err.__class__.__name__}: {err}")
        logger.error(message)


def upload_file(file: bytes, name_bucket: str, name_file: str) -> bool | None:
    """Функция для загрузки файла в bucket"""

    try: 
        s3.put_object(
            Bucket=name_bucket, 
            Key=name_file, 
            Body=file, 
            IfNoneMatch='*' # загрузит если файл не существует
        )
    except ClientError as err: 
        if err.response['Error']['Code'] == 'PreconditionFailed': 
            message = (f"{name_file} "
                       f"{message_err.get('file_exists_not_rewrite_err')}"
                       f" - {err.__class__.__name__}: {err}")
            logger.error(message)
    except FileNotFoundError as err:
        message = (f"{message_err.get('not_found_file_err')} - "
                   f"{err.__class__.__name__}: {err}")
        logger.error(message)
    except S3UploadFailedError as err:
        message = (f"{message_err.get('name_backet_err')} - "
                   f"{err.__class__.__name__}: {err}")
        logger.error(message)
    except AttributeError as err:
        message = (f"{message_err.get('atrr_not_exists_err')} - "
                   f"{err.__class__.__name__}: {err}")
        logger.error(message)
    else:
        return True


def delete_file(name_bucket: str, name_file: str) -> bool | None:
    """Функция для удаления файла из bucket"""

    try:
        s3.head_object(Bucket=name_bucket, Key=name_file)
        s3.delete_object(Bucket=name_bucket, Key=name_file)
    except ClientError as err: 
        if err.response['Error']['Code'] == '404': 
            message = (f"{name_file} "
                       f"{message_err.get('file_not_found_backet_err')} "
                       f"{name_bucket} - {err.__class__.__name__}: {err}")
            logger.error(message)
    except AttributeError as err:
        message = (f"{message_err.get('atrr_not_exists_err')} - "
                   f"{err.__class__.__name__}: {err}")
        logger.error(message)
    else:
        return True
