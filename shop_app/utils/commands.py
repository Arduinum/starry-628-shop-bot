from aiogram.types import BotCommand, BotCommandScopeDefault

from shop_app.settings import bot
from shop_app.utils.utils import get_message


async def register_commands():
    commands = [
        BotCommand(
            command='info',
            description=get_message('info_descr')
        ),
        BotCommand(
            command='help',
            description=get_message('help_descr')
        ),
        BotCommand(
            command='menu',
            description=get_message('menu_descr')
        ),
        BotCommand(
            command='paysupport',
            description=get_message('paysupport_descr')
        ),
        BotCommand(
            command='privacy',
            description=get_message('privacy_descr')
        )
    ]

    await bot.set_my_commands(
        commands=commands, 
        scope=BotCommandScopeDefault()  # команды будут доступны всем юзерам
    )
