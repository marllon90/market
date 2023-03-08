import uuid
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (Column, DateTime, Float, ForeignKey, Integer, String,
                        Text, create_engine)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

import config

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), default=uuid.uuid4(), primary_key=True)
    username = Column(String(64), unique=True)
    email = Column(String(64), unique=True)
    name = Column(String(64))
    city = Column(String(128))
    province = Column(String(128))
    country = Column(String(128))
    address = Column(String(256))
    zip_code = Column(String(16))
    phone = Column(String(16))
    order = relationship('Order', cascade='all,delete', backref='users')

    def __repr__(self):
        return '<User: {}>'.format(self.username)


class Order(Base):
    __tablename__ = 'orders'

    id = Column(UUID(as_uuid=True), default=uuid.uuid4(), primary_key=True)
    user = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    order_date = Column(DateTime, default=datetime.utcnow)
    order_detail = relationship('OrderDetail', cascade='all,delete', backref='orders')


class Product(Base):
    __tablename__ = 'products'

    id = Column(UUID(as_uuid=True), default=uuid.uuid4(), primary_key=True)
    name = Column(String(128))
    sku = Column(String(32))
    price = Column(Float)
    image_url = Column(String(2048), default='https://picsum.photos/200/300')
    description = Column(Text)
    order_detail = relationship('OrderDetail', cascade='all,delete', backref='products')


class OrderDetail(Base):
    __tablename__ = 'orderdetails'

    id = Column(UUID(as_uuid=True), default=uuid.uuid4(), primary_key=True)
    order = Column(UUID(as_uuid=True), ForeignKey('orders.id'), nullable=False)
    product = Column(UUID(as_uuid=True), ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer)
    total_price = Column(Float)


if __name__ == "__main__":
    engine = create_engine(config.Development.SQLALCHEMY_DATABASE_URI)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
