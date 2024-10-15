import os

from sqlalchemy import ForeignKey, Text, Date, ForeignKey, Integer, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass

class ProductBase(Base):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[int] = mapped_column(Integer)
    count: Mapped[int] = mapped_column(Integer)

    order_item = relationship('OrderItemBase', back_populates='product')

class OrdersBase(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[str] = mapped_column(Date)
    status: Mapped[str] = mapped_column(Text)

    order_item = relationship('OrderItemBase', back_populates='order')

class OrderItemBase(Base):
    __tablename__ = 'order_item'

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey('orders.id'))
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('product.id'))
    count: Mapped[int] = mapped_column(Integer)

    order = relationship('OrdersBase', back_populates='order_item')
    product = relationship('ProductBase', back_populates='order_item')

connection = create_engine(os.environ.get('DATABASE_URL'))
Base.metadata.create_all(connection)