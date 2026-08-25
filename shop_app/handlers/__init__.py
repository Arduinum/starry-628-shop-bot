from aiogram import Router

from shop_app.handlers.admin_commands import router_admin
from shop_app.handlers.info_commands import router_info
from shop_app.handlers.menu import router_menu
from shop_app.handlers.payment import router_pay
from shop_app.handlers.shop_commands import router_shop


router_handler = Router(name=__name__)
router_handler.include_routers(
    router_admin,
    router_info,
    router_menu,
    router_pay,
    router_shop
)
