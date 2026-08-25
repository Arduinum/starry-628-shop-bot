message_err = {
    'not_found_file_dir_err': 'Не найден файл или папка',
    'not_found_file_err': 'Файл не найден',
    'read_file_err': 'Ошибка чтения файла',
    'tg_net_err': 'Ошибка сети telegram',
    'atrr_not_exists_err': 'Атрибута не существует',
    'backet_exists_err': 'Бакет уже существует',
    'file_not_found_backet_err': 'файл не найден в bucket',
    'file_exists_not_rewrite_err': 'файл существует и не будет перезаписан',
    'name_backet_err': 'Ошибка имени backet',
    'field_doc_empty': ('Поле в одном из рядов документа "doc_name" пустое! '
                        'Исправьте документ и повторите попытку.'),
    'excel_doc_not_found': 'Файл excel не был найден',
    'dublicate_rec_product': ('Запись "title" с id категории "category_id"'
                              ' уже существует в базе данных!'),
    'dublicate_rec_category': 'Категория "title" уже существует в базе данных!',
    'get_session_err': 'Не удалось создать сессию'
}

class EmptyFieldError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
