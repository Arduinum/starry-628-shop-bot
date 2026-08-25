from shop_app.utils.json_config import json_data


def get_message(name: str) -> str:
    """Функция вернёт сообщение"""
    
    message = json_data.get(name)
    
    if message:
        if isinstance(message, list):
            message = "".join(message)
            return message
        return message
    return json_data.get('message_not_found')
