from aiogram.fsm.state import State, StatesGroup


class FileForm(StatesGroup):
    """Класс форма для файла"""
    
    FILE = State()


class EditCategoryForm(StatesGroup):
    """Класс форма для редактирования категории"""
    
    FIELDS = State()


class CreateCategoryForm(StatesGroup):
    """Класс форма для создания категории"""
    
    FIELDS = State()


class CreateProductForm(StatesGroup):
    """Класс форма для создания продукта"""
    
    FIELDS = State()


class EditProductForm(StatesGroup):
    """Класс форма для редактирования продукта"""
    
    FIELDS = State()


# создать форму для загрузки файла, а то она конфликтует с формой редактирования файла!!!!