from aiogram import Dispatcher
from aiogram.methods import DeleteWebhook
from asyncio import run

from shop_app.utils.commands import register_commands
from shop_app.settings import bot
from shop_app import router_shop


async def start():
    """Асинхронная функция запуска бота"""
    
    # диспетчер для бота
    dp = Dispatcher()

    # подключение роутера к диспетчеру
    dp.include_routers(
        router_shop
    )

    try:
        # регистрируем меню с командами
        await register_commands()

        # удаляем веб хук и непрочитанные обновления
        await bot(DeleteWebhook(drop_pending_updates=True))
        
        # периодическая проверка новых команд от пользователя
        await dp.start_polling(bot)
    finally:
        # ждём завершения сессии
        await bot.session.close()


def main():
    """Главная функция запуска бота"""

    try:
        run(start())
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    try:
        run(start())
    except KeyboardInterrupt:
        pass
