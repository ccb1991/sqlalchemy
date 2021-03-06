"""
Created by 陈辰柄 
datetime:2020/4/15 2:11
Describe:第八章
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Numeric, String, Boolean
from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref, sessionmaker

engine = create_engine('sqlite:///:memory:')
engine2 = create_engine('sqlite:///:memory:')

Session = sessionmaker(bind=engine)
Session2 = sessionmaker(bind=engine2)
session = Session()
session2 = Session2()
Base = declarative_base()


class Cookie(Base):
    __tablename__ = 'cookies'

    cookie_id = Column(Integer, primary_key=True)
    cookie_name = Column(String(50), index=True)
    cookie_recipe_url = Column(String(255))
    cookie_sku = Column(String(55))
    quantity = Column(Integer)
    unit_cost = Column(Numeric(12, 2))

    def __init__(self, cookie_id, name, recipe_url=None, sku=None, quantity=0,
                 unit_cost=0.00):
        self.cookie_id = cookie_id
        self.cookie_name = name
        self.cookie_recipe_url = recipe_url
        self.cookie_sku = sku
        self.quantity = quantity
        self.unit_cost = unit_cost

    def __repr__(self):
        return "Cookie(cookie_name='{self.cookie_name}', " \
               "cookie_recipe_url='{self.cookie_recipe_url}', " \
               "cookie_sku='{self.cookie_sku}', " \
               "quantity={self.quantity}, " \
               "unit_cost={self.unit_cost})".format(self=self)


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer(), primary_key=True)
    username = Column(String(15), nullable=False, unique=True)
    email_address = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    password = Column(String(25), nullable=False)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    def __init__(self, username, email_address, phone, password):
        self.username = username
        self.email_address = email_address
        self.phone = phone
        self.password = password

    def __repr__(self):
        return "User(username='{self.username}', " \
               "email_address='{self.email_address}', " \
               "phone='{self.phone}', " \
               "password='{self.password}')".format(self=self)


class Order(Base):
    __tablename__ = 'orders'
    order_id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey('users.user_id'))
    shipped = Column(Boolean(), default=False)
    user = relationship("User", backref=backref('orders', order_by=order_id))

    def __repr__(self):
        return "Order(user_id={self.user_id}, " \
               "shipped={self.shipped})".format(self=self)


class LineItems(Base):
    __tablename__ = 'line_items'
    line_items_id = Column(Integer(), primary_key=True)
    order_id = Column(Integer(), ForeignKey('orders.order_id'))
    cookie_id = Column(Integer(), ForeignKey('cookies.cookie_id'))
    quantity = Column(Integer())
    extended_cost = Column(Numeric(12, 2))
    order = relationship("Order", backref=backref('line_items', order_by=line_items_id))
    cookie = relationship("Cookie", uselist=False)

    def __repr__(self):
        return "LineItems(order_id={self.order_id}, " \
               "cookie_id={self.cookie_id}, " \
               "quantity={self.quantity}, " \
               "extended_cost={self.extended_cost})".format(self=self)


Base.metadata.create_all(engine)

from sqlalchemy import inspect

cc_cookie = Cookie(1, 'chocolate chip', 'http://some.aweso.me/cookie/recipe.html', 'CC01', 12, 0.50)


def print_status(object):
    insp = inspect(object)

    for state in ['transient', 'pending', 'persistent', 'detached']:
        print('{:>10}: {}'.format(state, getattr(insp, state)))
    print()


print_status(cc_cookie)
session.add(cc_cookie)
print_status(cc_cookie)
session.commit()
print_status(cc_cookie)
session.expunge(cc_cookie)
print_status(cc_cookie)
session2.add(cc_cookie)
print_status(cc_cookie)
