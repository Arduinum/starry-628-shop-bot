from pydantic import BaseModel


class CategoriesShop(BaseModel):
    """Модель для валидации модели Category для списка категорий"""

    id: int
    title: str
    is_active: bool


class CategoryCreateShop(BaseModel):
    """Модель для валидации модели Category для создания категории"""

    title: str
    is_active: bool


class ProductsShop(BaseModel):
    """Модель для валидации модели Product для списка продуктов"""

    id: int
    title: str
    is_active: bool
    category_id: int


class ProductShop(BaseModel):
    """Модель для валидации модели Product для списка продукта"""

    id: int
    title: str
    description: str | None
    price: int
    name_file: str | None
    name_image: str
    category_id: int
    is_active: bool


class ProductCreateShopAll(BaseModel):
    """Модель для валидации модели Product для списка продукта (все поля)"""

    title: str
    description: str
    price: int
    name_file: str
    name_image: str | None
    category_id: int
    is_active: bool


class ProductCreateShop(BaseModel):
    """Модель для валидации модели Product для создания продукта"""

    title: str
    category_id: int


class UserCreate(BaseModel):
    """Модель для валидации создания User"""

    chat_id: int
    user_name: str | None
    first_name: str
    last_name: str | None
