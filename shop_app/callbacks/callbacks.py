from aiogram.filters.callback_data import CallbackData

from shop_app.settings import settings


class CategoriesCallback(CallbackData, prefix='categories'):
    """
    Класс для связи с кнопкой и функцией ответа для кнопки Категории
    """
    
    page: int | None = None


class CategoryCallback(CallbackData, prefix='category'):
    """
    Класс для связи с кнопкой и функцией ответа для кнопки Категория
    """
    
    category_id: int | None = None
    title: str | None = None
    page: int | None = None


class CategoryEditCallback(CallbackData, prefix='category_edit'):
    """
    Класс для связи с кнопкой и функцией ответа для кнопки 
    Редактировать категорию
    """

    category_id: int


class CategoryEditFieldsCallback(CallbackData, prefix='category_edit_fields'):
    """
    Класс для связи с кнопкой и функцией ответа для кнопки Редактировать 
    поля категории
    """

    category_id: int
    title: str | None = None
    is_active: bool | None = None


class CategoryCreateCallback(CallbackData, prefix='category_create'):
    """
    Класс для связи с кнопкой и функцией ответа для кнопки 
    Создать категорию 
    """

    pass


class CategoryCreateFieldCallback(CallbackData, prefix='category_create_field'):
    """
    Класс для связи с кнопкой и функцией ответа для кнопки Редактировать 
    поля категории
    """

    title: str


class CategoryDeleteCallback(CallbackData, prefix='category_delete'):
    """
    Класс для связи с кнопкой и функцией ответа для кнопки Удалить 
    категорию
    """

    category_id: int


class CategoryDeleteCrudCallback(CallbackData, prefix='delete_category_crud'):
    """
    Класс для связи с кнопкой и функцией ответа для кнопки Удалить 
    категорию c crud операцией
    """

    category_id: int


class ProductCallback(CallbackData, prefix='product'):
    """
    Класс для связи с кнопкой и функцией ответа для кнопки Продукты
    """
    
    product_id: int | None = None
    title: str | None = None


class ProductCreateCallback(CallbackData, prefix='product_create'):
    """
    Класс для связи с кнопкой и функцией ответа для кнопки 
    Создать продукт
    """

    category_id: int


class ProductCreateFieldCallback(CallbackData, prefix='product_create_field'):
    """
    Класс для связи с кнопкой и функцией ответа для кнопки Создать 
    поля категории
    """

    title: str
    category_id: int


class ProductEditCallback(CallbackData, prefix='product_edit'):
    """
    Класс для связи с кнопкой и функцией ответа для кнопки 
    Редактировать продукт
    """

    product_id: int


class ProductEditFieldsCallback(CallbackData, prefix='product_edit_fields'):
    """
    Класс для связи с кнопкой и функцией ответа для кнопки Редактировать 
    поля продукта
    """

    product_id: int
    title: str | None = None
    description: str | None = None
    price: int | None = None
    name_file: str | None = None
    is_active: bool | None = None
    category_id: int | None = None

    @classmethod
    def truncate_str(cls, field: str):
        """Метод для уменьшения размера строки поля"""

        if len(field) > settings.max_length_str:
            max_length = settings.max_length_str - 3
            return f"{field[:max_length]}..."
        return field

    def truncate_fields(self):
        """Метод для уменьшения размера строк полей"""

        if self.description:
            self.description = self.truncate_str(field=self.description)
        return self


class ProductDeleteCallback(CallbackData, prefix='product_delete'):
    """
    Класс для связи с кнопкой и функцией ответа для кнопки Удалить 
    продукт
    """

    product_id: int


class ProductDeleteCrudCallback(CallbackData, prefix='delete_product_crud'):
    """
    Класс для связи с кнопкой и функцией ответа для кнопки Удалить 
    продукт c crud операцией
    """

    product_id: int


class PopUpCallback(CallbackData, prefix='pop_up'):
    """
    Класс для связи с кнопкой и функцией ответа для кнопок всплывающих 
    уведомлений
    """

    text: str


class MainMenuCallback(CallbackData, prefix='shop_menu'):
    """
    Класс для связи с кнопкой и функцией ответа для кнопки Меню магазина
    """

    pass
