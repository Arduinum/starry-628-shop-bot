from aiogram import Router

from shop_app.handlers import router_handler


router_shop = Router(name=__name__)
router_shop.include_router(router_handler)
