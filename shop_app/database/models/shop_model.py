from uuid import uuid4
from sqlalchemy import ( 
    Integer, 
    String, 
    Text,
    Boolean,
    DateTime,
    func,
    ForeignKey,
    UUID,
    UniqueConstraint
)
from sqlalchemy.orm import DeclarativeBase, relationship, mapped_column, Mapped
from sqlalchemy.ext.declarative import declared_attr
from datetime import datetime
from typing import TypeVar, Generic


class Base(DeclarativeBase):
    """Класс для корректной работы аннотаций"""

    pass


TypeID = TypeVar('TypeID')


class MixinID(Generic[TypeID]):
    @declared_attr
    def id(cls) -> Mapped[TypeID]:
        if cls.__orig_bases__[0].__args__[0] == int:
            return mapped_column(
                Integer,
                primary_key=True,
                autoincrement=True,
                name='id'
            )
        elif cls.__orig_bases__[0].__args__[0] == UUID:
            return mapped_column(
                UUID(as_uuid=True), 
                primary_key=True,
                default=uuid4,
                name='id'
            )
        else:
            raise TypeError("TypeID должен быть int или UUID!")


class Category(MixinID[int], Base):
    """Модель Категория"""

    __tablename__ = 'category'

    title: Mapped[str] = mapped_column(
        String(length=200),
        name='название',
        nullable=False,
        unique=True
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        name='активный',
        default=False,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        name='дата создания',
        default=datetime.now,
        server_default=func.now()
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        name='дата обновления',
        onupdate=func.now()
    )


class Product(MixinID[int], Base):
    """Модель Продукт"""

    __tablename__ = 'product'

    name_image: Mapped[str] = mapped_column(
        String(length=200),
        name='картинка',
        default='default.jpg',
        nullable=False
    )

    title: Mapped[str] = mapped_column(
        String(length=200),
        name='название',
        nullable=True
    )

    description: Mapped[str] = mapped_column(
        Text,
        name='описание',
        nullable=True
    )

    price: Mapped[int] = mapped_column(
        Integer,
        name='цена',
        default=0,
        nullable=False
    )

    name_file: Mapped[str] = mapped_column(
        String(length=255),
        name='имя файла',
        nullable=True
    )

    category_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('category.id', ondelete='CASCADE'),
        name='id категории'
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        name='активный',
        default=False,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        name='дата создания',
        default=datetime.now,
        server_default=func.now()
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        name='дата обновления',
        onupdate=func.now()
    )

    category = relationship(
        'Category', 
        backref='products', 
        cascade="all, delete"
    )

    __table_args__ = (
        UniqueConstraint(
            'название', 
            'id категории', 
            name='unique_title_category'
        ),
    )

class User(MixinID[UUID], Base):
    """Модель Пользователь"""

    __tablename__ = 'user'

    chat_id: Mapped[int] = mapped_column(
        Integer,
        name='id чата',
        nullable=False
    )

    user_name: Mapped[str | None] = mapped_column(
        String(length=200),
        name='никнейм'
    )

    first_name: Mapped[str] = mapped_column(
        String(length=200),
        name='имя',
        nullable=False
    )

    last_name: Mapped[str | None] = mapped_column(
        String(length=200),
        name='фамилия'
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        name='дата создания',
        default=datetime.now,
        server_default=func.now()
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        name='дата обновления',
        onupdate=func.now()
    )
