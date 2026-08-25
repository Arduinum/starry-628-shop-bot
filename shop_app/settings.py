from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, PostgresDsn
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties


class ModelConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file = '.env', 
        env_file_encoding='utf-8',
        extra='ignore'
    )


class SettingsDb(ModelConfig):
    """Класс для данных бд"""

    type_and_driver_db: str
    name_db: str
    user_db: str
    password_db: SecretStr
    host_db: str
    port_db: int
    url_db: PostgresDsn | None = None

    def __init__(self, **kwargs):  
        super().__init__(**kwargs)  
        if not self.url_db:  
            self.url_db = PostgresDsn.build(  
                scheme=self.type_and_driver_db,  
                username=self.user_db,  
                password=self.password_db.get_secret_value(),  
                host=self.host_db,  
                port=self.port_db,  
                path=self.name_db,  
            )


class SettingsStorage(ModelConfig):
    """Класс для данных хранилища s3"""

    minio_user: str
    minio_password: str
    host_minio: str
    port_minio_1: int
    port_minio_2: int
    storage_img: str
    storage_file: str
    default_img_url: str


class Settings(SettingsStorage, ModelConfig):
    """Класс для данных конфига"""
    
    db_settings: SettingsDb = SettingsDb()
    token: SecretStr
    admin_id: int
    instant_refund: bool
    max_length_str: int = 32  # для кирилицы
    excel_category_doc_path: str | None = None
    excel_product_doc_path: str | None = None


settings = Settings()

bot = Bot(
    token=settings.token.get_secret_value(), 
    default=DefaultBotProperties(parse_mode='Markdown')
)
