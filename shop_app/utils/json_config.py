from pathlib import Path
import json

from shop_app.utils.logger import logger
from shop_app.utils.errors import message_err

logger.name = __name__


def read_json_as_dict(base_path: str, file_name: str) -> dict:
    """Функция для чтения json документа как dict"""

    try:
        file_path = f'{base_path}/{file_name}'
        with open(file=file_path, mode='r') as file:
            json_read = file.read()
            return json.loads(json_read)
    except FileNotFoundError as err:
        message = (f'{err.__class__.__name__}'
                   f'({message_err.get('not_found_file_err')} {err}')
        logger.error(message)
    except json.decoder.JSONDecodeError as err:
        message = (f'{err.__class__.__name__}'
                   f'{message_err.get('read_file_err')} {err}')
        logger.error(message)
    else:
        return {}


base_path = f'{Path(__file__).resolve().parent.parent}/strings'

info_read = read_json_as_dict(base_path=base_path, file_name='info.json')
warning_read = read_json_as_dict(base_path=base_path, file_name='warning.json')
button_read = read_json_as_dict(base_path=base_path, file_name='button.json')
json_data = info_read | warning_read | button_read


if __name__ == '__main__':
    file_path = f'{Path(__file__).resolve().parent.parent}/strings/info.json'
    json_read = read_json_as_dict(file_path=file_path)
    print(json_read)
    print(json_read.get('start_bot'))
    print("".join(json_read['start']))
