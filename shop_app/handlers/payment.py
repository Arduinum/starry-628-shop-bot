from aiogram.types import (
    LabeledPrice, 
    Message, 
    PreCheckoutQuery,
    CallbackQuery
)
from aiogram.types.input_file import BufferedInputFile
from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.exceptions import TelegramNetworkError
import asyncio
from shop_app.storage.client import s3

from shop_app.keyboards.shop_inline_keyboards import pay_product_inline_keyboard 
from shop_app.database.cruds.category_crud import get_category
from shop_app.database.cruds.product_crud import get_product
from shop_app.settings import bot, settings
from shop_app.utils.state_forms import FileForm
from shop_app.callbacks.callbacks import ProductCallback
from shop_app.utils.utils import get_message
from shop_app.storage.s3_api import add_func_loop, get_file
from shop_app.utils.logger import logger
from shop_app.utils.errors import message_err


logger.name = __name__
router_pay = Router(name=__name__)


@router_pay.callback_query(ProductCallback.filter())
async def product_pay_invoice_callback_action(call: CallbackQuery, 
    state: FSMContext, callback_data: ProductCallback):
    """Обработчик для выставления счёта в stars"""

    product_id = callback_data.product_id
    product = await get_product(product_id=product_id)

    if product:
        category = await get_category(category_id=product.category_id)
        chat_id = call.message.chat.id

        # laber - валюта XTR (stars), amount - стоимость в stars
        prices = [LabeledPrice(
            label='XTR', 
            amount=1 if settings.instant_refund else product.price)]
        
        # переход в нужное состояние
        await state.set_state(FileForm.FILE)

        # обновление данных машины состояний
        await state.update_data(data={'file_name': product.name_file})
        
        file_bytes = await asyncio.gather(
            add_func_loop(get_file, settings.storage_img, product.name_image)
        )
        file_bytes = file_bytes[0]
        input_file = BufferedInputFile(file_bytes, filename=product.name_image)
        await bot.send_photo(chat_id=chat_id, photo=input_file, caption="Фото товара")

        await call.message.answer_invoice(
            title=product.title,
            description='отсутствует' if not product.description \
                else product.description,
            provider_token='',
            prices=prices,
            payload=f'{product.title}-{product.id}',
            currency='XTR',
            reply_markup=pay_product_inline_keyboard(
                product=product,
                category=category,
                chat_id=chat_id
            )
        )
    else:
        await call.message.answer(
            text=get_message('product_not_found')
        )


@router_pay.pre_checkout_query()
async def pre_checkout_handler(pre_checkout_query: PreCheckoutQuery):
    """Обработчик предпроверки оплаты заказа"""
    
    await pre_checkout_query.answer(ok=True)


@router_pay.message(F.successful_payment)
async def success_payment_handler(message: Message, state: FSMContext):  
    """Обработчик успешной покупки"""
    
    paiment_info = message.successful_payment
    paiment_id = paiment_info.telegram_payment_charge_id
    user_id = message.from_user.id

    await message.answer(text=get_message('buy_success'))
    
    # Получаем данные из состояния
    data = await state.get_data()
    file_name = data.get('file_name')
    
    # очищаем машину состояний
    await state.clear()
    
    # получаем файл из хранилища
    file_bytes = await asyncio.gather(
        add_func_loop(get_file, settings.storage_file, file_name))
    file_bytes = file_bytes[0]

    if file_bytes:
        try:
            if settings.instant_refund:
                # возврат средств (для режима разработки)
                await bot.refund_star_payment(
                    user_id=user_id, 
                    telegram_payment_charge_id=paiment_id
                )

            # подготовка и отправка файла
            document = BufferedInputFile(file=file_bytes, filename=file_name)
            await bot.send_document(
                chat_id=user_id, 
                document=document, 
                caption=get_message('here_file')
            )
        except TelegramNetworkError as err:
            # Todo: что делать если у тг будет ошибка сети, а звёзды спишутся?
            # скорее всего это надо как-то в бд отправить и создать задачу на возврат
            message_error = (f'{message_err.get('tg_net_err')} - '
                             f'{err.__class__.__name__}: {err}')
            logger.error(message_error)
    else:
        # если файл отсутствует выполняем автоматический возврат звёзд
        await bot.refund_star_payment(
            user_id=user_id, 
            telegram_payment_charge_id=paiment_id
        )
        
        await message.answer(
            text=get_message('refund_message')
        )
    

@router_pay.message(Command(commands='paysupport'))
async def pay_support_handler(message: Message):  
    """Обработчик, информирующий об условиях возврата средств"""

    await message.answer(  
        text=get_message('refund_info')
    )
