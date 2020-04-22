"""
Created by 陈辰柄 
datetime:2020/4/15 2:38
Describe:自动映射进行反射
"""

from sqlalchemy.ext.automap import automap_base
from sqlalchemy import inspect

Base = automap_base()

from sqlalchemy import create_engine
from sqlalchemy.sql import select

engine = create_engine('sqlite:///Chinook_Sqlite.sqlite')
mysql_engine = create_engine("mysql+mysqlconnector://root:@localhost:3306/guest", pool_recycle=3600)
Base.prepare(engine, reflect=True)

Base.metadata.create_all(mysql_engine)

Artist = Base.classes.Artist
Album = Base.classes.Album

from sqlalchemy.orm import Session

sqllite_session = Session(engine)
nums = sqllite_session.query(Artist).count()

mysql_session = Session(mysql_engine)


def print_state(object):
    insp = inspect(object)
    for state in ['transient', 'pending', 'persistent', 'detached']:
        print('{:>10}: {}'.format(state, getattr(insp, state)))
    print()


for i in range(0, nums, 100):
    result = sqllite_session.query(Artist).slice(i, i + 100).all()
    for j in result:
        print_state(j)
        sqllite_session.expunge(j)
        insp = inspect(j)
        print_state(j)
        # item=Artist(ArtistId=j.ArtistId,Name=j.Name)
        # print_state(item)
        j._sa_instance_state.transient = True
        j._sa_instance_state.detached = False
        mysql_session.add(j)
        print_state(j)
        mysql_session.commit()
    # try:
    #     mysql_session.commit()
    # except:
    #     print("error")
    #     mysql_session.rollback()
